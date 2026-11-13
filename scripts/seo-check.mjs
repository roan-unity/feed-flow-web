import { readFile, writeFile, access } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const origin = "https://tryfeedflow.app";
const errors = [];
const warnings = [];
const checked = [];

const sitemap = await readFile(path.join(root, "sitemap.xml"), "utf8");
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => match[1]);
if (new Set(urls).size !== urls.length) errors.push("Sitemap contains duplicate URLs");

function localPathForUrl(url) {
  const pathname = new URL(url, origin).pathname;
  if (pathname === "/") return path.join(root, "index.html");
  if (path.extname(pathname)) return path.join(root, pathname);
  return path.join(root, pathname + ".html");
}
function localPathForLink(href, pageUrl) {
  const target = new URL(href, pageUrl);
  return localPathForUrl(target.href);
}
function content(html, regex) {
  return html.match(regex)?.[1]?.trim() || "";
}

for (const url of urls) {
  const file = localPathForUrl(url);
  let html;
  try {
    html = await readFile(file, "utf8");
  } catch {
    errors.push(`${url}: missing local page ${path.relative(root, file)}`);
    continue;
  }
  const relative = path.relative(root, file);
  const title = content(html, /<title>([\s\S]*?)<\/title>/i);
  const description = content(html, /<meta\s+name="description"\s+content="([^"]*)"/i);
  const canonical = content(html, /<link\s+rel="canonical"\s+href="([^"]*)"/i);
  const h1Count = (html.match(/<h1(?:\s|>)/gi) || []).length;
  if (!title) errors.push(`${relative}: missing title`);
  if (!description) errors.push(`${relative}: missing meta description`);
  if (canonical !== url) errors.push(`${relative}: canonical ${canonical || "missing"} does not match sitemap URL ${url}`);
  if (h1Count !== 1) errors.push(`${relative}: expected one h1, found ${h1Count}`);
  if (!/<meta\s+name="viewport"/i.test(html)) errors.push(`${relative}: missing viewport meta`);
  if (title && (title.length < 25 || title.length > 65)) warnings.push(`${relative}: title is ${title.length} characters`);
  if (description && (description.length < 70 || description.length > 175)) warnings.push(`${relative}: meta description is ${description.length} characters`);

  for (const image of html.matchAll(/<img\b[^>]*>/gi)) {
    if (!/\salt="[^"]*"/i.test(image[0])) errors.push(`${relative}: image without alt attribute: ${image[0].slice(0, 120)}`);
  }
  for (const script of html.matchAll(/<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/gi)) {
    try { JSON.parse(script[1]); } catch (error) { errors.push(`${relative}: invalid JSON-LD: ${error.message}`); }
  }
  for (const link of html.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*>/gi)) {
    const href = link[1];
    if (href === "#") errors.push(`${relative}: placeholder href="#"`);
    if (/^(https?:|mailto:|tel:|data:|javascript:)/i.test(href)) continue;
    const resolved = new URL(href, url);
    if (resolved.origin !== origin) continue;
    const target = localPathForLink(href, url);
    try {
      await access(target);
      if (resolved.hash) {
        const targetHtml = await readFile(target, "utf8");
        const id = decodeURIComponent(resolved.hash.slice(1));
        if (!new RegExp(`\\bid=["']${id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}["']`).test(targetHtml)) {
          errors.push(`${relative}: link ${href} targets missing id ${id}`);
        }
      }
    } catch {
      errors.push(`${relative}: broken local link ${href} -> ${path.relative(root, target)}`);
    }
  }
  checked.push({ url, file: relative, titleLength: title.length, descriptionLength: description.length });
}

const home = await readFile(path.join(root, "index.html"), "utf8");
for (const id of ["feeding", "growth", "health", "resources", "reviews"]) {
  if (!new RegExp(`id="${id}"`).test(home)) errors.push(`Homepage is missing required #${id} section`);
}
if (/linkedin-bottom/.test(home)) errors.push("Homepage still contains the oversized LinkedIn banner");
const footer = home.match(/<footer[\s\S]*?<\/footer>/i)?.[0] || "";
if (/Robin|Andersson/.test(footer)) errors.push("Homepage footer still contains the removed personal/company name");

const publicFiles = await Promise.all(urls.map(async (url) => {
  try { return await readFile(localPathForUrl(url), "utf8"); } catch { return ""; }
}));
publicFiles.push(await readFile(path.join(root, "llms.txt"), "utf8"));
const publicText = publicFiles.join("\n");
for (const stale of [/two-tier/i, /25% commission/i, /5% override/i, /pre-launch/i]) {
  if (stale.test(publicText)) errors.push(`Public content contains retired affiliate wording: ${stale}`);
}
if (!/35–50%/.test(publicText)) errors.push("The 35–50% ambassador offer is missing");

const report = {
  workflow: "OpenSEO seo-audit local technical checks",
  liveKeywordData: "Not connected; no volume, ranking or traffic claims are included",
  sitemapUrls: urls.length,
  pagesChecked: checked.length,
  errors,
  warnings,
  checked
};
await writeFile(path.join(root, "seo", "technical-audit.json"), JSON.stringify(report, null, 2) + "\n");
for (const warning of warnings) console.warn(`WARN ${warning}`);
for (const error of errors) console.error(`FAIL ${error}`);
console.log(`OpenSEO local audit: ${checked.length} pages, ${errors.length} errors, ${warnings.length} warnings.`);
if (errors.length) process.exit(1);
