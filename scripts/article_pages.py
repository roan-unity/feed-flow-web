"""Parent guides (2026-11): one scripts/articles/<slug>.json + <slug>.body.html pair per guide.

Loaded here so build-content.py can treat them like any other PAGES entry. A guide with invalid JSON,
missing required keys or no body file is skipped with a warning on stderr, never a crash.
"""
import json
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://tryfeedflow.app"
ARTICLES_DIR = Path(__file__).resolve().parent / "articles"
ES_DIR = ARTICLES_DIR / "es"
REQUIRED = ("slug", "file", "title", "description", "eyebrow", "h1", "intro", "image", "srcset", "width", "height", "alt", "date")
_TABLE = re.compile(r'(<table\b[^>]*class="[^"]*\bdata-table\b[^"]*"[^>]*>.*?</table>)', re.S)


def _label_cells(table):
    """Give every body cell a data-label with its column heading, so a phone can show each row as a
    stacked card (site.css) instead of a table that scrolls sideways and hides its last column."""
    head = re.search(r"<thead>(.*?)</thead>", table, re.S)
    if not head:
        return table
    labels = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th\b[^>]*>(.*?)</th>", head.group(1), re.S)]

    def row(match):
        index = -1

        def cell(c):
            nonlocal index
            index += 1
            label = labels[index] if index < len(labels) else ""
            return f'<{c.group(1)} data-label="{html.escape(label, quote=True)}"{c.group(2)}>'

        return re.sub(r"<(td|th)\b([^>]*)>", cell, match.group(0))

    body = re.search(r"<tbody>.*?</tbody>", table, re.S)
    if not body:
        return table
    return table.replace(body.group(0), re.sub(r"<tr\b[^>]*>.*?</tr>", row, body.group(0), flags=re.S))


def _warn(message):
    print(f"article_pages: skipped {message}", file=sys.stderr)


def _note(message):
    print(f"article_pages: warning: {message}", file=sys.stderr)


def _read(json_path, folder_label):
    """One validated guide dict (raw JSON plus a body string), or None after a warning."""
    body_path = json_path.with_suffix(".body.html")
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        _warn(f"{json_path.name}: invalid JSON ({error})")
        return None
    if not isinstance(data, dict):
        _warn(f"{json_path.name}: not a JSON object")
        return None
    if not body_path.is_file():
        _warn(f"{json_path.name}: no {body_path.name}")
        return None
    missing = [key for key in REQUIRED if key not in data]
    if missing:
        _warn(f"{json_path.name}: missing keys {', '.join(missing)}")
        return None
    try:
        body = body_path.read_text(encoding="utf-8")
    except OSError as error:
        _warn(f"{body_path.name}: unreadable ({error})")
        return None
    data["_body"] = _TABLE.sub(lambda m: '<div class="table-wrap">' + _label_cells(m.group(1)) + "</div>", body)
    return data


def _hero_ok(hero, where):
    """A hero is used only when its 1200 px file is on disk; otherwise warn and render no figure."""
    if not hero:
        return False
    if not hero.startswith("/") or not hero.endswith("-1200.webp"):
        _note(f"{where}: hero must look like /images/guides/<name>-1200.webp, got {hero!r}")
        return False
    if not (ROOT / hero.lstrip("/")).is_file():
        _note(f"{where}: hero image {hero} not found on disk, no figure rendered")
        return False
    return True


def _load():
    english, spanish = {}, {}
    for json_path in sorted(ARTICLES_DIR.glob("*.json")):
        data = _read(json_path, "en")
        if data:
            english[data["slug"]] = data
    if ES_DIR.is_dir():
        for json_path in sorted(ES_DIR.glob("*.json")):
            data = _read(json_path, "es")
            if data:
                spanish[data["slug"]] = data

    pages_en, pages_es, queries, citations = [], [], {}, {}

    def build(data, lang):
        page = {key: data[key] for key in REQUIRED}
        page.update({
            "active": data.get("active", "resources"),
            "guide": True,
            "article": True,
            "body": data["_body"],
            "faqs": [tuple(item) for item in data.get("faqs", [])],
            "related": [tuple(item) for item in data.get("related", [])],
        })
        if lang == "es":
            page.update({"lang": "es", "ui": "es"})
        queries[data["slug"]] = data.get("queries", [])
        if data.get("citations"):
            citations[data["slug"]] = data["citations"]
        return page

    for slug, data in english.items():
        page = build(data, "en")
        if _hero_ok(data.get("hero"), data["slug"]):
            page["hero"], page["hero_alt"] = data["hero"], data.get("hero_alt", "")
        pages_en.append(page)
    by_slug = {page["slug"]: page for page in pages_en}

    for slug, data in spanish.items():
        page = build(data, "es")
        original = data.get("translation_of")
        if original not in by_slug:
            _note(f"{data['slug']}: translation_of {original!r} is not an English guide, so no hreflang pair and no inherited hero")
            original = None
        hero = data.get("hero") or (by_slug[original].get("hero") if original else None)
        if hero and _hero_ok(hero, data["slug"]):
            page["hero"] = hero
            page["hero_alt"] = data.get("hero_alt", "")
            if not page["hero_alt"]:
                _note(f"{data['slug']}: hero without its own hero_alt, using an empty alt")
        if original:
            page["translation_of"] = original
            pair = [("en", f"{SITE}/{original}"), ("es", f"{SITE}/{page['slug']}"), ("x-default", f"{SITE}/{original}")]
            page["hreflang"] = pair
            by_slug[original].setdefault("hreflang", pair)
        pages_es.append(page)

    pages_en.sort(key=lambda page: page["slug"])
    pages_es.sort(key=lambda page: page["slug"])
    return pages_en, pages_es, queries, citations


