// Tests for the site chat: the /api/chat/escalate Pages Function and the closed-mode opening-hours helpers.
// Run with: node --test scripts/chat-escalate.test.mjs
import { test, describe, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { onRequest, onRequestPost } from '../functions/api/chat/escalate.js';

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

const valid = { email: 'sam@example.com', question: 'My subscription shows twice.', page: '/support', reason: 'request', transcript: [], company: '', elapsedMs: 9000 };
function post(body, { origin = 'https://tryfeedflow.app', env = { RESEND_API_KEY: 'k' }, raw } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (origin) headers.Origin = origin;
  const request = new Request('https://tryfeedflow.app/api/chat/escalate', { method: 'POST', headers, body: raw ?? JSON.stringify(body) });
  return onRequestPost({ request, env });
}

describe('escalate function', () => {
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
    assert.equal(sent.subject, 'Site message: request');
    assert.match(sent.text, /Visitor email: sam@example\.com/);
    assert.match(sent.text, /Page: \/support/);
    assert.match(sent.text, /My subscription shows twice\./);
  });
  test('uses ESCALATION_FROM and includes a transcript', async () => {
    const res = await post({ ...valid, transcript: [{ role: 'user', content: 'Hi' }, { role: 'assistant', content: 'Hello' }] }, { env: { RESEND_API_KEY: 'k', ESCALATION_FROM: 'Site <a@tryfeedflow.app>' } });
    assert.equal(res.status, 200);
    const sent = JSON.parse(calls[0].init.body);
    assert.equal(sent.from, 'Site <a@tryfeedflow.app>');
    assert.match(sent.text, /Visitor: Hi\n\nNora: Hello/);
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
    assert.equal((await post(valid, { origin: 'https://evilpages.dev' })).status, 403);
    assert.equal((await post(valid, { origin: 'http://localhost:7222' })).status, 403);
    assert.equal((await post(valid, { origin: 'https://www.tryfeedflow.app' })).status, 200);
    assert.equal((await post(valid, { origin: 'https://abc123.feed-flow.pages.dev' })).status, 200);
    assert.equal((await post(valid, { origin: 'http://localhost:7222', env: { ENV: 'dev', RESEND_API_KEY: 'k' } })).status, 200);
  });
  test('honeypot drops silently with ok and sends nothing', async () => {
    const res = await post({ ...valid, company: 'Acme' });
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true });
    assert.equal(calls.length, 0);
  });
  test('a too-fast submit drops silently with ok and sends nothing', async () => {
    const res = await post({ ...valid, elapsedMs: 900 });
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true });
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
  test('rejects an empty or too long message', async () => {
    assert.equal((await post({ ...valid, question: '   ' })).status, 400);
    const long = await post({ ...valid, question: 'a'.repeat(1001) });
    assert.equal(long.status, 413);
    assert.equal((await long.json()).code, 'too_long');
    assert.equal((await post({ ...valid, question: 'a'.repeat(1000) })).status, 200);
  });
  test('rejects a body over 16 KB, bad JSON, and bad shapes', async () => {
    assert.equal((await post(null, { raw: JSON.stringify({ ...valid, page: 'x'.repeat(17000) }) })).status, 413);
    assert.equal((await post(null, { raw: '{nope' })).status, 400);
    assert.equal((await post(null, { raw: '[]' })).status, 400);
    assert.equal((await post({ ...valid, page: 'p'.repeat(201) })).status, 400);
    assert.equal((await post({ ...valid, transcript: new Array(21).fill({ role: 'user', content: 'a' }) })).status, 400);
    assert.equal((await post({ ...valid, transcript: [{ role: 'user', content: 'a'.repeat(1001) }] })).status, 400);
  });
  test('Resend failure answers 502 upstream', async () => {
    stubFetch(500);
    const res = await post(valid);
    assert.equal(res.status, 502);
    assert.equal((await res.json()).code, 'upstream');
    globalThis.fetch = async () => { throw new Error('network'); };
    assert.equal((await post(valid)).status, 502);
  });
  test('other methods get 405 and nothing is logged with the message or address', async () => {
    const res = await onRequest({ request: new Request('https://tryfeedflow.app/api/chat/escalate', { method: 'GET' }), env: {} });
    assert.equal(res.status, 405);
    assert.equal(res.headers.get('Cache-Control'), 'no-store');
    await post(valid);
    await post({ ...valid, email: 'bad' });
    const all = logged.join('\n');
    assert.doesNotMatch(all, /sam@example\.com|subscription/);
  });
});

