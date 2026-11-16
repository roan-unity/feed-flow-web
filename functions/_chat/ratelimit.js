// Best-effort per-visitor counters kept in the edge cache (caches.default).
// No accounts, no database, nothing personal stored: the key is a short hash of
// the IP and the hour. It is not atomic and it is per data centre, which is fine
// for what it is for: slowing down a script, not billing anyone.

const HOUR_MS = 3_600_000;

export const CHAT_PER_HOUR = 20;
export const FORM_PER_HOUR = 5;

async function shortHash(text) {
  const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(bytes).slice(0, 8)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Counts one hit for this visitor and kind. Returns false once `max` is passed.
 * Without a cache (local runs, some tests) it always allows.
 */
export async function withinLimit(request, kind, max, { cache, now = Date.now() } = {}) {
  const store = cache || globalThis.caches?.default;
  if (!store) return true;
  try {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const key = new Request(`https://rate.feedflow.invalid/${kind}/${Math.floor(now / HOUR_MS)}/${await shortHash(ip)}`);
    const found = await store.match(key);
    const count = found ? Number(await found.text()) || 0 : 0;
    if (count >= max) return false;
    await store.put(key, new Response(String(count + 1), { headers: { 'Cache-Control': 'max-age=3600' } }));
    return true;
  } catch {
    return true; // a broken counter must never take the chat down
  }
}
