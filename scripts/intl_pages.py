"""Localized landing pages (2026-11-16): /da /de /es /fi /fr /it /nl /pl /pt, same structure as /no and /sv.

The app is fully translated into these languages and the App Store screenshots are localized, so each page targets
local searches (Still-App, app de lactancia, imetyssovellus ...). One data dict per language: page copy, UI strings
for the shared renderer, and the printable log. Facts must match llms.txt. The countdown is a memory aid; follow the
label and the local health professional. No competitor claims. Native-speaker review welcome (not done yet).
"""

ARROW = '<svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#arrow"/></svg>'
IMG = 'style="max-width:100%;height:auto;border-radius:14px;border:1px solid var(--border);margin:8px 0 4px"'

# Every localized page, in footer order: (path, label, hreflang, print file code).
LANGS = [("/", "English", "en", "en"), ("/no", "Norsk", "nb", "nb"), ("/sv", "Svenska", "sv", "sv"),
         ("/da", "Dansk", "da", "da"), ("/de", "Deutsch", "de", "de"), ("/es", "Español", "es", "es"),
         ("/fi", "Suomi", "fi", "fi"), ("/fr", "Français", "fr", "fr"), ("/it", "Italiano", "it", "it"),
         ("/nl", "Nederlands", "nl", "nl"), ("/pl", "Polski", "pl", "pl"), ("/pt", "Português", "pt-BR", "pt")]
HREFLANG = [(code, "https://tryfeedflow.app" + path.rstrip("/") + ("/" if path == "/" else "")) for path, _, code, _ in LANGS] + [("x-default", "https://tryfeedflow.app/")]

C = {}

C["da"] = dict(
    lang="da", locale="da_DK", size="a4",
    title="Feed Flow: amning, flaske og modermælkserstatning | iPhone",
    description="Feed Flow er en babyapp til iPhone, helt på dansk. Log amning, pumpning, flaske og modermælkserstatning på én tidslinje. Gratis at logge, uden reklamer.",
    eyebrow="Babyapp på dansk", h1="Log til amning, pumpning og flaske",
    intro="Feed Flow er appen til alt, hvad din baby spiser: amning, pumpning, modermælk på flaske, modermælkserstatning og fast føde, på én tidslinje. Appen er helt på dansk, udviklet i Norge, og det er gratis at logge. Ingen reklamer, og dataene ligger i din egen iCloud.",
    alt1="Feed Flow på dansk: I dag-skærmen med seneste måltid, næste måltid og dagens flasker.",
    s1h="Alt, hvad din baby spiser, på én tidslinje", s1p="Mange starter med noter på telefonen, en seddel på køleskabet og en separat app til pumpning. Feed Flow samler det hele på samme dag.",
    li=[("Amning", "log en amning med få tryk."), ("Pumpning", "log hvor meget du har pumpet, ved siden af det din baby faktisk drak."), ("Flaske", "modermælk eller erstatning, lavet og drukket mængde i ml."), ("Fast føde og vand", "på samme tidslinje, holdt uden for mælketotalen.")],
    s1p2="Dagens mælketotal tæller erstatning, pumpet mælk og amning (amning som et skøn, da ingen kan se, hvor meget babyen drikker ved brystet).",
    s2h="Nedtælling fra flasken blev lavet", s2p="Når du logger en flaske, starter en nedtælling fra det tidspunkt, den blev lavet, og den vises på låseskærmen. Standard er én time for erstatning og to timer for pumpet modermælk, og du kan ændre begge i Indstillinger.",
    alt2="Feed Flow viser nedtællingen for en flaske med modermælkserstatning.",
    noteh="En huskehjælp, ikke en sikkerhedssensor", notep="Nedtællingen måler kun tid. Den ved ikke, hvordan flasken er opbevaret, eller hvor varmt der er i rummet. Følg anvisningen på pakken og sundhedsplejerskens råd, og lav en ny flaske, hvis du er i tvivl.",
    s3h="Hele familien i samme log", s3p="Inviter din partner, bedsteforældre eller babysitteren. Alle logger fra deres egen iPhone via deres egen iCloud, uden fælles adgangskode og uden grænse for, hvor mange I er. Deling er gratis.",
    s4h="Gratis, og Premium hvis du vil have mere", s4p="Logning af alle måltider, nedtællingen for flasken og deling med familien er gratis og uden reklamer. Premium tilføjer:",
    li4=[("FlowCast", "et sandsynligt tidsvindue for næste måltid, baseret på din babys egen historik efter cirka fire dages logning. En planlægningshjælp, ikke et skema."), ("Vækstkurver", "mod WHO's referencer og fuld historik."), ("Babyrapport", "med mad og vækst, som du kan vise sundhedsplejersken.")],
    s5h="Gratis amningsskema til print", s5p="Foretrækker du papir de første dage, eller skal babysitteren have en seddel på køleskabet? Her er et gratis skema på dansk: én side pr. døgn med tidspunkt, amning, flaske, pumpning og bleer.",
    alt3="Amnings- og madskema til print, én side pr. døgn.", dl="Hent skemaet (PDF, A4)",
    faqs=[("Findes Feed Flow på dansk?", "Ja. Hele appen er på dansk og følger sproget på din iPhone."), ("Er Feed Flow gratis?", "Ja. Logning af alle måltider, nedtællingen for flasken og deling med familien er gratis og uden reklamer. Premium er valgfrit."), ("Kan vi være flere, der logger?", "Ja. Alle logger fra deres egen iPhone, og der er ingen grænse for antallet."), ("Findes Feed Flow til Android?", "Nej, Feed Flow findes indtil videre kun til iPhone.")],
    queries=["amme app", "amningsskema", "babyapp dansk", "app til flaskemadning", "amningsskema til print"],
    ui=dict(skip="Gå til indholdet", download="Hent i App Store", download_sm="Hent", meta="Gratis at logge · iPhone · Dataene ligger i din egen iCloud", faq="Ofte stillede spørgsmål", explore="Se mere", aside1="Alt samlet ét sted", aside1p="Mad, vækst og helbred i én rolig app, helt på dansk.", aside2="En log, ikke lægefaglig rådgivning", aside2p="Feed Flow stiller ingen diagnoser, anbefaler ingen doser og erstatter ikke sundhedsplejersken, jordemoderen eller lægen.", more="Læs mere", lead="Én rolig log for mad, vækst og helbred.", tiers="Hent Feed Flow og begynd at logge i dag. Det er gratis at logge.", menu="Åbn menu",
            blurb="Feed Flow! er appen til amning, flaske og erstatning på iPhone, udviklet i Norge af Zeolite. Mad, vækst og babyens helbred i én rolig app med privatliv først.",
            nav=("Mad", "Nedtælling", "Udskrift", "Spørgsmål"), privacy="Privatliv (engelsk)", terms="Vilkår (engelsk)", pdf="Amningsskema (PDF)"),
    print=dict(title="Amnings- og madskema", date="Dato", baby="Barn", cols=["Tid", "Amning<br><small>V min / H min</small>", "Flaske lavet kl.", "Type<br><small>erstatning / modermælk</small>", "Givet", "Drukket", "Pumpet", "Våd", "Afføring", "Noter"], type="E &nbsp; MM", unit="ml", totals="Dagens total", t=["Måltider", "Drukket", "Pumpet", "Våde bleer", "Bleer m. afføring"],
               tip="Skriv ned, hvornår du laver hver flaske. Brug den inden for tiden på pakken eller sundhedsplejerskens råd, og lav en ny, hvis du er i tvivl.",
               foot="Gratis udskrift fra {url} &middot; En log, ikke lægefaglig rådgivning. Er du bekymret for måltider, våde bleer eller hvordan din baby har det, så kontakt sundhedsplejersken eller lægen."),
)