// The opening-hours helpers live between marker comments in chat.js; evaluate just that block.
const src = readFileSync(new URL('../chat.js', import.meta.url), 'utf8');
const block = src.slice(src.indexOf('/* time:start */'), src.indexOf('/* time:end */'));
const time = new Function(block + '\nreturn { zoneParts, zoneOffsetMs, isOpenNow, nextOpening, openingText };')();
const CFG = (live = true) => ({ live, hours: { tz: 'America/New_York', open: 9, close: 21 } });
const at = (iso) => Date.parse(iso);

describe('closed-mode hours', () => {
  test('never open while live is false', () => {
    assert.equal(time.isOpenNow(at('2026-06-10T16:00:00Z'), CFG(false)), false);
  });
  test('open from 9:00 to before 21:00 Eastern', () => {
    assert.equal(time.isOpenNow(at('2026-06-10T12:59:00Z'), CFG()), false); // 08:59 EDT
    assert.equal(time.isOpenNow(at('2026-06-10T13:00:00Z'), CFG()), true); // 09:00 EDT
    assert.equal(time.isOpenNow(at('2026-06-11T00:59:00Z'), CFG()), true); // 20:59 EDT
    assert.equal(time.isOpenNow(at('2026-06-11T01:00:00Z'), CFG()), false); // 21:00 EDT
    assert.equal(time.isOpenNow(at('2026-01-15T14:00:00Z'), CFG()), true); // 09:00 EST
    assert.equal(time.isOpenNow(at('2026-01-15T13:59:00Z'), CFG()), false);
  });
  test('midnight does not read as hour 24', () => {
    assert.equal(time.zoneParts(at('2026-06-10T04:00:00Z'), 'America/New_York').hour, 0);
  });
  test('next opening: same morning, or tomorrow', () => {
    assert.equal(new Date(time.nextOpening(at('2026-06-10T06:00:00Z'), CFG())).toISOString(), '2026-06-10T13:00:00.000Z'); // 02:00 EDT -> 09:00 EDT
    assert.equal(new Date(time.nextOpening(at('2026-06-11T02:00:00Z'), CFG())).toISOString(), '2026-06-11T13:00:00.000Z'); // 22:00 EDT -> next 09:00 EDT
  });
  test('DST edge: spring forward (8 Mar 2026) and fall back (1 Nov 2026) use the new offset', () => {
    // 01:00 EST on 8 Mar: 09:00 that day is already EDT = 13:00Z, not 14:00Z.
    assert.equal(new Date(time.nextOpening(at('2026-03-08T06:00:00Z'), CFG())).toISOString(), '2026-03-08T13:00:00.000Z');
    // Evening of 7 Mar (EST) -> tomorrow 09:00 is EDT.
    assert.equal(new Date(time.nextOpening(at('2026-03-08T03:00:00Z'), CFG())).toISOString(), '2026-03-08T13:00:00.000Z');
    // 00:30 EDT on 1 Nov -> 09:00 that day is EST = 14:00Z.
    assert.equal(new Date(time.nextOpening(at('2026-11-01T04:30:00Z'), CFG())).toISOString(), '2026-11-01T14:00:00.000Z');
    // Evening of 31 Oct (EDT) -> 1 Nov 09:00 EST.
    assert.equal(new Date(time.nextOpening(at('2026-11-01T01:30:00Z'), CFG())).toISOString(), '2026-11-01T14:00:00.000Z');
  });
  test('text: Eastern only when the visitor shares the offset, local time when not', () => {
    const now = at('2026-06-11T02:00:00Z');
    assert.equal(time.openingText(now, CFG(), { visitorTz: 'America/Toronto', locale: 'en-GB' }), '9:00 AM Eastern');
    assert.equal(time.openingText(now, CFG(), { visitorTz: 'Europe/Oslo', locale: 'en-GB' }), '9:00 AM Eastern (15:00 your time)');
    assert.equal(time.openingText(now, CFG(), { visitorTz: 'America/Los_Angeles', locale: 'en-US' }), '9:00 AM Eastern (6:00 AM your time)');
  });
  test('text across the weeks where the US and Europe change clocks on different days', () => {
    // 20 Mar 2026: New York is on EDT (UTC-4) already, Oslo still on CET (UTC+1): five hours apart, not six.
    assert.equal(time.openingText(at('2026-03-20T02:00:00Z'), CFG(), { visitorTz: 'Europe/Oslo', locale: 'en-GB' }), '9:00 AM Eastern (14:00 your time)');
    // In January it is six hours.
    assert.equal(time.openingText(at('2026-01-20T02:00:00Z'), CFG(), { visitorTz: 'Europe/Oslo', locale: 'en-GB' }), '9:00 AM Eastern (15:00 your time)');
  });
});
