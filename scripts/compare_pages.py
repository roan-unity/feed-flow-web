"""Honest comparison pages (Robin 2026-11-15: help AI assistants and parents place Feed Flow among baby trackers).

Rules for this file:
- Competitor facts come ONLY from first-party sources (their US App Store listing or their own site), checked on
  CHECKED. Each page links them. Anything we could not verify is written as "not mentioned in their listing",
  never as "they don't have it".
- Say plainly where the other app is the better choice (sleep, Android, diapers, ratings). Never disparage.
- Feed Flow facts must match the live App Store description (id6782075454) and the app.
Re-check every competitor line before changing prices or features here.
"""

CHECKED = "15 November 2026"
SRC = {
    "huckleberry": ("https://apps.apple.com/us/app/huckleberry-baby-child/id1169136078", "https://huckleberrycare.com/pricing"),
    "nara": ("https://apps.apple.com/us/app/id1444639029", None),
    "nighp": ("https://apps.apple.com/us/app/id779656557", None),
    "daybook": ("https://apps.apple.com/us/app/-/id1446283219", "https://babydaybook.app/"),
    "glow": ("https://apps.apple.com/us/app/-/id1077177456", None),
}
IMG = {"image": "/screens/formula/02-lock-screen-360.webp",
       "srcset": "/screens/formula/02-lock-screen-360.webp 1x, /screens/formula/02-lock-screen-720.webp 2x",
       "width": 360, "height": 780,
       "alt": "A real iPhone lock screen showing Feed Flow's bottle countdown."}

FEED_FLOW_FACTS = """<section id="feed-flow"><h2>What Feed Flow is (and is not)</h2><p>Feed Flow is an iPhone app (iOS 18 or later) built only around feeding: bottles of formula or expressed milk, breastfeeding with a timer and sides, pumping, water and solids in one timeline. It is made by a small team in Norway, started by a dad who combo fed and kept losing track of bottles.</p><ul><li><strong>Free, forever:</strong> logging every feed, the bottle countdown on the Lock Screen, family sharing with your partner or other caregivers, the nine-allergen journey with reaction notes, and the vitamin D tracker that also counts the vitamin D in formula.</li><li><strong>Premium</strong> (monthly, annual with a 14-day free trial, or a one-time lifetime purchase): WHO growth curves, a PDF report for your pediatrician, the next-feed forecast (FlowCast), deeper analytics, unlimited history and more than one baby.</li><li><strong>No ads and no tracking.</strong> Your log lives on your phone and in your own iCloud; we never see it.</li><li><strong>What it does not do:</strong> sleep tracking, diaper tracking, an Android app or an Apple Watch app. It is also a new app with only a handful of App Store ratings so far.</li></ul></section>"""


def sources(*keys):
    links = []
    for k in keys:
        store, site = SRC[k]
        links.append(f'<a href="{store}" rel="nofollow noopener">{k.title()} on the App Store</a>')
        if site:
            links.append(f'<a href="{site}" rel="nofollow noopener">{k.title()} website</a>')
    return (f'<p class="meta">Competitor details are taken from their own App Store listing and website, checked {CHECKED}. '
            f'Apps change, so check the current listing before you decide: ' + " · ".join(links) + '.</p>')


