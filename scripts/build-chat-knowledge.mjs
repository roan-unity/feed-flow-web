// Builds the knowledge block Nora answers from.
//   node scripts/build-chat-knowledge.mjs
// Reads the ENGLISH pages of the site (nav, footer, scripts and markup removed), puts each page's public
// URL above its section, then appends every .md under functions/_chat/chat-knowledge/.
// Writes functions/_chat/knowledge.js (committed). Neither the source folder nor the output is publicly
// served: Cloudflare Pages does not publish the functions/ folder.
import { readFileSync, readdirSync, writeFileSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(root, 'functions/_chat/knowledge.js');
const SOURCE_DIR = path.join(root, 'functions/_chat/chat-knowledge');
const SITE = 'https://tryfeedflow.app';
export const MAX_CHARS = 126_000;

const FIXED_PAGES = [
  'index', 'faq', 'support', 'flowcast', 'bottle-countdown', 'formula-feeding', 'breastfeeding-pumping',
  'combo-feeding', 'baby-health', 'baby-report', 'growth-development', 'free-baby-feeding-tracker',
  'compare', 'resources', 'privacy',
];

const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', mdash: ',', ndash: ',', hellip: '...', rsquo: "'", lsquo: "'", rdquo: '"', ldquo: '"', middot: '·', copy: '©', rarr: '→', larr: '←', times: '×' };

function decode(text) {
  return text
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&([a-z]+);/gi, (m, n) => (n.toLowerCase() in ENTITIES ? ENTITIES[n.toLowerCase()] : m));
}

export function htmlToText(html) {
  let s = html;
  const main = s.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  if (main) s = main[1];
  else s = (s.match(/<body\b[^>]*>([\s\S]*)<\/body>/i) || [null, s])[1];
  s = s.replace(/<!--[\s\S]*?-->/g, ' ');
  for (const tag of ['script', 'style', 'noscript', 'svg', 'template', 'nav', 'footer', 'form', 'button', 'iframe', 'select', 'textarea']) {
    s = s.replace(new RegExp(`<${tag}\\b[\\s\\S]*?</${tag}>`, 'gi'), ' ');
  }
  s = s.replace(/<h([1-6])\b[^>]*>/gi, '\n\n### ').replace(/<\/h[1-6]>/gi, '\n');
  s = s.replace(/<li\b[^>]*>/gi, '\n- ');
  s = s.replace(/<(td|th)\b[^>]*>/gi, ' | ');
  s = s.replace(/<\/?(p|div|section|article|ul|ol|table|tr|br|details|summary|blockquote|figure|figcaption|dl|dt|dd|header|aside)\b[^>]*>/gi, '\n');
  s = s.replace(/<[^>]+>/g, '');
  s = decode(s);
  s = s.replace(/ [—–] /g, ', ').replace(/[—–]/g, ', ');
  const lines = s.split('\n').map((l) => l.replace(/[ \t ]+/g, ' ').trim());
  const out = [];
  for (const line of lines) {
    if (!line && (!out.length || !out[out.length - 1])) continue;
    if (line && line === out[out.length - 1]) continue;
    out.push(line);
  }
  return out.join('\n').trim();
}

function titleOf(html, fallback) {
  const t = html.match(/<title>([\s\S]*?)<\/title>/i);
  return t ? decode(t[1]).replace(/\s+/g, ' ').replace(/ [—–|-] Feed Flow!?.*$/i, '').trim() : fallback;
}

function urlFor(rel) {
  return rel === 'index' ? `${SITE}/` : `${SITE}/${rel}`;
}

function pageList() {
  const list = FIXED_PAGES.map((p) => ({ rel: p, kind: 'page' }));
  for (const dir of ['compare', 'guides']) {
    const full = path.join(root, dir);
    if (!existsSync(full)) continue;
    for (const f of readdirSync(full).sort()) {
      if (f.endsWith('.html')) list.push({ rel: `${dir}/${f.replace(/\.html$/, '')}`, kind: dir });
    }
  }
  return list;
}

function mdFiles(dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const name of readdirSync(dir).sort()) {
    const full = path.join(dir, name);
    if (statSync(full).isDirectory()) out.push(...mdFiles(full));
    else if (name.endsWith('.md')) out.push(full);
  }
  return out;
}

export function build() {
  const sections = [];
  for (const p of pageList()) {
    const file = path.join(root, `${p.rel}.html`);
    if (!existsSync(file)) continue;
    const html = readFileSync(file, 'utf8');
    if (!/<html[^>]*\blang="en/i.test(html)) continue; // English pages only
    // Sourced parent guides (scripts/articles) go in as a pointer, never as full text: the chat links the
    // guide and leaves the health figures on the page, next to their sources. It also keeps the file small.
    const articleMeta = path.join(root, 'scripts', 'articles', `${path.basename(p.rel)}.json`);
    if (p.kind === 'guides' && existsSync(articleMeta)) {
      const meta = JSON.parse(readFileSync(articleMeta, 'utf8'));
      sections.push({
        key: p.rel,
        kind: 'page',
        text: `URL: ${urlFor(p.rel)}\n## ${titleOf(html, p.rel)}\n\nA sourced parent guide. ${meta.description} For questions on this topic, link this guide and do not restate its figures.`,
      });
      continue;
    }
    const text = htmlToText(html);
    sections.push({ key: p.rel, kind: p.kind, text: `URL: ${urlFor(p.rel)}\n## ${titleOf(html, p.rel)}\n\n${text}` });
  }
  const llms = path.join(root, 'llms.txt');
  if (existsSync(llms)) {
    const text = readFileSync(llms, 'utf8').replace(/ [—–] /g, ', ').trim();
    sections.push({ key: 'llms.txt', kind: 'page', text: `URL: ${SITE}/llms.txt\n## llms.txt (the site summary)\n\n${text}` });
  }
  const notes = mdFiles(SOURCE_DIR).map((f) => ({
    key: path.relative(SOURCE_DIR, f),
    kind: 'notes',
    text: `## Team notes: ${path.relative(SOURCE_DIR, f)}\n\n${readFileSync(f, 'utf8').trim()}`,
  }));

  const dropped = [];
  const total = () => [...sections, ...notes].reduce((n, s) => n + s.text.length + 2, 0);
  for (const kind of ['guides', 'compare']) {
    while (total() > MAX_CHARS) {
      const pool = sections.filter((s) => s.kind === kind);
      if (!pool.length) break;
      const biggest = pool.reduce((a, b) => (b.text.length > a.text.length ? b : a));
      sections.splice(sections.indexOf(biggest), 1);
      dropped.push(biggest.key);
    }
  }
  const text = [...sections, ...notes].map((s) => s.text).join('\n\n');
  return { text, dropped, pages: sections.map((s) => s.key), notes: notes.map((n) => n.key) };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const { text, dropped, pages, notes } = build();
  writeFileSync(
    OUT,
    '// GENERATED by scripts/build-chat-knowledge.mjs. Do not edit by hand.\n' + `export const KNOWLEDGE = ${JSON.stringify(text)};\n`,
  );
  console.log(`pages (${pages.length}): ${pages.join(', ')}`);
  console.log(`notes (${notes.length}): ${notes.join(', ') || 'none'}`);
  console.log(`knowledge: ${text.length} characters, about ${Math.round(text.length / 4)} tokens`);
  console.log(dropped.length ? `dropped to stay under ${MAX_CHARS}: ${dropped.join(', ')}` : `nothing dropped (limit ${MAX_CHARS} characters)`);
}
