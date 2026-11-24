"""French (Canadian) version of the home page. Translates the site's own wording; story headlines stay in their original language;
our own "why it matters" lines on Our Picks come from note_fr in curated.json. Draft translation: needs a native French reviewer."""
import html, re, json
from pathlib import Path

try:
    PICK_FR = {p["note"]: p["note_fr"] for p in json.loads((Path(__file__).parent / "curated.json").read_text(encoding="utf-8")).get("picks", []) if p.get("note") and p.get("note_fr")}
except Exception:
    PICK_FR = {}

EXACT = {
    "🎬 Canadian film and TV production volume, up 4.6%": "🎬 Volume de production cinéma et télé au Canada, en hausse de 4,6 %",
    "👷 film and TV jobs in 2025–26, down 0.3%": "👷 emplois en cinéma et télé en 2025-2026, en baisse de 0,3 %",
    "🍁 Ontario film and TV jobs in 2025, with $2.7B for its economy": "🍁 emplois en cinéma et télé en Ontario en 2025, et 2,7 G$ pour son économie",
    "🥧 Who does Canada's post work: share of national revenue": "🥧 Qui fait le travail de postproduction au Canada : part des revenus nationaux",
    "Record": "Record", "year, 2023": "année 2023", "Quebec 49.0% → 40.7%": "Québec 49,0 % → 40,7 %", "British Columbia 28.7% → 36.8%": "Colombie-Britannique 28,7 % → 36,8 %",
    "All other provinces and territories 22.3% → 22.5%": "Toutes les autres provinces et territoires 22,3 % → 22,5 %",
    "Why it matters:": "Pourquoi c'est important :",
    "📊 By the numbers": "📊 En chiffres", "💵 post revenue in 2025, Statistics Canada": "💵 revenus de postproduction en 2025, Statistique Canada",
    "📉 since the 2023 record": "📉 depuis le record de 2023", "📈 vs 2019, before the pandemic": "📈 par rapport à 2019, avant la pandémie",
    "🧮 operating profit margin (6.0% in 2023)": "🧮 marge bénéficiaire d'exploitation (6,0 % en 2023)",
    "of VFX and animation sales now in B.C., ahead of Quebec at 40.4%": "des ventes d'effets visuels et d'animation sont maintenant en C.-B., devant le Québec à 40,4 %",
    "📊 See all the numbers and charts →": "📊 Voir tous les chiffres et graphiques (en anglais) →",
    "Every figure is read from the publisher's own page and linked there.": "Chaque chiffre est lu sur la page de l'éditeur et lié à celle-ci.",
    "🔑 Subscribers": "🔑 Abonnés",
    "🆕 NEW": "🆕 NOUVEAU",
    "● LIVE": "● EN DIRECT", "Next update in": "Prochaine mise à jour dans", "Last updated": "Dernière mise à jour", "All stories from the last 3 weeks:": "Tous les articles des 3 dernières semaines :",
    "☕ Buy us a coffee": "☕ Offrez-nous un café", "Support us.": "Soutenez-nous.",
    "⚙️ Choose what you see": "⚙️ Choisissez ce que vous voyez", "Tick what you want on this page. We remember your choices on this device.": "Cochez ce que vous voulez voir sur cette page. Nous retenons vos choix sur cet appareil.",
    "☕ Morning Roll": "☕ Rouleau du matin", "📼 Past 10 days of the roll": "📼 Les 10 derniers jours du rouleau", "🕐 Update clock": "🕐 Horloge de mise à jour", "⭐ Our Picks": "⭐ Nos choix",
    "📢 Industry feeds (CMPA, LinkedIn, Avid)": "📢 Fils de l'industrie (CMPA, LinkedIn, Avid)", "📰 All stories, tabs and search": "📰 Tous les articles, onglets et recherche", "📚 Resources and feedback": "📚 Ressources et commentaires",
    "Jump to:": "Aller à :", "Morning Roll": "Rouleau du matin", "Our Picks": "Nos choix", "All stories": "Tous les articles", "Resources": "Ressources", "Show everything": "Tout afficher",
    "← Latest news": "← Dernières nouvelles", "Picture Start": "Accueil",
    "Post Production Canada — the latest news in one place": "Post Production Canada — l'actualité canadienne de la postproduction, au même endroit",
    # menu
    "📰 News": "📰 Actualités", "🎬 Post Buzz": "🎬 Post Buzz", "🏆 Awards": "🏆 Prix", "🇨🇦 Canadian Stories": "🇨🇦 Histoires canadiennes", "🎥 Documentary": "🎥 Documentaire",
    "✂️ Craft": "✂️ Métier", "✂️ Editors": "✂️ Monteurs et monteuses", "📷 Cinematographers": "📷 Direction photo", "🤖 Digital Assistant Editor": "🤖 L'assistant monteur numérique",
    "📐 Delivery Specs": "📐 Spécifications de livraison", "🎞️ Cut in Canada": "🎞️ Monté au Canada", "🎚️ Vibe Cutting": "🎚️ Vibe Cutting", "💻 Software": "💻 Logiciels",
    "🎶 Sound & Emotion": "🎶 Son et émotion", "🎼 Composers": "🎼 Compositeurs", "🎸 Music Supervisors": "🎸 Superviseurs musicaux",
    "🤝 Unions, Guilds & Associations": "🤝 Syndicats, guildes et associations", "🎓 Learn and connect": "🎓 Apprendre et réseauter", "🏠 Start": "🏠 Début", "🏠 Home": "🏠 Accueil", "🎓 Education": "🎓 Formation", "🗺️ Union Map": "🗺️ Carte des syndicats",
    "⚖️ Status & Tax Credits": "⚖️ Statut de l'artiste et crédits d'impôt", "💰 Funding & Tax Credits": "💰 Financement et crédits d'impôt", "Funding & Tax Credits": "Financement et crédits d'impôt", "Funding and Tax Credits": "Financement et crédits d'impôt", "— the $600M federal funding split and the tax credits by province.": "— la répartition des 600 M$ fédéraux et les crédits d'impôt par province.", "— what the laws mean for Editors, with production by region.": "— ce que les lois signifient pour les monteurs et monteuses, avec la production par région.", "🤝 Networking": "🤝 Réseautage", "💚 Wellbeing": "💚 Bien-être",
    "🌍 Sustainability": "🌍 Durabilité", "🌍 Green Post": "🌍 Postproduction verte", "✉️ Contact": "✉️ Contact",
    # hero
    "All of Canada's": "Toute l'actualité de la", "POST PRODUCTION": "POSTPRODUCTION", "NEWS": "CANADIENNE", "in one place.": "au même endroit.",
    "Editing, colour, sound, VFX, animation and the business behind them — gathered from": "Montage, étalonnage, son, effets visuels, animation et l'industrie qui les soutient, rassemblés à partir de",
    "and updated live every few hours.": "et mis à jour en direct toutes les quelques heures.", "Free, always.": "Gratuit, toujours.",
    "Original articles and features are coming soon. Stay in the loop:": "Des articles originaux et des reportages s'en viennent. Restez dans la boucle :", "click here →": "cliquez ici →",
    # roll and clock
    "Read the full article →": "Lire l'article complet →", "🇨🇦 Key takeaways for Canada": "🇨🇦 L'essentiel pour le Canada",
    "stories in the last 7 days;": "articles dans les 7 derniers jours;", "have a Canadian angle.": "ont un angle canadien.", "Most-mentioned places:": "Lieux les plus mentionnés :",
    "Busiest topic:": "Sujet le plus actif :", "Counted from the stories on this page, not opinion. Pick a province or tab below to dig in.": "Calculé à partir des articles de cette page, sans opinion. Choisissez une province ou un onglet ci-dessous pour creuser.",
    "📼 Past 10 days of the Morning Roll": "📼 Les 10 derniers jours du Rouleau du matin", "Missed a morning? Open a day to see its six reels.": "Un matin manqué? Ouvrez une journée pour voir ses six bobines.",
    "Days marked here before the roll began saving itself were rebuilt from our story archive, so they may differ slightly from what ran that morning.": "Les journées antérieures à l'enregistrement automatique du rouleau ont été reconstituées à partir de nos archives, et peuvent donc différer légèrement de ce qui a été publié ce matin-là.",
    "TODAY": "AUJOURD'HUI", "NEXT UPDATE IN": "PROCHAINE MISE À JOUR DANS", "LAST UPDATED": "DERNIÈRE MISE À JOUR", "LAST 21 DAYS": "21 DERNIERS JOURS", "● NOW": "● MAINTENANT",
    "COAST TO COAST · ACTION!": "D'UN OCÉAN À L'AUTRE · ACTION !",
    # tabs
    "📰 All": "📰 Tout", "✂️ Picture Editing": "✂️ Montage d'image", "🎬 Storytelling & Filmmaking": "🎬 Récit et réalisation", "🎧 Sound Editing": "🎧 Montage sonore", "🟩 VFX & Animation": "🟩 Effets visuels et compositing", "🎥 Gear & Software": "🎥 Équipement et logiciels",
    "🛡️ DGC Member": "🛡️ Membre de la DGC", "✂️ CCE Member": "✂️ Membre du CCE",
    "💼 Business, Unions & Guilds": "💼 Affaires, syndicats et guildes", "🛠️ AI Tools, Workflows & Vibe Cutting": "🛠️ Outils d'IA, flux de travail et Vibe Cutting", "🎞️ AI Films & Festivals": "🎞️ Films et festivals d'IA", "🎭 AI, Actors & Rights": "🎭 IA, acteurs et droits", "🏢 AI & the Business": "🏢 L'IA et l'industrie", "🤖 AI": "🤖 IA", "🍿 Love of Movies": "🍿 Amour du cinéma", "🌱 Green & Sustainability": "🌱 Écologie et durabilité", "🔊 Sound Design": "🔊 Conception sonore",
    "💼 Business & Unions": "💼 Affaires et syndicats", "🤖 AI Filmmaking": "🤖 Cinéma et IA", "⚖️ Status of the Artist": "⚖️ Statut de l'artiste",
    "©️ Copyright & Legal": "©️ Droit d'auteur et juridique", "💡 Tips & Tricks": "💡 Trucs et astuces", "📍 All provinces": "📍 Toutes les provinces",
    "⭐ Our Picks": "⭐ Nos choix",
    "📢 Latest from the CMPA": "📢 Dernières nouvelles de la CMPA", "💼 Industry voices on LinkedIn": "💼 Voix de l'industrie sur LinkedIn", "🎛️ Latest from Avid": "🎛️ Dernières nouvelles d'Avid",
    "Nothing matches that. Try a different filter or search.": "Aucun résultat. Essayez un autre filtre ou une autre recherche.",
    # resources
    "Feedback and tips": "Commentaires et suggestions", "Spot something missing or wrong? Know a story, a source, or a Canadian Editor or director we should feature?": "Vous remarquez une omission ou une erreur? Vous connaissez une histoire, une source, ou un monteur ou une réalisatrice du Canada à mettre en vedette?",
    "Send feedback": "Envoyer un commentaire", "Resources": "Ressources",
    "— a directory of film and TV productions and companies, including post and VFX houses. Mostly US-focused; contact details are for paying members.": "— un répertoire de productions et d'entreprises de cinéma et de télévision, y compris des maisons de postproduction et d'effets visuels. Surtout centré sur les États-Unis; les coordonnées sont réservées aux membres payants.",
    "— trade news and features on": "— nouvelles et reportages de l'industrie sur la", "Post-Production": "postproduction", ", VFX, editing, colour and sound. Its stories also appear in the news feed above.": ", les effets visuels, le montage, l'étalonnage et le son. Ses articles figurent aussi dans le fil ci-dessus.",
    "— the non-profit association for Canadian picture Editors, plus the Vancouver Post Alliance.": "— l'association sans but lucratif des monteurs et monteuses d'image canadiens, ainsi que la Vancouver Post Alliance.",
    "— film incentives by province and a tracker of productions across Canada.": "— les incitatifs au cinéma par province et un suivi des productions partout au Canada.",
    "— the annual economic report on Canada's screen industry.": "— le rapport économique annuel sur l'industrie canadienne de l'écran.",
    "— the awards that honour Editors, sound, VFX and music supervision, with winners and IMDb links.": "— les prix qui honorent le montage, le son, les effets visuels et la supervision musicale, avec les lauréats et des liens IMDb.",
    "Documentary in Canada": "Le documentaire au Canada", "— a sourced timeline and where to watch.": "— une chronologie sourcée et où regarder.",
    "— mental health and work-life balance support for screen workers.": "— soutien en santé mentale et en conciliation travail-vie pour les travailleurs de l'écran.",
    "— sustainability programs and what they mean for post.": "— programmes de durabilité et ce qu'ils signifient pour la postproduction.",
    "Did you know that was cut in Canada?": "Saviez-vous que c'était monté au Canada?", "— movies and TV whose editing, effects or sound was done in Canada.": "— films et émissions dont le montage, les effets ou le son ont été réalisés au Canada.",
    "— editing by telling the software what you want, and how AI is wiring into editing software.": "— monter en disant au logiciel ce qu'on veut, et comment l'IA s'intègre aux logiciels de montage.",
    "Education across Canada": "La formation au Canada", "— colleges, universities and private schools teaching picture editing, sound and post.": "— collèges, universités et écoles privées qui enseignent le montage d'image, le son et la postproduction.",
    "Canadian Stories": "Histoires canadiennes", "— the Editors and directors from Canada behind screens the world watches.": "— les monteurs, monteuses et réalisateurs du Canada derrière les écrans que le monde regarde.",
    "Union Map": "Carte des syndicats", "— pick a province to see which unions and guilds cover Editors there.": "— choisissez une province pour voir quels syndicats et guildes représentent les monteurs et monteuses.",
    "Privacy": "Confidentialité", "— what we collect (almost nothing) and how the newsletter works.": "— ce que nous recueillons (presque rien) et le fonctionnement de l'infolettre.",
    "Status of the Artist and tax credits": "Statut de l'artiste et crédits d'impôt", "— what the laws mean for Editors, with credits by province.": "— ce que les lois signifient pour les monteurs et monteuses, avec les crédits par province.",
    "Updated": "Mis à jour",
    "Want your outlet, guild or studio added, or have a story tip?": "Vous voulez qu'on ajoute votre média, votre guilde ou votre studio, ou vous avez une idée de reportage?",
    "All rights reserved.": "Tous droits réservés.", "What we are.": "Qui nous sommes.",
    "A collective for Canada's post-production community. We compile publicly available information: news, resources and reference. We are always adding things, and we want to hear what is missing.": "Un collectif pour la communauté canadienne de la postproduction. Nous compilons de l'information publique : nouvelles, ressources et références. Nous ajoutons sans cesse du contenu et nous voulons savoir ce qui manque.",
    "Send it to us.": "Envoyez-le-nous.", "Story tips, events, festivals, schools, videos, corrections or removal requests are all welcome.": "Idées de reportages, événements, festivals, écoles, vidéos, corrections ou demandes de retrait : tout est bienvenu.",
    "Contact us": "Nous joindre", "Rights.": "Droits.",
    "Headlines and excerpts link to their original publishers, who keep all rights in their own work. Summaries and original text on this site are ours; please do not republish them without permission.": "Les titres et extraits renvoient à leurs éditeurs d'origine, qui conservent tous les droits sur leurs œuvres. Les résumés et textes originaux de ce site sont les nôtres; veuillez ne pas les republier sans permission.",
    "Please note.": "À noter.",
    "Explore": "Explorer", "Home": "Accueil", "By the Numbers": "Les chiffres", "Status of the Artist": "Statut de l'artiste",
    "Networking": "Réseautage", "Education": "Formation", "Follow & contact": "Suivre et nous joindre", "RSS feed": "Fil RSS", "Contact": "Contact",
    "All sources": "Toutes les sources",
    "Free news and resources for the Post Production community in Canada and around the world. Independent, and every story links to its publisher.": "Nouvelles et ressources gratuites pour la communauté de la postproduction au Canada et dans le monde. Indépendant : chaque article renvoie à son éditeur.",
    "Provided for information only, with no guarantee of accuracy or completeness, so check anything important with the source. We are independent, and not affiliated with or endorsed by any union, guild, association or company mentioned.": "Fourni à titre informatif seulement, sans garantie d'exactitude ni d'exhaustivité; vérifiez tout élément important auprès de la source. Nous sommes indépendants et n'avons aucun lien avec les syndicats, guildes, associations ou entreprises mentionnés, qui ne nous endossent pas.",
}
FRAG = [
    ("Post Production Canada shows headlines and short excerpts only. Every story links to its original publisher — go read them.", "Post Production Canada n'affiche que des titres et de courts extraits. Chaque article renvoie à son éditeur d'origine : allez les lire."),
    ("Post Production Canada shows headlines and short excerpts only. Every story links to its original publisher — go read them. Sources:", "Post Production Canada n'affiche que des titres et de courts extraits. Chaque article renvoie à son éditeur d'origine : allez les lire. Sources :"),
    ("Press releases from the Canadian Media Producers Association. From", "Communiqués de l'Association canadienne des producteurs médiatiques. Source :"),
    ("Articles from industry voices on LinkedIn. LinkedIn blocks automated readers, so these are added by hand and some show no date. From", "Articles de voix de l'industrie sur LinkedIn. LinkedIn bloque les lecteurs automatisés; ils sont donc ajoutés à la main et certains n'ont pas de date. Source :"),
    ("Press releases and release notes from Avid, maker of Media Composer and Pro Tools. From", "Communiqués et notes de version d'Avid, fabricant de Media Composer et de Pro Tools. Source :"),
    (". This list is updated by hand.", ". Cette liste est mise à jour à la main."),
    ("Your 8 a.m. rundown of the latest.", "Votre survol de 8 h de l'actualité."), ("Read it with your first coffee or tea.", "À lire avec votre premier café ou thé."),
    ("Preview edition: the first full roll compiles at 8 a.m. Eastern.", "Édition préliminaire : le premier rouleau complet est compilé à 8 h, heure de l'Est."),
    ("🇨🇦 Canadian angle:", "🇨🇦 Angle canadien :"), ("🌐 Wider industry story", "🌐 Histoire de l'industrie en général"),
]
MONTHS = {"Jan": "janv.", "Feb": "févr.", "Mar": "mars", "Apr": "avr.", "May": "mai", "Jun": "juin", "Jul": "juill.", "Aug": "août", "Sep": "sept.", "Oct": "oct.", "Nov": "nov.", "Dec": "déc."}
DAYS = {"Mon": "LUN", "Tue": "MAR", "Wed": "MER", "Thu": "JEU", "Fri": "VEN", "Sat": "SAM", "Sun": "DIM"}
DAYS_LONG = {"Monday": "lundi", "Tuesday": "mardi", "Wednesday": "mercredi", "Thursday": "jeudi", "Friday": "vendredi", "Saturday": "samedi", "Sunday": "dimanche"}
PROV = {"British Columbia": "Colombie-Britannique", "Saskatchewan": "Saskatchewan", "Atlantic Canada": "Canada atlantique", "Territories": "Territoires"}
ATTR = {
    "Toggle theme": "Changer de thème", "Morning Roll": "Rouleau du matin", "Past ten days of the Morning Roll": "Les dix derniers jours du Rouleau du matin", "Update clock": "Horloge de mise à jour",
    "Search stories": "Rechercher des articles", "Filter by province": "Filtrer par province", "Our picks": "Nos choix", "Sections": "Sections",
    "Search headlines — Resolve, Avid, Telefilm, Vancouver, tax credit…": "Rechercher des titres — Resolve, Avid, Téléfilm, Vancouver, crédit d'impôt…",
    "Back to the home page": "Retour à l'accueil", "Back to the top": "Retour en haut de la page", "Back to the home page (the 2 beep)": "Retour à l'accueil",
}