C["de"] = dict(
    lang="de", locale="de_DE", size="a4",
    title="Feed Flow: Still-App und Stillprotokoll für Babys | iPhone",
    description="Feed Flow ist eine Baby-App fürs iPhone, komplett auf Deutsch. Stillen, Abpumpen, Fläschchen und Säuglingsnahrung protokollieren. Kostenlos, ohne Werbung.",
    eyebrow="Baby-App auf Deutsch", h1="Stillprotokoll für Stillen, Abpumpen und Fläschchen",
    intro="Feed Flow ist die App für alles, was dein Baby trinkt und isst: Stillen, Abpumpen, Muttermilch im Fläschchen, Säuglingsnahrung und Beikost, in einer Zeitleiste. Die App ist komplett auf Deutsch, wurde in Norwegen entwickelt, und das Protokollieren ist kostenlos. Keine Werbung, und die Daten liegen in deiner eigenen iCloud.",
    alt1="Feed Flow auf Deutsch: der Heute-Bildschirm mit letzter Mahlzeit, nächster Mahlzeit und den Fläschchen des Tages.",
    s1h="Alles in einer Zeitleiste", s1p="Viele fangen mit Notizen im Handy, einem Zettel am Kühlschrank und einer eigenen App fürs Abpumpen an. Feed Flow bringt alles in denselben Tag.",
    li=[("Stillen", "eine Stillmahlzeit mit wenigen Tipps protokollieren."), ("Abpumpen", "festhalten, wie viel du abgepumpt hast, neben dem, was dein Baby tatsächlich getrunken hat."), ("Fläschchen", "Muttermilch oder Säuglingsnahrung, zubereitete und getrunkene Menge in ml."), ("Beikost und Wasser", "in derselben Zeitleiste, getrennt von der Milchsumme.")],
    s1p2="Die Milchsumme des Tages zählt Säuglingsnahrung, abgepumpte Milch und Stillen (Stillen als Schätzung, weil niemand sehen kann, wie viel ein Baby an der Brust trinkt).",
    s2h="Countdown ab der Zubereitung", s2p="Wenn du ein Fläschchen protokollierst, startet ein Countdown ab dem Zeitpunkt der Zubereitung, sichtbar auf dem Sperrbildschirm. Standard ist eine Stunde für Säuglingsnahrung und zwei Stunden für abgepumpte Muttermilch. Beides kannst du in den Einstellungen ändern.",
    alt2="Feed Flow zeigt den Countdown für ein Fläschchen mit Säuglingsnahrung.",
    noteh="Eine Gedächtnisstütze, kein Sicherheitssensor", notep="Der Countdown misst nur die Zeit. Er weiß nicht, wie das Fläschchen aufbewahrt wurde oder wie warm der Raum ist. Richte dich nach der Packungsangabe und dem Rat deiner Hebamme oder Kinderarztpraxis, und mach im Zweifel ein neues Fläschchen.",
    s3h="Die ganze Familie im selben Protokoll", s3p="Lade Partner, Großeltern oder Babysitter ein. Alle protokollieren vom eigenen iPhone über die eigene iCloud, ohne gemeinsames Passwort und ohne Begrenzung der Anzahl. Teilen ist kostenlos.",
    s4h="Kostenlos, und Premium, wenn du mehr willst", s4p="Alle Mahlzeiten protokollieren, der Fläschchen-Countdown und das Teilen mit der Familie sind kostenlos und ohne Werbung. Premium bietet zusätzlich:",
    li4=[("FlowCast", "ein wahrscheinliches Zeitfenster für die nächste Mahlzeit, basierend auf dem Verlauf deines Babys nach etwa vier Tagen Protokoll. Eine Planungshilfe, kein Zeitplan."), ("Wachstumskurven", "mit WHO-Referenzen und dem vollständigen Verlauf."), ("Babybericht", "mit Ernährung und Wachstum für die Hebamme oder die Kinderarztpraxis.")],
    s5h="Kostenloses Stillprotokoll zum Ausdrucken", s5p="Lieber Papier in den ersten Tagen, oder braucht der Babysitter einen Zettel am Kühlschrank? Hier ist ein kostenloses Protokoll auf Deutsch: eine Seite pro Tag mit Uhrzeit, Stillen, Fläschchen, Abpumpen und Windeln.",
    alt3="Stillprotokoll zum Ausdrucken, eine Seite pro Tag.", dl="Protokoll herunterladen (PDF, A4)",
    faqs=[("Gibt es Feed Flow auf Deutsch?", "Ja. Die ganze App ist auf Deutsch und folgt der Sprache deines iPhones."), ("Ist Feed Flow kostenlos?", "Ja. Alle Mahlzeiten protokollieren, der Fläschchen-Countdown und das Teilen mit der Familie sind kostenlos und ohne Werbung. Premium ist optional."), ("Können mehrere Personen protokollieren?", "Ja. Alle protokollieren vom eigenen iPhone, ohne Begrenzung der Anzahl."), ("Gibt es Feed Flow für Android?", "Nein, Feed Flow gibt es bisher nur fürs iPhone.")],
    queries=["Still-App", "Stillprotokoll", "Baby App Fläschchen", "Stillprotokoll zum Ausdrucken", "Baby Tracker App Deutsch"],
    ui=dict(skip="Zum Inhalt", download="Im App Store laden", download_sm="Laden", meta="Kostenlos protokollieren · iPhone · Daten in deiner eigenen iCloud", faq="Häufige Fragen", explore="Mehr", aside1="Alles an einem Ort", aside1p="Ernährung, Wachstum und Gesundheit in einer ruhigen App, komplett auf Deutsch.", aside2="Ein Protokoll, keine medizinische Beratung", aside2p="Feed Flow stellt keine Diagnosen, empfiehlt keine Dosierungen und ersetzt weder Hebamme noch Kinderarztpraxis.", more="Weiterlesen", lead="Ein ruhiges Protokoll für Ernährung, Wachstum und Gesundheit.", tiers="Lade Feed Flow und fang heute an. Protokollieren ist kostenlos.", menu="Menü öffnen",
            blurb="Feed Flow! ist die App für Stillen, Fläschchen und Säuglingsnahrung auf dem iPhone, entwickelt in Norwegen von Zeolite. Ernährung, Wachstum und Gesundheit in einer ruhigen App, Datenschutz zuerst.",
            nav=("Ernährung", "Countdown", "Ausdrucken", "Fragen"), privacy="Datenschutz (Englisch)", terms="Bedingungen (Englisch)", pdf="Stillprotokoll (PDF)"),
    print=dict(title="Stillprotokoll für Neugeborene", date="Datum", baby="Baby", cols=["Uhrzeit", "Stillen<br><small>L Min / R Min</small>", "Fläschchen um", "Art<br><small>Nahrung / Muttermilch</small>", "Angeboten", "Getrunken", "Abgepumpt", "Nass", "Stuhl", "Notizen"], type="SN &nbsp; MM", unit="ml", totals="Tagessumme", t=["Mahlzeiten", "Getrunken", "Abgepumpt", "Nasse Windeln", "Stuhlwindeln"],
               tip="Notiere, wann du jedes Fläschchen zubereitest. Verwende es innerhalb der Zeit auf der Packung oder nach dem Rat deiner Hebamme, und mach im Zweifel ein neues.",
               foot="Kostenlos von {url} &middot; Ein Protokoll, keine medizinische Beratung. Wenn du dir Sorgen um Mahlzeiten, nasse Windeln oder das Befinden deines Babys machst, wende dich an deine Hebamme oder Kinderarztpraxis."),
)

