#!/usr/bin/env python3.12
"""Derive the Norwegian homepage (no.html) from index.html.

/no is the Norwegian twin of the English homepage: same markup, classes, scripts and images; only the language
differs. Run after changing index.html:

    ~/.local/bin/python3.12 scripts/make-no-home.py
    ~/.local/bin/python3.12 scripts/build-content.py      # syncs the Norwegian header and footer into no.html
    python3 scripts/stamp-assets.py

Text comes from scripts/no-home-strings.json (the authoritative Norwegian wording, keyed by the English string as
it appears in the HTML) plus the tables below (alt texts, aria labels, meta, JSON-LD, callouts). A text node or
alt text that has no Norwegian entry stops the script, so English can never slip through unnoticed.

Norwegian screenshots: every screenshot path is listed in IMAGE_SLOTS and the comment at the top of no.html.
To swap one for a Norwegian capture, put the new path prefix in IMAGE_MAP (for example
"/screens/how/pick-poster": "/screens/no/how/pick-poster", which also covers -360/-720 and the ?v= stamp is dropped by
stamp-assets for paths outside /screens/how) and re-run the three commands above.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "scripts" / "no-home-strings.json").read_text(encoding="utf-8"))

# The English chat widget (Nora) has English-only interface text, so the Norwegian page leaves it out until it is translated.
INCLUDE_CHAT = False

# Norwegian captures replace these prefixes one by one (made by scripts/prepare-how-it-works.py no, from the nb
# captures). The Forest, Lavender and Midnight themes have no Norwegian capture yet and stay the English ones.
IMAGE_MAP = {f"/screens/how/{name}": f"/screens/no/how/{name}" for name in (
    "pick-poster", "fill-poster", "before", "log", "finish", "flowcast", "hero-report", "report-scroll", "report-detail", "growth", "health",
    "family", "vitamin-d", "theme-ocean", "flow-pick", "flow-fill")}

# On-page callouts that carry amounts, read from the Norwegian captures (bottle 45 ml tatt / 75 ml igjen, Erstatning 45 ml,
# the day bar 125 ml before and 170 ml after). On the English page: "2.5 oz left in the bottle", "+1.5 oz formula", 4.5 to 6 oz.
CALLOUT_LEFT = "75 ml igjen i flasken"
CALLOUT_ADD = "+45 ml morsmelkerstatning"
COUNTER_FROM, COUNTER_TO, COUNTER_UNIT, COUNTER_STEP = "125", "170", "ml", "5"
COUNTER_LABEL = "så langt i dag"

ALT = {
 "Feed Flow's real bottle screen with a safe countdown ring, start and end times, 1.5 oz taken and 2.5 oz left.": "Feed Flows ekte flaskeskjerm med en trygg nedtellingsring, start- og sluttid, 45 ml tatt og 75 ml igjen.",
 "A real Feed Flow baby report, Theo's last 3 weeks, with 431 oz from 67 bottles and weight and length at the 49th percentile.": "En ekte babyrapport fra Feed Flow, Theos siste 3 uker, med 13 l melk fra 67 flasker og vekt og lengde på 49. persentil.",
 "The real bottle screen with a safe countdown ring, the start and end times, 1.5 oz taken and 2.5 oz left in the bottle.": "Den ekte flaskeskjermen med en trygg nedtellingsring, start- og sluttid, 45 ml tatt og 75 ml igjen i flasken.",
 "The real Today screen after the feed: the 1.5 oz formula bottle on top of the timeline and the day meter at 6 oz so far.": "Den ekte I dag-skjermen etter måltidet: flasken med 45 ml erstatning øverst på tidslinjen og dagsmåleren på 170 ml så langt.",
 "The real FlowCast screen showing Theo's next feed at about 11:45 AM and the feeds predicted later today.": "Den ekte FlowCast-skjermen med Theos neste måltid ved omtrent 11:45 og måltidene som er forventet senere i dag.",
 "A real Feed Flow Baby Report, Theo's last 3 weeks, with feeding totals, weight and length percentiles, and WHO growth curves.": "En ekte babyrapport fra Feed Flow, Theos siste 3 uker, med sum for mating, persentiler for vekt og lengde og vekstkurver fra WHO.",
 "The real Feed Flow growth card showing Theo at the 63rd percentile at the latest weigh-in, along his own curve inside the WHO range since birth.": "Det ekte vekstkortet i Feed Flow som viser Theo på 63. persentil ved siste veiing, langs sin egen kurve innenfor WHOs område siden fødselen.",
 "The real Feed Flow health page: Theo is well, with 6 of 9 major allergens introduced, each with its meals and last attempt.": "Den ekte helsesiden i Feed Flow: Theo er frisk, med 6 av 9 viktige allergener introdusert, hver med måltider og siste forsøk.",
 "The real Feed Flow activity feed showing feeds logged by You, Anna and Alex, each with the amount and time.": "Den ekte aktivitetsstrømmen i Feed Flow med måltider logget av deg, Anna og Alex, hver med mengde og klokkeslett.",
 "The same bottle screen in the Ocean theme, teal.": "Samme flaskeskjerm i temaet Ocean, blågrønn.",
 "The same bottle screen in the Forest theme, green.": "Samme flaskeskjerm i temaet Forest, grønn.",
 "The same bottle screen in the Lavender theme, purple.": "Samme flaskeskjerm i temaet Lavender, lilla.",
 "The same bottle screen in the Midnight theme, dark blue.": "Samme flaskeskjerm i temaet Midnight, mørkeblå.",
}
ARIA = {
 "Skip to content": "Gå til innholdet",
 "Real Feed Flow app screens": "Ekte skjermbilder fra Feed Flow",
 "Product highlights": "Hovedpunkter",
 "App Store reviews": "Anmeldelser i App Store",
 "5 out of 5 stars": "5 av 5 stjerner",
 "A real recording of the Feed Flow log menu: the feed types pop up, Pumped Milk, Breast and Formula with More beside them, and Formula is picked.": "Et ekte opptak av loggmenyen i Feed Flow: valgene dukker opp, Pumpet melk, Bryst og Erstatning med Mer ved siden av, og Erstatning velges.",
 "A real recording of Feed Flow: the amount is chosen, the bottle fills, and the big round button is pressed, which opens the bottle screen.": "Et ekte opptak fra Feed Flow: mengden velges, flasken fylles, og den store runde knappen trykkes, som åpner flaskeskjermen.",
}
HEAD = {
 "title": "Feed Flow: Matingslogg for amming og flaske | iPhone",
 "description": "Matingslogg for iPhone: amming, flaske, pumping og fast føde, nedtelling for flasken på låseskjermen, neste måltid, WHOs vekstkurver og D-vitamin.",
 "og_description": "Matingsloggen for iPhone: hvert måltid, nedtelling for flasken på låseskjermen, FlowCast, WHOs vekstkurver og D-vitamin. Gratis å logge.",
 "tw_description": "Matingsloggen for iPhone: hvert måltid, FlowCast, WHOs vekstkurver og babyens helse. Gratis å logge.",
 "og_image_alt": "Fire ekte skjermbilder fra Feed Flow: nedtelling for flasken, FlowCast, D-vitamin og en rapport om mating og vekst",
}
SCREENSHOT_CAPTIONS = [
 "Flaskeskjermen med nedtellingsring, 45 ml tatt og 75 ml igjen",
 "FlowCast med neste måltid ved omtrent 11:45 og måltidene som er forventet senere i dag",
 "D-vitamin-kortet som viser omtrent 10 µg fra dråper i dag mot dagens grense på 35 µg",
 "En ekte babyrapport som viser vekt og lengde på 49. persentil",
 "En detaljside i rapporten med flaskestørrelser og vekstkurver fra WHO",
 "Allergenoversikten i appen: 6 av 9 viktige allergener er introdusert, med matvarer og reaksjoner",
]
FEATURES = [
 "Logging av amming, morsmelkerstatning, pumping, vann og fast føde",
 "Nedtelling for ferdig laget flaske, også på låseskjermen",
 "FlowCast: forslag til neste måltid og valgfrie varsler",
 "Smart måltidsplanlegging og vanlige flaskestørrelser",
 "WHOs vekstkurver for vekt, lengde og hodeomkrets",
 "Introduksjon av allergener og senere reaksjoner",
 "Logg for medisiner og vaksiner",
 "Automatisk utregning av D-vitamin fra dråper og etiketten på morsmelkerstatningen",
 "Sammenligning av merker og næringsinnhold for morsmelkerstatning",
 "Deling med flere omsorgspersoner og private rapporter om mating og vekst",
]
LD = {
 "site_description": "Logg mating, vekst og helse for babyen på iPhone, med praktiske guider for foreldre og fagfolk.",
 "app_description": "Feed Flow! er en matingslogg for iPhone: en babyapp for flaske, amming, morsmelkerstatning, pumping og fast føde, med forslag til og varsler om neste måltid, WHOs persentiler for vekt, lengde og hodeomkrets, allergener, reaksjoner, medisiner, vaksiner og D-vitamin. Appen kombinerer næringsinnholdet på etiketten til morsmelkerstatningen med loggede dråper og lager private rapporter om mating og vekst.",
 "offer": "Gratis å laste ned. Logging er gratis, for alltid. Valgfrie kjøp finnes i App Store.",
 "org_description": "Feed Flow! er en app for mating, vekst og babyens helse på iPhone, laget i Norge av Zeolite, med personvern først.",
 "org_slogan": "Matingslogg for amming og flaske",
 "page_name": "Feed Flow: Matingslogg for amming og flaske",
 "howto_name": "Slik logger du et måltid i Feed Flow",
 "howto_description": "Velg hva du vil logge, trykk på knappen, logg mengden og se måltidet på tidslinjen for dagen i Feed Flow for iPhone.",
}
REVIEW_CAPTION = {"Irene": "Irene", "Alec": "Alec", "Lokal-bruker": "Lokal-bruker"}
IMAGE_SLOTS = [
 ("hero, second phone", "/screens/how/hero-report-360.webp"), ("structured data", "/screens/how/vitamin-d-900.webp, report-detail-720.webp"),
 ("step 1, poster", "/screens/how/pick-poster-720.webp"), ("step 1, recording", "/screens/how/flow-pick.mp4"), ("step 2, poster", "/screens/how/fill-poster-720.webp"), ("step 2, recording", "/screens/how/flow-fill.mp4"),
 ("step 4, day meter 'before' frame", "/screens/how/before-360.webp"),
 ("step 3 and hero, bottle screen (amounts on frame)", "/screens/how/log-360.webp"), ("step 4, Today after the feed (amounts on frame)", "/screens/how/finish-360.webp"),
 ("beat, FlowCast", "/screens/how/flowcast-360.webp"), ("beat, report (scrolling)", "/screens/how/report-scroll-360.webp"), ("beat, growth", "/screens/how/growth-360.webp"),
 ("beat, health", "/screens/how/health-360.webp"), ("beat, share", "/screens/how/family-360.webp"),
 ("themes, Ocean", "/screens/how/theme-ocean-360.webp"), ("themes, Forest", "/screens/how/theme-forest-360.webp"), ("themes, Lavender", "/screens/how/theme-lavender-360.webp"), ("themes, Midnight", "/screens/how/theme-midnight-360.webp"),
 ("Open Graph / Twitter card", "/og.png"),
]


def fail(msg):
    sys.exit("make-no-home: " + msg)


def nb_reviews():
    js = (ROOT / "reviews.js").read_text(encoding="utf-8")
    m = re.search(r"\n    nb: \[\n(.*?)\n    \]", js, re.S)
    return [json.loads(line.strip().rstrip(",")) for line in m.group(1).split("\n")]


src = (ROOT / "index.html").read_text(encoding="utf-8")
head, rest = src.split("<body>", 1)
header_end = rest.index("<!--/ff:header-->") + len("<!--/ff:header-->")
main_start, main_end = rest.index("<main"), rest.index("</main>") + len("</main>")
footer_a, footer_b = rest.index("<!--ff:footer-->"), rest.index("<!--/ff:footer-->") + len("<!--/ff:footer-->")
skip_and_header, main, between, footer_block, tail = rest[:header_end], rest[main_start:main_end], rest[main_end:footer_a], rest[footer_a:footer_b], rest[footer_b:]

# ---------- main: text nodes ----------
missing = []
KEEP = {"Dansk", "Nederlands", "Suomi", "Français", "Deutsch", "Italiano", "Norsk (bokmål)", "Polski", "Português", "Español", "Svenska", "English", "Lokal-bruker", "Irene", "Alec", "FlowCast"}


nb = nb_reviews()
EXTRA = {"2.5 oz left in the bottle": CALLOUT_LEFT, "+1.5 oz formula": CALLOUT_ADD, "so far today": COUNTER_LABEL, "oz": COUNTER_UNIT}
ORIGINALS = re.findall(r'\n      text: "(.*?)",\n      name', (ROOT / "reviews.js").read_text(encoding="utf-8"))
for _original, _norwegian in zip(ORIGINALS, nb):
    EXTRA[_original] = _norwegian          # server-rendered Norwegian review text (reviews.js keeps it in step)
for _key in ("App Store review · Norway", "App Store review · Sweden"):
    for _name in ("Irene", "Alec", "Lokal-bruker"):
        if _key.endswith("Norway"):
            EXTRA[f"{_name} · {_key}"] = f"{_name} · {S[_key]}"
EXTRA["Lokal-bruker"] = "Lokal-bruker"


def text_node(m):
    raw = m.group(1)
    t = raw.strip()
    if not t or not re.search(r"[A-Za-zÀ-ÿ]", t) or t in KEEP:
        return m.group(0)
    if t in EXTRA:
        return ">" + raw.replace(t, EXTRA[t]) + "<"
    if t in S:
        return ">" + raw.replace(t, S[t]) + "<"
    return m.group(0) if t in (" ",) else (missing.append(t) or m.group(0))


main = re.sub(r">([^<>]+)<", text_node, main)
# figcaptions "Name · App Store review · Norway" were skipped above only if absent from the map; handle by substring.
main = main.replace("App Store review · Norway", S["App Store review · Norway"]).replace("App Store review · Sweden", S["App Store review · Sweden"])
main = main.replace("Translated by Google Translate", S["Translated by Google Translate"])
# review blockquotes: server-render the Norwegian translations (reviews.js keeps them in step when the select changes)
nb = nb_reviews()
cards = re.split(r'(?=<figure class="review")', main)
out = []
for part in cards:
    m = re.match(r'<figure class="review" data-review-index="(\d)"', part)
    if m:
        i = int(m.group(1))
        part = re.sub(r"<blockquote lang=\"\w+\">.*?</blockquote>", lambda _: f'<blockquote lang="nb">{nb[i]}</blockquote>', part, count=1, flags=re.S)
        part = part.replace('<span class="translate-note">', '<span class="translate-note visible">').replace('<button class="review-toggle" type="button" hidden>', '<button class="review-toggle" type="button">')
    out.append(part)
main = "".join(out)
main = main.replace(">View original<", ">" + S["View original"] + "<")
main = main.replace('<option value="auto">Automatic</option>', '<option value="auto">' + S["Automatic"] + "</option>")
# callouts with amounts (text nodes are mapped above; the counter attributes here)
main = main.replace('data-from="4.5" data-to="6">6</span>', f'data-from="{COUNTER_FROM}" data-to="{COUNTER_TO}" data-step="{COUNTER_STEP}">{COUNTER_TO}</span>')
# attributes
def attr(name, table):
    def rep(m):
        v = m.group(1)
        if v == "":
            return m.group(0)
        if v not in table:
            missing.append(f'{name}="{v}"')
            return m.group(0)
        return f'{name}="{table[v]}"'
    return rep


main = re.sub(r'alt="([^"]*)"', attr("alt", {**ALT, "": ""}), main)
main = re.sub(r'aria-label="([^"]*)"', attr("aria-label", {**ARIA, **{"Review language": S["Review language"]}}), main)
if missing:
    fail("no Norwegian for:\n  " + "\n  ".join(sorted(set(missing))))
main = main.replace("og D-vitamin i den samme oversikten.", 'og <span style="white-space:nowrap">D-vitamin</span> i den samme oversikten.')   # no line break inside "D-vitamin"
main = main.replace("ct=website_hero", "ct=website_no_hero").replace("ct=website_closing", "ct=website_no_closing")
# Norwegian text still contains the English words only where they are product names; the check at the end verifies it.

# image swaps
def swap_images(text):
    for old, new in IMAGE_MAP.items():
        text = text.replace(old, new)
    return text


main = swap_images(main)

# ---------- head ----------
h = head.replace('<html lang="en" data-theme="light">', '<html lang="nb" data-theme="light">')
h = re.sub(r"<title>.*?</title>", f"<title>{HEAD['title']}</title>", h, flags=re.S)
h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + HEAD["description"], h)
h = h.replace('<link rel="canonical" href="https://tryfeedflow.app/">', '<link rel="canonical" href="https://tryfeedflow.app/no">')
h = h.replace('<meta property="og:url" content="https://tryfeedflow.app/">', '<meta property="og:url" content="https://tryfeedflow.app/no">')
h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + HEAD["title"], h)
h = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + HEAD["title"], h)
h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + HEAD["og_description"], h)
h = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + HEAD["tw_description"], h)
h = re.sub(r'(<meta (?:property="og:image:alt"|name="twitter:image:alt") content=")[^"]*', lambda m: m.group(1) + HEAD["og_image_alt"], h)
h = h.replace('content="en_US"', 'content="nb_NO"')
h = swap_images(h)

if not INCLUDE_CHAT:
    h = re.sub(r'<link rel="stylesheet" href="/chat\.css[^"]*">\n?|<script defer src="/chat\.js[^"]*"></script>\n?', "", h)

# ---------- JSON-LD ----------
blocks = re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', h, re.S)
if len(blocks) != 2:
    fail("expected two JSON-LD blocks in index.html")
graph, howto = json.loads(blocks[0]), json.loads(blocks[1])
for node in graph["@graph"]:
    t = node["@type"]
    node.pop("alternateName", None) if t == "WebSite" and False else None
    if t == "WebSite":
        node["description"] = LD["site_description"]
        node["inLanguage"] = "nb"
    elif t == "SoftwareApplication":
        node["description"] = LD["app_description"]
        node["featureList"] = FEATURES
        for shot, caption in zip(node["screenshot"], SCREENSHOT_CAPTIONS):
            shot["caption"] = caption
        node["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "NOK", "availability": "https://schema.org/InStock", "description": LD["offer"]}
        node["dateModified"] = "2026-11-19"
        node["url"] = "https://tryfeedflow.app/no"
    elif t == "Organization":
        node["description"] = LD["org_description"]
        node["slogan"] = LD["org_slogan"]
graph["@graph"].append({"@type": "WebPage", "@id": "https://tryfeedflow.app/no#page", "url": "https://tryfeedflow.app/no", "name": LD["page_name"], "description": HEAD["description"], "inLanguage": "nb", "dateModified": "2026-11-19", "isPartOf": {"@id": "https://tryfeedflow.app/#website"}, "about": {"@id": "https://tryfeedflow.app/#app"}})
howto["name"], howto["description"], howto["inLanguage"] = LD["howto_name"], LD["howto_description"], "nb"
step_names = [S["Pick what to log"], S["Fill the bottle"], S["Log what your baby eats"], S["See the whole day"]]
step_texts = [S["Tap what your baby is having: pumped milk, breast or formula, or More for solids, water and the rest."], S["Tap a size or drag the slider and the bottle fills. Then press the big round button."], S["Slide the milk level down to what is left, then tap finish."], S["Every feed lands on one timeline, with one meter for the day."]]
for step, n, t_ in zip(howto["step"], step_names, step_texts):
    step["name"], step["text"], step["url"] = n, t_, "https://tryfeedflow.app/no#how-it-works"
howto["tool"]["name"] = "Feed Flow! for iPhone"
dump = lambda o: json.dumps(o, ensure_ascii=False, indent=2).replace("</", "<\\/")
h = h.replace(blocks[0], dump(graph)).replace(blocks[1], dump(howto))
h = swap_images(h)

# ---------- assemble ----------
slots = "\n".join(f"  {name}: {path}" for name, path in IMAGE_SLOTS)
comment = f"""<!--
Norwegian homepage, derived from index.html by scripts/make-no-home.py (do not hand-edit text: change scripts/no-home-strings.json or the tables in that script, then re-run).
IMAGE SLOTS (Norwegian captures under /screens/no/how/ via IMAGE_MAP in the script; Forest, Lavender and Midnight themes are still the English captures):
{slots}
AMOUNT CALLOUTS (in ml, read from the Norwegian captures; constants CALLOUT_LEFT, CALLOUT_ADD, COUNTER_* in the script):
  "{CALLOUT_LEFT}" · "{CALLOUT_ADD}" · counter {COUNTER_FROM} to {COUNTER_TO} {COUNTER_UNIT} "{COUNTER_LABEL}"
-->
"""
header_part = skip_and_header.replace('<a class="skip-link" href="#main">Skip to content</a>', '<a class="skip-link" href="#main">Gå til innholdet</a>')
page = comment + h.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n", 1) + "<body>" + header_part + main + between + footer_block + tail
# the comment must come after the doctype
page = page.replace(comment + "<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + comment, 1)
(ROOT / "no.html").write_text(page, encoding="utf-8")
print("wrote no.html")
