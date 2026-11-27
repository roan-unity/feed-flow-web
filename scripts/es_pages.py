"""Spanish feature, compare and FAQ pages under /es/ (2026-11-27, Robin: "Let's add Spanish first").

One scripts/pages-es/<name>.json + <name>.body.html pair per page, each a full translation of one English page
("translation_of" holds the English slug). Facts must stay identical to the English page: when the English page
changes, change the Spanish pair in the same commit. Image fields are inherited from the English page.

Links are written with the English paths in the source files and remapped here, so a link always lands on the
Spanish page when one exists. A link that still leads to an English page says so ("en inglés").
"""
from pathlib import Path
import json
import re

DIR = Path(__file__).resolve().parent / "pages-es"
SITE = "https://tryfeedflow.app"
DATE = "2026-11-27"

# The hand-written FAQ (faq.html) and its Spanish twin (es/preguntas-frecuentes.html, also hand-written).
FAQ_EN, FAQ_ES = "faq", "es/preguntas-frecuentes"
FAQ_TITLE = "Preguntas frecuentes sobre Feed Flow"

# Header and menu for every Spanish page. "{en}" is replaced by the English twin of the page being built.
DESKTOP_NAV_ES = [("feeding", "/es/alimentacion-con-formula", "Alimentación"), ("growth", "/es/crecimiento-y-desarrollo", "Crecimiento"),
                  ("health", "/es/salud-del-bebe", "Salud"), ("resources", "/es/guias", "Guías"), ("faq", "/es/preguntas-frecuentes", "Preguntas"), ("en", "{en}", "English")]
MENU_GROUPS_ES = [
    ("Alimentación", [("/es/alimentacion-con-formula", "Fórmula y biberones"), ("/es/lactancia-y-extraccion", "Lactancia y extracción"), ("/es/solidos-y-alergenos", "Sólidos y alérgenos")]),
    ("Crecimiento y salud", [("/es/crecimiento-y-desarrollo", "Crecimiento y desarrollo"), ("/es/salud-del-bebe", "Salud del bebé"), ("/es/informe-del-bebe", "Informe del bebé")]),
    ("Guías y ayuda", [("/es/guias", "Guías"), ("/es/comparar", "Comparar apps"), ("/es/preguntas-frecuentes", "Preguntas frecuentes"), ("/es#printable", "Registro para imprimir")]),
    ("Idioma", [("/es", "Inicio en español"), ("{en}", "English")]),
]
FT_ES_HEADINGS = {"product": "Producto", "learn": "Aprende", "company": "Feed Flow", "languages": "Idiomas"}
# Footer links that have a Spanish page: English path -> (Spanish path, label). The rest keep their English label.
FT_ES = {
    "/formula-feeding": ("/es/alimentacion-con-formula", "Fórmula y biberones"),
    "/breastfeeding-pumping": ("/es/lactancia-y-extraccion", "Lactancia y extracción"),
    "/solids-allergens": ("/es/solidos-y-alergenos", "Sólidos y alérgenos"),
    "/growth-development": ("/es/crecimiento-y-desarrollo", "Crecimiento y desarrollo"),
    "/baby-health": ("/es/salud-del-bebe", "Salud del bebé"),
    "/baby-report": ("/es/informe-del-bebe", "Informe del bebé"),
    "/compare": ("/es/comparar", "Comparar apps"),
    "/faq": ("/es/preguntas-frecuentes", "Preguntas frecuentes"),
}
_SVG = '<svg class="icon"'


def _read():
    items = []
    for json_path in sorted(DIR.glob("*.json")):
        data = json.loads(json_path.read_text(encoding="utf-8"))
        body_path = json_path.with_name(json_path.name[: -len(".json")] + ".body.html")
        data["_body"] = body_path.read_text(encoding="utf-8").strip()
        items.append(data)
    return items


def build(pages_en, es_articles):
    """Returns (Spanish pages, queries, url map). Also sets the hreflang pair on each English twin."""
    by_slug = {page["slug"]: page for page in pages_en}
    items = _read()
    url_map = {"/" + d["translation_of"]: "/" + d["slug"] for d in items}
    url_map["/" + FAQ_EN] = "/" + FAQ_ES
    url_map["/resources"] = "/es/guias"
    for article in es_articles:
        if article.get("translation_of"):
            url_map["/" + article["translation_of"]] = "/" + article["slug"]

    def spanish(path):
        return url_map.get(path)

    def remap_anchor(match):
        head, path, frag, rest, text = match.group(1), match.group(2), match.group(3) or "", match.group(4), match.group(5)
        if spanish(path):
            return f'{head}{spanish(path)}{frag}{rest}{text}</a>'
        if path.startswith("/printables/") or path.startswith("/es"):
            return match.group(0)
        mark = " (en inglés)"
        at = text.find(_SVG)
        text = (text[:at].rstrip() + mark + " " + text[at:]) if at >= 0 else text.rstrip() + mark
        return f'{head}{path}{frag}{rest}{text}</a>'

    pages, queries = [], {}
    for data in items:
        original = by_slug[data["translation_of"]]
        body = re.sub(r'(<a\b[^>]*?href=")(/[^"#]*)(#[^"]*)?("[^>]*>)(.*?)</a>', remap_anchor, data["_body"], flags=re.S)
        related = [(spanish(link) or link, label if (spanish(link) or link.startswith("/es")) else f"{label} (en inglés)") for link, label in data["related"]]
        pair = [("en", f"{SITE}/{original['slug']}"), ("es", f"{SITE}/{data['slug']}"), ("x-default", f"{SITE}/{original['slug']}")]
        page = {
            "slug": data["slug"], "file": data["slug"] + ".html", "lang": "es", "ui": "es", "es_page": True, "date": DATE,
            "active": original["active"], "translation_of": original["slug"], "hreflang": pair,
            "title": data["title"], "description": data["description"], "eyebrow": data["eyebrow"], "h1": data["h1"], "intro": data["intro"],
            "image": original["image"], "srcset": original["srcset"], "width": original["width"], "height": original["height"], "alt": data["alt"],
            "body": body, "faqs": [tuple(item) for item in data["faqs"]], "related": related,
        }
        if original.get("compare"):
            page["compare"] = True
        original["hreflang"] = pair
        original["es_twin"] = "/" + data["slug"]
        queries[data["slug"]] = data.get("queries", [])
        pages.append(page)
    return pages, queries, url_map


def home_section(pages):
    """A grid on /es that links every Spanish feature page, the FAQ and the compare hub."""
    cards = []
    for page in pages:
        if page.get("compare") and page["slug"] != "es/comparar":
            continue
        title = page["title"].rsplit(" | ", 1)[0]
        cards.append(f'<a class="resource-card" href="/{page["slug"]}"><span class="tag">{page["eyebrow"]}</span><h3>{title}</h3><p>{page["description"]}</p>{_SVG} aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a>')
    cards.append(f'<a class="resource-card" href="/{FAQ_ES}"><span class="tag">Preguntas</span><h3>{FAQ_TITLE}</h3><p>Respuestas sobre el registro de tomas, la cuenta regresiva del biberón, FlowCast, la privacidad y qué incluye Premium.</p>{_SVG} aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a>')
    cards.append(f'<a class="resource-card" href="/es/guias"><span class="tag">Guías</span><h3>Guías para alimentar a tu bebé</h3><p>Respuestas cortas a las dudas de cada toma, con la fuente oficial al lado de cada cifra.</p>{_SVG} aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a>')
    return f'<section id="mas"><h2>Conoce Feed Flow a fondo</h2><div class="resource-grid">{"".join(cards)}</div></section>'