C["es"] = dict(
    lang="es", locale="es_MX", size="letter",
    title="Feed Flow: app de lactancia y biberones para bebés | iPhone",
    description="Feed Flow es una app para bebés en iPhone, totalmente en español. Registra lactancia, extracción, biberones y fórmula. Gratis y sin anuncios.",
    eyebrow="App para bebés en español", h1="Registro de lactancia, extracción y biberones",
    intro="Feed Flow es la app para todo lo que come tu bebé: lactancia, extracción, leche materna en biberón, fórmula y sólidos, en una sola línea de tiempo. La app está totalmente en español, se creó en Noruega y registrar es gratis. Sin anuncios, y los datos se guardan en tu propio iCloud.",
    alt1="Feed Flow en español: la pantalla Hoy con la última toma, la próxima toma y los biberones del día.",
    s1h="Todo en una sola línea de tiempo", s1p="Muchas familias empiezan con notas en el celular, un papel en el refrigerador y otra app para la extracción. Feed Flow lo junta todo en el mismo día.",
    li=[("Lactancia", "registra una toma en pocos toques."), ("Extracción", "anota cuánto te extrajiste, junto a lo que tu bebé realmente tomó."), ("Biberones", "leche materna o fórmula, cantidad preparada y tomada en ml."), ("Sólidos y agua", "en la misma línea de tiempo, fuera del total de leche.")],
    s1p2="El total de leche del día suma fórmula, leche extraída y lactancia (la lactancia como estimación, porque nadie puede ver cuánto toma un bebé del pecho).",
    s2h="Cuenta regresiva desde que preparas el biberón", s2p="Al registrar un biberón empieza una cuenta regresiva desde la hora en que lo preparaste, visible en la pantalla bloqueada. Por defecto es una hora para la fórmula y dos horas para la leche materna extraída, y puedes cambiar ambas en Ajustes.",
    alt2="Feed Flow muestra la cuenta regresiva de un biberón de fórmula.",
    noteh="Una ayuda para recordar, no un sensor de seguridad", notep="La cuenta regresiva solo mide el tiempo. No sabe cómo se guardó el biberón ni qué temperatura hay en la habitación. Sigue las indicaciones del envase y de tu pediatra, y si tienes dudas, prepara uno nuevo.",
    s3h="Toda la familia en el mismo registro", s3p="Invita a tu pareja, a los abuelos o a quien cuide al bebé. Cada persona registra desde su propio iPhone con su propio iCloud, sin contraseña compartida y sin límite de cuidadores. Compartir es gratis.",
    s4h="Gratis, y Premium si quieres más", s4p="Registrar todas las tomas, la cuenta regresiva del biberón y compartir con la familia es gratis y sin anuncios. Premium añade:",
    li4=[("FlowCast", "una ventana probable para la próxima toma, basada en el historial de tu bebé tras unos cuatro días de registro. Una ayuda para planear, no un horario."), ("Curvas de crecimiento", "con las referencias de la OMS e historial completo."), ("Informe del bebé", "con alimentación y crecimiento para llevar al pediatra.")],
    s5h="Registro de tomas gratis para imprimir", s5p="¿Prefieres papel los primeros días, o quien cuida al bebé necesita una hoja en el refrigerador? Aquí tienes un registro gratis en español: una página por día con hora, lactancia, biberón, extracción y pañales.",
    alt3="Registro de tomas del recién nacido para imprimir, una página por día.", dl="Descargar el registro (PDF, tamaño carta)",
    faqs=[("¿Feed Flow está en español?", "Sí. Toda la app está en español y sigue el idioma de tu iPhone."), ("¿Feed Flow es gratis?", "Sí. Registrar todas las tomas, la cuenta regresiva del biberón y compartir con la familia es gratis y sin anuncios. Premium es opcional."), ("¿Podemos registrar varias personas?", "Sí. Cada persona registra desde su propio iPhone y no hay límite de cuidadores."), ("¿Feed Flow está disponible para Android?", "No, por ahora Feed Flow solo está disponible para iPhone.")],
    queries=["app de lactancia", "registro de tomas del bebé", "app para biberones", "registro de lactancia para imprimir", "app para bebés en español"],
    ui=dict(skip="Ir al contenido", download="Descargar en el App Store", download_sm="Descargar", meta="Registrar es gratis · iPhone · Los datos quedan en tu propio iCloud", faq="Preguntas frecuentes", explore="Ver más", aside1="Todo en un solo lugar", aside1p="Alimentación, crecimiento y salud en una app tranquila, totalmente en español.", aside2="Un registro, no consejo médico", aside2p="Feed Flow no diagnostica, no recomienda dosis y no reemplaza a tu pediatra, partera o especialista en lactancia.", more="Sigue leyendo", lead="Un registro tranquilo para alimentación, crecimiento y salud.", tiers="Descarga Feed Flow y empieza a registrar hoy. Registrar es gratis.", menu="Abrir menú",
            blurb="Feed Flow! es la app de lactancia, biberones y fórmula para iPhone, creada en Noruega por Zeolite. Alimentación, crecimiento y salud del bebé en una app tranquila, con la privacidad primero.",
            nav=("Tomas", "Cuenta regresiva", "Imprimir", "Preguntas"), privacy="Privacidad (inglés)", terms="Términos (inglés)", pdf="Registro de tomas (PDF)"),
    print=dict(title="Registro de tomas del recién nacido", date="Fecha", baby="Bebé", cols=["Hora", "Pecho<br><small>I min / D min</small>", "Biberón hecho a las", "Tipo<br><small>fórmula / leche materna</small>", "Ofrecido", "Tomó", "Extraído", "Pipí", "Popó", "Notas"], type="F &nbsp; LM", unit="ml / oz", totals="Total del día", t=["Tomas", "Tomó", "Extraído", "Pañales mojados", "Pañales con popó"],
               tip="Anota la hora en que preparas cada biberón. Úsalo dentro del tiempo que indica el envase o tu pediatra, y si tienes dudas, prepara uno nuevo.",
               foot="Gratis en {url} &middot; Un registro, no consejo médico. Si te preocupa cómo come tu bebé, los pañales mojados o cómo se ve, consulta a tu pediatra."),
)