ARTICLES, ES_ARTICLES, ARTICLE_QUERIES, ARTICLE_CITATIONS = _load()


def _es_index():
    """The Spanish guides index at /es/guias, only when at least one Spanish guide exists."""
    if not ES_ARTICLES:
        return []
    cards = resource_cards(ES_ARTICLES)
    return [{
        "slug": "es/guias", "file": "es/guias.html", "active": "resources", "lang": "es", "ui": "es", "guide": False, "es_index": True,
        "date": max(page["date"] for page in ES_ARTICLES),
        "title": "Guías para alimentar a tu bebé | Feed Flow",
        "description": "Guías claras sobre lactancia, fórmula, biberón, sólidos y alérgenos, con las fuentes de salud enlazadas y las cifras explicadas paso a paso.",
        "eyebrow": "Guías en español", "h1": "Guías para alimentar a tu bebé",
        "intro": "Respuestas cortas a las dudas de cada toma, con la fuente oficial al lado de cada cifra.",
        "image": "/screens/nordic/es-03-360.webp", "srcset": "/screens/nordic/es-03-360.webp 1x, /screens/nordic/es-03-720.webp 2x", "width": 360, "height": 780,
        "alt": "Feed Flow en español: la pantalla de hoy con la última toma, la próxima toma y los biberones del día.",
        "body": f'<section id="guias"><div class="resource-grid">{cards}</div></section>',
        "faqs": [], "related": [("/es", "Feed Flow en español")],
    }]


# feature page slug -> [(article slug, link text)]; a link is added only when that article exists.
ARTICLE_LINKS = {
    "bottle-countdown": [("breast-milk-storage", "How long breast milk can sit out")],
    "breastfeeding-pumping": [
        ("breast-milk-storage", "How long breast milk can sit out"),
        ("is-my-baby-eating-enough", "Is my baby eating enough?"),
    ],
    "formula-feeding": [
        ("how-much-formula-by-age", "How much formula by age"),
        ("paced-bottle-feeding", "How paced bottle feeding works"),
        ("switching-formula", "How to switch baby formula"),
    ],
    "flowcast": [("newborn-feeding-schedule", "What a newborn feeding schedule looks like")],
    "combo-feeding": [
        ("combination-feeding", "How to combination feed"),
        ("paced-bottle-feeding", "How paced bottle feeding works"),
    ],
    "solids-allergens": [
        ("starting-solids", "When and how to start solids"),
        ("introducing-allergens", "When to introduce peanut, egg and other allergens"),
        ("water-for-babies", "When babies can drink water"),
    ],
    "growth-development": [("is-my-baby-eating-enough", "Is my baby eating enough?")],
    "baby-report": [("is-my-baby-eating-enough", "Is my baby eating enough?")],
}
_ARROW = '<svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg>'


def inject_article_links(pages):
    """Append one plain text-link per existing article to the feature pages above (idempotent)."""
    existing = {page["slug"] for page in ARTICLES}
    for page in pages:
        for article_slug, label in ARTICLE_LINKS.get(page["slug"], []):
            href = f"/guides/{article_slug}"
            if f"guides/{article_slug}" not in existing or f'href="{href}"' in page["body"]:
                continue
            link = f'<a class="text-link" href="{href}">{label} {_ARROW}</a>'
            head, sep, tail = page["body"].rpartition("</section>")
            if sep:
                page["body"] = head + link + sep + tail
            else:
                page["body"] += link


def resource_cards(articles=None):
    """Cards for the /resources guides grid, same markup as the hand-written ones."""
    cards = []
    for page in articles if articles is not None else ARTICLES:
        title = page["title"].rsplit(" | ", 1)[0]
        blurb = page["description"]
        if len(blurb) > 150:
            blurb = blurb[:150].rsplit(" ", 1)[0].rstrip(",;:") + "…"
        tag = page["eyebrow"].replace(" guide", "")
        cards.append(
            f'<a class="resource-card" href="/{page["slug"]}"><span class="tag">{tag}</span><h3>{title}</h3><p>{blurb}</p>{_ARROW}</a>'
        )
    return "".join(cards)


ES_INDEX = _es_index()
