#!/usr/bin/env python3
"""Stamp asset references in every HTML page with ?v=<content hash>.

The zone lets browsers keep scripts, styles and images for four hours, so a
changed file under the same name stays stale on a visitor's phone. The HTML
itself is always revalidated, so a hash in the URL makes the browser fetch the
new file at once. Run after any change to the files below, and after
scripts/build-content.py (it writes pages with a bare /site.css).
"""
import hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATTERN = re.compile(
    r'/(site\.css|chat\.css|chat\.js|how-it-works\.js|ambassador\.js|screens/(?:no/)?how/[\w-]+\.(?:webp|png|mp4))(?:\?v=[0-9a-f]+)?'
)
_cache = {}

def stamp(match):
    rel = match.group(1)
    if rel not in _cache:
        path = ROOT / rel
        _cache[rel] = hashlib.sha1(path.read_bytes()).hexdigest()[:8] if path.is_file() else None
    digest = _cache[rel]
    return f'/{rel}?v={digest}' if digest else f'/{rel}'

changed = 0
for page in ROOT.rglob('*.html'):
    if '.git' in page.parts or 'node_modules' in page.parts:
        continue
    text = page.read_text(encoding='utf-8')
    new = PATTERN.sub(stamp, text)
    if new != text:
        page.write_text(new, encoding='utf-8')
        changed += 1
print(f'stamped {changed} pages, {len([d for d in _cache.values() if d])} assets')