C["fi"] = dict(
    lang="fi", locale="fi_FI", size="a4",
    title="Feed Flow: Vauvasovellus imetykseen ja pulloruokintaan",
    description="Feed Flow on iPhonen vauvasovellus suomeksi. Kirjaa imetys, pumppaus, pullot ja äidinmaidonkorvike samalle aikajanalle. Ilmainen kirjata, ei mainoksia.",
    eyebrow="Vauvasovellus suomeksi", h1="Syöttöseuranta imetykseen, pumppaukseen ja pulloon",
    intro="Feed Flow on sovellus kaikkeen, mitä vauvasi syö: imetys, pumppaus, äidinmaito pullosta, korvike ja kiinteät ruoat samalla aikajanalla. Sovellus on kokonaan suomeksi, se on tehty Norjassa, ja kirjaaminen on ilmaista. Ei mainoksia, ja tiedot ovat omassa iCloudissasi.",
    alt1="Feed Flow suomeksi: Tänään-näkymä, jossa viimeisin syöttö, seuraava syöttö ja päivän pullot.",
    s1h="Kaikki samalla aikajanalla", s1p="Moni aloittaa muistiinpanoilla puhelimessa, lapulla jääkaapin ovessa ja erillisellä pumppaussovelluksella. Feed Flow kokoaa kaiken samaan päivään.",
    li=[("Imetys", "kirjaa imetys muutamalla napautuksella."), ("Pumppaus", "kirjaa, paljonko pumppasit, sen viereen, mitä vauva oikeasti joi."), ("Pullo", "äidinmaito tai korvike, valmistettu ja juotu määrä millilitroina."), ("Kiinteät ja vesi", "samalla aikajanalla, maitomäärän ulkopuolella.")],
    s1p2="Päivän maitomäärään lasketaan korvike, pumpattu maito ja imetys (imetys arviona, koska kukaan ei näe, paljonko vauva juo rinnalta).",
    s2h="Ajastin pullon valmistuksesta", s2p="Kun kirjaat pullon, ajastin käynnistyy valmistushetkestä ja näkyy lukitusnäytöllä. Oletus on tunti korvikkeelle ja kaksi tuntia pumpatulle äidinmaidolle, ja voit muuttaa molempia asetuksista.",
    alt2="Feed Flow näyttää korvikepullon ajastimen.",
    noteh="Muistin tuki, ei turvallisuusanturi", notep="Ajastin mittaa vain aikaa. Se ei tiedä, miten pulloa on säilytetty tai kuinka lämmin huone on. Noudata pakkauksen ohjetta ja neuvolan neuvoja, ja tee epävarmana uusi pullo.",
    s3h="Koko perhe samassa seurannassa", s3p="Kutsu kumppani, isovanhemmat tai lapsenvahti. Jokainen kirjaa omalla iPhonellaan oman iCloudinsa kautta, ilman yhteistä salasanaa ja ilman rajaa hoitajien määrälle. Jakaminen on ilmaista.",
    s4h="Ilmainen, ja Premium jos haluat enemmän", s4p="Kaikkien syöttöjen kirjaaminen, pullon ajastin ja jakaminen perheen kanssa ovat ilmaisia ja ilman mainoksia. Premium tuo lisäksi:",
    li4=[("FlowCast", "todennäköinen aikaikkuna seuraavalle syötölle vauvan oman historian perusteella, noin neljän päivän kirjaamisen jälkeen. Suunnittelun apu, ei aikataulu."), ("Kasvukäyrät", "WHO:n viitearvoja vasten ja koko historia."), ("Vauvaraportti", "syötöistä ja kasvusta, neuvolaan mukaan.")],
    s5h="Ilmainen tulostettava syöttöseuranta", s5p="Haluatko paperin ensimmäisiksi päiviksi, tai tarvitseeko lapsenvahti lapun jääkaapin oveen? Tässä ilmainen seurantalomake suomeksi: yksi sivu vuorokaudessa, kellonaika, imetys, pullo, pumppaus ja vaipat.",
    alt3="Tulostettava syöttöseuranta, yksi sivu vuorokaudessa.", dl="Lataa lomake (PDF, A4)",
    faqs=[("Onko Feed Flow suomeksi?", "Kyllä. Koko sovellus on suomeksi ja seuraa iPhonesi kieltä."), ("Onko Feed Flow ilmainen?", "Kyllä. Kaikkien syöttöjen kirjaaminen, pullon ajastin ja jakaminen perheen kanssa ovat ilmaisia ja ilman mainoksia. Premium on valinnainen."), ("Voiko kirjaajia olla useampi?", "Kyllä. Jokainen kirjaa omalla iPhonellaan, eikä hoitajien määrää ole rajattu."), ("Onko Feed Flow saatavilla Androidille?", "Ei, Feed Flow on toistaiseksi vain iPhonelle.")],
    queries=["imetyssovellus", "syöttöseuranta vauva", "vauvasovellus suomeksi", "imetysseuranta tulostettava", "pulloruokinta sovellus"],
    ui=dict(skip="Siirry sisältöön", download="Lataa App Storesta", download_sm="Lataa", meta="Ilmainen kirjata · iPhone · Tiedot omassa iCloudissasi", faq="Usein kysyttyä", explore="Lue lisää", aside1="Kaikki yhdessä paikassa", aside1p="Syöttö, kasvu ja terveys yhdessä rauhallisessa sovelluksessa, kokonaan suomeksi.", aside2="Seuranta, ei lääketieteellinen neuvo", aside2p="Feed Flow ei tee diagnooseja, ei suosittele annoksia eikä korvaa neuvolaa, kätilöä tai lääkäriä.", more="Lue lisää", lead="Yksi rauhallinen seuranta syötölle, kasvulle ja terveydelle.", tiers="Lataa Feed Flow ja aloita kirjaaminen tänään. Kirjaaminen on ilmaista.", menu="Avaa valikko",
            blurb="Feed Flow! on iPhonen sovellus imetykseen, pulloruokintaan ja korvikkeeseen, Zeoliten tekemä Norjassa. Syöttö, kasvu ja vauvan terveys yhdessä rauhallisessa sovelluksessa, yksityisyys edellä.",
            nav=("Syöttö", "Ajastin", "Tulosta", "Kysymykset"), privacy="Tietosuoja (englanniksi)", terms="Ehdot (englanniksi)", pdf="Syöttöseuranta (PDF)"),
    print=dict(title="Vastasyntyneen syöttöseuranta", date="Päivä", baby="Vauva", cols=["Klo", "Imetys<br><small>V min / O min</small>", "Pullo tehty klo", "Tyyppi<br><small>korvike / äidinmaito</small>", "Tarjottu", "Juotu", "Pumpattu", "Märkä", "Kakka", "Muistiinpanot"], type="K &nbsp; ÄM", unit="ml", totals="Päivän yhteensä", t=["Syötöt", "Juotu", "Pumpattu", "Märät vaipat", "Kakkavaipat"],
               tip="Kirjaa, milloin teet kunkin pullon. Käytä se pakkauksessa tai neuvolan ohjeissa mainitun ajan sisällä, ja tee epävarmana uusi.",
               foot="Ilmainen tuloste: {url} &middot; Seuranta, ei lääketieteellinen neuvo. Jos olet huolissasi syömisestä, märistä vaipoista tai vauvan voinnista, ota yhteyttä neuvolaan tai lääkäriin."),
)

C["fr"] = dict(
    lang="fr", locale="fr_FR", size="a4",
    title="Feed Flow : appli d'allaitement et de biberons | iPhone",
    description="Feed Flow, l'appli bébé pour iPhone entièrement en français. Notez l'allaitement, le tire-lait, les biberons et le lait infantile. Gratuit, sans publicité.",
    eyebrow="Appli bébé en français", h1="Suivi de l'allaitement, du tire-lait et des biberons",
    intro="Feed Flow est l'appli pour tout ce que mange votre bébé : allaitement, tire-lait, lait maternel au biberon, lait infantile et diversification, sur une seule chronologie. L'appli est entièrement en français, conçue en Norvège, et la saisie est gratuite. Pas de publicité, et les données restent dans votre propre iCloud.",
    alt1="Feed Flow en français : l'écran Aujourd'hui avec le dernier repas, le prochain repas et les biberons du jour.",
    s1h="Tout sur une seule chronologie", s1p="Beaucoup de parents commencent avec des notes sur le téléphone, un papier sur le frigo et une autre appli pour le tire-lait. Feed Flow réunit tout dans la même journée.",
    li=[("Allaitement", "notez une tétée en quelques touches."), ("Tire-lait", "notez la quantité tirée, à côté de ce que votre bébé a réellement bu."), ("Biberons", "lait maternel ou lait infantile, quantité préparée et bue en ml."), ("Diversification et eau", "sur la même chronologie, hors du total de lait.")],
    s1p2="Le total de lait du jour compte le lait infantile, le lait tiré et l'allaitement (l'allaitement sous forme d'estimation, puisque personne ne voit combien un bébé boit au sein).",
    s2h="Un compte à rebours depuis la préparation du biberon", s2p="Quand vous notez un biberon, un compte à rebours démarre à l'heure de sa préparation et s'affiche sur l'écran verrouillé. Par défaut, une heure pour le lait infantile et deux heures pour le lait maternel tiré, modifiables dans les Réglages.",
    alt2="Feed Flow affiche le compte à rebours d'un biberon de lait infantile.",
    noteh="Un aide-mémoire, pas un capteur de sécurité", notep="Le compte à rebours ne mesure que le temps. Il ne sait pas comment le biberon a été conservé ni quelle est la température de la pièce. Suivez les indications de l'emballage et les conseils de votre sage-femme ou de votre pédiatre, et en cas de doute, préparez-en un nouveau.",
    s3h="Toute la famille dans le même suivi", s3p="Invitez votre partenaire, les grands-parents ou la nounou. Chacun note depuis son propre iPhone avec son propre iCloud, sans mot de passe partagé et sans limite de personnes. Le partage est gratuit.",
    s4h="Gratuit, et Premium si vous voulez plus", s4p="Noter tous les repas, le compte à rebours du biberon et le partage avec la famille sont gratuits et sans publicité. Premium ajoute :",
    li4=[("FlowCast", "un créneau probable pour le prochain repas, basé sur l'historique de votre bébé après environ quatre jours de saisie. Une aide pour s'organiser, pas un horaire."), ("Courbes de croissance", "avec les références de l'OMS et l'historique complet."), ("Rapport bébé", "alimentation et croissance, à montrer au pédiatre.")],
    s5h="Fiche de suivi des repas gratuite à imprimer", s5p="Vous préférez le papier les premiers jours, ou la nounou a besoin d'une feuille sur le frigo ? Voici une fiche gratuite en français : une page par jour avec l'heure, l'allaitement, le biberon, le tire-lait et les couches.",
    alt3="Fiche de suivi des repas du nouveau-né à imprimer, une page par jour.", dl="Télécharger la fiche (PDF, A4)",
    faqs=[("Feed Flow est-il en français ?", "Oui. Toute l'appli est en français et suit la langue de votre iPhone."), ("Feed Flow est-il gratuit ?", "Oui. Noter tous les repas, le compte à rebours du biberon et le partage avec la famille sont gratuits et sans publicité. Premium est facultatif."), ("Peut-on être plusieurs à noter ?", "Oui. Chacun note depuis son propre iPhone, sans limite de personnes."), ("Feed Flow existe-t-il sur Android ?", "Non, Feed Flow est pour l'instant disponible uniquement sur iPhone.")],
    queries=["application allaitement", "suivi biberon bébé appli", "appli bébé en français", "fiche suivi allaitement à imprimer", "tableau biberons bébé"],
    ui=dict(skip="Aller au contenu", download="Télécharger dans l'App Store", download_sm="Télécharger", meta="Saisie gratuite · iPhone · Vos données restent dans votre iCloud", faq="Questions fréquentes", explore="Découvrir", aside1="Tout au même endroit", aside1p="Alimentation, croissance et santé dans une appli apaisante, entièrement en français.", aside2="Un suivi, pas un avis médical", aside2p="Feed Flow ne pose pas de diagnostic, ne recommande pas de doses et ne remplace pas votre sage-femme, votre pédiatre ou votre médecin.", more="À lire aussi", lead="Un suivi apaisant pour l'alimentation, la croissance et la santé.", tiers="Téléchargez Feed Flow et commencez aujourd'hui. La saisie est gratuite.", menu="Ouvrir le menu",
            blurb="Feed Flow! est l'appli d'allaitement, de biberons et de lait infantile pour iPhone, conçue en Norvège par Zeolite. Alimentation, croissance et santé de bébé dans une appli apaisante, respectueuse de la vie privée.",
            nav=("Repas", "Compte à rebours", "Imprimer", "Questions"), privacy="Confidentialité (anglais)", terms="Conditions (anglais)", pdf="Fiche de suivi (PDF)"),
    print=dict(title="Suivi des repas du nouveau-né", date="Date", baby="Bébé", cols=["Heure", "Sein<br><small>G min / D min</small>", "Biberon préparé à", "Type<br><small>lait infantile / maternel</small>", "Proposé", "Bu", "Tiré", "Pipi", "Selles", "Notes"], type="LI &nbsp; LM", unit="ml", totals="Total du jour", t=["Repas", "Bu", "Tiré", "Couches mouillées", "Couches avec selles"],
               tip="Notez l'heure de préparation de chaque biberon. Utilisez-le dans le délai indiqué sur l'emballage ou par votre sage-femme, et en cas de doute, préparez-en un nouveau.",
               foot="Fiche gratuite de {url} &middot; Un suivi, pas un avis médical. En cas d'inquiétude sur les repas, les couches mouillées ou l'état de votre bébé, contactez votre sage-femme, votre pédiatre ou votre médecin."),
)

