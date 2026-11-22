#!/usr/bin/env python3
"""App Store ratings per country, on the homepage (Robin 2026-11-22: "aggregate the new ratings that we have and
also print country of origin and present these on our web page").

Reads Apple's public lookup for every storefront (rating count and average per country; no key, no personal data),
writes ratings.json and rewrites the block between <!-- ratings:start --> and <!-- ratings:end --> in index.html and
no.html, plus aggregateRating in the homepage's structured data. Nothing is rounded up: the average is weighted by
count and shown with one decimal. Changes nothing when Apple answers for fewer than 30 storefronts.
Run: python3 scripts/update_ratings.py [--check]   (--check prints, writes nothing)"""
import concurrent.futures as cf, datetime as dt, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_ID = "6782075454"
STORES = ("ae ag ai al am ao ar at au az bb be bf bg bh bj bm bn bo br bs bt bw by bz ca cg ch cl cn co cr cv cy cz "
          "de dk dm do dz ec ee eg es fi fj fm fr gb gd gh gm gr gt gw gy hk hn hr hu id ie il in is it jm jo jp ke "
          "kg kh kn kr kw ky kz la lb lc lk lr lt lu lv md mg mk ml mn mo mr ms mt mu mw mx my mz na ne ng ni nl no "
          "np nz om pa pe pg ph pk pl pt pw py qa ro ru sa sb sc se sg si sk sl sn sr st sv sz tc td th tj tm tn tr "
          "tt tw tz ua ug us uy uz vc ve vg vn ye za zw").split()
NAMES = {"us": ("United States", "USA"), "gb": ("United Kingdom", "Storbritannia"), "no": ("Norway", "Norge"),
         "se": ("Sweden", "Sverige"), "dk": ("Denmark", "Danmark"), "fi": ("Finland", "Finland"),
         "fr": ("France", "Frankrike"), "de": ("Germany", "Tyskland"), "es": ("Spain", "Spania"),
         "it": ("Italy", "Italia"), "nl": ("Netherlands", "Nederland"), "be": ("Belgium", "Belgia"),
         "ie": ("Ireland", "Irland"), "pt": ("Portugal", "Portugal"), "pl": ("Poland", "Polen"),
         "ch": ("Switzerland", "Sveits"), "at": ("Austria", "Østerrike"), "ca": ("Canada", "Canada"),
         "au": ("Australia", "Australia"), "nz": ("New Zealand", "New Zealand"), "mx": ("Mexico", "Mexico"),
         "co": ("Colombia", "Colombia"), "ar": ("Argentina", "Argentina"), "cl": ("Chile", "Chile"),
         "pe": ("Peru", "Peru"), "ve": ("Venezuela", "Venezuela"), "ec": ("Ecuador", "Ecuador"),
         "br": ("Brazil", "Brasil"), "in": ("India", "India"), "sg": ("Singapore", "Singapore"),
         "za": ("South Africa", "Sør-Afrika"), "ae": ("United Arab Emirates", "De forente arabiske emirater"),
         "ph": ("Philippines", "Filippinene"), "jp": ("Japan", "Japan"), "kr": ("South Korea", "Sør-Korea"),
         "il": ("Israel", "Israel"), "tr": ("Türkiye", "Tyrkia"), "gr": ("Greece", "Hellas"),
         "is": ("Iceland", "Island"), "ee": ("Estonia", "Estland"), "cz": ("Czechia", "Tsjekkia")}
MONTHS_NB = "januar februar mars april mai juni juli august september oktober november desember".split()
TEXT = {"en": {"label": "App Store ratings by country", "line": "{n} ratings from {c} countries",
               "one": "1 rating from 1 country", "date": "Counted in the App Store on {d}.", "of": "out of 5"},
        "nb": {"label": "Vurderinger i App Store per land", "line": "{n} vurderinger fra {c} land",
               "one": "1 vurdering fra 1 land", "date": "Talt i App Store {d}.", "of": "av 5"}}


