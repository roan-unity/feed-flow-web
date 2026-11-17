"""Build Feed Flow's static, intent-focused content pages. No runtime backend required."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
APP_STORE = "https://apps.apple.com/app/apple-store/id6782075454?pt=126898045&ct=website_content&mt=8"

PAGES = [
    {
        "slug": "formula-feeding", "file": "formula-feeding.html", "active": "feeding",
        "title": "Formula Feeding Tracker, Bottle Timer & Formula Brands",
        "description": "Track formula bottles, brands, preparation times, amounts and vitamin D. Compare formula labels and use Feed Flow's bottle countdown and meal-planning tools.",
        "eyebrow": "Formula & bottle feeding", "h1": "Formula feeding, without the mental arithmetic.",
        "intro": "Keep every bottle, formula brand, amount and preparation time in one calm record. Feed Flow helps with countdowns, daily totals and planning while your label and health professional remain the source of feeding advice.",
        "image": "/screens/formula/01-safe-bottle-360.webp", "srcset": "/screens/formula/01-safe-bottle-360.webp 1x, /screens/formula/01-safe-bottle-720.webp 2x", "width": 360, "height": 780,
        "alt": "Feed Flow's real formula bottle screen with a countdown ring and amounts taken and left.",
        "body": """
<section id="bottle-tracking"><h2>A formula feeding tracker built around real bottles</h2><p>A bottle is more than a number in a daily total. You may want to remember which formula you used, when it was prepared, when feeding started, how much your baby took and how much was left. Feed Flow keeps those details together so the next caregiver does not have to reconstruct the story.</p><ul><li>Record prepared and consumed amounts in <strong>ml or oz</strong>.</li><li>See formula and expressed-milk bottles alongside nursing and pumping.</li><li>Keep a history of the formula or brand used and your baby's response.</li><li>After a few bottles, Feed Flow offers the amounts you usually pour as one-tap buttons. You can turn this off in Settings.</li></ul><p>A little milk left in a bottle is normal. Feed Flow is designed to reduce avoidable waste, not to pressure a baby to finish or make a parent feel guilty.</p></section>
<section id="countdown"><h2>A bottle countdown that stays on your lock screen</h2><p>The countdown runs from when you make the bottle. The default is one hour for formula and two hours for pumped milk, and you can change it in Settings. The remaining time stays visible on your iPhone lock screen, so you do not need to unlock the phone and search through an app at 3am.</p><p>The countdown is a memory aid, not a sensor. Feed Flow cannot know where a bottle was stored, whether it was touched or heated, or whether local safety guidance differs. Set and interpret timers using the formula label and guidance from your local health authority.</p><a class="text-link" href="/guides/formula-safety">Read the formula preparation and storage guide <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="brands"><h2>Compare formula brands using their actual labels</h2><p>Searching for a formula brand often leads to conflicting marketing claims. Feed Flow's formula finder gives you a record-keeping alternative: compare the products you use side by side using the values on their labels.</p><ul><li>Keep formula brand and product details with feeding history.</li><li>Compare formulas by milk base, protein, the tummy worry they address, stage and vitamin D, using the values on the label. You can enter your own product.</li><li>Record vitamin D from formula alongside separate supplement drops, and see the vitamin D meter add them up.</li><li>Bring a clear history to a pediatrician, dietitian or feeding consultation.</li></ul><p>Feed Flow does not rank brands, recommend a switch or decide which formula is suitable for your baby. Those decisions belong with you and a qualified professional who knows your child.</p></section>
<section id="planning"><h2>Smart meal planning and less leftover formula</h2><p>FlowCast learns from your baby's own logged feeding rhythm. After about four days of logged feeds FlowCast shows a likely window for the next feed and the day ahead. The bottle sizes you usually pour help you prepare closer to what your baby typically takes.</p><p>This is not a schedule to enforce and it is not a medical prediction. It is a calm answer to a practical question: <strong>roughly how much should we get ready, and when might the next feed happen?</strong></p><div class="data-example"><span class="example-label">What stays connected</span><h3>Bottle + brand + amount + response + growth</h3><p>When feeding, health and growth records live together, you have more useful context for your next check-up without turning everyday feeding into a test.</p></div></section>
""",
        "faqs": [
            ("Can I track different formula brands in Feed Flow?", "Yes. You can keep formula product details with feeding records and compare label-listed nutrition. Feed Flow does not recommend or rank brands."),
            ("Does the bottle timer guarantee that formula is safe?", "No. It is a countdown based on time, not a safety sensor. Follow the product label and local health guidance for preparation, storage and disposal."),
            ("Can Feed Flow include vitamin D from formula?", "Yes. Record the vitamin D information from the formula label and log separate vitamin D drops. The app keeps records; it does not recommend supplement doses."),
            ("Is mixed formula and breastfeeding supported?", "Yes. Nursing, pumping, expressed milk and formula appear in the same feeding picture without judgement.")
        ],
        "related": [("/guides/formula-safety", "Formula preparation & storage"), ("/guides/vitamin-d-for-babies", "Vitamin D tracking"), ("/breastfeeding-pumping", "Breastfeeding & mixed feeding")]
    },
    {
        "slug": "breastfeeding-pumping", "file": "breastfeeding-pumping.html", "active": "feeding",
        "title": "Breastfeeding, Pumping & Mixed Feeding Tracker",
        "description": "Log breastfeeding, pumping, expressed milk and formula together. Feed Flow gives parents and lactation professionals a clear feeding history without judgement.",
        "eyebrow": "Breastfeeding, pumping & mixed feeding", "h1": "Your feeding routine does not need separate apps.",
        "intro": "Nurse, pump, give expressed milk, use formula, or combine them all. Feed Flow keeps the whole feeding picture together and turns it into useful history for you and the professionals supporting you.",
        "image": "/screens/formula/04-home-360.webp", "srcset": "/screens/formula/04-home-360.webp 1x, /screens/formula/04-home-720.webp 2x", "width": 360, "height": 780,
        "alt": "The Feed Flow Today screen with feeding totals and the latest feeds.",
        "body": """
<section id="nursing"><h2>A breastfeeding log that stays out of the way</h2><p>Record nursing sessions in a few taps and see minutes at the breast beside bottle totals. The purpose is not to grade a feed or tell you how feeding should look. It is to give you a reliable memory of what happened when the days and nights start to blur.</p><ul><li>Nursing, bottles, pumping, water and solids all appear in the day's timeline. The milk total counts formula, pumped milk and nursing (nursing as an estimate). Solids and water are shown separately.</li><li>See daily amounts and patterns without separating breast and bottle into different worlds.</li><li>Share the same baby log with a partner or another caregiver.</li><li>Keep private feeding notes with Premium when you want more context.</li></ul></section>
<section id="pumping"><h2>Pumping and expressed milk stay connected</h2><p>Pumping is both its own task and part of a later feed. Feed Flow keeps pumping records and expressed-milk bottles in the same picture, making it easier to understand what was expressed, what was offered and what your baby actually took. Feed Flow compares what you pump with what your baby takes.</p><p>You do not need to choose a single feeding identity in the app. A day can include nursing, pumping and formula, and each remains a valid part of the record.</p><div class="note"><strong>No judgement, no supply promises</strong><p>Feed Flow does not assess milk supply, diagnose feeding difficulty or replace hands-on lactation support. It gives you and your chosen professional clearer records to work from.</p></div></section>
<section id="mixed-feeding"><h2>Mixed feeding without a sense of failure</h2><p>Combination feeding can be planned, temporary, occasional or simply what works today. The app treats breast milk and formula as records in the same feeding history, not as opposing teams.</p><p>FlowCast learns from the logged rhythm and, after about four days, suggests a likely window for the next feed. It is based on your baby's history and remains a guide, not a schedule you need to follow.</p></section>
<section id="lactation"><h2>Useful history for IBCLCs and lactation experts</h2><p>A consultation is more productive when nobody has to reconstruct a week from memory. Parents can bring feeding times, bottle amounts, pumping history, health notes and growth records into the conversation. A Baby Report gives you a shareable summary.</p><ul><li>Review the sequence of feeds rather than isolated snapshots.</li><li>See bottle and formula details alongside nursing history.</li><li>Keep medicines, reactions and health notes available when relevant.</li><li>Use the record as a conversation aid, never as a diagnosis.</li></ul><p>Feed Flow does not replace an IBCLC, midwife, nurse or physician, and it does not claim WHO Code certification or clinical endorsement.</p><a class="text-link" href="/ambassador">Professional and ambassador collaborations <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
""",
        "faqs": [
            ("Can I breastfeed and formula feed in the same app?", "Yes. Mixed feeding is a core part of Feed Flow. Nursing, pumping, expressed milk and formula stay in one timeline and daily overview."),
            ("Does Feed Flow assess milk supply?", "No. It records feeding and pumping history but does not diagnose low supply, evaluate feeding quality or replace lactation support."),
            ("Can a lactation consultant use the history with me?", "Yes. You can share your own records or a report during a consultation. The information is a conversation aid, not a clinical assessment."),
            ("Does FlowCast tell me when I must feed?", "No. It estimates a likely window from your baby's logged rhythm. Your baby's cues and professional guidance come first.")
        ],
        "related": [("/formula-feeding", "Formula & bottle tracking"), ("/growth-development", "Growth & development"), ("/ambassador", "IBCLC & professional ambassadors")]
    },
    {
        "slug": "solids-allergens", "file": "solids-allergens.html", "active": "health",
        "title": "Solid Foods, Allergen & Baby Reaction Tracker",
        "description": "Log solid foods, allergen introductions and later reactions in one timeline. Keep egg, peanut, milk and other food records ready for your health professional.",
        "eyebrow": "Solid foods & allergens", "h1": "A clear food story, even when the reaction comes later.",
        "intro": "Log meals and allergen introductions when they happen. Add an observed reaction minutes, hours or days later without losing the original food and timing.",
        "image": "/screens/health-allergens-360.webp", "srcset": "/screens/health-allergens-360.webp 1x, /screens/health-allergens-720.webp 2x", "width": 360, "height": 783,
        "alt": "The real Feed Flow allergen journey with six of nine major allergens introduced and a mild marker on egg.",
        "body": """