C["it"] = dict(
    lang="it", locale="it_IT", size="a4",
    title="Feed Flow: app per allattamento, biberon e latte artificiale",
    description="Feed Flow è un'app per neonati su iPhone, completamente in italiano. Registra allattamento, tiralatte, biberon e latte artificiale. Gratis, senza pubblicità.",
    eyebrow="App per neonati in italiano", h1="Diario dell'allattamento, del tiralatte e dei biberon",
    intro="Feed Flow è l'app per tutto ciò che mangia il tuo bambino: allattamento, tiralatte, latte materno nel biberon, latte artificiale e svezzamento, in un'unica cronologia. L'app è completamente in italiano, è nata in Norvegia e registrare è gratis. Niente pubblicità, e i dati restano nel tuo iCloud.",
    alt1="Feed Flow in italiano: la schermata Oggi con l'ultimo pasto, il prossimo pasto e i biberon del giorno.",
    s1h="Tutto in un'unica cronologia", s1p="Molti genitori iniziano con note sul telefono, un foglio sul frigo e un'altra app per il tiralatte. Feed Flow mette tutto nella stessa giornata.",
    li=[("Allattamento", "registra una poppata con pochi tocchi."), ("Tiralatte", "segna quanto hai tirato, accanto a quello che il bambino ha davvero bevuto."), ("Biberon", "latte materno o artificiale, quantità preparata e bevuta in ml."), ("Svezzamento e acqua", "nella stessa cronologia, fuori dal totale di latte.")],
    s1p2="Il totale di latte del giorno conta latte artificiale, latte tirato e allattamento (l'allattamento come stima, perché nessuno vede quanto beve un bambino al seno).",
    s2h="Conto alla rovescia da quando prepari il biberon", s2p="Quando registri un biberon parte un conto alla rovescia dall'ora in cui l'hai preparato, visibile sulla schermata di blocco. Di default è un'ora per il latte artificiale e due ore per il latte materno tirato, e puoi cambiarle entrambe nelle Impostazioni.",
    alt2="Feed Flow mostra il conto alla rovescia di un biberon di latte artificiale.",
    noteh="Un promemoria, non un sensore di sicurezza", notep="Il conto alla rovescia misura solo il tempo. Non sa come è stato conservato il biberon né quanto è calda la stanza. Segui le indicazioni sulla confezione e i consigli del tuo pediatra, e nel dubbio preparane uno nuovo.",
    s3h="Tutta la famiglia nello stesso diario", s3p="Invita il partner, i nonni o la babysitter. Ognuno registra dal proprio iPhone con il proprio iCloud, senza password condivise e senza limiti di persone. La condivisione è gratis.",
    s4h="Gratis, e Premium se vuoi di più", s4p="Registrare tutte le poppate, il conto alla rovescia del biberon e la condivisione con la famiglia sono gratis e senza pubblicità. Premium aggiunge:",
    li4=[("FlowCast", "una finestra probabile per la prossima poppata, basata sulla storia del tuo bambino dopo circa quattro giorni di registrazioni. Un aiuto per organizzarti, non un orario."), ("Curve di crescita", "con i riferimenti OMS e lo storico completo."), ("Report del bambino", "con alimentazione e crescita da mostrare al pediatra.")],
    s5h="Diario delle poppate gratis da stampare", s5p="Preferisci la carta nei primi giorni, o alla babysitter serve un foglio sul frigo? Ecco un diario gratis in italiano: una pagina al giorno con ora, allattamento, biberon, tiralatte e pannolini.",
    alt3="Diario delle poppate del neonato da stampare, una pagina al giorno.", dl="Scarica il diario (PDF, A4)",
    faqs=[("Feed Flow è in italiano?", "Sì. Tutta l'app è in italiano e segue la lingua del tuo iPhone."), ("Feed Flow è gratis?", "Sì. Registrare tutte le poppate, il conto alla rovescia del biberon e la condivisione con la famiglia sono gratis e senza pubblicità. Premium è facoltativo."), ("Possiamo registrare in più persone?", "Sì. Ognuno registra dal proprio iPhone, senza limiti di persone."), ("Feed Flow è disponibile per Android?", "No, per ora Feed Flow è disponibile solo per iPhone.")],
    queries=["app allattamento", "diario poppate", "app neonato biberon", "diario poppate da stampare", "app per neonati in italiano"],
    ui=dict(skip="Vai al contenuto", download="Scarica su App Store", download_sm="Scarica", meta="Registrare è gratis · iPhone · I dati restano nel tuo iCloud", faq="Domande frequenti", explore="Scopri", aside1="Tutto in un posto", aside1p="Alimentazione, crescita e salute in un'app tranquilla, completamente in italiano.", aside2="Un diario, non un consiglio medico", aside2p="Feed Flow non fa diagnosi, non consiglia dosi e non sostituisce il pediatra, l'ostetrica o il medico.", more="Continua a leggere", lead="Un diario tranquillo per alimentazione, crescita e salute.", tiers="Scarica Feed Flow e inizia oggi. Registrare è gratis.", menu="Apri il menu",
            blurb="Feed Flow! è l'app per allattamento, biberon e latte artificiale su iPhone, creata in Norvegia da Zeolite. Alimentazione, crescita e salute del bambino in un'app tranquilla, con la privacy al primo posto.",
            nav=("Poppate", "Conto alla rovescia", "Stampa", "Domande"), privacy="Privacy (inglese)", terms="Termini (inglese)", pdf="Diario delle poppate (PDF)"),
    print=dict(title="Diario delle poppate del neonato", date="Data", baby="Bambino", cols=["Ora", "Seno<br><small>S min / D min</small>", "Biberon preparato alle", "Tipo<br><small>artificiale / materno</small>", "Offerto", "Bevuto", "Tirato", "Pipì", "Cacca", "Note"], type="LA &nbsp; LM", unit="ml", totals="Totale del giorno", t=["Poppate", "Bevuto", "Tirato", "Pannolini bagnati", "Pannolini con cacca"],
               tip="Annota l'ora in cui prepari ogni biberon. Usalo entro il tempo indicato sulla confezione o dal pediatra, e nel dubbio preparane uno nuovo.",
               foot="Gratis da {url} &middot; Un diario, non un consiglio medico. In caso di dubbi su poppate, pannolini bagnati o su come sta il bambino, contatta il pediatra."),
)

