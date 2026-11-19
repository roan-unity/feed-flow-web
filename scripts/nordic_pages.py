"""Norwegian and Swedish landing pages (2026-11-16): /no/matingslogg and /sv.

Since 2026-11-19 /no itself is the Norwegian twin of the English homepage (no.html, see scripts/make-no-home.py);
the Norwegian article that used to live there moved to /no/matingslogg.

Most of Feed Flow's ratings come from Norway and Sweden, and the app is fully translated, so these pages target
local searches (amming app, matingslogg, bebisapp, amning app). Facts must match llms.txt. Health wording:
the countdown is a memory aid; follow the label and helsestasjonen/BVC. No competitor claims.
"""

ARROW = '<svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg>'
IMG = 'style="max-width:100%;height:auto;border-radius:14px;border:1px solid var(--border);margin:8px 0 4px"'
from intl_pages import HREFLANG  # all localized pages

NORDIC = [
    {
        "slug": "no/matingslogg", "file": "no/matingslogg.html", "lang": "nb", "active": "feeding", "date": "2026-11-19", "hreflang": [("nb", "https://tryfeedflow.app/no/matingslogg")],
        "title": "Feed Flow: Babyapp for amming, flaske og MME på norsk | iPhone",
        "description": "Feed Flow er en babyapp for iPhone, helt på norsk. Logg amming, pumping, flaske og morsmelkerstatning på én tidslinje. Gratis å logge, uten reklame.",
        "eyebrow": "Babyapp på norsk", "h1": "Matingslogg for amming, pumping og flaske, laget i Norge",
        "intro": "Feed Flow er appen for alt babyen spiser: amming, pumping, morsmelk på flaske, morsmelkerstatning og fast føde, på én tidslinje. Appen er helt på norsk, laget i Norge, og det er gratis å logge. Ingen reklame, og dataene ligger i din egen iCloud.",
        "image": "/screens/nordic/no-03-360.webp", "srcset": "/screens/nordic/no-03-360.webp 1x, /screens/nordic/no-03-720.webp 2x", "width": 360, "height": 780,
        "alt": "Feed Flow på norsk: I dag-skjermen med siste måltid, neste måltid og dagens flasker.",
        "body": f"""
<section id="mating"><h2>Alt babyen spiser, på én tidslinje</h2><p>Mange begynner med notater på telefonen, en lapp på kjøleskapet og en egen app for pumping. Feed Flow samler alt i samme dag.</p><ul><li><strong>Amming:</strong> logg en amming med noen få trykk.</li><li><strong>Pumping:</strong> logg hvor mye du pumpet, ved siden av det babyen faktisk drakk.</li><li><strong>Flaske:</strong> morsmelk eller MME, laget og drukket mengde i ml.</li><li><strong>Fast føde og vann:</strong> i samme tidslinje, holdt utenfor melkesummen.</li></ul><p>Dagens melkesum teller MME, pumpet melk og amming (amming som et anslag, siden ingen kan se hvor mye babyen drikker ved brystet). Du får ett tall for døgnet i stedet for å legge sammen lister om kvelden.</p></section>
<section id="nedtelling"><h2>Nedtelling fra flasken ble laget</h2><p>Når du logger en flaske, starter en nedtelling fra tidspunktet den ble laget, og den vises på låseskjermen. Da ser du hvor lenge flasken har stått uten å låse opp telefonen. Standard er én time for MME og to timer for pumpet morsmelk, og du kan endre begge i Innstillinger.</p><img src="/screens/nordic/no-01-360.webp" srcset="/screens/nordic/no-01-360.webp 1x, /screens/nordic/no-01-720.webp 2x" width="300" height="650" loading="lazy" decoding="async" alt="Feed Flow viser nedtelling for en flaske med morsmelkerstatning." {IMG}><div class="note"><strong>En hukommelseshjelp, ikke en sikkerhetssensor</strong><p>Nedtellingen måler bare tid. Den vet ikke hvordan flasken er oppbevart eller hvor varmt det er i rommet. Følg det som står på pakningen og rådene fra helsestasjonen, og lag en ny flaske hvis du er usikker.</p></div></section>
<section id="dele"><h2>Hele familien i samme logg</h2><p>Inviter partner, besteforeldre eller barnevakt. Alle logger fra sin egen iPhone via sin egen iCloud, uten felles passord og uten grense på hvor mange dere er. Da slipper dere spørsmålet «når spiste hun sist?» ved hvert vaktskifte. Deling er gratis.</p><p>Dukker ikke måltidene til partneren din opp? <a href="/no/hjelp/deling-synkronisering">Slik får du delingen og synkroniseringen til å virke</a>.</p></section>
<section id="premium"><h2>Gratis, og Premium hvis du vil ha mer</h2><p>Logging av alle måltider, nedtellingen for flasken og deling med familien er gratis, uten reklame. Premium legger til:</p><ul><li><strong>FlowCast:</strong> et sannsynlig tidsvindu for neste måltid, basert på babyens egen historikk etter omtrent fire dager med logging. Et planleggingsverktøy, ikke en timeplan.</li><li><strong>Vekstkurver</strong> mot WHO-referanser og full historikk.</li><li><strong>Babyrapport</strong> med mating og vekst som du kan ta med til helsestasjonen.</li></ul></section>
<section id="utskrift"><h2>Gratis matingslogg til utskrift</h2><p>Foretrekker du papir de første dagene, eller trenger barnevakten en lapp på kjøleskapet? Her er en gratis matingslogg på norsk: én side per døgn med klokkeslett, amming, flaske, pumping og bleier.</p><img src="/printables/feeding-log-nb-480.webp" srcset="/printables/feeding-log-nb-480.webp 1x, /printables/feeding-log-nb-960.webp 2x" width="360" height="509" loading="lazy" decoding="async" alt="Matingslogg for nyfødt til utskrift, én side per døgn." {IMG}><p><a class="text-link" href="/printables/feeding-log-nb-a4.pdf" download>Last ned matingsloggen (PDF, A4) {ARROW}</a></p></section>
<section id="trygt"><h2>En logg, ikke medisinske råd</h2><p>Feed Flow stiller ingen diagnoser og sier ikke hvor mye babyen din bør spise. Er du bekymret for måltider, våte bleier eller hvordan babyen har det, kontakt helsestasjonen eller legen.</p></section>
""",
        "faqs": [
            ("Finnes Feed Flow på norsk?", "Ja. Hele appen er på norsk, i tillegg til svensk, dansk, finsk og flere andre språk. Den følger språket på iPhonen din."),
            ("Er Feed Flow gratis?", "Ja. Logging av alle måltider, nedtellingen for flasken og deling med familien er gratis og uten reklame. Premium er valgfritt."),
            ("Kan vi være flere som logger?", "Ja. Inviter partner, besteforeldre eller barnevakt. Alle logger fra sin egen iPhone, og det er ingen grense på antall."),
            ("Hvor lagres dataene?", "På telefonen din og i din egen iCloud, ikke på en reklameplattform. Feed Flow har ingen reklame."),
            ("Finnes Feed Flow til Android?", "Nei, Feed Flow er foreløpig bare for iPhone."),
            ("Reklamerer Feed Flow for morsmelkerstatning?", "Nei. Det finnes ikke promotert innhold i appen: ingen reklame, ingen sponsede plasseringer og ingen betalt rangering av produkter. Per i dag har vi ingen sponsoravtale eller kommersiell avtale med noen produsent av morsmelkerstatning, flasker eller flaskesmokker. Produktlisten finnes av to grunner: så du kan notere hvilket produkt ditt eget barn får og se hva som fungerer for akkurat det barnet, og så appen kan regne næringsstoffer som vitamin D fra nettopp det produktet. Amming, pumpet melk, morsmelkerstatning og fast føde behandles likt. Appen fører loggen og gir deg oversikten. Den gir ingen råd om mating og foreslår aldri at du skal bytte måte å mate på. Feed Flow lager og selger ikke morsmelkerstatning, flasker eller smokker, så WHO-koden for markedsføring av morsmelkerstatninger gjelder formelt ikke for appen. Vi bryr oss likevel om det koden er til for: foreldre skal få informasjon, ikke markedsføring."),
        ],
        "related": [("/printables/feeding-log-nb-a4.pdf", "Matingslogg til utskrift (PDF)"), ("/no", "Til forsiden"), ("/", "In English")],
    },
    {
        "slug": "sv", "file": "sv.html", "lang": "sv", "active": "feeding", "date": "2026-11-16", "hreflang": HREFLANG,
        "title": "Feed Flow: Bebisapp för amning, flaska och ersättning | iPhone",
        "description": "Feed Flow är en bebisapp för iPhone, helt på svenska. Logga amning, pumpning, flaska och modersmjölksersättning i en tidslinje. Gratis att logga, utan reklam.",
        "eyebrow": "Bebisapp på svenska", "h1": "Matningslogg för amning, pumpning och flaska",
        "intro": "Feed Flow är appen för allt din bebis äter: amning, pumpning, bröstmjölk på flaska, ersättning och fast föda, i en och samma tidslinje. Appen finns helt på svenska, är byggd i Norge och det är gratis att logga. Ingen reklam, och datan ligger i ditt eget iCloud.",
        "image": "/screens/nordic/sv-03-360.webp", "srcset": "/screens/nordic/sv-03-360.webp 1x, /screens/nordic/sv-03-720.webp 2x", "width": 360, "height": 780,
        "alt": "Feed Flow på svenska: Idag-skärmen med senaste måltid, nästa måltid och dagens flaskor.",
        "body": f"""
<section id="matning"><h2>Allt din bebis äter, i en tidslinje</h2><p>Många börjar med anteckningar i mobilen, en lapp på kylskåpet och en separat app för pumpning. Feed Flow samlar allt på samma dag.</p><ul><li><strong>Amning:</strong> logga en amning med några få tryck.</li><li><strong>Pumpning:</strong> logga hur mycket du pumpade, bredvid det bebisen faktiskt drack.</li><li><strong>Flaska:</strong> bröstmjölk eller ersättning, gjord och drucken mängd i ml.</li><li><strong>Fast föda och vatten:</strong> i samma tidslinje, utanför mjölksumman.</li></ul><p>Dagens mjölksumma räknar ersättning, pumpad mjölk och amning (amning som en uppskattning, eftersom ingen kan se hur mycket bebisen dricker vid bröstet). Du får en siffra för dygnet i stället för att lägga ihop listor på kvällen.</p></section>
<section id="nedrakning"><h2>Nedräkning från att flaskan gjordes</h2><p>När du loggar en flaska startar en nedräkning från tiden den gjordes, och den syns på låsskärmen. Då ser du hur länge flaskan har stått utan att låsa upp telefonen. Standard är en timme för ersättning och två timmar för pumpad bröstmjölk, och du kan ändra båda i Inställningar.</p><img src="/screens/nordic/sv-01-360.webp" srcset="/screens/nordic/sv-01-360.webp 1x, /screens/nordic/sv-01-720.webp 2x" width="300" height="650" loading="lazy" decoding="async" alt="Feed Flow visar nedräkning för en flaska med ersättning." {IMG}><div class="note"><strong>Ett minnesstöd, inte en säkerhetssensor</strong><p>Nedräkningen mäter bara tid. Den vet inte hur flaskan har förvarats eller hur varmt det är i rummet. Följ det som står på förpackningen och BVC:s råd, och gör en ny flaska om du är osäker.</p></div></section>
<section id="dela"><h2>Hela familjen i samma logg</h2><p>Bjud in din partner, mor- och farföräldrar eller barnvakten. Alla loggar från sin egen iPhone via sitt eget iCloud, utan gemensamt lösenord och utan gräns för hur många ni är. Då slipper ni frågan ”när åt hon senast?” vid varje överlämning. Delning är gratis.</p></section>
<section id="premium"><h2>Gratis, och Premium om du vill ha mer</h2><p>Loggning av alla måltider, nedräkningen för flaskan och delning med familjen är gratis, utan reklam. Premium lägger till:</p><ul><li><strong>FlowCast:</strong> ett troligt tidsfönster för nästa måltid, baserat på bebisens egen historik efter ungefär fyra dagars loggning. Ett planeringsstöd, inte ett schema.</li><li><strong>Tillväxtkurvor</strong> mot WHO:s referenser och full historik.</li><li><strong>Bebisrapport</strong> med matning och tillväxt som du kan ta med till BVC.</li></ul></section>
<section id="utskrift"><h2>Gratis matningslogg att skriva ut</h2><p>Föredrar du papper de första dagarna, eller behöver barnvakten en lapp på kylskåpet? Här är en gratis matningslogg på svenska: en sida per dygn med tid, amning, flaska, pumpning och blöjor.</p><img src="/printables/feeding-log-sv-480.webp" srcset="/printables/feeding-log-sv-480.webp 1x, /printables/feeding-log-sv-960.webp 2x" width="360" height="509" loading="lazy" decoding="async" alt="Matningslogg för nyfödd att skriva ut, en sida per dygn." {IMG}><p><a class="text-link" href="/printables/feeding-log-sv-a4.pdf" download>Ladda ner matningsloggen (PDF, A4) {ARROW}</a></p></section>
<section id="tryggt"><h2>En logg, inte medicinska råd</h2><p>Feed Flow ställer inga diagnoser och säger inte hur mycket din bebis borde äta. Är du orolig för måltider, blöta blöjor eller hur bebisen mår, kontakta BVC eller läkare.</p></section>
""",
        "faqs": [
            ("Finns Feed Flow på svenska?", "Ja. Hela appen finns på svenska, och även på norska, danska, finska och flera andra språk. Den följer språket på din iPhone."),
            ("Är Feed Flow gratis?", "Ja. Loggning av alla måltider, nedräkningen för flaskan och delning med familjen är gratis och utan reklam. Premium är valfritt."),
            ("Kan vi vara flera som loggar?", "Ja. Bjud in din partner, mor- och farföräldrar eller barnvakten. Alla loggar från sin egen iPhone, och det finns ingen gräns för antalet."),
            ("Var sparas datan?", "På din telefon och i ditt eget iCloud, inte på en reklamplattform. Feed Flow har ingen reklam."),
            ("Finns Feed Flow för Android?", "Nej, Feed Flow finns än så länge bara för iPhone."),
        ],
        "related": [("/printables/feeding-log-sv-a4.pdf", "Matningslogg att skriva ut (PDF)"), ("/no", "På norsk"), ("/", "In English")],
    },
]

NORDIC_QUERIES = {
    "no/matingslogg": ["app for amming", "matingslogg baby", "babyapp norsk", "app for flaskemating og MME", "ammeapp iPhone", "matingslogg til utskrift"],
    "sv": ["amningsapp", "bebisapp svenska", "matningslogg bebis", "app för flaskmatning och ersättning", "amning app iPhone", "matningsschema att skriva ut"],
}
