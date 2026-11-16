// Feed Flow site chat: POST /api/chat (SSE answer). No dependencies, stores nothing.
// Cloudflare Pages Function logic. functions/api/chat/index.js is the route; this file is not.
//
// Events the widget reads: delta {text} · action {type:'hand_over', to, reason, summary} · done {tier, model} · error {code, message}

import { KNOWLEDGE } from './knowledge.js';
import { buildSystemPrompt } from './prompt.js';
import { explainTier, interpretToolCalls, modelsFor, toolsFor } from './router.js';
import { CHAT_PER_HOUR, withinLimit } from './ratelimit.js';

export const LIMITS = {
  BODY_BYTES: 16 * 1024,
  MESSAGE_CHARS: 1000,
  USER_TURNS: 12,
  UPSTREAM_MESSAGES: 8,
  MAX_TOKENS: 350,
  UPSTREAM_TIMEOUT_MS: 25_000,
  PAGE_CHARS: 200,
  SESSION_SECONDS: 30 * 60,
};

const PROD_ORIGINS = ['https://tryfeedflow.app', 'https://www.tryfeedflow.app'];
const DEV_ORIGIN = /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/;
const PAGES_ORIGIN = /^https:\/\/[a-z0-9-]+(\.[a-z0-9-]+)*\.pages\.dev$/;
const DEFAULT_BASE_URL = 'https://openrouter.ai/api/v1';
const SESSION_COOKIE = 'ffchat';

const ERRORS = {
  not_configured: [503, 'Chat is not switched on here. Write to support@tryfeedflow.app instead.'],
  rate_limited: [429, 'You’re sending messages quickly. Please wait a while and try again.'],
  too_long: [413, 'That message is a bit long. Please keep it under 1,000 characters.'],
  bot_check: [403, 'We couldn’t confirm you’re a person. Please reload the page and try again.'],
  upstream: [502, 'I can’t answer right now. Please try again in a moment, or email support@tryfeedflow.app.'],
  bad_request: [400, 'That request didn’t look right. Please reload the page and try again.'],
};

const LIMIT_REACHED_TEXT =
  'We’ve covered a lot in this chat. To keep going, leave your email below and the team will write back.';
const HAND_OVER_FALLBACK = {
  founder: 'I’ll pass this on to Robin. Leave your email in the form below and Robin will write back.',
  support: 'I’ll pass this to support. Leave your email in the form below and they’ll write back.',
};

const FORM_STILL_OPEN = 'The form above is still open. It’s there whenever it suits.';
const SMILEYS = /[\u{1F600}-\u{1F64F}\u{1F44D}\u{263A}]\uFE0F?/gu;

// Cleans a streamed reply: no smiley in the first reply of a chat, and a model that writes its
// answer twice in one stream (seen with the fast chain) is cut at the repeat.
export function createReplyFilter({ firstReply = false } = {}) {
  let sent = '';
  let held = '';
  let cut = false;
  const clean = (t) => (firstReply ? t.replace(SMILEYS, '') : t);
  const opening = () => sent.replace(/\s+/g, ' ').slice(0, 24);
  return {
    push(text) {
      if (cut) return '';
      held += text;
      const at = held.lastIndexOf('\n\n');
      // Text before the last paragraph break is safe unless that paragraph repeats the opening.
      let out = '';
      const parts = held.split(/\n\n+/);
      const breaks = held.match(/\n\n+/g) || [];
      held = '';
      for (let i = 0; i < parts.length; i++) {
        const para = parts[i];
        const last = i === parts.length - 1;
        const startsNew = i > 0 || /\n\n\s*$/.test(sent + out) || (sent + out) === '';
        const isRepeat = (sent + out).length >= 24 && startsNew && para.replace(/\s+/g, ' ').trimStart().startsWith(opening().slice(0, 24)) && opening().length >= 24;
        if (isRepeat) { cut = true; break; }
        if (!last && para && !/[\p{L}\p{N}]/u.test(para)) continue; // a stray comma on its own line
        if (last && startsNew && (sent + out).length >= 24 && para.replace(/\s+/g, ' ').trimStart().length < 24) { held = para; break; } // wait until it can be judged
        out += para + (last ? '' : breaks[i]);
      }
      void at;
      out = clean(out);
      sent += out;
      return out;
    },
    end() {
      if (cut) return '';
      const out = clean(held);
      held = '';
      sent += out;
      return out;
    },
  };
}

const isDev = (env) => env?.ENV === 'dev';

function jsonError(code, extraHeaders, status) {
  const [defaultStatus, message] = ERRORS[code];
  return new Response(JSON.stringify({ code, message }), {
    status: status ?? defaultStatus,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extraHeaders },
  });
}