def _dyn(t):
    m = re.match(r"^MORNING ROLL · (\w{3}) (\w{3}) (\d+)$", t)
    if m:
        return f"LE ROULEAU DU MATIN · {DAYS.get(m.group(1), m.group(1))} {m.group(3)} {MONTHS.get(m.group(2), m.group(2)).upper()}"
    m = re.match(r"^(\w+), (\w{3}) (\d+), (\d{4})$", t)
    if m and m.group(1) in DAYS_LONG:
        return f"{DAYS_LONG[m.group(1)]} {m.group(3)} {MONTHS.get(m.group(2), m.group(2))} {m.group(4)}"
    m = re.match(r"^(\d+) sources$", t)
    if m:
        return f"{m.group(1)} sources"
    m = re.match(r"^\((\d+) stories\)\.$", t)
    if m:
        return f"({m.group(1)} articles)."
    m = re.match(r"^· (\d+) stories from the last three weeks\.$", t)
    if m:
        return f"· {m.group(1)} articles des trois dernières semaines."
    m = re.match(r"^(.+) \((\d+)\)$", t)
    if m and m.group(1) in PROV:
        return f"{PROV[m.group(1)]} ({m.group(2)})"
    m = re.match(r"^Page built (\S+)\. Post Production Canada is independent\. Summaries are ours,? and each (item|entry) links to its source\.$", t)
    if m:
        return f"Page créée le {m.group(1)}. Post Production Canada est indépendant. Les résumés sont les nôtres, et chaque {'élément' if m.group(2) == 'item' else 'entrée'} renvoie à sa source."
    m = re.match(r"^REEL (\d+)$", t)
    if m:
        return f"BOBINE {m.group(1)}"
    return None