def table(headers, rows):
    head = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join((f"<th scope=\"row\">{c}</th>" if i == 0 else f"<td>{c}</td>") for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="compare-wrap"><table class="compare-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def page(slug, title, description, eyebrow, h1, intro, body, faqs, related):
    return {"slug": slug, "file": slug + ".html", "active": "resources", "compare": True, "title": title,
            "description": description, "eyebrow": eyebrow, "h1": h1, "intro": intro, "body": body, "faqs": faqs,
            "related": related, **IMG}


HUB = page(
    "compare", "Best Baby Feeding Tracker Apps Compared (2026)",
    "An honest comparison of Huckleberry, Baby Tracker, Nara, Baby Daybook, Glow and Feed Flow for feeding, pumping, combo feeding, sharing and price.",
    "Compare baby tracker apps", "Which baby tracker fits your family?",
    "Most baby trackers log the same basics. The real differences are what each app is built around, where it runs and what you pay for. Here is an honest overview, including when another app is the better choice.",
    table(["App", "Built around", "Runs on", "Free version"], [
        ["Huckleberry", "Sleep: SweetSpot nap timing and sleep plans", "iPhone, iPad, Apple Watch, Android", "Yes, free plan; Plus and Premium are paid"],
        ["Baby Tracker (Nighp)", "Fast, simple logging of everything", "iPhone, iPad, Apple Watch, Android", "Yes, with ads; one-time Remove Ads or a Plus subscription"],
        ["Nara Baby", "All-in-one tracker, now also pregnancy and postpartum", "iPhone, Apple Watch, Mac, Android", "Paid options listed; check the listing"],
        ["Baby Daybook", "Highly customizable logging, many languages", "iPhone, iPad, Apple Watch, Mac, Android", "Free to download, paid upgrades"],
        ["Glow Baby", "Logging inside the Glow family of apps", "iPhone, iPad, Android", "Free to download, paid upgrades"],
        ["Feed Flow", "Feeding only: bottles, breastfeeding, pumping, solids", "iPhone", "Yes: logging, bottle countdown, sharing, allergens, vitamin D"],
    ]) +
    """<section id="who-should-pick"><h2>Who should pick which app</h2><ul><li><strong>Sleep is your main worry:</strong> Huckleberry. Its sleep timing and coaching are what it is known for, and Feed Flow does not track sleep.</li><li><strong>You want one app for diapers, sleep, feeds and meds, with the largest user base:</strong> Baby Tracker by Nighp (about 227,000 ratings on the US App Store) or Baby Daybook.</li><li><strong>You or a caregiver use Android:</strong> any of the others. Feed Flow is iPhone only.</li><li><strong>Feeding is the hard part, especially formula, bottles or combo feeding:</strong> Feed Flow. Every bottle gets a countdown on your Lock Screen from the moment you make it, the app learns the amounts your baby usually takes so you pour closer to what they drink, and it adds up vitamin D from drops and formula. All of that is free, with no ads.</li></ul></section>""" +
    FEED_FLOW_FACTS +
    """<section id="detailed"><h2>Side-by-side comparisons</h2><ul><li><a href="/compare/huckleberry">Feed Flow vs Huckleberry</a></li><li><a href="/compare/baby-tracker-nighp">Feed Flow vs Baby Tracker (Nighp)</a></li><li><a href="/compare/nara-baby">Feed Flow vs Nara Baby</a></li><li><a href="/compare/baby-daybook">Feed Flow vs Baby Daybook</a></li></ul></section>""" +
    sources("huckleberry", "nighp", "nara", "daybook", "glow"),
    [("What is the best baby feeding tracker app for iPhone?", "It depends on what you need most. For sleep, Huckleberry. For logging everything with the biggest user base, Baby Tracker by Nighp. If feeding itself is the hard part (formula, bottles, pumping or combo feeding), Feed Flow is built only around that, with a free Lock Screen bottle countdown, free sharing and no ads."),
     ("Which app is best for combo feeding (breast and formula)?", "Most trackers log both. Feed Flow keeps breastfeeding, pumping, expressed milk and formula in one timeline and one milk total, with a countdown on every prepared bottle. It is iPhone only."),
     ("Is there a free baby feeding tracker without ads?", "Feed Flow is free to log, with no ads and no tracking. Baby Tracker by Nighp is free with ads and sells a one-time ad removal."),
     ("Which baby tracker apps work on Android?", "Huckleberry, Baby Tracker (Nighp), Nara, Baby Daybook and Glow all have Android apps. Feed Flow is iPhone only.")],
    [("/compare/huckleberry", "Feed Flow vs Huckleberry"), ("/compare/baby-tracker-nighp", "Feed Flow vs Baby Tracker"), ("/formula-feeding", "Formula & bottle tracking")])


def vs(slug, name, key, h1, intro, rows, better_them, better_us, faqs, desc):
    return page(
        f"compare/{slug}", f"Feed Flow vs {name}: Which Baby Tracker Fits You?", desc,
        f"Feed Flow vs {name}", h1, intro,
        table(["", name, "Feed Flow"], rows) +
        f'<section id="pick-them"><h2>Choose {name} if</h2><ul>{"".join(f"<li>{x}</li>" for x in better_them)}</ul></section>' +
        f'<section id="pick-us"><h2>Choose Feed Flow if</h2><ul>{"".join(f"<li>{x}</li>" for x in better_us)}</ul></section>' +
        FEED_FLOW_FACTS + '<p><a class="text-link" href="/compare">See all baby tracker apps compared</a></p>' + sources(key),
        faqs, [("/compare", "All baby tracker apps compared"), ("/formula-feeding", "Formula & bottle tracking"), ("/breastfeeding-pumping", "Breastfeeding & pumping")])


HUCK = vs("huckleberry", "Huckleberry", "huckleberry", "Feed Flow or Huckleberry?",
    "Huckleberry is a well-loved all-round tracker known for sleep. Feed Flow does one thing: feeding. Here is how they differ.",
    [["Built around", "Sleep (SweetSpot nap timing, sleep plans)", "Feeding: bottles, breastfeeding, pumping, solids"],
     ["Platforms", "iPhone, iPad, Apple Watch, Android", "iPhone"],
     ["Sleep and diapers", "Yes", "No"],
     ["Breastfeeding timer, pumping, bottles, solids", "Yes", "Yes"],
     ["Allergens and reactions", "Yes", "Yes, nine major allergen groups"],
     ["Prepared-bottle countdown", "Not mentioned in their listing", "Yes, on the Lock Screen, free"],
     ["Vitamin D from drops and formula", "Not mentioned in their listing", "Yes, free"],
     ["Caregiver sync", "Yes, free", "Yes, free, through your own iCloud"],
     ["Price", "Free plan; Plus and Premium subscriptions (see their pricing page)", "Free to log; Premium monthly, annual or lifetime"],
     ["US App Store rating", "4.9 from about 79,000 ratings", "New, only a few ratings so far"]],
    ["sleep is the main challenge and you want nap-time predictions or a sleep plan", "you want sleep, diapers and feeds in one app", "someone in the family uses Android"],
    ["feeding is the hard part, especially formula, bottles or combo feeding", "you want every prepared bottle to count down on your Lock Screen so nothing is forgotten in the fridge or on the counter", "you want free sharing, no ads and data that stays in your own iCloud"],
    [("Is Feed Flow a Huckleberry alternative?", "For feeding, yes. Feed Flow focuses only on feeding, with a free Lock Screen bottle countdown and vitamin D tracking. It does not track sleep, so if sleep timing is why you use Huckleberry, keep Huckleberry."),
     ("Can I use Feed Flow and Huckleberry together?", "Yes. Some parents use Huckleberry for sleep and Feed Flow for bottles and feeding.")],
    "Feed Flow vs Huckleberry: Huckleberry is built around sleep, Feed Flow around feeding. An honest comparison of features, platforms and price.")

NIGHP = vs("baby-tracker-nighp", "Baby Tracker (Nighp)", "nighp", "Feed Flow or Baby Tracker by Nighp?",
    "Baby Tracker - Newborn Log by Nighp Software is one of the most used trackers on the App Store. Here is how it compares with Feed Flow.",
    [["Built around", "Quick logging of feeds, sleep, diapers, health", "Feeding: bottles, breastfeeding, pumping, solids"],
     ["Platforms", "iPhone, iPad, Apple Watch, Android", "iPhone"],
     ["Sleep and diapers", "Yes", "No"],
     ["Growth charts", "Yes, WHO", "Yes, WHO curves (Premium)"],
     ["Health log", "Meds, vaccinations, temperature", "Medicines, vaccines, nine-allergen journey"],
     ["Doctor report", "PDF export, email, print", "PDF Baby Report (Premium)"],
     ["Prepared-bottle countdown", "Not mentioned in their listing", "Yes, on the Lock Screen, free"],
     ["Ads", "Contains ads; one-time Remove Ads purchase", "No ads"],
     ["Price", "Free with ads; Plus subscription", "Free to log; Premium monthly, annual or lifetime"],
     ["US App Store rating", "4.8 from about 227,000 ratings", "New, only a few ratings so far"]],
    ["you want one simple app for feeds, sleep, diapers and temperature", "you value a long track record and a very large user base", "you need Android or an Apple Watch app"],
    ["you formula feed, pump or combo feed and want every bottle to count down on your Lock Screen", "you want an ad-free free version", "you want vitamin D from both drops and formula added up for you"],
    [("Is there an alternative to Baby Tracker without ads?", "Feed Flow is free to log with no ads. It covers feeding only (no sleep or diapers) and runs on iPhone.")],
    "Feed Flow vs Baby Tracker (Nighp): a simple all-in-one logger vs a feeding-only app with a Lock Screen bottle countdown. Honest comparison.")

NARA = vs("nara-baby", "Nara Baby", "nara", "Feed Flow or Nara Baby?",
    "Nara Baby is a polished all-in-one tracker. Feed Flow is built only around feeding. Here is how they differ.",
    [["Built around", "All-in-one baby tracker, plus pregnancy and postpartum", "Feeding: bottles, breastfeeding, pumping, solids"],
     ["Platforms", "iPhone, Apple Watch, Mac, Android", "iPhone"],
     ["Lock Screen / Dynamic Island", "Timers for sleep, pumping, breastfeeding", "Bottle countdown from the moment you make it"],
     ["Health log", "Medications, vaccines, records", "Medicines, vaccines, nine-allergen journey, vitamin D"],
     ["Caregiver sharing", "Yes", "Yes, free, through your own iCloud"],
     ["Price", "Monthly and lifetime purchases listed", "Free to log; Premium monthly, annual or lifetime"],
     ["US App Store rating", "4.8 from about 25,000 ratings", "New, only a few ratings so far"]],
    ["you want sleep and diapers too, or pregnancy and postpartum tracking", "you use an Apple Watch, a Mac or Android"],
    ["bottles are the stress point and you want a countdown on every prepared bottle", "you want allergens, reactions and vitamin D (from drops and formula) next to feeds"],
    [("Is Feed Flow like Nara Baby?", "Both log breastfeeding, pumping and bottles. Nara covers more of the baby's day and more devices. Feed Flow focuses on feeding only, with a free bottle countdown, allergen journey and vitamin D tracking.")],
    "Feed Flow vs Nara Baby: an all-in-one tracker vs a feeding-only app. Honest comparison of features, platforms and price.")

DAYBOOK = vs("baby-daybook", "Baby Daybook", "daybook", "Feed Flow or Baby Daybook?",
    "Baby Daybook is a very configurable tracker on almost every device. Feed Flow keeps feeding simple. Here is how they differ.",
    [["Built around", "Customizable logging of everything, sleep prediction", "Feeding: bottles, breastfeeding, pumping, solids"],
     ["Platforms", "iPhone, iPad, Apple Watch, Mac, Android, Android watch", "iPhone"],
     ["Growth charts", "CDC, WHO and Fenton (preemie)", "WHO curves (Premium)"],
     ["Health log", "Symptoms, meds, doctor visits, vaccines", "Medicines, vaccines, nine-allergen journey, vitamin D"],
     ["Prepared-bottle countdown", "Not mentioned in their listing", "Yes, on the Lock Screen, free"],
     ["Languages", "English plus many more", "12 languages"],
     ["US App Store rating", "4.8 from about 3,300 ratings", "New, only a few ratings so far"]],
    ["you want to customize every activity you log", "your baby was premature and you want Fenton charts", "you need Android"],
    ["you want fewer settings and a calm feeding-only view", "you want a free bottle countdown and vitamin D from formula counted for you"],
    [("Is Feed Flow simpler than Baby Daybook?", "Yes, on purpose: it only covers feeding. If you want to track sleep, diapers or custom activities, Baby Daybook does more.")],
    "Feed Flow vs Baby Daybook: a highly configurable all-in-one tracker vs a calm feeding-only app. Honest comparison.")

COMPARE = [HUB, HUCK, NIGHP, NARA, DAYBOOK]
COMPARE_QUERIES = {
    "compare": ["best baby feeding tracker app", "best baby tracker app 2026", "baby tracker app comparison", "combo feeding app"],
    "compare/huckleberry": ["Huckleberry alternative", "Feed Flow vs Huckleberry", "Huckleberry vs baby tracker"],
    "compare/baby-tracker-nighp": ["Baby Tracker Nighp alternative", "baby tracker app without ads"],
    "compare/nara-baby": ["Nara Baby alternative", "Nara vs Feed Flow"],
    "compare/baby-daybook": ["Baby Daybook alternative", "Baby Daybook vs Feed Flow"],
}