class RequestError extends Error {
  constructor(code, status) {
    super(code);
    this.code = code;
    this.status = status;
  }
}

// ---------- entry point ----------

export async function handleChat({ request, env, waitUntil }) {
  try {
    if (request.method !== 'POST') return jsonError('bad_request', { Allow: 'POST' }, 405);
    if (!env?.OPENROUTER_API_KEY) return jsonError('not_configured'); // before anything else: the widget falls back to its form
    if (!originAllowed(request, env)) return jsonError('bad_request', {}, 403);
    if (!(await withinLimit(request, 'chat', CHAT_PER_HOUR))) return jsonError('rate_limited');
    const body = await readJson(request);
    return await streamAnswer(request, env, waitUntil, body);
  } catch (err) {
    if (err instanceof RequestError) return jsonError(err.code, {}, err.status);
    console.error('chat: unexpected', err?.name || 'Error'); // never the message content
    return jsonError('upstream');
  }
}

// ---------- guards ----------

export function originAllowed(request, env) {
  const origin = request.headers.get('Origin');
  if (!origin) return isDev(env); // browsers always send Origin on a same-origin POST
  if (PROD_ORIGINS.includes(origin)) return true;
  if (PAGES_ORIGIN.test(origin)) return true; // preview deployments
  return isDev(env) && DEV_ORIGIN.test(origin);
}

async function readJson(request) {
  const declared = Number(request.headers.get('Content-Length'));
  if (declared > LIMITS.BODY_BYTES) throw new RequestError('too_long', 413);
  const chunks = [];
  let total = 0;
  if (request.body) {
    const reader = request.body.getReader();
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > LIMITS.BODY_BYTES) {
        reader.cancel().catch(() => {});
        throw new RequestError('too_long', 413);
      }
      chunks.push(value);
    }
  }
  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const c of chunks) {
    bytes.set(c, offset);
    offset += c.byteLength;
  }
  try {
    const parsed = JSON.parse(new TextDecoder().decode(bytes));
    if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('shape');
    return parsed;
  } catch {
    throw new RequestError('bad_request', 400);
  }
}

function cleanPage(page) {
  return typeof page === 'string' ? page.slice(0, LIMITS.PAGE_CHARS) : '';
}

function cleanToken(token) {
  return typeof token === 'string' && token.length > 0 && token.length <= 2048 ? token : null;
}

/** Returns the validated, trimmed conversation or throws RequestError. */
export function validateMessages(raw) {
  if (!Array.isArray(raw) || raw.length === 0 || raw.length > 60) throw new RequestError('bad_request', 400);
  const out = [];
  for (const m of raw) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant') || typeof m.content !== 'string') {
      throw new RequestError('bad_request', 400);
    }
    let content = m.content.trim();
    if (!content) throw new RequestError('bad_request', 400);
    if (content.length > LIMITS.MESSAGE_CHARS) {
      // A visitor's own message that is too long is rejected. Our own earlier
      // replies can run a little long, so those are trimmed instead.
      if (m.role === 'user') throw new RequestError('too_long', 413);
      content = content.slice(0, LIMITS.MESSAGE_CHARS);
    }
    out.push({ role: m.role, content });
  }
  if (out[out.length - 1].role !== 'user') throw new RequestError('bad_request', 400);
  return out;
}

// ---------- Turnstile (OFF unless TURNSTILE_SECRET is set) + stateless session cookie ----------
// Turnstile tokens are single use, so only the first message can carry one. A
// verified visitor gets a signed 30-minute cookie (needs CHAT_SESSION_SECRET).
// With no TURNSTILE_SECRET none of this runs: the money ceiling is the hard limit
// on the OpenRouter key plus the per-IP counter.

const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
const unhex = (s) => new Uint8Array(s.match(/../g)?.map((h) => parseInt(h, 16)) || []);

async function hmacKey(secret, usage) {
  return crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, [usage]);
}

async function signSession(secret, expires) {
  const sig = await crypto.subtle.sign('HMAC', await hmacKey(secret, 'sign'), new TextEncoder().encode(`ffchat.${expires}`));
  return `${expires}.${hex(sig)}`;
}

async function sessionValid(request, env) {
  if (!env.CHAT_SESSION_SECRET) return false;
  const cookie = (request.headers.get('Cookie') || '').split(';').map((c) => c.trim()).find((c) => c.startsWith(`${SESSION_COOKIE}=`));
  if (!cookie) return false;
  const [expires, sig] = cookie.slice(SESSION_COOKIE.length + 1).split('.');
  if (!expires || !sig || !(Number(expires) > Date.now() / 1000) || !/^[0-9a-f]{64}$/.test(sig)) return false;
  try {
    return await crypto.subtle.verify('HMAC', await hmacKey(env.CHAT_SESSION_SECRET, 'verify'), unhex(sig), new TextEncoder().encode(`ffchat.${expires}`));
  } catch {
    return false;
  }
}

