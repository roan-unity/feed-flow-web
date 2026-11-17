// Tests for the ambassador application: the /api/ambassador Pages Function. No real email is ever sent.
// Run with: node --test scripts/ambassador-function.test.mjs
import { test, describe, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { onRequest, onRequestPost } from '../functions/api/ambassador.js';

const realFetch = globalThis.fetch;
const realLog = console.log;
let calls;
let logged;

function stubFetch(status = 200) {
  calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return new Response(JSON.stringify({ id: 'x' }), { status });
  };
}
beforeEach(() => {
  logged = [];
  console.log = (...a) => logged.push(a.join(' '));
  stubFetch();
});
afterEach(() => {
  globalThis.fetch = realFetch;
  console.log = realLog;
});

const valid = { name: 'Sam  Rivera', email: 'Sam@Example.com', work: 'instagram.com/samandbaby', note: 'Two under two.\r\nI post about night feeds.', agree: true, company: '', elapsedMs: 9000 };
function post(body, { origin = 'https://tryfeedflow.app', env = { RESEND_API_KEY: 'k' }, raw } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (origin) headers.Origin = origin;
  const request = new Request('https://tryfeedflow.app/api/ambassador', { method: 'POST', headers, body: raw ?? JSON.stringify(body) });
  return onRequestPost({ request, env });
}

describe('ambassador function', () => {
  test('happy path sends one Resend request and answers ok', async () => {
    const res = await post(valid, { env: { RESEND_API_KEY: 'key-123' } });
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true });
    assert.equal(res.headers.get('Cache-Control'), 'no-store');
    assert.equal(calls.length, 1);
    assert.equal(calls[0].url, 'https://api.resend.com/emails');
    assert.equal(calls[0].init.headers.Authorization, 'Bearer key-123');
    const sent = JSON.parse(calls[0].init.body);
    assert.equal(sent.from, 'Feed Flow site <chat@tryfeedflow.app>');
    assert.deepEqual(sent.to, ['support@tryfeedflow.app']);
    assert.equal(sent.reply_to, 'sam@example.com');
    assert.equal(sent.subject, 'Ambassador application: Sam Rivera');
    assert.match(sent.text, /^FF-AMBASSADOR v1\nref: [0-9a-f]{8}\n/);
    assert.match(sent.text, /name: Sam Rivera\nemail: sam@example\.com\nwork: instagram\.com\/samandbaby\n/);
    assert.match(sent.text, /disclosure and honest opinions: agreed/);
    assert.match(sent.text, /note:\nTwo under two\.\nI post about night feeds\.\n$/);
  });
  test('the note is optional', async () => {
    const { note, ...rest } = valid;
    const res = await post(rest);
    assert.equal(res.status, 200);
    assert.match(JSON.parse(calls[0].init.body).text, /note:\n\(none\)\n$/);
  });
  test('accepts a plain handle and names with accents and apostrophes', async () => {
    assert.equal((await post({ ...valid, work: '@samandbaby', name: "Zoë O'Neil-Åberg" })).status, 200);
    assert.equal(JSON.parse(calls[0].init.body).subject, "Ambassador application: Zoë O'Neil-Åberg");
  });
  test('five applications an hour per visitor, then 429', async () => {
    const store = new Map();
    globalThis.caches = { default: { match: async (r) => (store.has(r.url) ? new Response(store.get(r.url)) : undefined), put: async (r, res) => { store.set(r.url, await res.text()); } } };
    try {
      const results = [];
      for (let i = 0; i < 7; i += 1) results.push((await post(valid)).status);
      assert.deepEqual(results, [200, 200, 200, 200, 200, 429, 429]);
    } finally {
      delete globalThis.caches;
    }
  });
  test('answers 503 not_configured without a key', async () => {
    const res = await post(valid, { env: {} });
    assert.equal(res.status, 503);
    const j = await res.json();
    assert.equal(j.code, 'not_configured');
    assert.equal(typeof j.message, 'string');
    assert.equal(calls.length, 0);
  });
  test('rejects a bad or missing Origin, allows preview and www', async () => {
    assert.equal((await post(valid, { origin: 'https://evil.example' })).status, 403);
    assert.equal((await post(valid, { origin: null })).status, 403);
    assert.equal((await post(valid, { origin: 'https://tryfeedflow.app.evil.example' })).status, 403);
    assert.equal((await post(valid, { origin: 'https://evilfeed-flow-web.pages.dev' })).status, 403);
    assert.equal((await post(valid, { origin: 'http://localhost:7100' })).status, 403);
    assert.equal(calls.length, 0);
    assert.equal((await post(valid, { origin: 'https://www.tryfeedflow.app' })).status, 200);
    assert.equal((await post(valid, { origin: 'https://feature-ambassador-simple.feed-flow-web.pages.dev' })).status, 200);
  });
  test('honeypot drops silently with ok and sends nothing', async () => {
    const res = await post({ ...valid, company: 'Acme' });
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true });
    assert.equal(calls.length, 0);
  });
  test('a too-fast submit drops silently with ok and sends nothing', async () => {
    for (const elapsedMs of [900, undefined, '9000']) {
      const res = await post({ ...valid, elapsedMs });
      assert.equal(res.status, 200);
      assert.deepEqual(await res.json(), { ok: true });
    }
    assert.equal(calls.length, 0);
  });
  test('rejects a bad name', async () => {
    for (const name of ['', '   ', 42, '<b>Sam</b>', 'Sam\nBcc: x@y.z', 'http://spam.example', 'a'.repeat(81)]) {
      const res = await post({ ...valid, name });
      assert.equal(res.status, 400, String(name).slice(0, 20));
      assert.equal((await res.json()).code, 'bad_name');
    }
    assert.equal(calls.length, 0);
  });
  test('rejects a bad email', async () => {
    for (const email of ['', 'nope', 'a@b', 'a b@c.com', 'x'.repeat(250) + '@example.com']) {
      const res = await post({ ...valid, email });
      assert.equal(res.status, 400, email.slice(0, 20));
      assert.equal((await res.json()).code, 'bad_email');
    }
    assert.equal(calls.length, 0);
  });
  test('rejects a missing, too long or multi-line work link', async () => {
    for (const work of ['', 'x', undefined, 'a'.repeat(301), 'insta\nBcc: x@y.z']) {
      const res = await post({ ...valid, work });
      assert.equal(res.status, 400);
      assert.equal((await res.json()).code, 'bad_work');
    }
    assert.equal(calls.length, 0);
  });
  test('rejects a note over 1,000 characters', async () => {
    const res = await post({ ...valid, note: 'a'.repeat(1001) });
    assert.equal(res.status, 400);
    assert.equal((await res.json()).code, 'note_too_long');
  });
  test('the disclosure box must be ticked', async () => {
    for (const agree of [false, undefined, 'true', 1]) {
      const res = await post({ ...valid, agree });
      assert.equal(res.status, 400);
      assert.equal((await res.json()).code, 'not_agreed');
    }
    assert.equal(calls.length, 0);
  });
  test('rejects unreadable and oversized bodies', async () => {
    assert.equal((await post(null, { raw: '{nope' })).status, 400);
    assert.equal((await post(null, { raw: '[]' })).status, 400);
    assert.equal((await post(null, { raw: 'null' })).status, 400);
    assert.equal((await post({ ...valid, padding: 'x'.repeat(9000) })).status, 413);
    assert.equal(calls.length, 0);
  });
  test('answers 502 when Resend fails or is unreachable', async () => {
    stubFetch(500);
    let res = await post(valid);
    assert.equal(res.status, 502);
    assert.equal((await res.json()).code, 'upstream');
    globalThis.fetch = async () => { throw new Error('network'); };
    res = await post(valid);
    assert.equal(res.status, 502);
  });
  test('only POST is accepted', async () => {
    const res = await onRequest({ request: new Request('https://tryfeedflow.app/api/ambassador'), env: {} });
    assert.equal(res.status, 405);
  });
  test('nothing about the applicant is logged', async () => {
    await post(valid);
    await post({ ...valid, email: 'nope' });
    await post({ ...valid, company: 'Acme' });
    const all = logged.join('\n');
    assert.ok(all.length > 0);
    for (const secret of ['Sam', 'sam@example.com', 'samandbaby', 'night feeds', 'Acme', 'nope']) {
      assert.ok(!all.includes(secret), `log leaks ${secret}`);
    }
  });
});