<section id="solids"><h2>Keep solid foods in the same daily picture</h2><p>The move to solid foods adds ingredients, meals, preferences and new questions. Feed Flow keeps solids alongside milk feeds so you can see the day as a whole rather than splitting food into a separate notebook.</p><p>Use the record to remember what was offered and when, which allergens have appeared, and what you observed afterwards. It is a food and health history, not a menu your baby must follow.</p></section>
<section id="allergens"><h2>Follow the major allergen journey</h2><p>The allergen journey gives you an at-a-glance record of introductions across nine major allergen groups. The allergen ring shows how many of nine you have tried. Each allergen opens with its meals, last attempt and reaction flags, so a food tried last week does not disappear into a daily feed list.</p><ul><li>Keep egg, peanut, tree nut, cow's milk, soy, wheat, fish, shellfish and sesame records together.</li><li>See which foods have been tried and which have not.</li><li>Add a reaction marker and your own observation notes.</li><li>Bring the food and reaction timeline to a qualified health professional.</li></ul><p>Feed Flow does not tell you when to introduce an allergen or whether a food is safe for your child. Follow local guidance and individualized advice, especially if your baby has eczema, an existing allergy or a previous reaction.</p></section>
<section id="later-reaction"><h2>Example: egg yesterday, a reaction note today</h2><div class="data-example"><span class="example-label">Example, not a diagnosis</span><div class="health-timeline"><div class="health-event"><time>Yesterday · 12:10</time><strong>Egg is logged with lunch</strong><p>The food and time remain in the allergen journey.</p></div><div class="health-event"><time>Today · 08:40</time><strong>A reaction note is added</strong><p>You record what you observed and when it appeared. The later note stays connected to the food history.</p></div></div></div><p>A time relationship alone does not prove that a food caused a symptom. Other foods, illness, skin irritation and many everyday factors can overlap. A clear diary helps a professional assess the situation; it does not replace that assessment.</p><a class="text-link" href="/guides/allergen-reaction-diary">How to keep an allergen reaction diary <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="reaction-support"><h2>Know when the diary is not the next step</h2><p>For severe, rapidly worsening or breathing-related symptoms, seek emergency medical care rather than stopping to log. For ongoing or concerning symptoms, contact your pediatrician or local health service.</p><p>For evidence-based clinical resources on food allergy, see the <a href="https://www.niaid.nih.gov/diseases-conditions/guidelines-clinicians-and-patients-food-allergy" target="_blank" rel="noopener">US National Institute of Allergy and Infectious Diseases guidelines</a>. Guidance for families varies by country and individual circumstance.</p></section>
""",
        "faqs": [
            ("Can I log a reaction after the food was recorded?", "Yes. That is a central part of the health timeline: keep the original food event and add an observed reaction when it happens, including later."),
            ("Does Feed Flow diagnose a food allergy?", "No. It records foods, times and observations. A qualified health professional must assess symptoms and diagnose an allergy."),
            ("Which allergens can I track?", "The allergen journey covers nine major groups: egg, peanut, tree nut, cow's milk, soy, wheat, fish, shellfish and sesame."),
            ("Can I track ordinary solid foods too?", "Yes. Solids sit alongside milk feeds in the daily record, while allergen introductions also appear in the allergen journey.")
        ],
        "related": [("/guides/allergen-reaction-diary", "Allergen reaction diary guide"), ("/baby-health", "Medicine, vaccines & health"), ("/growth-development", "Growth & development")]
    },
    {
        "slug": "growth-development", "file": "growth-development.html", "active": "growth",
        "title": "Baby Growth Tracker with WHO Weight Percentiles",
        "description": "Track baby weight, height and head circumference against WHO growth references. See percentiles, follow development milestones and share a clear baby report.",
        "eyebrow": "Growth & development", "h1": "Turn weight, height and head circumference into a story you can follow.",
        "intro": "See your baby's measurements against WHO growth references, follow the pattern over time and keep developmental milestones in the same record as feeding and health.",
        "image": "/screens/growth-report-360.webp", "srcset": "/screens/growth-report-360.webp 1x, /screens/growth-report-720.webp 2x", "width": 360, "height": 783,
        "alt": "A real Feed Flow report showing weight at the 49th percentile and height at the 50th percentile.",
        "body": """
<section id="weight"><h2>Baby weight tracking with WHO percentile context</h2><p>A weight measurement on its own is hard to interpret. Feed Flow places weight in the context of age and sex using WHO growth references, then shows a percentile and the pattern created by your baby's recorded measurements. Log weight, height and head circumference and see them against the WHO band, with the percentile named.</p><p>The example above is a real app report: <strong>7.4 kg at the 49th weight percentile</strong> and <strong>66.3 cm at the 50th height percentile</strong>. The percentile is context, not a grade. A higher number is not a better baby, and a single measurement does not establish a growth problem.</p><a class="text-link" href="/guides/who-growth-percentiles">Understand baby growth percentiles <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="height-head"><h2>Height and head circumference belong in the same record</h2><p>Track weight, height and head circumference together instead of keeping separate notes from each check-up. Feed Flow compares the measurements with WHO growth references and keeps them beside your child's broader development history.</p><ul><li><strong>Weight-for-age:</strong> follow the recorded weight pattern and percentile.</li><li><strong>Length or height:</strong> keep growth measurements together over time.</li><li><strong>Head circumference:</strong> retain another important check-up measurement in context.</li><li><strong>Growth curves:</strong> explore longer history and trends beyond everyday logging.</li></ul><p>The World Health Organization publishes the underlying <a href="https://www.who.int/tools/child-growth-standards/standards" target="_blank" rel="noopener">WHO Child Growth Standards</a>. Your health professional may use a different national reference or interpret measurements alongside examination and history.</p></section>
<section id="development"><h2>Development is more than a growth chart</h2><p>Record developmental milestones with dates, notes and photos. Keep those moments next to feeding and health records so the story of a check-up does not begin and end with weight.</p><p>Feed Flow does not screen for developmental conditions or tell you whether a milestone is delayed. It helps you remember what happened and bring questions to your health nurse or pediatrician.</p></section>
<section id="report"><h2>A report ready for the next conversation</h2><p>A Baby Report turns your own logged information into a clear PDF that can be printed or shared before a visit.</p><p>Use the report to discuss a pattern, not to self-diagnose. Measurement technique, timing, prematurity, health history and clinical examination all matter.</p><div class="note"><strong>When to ask for advice</strong><p>Contact your pediatrician or local child health service if you are worried about feeding, growth, hydration, development or a change in your child's usual pattern. Do not wait for an app threshold to seek help.</p></div></section>
""",
        "faqs": [
            ("Does Feed Flow use WHO baby growth charts?", "Yes. It places weight, height and head circumference measurements in the context of WHO growth references. Your clinician may also use local references and clinical assessment."),
            ("What does the 49th weight percentile mean?", "In the reference population, about 49 percent of children of the same age and sex weigh less and about 51 percent weigh more. It is not a score or a target."),
            ("Can I track head circumference as well as weight and height?", "Yes. Head circumference, weight and height can be kept in the same growth record with WHO reference context."),
            ("Are growth curves free?", "Everyday milestone logging is free. Premium includes full growth curves, unlimited history and broader analytics; current options are shown in the App Store.")
        ],
        "related": [("/guides/who-growth-percentiles", "WHO percentile guide"), ("/baby-health", "Baby health records"), ("/solids-allergens", "Solid foods & allergens")]
    },
    {
        "slug": "baby-health", "file": "baby-health.html", "active": "health",
        "title": "Baby Health Tracker: Medicines, Vaccines & Reactions",
        "description": "Log baby medicines, vaccines, vitamin D, allergens, reactions and health notes in one timeline. Bring clearer records to your pediatrician or health nurse.",
        "eyebrow": "Baby health records", "h1": "The health details you never want to reconstruct from memory.",
        "intro": "Keep medicines, vaccination dates, health reactions, allergens, supplements and notes beside feeding and growth. Feed Flow remembers the record; your health professional handles the medical advice.",
        "image": "/screens/health-allergens-360.webp", "srcset": "/screens/health-allergens-360.webp 1x, /screens/health-allergens-720.webp 2x", "width": 360, "height": 783,
        "alt": "Feed Flow's real health and allergen screen with food attempts and reaction status.",
        "body": """
<section id="medicines"><h2>Medicine records without dosing guesswork</h2><p>Log when a medicine was given and keep the name and your own notes in the health timeline. This is especially useful when caregivers share responsibility or a clinician later asks what happened and when.</p><p>Feed Flow does not calculate doses, check interactions, recommend medicines or tell you when the next dose is safe. Use the medicine label and instructions from your pediatrician or pharmacist.</p></section>
<section id="vaccines"><h2>Vaccination dates in the same baby history</h2><p>Record vaccines and their dates alongside other health events. Instead of searching through papers before an appointment, you can keep the vaccination note with the rest of your child's health record.</p><p>Vaccine schedules differ by country and individual circumstance. Feed Flow does not create a schedule or tell you which vaccine is due; use your national programme and health professional for that guidance.</p></section>
<section id="reactions"><h2>Allergens, symptoms and health reactions over time</h2><p>Food introductions and later observations belong on a timeline. Log egg yesterday, add a reaction note today, and retain both events with their actual times. The same record can hold other health notes you want to discuss.</p><a class="text-link" href="/solids-allergens">Explore solid foods and allergen tracking <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><div class="note"><strong>Timing is not causation</strong><p>A symptom recorded after a food or medicine does not prove that it caused the symptom. Feed Flow does not diagnose allergies or adverse effects. For severe or rapidly worsening symptoms, seek emergency care rather than stopping to log.</p></div></section>
<section id="vitamin-d"><h2>Vitamin D drops and formula-label contributions</h2><p>Log vitamin D supplements and record the vitamin D listed on your formula label. Keeping both in one place makes it easier to discuss your child's actual routine with a health visitor, pharmacist or pediatrician.</p><p>Recommendations vary by feeding method, formula intake, age and country. Feed Flow adds your logged drops to the vitamin D in formula, read from the label values. It does not recommend a supplement or a dose.</p><a class="text-link" href="/guides/vitamin-d-for-babies">Read the vitamin D tracking guide <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="visits"><h2>Bring a coherent record to the appointment</h2><p>Feeding, growth, medicines, vaccines and reactions can all matter in the same conversation. Feed Flow keeps them together so you can spend less time searching and more time explaining what you have observed.</p><p>Reports include feeding, growth, milestones, allergens and reactions. You choose what to share and with whom; your baby's data stays in your own iCloud.</p></section>
""",
        "faqs": [
            ("Can Feed Flow remind me which medicine dose to give?", "No. It keeps a record of medicines and times but does not recommend or calculate doses. Follow the label and your clinician or pharmacist."),
            ("Can I log vaccines from my national programme?", "Yes. Record the vaccination and date in your child's health history. Feed Flow does not create or replace an official vaccination schedule."),
            ("Does the app track vitamin D from both drops and formula?", "Yes. It can log supplement drops and retain vitamin D information from the formula label so both appear in your records."),
            ("Can Feed Flow diagnose a reaction?", "No. It records observations and timing for discussion with a professional. Seek urgent medical help for severe or rapidly worsening symptoms.")
        ],
        "related": [("/guides/vitamin-d-for-babies", "Vitamin D tracking"), ("/guides/allergen-reaction-diary", "Reaction diary guide"), ("/growth-development", "WHO growth tracking")]
    },
    {
        "slug": "flowcast", "file": "flowcast.html", "active": "feeding",
        "title": "FlowCast Next-Feed Prediction & Meal Planning | Feed Flow",
        "description": "See your baby's next feeding window with FlowCast. Get optional notifications, likely amounts and day-ahead meal planning based on your baby's own rhythm.",
        "eyebrow": "FlowCast predictions", "h1": "A calm next-feed notification, learned from your baby.",
        "intro": "FlowCast turns your baby's recent feeding history into likely windows, estimated amounts and a practical day-ahead guide. Prepare for the next feed without treating a prediction as a schedule.",
        "image": "/screens/flowcast-360.webp", "srcset": "/screens/flowcast-360.webp 1x, /screens/flowcast-720.webp 2x", "width": 360, "height": 783,
        "alt": "The real FlowCast screen with a next-feed window, estimated amount and a sequence of later feeding windows.",
        "body": """