_EX = {}
_PRE = []


def _setup(pairs):
    global _EX, _PRE
    _EX = {k: v for k, v in (pairs or [])}
    _PRE = sorted([(k, v) for k, v in (pairs or []) if len(k) >= 12], key=lambda kv: -len(kv[0]))


def _text(t, fragments):
    raw = t
    s = html.unescape(t.strip())
    if not s:
        return raw
    out = _EX.get(s) or EXACT.get(s) or _dyn(s)
    if out is None:
        for k, v in _PRE:
            if s.startswith(k):
                out = v
                break
    if out is None and fragments:
        out = s
        for en, fr in FRAG:
            out = out.replace(en, fr)
        m = re.search(r"Compiled (\d+):(\d+) (AM|PM) ET\.", out)
        if m:
            h = int(m.group(1)) % 12 + (12 if m.group(3) == "PM" else 0)
            out = out.replace(m.group(0), f"Compilé à {h} h {m.group(2)} (HE).")
        if out == s:
            return raw
    elif out is None:
        return raw
    lead = t[: len(t) - len(t.lstrip())]
    trail = t[len(t.rstrip()):]
    return lead + html.escape(out, quote=False) + trail


def to_french(page, pairs=None, title=None):
    _setup(pairs)
    parts = re.split(r"(<[^>]*>)", page)
    out, mode = [], None
    skip_re = re.compile(r"<(script|style|title)\b", re.I)
    for seg in parts:
        if seg.startswith("<"):
            low = seg.lower()
            if skip_re.match(low):
                mode = "skip"
            elif re.match(r"</(script|style)\b", low):
                mode = None
            elif re.match(r'<article class="(card|pick)\b', low):
                mode = "card"
            elif low.startswith("</article") and mode == "card":
                mode = None
            def rep(m):
                k = html.unescape(m.group(2))
                return m.group(1) + html.escape(ATTR[k], quote=True) + '"' if k in ATTR else m.group(0)
            seg = re.sub(r'((?:placeholder|aria-label|title)=")([^"]*)"', rep, seg)
            out.append(seg)
        elif mode == "skip":
            out.append(seg)
        elif mode == "card":
            _s = html.unescape(seg.strip())
            if _s == "Why it matters:":
                seg = seg.replace("Why it matters:", "Pourquoi c'est important :")
            elif _s in PICK_FR:
                seg = seg.replace(seg.strip(), html.escape(PICK_FR[_s], quote=False))
            out.append(seg)
        else:
            out.append(_text(seg, fragments=True))
    res = "".join(out)
    res = re.sub(r'(<button[^>]*>[^<]{0,6}<span class="nb">)postproduction', r'\1Postproduction', res)
    res = res.replace("<title>", "<title>", 1)
    res = re.sub(r"<title>[^<]*</title>", "<title>" + html.escape(title or "Post Production Canada — l'actualité canadienne de la postproduction, au même endroit", quote=False) + "</title>", res, count=1)
    res = re.sub(r'<html lang="[^"]*"', '<html lang="fr-CA"', res, count=1)
    return res


FR_PAGES = {"index.html": "fr.html", "networking.html": "fr-networking.html", "schools.html": "fr-schools.html"}


def localize_links(page):
    for en, fr in FR_PAGES.items():
        page = page.replace(f'href="{en}"', f'href="{fr}"')
    return page.replace('href="/"', 'href="fr.html"')
