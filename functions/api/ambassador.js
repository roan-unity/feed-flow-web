/* POST /api/ambassador: an ambassador application from /ambassador.
   Cloudflare Pages Function, no dependencies, no storage. It checks the form and passes the application on as one
   email to the business inbox, with the applicant as reply-to, so every application is read and answered by a
   person. Secret: RESEND_API_KEY. Nothing about the visitor is logged. */

import { FORM_PER_HOUR, withinLimit } from '../_chat/ratelimit.js';

const SUPPORT_ADDRESS = 'support@tryfeedflow.app';
const FROM = 'Feed Flow site <chat@tryfeedflow.app>';
const EMAIL_RE = /^[^\s@<>"',;:\\()[\]]+@[^\s@<>"',;:\\()[\]]+\.[^\s@<>"',;:\\()[\]]+$/;
const NAME_RE = /^[\p{L}\p{M}][\p{L}\p{M} .'’-]{0,79}$/u;
const CONTROL_RE = /[\u0000-\u001f\u007f]/;
const LIMITS = { BODY_BYTES: 8 * 1024, EMAIL_CHARS: 254, WORK_MIN: 3, WORK_CHARS: 300, NOTE_CHARS: 1000, MIN_FILL_MS: 2500 };
const ALLOWED_ORIGINS = ['https://tryfeedflow.app', 'https://www.tryfeedflow.app'];

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}
function fail(status, code, message) {
  console.log(`ambassador: ${status} ${code}`);
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
  if (!(await withinLimit(request, 'ambassador', FORM_PER_HOUR))) {
    return fail(429, 'rate_limited', 'That is a lot of applications for now. Write to ' + SUPPORT_ADDRESS + ' instead.');
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

  const name = typeof body.name === 'string' ? body.name.trim().replace(/\s+/g, ' ') : '';
  if (!name || !NAME_RE.test(name)) return fail(400, 'bad_name', 'Write your name, letters only.');
  const email = typeof body.email === 'string' ? body.email.trim().toLowerCase() : '';
  if (!email || email.length > LIMITS.EMAIL_CHARS || !EMAIL_RE.test(email)) {
    return fail(400, 'bad_email', "That email doesn't look right.");
  }
  const work = typeof body.work === 'string' ? body.work.trim() : '';
  if (work.length < LIMITS.WORK_MIN || work.length > LIMITS.WORK_CHARS || CONTROL_RE.test(work)) {
    return fail(400, 'bad_work', 'Add one link or handle where we can see your work.');
  }
  const note = typeof body.note === 'string' ? body.note.replace(/\r\n?/g, '\n').trim() : '';
  if (note.length > LIMITS.NOTE_CHARS) return fail(400, 'note_too_long', 'Keep the note under 1,000 characters.');
  if (body.agree !== true) {
    return fail(400, 'not_agreed', 'Tick the box about telling your audience and sharing honest opinions.');
  }

  // Spam guards. Both answer as if it worked, so a bot learns nothing.
  if (typeof body.company === 'string' && body.company.trim() !== '') {
    console.log('ambassador: 200 dropped honeypot');
    return json(200, { ok: true });
  }
  if (typeof body.elapsedMs !== 'number' || body.elapsedMs < LIMITS.MIN_FILL_MS) {
    console.log('ambassador: 200 dropped too_fast');
    return json(200, { ok: true });
  }

  if (!env || !env.RESEND_API_KEY) {
    return fail(503, 'not_configured', 'The form is not set up yet. Write to ' + SUPPORT_ADDRESS + ' instead.');
  }

  const country = (request.cf && typeof request.cf.country === 'string' && request.cf.country) || '??';
  const ref = crypto.randomUUID().slice(0, 8);
  const text = `FF-AMBASSADOR v1\nref: ${ref}\nname: ${name}\nemail: ${email}\nwork: ${work}\ncountry: ${country}\ndisclosure and honest opinions: agreed\nat: ${new Date().toISOString()}\n\nnote:\n${note || '(none)'}\n`;

  let res;
  try {
    res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: FROM, to: [SUPPORT_ADDRESS], reply_to: email, subject: `Ambassador application: ${name}`, text }),
    });
  } catch {
    return fail(502, 'upstream', "That didn't go through.");
  }
  if (!res.ok) return fail(502, 'upstream', "That didn't go through.");

  console.log('ambassador: 200 accepted');
  return json(200, { ok: true });
}

export async function onRequest(context) {
  if (context.request.method === 'POST') return onRequestPost(context);
  return fail(405, 'method_not_allowed', 'Use POST.');
}