<section id="prediction"><h2>Next-feed predictions from your baby's own rhythm</h2><p>After about four days of logged feeds FlowCast looks at your baby's recent pattern and shows a likely window for the next feed and the day ahead.</p><p>The estimate can include a likely amount and the gaps between feeds. It is built from your records, so it reflects this baby rather than a generic feeding timetable.</p><ul><li>See the next likely feeding window and when it opens.</li><li>Review later windows across the day.</li><li>Use estimated amounts as preparation guidance, not a portion your baby must finish.</li><li>Watch the prediction become more useful as consistent history builds.</li></ul></section>
<section id="notification"><h2>An optional notification when the next feed approaches</h2><p>Once your baby's rhythm is steady, about a week of regular days, Feed Flow can send a quiet reminder before the next window. It stays silent overnight. That gives you time to warm milk, check a bottle or simply take a breath before the next feed.</p><p>The reminder is optional and follows the prediction. Feed Flow refreshes its timing as new feeds are logged and when you return to the app, helping it avoid relying on an old window.</p><div class="note"><strong>A nudge, never an alarm you must obey</strong><p>Feed when your baby needs it, whether that is before, during or after the predicted window. FlowCast does not assess hunger, diagnose a feeding issue or replace your judgement.</p></div></section>
<section id="planning"><h2>Smart meal planning with less waste</h2><p>FlowCast works beside the app's learned bottle sizes. Together they help you answer two practical questions: when might the next feed happen, and roughly how much should we prepare?</p><p>Preparing closer to your baby's usual amount can reduce leftovers without pressuring anyone to finish. A little milk left over is normal, and an empty bottle is never the goal at any cost.</p><a class="text-link" href="/formula-feeding">Explore formula planning and bottle sizes <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="honesty"><h2>What FlowCast does not know</h2><p>Growth spurts, illness, travel, daycare and ordinary chaotic days can all change a feeding pattern. FlowCast cannot see those causes and does not promise that the next feed will happen inside its window.</p><p>Use it as a gentle planning aid beside your baby's cues and your health professional's guidance. It is not a medical prediction or a feeding schedule to enforce.</p></section>
""",
        "faqs": [
            ("When does FlowCast start predicting the next feed?", "After about four days of feeding history, FlowCast can begin showing likely windows from your baby's own logged rhythm. More consistent history gives it a clearer basis."),
            ("Can FlowCast notify me before the next feed?", "Yes. Once your baby's rhythm is steady, about a week of regular days, Feed Flow can send a quiet reminder before the next window. It stays silent overnight. It is a planning nudge, not an alarm you need to follow."),
            ("Is FlowCast free?", "Logging is free. The next-feed time and the day-ahead view are part of Premium. Current options are shown in the App Store."),
            ("Should I feed my baby only inside the FlowCast window?", "No. Always respond to your baby's cues and professional guidance. A predicted window is a useful estimate, not a rule or a medical recommendation.")
        ],
        "related": [("/formula-feeding", "Formula & smart meal planning"), ("/breastfeeding-pumping", "Breastfeeding & mixed feeding"), ("/baby-report", "Feeding & growth reports")]
    },
    {
        "slug": "vitamin-d-tracker", "file": "vitamin-d-tracker.html", "active": "health",
        "title": "Vitamin D Tracker for Drops & Formula | Feed Flow",
        "description": "Track baby vitamin D drops and formula. Feed Flow calculates formula-label vitamin D and shows the total remaining toward the 10 µg / 400 IU reference.",
        "eyebrow": "Vitamin D tracker", "h1": "Vitamin D drops and formula, calculated together.",
        "intro": "See how much vitamin D you have logged, how much today’s formula contributes, and what remains toward the daily reference. Feed Flow does the arithmetic without deciding your baby's supplement dose.",
        "image": "/screens/vitamin-d-detail-450.webp", "srcset": "/screens/vitamin-d-detail-450.webp 1x, /screens/vitamin-d-detail-900.webp 2x", "width": 450, "height": 410,
        "alt": "A real Feed Flow screen showing vitamin D from formula and the contribution today's planned drops make toward the reference.",
        "body": """
<section id="calculation"><h2>Automatic vitamin D calculations from drops and formula</h2><p>Feed Flow combines two sources in one daily readout: the supplement drops you log and the vitamin D carried by today's formula feeds. Formula is calculated from the feed amount and the vitamin D value read from the label. Known products are filled in from our catalogue, so check them against your tin.</p><ul><li>Logged drops contribute the dose you recorded.</li><li>Formula contributes according to actual consumed amounts and your label's per-100 ml value.</li><li>The card separates formula and drops so the total has an understandable source.</li><li>If a formula has no label value entered, the app discloses that it is not counted rather than guessing.</li></ul><p>Breast milk is not assigned an estimated vitamin D contribution. Feed Flow does not invent a fortification value for a brand.</p></section>
<section id="remaining"><h2>See what remains toward the daily reference</h2><p>The meter uses <strong>10 µg / 400 IU per day</strong> as the reference for a baby's first year, the figure the American Academy of Pediatrics, Helsedirektoratet and ESPGHAN give. It can show the counted amount so far, what remains toward that reference, and when your planned drops will cover the rest.</p><p>This is arithmetic against a printed reference, not a judgement that your baby is deficient, adequately supplemented or receiving the right dose. Recommendations differ by feeding method, formula intake, age and country.</p><div class="note"><strong>Your clinician sets the plan, not the app</strong><p>Use the supplement label and advice from your pediatrician, pharmacist or child health service. Feed Flow does not prescribe a dose, assess a deficiency or check interactions.</p></div></section>
<section id="habit"><h2>A daily log and optional reminder that stays gentle</h2><p>Mark today's drops with one tap and see when they were logged. An optional reminder helps you remember, while a simple streak can make the routine visible without turning a missed day into a failure.</p><p>Caregivers can see the same record through the shared baby log, reducing the chance that anyone has to ask whether the drops were already given.</p></section>
<section id="sources"><h2>Official guidance stays one step away</h2><p>For an example of feeding-specific national advice, the UK NHS explains <a href="https://www.nhs.uk/conditions/baby/weaning-and-feeding/vitamins-for-children/" target="_blank" rel="noopener">vitamin supplements for babies and children</a>. The US CDC provides separate guidance for <a href="https://www.cdc.gov/infant-toddler-nutrition/vitamins-minerals/vitamin-d.html" target="_blank" rel="noopener">breast milk, mixed feeding and infant formula</a>.</p><p>Those sources illustrate why a universal automatic dose would be inappropriate. Use the recommendation for your country and your child.</p><a class="text-link" href="/guides/vitamin-d-for-babies">Read the vitamin D tracking guide <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
""",
        "faqs": [
            ("Does Feed Flow calculate vitamin D from formula?", "Yes. It uses consumed formula amounts and the vitamin D value on the formula label. It never guesses a missing brand value."),
            ("Can it show how much is left to supplement?", "It shows what remains toward the 10 µg / 400 IU daily reference and when your planned drops cover the rest. That is reference arithmetic, not a personalized dosing instruction."),
            ("Does it remind me to give vitamin D drops?", "Yes. You can log daily drops and enable an optional reminder. A missed day simply starts a new streak without scolding."),
            ("Does the app decide whether my baby needs a supplement?", "No. Your child's clinician, pharmacist, product label and national guidance determine the appropriate plan. Feed Flow keeps records and performs calculations.")
        ],
        "related": [("/guides/vitamin-d-for-babies", "Vitamin D tracking guide"), ("/formula-feeding", "Formula brands & nutrition"), ("/baby-health", "Medicine & supplement records")]
    },
    {
        "slug": "baby-report", "file": "baby-report.html", "active": "growth",
        "title": "Baby Feeding & Growth Report PDF | Feed Flow",
        "description": "Create a baby report with feeding totals, weekly patterns, WHO growth curves, weight, height and head percentiles, and milestones. Private in your iCloud and ready to share.",
        "eyebrow": "Baby Reports", "h1": "A full report with all your feeding and growth data.",
        "intro": "Turn everyday records into a clear PDF for a health nurse, pediatrician or lactation consultation. Feeding, growth and milestones stay private in your own iCloud until you choose to share.",
        "image": "/screens/formula/10-feeding-report-360.webp", "srcset": "/screens/formula/10-feeding-report-360.webp 1x, /screens/formula/10-feeding-report-720.webp 2x", "width": 360, "height": 780,
        "alt": "A real Feed Flow Baby Report with feeding totals, growth since birth, daily averages and percentiles.",
        "body": """
<section id="inside"><h2>Feeding history, growth curves and milestones in one PDF</h2><p>A Baby Report brings the information you already logged into one calm document. Start with the baby's summary, then move into feeding patterns and growth rather than assembling screenshots and notes before an appointment.</p><ul><li>Milk and feed totals, daily averages and the period covered.</li><li>Weekly feeding patterns and amounts prepared, taken and left.</li><li>Weight, height and head circumference with WHO reference percentiles.</li><li>Developmental milestones with their recorded dates.</li></ul><p>The detailed growth page explains what a percentile means in plain language and keeps the emphasis on following your baby's own curve rather than chasing a score.</p></section>
<section id="conversation"><h2>Made for a better professional conversation</h2><p>Print the report, share the PDF or open it during a visit. A health nurse can see the trend, a pediatrician can review the broader picture, and an IBCLC can discuss feeding history with concrete amounts and times.</p><p>Feed Flow does not diagnose from the report or replace an examination. It gives you and your chosen professional a clearer starting point.</p><a class="text-link" href="/growth-development">Explore WHO growth tracking <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="privacy"><h2>Private in your iCloud until you decide to share</h2><p>Your baby's records live on your device and in your own iCloud, not on a Feed Flow server. Caregiver sharing uses your private iCloud setup. Exporting or sharing a report is an action you take, not something that happens automatically.</p><p>You can also export your underlying data or delete it. The report is a view of your record, not a separate advertising profile.</p><a class="text-link" href="/privacy">Read the privacy policy <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
<section id="access"><h2>Get your Baby Report</h2><p>You build a Baby Report in the app from the feeds, growth measurements and milestones you have already logged.</p><p>Everyday feed logging remains free. See the current purchase options and regional pricing in the App Store.</p></section>
""",
        "faqs": [
            ("What is included in the Baby Report?", "Feeding totals and patterns, weekly trends, WHO growth curves and percentiles for weight, height and head circumference, and developmental milestones from your own records."),
            ("Can I share the report with my pediatrician or IBCLC?", "Yes. You can print or share the PDF before or during an appointment. It is a conversation aid, not a diagnosis."),
            ("Is my baby's report stored on Feed Flow's servers?", "No. Baby data stays on your device and in your own iCloud. You decide when to export or share a report."),
            ("Do I need full Premium for reports?", "Reports are included with Premium, and a separate Reports Pass is available. The App Store shows current options and prices.")
        ],
        "related": [("/growth-development", "WHO growth & development"), ("/baby-health", "Baby health records"), ("/flowcast", "FlowCast predictions")]
    },
    {
        "slug": "resources", "file": "resources.html", "active": "resources",
        "title": "Baby Feeding, Growth & Health Guides | Feed Flow",
        "description": "Practical guides on formula safety, breastfeeding, pumping, solids, allergens, WHO baby growth, vitamin D, medicines and vaccines from Feed Flow.",
        "eyebrow": "Feed Flow resource hub", "h1": "Useful answers for feeding, growth and baby health.",
        "intro": "Start with a specific question or explore a feature. Every guide explains what Feed Flow records, where official health guidance belongs, and what you can bring to a professional conversation.",
        "image": "/screens/flowcast-360.webp", "srcset": "/screens/flowcast-360.webp 1x, /screens/flowcast-720.webp 2x", "width": 360, "height": 783,
        "alt": "Feed Flow's FlowCast screen with likely feeding windows based on the baby's history.",
        "body": """