async function verifyTurnstile(env, token, request) {
  if (!token) return false;
  try {
    const form = new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token });
    const ip = request.headers.get('CF-Connecting-IP');
    if (ip) form.set('remoteip', ip);
    const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    if (!res.ok) return false;
    return (await res.json()).success === true;
  } catch {
    return false; // fail closed
  }
}

/** Returns extra response headers (a Set-Cookie when a session was minted) or throws bot_check. */
async function botCheck(request, env, token, firstMessage) {
  if (!env.TURNSTILE_SECRET) return {}; // check is off
  if (await sessionValid(request, env)) return {};
  if (!firstMessage && !env.CHAT_SESSION_SECRET) return {}; // weaker mode
  if (!(await verifyTurnstile(env, token, request))) throw new RequestError('bot_check', 403);
  if (!env.CHAT_SESSION_SECRET) return {};
  const expires = Math.floor(Date.now() / 1000) + LIMITS.SESSION_SECONDS;
  const secure = new URL(request.url).protocol === 'https:' ? '; Secure' : '';
  return {
    'Set-Cookie': `${SESSION_COOKIE}=${await signSession(env.CHAT_SESSION_SECRET, expires)}; Path=/api/chat; Max-Age=${LIMITS.SESSION_SECONDS}; HttpOnly; SameSite=Strict${secure}`,
  };
}

// ---------- chat ----------