def lookup(code):
    try:
        url = f"https://itunes.apple.com/lookup?id={APP_ID}&country={code}"
        res = json.loads(urllib.request.urlopen(url, timeout=20).read()).get("results") or []
        return code, (int(res[0].get("userRatingCount") or 0), float(res[0].get("averageUserRating") or 0)) if res else (0, 0.0)
    except Exception:
        return code, None


def collect(fetch=lookup, stores=STORES):
    with cf.ThreadPoolExecutor(8) as pool:
        got = dict(pool.map(fetch, stores))
    answered = {c: v for c, v in got.items() if v is not None}
    rows = sorted(((c, n, avg) for c, (n, avg) in answered.items() if n > 0), key=lambda r: (-r[1], r[0]))
    total = sum(n for _, n, _ in rows)
    return {"answered": len(answered), "total": total,
            "average": round(sum(n * avg for _, n, avg in rows) / total, 2) if total else 0,
            "countries": [{"code": c, "count": n, "average": round(avg, 2)} for c, n, avg in rows]}


def flag(code):
    return "".join(chr(0x1F1E6 + ord(ch) - 97) for ch in code)


def block(data, lang, today):
    t, i = TEXT[lang], 0 if lang == "en" else 1
    date = today.strftime("%-d %B %Y") if lang == "en" else f"{today.day}. {MONTHS_NB[today.month - 1]} {today.year}"
    n, c = data["total"], len(data["countries"])
    score = f"{data['average']:.1f}" if lang == "en" else f"{data['average']:.1f}".replace(".", ",")
    stars = "★" * round(data["average"]) + "☆" * (5 - round(data["average"]))
    line = t["one"] if (n, c) == (1, 1) else t["line"].format(n=n, c=c)
    items = "".join(f'<li><span class="rating-flag" aria-hidden="true">{flag(r["code"])}</span>'
                    f'<span class="rating-country">{NAMES.get(r["code"], (r["code"].upper(),) * 2)[i]}</span>'
                    f'<b>{r["count"]}</b></li>' for r in data["countries"])
    return (f'<div class="rating-summary"><div class="rating-score"><strong>{score}</strong>'
            f'<div><div class="stars" aria-label="{score} {t["of"]}">{stars}</div><p>{line}</p></div></div>'
            f'<ul class="rating-countries" aria-label="{t["label"]}">{items}</ul>'
            f'<p class="rating-date">{t["date"].format(d=date)}</p></div>')


def apply(html, data, lang, today):
    html, n = re.subn(r"(<!-- ratings:start -->).*?(<!-- ratings:end -->)",
                      lambda m: m.group(1) + block(data, lang, today) + m.group(2), html, flags=re.S)
    if not n:
        raise SystemExit("no <!-- ratings:start --> marker in the page")
    rating = (f'"aggregateRating": {{"@type": "AggregateRating", "ratingValue": "{data["average"]:.1f}", '
              f'"ratingCount": "{data["total"]}", "bestRating": "5", "worstRating": "1"}},')
    html = re.sub(r'[ \t]*"aggregateRating": \{[^}]*\},\n', "", html)
    return re.sub(r'(\n([ \t]*)"@type": "SoftwareApplication",\n)', lambda m: m.group(1) + m.group(2) + rating + "\n", html, count=1)


def main():
    data = collect()
    if data["answered"] < 30 or not data["total"]:
        raise SystemExit(f"Apple answered for {data['answered']} storefronts, {data['total']} ratings: nothing changed")
    print(json.dumps(data, ensure_ascii=False))
    if "--check" in sys.argv:
        return
    old = json.loads((ROOT / "ratings.json").read_text()) if (ROOT / "ratings.json").exists() else {}
    if old.get("countries") == data["countries"]:
        print("ratings unchanged")
        return
    today = dt.date.today()
    data["counted"] = today.isoformat()
    (ROOT / "ratings.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    for page, lang in (("index.html", "en"), ("no.html", "nb")):
        p = ROOT / page
        p.write_text(apply(p.read_text(encoding="utf-8"), data, lang, today), encoding="utf-8")
    print("ratings updated")


if __name__ == "__main__":
    main()
