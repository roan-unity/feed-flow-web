/* POST /api/chat/escalate: emails a visitor's message from the site chat to support or to the founder.
   Cloudflare Pages Function, no dependencies. Secrets: RESEND_API_KEY (required to send), ESCALATION_FROM (optional),
   FOUNDER_EMAIL (optional, where `to: "founder"` goes; falls back to support).
   Nothing about the message or the visitor's address is ever logged. */

import { FORM_PER_HOUR, withinLimit } from '../../_chat/ratelimit.js';

const SUPPORT_ADDRESS = 'support@tryfeedflow.app';
const DEFAULT_FROM = 'Feed Flow site <chat@tryfeedflow.app>';
const EMAIL_RE = /^[^\s@<>"',;:\\()[\]]+@[^\s@<>"',;:\\()[\]]+\.[^\s@<>"',;:\\()[\]]+$/;
const LIMITS = { BODY_BYTES: 16 * 1024, EMAIL_CHARS: 254, MESSAGE_CHARS: 1000, PAGE_CHARS: 200, TRANSCRIPT_MESSAGES: 60, MAIL_TRANSCRIPT: 8, MIN_FILL_MS: 2500 };
const REASONS = ['billing', 'bug', 'account', 'request', 'unknown', 'feedback', 'important', 'medical'];
const TARGETS = ['support', 'founder'];
const ALLOWED_ORIGINS = ['https://tryfeedflow.app', 'https://www.tryfeedflow.app'];

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}
function fail(status, code, message) {
  console.log(`escalate: ${status} ${code}`);
  return json(status, { code, message });
}

function originAllowed(origin, env) {
  if (!origin) return false;
  if (ALLOWED_ORIGINS.includes(origin)) return true;
  let url;
  try {
    url = new URL(origin);
  } catch {
    return false;
  }
  if (url.protocol === 'https:' && url.origin === origin && url.hostname.endsWith('.pages.dev')) return true;
  if (env && env.ENV === 'dev' && url.protocol === 'http:' && (url.hostname === 'localhost' || url.hostname === '127.0.0.1')) return true;
  return false;
}

export function renderTranscript(transcript) {
  return transcript.map((m) => `${m.role === 'user' ? 'Visitor' : 'Nora'}: ${m.content}`).join('\n\n');
}

export async function onRequestPost({ request, env }) {
  if (!originAllowed(request.headers.get('Origin'), env)) {
    return fail(403, 'forbidden', 'This request did not come from the Feed Flow site.');
  }
  if (!(await withinLimit(request, 'form', FORM_PER_HOUR))) {
    return fail(429, 'rate_limited', 'That is a lot of messages for now. Try again in a while, or write to ' + SUPPORT_ADDRESS + '.');
  }

  const declared = Number(request.headers.get('Content-Length') || 0);
  if (declared > LIMITS.BODY_BYTES) return fail(413, 'too_long', 'That message is too long.');
  let raw;
  try {
    raw = await request.text();
  } catch {
    return fail(400, 'bad_request', 'We could not read that message.');
  }
  if (new TextEncoder().encode(raw).length > LIMITS.BODY_BYTES) return fail(413, 'too_long', 'That message is too long.');
  let body;
  try {
    body = JSON.parse(raw);
  } catch {
    return fail(400, 'bad_request', 'We could not read that message.');
  }
  if (!body || typeof body !== 'object' || Array.isArray(body)) return fail(400, 'bad_request', 'We could not read that message.');

  const email = typeof body.email === 'string' ? body.email.trim() : '';
  if (!email || email.length > LIMITS.EMAIL_CHARS || !EMAIL_RE.test(email)) {
    return fail(400, 'bad_email', "That email doesn't look right.");
  }
  const question = typeof body.question === 'string' ? body.question.trim() : '';
  if (!question) return fail(400, 'bad_request', 'Write a short message first.');
  if (question.length > LIMITS.MESSAGE_CHARS) return fail(413, 'too_long', 'That message is too long. Shorten it and send it again.');

  let page = '';
  if (body.page !== undefined && body.page !== null) {
    if (typeof body.page !== 'string' || body.page.length > LIMITS.PAGE_CHARS) return fail(400, 'bad_request', 'We could not read that message.');
    page = body.page;
  }
  const reason = REASONS.includes(body.reason) ? body.reason : 'request';
  const to = TARGETS.includes(body.to) ? body.to : 'support';
  const summary = typeof body.summary === 'string' ? body.summary.trim().slice(0, 300) : '';

  const transcript = [];
  if (body.transcript !== undefined && body.transcript !== null) {
    if (!Array.isArray(body.transcript) || body.transcript.length > LIMITS.TRANSCRIPT_MESSAGES) {
      return fail(400, 'bad_request', 'We could not read that message.');
    }
    for (const m of body.transcript) {
      if (!m || (m.role !== 'user' && m.role !== 'assistant') || typeof m.content !== 'string') {
        return fail(400, 'bad_request', 'We could not read that message.');
      }
      transcript.push({ role: m.role, content: m.content.slice(0, LIMITS.MESSAGE_CHARS) });
    }
  }

  // Spam guards that need no secrets. Both answer as if it worked, so a bot learns nothing.
  if (typeof body.company === 'string' && body.company.trim() !== '') {
    console.log('escalate: 200 dropped honeypot');
    return json(200, { ok: true });
  }
  if (typeof body.elapsedMs === 'number' && body.elapsedMs < LIMITS.MIN_FILL_MS) {
    console.log('escalate: 200 dropped too_fast');
    return json(200, { ok: true });
  }

  if (!env || !env.RESEND_API_KEY) {
    return fail(503, 'not_configured', 'Sending is not set up yet. Write to ' + SUPPORT_ADDRESS + ' instead.');
  }

  const recipient = to === 'founder' ? env.FOUNDER_EMAIL || SUPPORT_ADDRESS : SUPPORT_ADDRESS;
  const subject = to === 'founder' ? `For Robin: ${reason}` : `Support: ${reason}`;
  const text =
    `Visitor email: ${email}\nPage: ${page || '(unknown)'}\n` +
    (summary ? `Nora's summary: ${summary}\n` : '') +
    `\nMessage:\n${question}\n\nLast messages in the chat:\n${renderTranscript(transcript.slice(-LIMITS.MAIL_TRANSCRIPT)) || '(none)'}\n`;

  let res;
  try {
    res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: env.ESCALATION_FROM || DEFAULT_FROM,
        to: [recipient],
        reply_to: email,
        subject,
        text,
      }),
    });
  } catch {
    return fail(502, 'upstream', "That didn't go through. Try again in a minute.");
  }
  if (!res.ok) return fail(502, 'upstream', "That didn't go through. Try again in a minute.");

  console.log('escalate: 200 sent');
  return json(200, { ok: true });
}

export async function onRequest(context) {
  if (context.request.method === 'POST') return onRequestPost(context);
  return fail(405, 'method_not_allowed', 'Use POST.');
}