C["nl"] = dict(
    lang="nl", locale="nl_NL", size="a4",
    title="Feed Flow: app voor borstvoeding, flesvoeding en kolven | iPhone",
    description="Feed Flow is een baby-app voor iPhone, helemaal in het Nederlands. Houd borstvoeding, kolven, flesjes en kunstvoeding bij. Gratis, zonder advertenties.",
    eyebrow="Baby-app in het Nederlands", h1="Voedingslogboek voor borstvoeding, kolven en flesjes",
    intro="Feed Flow is de app voor alles wat je baby eet: borstvoeding, kolven, moedermelk uit de fles, kunstvoeding en vaste voeding, op één tijdlijn. De app is helemaal in het Nederlands, gemaakt in Noorwegen, en bijhouden is gratis. Geen advertenties, en de gegevens staan in je eigen iCloud.",
    alt1="Feed Flow in het Nederlands: het Vandaag-scherm met de laatste voeding, de volgende voeding en de flesjes van de dag.",
    s1h="Alles op één tijdlijn", s1p="Veel ouders beginnen met notities op hun telefoon, een briefje op de koelkast en een aparte app voor het kolven. Feed Flow zet alles op dezelfde dag.",
    li=[("Borstvoeding", "leg een voeding vast met een paar tikken."), ("Kolven", "noteer hoeveel je hebt gekolfd, naast wat je baby echt heeft gedronken."), ("Flesjes", "moedermelk of kunstvoeding, bereide en gedronken hoeveelheid in ml."), ("Vaste voeding en water", "op dezelfde tijdlijn, buiten het melktotaal.")],
    s1p2="Het melktotaal van de dag telt kunstvoeding, gekolfde melk en borstvoeding (borstvoeding als schatting, want niemand ziet hoeveel een baby aan de borst drinkt).",
    s2h="Aftellen vanaf het moment dat het flesje is gemaakt", s2p="Als je een flesje vastlegt, begint een aftelling vanaf het moment dat je het maakte, zichtbaar op je toegangsscherm. Standaard is dat een uur voor kunstvoeding en twee uur voor gekolfde moedermelk, en je kunt beide aanpassen in Instellingen.",
    alt2="Feed Flow toont de aftelling voor een flesje kunstvoeding.",
    noteh="Een geheugensteun, geen veiligheidssensor", notep="De aftelling meet alleen tijd. Ze weet niet hoe het flesje bewaard is of hoe warm de kamer is. Volg de verpakking en het advies van het consultatiebureau, en maak bij twijfel een nieuw flesje.",
    s3h="Het hele gezin in hetzelfde logboek", s3p="Nodig je partner, opa en oma of de oppas uit. Iedereen houdt bij vanaf de eigen iPhone via de eigen iCloud, zonder gedeeld wachtwoord en zonder limiet. Delen is gratis.",
    s4h="Gratis, en Premium als je meer wilt", s4p="Alle voedingen bijhouden, de aftelling voor het flesje en delen met het gezin zijn gratis en zonder advertenties. Premium voegt toe:",
    li4=[("FlowCast", "een waarschijnlijk tijdvenster voor de volgende voeding, gebaseerd op de eigen geschiedenis van je baby na ongeveer vier dagen bijhouden. Een hulp bij plannen, geen schema."), ("Groeicurves", "met WHO-referenties en de volledige geschiedenis."), ("Babyrapport", "met voeding en groei om mee te nemen naar het consultatiebureau.")],
    s5h="Gratis voedingsschema om te printen", s5p="Liever papier in de eerste dagen, of heeft de oppas een briefje op de koelkast nodig? Hier is een gratis schema in het Nederlands: één pagina per dag met tijd, borstvoeding, fles, kolven en luiers.",
    alt3="Voedingsschema voor een pasgeborene om te printen, één pagina per dag.", dl="Download het schema (PDF, A4)",
    faqs=[("Is Feed Flow in het Nederlands?", "Ja. De hele app is in het Nederlands en volgt de taal van je iPhone."), ("Is Feed Flow gratis?", "Ja. Alle voedingen bijhouden, de aftelling voor het flesje en delen met het gezin zijn gratis en zonder advertenties. Premium is optioneel."), ("Kunnen we met meerdere mensen bijhouden?", "Ja. Iedereen houdt bij vanaf de eigen iPhone, zonder limiet."), ("Is Feed Flow er voor Android?", "Nee, Feed Flow is voorlopig alleen voor iPhone.")],
    queries=["borstvoeding app", "voedingsschema baby", "flesvoeding app", "voedingsschema baby printen", "baby app Nederlands"],
    ui=dict(skip="Naar de inhoud", download="Download in de App Store", download_sm="Download", meta="Gratis bijhouden · iPhone · Gegevens in je eigen iCloud", faq="Veelgestelde vragen", explore="Bekijk", aside1="Alles op één plek", aside1p="Voeding, groei en gezondheid in één rustige app, helemaal in het Nederlands.", aside2="Een logboek, geen medisch advies", aside2p="Feed Flow stelt geen diagnoses, raadt geen doseringen aan en vervangt het consultatiebureau, de verloskundige of de arts niet.", more="Lees verder", lead="Eén rustig logboek voor voeding, groei en gezondheid.", tiers="Download Feed Flow en begin vandaag. Bijhouden is gratis.", menu="Menu openen",
            blurb="Feed Flow! is de app voor borstvoeding, flesjes en kunstvoeding op iPhone, gemaakt in Noorwegen door Zeolite. Voeding, groei en gezondheid van je baby in één rustige app, met privacy voorop.",
            nav=("Voeding", "Aftellen", "Printen", "Vragen"), privacy="Privacy (Engels)", terms="Voorwaarden (Engels)", pdf="Voedingsschema (PDF)"),
    print=dict(title="Voedingsschema pasgeborene", date="Datum", baby="Baby", cols=["Tijd", "Borst<br><small>L min / R min</small>", "Fles gemaakt om", "Soort<br><small>kunstvoeding / moedermelk</small>", "Aangeboden", "Gedronken", "Gekolfd", "Nat", "Poep", "Notities"], type="KV &nbsp; MM", unit="ml", totals="Totaal van de dag", t=["Voedingen", "Gedronken", "Gekolfd", "Natte luiers", "Poepluiers"],
               tip="Schrijf op wanneer je elk flesje maakt. Gebruik het binnen de tijd op de verpakking of volgens het consultatiebureau, en maak bij twijfel een nieuw flesje.",
               foot="Gratis van {url} &middot; Een logboek, geen medisch advies. Maak je je zorgen over voedingen, natte luiers of hoe je baby zich voelt, neem dan contact op met het consultatiebureau of de huisarts."),
)

