/* POST /api/founding: a founding-family sign-up from /founding-families.
   Cloudflare Pages Function, no dependencies, no storage. It checks the form and passes the sign-up on as one
   email to the business inbox; the gift code itself is sent from Robin's own machine, so no code and no list of
   people ever lives here. Secret: RESEND_API_KEY. Nothing about the visitor is logged. */

import { FORM_PER_HOUR, withinLimit } from '../_chat/ratelimit.js';

const SUPPORT_ADDRESS = 'support@tryfeedflow.app';
const FROM = 'Feed Flow site <chat@tryfeedflow.app>';
const EMAIL_RE = /^[^\s@<>"',;:\\()[\]]+@[^\s@<>"',;:\\()[\]]+\.[^\s@<>"',;:\\()[\]]+$/;
const NAME_RE = /^[\p{L}\p{M}][\p{L}\p{M} .'-]{0,39}$/u;
const STORES = ['US', 'GB', 'CA', 'AU', 'NO', 'SE', 'DK', 'FI', 'MX', 'CO', 'OTHER'];
const LIMITS = { BODY_BYTES: 4 * 1024, EMAIL_CHARS: 254, MIN_FILL_MS: 2500 };
const ALLOWED_ORIGINS = ['https://tryfeedflow.app', 'https://www.tryfeedflow.app'];

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}
function fail(status, code, message) {
  console.log(`founding: ${status} ${code}`);
  return json(status, { code, message });
}
function originAllowed(origin) {
  if (!origin) return false;
  if (ALLOWED_ORIGINS.includes(origin)) return true;
  try {
    const url = new URL(origin);
    return url.protocol === 'https:' && url.origin === origin && url.hostname.endsWith('.feed-flow-web.pages.dev');
  } catch {
    return false;
  }
}

export async function onRequestPost({ request, env }) {
  if (!originAllowed(request.headers.get('Origin'))) {
    return fail(403, 'forbidden', 'This request did not come from the Feed Flow site.');
  }
  if (!(await withinLimit(request, 'founding', FORM_PER_HOUR))) {
    return fail(429, 'rate_limited', 'That is a lot of sign-ups for now. Try again in a while, or write to ' + SUPPORT_ADDRESS + '.');
  }
  let raw;
  try {
    raw = await request.text();
  } catch {
    return fail(400, 'bad_request', 'We could not read that.');
  }
  if (new TextEncoder().encode(raw).length > LIMITS.BODY_BYTES) return fail(413, 'too_long', 'That is too long.');
  let body;
  try {
    body = JSON.parse(raw);
  } catch {
    return fail(400, 'bad_request', 'We could not read that.');
  }
  if (!body || typeof body !== 'object' || Array.isArray(body)) return fail(400, 'bad_request', 'We could not read that.');

  const email = typeof body.email === 'string' ? body.email.trim().toLowerCase() : '';
  if (!email || email.length > LIMITS.EMAIL_CHARS || !EMAIL_RE.test(email)) {
    return fail(400, 'bad_email', "That email doesn't look right.");
  }
  const first = typeof body.first === 'string' ? body.first.trim().replace(/\s+/g, ' ') : '';
  if (!first || !NAME_RE.test(first)) return fail(400, 'bad_name', 'Write your first name, letters only.');
  const store = typeof body.store === 'string' ? body.store.trim().toUpperCase() : '';
  if (!STORES.includes(store)) return fail(400, 'bad_store', 'Choose the country of your App Store account.');
  const other = store === 'OTHER' && typeof body.other === 'string' ? body.other.replace(/[^\p{L}\p{M} .'-]/gu, '').trim().slice(0, 40) : '';

  // Spam guards. Both answer as if it worked, so a bot learns nothing.
  if (typeof body.company === 'string' && body.company.trim() !== '') {
    console.log('founding: 200 dropped honeypot');
    return json(200, { ok: true });
  }
  if (typeof body.elapsedMs !== 'number' || body.elapsedMs < LIMITS.MIN_FILL_MS) {
    console.log('founding: 200 dropped too_fast');
    return json(200, { ok: true });
  }

  if (!env || !env.RESEND_API_KEY) {
    return fail(503, 'not_configured', 'Sign-up is not set up yet. Write to ' + SUPPORT_ADDRESS + ' instead.');
  }

  const country = (request.cf && typeof request.cf.country === 'string' && request.cf.country) || '??';
  const ref = crypto.randomUUID().slice(0, 8);
  const text = `FF-FOUNDING v1\nref: ${ref}\nemail: ${email}\nfirst: ${first}\ncountry: ${country}\nstore: ${store}\nother: ${other || '-'}\nat: ${new Date().toISOString()}\n`;

  let res;
  try {
    res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: FROM, to: [SUPPORT_ADDRESS], subject: `Founding family sign-up [${ref}]`, text }),
    });
  } catch {
    return fail(502, 'upstream', "That didn't go through. Try again in a minute.");
  }
  if (!res.ok) return fail(502, 'upstream', "That didn't go through. Try again in a minute.");

  console.log('founding: 200 accepted');
  return json(200, { ok: true });
}

export async function onRequest(context) {
  if (context.request.method === 'POST') return onRequestPost(context);
  return fail(405, 'method_not_allowed', 'Use POST.');
}
