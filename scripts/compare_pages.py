"""Comparison pages, kept to core differences we are sure of (Robin 2026-11-15: "a comparison FAQ about core
differences seems more safe").

Rules for this file:
- About another app we only state stable, high-confidence facts from its own App Store listing or website: what it is
  built around, whether it has an Android app, whether it also tracks sleep and diapers. No prices, no rating counts,
  no "they don't have X", no ads claims: those change or read as claims about a competitor.
- Feed Flow's own features are stated about Feed Flow only, never as something the others lack.
- Say plainly when the other app is the better choice. Never disparage.
- Feed Flow facts must match the live App Store description (id6782075454) and the app.
"""

CHECKED = "15 November 2026"
SRC = {
    "Huckleberry": "https://apps.apple.com/us/app/huckleberry-baby-child/id1169136078",
    "Nara Baby": "https://apps.apple.com/us/app/id1444639029",
    "Baby Tracker (Nighp)": "https://apps.apple.com/us/app/id779656557",
    "Baby Daybook": "https://apps.apple.com/us/app/-/id1446283219",
}
IMG = {"image": "/screens/formula/02-lock-screen-360.webp",
       "srcset": "/screens/formula/02-lock-screen-360.webp 1x, /screens/formula/02-lock-screen-720.webp 2x",
       "width": 360, "height": 780,
       "alt": "A real iPhone lock screen showing Feed Flow's bottle countdown."}

FEED_FLOW = """<section id="feed-flow"><h2>What Feed Flow is, and what it is not</h2><p>Feed Flow is an iPhone app built around feeding first: bottles of formula or expressed milk, breastfeeding with a timer and sides, pumping, water and solids in one timeline. It is made in Norway by a dad who combo fed and kept losing track of bottles.</p><ul><li><strong>Free:</strong> logging every feed, a countdown on every prepared bottle that stays on your Lock Screen, sharing with your partner or other caregivers, the nine-allergen journey with reaction notes, and a vitamin D tracker that also counts the vitamin D in formula. No ads.</li><li><strong>Premium</strong> (monthly, annual or lifetime): WHO growth curves, a PDF report for your pediatrician, the next-feed forecast, deeper analytics, unlimited history and more than one baby.</li><li><strong>Private:</strong> the log lives on your phone and in your own iCloud. We never see it.</li><li><strong>Not included:</strong> sleep tracking, diaper tracking, and apps for Android or Apple Watch.</li></ul></section>"""


def source_line(name):
    return (f'<p class="meta">About {name}: taken from its own App Store listing, checked {CHECKED}. Apps change, so '
            f'check <a href="{SRC[name]}" rel="nofollow noopener">the current listing</a> before you decide.</p>')


def page(slug, title, description, eyebrow, h1, intro, body, faqs, related):
    return {"slug": slug, "file": slug + ".html", "active": "resources", "compare": True, "title": title,
            "description": description, "eyebrow": eyebrow, "h1": h1, "intro": intro, "body": body, "faqs": faqs,
            "related": related, **IMG}