<section id="guides"><h2>Practical health and tracking guides</h2><p>Short, focused reading for the questions that send parents searching at inconvenient hours. Official sources are linked where guidance matters.</p><div class="resource-grid"><a class="resource-card" href="/guides/should-you-use-a-feeding-tracker"><span class="tag">Start here</span><h3>Should you use a feeding tracker?</h3><p>An honest answer: when tracking helps, when it adds pressure, and how to log calmly.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/guides/formula-safety"><span class="tag">Formula</span><h3>Preparation, storage & bottle timing</h3><p>CDC storage windows, label instructions and how a countdown supports memory.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/guides/who-growth-percentiles"><span class="tag">Growth</span><h3>WHO growth percentiles explained</h3><p>What weight, height and head-circumference percentiles do and do not mean.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/guides/allergen-reaction-diary"><span class="tag">Allergens</span><h3>Keeping a reaction diary</h3><p>What to record when a food and an observed reaction are separated by time.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/guides/vitamin-d-for-babies"><span class="tag">Vitamin D</span><h3>Drops and formula together</h3><p>How to keep supplement and formula-label records without dosing advice.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></div></section>
<section id="features"><h2>Find the right part of Feed Flow</h2><div class="resource-grid"><a class="resource-card" href="/formula-feeding"><span class="tag">Bottle</span><h3>Formula & bottle feeding</h3><p>Brands, timers, label nutrition and reduced waste.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/breastfeeding-pumping"><span class="tag">Milk</span><h3>Breastfeeding & pumping</h3><p>Mixed feeding and consultation-ready history.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/solids-allergens"><span class="tag">Food</span><h3>Solids & allergens</h3><p>Introductions, meals and later reaction notes.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/growth-development"><span class="tag">WHO</span><h3>Growth & development</h3><p>Percentiles, milestones and check-up reports.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></div></section>
<section id="smart-tools"><h2>Prediction, nutrition and reporting tools</h2><div class="resource-grid"><a class="resource-card" href="/flowcast"><span class="tag">FlowCast</span><h3>Next-feed predictions</h3><p>Likely windows, estimated amounts, optional notifications and day-ahead planning.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/vitamin-d-tracker"><span class="tag">Nutrition</span><h3>Vitamin D tracker</h3><p>Drops plus formula-label vitamin D, with the daily total and reference remainder.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><a class="resource-card" href="/baby-report"><span class="tag">PDF</span><h3>Baby Reports</h3><p>Feeding, WHO growth curves and milestones in a private, shareable report.</p><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></div></section>
<section id="professionals"><h2>For lactation and feeding professionals</h2><p>Feed Flow is a record-keeping companion for families, not a clinical decision tool. IBCLCs, lactation experts, dietitians and feeding professionals can use parent-shared records to make conversations more concrete.</p><ul><li>Review feeding sequences and bottle details rather than relying on recall.</li><li>Keep growth, health notes and reactions in context.</li><li>Share only information the parent chooses to provide.</li><li>Keep diagnosis, treatment and individualized feeding advice with the qualified professional.</li></ul><a class="text-link" href="/ambassador">Explore ambassador and professional collaborations <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a><br><a class="text-link" href="/mom-creator-affiliate-program">Earn as a mom creator <svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg></a></section>
""",
        "faqs": [],
        "related": [("/baby-health", "Baby health tracker"), ("/faq", "Product FAQ"), ("/support", "Get support")]
    },
    {
        "slug": "guides/formula-safety", "file": "guides/formula-safety.html", "active": "resources", "guide": True,
        "title": "Formula Safety: Preparation, Storage & Bottle Timers",
        "description": "How long can formula stay out? Review CDC preparation and storage windows, leftover bottle guidance, and how Feed Flow's countdown helps you keep track.",
        "eyebrow": "Formula safety guide", "h1": "How long can a prepared bottle stay out?",
        "intro": "The answer depends on whether feeding has started and how the bottle is stored. Here is the current CDC summary, the role of the product label, and how a Feed Flow timer can help you remember.",
        "image": "/screens/formula/02-lock-screen-360.webp", "srcset": "/screens/formula/02-lock-screen-360.webp 1x, /screens/formula/02-lock-screen-720.webp 2x", "width": 360, "height": 780,
        "alt": "A real iPhone lock screen showing Feed Flow's bottle countdown.",
        "body": """
<section id="windows"><h2>The three time windows to keep distinct</h2><p>According to the <a href="https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html" target="_blank" rel="noopener">US Centers for Disease Control and Prevention</a>, prepared infant formula should be used <strong>within 2 hours of preparation</strong> and <strong>within 1 hour from when feeding begins</strong>.</p><ol><li><strong>After preparation:</strong> if you will not start using the formula within 2 hours, refrigerate it immediately.</li><li><strong>After feeding starts:</strong> use the bottle within 1 hour, then discard what remains.</li><li><strong>In the refrigerator:</strong> use refrigerated prepared formula within 24 hours.</li></ol><p>These are US CDC storage guidelines, not a universal rule for every product or country. Always check the formula label and your local health authority. Some children need additional precautions.</p><div class="note"><strong>Leftovers are different</strong><p>Do not refrigerate a bottle your baby has already drunk from to save for later. CDC guidance says to discard leftover formula because saliva can allow germs to grow.</p></div></section>
<section id="preparation"><h2>Preparation details matter as much as time</h2><p>Use safe water, clean feeding equipment and the exact water-to-formula ratio on the container. Do not dilute formula or add extra powder to change the concentration. Check the container's use-by date and its instructions for storage after opening.</p><p>Powdered infant formula is not sterile. Babies who are very young, were born prematurely or have weakened immune systems may need extra precautions; discuss ready-to-feed options and preparation with a qualified professional.</p></section>
<section id="timer"><h2>Where Feed Flow helps, and where it cannot</h2><p>The countdown runs from when you make the bottle. The default is one hour for formula and two hours for pumped milk, and you can change it in Settings. It stays on the lock screen. That removes the need to remember the start time during a tired night feed.</p><ul><li>The app records the time you enter; it does not sense the room or refrigerator temperature.</li><li>A timer cannot tell whether a bottle was prepared correctly or previously touched.</li><li>The default one-hour countdown is not a replacement for the separate preparation and refrigeration windows.</li><li>If timing is uncertain, follow local safety guidance rather than relying on a recollection or an app screen.</li></ul><p>Think of Feed Flow as the notebook and clock, not the safety authority.</p></section>
<section id="less-waste"><h2>Reduce waste without stretching safety windows</h2><p>Preparing closer to your baby's usual amount can reduce leftovers without trying to extend a bottle's life. After a few bottles, Feed Flow offers the amounts you usually pour as one-tap buttons, and you can turn this off in Settings.</p><p>Never pressure a baby to finish to avoid waste, and never reuse a leftover bottle outside official guidance. A little leftover milk can be the safer outcome.</p></section>
""",
        "faqs": [
            ("Is prepared formula always safe for two hours?", "No single timer covers every situation. CDC guidance distinguishes within 2 hours of preparation from within 1 hour after feeding begins, with immediate refrigeration if it will not be used within 2 hours. Labels and local guidance matter."),
            ("Can I save a bottle my baby did not finish?", "CDC guidance says to discard formula left after feeding rather than refrigerating it for later. Follow your local health authority and product label."),
            ("Does Feed Flow know whether a bottle is safe?", "No. It records times and shows a countdown. It cannot measure contamination, temperature, preparation or handling.")
        ],
        "related": [("/formula-feeding", "Formula feeding tracker"), ("/guides/vitamin-d-for-babies", "Vitamin D & formula"), ("/resources", "All feeding guides")]
    },
    {
        "slug": "guides/who-growth-percentiles", "file": "guides/who-growth-percentiles.html", "active": "resources", "guide": True,
        "title": "WHO Baby Growth Percentiles: Weight, Height & Head",
        "description": "What does a baby weight percentile mean? Understand WHO weight, height and head-circumference charts, why patterns matter, and how Feed Flow keeps growth records.",
        "eyebrow": "WHO growth guide", "h1": "What does your baby’s growth percentile actually mean?",
        "intro": "A percentile is a comparison with a reference population, not a grade or a target. Learn how to read it and why the pattern and clinical context matter more than a single number.",
        "image": "/screens/growth-report-360.webp", "srcset": "/screens/growth-report-360.webp 1x, /screens/growth-report-720.webp 2x", "width": 360, "height": 783,
        "alt": "A real Feed Flow report showing the 49th weight percentile and 50th height percentile.",
        "body": """
