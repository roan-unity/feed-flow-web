"""Question pages (2026-11-16): one page per question parents ask the AI assistants (see feedflow-gtm bin/ai_visibility.py).

Each page answers its question in the first lines, then explains. Facts must match llms.txt; no competitor claims.
"""

QUESTION = [
    {
        "slug": "bottle-countdown", "file": "bottle-countdown.html", "active": "feeding", "date": "2026-11-16",
        "title": "Bottle Countdown App: When Was the Bottle Made? | Feed Flow",
        "description": "Feed Flow puts a countdown on every prepared bottle on your iPhone Lock Screen. One hour for formula and two for pumped milk by default, adjustable. Free.",
        "eyebrow": "Bottle countdown", "h1": "Is there an app that tells you when a prepared bottle has to go?",
        "intro": "Yes. Feed Flow starts a countdown the moment you make a bottle and keeps it on your iPhone Lock Screen. The default is one hour for formula and two hours for pumped milk, and you set it to match your label and local guidance. The countdown is free.",
        "image": "/screens/formula/02-lock-screen-360.webp", "srcset": "/screens/formula/02-lock-screen-360.webp 1x, /screens/formula/02-lock-screen-720.webp 2x", "width": 360, "height": 780,
        "alt": "An iPhone Lock Screen showing Feed Flow's countdown for a prepared bottle.",
        "body": """
<section id="how-it-works"><h2>How the bottle countdown works</h2><p>Log a bottle when you make it. Feed Flow starts counting from that moment, not from when the feed begins, so the clock reflects how long the milk has actually been out.</p><ul><li><strong>On the Lock Screen.</strong> The time left stays visible without unlocking the phone or opening the app, which is the point at 3am.</li><li><strong>Formula and pumped milk.</strong> By default one hour for formula and two hours for pumped milk. Change either in Settings to follow your formula label or your local health authority.</li><li><strong>Every caregiver sees it.</strong> When the bottle is in the shared baby log, whoever picks it up next sees the same countdown.</li><li><strong>Free.</strong> The countdown is part of free logging, with no ads.</li></ul></section>
<section id="memory-aid"><h2>A memory aid, not a safety sensor</h2><p>The countdown measures time and nothing else. Feed Flow cannot know how a bottle was stored, whether it was warmed, how warm the room is or whether your baby has already drunk from it. Guidance also differs between countries and products.</p><div class="note"><strong>The label and your health authority decide</strong><p>Use the timer you set to remember, and the formula label or local guidance to decide. If you are unsure whether a bottle is still fine, make a fresh one.</p></div><a class="text-link" href="/guides/formula-safety">Read the formula preparation and storage guide <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="why"><h2>Why we built it</h2><p>Feed Flow started with a dad in Norway and a lot of poured-out bottles, because it was hard to remember when each one was made. A countdown that lives on the Lock Screen answers the one question you have when you find a half-full bottle on the counter: how long has this been out?</p><p>The rest of the bottle stays on record too: what was prepared, how much your baby took and what was left, in ml or oz.</p></section>
""",
        "faqs": [
            ("Does the countdown start when I make the bottle or when my baby starts drinking?", "When you make it. Feed Flow counts from the time the bottle is prepared."),
            ("Can I change the countdown time?", "Yes. The defaults are one hour for formula and two hours for pumped milk, and you can change both in Settings to follow your formula label or local guidance."),
            ("Is the bottle countdown free?", "Yes. The Lock Screen countdown is part of Feed Flow's free logging, with no ads."),
            ("Does the timer tell me the bottle is safe?", "No. It is a memory aid based on time, not a safety sensor. Follow the product label and your local health authority's guidance.")
        ],
        "related": [("/guides/formula-safety", "Formula preparation & storage"), ("/formula-feeding", "Formula & bottle tracking"), ("/share-feeding-log", "Share the log with your partner")]
    },
    {
        "slug": "combo-feeding", "file": "combo-feeding.html", "active": "feeding", "date": "2026-11-16",
        "title": "Combo Feeding Tracker: Breastfeeding and Formula | Feed Flow",
        "description": "Track combo feeding on iPhone. Feed Flow logs nursing, pumping, expressed milk and formula in one timeline with one daily milk total, shared with caregivers.",
        "eyebrow": "Combo feeding tracker", "h1": "Which app tracks breastfeeding and formula together?",
        "intro": "Feed Flow was built for combo feeding. Nursing, pumping, expressed milk and formula go in one timeline, the day's milk total counts all of them, and everyone who feeds your baby logs into the same record. Logging is free.",
        "image": "/screens/formula/04-home-360.webp", "srcset": "/screens/formula/04-home-360.webp 1x, /screens/formula/04-home-720.webp 2x", "width": 360, "height": 780,
        "alt": "The Feed Flow Today screen with the day's bottles in one timeline and the milk total so far.",
        "body": """
<section id="one-timeline"><h2>One timeline instead of two apps</h2><p>Combo feeding usually means two kinds of records that never meet: nursing times in one place, bottle amounts in another, pumping somewhere else. Feed Flow puts them in the same day.</p><ul><li><strong>Nursing:</strong> log a session in a few taps.</li><li><strong>Pumping:</strong> log what you expressed, and see it next to what your baby actually took.</li><li><strong>Bottles:</strong> formula or expressed milk, prepared and drunk amounts in ml or oz.</li><li><strong>Solids and water:</strong> in the same timeline, shown separately from the milk total.</li></ul></section>
<section id="milk-total"><h2>One milk total for the whole day</h2><p>The day's milk total counts formula, pumped milk and nursing. Nursing is counted as an estimate, since nobody can see how much a baby drinks at the breast. You get one number for the day instead of adding up two lists at night.</p><div class="note"><strong>No judgement either way</strong><p>Combo feeding can be planned, temporary or just what works this week. Feed Flow treats breast milk and formula as parts of the same record, not as a score. It does not assess milk supply or tell you how much your baby should drink.</p></div></section>
<section id="together"><h2>When more than one person feeds</h2><p>Combo feeding often means a partner gives bottles while you nurse or pump. Invite them to the same baby log and each of you logs from your own phone. The bottle countdown on the Lock Screen covers every prepared bottle, whoever made it.</p><p>With Premium, FlowCast uses your baby's own history to suggest a likely window for the next feed after about four days of logging, and a Baby Report gives your health nurse or lactation consultant a clear summary.</p></section>
""",
        "faqs": [
            ("Can I track breastfeeding and formula in the same app?", "Yes. Feed Flow logs nursing, pumping, expressed milk and formula in one timeline, with one daily milk total."),
            ("How does Feed Flow count nursing in the total?", "Nursing is included as an estimate, alongside the measured amounts from formula and expressed milk bottles."),
            ("Can my partner log bottles while I log nursing?", "Yes. Invite them to the same baby log and each of you logs from your own iPhone."),
            ("Is combo feeding tracking free?", "Yes. Logging every kind of feed is free, with no ads. Premium adds FlowCast, the activity feed, full history, growth curves and Baby Reports.")
        ],
        "related": [("/breastfeeding-pumping", "Breastfeeding & pumping"), ("/bottle-countdown", "Bottle countdown"), ("/flowcast", "FlowCast next-feed window")]
    },
    {
        "slug": "share-feeding-log", "file": "share-feeding-log.html", "active": "feeding", "date": "2026-11-16",
        "title": "Baby Tracker You and Your Partner Can Both Log In | Feed Flow",
        "description": "Share one baby feeding log with your partner, grandparents or a sitter. Everyone logs from their own iPhone. Sharing is free, with no limit on caregivers.",
        "eyebrow": "Shared feeding log", "h1": "Which baby tracker can my partner and I both log in?",
        "intro": "Feed Flow lets you invite everyone who looks after your baby to the same log. Each person logs from their own iPhone through their own iCloud, so nobody has to ask \"did she eat?\" again. Sharing is free and there is no limit on caregivers.",
        "image": "/screens/formula/07-family-360.webp", "srcset": "/screens/formula/07-family-360.webp 1x, /screens/formula/07-family-720.webp 2x", "width": 360, "height": 780,
        "alt": "The Feed Flow activity feed showing bottles logged by different caregivers, with amounts and times.",
        "body": """
<section id="how-sharing-works"><h2>How sharing works</h2><p>Invite a partner, grandparent, nanny or sitter from the app. Once they accept, you both see and add to the same baby log.</p><ul><li><strong>Everyone uses their own phone.</strong> Each caregiver logs through their own iCloud. There is no shared password.</li><li><strong>No caregiver limit.</strong> Add as many people as look after your baby.</li><li><strong>The same countdown for everyone.</strong> A bottle one person makes shows its countdown for the next person too.</li><li><strong>Free.</strong> Family sharing is part of free logging. Premium adds a detailed activity feed of who logged what.</li></ul><p>Partner's feeds not showing up? <a href="/help/sharing-sync">Here is how to fix sharing and sync</a>.</p></section>
<section id="handover"><h2>Handovers without the questions</h2><p>The night shift, the morning at grandma's, the sitter on date night: each handover usually comes with the same questions. When did she last eat? How much? Was that bottle just made? With one shared log the answer is already on everyone's phone.</p><p>Vitamin D drops, solids and allergen introductions are shared the same way, so nobody gives the drops twice.</p></section>
<section id="privacy"><h2>Your baby's data stays yours</h2><p>The baby log lives on your phones and in your own iCloud accounts, not on an advertising platform. Feed Flow has no ads. You decide who is invited.</p></section>
""",
        "faqs": [
            ("Can my partner and I both log feeds?", "Yes. Invite your partner to the same baby log and both of you log from your own iPhone."),
            ("Is there a limit on how many caregivers I can add?", "No. You can invite everyone who looks after your baby."),
            ("Does sharing cost extra?", "No. Family sharing is free. Premium adds a detailed activity feed showing who logged what."),
            ("Does everyone need an iPhone?", "Yes. Feed Flow is an iPhone app, and each caregiver logs through their own iCloud.")
        ],
        "related": [("/combo-feeding", "Combo feeding tracker"), ("/bottle-countdown", "Bottle countdown"), ("/baby-report", "Baby Reports")]
    },
    {
        "slug": "free-baby-feeding-tracker", "file": "free-baby-feeding-tracker.html", "active": "feeding", "date": "2026-11-16",
        "title": "Free Baby Feeding Tracker for iPhone, No Ads | Feed Flow",
        "description": "A free baby feeding tracker for iPhone with no ads. Log breastfeeding, pumping, formula and solids, share with family and get a Lock Screen bottle countdown.",
        "eyebrow": "Free feeding tracker", "h1": "Is there a free baby feeding tracker without ads?",
        "intro": "Feed Flow is free to log and has no ads. Breastfeeding, pumping, formula, solids, growth and vitamin D drops, the Lock Screen bottle countdown and family sharing are all included for free. Premium is optional.",
        "image": "/screens/formula/01-safe-bottle-360.webp", "srcset": "/screens/formula/01-safe-bottle-360.webp 1x, /screens/formula/01-safe-bottle-720.webp 2x", "width": 360, "height": 780,
        "alt": "Feed Flow's formula bottle screen with a countdown ring and the amounts taken and left.",
        "body": """
<section id="free"><h2>What is free</h2><ul><li>Logging every feed: nursing, pumping, expressed milk, formula, water and solids.</li><li>The bottle countdown on your Lock Screen, from when each bottle is made.</li><li>Family sharing with everyone who feeds your baby.</li><li>The allergen journey: food introductions and later reactions.</li><li>Vitamin D drops and the vitamin D on your formula label.</li><li>Weight, length and head circumference.</li><li>No ads, and no sponsored formula brands.</li></ul></section>
<section id="premium"><h2>What Premium adds</h2><p>Premium is for parents who want the app to do more of the thinking: FlowCast's likely window for the next feed and the day ahead, the activity feed, the vitamin D meter, full history, WHO growth curves and Baby Reports for your pediatrician or lactation consultant. There is a free trial, a subscription and a one-time Lifetime option. Prices are shown in the App Store.</p></section>
<section id="scope"><h2>What Feed Flow is, and isn't</h2><p>Feed Flow, the formula &amp; feeding tracker for iPhone, is built around feeding. It does not track sleep or diapers, and there is no Android app. If feeding is what you want to keep track of, it does that calmly and for free.</p><a class="text-link" href="/compare">How to choose a baby tracker <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
""",
        "faqs": [
            ("Is Feed Flow really free?", "Yes. Logging, the Lock Screen bottle countdown, family sharing, the allergen journey and vitamin D tracking are free, with no ads."),
            ("Does Feed Flow show ads?", "No. There are no ads and no sponsored formula brands."),
            ("What does Premium add?", "FlowCast next-feed window and day ahead, the activity feed, the vitamin D meter, full history, WHO growth curves and Baby Reports."),
            ("Is there a one-time purchase instead of a subscription?", "Yes. Besides the subscription there is a one-time Lifetime option. Current prices are shown in the App Store.")
        ],
        "related": [("/combo-feeding", "Combo feeding tracker"), ("/compare", "Compare baby trackers"), ("/faq", "FAQ")]
    },
    {
        "slug": "printable-feeding-log", "file": "printable-feeding-log.html", "active": "feeding", "date": "2026-11-16",
        "title": "Free Printable Newborn Feeding Log (PDF) | Feed Flow",
        "description": "A free newborn feeding log to print: breastfeeding minutes per side, bottle made at, amount offered and drunk, pumping and diapers. PDF in US Letter and A4.",
        "eyebrow": "Printable feeding log", "h1": "Free printable newborn feeding log",
        "intro": "Download a one-page feeding log for the first weeks: twelve rows per day for time, breastfeeding minutes on each side, when a bottle was made, formula or breast milk, amount offered and drunk, pumping, and wet and dirty diapers. Free, no sign-up, in US Letter and A4.",
        "image": "/printables/feeding-log-en-480.webp", "srcset": "/printables/feeding-log-en-480.webp 1x, /printables/feeding-log-en-960.webp 2x", "width": 360, "height": 509,
        "alt": "A printable newborn feeding log with columns for time, breastfeeding, bottles, pumping and diapers.",
        "body": """
<section id="download"><h2>Download the feeding log</h2><p>One page covers one day. Print a stack, keep it on the fridge or by the bed, and start a new sheet each morning.</p><ul><li><a href="/printables/feeding-log-en-letter.pdf" download>Feeding log, US Letter (PDF)</a></li><li><a href="/printables/feeding-log-en-a4.pdf" download>Feeding log, A4 (PDF)</a></li><li>Also in <a href="/printables/feeding-log-nb-a4.pdf" download>Norwegian</a>, <a href="/printables/feeding-log-sv-a4.pdf" download>Swedish</a>, <a href="/printables/feeding-log-da-a4.pdf" download>Danish</a>, <a href="/printables/feeding-log-de-a4.pdf" download>German</a>, <a href="/printables/feeding-log-es-letter.pdf" download>Spanish</a>, <a href="/printables/feeding-log-fi-a4.pdf" download>Finnish</a>, <a href="/printables/feeding-log-fr-a4.pdf" download>French</a>, <a href="/printables/feeding-log-it-a4.pdf" download>Italian</a>, <a href="/printables/feeding-log-nl-a4.pdf" download>Dutch</a>, <a href="/printables/feeding-log-pl-a4.pdf" download>Polish</a> and <a href="/printables/feeding-log-pt-a4.pdf" download>Portuguese</a>.</li></ul><p>Free to print and share with your partner, family or childcare. Please link to this page rather than re-hosting the file.</p></section>
<section id="columns"><h2>What each column is for</h2><ul><li><strong>Time:</strong> when the feed started.</li><li><strong>Breast, L / R min:</strong> minutes on each side, if you nurse.</li><li><strong>Bottle made at:</strong> the time you prepared the bottle, so anyone can see how long it has been out.</li><li><strong>Type:</strong> circle F for formula or BM for breast milk.</li><li><strong>Offered and drank:</strong> what went in the bottle and what your baby actually took, in ml or oz.</li><li><strong>Pumped:</strong> how much you expressed.</li><li><strong>Wet and dirty:</strong> tick the diapers.</li><li><strong>Day totals:</strong> add up feeds, amounts and diapers at the end of the day, which is often what a pediatrician or health nurse asks about.</li></ul></section>
<section id="how-often"><h2>How often do newborns feed?</h2><p>Breastfed newborns usually feed about 8 to 12 times in 24 hours, according to the <a href="https://www.cdc.gov/infant-toddler-nutrition/breastfeeding/how-much-and-how-often.html" target="_blank" rel="noopener">CDC</a>. Formula-fed babies often feed a little less often. Every baby is different, so twelve rows is room to write, not a target. Follow your baby's hunger cues and your pediatrician's advice.</p><div class="note"><strong>A record, not medical advice</strong><p>If you are worried about how your baby is feeding, the number of wet diapers, or how your baby seems, contact your pediatrician, midwife or health nurse. Prepared bottles: follow the formula label and your local guidance on how long a bottle can stay out.</p></div></section>
<section id="app"><h2>When paper gets hard to share</h2><p>Paper works well until two people are feeding the baby, or the sheet is in the kitchen when you are in the nursery. Feed Flow keeps the same record on every caregiver's iPhone, counts the day's totals for you and shows a countdown on the Lock Screen from when each bottle was made, as a memory aid. Logging is free, with no ads.</p></section>
""",
        "faqs": [
            ("Is the printable feeding log free?", "Yes. Download it as a PDF in US Letter or A4, with no sign-up."),
            ("How many feeds fit on one page?", "Twelve rows per page, one page per day, with a totals row for feeds, amounts and diapers."),
            ("Does the log work for both breastfeeding and formula?", "Yes. It has columns for minutes on each side, bottle type and amounts, and pumping, so it works for nursing, bottle feeding and combo feeding."),
            ("Is it available in other languages?", "Yes. The same log is available in Norwegian, Swedish, Danish, German, Spanish, Finnish, French, Italian, Dutch, Polish and Portuguese.")
        ],
        "related": [("/combo-feeding", "Combo feeding tracker"), ("/bottle-countdown", "Bottle countdown"), ("/share-feeding-log", "Share the log with your partner")]
    },
]

QUESTION_QUERIES = {
    "printable-feeding-log": ["printable newborn feeding log", "free printable baby feeding chart", "newborn feeding chart pdf", "breastfeeding log printable", "baby feeding and diaper log printable"],
    "bottle-countdown": ["app that tells me when formula bottle expires", "bottle timer app lock screen", "prepared formula countdown app", "how long has this bottle been out app"],
    "combo-feeding": ["combo feeding tracker", "breastfeeding and formula tracker app", "mixed feeding app iPhone", "track nursing and bottles together"],
    "share-feeding-log": ["baby tracker app for both parents", "shared baby feeding log", "baby tracker partner sync", "caregiver baby log app"],
    "free-baby-feeding-tracker": ["free baby feeding tracker", "baby tracker app no ads", "free breastfeeding and formula app", "free baby feeding log iPhone"],
}
