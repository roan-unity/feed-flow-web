import http from "node:http";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const valueAfter = (flag, fallback) => {
  const index = args.indexOf(flag);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
};
const host = valueAfter("--host", process.env.HOST || "127.0.0.1");
const port = Number(valueAfter("--port", process.env.PORT || "7100"));
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8"
};

const server = http.createServer(async (request, response) => {
  try {
    if (request.method !== "GET" && request.method !== "HEAD") {
      response.writeHead(501, { "Content-Type": "text/plain; charset=utf-8" });
      response.end("The local preview does not accept form submissions.");
      return;
    }
    const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
    let relative = pathname === "/" ? "index.html" : pathname.replace(/^\/+/, "");
    if (!path.extname(relative) && !relative.endsWith("/")) relative += ".html";
    const file = path.resolve(root, relative);
    if (file !== root && !file.startsWith(root + path.sep)) {
      response.writeHead(403).end("Forbidden");
      return;
    }
    const info = await stat(file);
    const target = info.isDirectory() ? path.join(file, "index.html") : file;
    const body = await readFile(target);
    response.writeHead(200, {
      "Content-Type": types[path.extname(target)] || "application/octet-stream",
      "Cache-Control": "no-store"
    });
    response.end(body);
  } catch {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("Not found");
  }
});
server.listen(port, host, () => console.log(`Feed Flow website preview: http://${host}:${port}/`));
