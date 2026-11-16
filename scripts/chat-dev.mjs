// Local runner for the site chat: serves the site and calls the real Pages Function handlers
// (functions/api/chat/index.js and escalate.js). No wrangler needed.
//   OPENROUTER_API_KEY=... node scripts/chat-dev.mjs [--port 7222]
// Without a key /api/chat answers 503 not_configured, which is what the widget's fallback form expects.
// Optional env: CHAT_MODELS_FAST, CHAT_MODELS_STRONG, FOUNDER_EMAIL, RESEND_API_KEY.
import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import * as chatRoute from '../functions/api/chat/index.js';
import * as escalateRoute from '../functions/api/chat/escalate.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.pdf': 'application/pdf',
};

/** An in-memory stand-in for caches.default, so the per-IP counters run locally too. */
export function memoryCache() {
  const store = new Map();
  return {
    match: async (request) => (store.has(request.url) ? new Response(store.get(request.url)) : undefined),
    put: async (request, response) => { store.set(request.url, await response.text()); },
  };
}

export function createRunner(env = {}) {
  if (!globalThis.caches) globalThis.caches = { default: memoryCache() };
  const runEnv = { ENV: 'dev', ...env };
  const routes = { '/api/chat': chatRoute, '/api/chat/escalate': escalateRoute };
  return http.createServer(async (req, res) => {
    try {
      const pathname = decodeURIComponent(new URL(req.url, 'http://local').pathname).replace(/(.)\/+$/, '$1');
      const route = routes[pathname];
      if (route) {
        const chunks = [];
        for await (const c of req) chunks.push(c);
        const hasBody = req.method !== 'GET' && req.method !== 'HEAD';
        const request = new Request(`http://${req.headers.host}${req.url}`, { method: req.method, headers: req.headers, body: hasBody ? Buffer.concat(chunks) : undefined });
        const response = await route.onRequest({ request, env: runEnv, waitUntil() {} });
        res.writeHead(response.status, Object.fromEntries(response.headers));
        if (!response.body) return res.end();
        const reader = response.body.getReader();
        res.on('close', () => reader.cancel().catch(() => {}));
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          res.write(value);
        }
        return res.end();
      }
      let relative = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
      if (!path.extname(relative)) relative += '.html';
      const file = path.resolve(root, relative);
      // Same as production: the code and knowledge folders are never served.
      if ((file !== root && !file.startsWith(root + path.sep)) || /^(functions|scripts|\.git|node_modules)(\/|$)/.test(path.relative(root, file))) {
        res.writeHead(404).end('Not found');
        return;
      }
      const info = await stat(file);
      const target = info.isDirectory() ? path.join(file, 'index.html') : file;
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(target)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
      res.end(req.method === 'HEAD' ? undefined : await readFile(target));
    } catch {
      if (!res.headersSent) res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Not found');
    }
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const args = process.argv.slice(2);
  const portAt = args.indexOf('--port');
  const port = Number(portAt >= 0 ? args[portAt + 1] : process.env.PORT || 7222);
  const env = {};
  for (const k of ['OPENROUTER_API_KEY', 'CHAT_MODELS_FAST', 'CHAT_MODELS_STRONG', 'FOUNDER_EMAIL', 'RESEND_API_KEY', 'AI_GATEWAY_URL']) {
    if (process.env[k]) env[k] = process.env[k];
  }
  createRunner(env).listen(port, '127.0.0.1', () => {
    console.log(`Feed Flow chat runner: http://127.0.0.1:${port}/  (chat: ${env.OPENROUTER_API_KEY ? 'LIVE via OpenRouter' : 'no key, /api/chat answers 503'})`);
  });
}