describe('ambassador page and script', () => {
  const html = readFileSync(new URL('../ambassador.html', import.meta.url), 'utf8');
  const js = readFileSync(new URL('../ambassador.js', import.meta.url), 'utf8');
  test('the form shows only name, email, one work link, an optional note and the disclosure box', () => {
    const form = html.match(/<form id="ambassadorForm"[\s\S]*?<\/form>/)[0];
    const names = [...form.matchAll(/<(?:input|textarea|select)\b[^>]*\bname="([^"]+)"/g)].map((m) => m[1]);
    assert.deepEqual(names, ['name', 'email', 'work', 'note', 'company', 'agree']);
    assert.ok(!/<select/.test(form));
    assert.match(form, /class="hp"[^>]*aria-hidden="true"[^>]*>[\s\S]*name="company"/);
    for (const required of ['name', 'email', 'work', 'agree']) assert.match(form, new RegExp(`name="${required}"[^>]*required`));
    assert.ok(!/name="note"[^>]*required/.test(form));
  });
  test('the script posts to /api/ambassador and keeps the email fallback', () => {
    assert.match(js, /fetch\('\/api\/ambassador'/);
    assert.match(js, /mailto:support@tryfeedflow\.app/);
  });
  test('the published terms are on the page, and no job markup', () => {
    assert.match(html, /35–50% commission on net profit/);
    assert.match(html, /own link or code/);
    assert.match(html, /not guaranteed/);
    assert.ok(!/JobPosting/.test(html));
  });
});