C["pl"] = dict(
    lang="pl", locale="pl_PL", size="a4",
    title="Feed Flow: aplikacja do karmienia piersią i butelką | iPhone",
    description="Feed Flow to aplikacja dla niemowląt na iPhone'a, po polsku. Zapisuj karmienie piersią, odciąganie, butelki i mleko modyfikowane. Za darmo, bez reklam.",
    eyebrow="Aplikacja dla niemowląt po polsku", h1="Dziennik karmienia piersią, odciągania i butelek",
    intro="Feed Flow to aplikacja do wszystkiego, co je Twoje dziecko: karmienia piersią, odciągania, mleka mamy z butelki, mleka modyfikowanego i stałych pokarmów, na jednej osi czasu. Aplikacja jest w całości po polsku, powstała w Norwegii, a zapisywanie jest darmowe. Bez reklam, a dane zostają w Twoim własnym iCloud.",
    alt1="Feed Flow po polsku: ekran Dziś z ostatnim karmieniem, następnym karmieniem i butelkami z całego dnia.",
    s1h="Wszystko na jednej osi czasu", s1p="Wielu rodziców zaczyna od notatek w telefonie, kartki na lodówce i osobnej aplikacji do odciągania. Feed Flow zbiera wszystko w jednym dniu.",
    li=[("Karmienie piersią", "zapisz karmienie kilkoma dotknięciami."), ("Odciąganie", "zapisz, ile mleka odciągnięto, obok tego, co dziecko naprawdę wypiło."), ("Butelki", "mleko mamy lub modyfikowane, ilość przygotowana i wypita w ml."), ("Stałe pokarmy i woda", "na tej samej osi czasu, poza sumą mleka.")],
    s1p2="Dzienna suma mleka obejmuje mleko modyfikowane, odciągnięte i karmienie piersią (karmienie piersią jako szacunek, bo nikt nie widzi, ile dziecko wypija z piersi).",
    s2h="Odliczanie od przygotowania butelki", s2p="Gdy zapisujesz butelkę, rusza odliczanie od chwili jej przygotowania, widoczne na ekranie blokady. Domyślnie to godzina dla mleka modyfikowanego i dwie godziny dla odciągniętego mleka mamy, a oba czasy zmienisz w Ustawieniach.",
    alt2="Feed Flow pokazuje odliczanie dla butelki z mlekiem modyfikowanym.",
    noteh="Pomoc dla pamięci, nie czujnik bezpieczeństwa", notep="Odliczanie mierzy tylko czas. Nie wie, jak przechowywano butelkę ani jak ciepło jest w pokoju. Kieruj się opisem na opakowaniu i zaleceniami położnej lub pediatry, a w razie wątpliwości przygotuj nową butelkę.",
    s3h="Cała rodzina w jednym dzienniku", s3p="Zaproś partnera, dziadków albo nianię. Każdy zapisuje ze swojego iPhone'a przez własny iCloud, bez wspólnego hasła i bez limitu osób. Udostępnianie jest darmowe.",
    s4h="Za darmo, a Premium, jeśli chcesz więcej", s4p="Zapisywanie wszystkich karmień, odliczanie dla butelki i udostępnianie rodzinie są darmowe i bez reklam. Premium dodaje:",
    li4=[("FlowCast", "prawdopodobne okno czasowe kolejnego karmienia, oparte na historii Twojego dziecka po około czterech dniach zapisywania. Pomoc w planowaniu, nie harmonogram."), ("Krzywe wzrostu", "według norm WHO, z pełną historią."), ("Raport dziecka", "z karmieniem i wzrostem do pokazania pediatrze.")],
    s5h="Darmowy dziennik karmienia do druku", s5p="Wolisz papier w pierwszych dniach, albo niania potrzebuje kartki na lodówce? Oto darmowy dziennik po polsku: jedna strona na dobę z godziną, karmieniem piersią, butelką, odciąganiem i pieluchami.",
    alt3="Dziennik karmienia noworodka do druku, jedna strona na dobę.", dl="Pobierz dziennik (PDF, A4)",
    faqs=[("Czy Feed Flow jest po polsku?", "Tak. Cała aplikacja jest po polsku i używa języka Twojego iPhone'a."), ("Czy Feed Flow jest darmowy?", "Tak. Zapisywanie wszystkich karmień, odliczanie dla butelki i udostępnianie rodzinie są darmowe i bez reklam. Premium jest opcjonalne."), ("Czy kilka osób może zapisywać?", "Tak. Każdy zapisuje ze swojego iPhone'a, bez limitu osób."), ("Czy Feed Flow jest na Androida?", "Nie, na razie Feed Flow jest dostępny tylko na iPhone'a.")],
    queries=["aplikacja do karmienia piersią", "dziennik karmienia niemowlęcia", "aplikacja dla niemowląt po polsku", "dziennik karmienia do druku", "aplikacja karmienie butelką"],
    ui=dict(skip="Przejdź do treści", download="Pobierz z App Store", download_sm="Pobierz", meta="Zapisywanie za darmo · iPhone · Dane w Twoim iCloud", faq="Częste pytania", explore="Zobacz", aside1="Wszystko w jednym miejscu", aside1p="Karmienie, wzrost i zdrowie w jednej spokojnej aplikacji, w całości po polsku.", aside2="Dziennik, nie porada medyczna", aside2p="Feed Flow nie stawia diagnoz, nie zaleca dawek i nie zastępuje położnej, pediatry ani lekarza.", more="Czytaj dalej", lead="Jeden spokojny dziennik karmienia, wzrostu i zdrowia.", tiers="Pobierz Feed Flow i zacznij zapisywać już dziś. Zapisywanie jest darmowe.", menu="Otwórz menu",
            blurb="Feed Flow! to aplikacja do karmienia piersią, butelką i mlekiem modyfikowanym na iPhone'a, stworzona w Norwegii przez Zeolite. Karmienie, wzrost i zdrowie dziecka w jednej spokojnej aplikacji, z prywatnością na pierwszym miejscu.",
            nav=("Karmienie", "Odliczanie", "Do druku", "Pytania"), privacy="Prywatność (po angielsku)", terms="Warunki (po angielsku)", pdf="Dziennik karmienia (PDF)"),
    print=dict(title="Dziennik karmienia noworodka", date="Data", baby="Dziecko", cols=["Godz.", "Pierś<br><small>L min / P min</small>", "Butelka przygot. o", "Rodzaj<br><small>modyfikowane / mamy</small>", "Podane", "Wypite", "Odciągnięte", "Mokra", "Kupka", "Uwagi"], type="MM &nbsp; MP", unit="ml", totals="Suma dnia", t=["Karmienia", "Wypite", "Odciągnięte", "Mokre pieluchy", "Pieluchy z kupką"],
               tip="Zapisz, kiedy przygotowujesz każdą butelkę. Wykorzystaj ją w czasie podanym na opakowaniu lub zaleconym przez położną, a w razie wątpliwości przygotuj nową.",
               foot="Za darmo z {url} &middot; Dziennik, nie porada medyczna. Jeśli niepokoją Cię karmienia, liczba mokrych pieluch lub samopoczucie dziecka, skontaktuj się z położną, pediatrą lub lekarzem."),
)