def ul(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


HUB = page(
    "compare", "Choosing a Baby Feeding Tracker App: Core Differences",
    "How Feed Flow differs from Huckleberry, Baby Tracker, Nara and Baby Daybook: what each app is built around, sleep, Android, and when another app fits better.",
    "Choosing a baby tracker", "Which baby tracker fits your family?",
    "Most baby trackers log the same basics. The real difference is what each app is built around. Here is an honest guide, including when another app is the better choice.",
    """<section id="core"><h2>The core differences</h2>""" + ul([
        "<strong>Huckleberry</strong> is built around sleep, with nap timing and sleep plans, and tracks feeds too. It has an Android app.",
        "<strong>Baby Tracker by Nighp</strong>, <strong>Nara Baby</strong> and <strong>Baby Daybook</strong> are all-in-one trackers for feeds, sleep, diapers and more, and have Android apps.",
        "<strong>Feed Flow</strong> is built around feeding first, with health tracking, growth and a Baby Report in the same app, on iPhone. It does not track sleep or diapers.",
    ]) + """</section><section id="who-should-pick"><h2>Who should pick which</h2>""" + ul([
        "<strong>Sleep is your main worry:</strong> Huckleberry.",
        "<strong>You want feeds, sleep and diapers in one app:</strong> one of the all-in-one trackers.",
        "<strong>Someone in the family uses Android:</strong> any of the others. Feed Flow is iPhone only.",
        "<strong>Feeding is the hard part, especially formula, bottles, pumping or combo feeding:</strong> Feed Flow. Every prepared bottle counts down on your Lock Screen, the app learns the amounts your baby usually takes so you pour closer to what they drink, and it adds up vitamin D from drops and formula. Free, with no ads.",
    ]) + "</section>" + FEED_FLOW +
    """<section id="detailed"><h2>App by app</h2><ul><li><a href="/compare/huckleberry">Feed Flow and Huckleberry</a></li><li><a href="/compare/baby-tracker-nighp">Feed Flow and Baby Tracker (Nighp)</a></li><li><a href="/compare/nara-baby">Feed Flow and Nara Baby</a></li><li><a href="/compare/baby-daybook">Feed Flow and Baby Daybook</a></li></ul></section>"""
    + f'<p class="meta">Details about other apps come from their own App Store listings, checked {CHECKED}. Apps change, so check the current listing before you decide.</p>',
    [("What is the best baby feeding tracker app for iPhone?", "It depends on what you need most. For sleep, Huckleberry. For feeds, sleep and diapers in one app, an all-in-one tracker such as Baby Tracker, Nara or Baby Daybook. If feeding itself is the hard part (formula, bottles, pumping or combo feeding), Feed Flow is built only around that, with a free Lock Screen bottle countdown, free sharing and no ads."),
     ("Which app is good for combo feeding (breast and formula)?", "Feed Flow keeps breastfeeding, pumping, expressed milk and formula in one timeline and one milk total, with a countdown on every prepared bottle. It is iPhone only."),
     ("Is there a free baby feeding tracker without ads?", "Feed Flow is free to log, with no ads and no tracking. Premium adds growth curves, a pediatrician report and the next-feed forecast."),
     ("Does Feed Flow track sleep or diapers?", "No. Feed Flow is built around feeding first, and also tracks health, growth and milestones, but not sleep or diapers. If you want sleep or diapers too, an all-in-one tracker or Huckleberry fits better, and some parents use one of those alongside Feed Flow.")],
    [("/compare/huckleberry", "Feed Flow and Huckleberry"), ("/formula-feeding", "Formula & bottle tracking"), ("/breastfeeding-pumping", "Breastfeeding & pumping")])


def vs(slug, name, h1, intro, core, them, us, faqs, desc):
    return page(
        f"compare/{slug}", f"Feed Flow or {name}? Core Differences", desc, f"Feed Flow and {name}", h1, intro,
        f'<section id="core"><h2>The core difference</h2>{ul(core)}</section>'
        f'<section id="pick-them"><h2>{name} fits better if</h2>{ul(them)}</section>'
        f'<section id="pick-us"><h2>Feed Flow fits better if</h2>{ul(us)}</section>' + FEED_FLOW +
        '<p><a class="text-link" href="/compare">How to choose a baby tracker</a></p>' + source_line(name),
        faqs, [("/compare", "Choosing a baby tracker"), ("/formula-feeding", "Formula & bottle tracking"), ("/breastfeeding-pumping", "Breastfeeding & pumping")])


HUCK = vs("huckleberry", "Huckleberry", "Feed Flow or Huckleberry?",
    "Huckleberry is a well-loved tracker known for sleep. Feed Flow does one thing: feeding.",
    ["Huckleberry is built around sleep (nap timing and sleep plans) and also tracks feeds, diapers and more, on iPhone and Android.",
     "Feed Flow is built around feeding first, with health and growth tracking, on iPhone, and does not track sleep."],
    ["sleep is the main challenge", "you want sleep, diapers and feeds in one app", "someone in the family uses Android"],
    ["feeding is the hard part, especially formula, bottles or combo feeding", "you want every prepared bottle to count down on your Lock Screen", "you want free sharing, no ads and data in your own iCloud"],
    [("Is Feed Flow a Huckleberry alternative?", "For feeding, it can be. Feed Flow focuses only on feeding. It does not track sleep, so if sleep is why you use Huckleberry, keep Huckleberry."),
     ("Can I use Feed Flow and Huckleberry together?", "Yes. Some parents use Huckleberry for sleep and Feed Flow for bottles and feeding.")],
    "Feed Flow or Huckleberry? Huckleberry is built around sleep, Feed Flow around feeding. The core differences, honestly.")

NIGHP = vs("baby-tracker-nighp", "Baby Tracker (Nighp)", "Feed Flow or Baby Tracker by Nighp?",
    "Baby Tracker - Newborn Log by Nighp Software is one of the longest-running trackers on the App Store. Feed Flow focuses on feeding.",
    ["Baby Tracker is an all-in-one logger for feeds, sleep, diapers and health, on iPhone and Android.",
     "Feed Flow is built around feeding first, with health tracking, growth and a Baby Report in the same app, on iPhone."],
    ["you want one app for feeds, sleep, diapers and health", "you need Android"],
    ["you formula feed, pump or combo feed and want every bottle to count down on your Lock Screen", "you want vitamin D from drops and formula added up for you", "you want a free version with no ads"],
    [("How is Feed Flow different from Baby Tracker?", "Baby Tracker covers more of the baby's day. Feed Flow covers only feeding, with a free Lock Screen bottle countdown, an allergen journey and vitamin D tracking.")],
    "Feed Flow or Baby Tracker (Nighp)? An all-in-one logger and a feeding-first app. The core differences, honestly.")

NARA = vs("nara-baby", "Nara Baby", "Feed Flow or Nara Baby?",
    "Nara Baby is a polished all-in-one tracker. Feed Flow is built around feeding first, with health and growth tracking.",
    ["Nara Baby tracks feeds, sleep, diapers and more, and also covers pregnancy and postpartum, on iPhone and Android.",
     "Feed Flow is built around feeding first, with health tracking, growth and a Baby Report in the same app, on iPhone."],
    ["you want sleep and diapers too, or pregnancy and postpartum tracking", "you need Android"],
    ["bottles are the stress point and you want a countdown on every prepared bottle", "you want allergens, reactions and vitamin D next to feeds"],
    [("How is Feed Flow different from Nara Baby?", "Nara covers more of the baby's day. Feed Flow focuses on feeding first, with a free bottle countdown, allergen journey and vitamin D tracking.")],
    "Feed Flow or Nara Baby? An all-in-one tracker and a feeding-first app. The core differences, honestly.")

DAYBOOK = vs("baby-daybook", "Baby Daybook", "Feed Flow or Baby Daybook?",
    "Baby Daybook is a very configurable all-in-one tracker. Feed Flow keeps feeding simple.",
    ["Baby Daybook tracks feeds, sleep, diapers, health and custom activities, on iPhone and Android.",
     "Feed Flow is built around feeding first, with health and growth tracking, on iPhone, with fewer settings on purpose."],
    ["you want to customize every activity you log", "you want sleep and diapers too", "you need Android"],
    ["you want a calm feeding-first view", "you want a free bottle countdown and vitamin D from formula counted for you"],
    [("Is Feed Flow simpler than Baby Daybook?", "Yes, on purpose: it is built around feeding first, with health and growth tracking. If you want sleep, diapers or custom activities, Baby Daybook does more.")],
    "Feed Flow or Baby Daybook? A configurable all-in-one tracker and a calm feeding-first app. The core differences, honestly.")

COMPARE = [HUB, HUCK, NIGHP, NARA, DAYBOOK]
COMPARE_QUERIES = {
    "compare": ["best baby feeding tracker app", "best baby tracker app 2026", "baby tracker app comparison", "combo feeding app"],
    "compare/huckleberry": ["Huckleberry alternative", "Feed Flow vs Huckleberry", "Huckleberry vs baby tracker"],
    "compare/baby-tracker-nighp": ["Baby Tracker Nighp alternative", "baby tracker app without ads"],
    "compare/nara-baby": ["Nara Baby alternative", "Nara vs Feed Flow"],
    "compare/baby-daybook": ["Baby Daybook alternative", "Baby Daybook vs Feed Flow"],
}
