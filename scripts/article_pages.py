"""Parent guides (2026-11): one scripts/articles/<slug>.json + <slug>.body.html pair per guide.

Loaded here so build-content.py can treat them like any other PAGES entry. A guide with invalid JSON,
missing required keys or no body file is skipped with a warning on stderr, never a crash.
"""
import json
import html
import re
import sys
from pathlib import Path

ARTICLES_DIR = Path(__file__).resolve().parent / "articles"
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


def _load():
    pages, queries, citations = [], {}, {}
    for json_path in sorted(ARTICLES_DIR.glob("*.json")):
        body_path = json_path.with_suffix(".body.html")
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as error:
            _warn(f"{json_path.name}: invalid JSON ({error})")
            continue
        if not isinstance(data, dict):
            _warn(f"{json_path.name}: not a JSON object")
            continue
        if not body_path.is_file():
            _warn(f"{json_path.name}: no {body_path.name}")
            continue
        missing = [key for key in REQUIRED if key not in data]
        if missing:
            _warn(f"{json_path.name}: missing keys {', '.join(missing)}")
            continue
        try:
            body = body_path.read_text(encoding="utf-8")
        except OSError as error:
            _warn(f"{body_path.name}: unreadable ({error})")
            continue
        body = _TABLE.sub(lambda m: '<div class="table-wrap">' + _label_cells(m.group(1)) + "</div>", body)
        page = {key: data[key] for key in REQUIRED}
        page.update({
            "active": data.get("active", "resources"),
            "guide": True,
            "article": True,
            "body": body,
            "faqs": [tuple(item) for item in data.get("faqs", [])],
            "related": [tuple(item) for item in data.get("related", [])],
        })
        pages.append(page)
        queries[data["slug"]] = data.get("queries", [])
        if data.get("citations"):
            citations[data["slug"]] = data["citations"]
    pages.sort(key=lambda page: page["slug"])
    return pages, queries, citations


ARTICLES, ARTICLE_QUERIES, ARTICLE_CITATIONS = _load()

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