C["pt"] = dict(
    lang="pt-BR", locale="pt_BR", size="a4",
    title="Feed Flow: app de amamentação e mamadeira para bebês | iPhone",
    description="Feed Flow é um app para bebês no iPhone, todo em português. Registre amamentação, extração, mamadeiras e fórmula em uma linha do tempo. Grátis e sem anúncios.",
    eyebrow="App para bebês em português", h1="Registro de mamadas, extração e mamadeiras",
    intro="Feed Flow é o app para tudo o que seu bebê come: amamentação, extração, leite materno na mamadeira, fórmula e introdução alimentar, em uma só linha do tempo. O app é todo em português, foi criado na Noruega e registrar é grátis. Sem anúncios, e os dados ficam no seu próprio iCloud.",
    alt1="Feed Flow em português: a tela Hoje com a última mamada, a próxima mamada e as mamadeiras do dia.",
    s1h="Tudo em uma só linha do tempo", s1p="Muitas famílias começam com anotações no celular, um papel na geladeira e outro app para a extração. O Feed Flow junta tudo no mesmo dia.",
    li=[("Amamentação", "registre uma mamada com poucos toques."), ("Extração", "anote quanto você tirou, ao lado do que o bebê realmente tomou."), ("Mamadeiras", "leite materno ou fórmula, quantidade preparada e tomada em ml."), ("Introdução alimentar e água", "na mesma linha do tempo, fora do total de leite.")],
    s1p2="O total de leite do dia soma fórmula, leite extraído e amamentação (a amamentação como estimativa, porque ninguém vê quanto o bebê mama no peito).",
    s2h="Contagem regressiva desde o preparo da mamadeira", s2p="Ao registrar uma mamadeira, começa uma contagem regressiva a partir da hora em que ela foi preparada, visível na tela bloqueada. O padrão é uma hora para fórmula e duas horas para leite materno extraído, e você pode mudar os dois em Ajustes.",
    alt2="Feed Flow mostra a contagem regressiva de uma mamadeira de fórmula.",
    noteh="Um lembrete, não um sensor de segurança", notep="A contagem só mede o tempo. Ela não sabe como a mamadeira foi guardada nem a temperatura do ambiente. Siga as orientações da embalagem e do seu pediatra e, na dúvida, prepare uma nova.",
    s3h="A família toda no mesmo registro", s3p="Convide quem divide os cuidados com você, os avós ou a babá. Cada pessoa registra do próprio iPhone, pelo próprio iCloud, sem senha compartilhada e sem limite de cuidadores. Compartilhar é grátis.",
    s4h="Grátis, e Premium se você quiser mais", s4p="Registrar todas as mamadas, a contagem regressiva da mamadeira e o compartilhamento com a família são grátis e sem anúncios. O Premium adiciona:",
    li4=[("FlowCast", "uma janela provável para a próxima mamada, com base no histórico do seu bebê depois de uns quatro dias de registro. Uma ajuda para planejar, não um horário fixo."), ("Curvas de crescimento", "com as referências da OMS e o histórico completo."), ("Relatório do bebê", "com alimentação e crescimento para levar ao pediatra.")],
    s5h="Registro de mamadas grátis para imprimir", s5p="Prefere papel nos primeiros dias, ou a babá precisa de uma folha na geladeira? Aqui está um registro grátis em português: uma página por dia com horário, amamentação, mamadeira, extração e fraldas.",
    alt3="Registro de mamadas do recém-nascido para imprimir, uma página por dia.", dl="Baixar o registro (PDF, A4)",
    faqs=[("O Feed Flow está em português?", "Sim. O app todo está em português e segue o idioma do seu iPhone."), ("O Feed Flow é grátis?", "Sim. Registrar todas as mamadas, a contagem regressiva da mamadeira e o compartilhamento com a família são grátis e sem anúncios. O Premium é opcional."), ("Mais de uma pessoa pode registrar?", "Sim. Cada pessoa registra do próprio iPhone, sem limite de cuidadores."), ("O Feed Flow tem versão para Android?", "Não, por enquanto o Feed Flow é só para iPhone.")],
    queries=["app de amamentação", "registro de mamadas", "app para bebê mamadeira", "tabela de mamadas para imprimir", "app para bebês em português"],
    ui=dict(skip="Pular para o conteúdo", download="Baixar na App Store", download_sm="Baixar", meta="Registrar é grátis · iPhone · Os dados ficam no seu iCloud", faq="Perguntas frequentes", explore="Ver mais", aside1="Tudo em um só lugar", aside1p="Alimentação, crescimento e saúde em um app tranquilo, todo em português.", aside2="Um registro, não um conselho médico", aside2p="O Feed Flow não faz diagnósticos, não recomenda doses e não substitui seu pediatra, obstetriz ou médico.", more="Continue lendo", lead="Um registro tranquilo para alimentação, crescimento e saúde.", tiers="Baixe o Feed Flow e comece a registrar hoje. Registrar é grátis.", menu="Abrir menu",
            blurb="Feed Flow! é o app de amamentação, mamadeira e fórmula para iPhone, criado na Noruega pela Zeolite. Alimentação, crescimento e saúde do bebê em um app tranquilo, com privacidade em primeiro lugar.",
            nav=("Mamadas", "Contagem", "Imprimir", "Perguntas"), privacy="Privacidade (inglês)", terms="Termos (inglês)", pdf="Registro de mamadas (PDF)"),
    print=dict(title="Registro de mamadas do recém-nascido", date="Data", baby="Bebê", cols=["Hora", "Peito<br><small>E min / D min</small>", "Mamadeira feita às", "Tipo<br><small>fórmula / leite materno</small>", "Oferecido", "Tomou", "Extraído", "Xixi", "Cocô", "Anotações"], type="F &nbsp; LM", unit="ml", totals="Total do dia", t=["Mamadas", "Tomou", "Extraído", "Fraldas com xixi", "Fraldas com cocô"],
               tip="Anote a hora em que prepara cada mamadeira. Use dentro do tempo indicado na embalagem ou pelo pediatra e, na dúvida, prepare uma nova.",
               foot="Grátis em {url} &middot; Um registro, não um conselho médico. Em caso de dúvida sobre as mamadas, as fraldas ou como o bebê está, fale com o pediatra."),
)


def _body(slug, c):
    li = "".join(f"<li><strong>{a}:</strong> {b}</li>" for a, b in c["li"])
    li4 = "".join(f"<li><strong>{a}:</strong> {b}</li>" for a, b in c["li4"])
    return f"""
<section id="feeding"><h2>{c['s1h']}</h2><p>{c['s1p']}</p><ul>{li}</ul><p>{c['s1p2']}</p></section>
<section id="countdown"><h2>{c['s2h']}</h2><p>{c['s2p']}</p><img src="/screens/nordic/{slug}-01-360.webp" srcset="/screens/nordic/{slug}-01-360.webp 1x, /screens/nordic/{slug}-01-720.webp 2x" width="300" height="650" loading="lazy" decoding="async" alt="{c['alt2']}" {IMG}><div class="note"><strong>{c['noteh']}</strong><p>{c['notep']}</p></div></section>
<section id="sharing"><h2>{c['s3h']}</h2><p>{c['s3p']}</p></section>
<section id="premium"><h2>{c['s4h']}</h2><p>{c['s4p']}</p><ul>{li4}</ul></section>
<section id="printable"><h2>{c['s5h']}</h2><p>{c['s5p']}</p><img src="/printables/feeding-log-{slug}-480.webp" srcset="/printables/feeding-log-{slug}-480.webp 1x, /printables/feeding-log-{slug}-960.webp 2x" width="360" height="509" loading="lazy" decoding="async" alt="{c['alt3']}" {IMG}><p><a class="text-link" href="{pdf_path(slug)}" download>{c['dl']} {ARROW}</a></p></section>
"""


def pdf_path(code):
    size = C[code]["size"] if code in C else "a4"
    return f"/printables/feeding-log-{code}-{size}.pdf"


INTL = []
for slug, c in C.items():
    INTL.append({
        "slug": slug, "file": f"{slug}.html", "lang": c["lang"], "ui": slug, "active": "feeding", "date": "2026-11-16", "hreflang": HREFLANG,
        "title": c["title"], "description": c["description"], "eyebrow": c["eyebrow"], "h1": c["h1"], "intro": c["intro"],
        "image": f"/screens/nordic/{slug}-03-360.webp", "srcset": f"/screens/nordic/{slug}-03-360.webp 1x, /screens/nordic/{slug}-03-720.webp 2x", "width": 360, "height": 780,
        "alt": c["alt1"], "body": _body(slug, c), "faqs": c["faqs"],
        "related": [(pdf_path(slug), c["ui"]["pdf"]), ("/", "In English"), ("/printable-feeding-log", "Printable feeding log (English)")],
    })

INTL_QUERIES = {slug: c["queries"] for slug, c in C.items()}

# UI strings and nav for the shared renderer (build-content.py merges these into L and NAV).
INTL_UI = {}
INTL_NAV = {}
for slug, c in C.items():
    u = dict(c["ui"])
    u["locale"] = c["locale"]
    u["footer_links"] = [("/", "English"), (pdf_path(slug), u["pdf"]), ("/support", "Support"), ("/privacy", u["privacy"]), ("/terms", u["terms"])]
    if slug == "es":
        u.update(breadcrumb="Ruta de navegación", related_info="Información relacionada")
    INTL_UI[slug] = u
    f, cd, pr, fq = u["nav"]
    INTL_NAV[slug] = [("feeding", f"/{slug}#feeding", f), ("countdown", f"/{slug}#countdown", cd), ("print", f"/{slug}#printable", pr), ("faq", f"/{slug}#faq", fq), ("en", "/", "English")]

# Printable sheet strings, keyed by file code (printables.py).
PRINT = {slug: dict(c["print"], foot=c["print"]["foot"].replace("{url}", f"tryfeedflow.app/{slug}"), lang=c["lang"]) for slug, c in C.items()}