<section id="meaning"><h2>A plain-language percentile example</h2><p>If a baby is at the <strong>49th percentile for weight-for-age</strong>, about 49 out of 100 children of the same age and sex in the reference population weigh less, and about 51 weigh more.</p><p>That does not mean the baby is 49 percent healthy, 49 percent grown, or expected to move toward the 100th percentile. Children have different bodies and growth patterns. The 10th and 90th percentiles are not grades either.</p></section>
<section id="measurements"><h2>Weight, height and head circumference answer different questions</h2><ul><li><strong>Weight-for-age</strong> places a measured weight in age and sex reference context.</li><li><strong>Length or height-for-age</strong> tracks another dimension of growth over time.</li><li><strong>Head circumference-for-age</strong> preserves a separate measurement commonly collected in early-childhood care.</li></ul><p>Looking at these together is more informative than isolating one reading. Feeding, health, prematurity, genetics, measurement technique and clinical examination can all affect interpretation.</p></section>
<section id="pattern"><h2>The pattern matters more than chasing a line</h2><p>A single measurement can vary with scale, clothing, timing or technique. A series of carefully recorded measurements helps a professional understand the pattern. Crossing a percentile line is a reason for a qualified review, not something an app should diagnose.</p><p>The <a href="https://www.who.int/tools/child-growth-standards/standards" target="_blank" rel="noopener">WHO Child Growth Standards</a> describe the reference charts and methods. Your country or clinician may use another reference, particularly as children grow older or when prematurity needs to be considered.</p></section>
<section id="tracking"><h2>How Feed Flow presents growth</h2><p>Log weight, height and head circumference and see them against the WHO band, with the percentile named. Keep milestones beside those measurements, then use a Baby Report to bring feeding and growth history to a check-up.</p><p>The real example screen on this page shows 7.4 kg at the 49th weight percentile and 66.3 cm at the 50th height percentile. Those values belong to the example record; they are not targets for another child.</p><div class="note"><strong>Ask a professional when you are concerned</strong><p>Do not wait for an app to label a measurement. Contact your pediatrician or child health service about poor feeding, hydration concerns, persistent changes or anything else that worries you.</p></div></section>
""",
        "faqs": [
            ("Is a higher baby percentile better?", "No. A percentile is not a grade. Health professionals interpret the measurement alongside growth pattern, examination and history."),
            ("Should every baby be near the 50th percentile?", "No. Healthy children sit at many different percentiles. The 50th is the middle of a reference population, not a universal target."),
            ("Does Feed Flow diagnose growth problems?", "No. It records measurements and shows WHO reference context. A qualified professional must assess growth and health.")
        ],
        "related": [("/growth-development", "WHO growth tracker"), ("/baby-health", "Baby health records"), ("/resources", "All growth guides")]
    },
    {
        "slug": "guides/allergen-reaction-diary", "file": "guides/allergen-reaction-diary.html", "active": "resources", "guide": True,
        "title": "Baby Allergen & Reaction Diary: What to Record",
        "description": "Learn what to record when a baby tries egg, peanut or another allergen and a reaction appears later. Keep useful notes without diagnosing the cause.",
        "eyebrow": "Allergen & reaction guide", "h1": "What should you write down when a reaction appears later?",
        "intro": "A useful diary connects the food, the timing and the observation without deciding the cause for you. Here is a practical structure you can use in Feed Flow or discuss with your health professional.",
        "image": "/screens/health-allergens-360.webp", "srcset": "/screens/health-allergens-360.webp 1x, /screens/health-allergens-720.webp 2x", "width": 360, "height": 783,
        "alt": "The real Feed Flow allergen journey with major allergens and reaction status.",
        "body": """
<section id="record"><h2>Record the food event before the details fade</h2><ul><li>The food or allergen and the meal it appeared in.</li><li>The date and time it was offered.</li><li>Other foods or relevant events around the same meal.</li><li>Any notes you chose to keep about the feeding.</li></ul><p>Do not delay urgent care to complete a diary. For severe, rapidly worsening or breathing-related symptoms, seek emergency medical help first.</p></section>
<section id="later"><h2>Add the observation at its actual later time</h2><p>If you notice something the next morning, record it then rather than placing it at yesterday's meal. Feed Flow lets the original egg entry and today's reaction note remain separate but connected events.</p><div class="data-example"><span class="example-label">Example timeline</span><div class="health-timeline"><div class="health-event"><time>Yesterday · 12:10</time><strong>Egg logged</strong><p>Food event preserved.</p></div><div class="health-event"><time>Today · 08:40</time><strong>Reaction note added</strong><p>Observation preserved at its later time.</p></div></div></div><p>Write what you observed rather than assigning a diagnosis. A professional can ask about appearance, duration, other symptoms, illness, medications and the broader context.</p></section>
<section id="cause"><h2>Do not let the timeline decide causation</h2><p>“After egg” is not the same as “because of egg.” Symptoms can coincide with another food, a viral illness, skin irritation or an unrelated event. Likewise, the absence of a logged reaction does not prove future tolerance.</p><p>Feed Flow does not diagnose allergies, predict reactions or tell you to reintroduce a food. Those decisions require a qualified health professional who can assess the child and the complete history.</p></section>
<section id="professional"><h2>Bring the record, not just the conclusion</h2><p>A chronological food and health record can help a pediatrician, allergist or dietitian ask better questions. Keep medicine and vaccine records available too when they are relevant.</p><p>For clinical background, the US National Institute of Allergy and Infectious Diseases publishes <a href="https://www.niaid.nih.gov/diseases-conditions/guidelines-clinicians-and-patients-food-allergy" target="_blank" rel="noopener">food allergy guidelines for clinicians and patients</a>. Introduction and management advice should be individualized, especially after a previous reaction or when eczema or an existing allergy is present.</p></section>
""",
        "faqs": [
            ("Can I add a reaction the day after logging a food?", "Yes. Keep the food at its original time and add the reaction note at the later time you observed it."),
            ("Does a reaction note prove an allergy?", "No. It records an observation, not a diagnosis. A health professional needs to assess the history and symptoms."),
            ("Should I log symptoms during an emergency?", "No. Seek emergency care first for severe, rapidly worsening or breathing-related symptoms. Record information later if useful.")
        ],
        "related": [("/solids-allergens", "Solid foods & allergen tracker"), ("/baby-health", "Baby health tracker"), ("/resources", "All health guides")]
    },
    {
        "slug": "guides/vitamin-d-for-babies", "file": "guides/vitamin-d-for-babies.html", "active": "resources", "guide": True,
        "title": "Vitamin D for Babies: Track Drops & Formula Intake",
        "description": "Keep baby vitamin D drops and formula-label vitamin D together. Learn why recommendations vary and how Feed Flow supports records without giving dosing advice.",
        "eyebrow": "Vitamin D tracking guide", "h1": "Vitamin D drops and formula belong in the same record.",
        "intro": "Supplement recommendations depend on feeding method, formula intake, age and national guidance. Feed Flow helps you record what your baby receives so you can discuss it accurately with a professional.",
        "image": "/screens/formula/04-home-360.webp", "srcset": "/screens/formula/04-home-360.webp 1x, /screens/formula/04-home-720.webp 2x", "width": 360, "height": 780,
        "alt": "Feed Flow's daily feeding screen where formula amounts contribute to nutrition records.",
        "body": """
<section id="varies"><h2>Why there is no single answer for every baby</h2><p>Breastfed babies, mixed-fed babies and formula-fed babies can have different supplement guidance. Formula itself is fortified, and the amount consumed can affect a national recommendation.</p><p>For example, the UK NHS publishes separate advice for breastfed babies, babies consuming infant formula, and older children on its <a href="https://www.nhs.uk/conditions/baby/weaning-and-feeding/vitamins-for-children/" target="_blank" rel="noopener">vitamins for children page</a>. That is UK guidance, not a global dosage rule. Use the recommendation for your country and your child.</p></section>
<section id="track"><h2>What Feed Flow can keep track of</h2><ul><li>When you record a vitamin D supplement or drops.</li><li>The vitamin D listed on the formula product label.</li><li>Formula amounts that contribute to the day's nutrition record.</li><li>A history you can show a health visitor, pharmacist or pediatrician.</li></ul><p>The vitamin D meter shows the amount counted so far and what remains toward the daily reference. The app does not scan a bottle, independently verify a label or know what was actually absorbed; the records depend on what you enter.</p></section>
<section id="not-dose"><h2>What Feed Flow deliberately does not do</h2><p>Feed Flow does not recommend a supplement, calculate a dose, assess a deficiency or decide whether your baby needs drops. It also does not check supplement interactions.</p><p>Use the supplement label and advice from a qualified professional. If you are unsure whether two products contain overlapping vitamins, ask a pharmacist or clinician before combining them.</p></section>
<section id="appointment"><h2>A simple routine for a better appointment</h2><ol><li>Keep the supplement name and the times you give it in the health record.</li><li>Enter nutrition exactly as printed on the formula label.</li><li>Record formula and mixed feeding consistently enough to show the real routine.</li><li>Bring the products or their labels and your Feed Flow history to the appointment.</li></ol><p>The goal is not a perfect nutrition score. It is an accurate answer when someone asks, “What does your baby usually receive?”</p></section>
""",
        "faqs": [
            ("Does Feed Flow tell me how much vitamin D to give?", "No. It records supplements and formula-label information. Dose and supplement decisions belong with the product label and your qualified health professional."),
            ("Can formula contribute to the vitamin D record?", "Yes. Feed Flow can retain the vitamin D listed on the formula label alongside formula amounts and separate drops."),
            ("Is NHS vitamin D guidance relevant in every country?", "No. It is a useful official UK example, but recommendations vary. Follow your local health authority and your child's clinician.")
        ],
        "related": [("/baby-health", "Medicine & supplement records"), ("/formula-feeding", "Formula brands & nutrition"), ("/resources", "All baby health guides")]
    },
    {
        "slug": "guides/should-you-use-a-feeding-tracker", "file": "guides/should-you-use-a-feeding-tracker.html", "active": "resources", "guide": True,
        "title": "Should You Use a Baby Feeding Tracker? An Honest Answer",
        "description": "When a baby feeding tracker helps, when it adds pressure, and how to log without obsessing over numbers. An honest guide from the dad who built Feed Flow, with CDC, AAP and WHO sources.",
        "eyebrow": "Should you track feeds?", "h1": "Should you use a baby feeding tracker?",
        "intro": "An honest answer from the dad who built one: sometimes the answer is no. Here is when a tracker earns its place, when it gets in the way, and how to use one without letting the numbers take over.",
        "image": "/screens/formula/04-home-360.webp", "srcset": "/screens/formula/04-home-360.webp 1x, /screens/formula/04-home-720.webp 2x", "width": 360, "height": 780,
        "alt": "The Feed Flow Today screen with the day's feeds in one simple overview.",
        "body": """