const sseFrame = (event, data) => `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;

async function streamAnswer(request, env, waitUntil, body) {
  const messages = validateMessages(body.messages);
  const page = cleanPage(body.page);
  const sessionHeaders = await botCheck(request, env, cleanToken(body.turnstileToken), messages.length === 1);

  const { readable, writable } = new TransformStream();
  const writer = writable.getWriter();
  const encoder = new TextEncoder();
  const abort = new AbortController();
  let open = true;
  const send = async (event, data) => {
    if (!open) return;
    try {
      await writer.write(encoder.encode(sseFrame(event, data)));
    } catch {
      open = false; // the visitor went away: stop spending money
      abort.abort();
    }
  };

  const run = (async () => {
    try {
      if (messages.filter((m) => m.role === 'user').length > LIMITS.USER_TURNS) {
        await send('delta', { text: LIMIT_REACHED_TEXT });
        await send('action', { type: 'hand_over', to: 'support', reason: 'request', summary: 'Conversation length limit reached.' });
        await send('done', { tier: 'fast' });
        return;
      }
      await answer({ env, messages, page, send, signal: abort.signal });
    } catch (err) {
      console.error('chat: failed', JSON.stringify({ name: err?.name, status: err?.status }));
      await send('error', { code: 'upstream', message: ERRORS.upstream[1] });
    } finally {
      await writer.close().catch(() => {});
    }
  })();
  waitUntil?.(run);

  return new Response(readable, {
    headers: {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Accel-Buffering': 'no',
      ...sessionHeaders,
    },
  });
}

async function answer({ env, messages, page, send, signal }) {
  const { tier: chosen, reason } = explainTier(messages);
  const upstreamMessages = lastUpstreamMessages(messages);
  let tier = chosen;
  let result = await callUpstream({ env, tier, page, upstreamMessages, send, signal });
  let { handOver } = interpretToolCalls(result.toolCalls);

  // The fast chain asked for more brainpower before saying anything, or came back with nothing at all
  // (a model that spent its whole budget thinking): one rerun on the strong chain, never a loop.
  if (tier === 'fast' && !result.emitted && !handOver) {
    tier = 'strong';
    result = await callUpstream({ env, tier, page, upstreamMessages, send, signal });
    ({ handOver } = interpretToolCalls(result.toolCalls));
  }
  if (!result.emitted && !handOver) throw new Error('empty answer'); // the widget shows its error / form, never a blank bubble

  // The form from the previous reply is still on screen: never show the hand-over line twice in a row.
  const previous = [...messages].reverse().find((m) => m.role === 'assistant');
  if (handOver && previous && /form (below|above)/i.test(previous.content || '')) {
    if (!result.emitted) await send('delta', { text: FORM_STILL_OPEN });
    handOver = null;
  }
  if (handOver) {
    if (!result.emitted) await send('delta', { text: HAND_OVER_FALLBACK[handOver.to] || HAND_OVER_FALLBACK.support });
    await send('action', handOver);
  }
  const model = result.model || null;
  console.log(JSON.stringify({ evt: 'chat', tier, routed: reason, model, in: result.usage?.prompt_tokens, out: result.usage?.completion_tokens }));
  await send('done', { tier, model });
}

function lastUpstreamMessages(messages) {
  const tail = messages.slice(-LIMITS.UPSTREAM_MESSAGES);
  while (tail.length && tail[0].role !== 'user') tail.shift();
  return tail;
}

export function buildPayload({ env, tier, page, upstreamMessages }) {
  return {
    models: modelsFor(env, tier),
    stream: true,
    stream_options: { include_usage: true },
    max_tokens: LIMITS.MAX_TOKENS,
    reasoning: { enabled: false }, // a reasoning model otherwise spends the whole 350 tokens thinking and answers with nothing
    messages: [{ role: 'system', content: buildSystemPrompt({ knowledge: KNOWLEDGE, page, tier }) }, ...upstreamMessages],
    tools: toolsFor(tier),
  };
}

async function callUpstream({ env, tier, page, upstreamMessages, send, signal }) {
  const filter = createReplyFilter({ firstReply: !upstreamMessages.some((m) => m.role === 'assistant') });
  const base = (env.AI_GATEWAY_URL || DEFAULT_BASE_URL).replace(/\/+$/, '');
  const payload = buildPayload({ env, tier, page, upstreamMessages });
  const headers = {
    Authorization: `Bearer ${env.OPENROUTER_API_KEY}`,
    'Content-Type': 'application/json',
    'HTTP-Referer': 'https://tryfeedflow.app',
    'X-Title': 'Feed Flow site chat',
  };
  if (env.AI_GATEWAY_TOKEN) headers['cf-aig-authorization'] = `Bearer ${env.AI_GATEWAY_TOKEN}`;

  const timeout = new AbortController();
  const timer = setTimeout(() => timeout.abort(), LIMITS.UPSTREAM_TIMEOUT_MS);
  const onOuterAbort = () => timeout.abort();
  signal?.addEventListener('abort', onOuterAbort);

  const toolCalls = [];
  let emitted = false;
  let started = false;
  let usage = null;
  let model = null;
  try {
    const res = await fetch(`${base}/chat/completions`, { method: 'POST', headers, body: JSON.stringify(payload), signal: timeout.signal });
    if (!res.ok || !res.body) {
      const err = new Error('upstream status');
      err.status = res.status;
      throw err;
    }
    for await (const data of parseSSE(res.body)) {
      let chunk;
      try {
        chunk = JSON.parse(data);
      } catch {
        continue;
      }
      if (chunk.error) throw new Error('upstream stream error');
      if (chunk.usage) usage = chunk.usage;
      if (typeof chunk.model === 'string' && chunk.model) model = chunk.model;
      const delta = chunk.choices?.[0]?.delta;
      if (!delta) continue;
      if (typeof delta.content === 'string' && delta.content) {
        let text = delta.content;
        if (!started) {
          text = text.replace(/^\s+/, ''); // never open an answer with blank space
          if (!text) continue;
          started = true;
        }
        text = filter.push(text);
        if (!text) continue;
        emitted = true;
        await send('delta', { text });
      }
      for (const tc of delta.tool_calls || []) {
        const entry = (toolCalls[tc.index ?? 0] ||= { name: '', arguments: '' });
        if (tc.function?.name && !entry.name) entry.name = tc.function.name;
        if (tc.function?.arguments) entry.arguments += tc.function.arguments;
      }
    }
    const rest = filter.end();
    if (rest.trim()) {
      emitted = true;
      await send('delta', { text: rest });
    }
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener('abort', onOuterAbort);
  }
  return { emitted, toolCalls: toolCalls.filter(Boolean), usage, model };
}

/** Yields the data payload of each SSE event. Ignores comments; stops at [DONE]. */
export async function* parseSSE(body) {
  const reader = body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  const events = function* (final) {
    let idx;
    while ((idx = buffer.search(/\r?\n\r?\n/)) !== -1) {
      const block = buffer.slice(0, idx);
      buffer = buffer.slice(idx).replace(/^\r?\n\r?\n/, '');
      yield block;
    }
    if (final && buffer.trim()) {
      yield buffer;
      buffer = '';
    }
  };
  const dataOf = (block) =>
    block
      .split(/\r?\n/)
      .filter((l) => l.startsWith('data:'))
      .map((l) => l.slice(5).replace(/^ /, ''))
      .join('\n');
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (value) buffer += decoder.decode(value, { stream: !done });
      for (const block of events(done)) {
        const data = dataOf(block);
        if (!data) continue;
        if (data.trim() === '[DONE]') return;
        yield data;
      }
      if (done) return;
    }
  } finally {
    reader.cancel().catch(() => {});
  }
}