<section id="maybe-not"><h2>If feeding is going well, you may not need one</h2><p>Picture the ideal: breastfeeding works, or the bottles go smoothly, your baby is growing well at check-ups, and you feel sure your baby is eating and thriving. In that world, a feeding tracker adds little. Your baby's cues already tell you what you need to know.</p><p>Official guidance points the same way. The World Health Organization asks parents to practise <a href="https://www.who.int/news-room/fact-sheets/detail/infant-and-young-child-feeding" target="_blank" rel="noopener">responsive feeding</a>, recognising and responding to signs of hunger and fullness, and the American Academy of Pediatrics encourages parents to <a href="https://www.healthychildren.org/English/ages-stages/baby/feeding-nutrition/Pages/How-Often-and-How-Much-Should-Your-Baby-Eat.aspx" target="_blank" rel="noopener">look to their baby rather than the clock</a>.</p><p>Some feeding specialists go further, and they have a point. Therapists who help babies with bottle refusal often work on helping parents step back from the numbers, because measuring every feed can raise anxiety, create expectations about volumes and timings, and babies notice that tension. If tracking makes feeds feel more stressful in your home, stopping is a perfectly good choice.</p><p>Research on feeding apps is still small and mixed. In one <a href="https://pubmed.ncbi.nlm.nih.gov/31793799/" target="_blank" rel="noopener">interview study</a>, breastfeeding mothers said tracker apps gave them a feeling of control and confidence, but also worried about relying on them and being overwhelmed by data. Another <a href="https://pubmed.ncbi.nlm.nih.gov/37887451/" target="_blank" rel="noopener">survey</a> linked lighter app use with better feeding interactions than heavy use.</p></section>
<section id="reality"><h2>But that is not how it looks for many families</h2><p>Real feeding is often messier. Newborns feed about <a href="https://www.cdc.gov/infant-toddler-nutrition/breastfeeding/how-much-and-how-often.html" target="_blank" rel="noopener">8 to 12 times in 24 hours</a>, and during cluster feeding the CDC notes it can be as often as every hour. Add sleep deprivation and the days and nights blur together quickly.</p><ul><li><strong>Mixed feeding is common.</strong> In CDC data for babies born in 2023, <a href="https://www.cdc.gov/breastfeeding-data/about/index.html" target="_blank" rel="noopener">22.6% of breastfed infants received formula within their first two days</a>, and fewer than a third were exclusively breastfed through six months. Nursing, pumping and formula in the same day is normal, and hard to keep in your head.</li><li><strong>Bottles run on a clock.</strong> The CDC says prepared formula should be used <a href="https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html" target="_blank" rel="noopener">within 2 hours of preparation and within one hour from when feeding begins</a>. Freshly expressed breast milk can stay at room temperature <a href="https://www.cdc.gov/breastfeeding/breast-milk-preparation-and-storage/handling-breastmilk.html" target="_blank" rel="noopener">for up to 4 hours</a>, and leftovers should be used within 2 hours. At 3am, &ldquo;when did I make this?&rdquo; is a real question.</li><li><strong>More than one person feeds.</strong> When a partner, grandparent or sitter takes a turn, &ldquo;when did she last eat?&rdquo; needs an answer nobody has to remember.</li><li><strong>Sometimes someone asks for a record.</strong> A pediatrician, health nurse or lactation consultant may want to know what a normal day looks like.</li></ul><p>This is where a feeding tracker can earn its place: not as a judge of how feeding should look, but as a memory for tired parents.</p></section>
<section id="our-story"><h2>Where I come from</h2><p>I am Robin, a dad of two in Norway, and I built Feed Flow. When our first daughter arrived we had trouble with breastfeeding, and everything turned into a confusing mix of nursing, pumping and formula. Some days we made 14 bottles, some barely touched, some half drunk, and we poured a lot of formula down the drain because we could not see the pattern. We wrote feeds on paper and in our phones because, as new and insecure parents, we just wanted to know what was normal and whether she was getting enough.</p><p>Feed Flow started as a simple way to stop giving a bottle that had been out too long, and to stop throwing away milk that was still fine. It grew into one view of every kind of feed, tested every day on our own children. I will say honestly what I told a feeding specialist who disagreed with tracking: obsessing over numbers is not good for anyone. The goal was never more numbers. It was an app that helps you instead of becoming one more chore: calm, useful and even a little playful. That is still how we build Feed Flow, as parents who struggled with feeding ourselves.</p></section>
<section id="track-calmly"><h2>If you do track, track in a way that keeps you calm</h2><ul><li><strong>Log less, not more.</strong> Record what helps you, skip what does not. A missed entry is not a failure.</li><li><strong>Let the app do the arithmetic.</strong> Totals, averages and timings should not be your job at 3am.</li><li><strong>Watch your baby, not the screen.</strong> The record is a memory aid. Your baby's hunger and fullness cues come first.</li><li><strong>Use patterns, not single numbers.</strong> One small feed means little. A week can show what is normal for your baby.</li><li><strong>Keep what helps, drop what does not.</strong> Some parents stop logging bottles once things settle. Others keep going through the move to solid foods, because seeing feeding, growth, development and allergen introductions in one place is genuinely useful. Either is fine; you never owe the app an entry.</li></ul></section>
<section id="how-feed-flow-helps"><h2>How Feed Flow tries to help without adding pressure</h2><p>Feed Flow, the formula &amp; feeding tracker for iPhone, was designed by a sleep-deprived parent to take thinking off your plate rather than give you more numbers to analyse.</p><ul><li><strong>One view of every feed.</strong> Nursing, pumping, expressed milk, formula, water and solids sit in one timeline with one milk total.</li><li><strong>No mental maths.</strong> You slide a picture of the bottle to show what was drunk and read what is left. After a few bottles, the amounts you usually pour become one-tap buttons, so you prepare closer to what your baby takes and waste less.</li><li><strong>A bottle countdown on your Lock Screen.</strong> It runs from when you make the bottle, one hour for formula and two hours for pumped milk by default, and you can adjust it to your label and local guidance. It is a reminder, not a safety sensor.</li><li><strong>FlowCast next-feed predictions.</strong> After about four days of logged feeds, FlowCast learns your baby's own rhythm and shows a likely window for the next feed and the day ahead. Babies change with growth spurts, illness and development, so it is a guide, never a schedule.</li><li><strong>Vitamin D, added up for you.</strong> Feed Flow counts the vitamin D in the formula your baby drank, from the label, plus any drops you log, and shows what remains toward the 10 µg / 400 IU daily reference. Whether and how much to supplement is your and your clinician's decision.</li><li><strong>Growth against WHO references.</strong> Weight, height and head circumference are shown against the <a href="https://www.who.int/tools/child-growth-standards/standards" target="_blank" rel="noopener">WHO Child Growth Standards</a>, as context, never as a grade.</li><li><strong>Health in the same story.</strong> Log reactions, sick periods, medicines and the nine major allergens as your baby moves to solids, and keep track of which formula you use and how your baby does on it.</li><li><strong>A report when someone asks.</strong> Share a clear PDF with your partner, health nurse or pediatrician instead of reconstructing a week from memory.</li></ul></section>
<section id="what-we-dont-do"><h2>What Feed Flow does not do</h2><p>It does not diagnose, set targets, tell you how much your baby should drink or grade a feed. It has no ads and no sponsored or paid formula brands. Formula products appear only so you can record what you use, and the app does not recommend one product over another. Your baby's records live on your phone and in your own iCloud.</p><div class="note"><strong>When to ask for help instead</strong><p>If you are worried about feeding, weight, wet diapers, hydration or how your baby seems, contact your pediatrician, health nurse or a lactation consultant. Do not wait for an app to tell you something is wrong.</p></div></section>
<section id="quick-test"><h2>A quick test: would a tracker help you right now?</h2><ol><li>Are you losing track of when your baby last fed, or which side, or which bottle?</li><li>Is more than one person feeding your baby?</li><li>Are bottles going down the drain because you are not sure how long they have been out?</li><li>Has a professional asked you to keep a record?</li><li>Does logging make you calmer, or more anxious?</li></ol><p>If you answered yes to the first four, a tracker can take real load off your day. If logging makes you more anxious, that matters more than any feature: put the app away and follow your baby.</p></section>
""",
        "faqs": [
            ("Do I need a baby feeding tracker?", "Not necessarily. If feeding is going well, your baby is growing and you feel confident reading their cues, you may not need one. A tracker helps most with mixed feeding, many caregivers, bottle timing or when a professional asks for a record."),
            ("Can tracking feeds make anxiety worse?", "It can for some parents, especially when every millilitre starts to feel like a test. Small studies of feeding apps report both more confidence and worries about relying on the data. If logging raises your stress, it is fine to stop."),
            ("How often do newborns feed?", "The CDC says breastfed babies feed about 8 to 12 times in 24 hours, sometimes as often as every hour during cluster feeding. Follow your baby's cues and your health professional's advice."),
            ("Is a feeding tracker useful after the newborn stage?", "It can be. As babies move to solid foods, many parents like having feeding, growth, development, allergen introductions and any reactions in one overview. The point is an overview that helps you, not more numbers to worry about."),
            ("Does Feed Flow advertise formula?", "No. There are no ads and no sponsored or paid brands. Formula products appear only so parents can record what they use, and the app does not recommend one over another.")
        ],
        "related": [("/breastfeeding-pumping", "Breastfeeding & mixed feeding"), ("/guides/formula-safety", "Formula preparation & storage"), ("/flowcast", "FlowCast predictions")]
    }
]


L = {
    "en": {"skip": "Skip to content", "download": "Download on the App Store", "download_sm": "Download", "meta": "Free to log · iPhone · Your baby’s data stays in your own iCloud", "faq": "Common questions", "explore": "Explore", "aside1": "Keep the whole picture", "aside1p": "Feeding, growth and health records stay together in Feed Flow.", "aside2": "A record, not medical advice", "aside2p": "Feed Flow does not diagnose conditions, recommend medicine doses or replace your pediatrician, midwife, health nurse or lactation professional.", "more": "Continue exploring", "lead": "One calm record for feeding, growth and health.", "tiers": "Download Feed Flow and start logging today. Logging is free, forever.", "locale": "en_US", "menu": "Open menu", "home": "Feed Flow home"},
    "nb": {"skip": "Gå til innholdet", "download": "Last ned i App Store", "download_sm": "Last ned", "meta": "Gratis å logge · iPhone · Dataene ligger i din egen iCloud", "faq": "Vanlige spørsmål", "explore": "Se mer", "aside1": "Alt på ett sted", "aside1p": "Mating, vekst og helse samlet i én rolig app, helt på norsk.", "aside2": "En logg, ikke medisinske råd", "aside2p": "Feed Flow stiller ingen diagnoser, anbefaler ikke doser og erstatter ikke helsestasjonen, jordmor eller legen.", "more": "Les mer", "lead": "Én rolig logg for mating, vekst og helse.", "tiers": "Last ned Feed Flow og begynn å logge i dag. Det er gratis å logge.", "locale": "nb_NO", "menu": "Åpne meny", "home": "Feed Flow forsiden"},
    "sv": {"skip": "Till innehållet", "download": "Hämta i App Store", "download_sm": "Hämta", "meta": "Gratis att logga · iPhone · Datan ligger i ditt eget iCloud", "faq": "Vanliga frågor", "explore": "Läs mer", "aside1": "Allt på ett ställe", "aside1p": "Matning, tillväxt och hälsa samlat i en lugn app, helt på svenska.", "aside2": "En logg, inte medicinska råd", "aside2p": "Feed Flow ställer inga diagnoser, rekommenderar inga doser och ersätter inte BVC, barnmorskan eller läkaren.", "more": "Läs vidare", "lead": "En lugn logg för matning, tillväxt och hälsa.", "tiers": "Hämta Feed Flow och börja logga i dag. Det är gratis att logga.", "locale": "sv_SE", "menu": "Öppna menyn", "home": "Feed Flow startsida"},
}
NAV = {
    "nb": [("feeding", "/no#mating", "Mating"), ("countdown", "/no#nedtelling", "Nedtelling"), ("print", "/no#utskrift", "Utskrift"), ("faq", "/no#faq", "Spørsmål"), ("sv", "/sv", "Svenska"), ("en", "/", "English")],
    "sv": [("feeding", "/sv#matning", "Matning"), ("countdown", "/sv#nedrakning", "Nedräkning"), ("print", "/sv#utskrift", "Utskrift"), ("faq", "/sv#faq", "Frågor"), ("nb", "/no", "Norsk"), ("en", "/", "English")],
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="/assets/icons.svg#{name}"/></svg>'


def wordmark():
    return f'<a href="/" class="wordmark" aria-label="Feed Flow"><span>Feed</span><span class="flow">Flow</span><span class="bottle" aria-hidden="true"><svg><use href="/assets/icons.svg#bottle"/></svg></span></a>'


def header(active, lang="en"):
    t = L[lang]
    store = APP_STORE if lang == "en" else APP_STORE.replace("ct=website_content", f"ct=website_{lang}")
    items = NAV[lang] if lang in NAV else [("feeding", "/#feeding", "Feeding"), ("growth", "/#growth", "Growth"), ("health", "/#health", "Health"), ("resources", "/resources", "Guides"), ("ambassador", "/ambassador", "Ambassadors")]
    desktop = "".join(f'<a href="{url}"{(" aria-current=\"page\"" if key == active else "")}>{label}</a>' for key, url, label in items)
    mobile = "".join(f'<a href="{url}">{label}<span aria-hidden="true">→</span></a>' for _, url, label in items)
    return f'''<header class="nav"><div class="wrap nav-inner">{wordmark()}<nav class="desktop-nav" aria-label="Primary navigation">{desktop}</nav><div class="nav-right"><button class="theme-toggle" id="themeToggle" type="button" aria-label="Use dark theme">{icon('sun','sun')}{icon('moon','moon')}</button><a href="{store.replace('website_content','website_header')}" class="btn btn-primary btn-sm nav-download">{icon('apple','apple')}{t['download_sm']}</a><button class="menu-toggle" id="menuToggle" type="button" aria-label="{t['menu']}" aria-expanded="false" aria-controls="mobileNav">{icon('menu')}</button></div></div><nav class="mobile-nav" id="mobileNav" aria-label="Mobile navigation" hidden>{mobile}<a href="{store.replace('website_content','website_mobile_menu')}">{t['download']}<span aria-hidden="true">→</span></a></nav></header>'''


FT_HEADINGS = {"product": "Product", "learn": "Learn", "company": "Feed Flow", "languages": "Languages"}
# Where a translation already existed on the old language footers it is kept; everything else stays English.
FT_NORDIC = {
    "nb": {"privacy": "Personvern (engelsk)", "terms": "Vilkår (engelsk)", "pdf": ("/printables/feeding-log-nb-a4.pdf", "Matingslogg (PDF)"), "blurb": "Feed Flow! er appen for mating og MME på iPhone, laget i Norge av Zeolite. Mating, vekst og babyens helse i én rolig app med personvern først."},
    "sv": {"privacy": "Integritet (engelska)", "terms": "Villkor (engelska)", "pdf": ("/printables/feeding-log-sv-a4.pdf", "Matningslogg (PDF)"), "blurb": "Feed Flow! är appen för matning och ersättning på iPhone, byggd i Norge av Zeolite. Matning, tillväxt och bebisens hälsa i en lugn app med integriteten först."},
}


def footer(lang="en"):
    """The one footer: four labelled columns, used on every page (generated pages, index and the four legacy pages)."""
    social = [("linkedin", "https://www.linkedin.com/company/feedflow-babyfeedingapp/", "LinkedIn", "Feed Flow on LinkedIn"), ("instagram", "https://www.instagram.com/feedflow_babyfeedingapp", "Instagram", "Feed Flow on Instagram"), ("tiktok", "https://www.tiktok.com/@feedflow_babyfeedingapp", "TikTok", "Feed Flow on TikTok"), ("youtube", "https://www.youtube.com/@FeedFlow-BabyFeedingApp", "YouTube", "Feed Flow on YouTube"), ("facebook", "https://www.facebook.com/feedflowapp", "Facebook", "Feed Flow on Facebook"), ("reddit", "https://www.reddit.com/r/FeedFlowParents/", "Reddit", "Feed Flow Parents on Reddit")]
    icons = "".join(f'<a class="social-link" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{label}" title="{name}">{icon(key)}</a>' for key, url, name, label in social)
    blurb = "Feed Flow! is the formula &amp; feeding tracker for iPhone, built in Norway by Zeolite. Feeding, growth and baby health in one calm, privacy-first app."
    privacy, terms, pdf = "Privacy", "Terms", None
    if lang in FT_NORDIC:
        n = FT_NORDIC[lang]
        blurb, privacy, terms, pdf = n["blurb"], n["privacy"], n["terms"], n["pdf"]
    elif "footer_links" in L.get(lang, {}):
        u = L[lang]
        blurb, privacy, terms, pdf = u["blurb"], u["privacy"], u["terms"], (u["footer_links"][1][0], u["footer_links"][1][1])
    learn = [("/resources", "Guides"), ("/vitamin-d-tracker", "Vitamin D tracker"), ("/bottle-countdown", "Bottle countdown"), ("/combo-feeding", "Combo feeding"), ("/printable-feeding-log", "Printable feeding log"), ("/compare", "Compare apps"), ("/free-baby-feeding-tracker", "Free tracker"), ("/faq", "FAQ")]
    if pdf:
        learn.insert(5, pdf)
    columns = [
        ("product", [("/formula-feeding", "Formula feeding"), ("/breastfeeding-pumping", "Breast &amp; pumping"), ("/solids-allergens", "Solids &amp; allergens"), ("/growth-development", "Growth &amp; development"), ("/baby-health", "Baby health"), ("/flowcast", "FlowCast"), ("/baby-report", "Baby Reports"), ("/share-feeding-log", "Shared feeding log")]),
        ("learn", learn),
        ("company", [("/support", "Support"), ("/ambassador", "Ambassadors"), ("/mom-creator-affiliate-program", "Earn as a creator"), ("https://apps.apple.com/app/id6782075454?action=write-review", "Leave a review"), ("/privacy", privacy), ("/terms", terms)]),
    ]
    cols = "".join(f'<nav class="ft-col" aria-labelledby="ft-h-{key}"><h2 class="ft-h" id="ft-h-{key}">{FT_HEADINGS[key]}</h2><ul>' + "".join(f'<li><a href="{url}">{label}</a></li>' for url, label in items) + '</ul></nav>' for key, items in columns)
    lang_items = "".join(f'<li><a href="{path}" hreflang="{code}" lang="{code}">{name}</a></li>' for path, name, code, _ in LANGS)
    cols += f'<nav class="ft-col" aria-labelledby="ft-h-languages"><h2 class="ft-h" id="ft-h-languages">{FT_HEADINGS["languages"]}</h2><ul>{lang_items}</ul></nav>'
    return f'''<footer class="ft" id="support"><div class="wrap"><div class="ft-inner"><div class="ft-left">{wordmark()}<p>{blurb}</p><a class="ft-mail" href="mailto:support@tryfeedflow.app">support@tryfeedflow.app</a><nav class="social-list" aria-label="Feed Flow on social media">{icons}</nav></div><div class="ft-cols">{cols}</div></div><div class="ft-bottom">&copy; 2026 Feed Flow!</div></div></footer>'''


def schema(page):
    url = "https://tryfeedflow.app/" + page["slug"]
    webpage = {"@type": "WebPage", "@id": url + "#page", "url": url, "name": page["title"], "description": page["description"], "dateModified": page.get("date", "2026-11-12"), "image": "https://tryfeedflow.app" + page["image"], "isPartOf": {"@id": "https://tryfeedflow.app/#website"}, "about": {"@id": "https://tryfeedflow.app/#app"}, "inLanguage": page.get("lang", "en")}
    citations = {
        "guides/formula-safety": ["https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html"],
        "printable-feeding-log": ["https://www.cdc.gov/infant-toddler-nutrition/breastfeeding/how-much-and-how-often.html"],
        "guides/who-growth-percentiles": ["https://www.who.int/tools/child-growth-standards/standards"],
        "growth-development": ["https://www.who.int/tools/child-growth-standards/standards"],
        "guides/allergen-reaction-diary": ["https://www.niaid.nih.gov/diseases-conditions/guidelines-clinicians-and-patients-food-allergy"],
        "solids-allergens": ["https://www.niaid.nih.gov/diseases-conditions/guidelines-clinicians-and-patients-food-allergy"],
        "guides/vitamin-d-for-babies": ["https://www.nhs.uk/conditions/baby/weaning-and-feeding/vitamins-for-children/", "https://www.cdc.gov/infant-toddler-nutrition/vitamins-minerals/vitamin-d.html"],
        "vitamin-d-tracker": ["https://www.nhs.uk/conditions/baby/weaning-and-feeding/vitamins-for-children/", "https://www.cdc.gov/infant-toddler-nutrition/vitamins-minerals/vitamin-d.html"],
        "guides/should-you-use-a-feeding-tracker": ["https://www.who.int/news-room/fact-sheets/detail/infant-and-young-child-feeding", "https://www.healthychildren.org/English/ages-stages/baby/feeding-nutrition/Pages/How-Often-and-How-Much-Should-Your-Baby-Eat.aspx", "https://www.cdc.gov/infant-toddler-nutrition/breastfeeding/how-much-and-how-often.html", "https://www.cdc.gov/breastfeeding-data/about/index.html", "https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html", "https://www.cdc.gov/breastfeeding/breast-milk-preparation-and-storage/handling-breastmilk.html", "https://www.who.int/tools/child-growth-standards/standards", "https://pubmed.ncbi.nlm.nih.gov/31793799/", "https://pubmed.ncbi.nlm.nih.gov/37887451/"]
    }
    citations.update(ARTICLE_CITATIONS)
    if page["slug"] in citations:
        webpage["citation"] = citations[page["slug"]]
    if page.get("guide"):
        webpage["lastReviewed"] = page["date"] if page.get("article") else "2026-11-12"
    graph = [webpage, {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Feed Flow", "item": "https://tryfeedflow.app/"}] + ([{"@type": "ListItem", "position": 2, "name": "Guides", "item": "https://tryfeedflow.app/resources"}, {"@type": "ListItem", "position": 3, "name": page["eyebrow"].replace(" guide", ""), "item": url}] if page.get("guide") else [{"@type": "ListItem", "position": 2, "name": page["eyebrow"], "item": url}])}]
    if page.get("article"):
        graph.append({"@type": "Article", "@id": url + "#article", "headline": page["h1"], "description": page["description"], "datePublished": page["date"], "dateModified": page["date"], "image": "https://tryfeedflow.app" + page["image"], "mainEntityOfPage": {"@id": url + "#page"}, "author": {"@id": "https://tryfeedflow.app/#org"}, "publisher": {"@id": "https://tryfeedflow.app/#org"}, "inLanguage": "en"})
    if page["slug"] == "resources":
        graph.append({"@type": "ItemList", "name": "Feed Flow feature and guide library", "itemListElement": [{"@type": "ListItem", "position": index, "name": item["title"], "url": "https://tryfeedflow.app/" + item["slug"]} for index, item in enumerate([entry for entry in PAGES if entry["slug"] != "resources"], start=1)]})
    if page["faqs"]:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faqs"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")


def render(page):
    html_lang = page.get("lang", "en")
    lang = page.get("ui", html_lang)
    t = L[lang]
    store = APP_STORE if lang == "en" else APP_STORE.replace("ct=website_content", f"ct=website_{lang}")
    url = "https://tryfeedflow.app/" + page["slug"]
    hreflang = "".join(f'<link rel="alternate" hreflang="{code}" href="{href}">' for code, href in page.get("hreflang", []))
    faqs = ""
    if page["faqs"]:
        details = "".join(f'<details><summary>{escape(q)}</summary><div>{escape(a)}</div></details>' for q, a in page["faqs"])
        faqs = f'<section id="faq"><h2>{t['faq']}</h2><div class="faq-list">{details}</div></section>'
    related = "".join(f'<a class="resource-card" href="{link}"><span class="tag">{t['explore']}</span><h3>{escape(label)}</h3>{icon("arrow")}</a>' for link, label in page["related"])
    aside_links = "".join(f'<a href="{link}">{escape(label)} →</a>' for link, label in page["related"])
    guide_crumb = '<a href="/resources">Guides</a><span>/</span>' if page.get("guide") else ('<a href="/compare">Compare apps</a><span>/</span>' if page.get("compare") and page["slug"] != "compare" else '')
    return f'''<!DOCTYPE html>
<html lang="{html_lang}" data-theme="light"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="apple-itunes-app" content="app-id=6782075454">
<title>{escape(page['title'])}</title><meta name="description" content="{escape(page['description'], quote=True)}"><meta name="robots" content="index, follow, max-image-preview:large"><meta name="theme-color" content="#2F7886">
<link rel="canonical" href="{url}">{hreflang}<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@800&amp;display=swap"><link rel="stylesheet" href="/site.css">
<script defer data-domain="tryfeedflow.app" src="https://plausible.io/js/script.outbound-links.tagged-events.js"></script><script defer src="/analytics.js"></script><script defer src="/site.js"></script><script>try{{var t=localStorage.getItem('ff-web-theme');if(t!=='light'&&t!=='dark')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 96 96'%3E%3Crect width='96' height='96' rx='22' fill='%232F7886'/%3E%3Crect x='27' y='28' width='7' height='40' rx='3' fill='%23fff'/%3E%3Crect x='27' y='28' width='22' height='7' rx='3' fill='%23fff'/%3E%3Ccircle cx='63.5' cy='55' r='12' fill='%23E87352'/%3E%3C/svg%3E">
<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:title" content="{escape(page['title'], quote=True)}"><meta property="og:description" content="{escape(page['description'], quote=True)}"><meta property="og:image" content="https://tryfeedflow.app/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Four real Feed Flow screens: bottle countdown, FlowCast, vitamin D tracking and a feeding and growth report"><meta property="og:site_name" content="Feed Flow!"><meta property="og:locale" content="{t['locale']}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(page['title'], quote=True)}"><meta name="twitter:description" content="{escape(page['description'], quote=True)}"><meta name="twitter:image" content="https://tryfeedflow.app/og.png"><meta name="twitter:image:alt" content="Four real Feed Flow screens: bottle countdown, FlowCast, vitamin D tracking and a feeding and growth report">
<script type="application/ld+json">{schema(page)}</script></head><body><a class="skip-link" href="#main">{t['skip']}</a>{header(page['active'], lang)}
<main id="main"><section class="content-hero"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Feed Flow</a><span>/</span>{guide_crumb}<span>{escape(page['eyebrow'].replace(' guide',''))}</span></nav><div class="content-hero-grid"><div><p class="eyebrow">{escape(page['eyebrow'])}</p><h1>{escape(page['h1'])}</h1><p class="intro">{escape(page['intro'])}</p><div class="hero-cta"><a class="btn btn-primary" href="{store}">{icon('apple','apple')}{t['download']}</a></div><p class="meta">{t['meta']}</p></div><figure class="shot"><img src="{page['image']}" srcset="{page['srcset']}" width="{page['width']}" height="{page['height']}" fetchpriority="high" decoding="async" alt="{escape(page['alt'], quote=True)}"></figure></div></div></section>
<div class="wrap content-layout"><article class="article-body">{page['body']}{faqs}</article><aside class="article-aside" aria-label="Related information"><div class="aside-card"><h2>{t['aside1']}</h2><p>{t['aside1p']}</p><div class="aside-links">{aside_links}</div></div><div class="aside-card"><h2>{t['aside2']}</h2><p>{t['aside2p']}</p></div></aside></div>
<section class="related-section"><div class="wrap"><h2>{t['more']}</h2><div class="resource-grid">{related}</div></div></section>
<section class="cta"><div class="wrap"><div class="cta-banner"><p class="lead">{t['lead']}</p><p class="tiers">{t['tiers']}</p><a class="btn btn-primary" href="{store.replace('website_content','website_closing')}">{icon('apple','apple')}{t['download']}</a></div></div></section></main>{footer(lang)}<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"066ad3912fc4436c8f31f2f912b89230"}}'></script></body></html>'''


import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_pages import COMPARE, COMPARE_QUERIES
from question_pages import QUESTION, QUESTION_QUERIES
from nordic_pages import NORDIC, NORDIC_QUERIES
from intl_pages import INTL, INTL_QUERIES, INTL_UI, INTL_NAV, LANGS
from article_pages import ARTICLES, ARTICLE_QUERIES, ARTICLE_CITATIONS, inject_article_links, resource_cards
L.update(INTL_UI)
NAV.update(INTL_NAV)
PAGES += COMPARE + QUESTION + NORDIC + INTL + ARTICLES
inject_article_links(PAGES)
for _page in PAGES:
    if _page["slug"] == "resources" and ARTICLES:
        _marker = '</div></section>'
        _head, _sep, _tail = _page["body"].partition(_marker)
        _page["body"] = _head + resource_cards() + _sep + _tail

import re as _re


def sync_static_pages():
    """index.html and the four legacy pages are hand-edited, but their footer (and the legacy header) come from here."""
    block = lambda name, html: f"<!--ff:{name}-->{html}<!--/ff:{name}-->"
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    if "<!--ff:footer-->" in text:
        text = _re.sub(r"<!--ff:footer-->.*?<!--/ff:footer-->", lambda m: block("footer", footer("en")), text, flags=_re.S)
    else:
        text = _re.sub(r'<footer class="ft".*?</footer>', lambda m: block("footer", footer("en")), text, count=1, flags=_re.S)
    index.write_text(text, encoding="utf-8")
    for name in ("faq", "support", "privacy", "terms"):
        path = ROOT / f"{name}.html"
        text = path.read_text(encoding="utf-8")
        for part, html in (("header", header("", "en")), ("footer", footer("en"))):
            text = _re.sub(rf"<!--ff:{part}-->.*?<!--/ff:{part}-->", lambda m: block(part, html), text, flags=_re.S)
        path.write_text(text, encoding="utf-8")
        print(f"Synced {path.relative_to(ROOT)}")


for item in PAGES:
    target = ROOT / item["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(item), encoding="utf-8")
    print(f"Built {target.relative_to(ROOT)}")

query_map = {
    "guides/should-you-use-a-feeding-tracker": ["should I use a baby feeding tracker", "do I need a baby tracker app", "feeding tracker anxiety", "is tracking baby feeds necessary"],
    "formula-feeding": ["formula feeding tracker", "baby bottle timer app", "formula brand comparison", "formula nutrition tracker"],
    "breastfeeding-pumping": ["breastfeeding tracker app", "pumping log app", "mixed feeding tracker", "breast and formula feeding app"],
    "solids-allergens": ["baby allergen tracker", "solid food tracker for babies", "baby food reaction diary", "egg allergy food log"],
    "growth-development": ["baby growth tracker", "WHO growth chart app", "baby weight percentile tracker", "height and head circumference app"],
    "baby-health": ["baby medicine tracker", "baby vaccine record app", "baby health tracker", "baby reaction and symptom log"],
    "flowcast": ["next feed prediction app", "next feed notification", "baby feeding schedule app", "smart baby meal planning"],
    "vitamin-d-tracker": ["baby vitamin D tracker", "vitamin D formula calculator", "infant vitamin D app", "vitamin D drops and formula tracker"],
    "baby-report": ["baby feeding report PDF", "feeding and growth report app", "pediatrician baby report", "WHO growth report for babies"],
    "resources": ["baby feeding guides", "baby health resources", "infant feeding app resources", "baby growth tracking guides"],
    "guides/formula-safety": ["how long can formula stay out", "prepared formula storage guidelines", "baby bottle safety timer"],
    "guides/who-growth-percentiles": ["what does baby weight percentile mean", "WHO baby growth percentiles", "head circumference percentile explained"],
    "guides/allergen-reaction-diary": ["baby allergen reaction diary", "baby reaction after egg next day", "what to record after baby food reaction"],
    **COMPARE_QUERIES,
    **QUESTION_QUERIES,
    **NORDIC_QUERIES,
    **INTL_QUERIES,
    **ARTICLE_QUERIES,
    "guides/vitamin-d-for-babies": ["vitamin D for babies", "baby vitamin D drops and formula", "infant vitamin D supplement guide"]
}
(ROOT / "seo").mkdir(exist_ok=True)
(ROOT / "seo" / "content-map.json").write_text(json.dumps({
    "source": "OpenSEO keyword-research and keyword-clustering workflows, using public search evidence without live provider metrics",
    "domain": "tryfeedflow.app",
    "note": "Query clusters are editorial hypotheses until validated with OpenSEO/DataForSEO or Search Console. No search-volume, keyword-difficulty or ranking claims are made.",
    "pages": [{"url": "https://tryfeedflow.app/" + p["slug"], "title": p["title"], "intent": p["eyebrow"], "role": "guide" if p.get("guide") else "hub", "primaryQueries": query_map[p["slug"]], "relatedLinks": [link for link, _ in p["related"]]} for p in PAGES]
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
sync_static_pages()


def sync_article_discovery():
    """Keep sitemap.xml and llms.txt in step with scripts/articles (idempotent: our lines are removed and re-added)."""
    if not ARTICLES:
        return
    urls = {"https://tryfeedflow.app/" + a["slug"] for a in ARTICLES}
    sitemap = ROOT / "sitemap.xml"
    lines = [l for l in sitemap.read_text(encoding="utf-8").split("\n") if not any(f"<loc>{u}</loc>" in l for u in urls)]
    new = [f'  <url><loc>https://tryfeedflow.app/{a["slug"]}</loc><lastmod>{a["date"]}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>' for a in ARTICLES]
    at = max(i for i, l in enumerate(lines) if "/guides/" in l) + 1
    sitemap.write_text("\n".join(lines[:at] + new + lines[at:]), encoding="utf-8")
    llms = ROOT / "llms.txt"
    lines = [l for l in llms.read_text(encoding="utf-8").split("\n") if not any(l.endswith(u) for u in urls)]
    new = [f'- {a["title"].rsplit(" | ", 1)[0]} ({a["description"]}): https://tryfeedflow.app/{a["slug"]}' for a in ARTICLES]
    at = max(i for i, l in enumerate(lines) if "tryfeedflow.app/guides/" in l) + 1
    llms.write_text("\n".join(lines[:at] + new + lines[at:]), encoding="utf-8")
    print(f"Synced sitemap.xml and llms.txt for {len(ARTICLES)} guides")


sync_article_discovery()
