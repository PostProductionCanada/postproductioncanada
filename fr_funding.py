"""French draft translation of the funding agencies directory on the Funding page.

PAIRS is built from agencies.AGENCIES, so each English text node is matched exactly. Only the directory
(and the page title and jump link) is translated; the rest of the Funding page stays in English for now.
"""
import agencies

TITLE = "Financement et crédits d'impôt — Post Production Canada"

WHERE = {
    "Federal": "Fédéral", "National": "National", "Ontario": "Ontario", "British Columbia": "Colombie-Britannique",
    "B.C. and Alberta": "C.-B. et Alberta", "Alberta": "Alberta", "Alberta (Edmonton)": "Alberta (Edmonton)",
    "Saskatchewan": "Saskatchewan", "Manitoba": "Manitoba", "Québec": "Québec",
    "Newfoundland and Labrador": "Terre-Neuve-et-Labrador", "Nova Scotia": "Nouvelle-Écosse",
    "New Brunswick": "Nouveau-Brunswick", "Prince Edward Island": "Île-du-Prince-Édouard", "Yukon": "Yukon",
    "Northwest Territories": "Territoires du Nord-Ouest", "Nunavut": "Nunavut", "By province": "Par province",
}

LABELS = {
    "Production Program": "Programme de production", "Indigenous funding": "Financement autochtone",
    "All CMF programs": "Tous les programmes du FMC", "Program deadlines": "Dates limites des programmes",
    "Prototyping": "Prototypage", "Innovation & Experimentation": "Innovation et expérimentation",
    "Commercial Projects": "Projets commerciaux", "Video Games Business Development": "Développement des affaires, jeux vidéo",
    "FAP program page": "Page du programme (ACIC)", "Explore and Create": "Explorer et créer",
    "ISO funding opportunities": "Occasions de financement du BEA", "Black Screen Office": "Bureau de l'écran des Noirs",
    "Canadian Film or Video Production Tax Credit": "Crédit d'impôt pour production cinématographique ou magnétoscopique canadienne",
    "Funding programs": "Programmes de financement", "STORYHIVE": "STORYHIVE",
    "Canadian Independent Screen Fund": "Canadian Independent Screen Fund",
    "Ontario Creates": "Ontario Creates", "Film and TV tax credit (OFTTC)": "Crédit d'impôt pour le cinéma et la télévision (OFTTC)",
    "Interactive sector page": "Page du secteur interactif", "Interactive digital media page": "Page des médias numériques interactifs",
    "Creative BC": "Creative BC", "Interactive Fund": "Fonds interactif", "Early Stage Growth": "Croissance en phase de démarrage",
    "Alberta Media Fund": "Alberta Media Fund", "Funding and incentives for film": "Financement et incitatifs pour le cinéma",
    "Alberta Made Production Grant": "Alberta Made Production Grant", "Edmonton Screen Industries": "Edmonton Screen Industries",
    "Film and TV production": "Production cinématographique et télévisuelle", "Digital Game Development": "Développement de jeux numériques",
    "Manitoba Film & Music": "Manitoba Film & Music", "SODEC": "SODEC", "Equity Investment Program": "Programme d'investissement en capital",
    "Incentive Fund": "Fonds d'incitation", "Screen Nova Scotia": "Screen Nova Scotia",
    "Province of New Brunswick": "Province du Nouveau-Brunswick", "CMPA: provinces and territories": "ACPM : provinces et territoires",
    "PEI Film Production Fund": "Fonds de production cinématographique de l'Î.-P.-É.", "Program framework": "Cadre du programme",
    "Film rebate": "Remise pour le cinéma", "Québec": "Québec", "B.C.": "C.-B.", "Manitoba": "Manitoba",
    "Newfoundland and Labrador": "Terre-Neuve-et-Labrador", "Nova Scotia": "Nouvelle-Écosse", "Ontario": "Ontario",
}

# English agency name -> (French name, French description)
FR = {
    "Telefilm Canada": ("Téléfilm Canada",
        "Organisme fédéral de financement des longs métrages canadiens. Son Programme de production finance des longs métrages à l'étape de la production ou de la postproduction, et il offre des volets distincts de développement et de production autochtones."),
    "Canada Media Fund (CMF)": ("Fonds des médias du Canada (FMC)",
        "Finance les contenus canadiens de télévision et numériques, et gère les principaux programmes fédéraux pour les projets interactifs. Sa liste de programmes couvre la production linéaire, ainsi que des programmes de médias numériques interactifs."),
    "CMF, game and interactive programs": ("FMC : programmes de jeux et d'interactif",
        "Les volets de médias numériques interactifs du FMC : conceptualisation, prototypage, innovation et expérimentation (applications logicielles innovantes et à la fine pointe) et projets commerciaux (projets ayant de plus grandes chances de succès commercial), ainsi que le Programme de développement des affaires des jeux vidéo du FMC et de Creative BC pour les entreprises de jeux appartenant à des intérêts de la C.-B. et sous leur contrôle."),
    "National Film Board: Filmmaker Assistance Program": ("Office national du film : Aide au cinéma indépendant du Canada (ACIC)",
        "Rembourse aux cinéastes indépendants sélectionnés leurs frais de postproduction. La page fixe le plafond à 7 500 $ par cinéaste pour un court métrage et à 15 000 $ pour un long métrage. Les cinéastes de Montréal ou à moins de 150 km peuvent plutôt obtenir des services de postproduction dans les studios de l'ONF, en payant 10 % du coût."),
    "Canada Council for the Arts: Explore and Create": ("Conseil des arts du Canada : Explorer et créer",
        "Subventions pour la recherche, le développement, la création, la production et la diffusion d'œuvres, y compris les arts médiatiques et numériques, ainsi que le perfectionnement professionnel. La page du programme montre des projets de cinéma et de documentaire parmi les bénéficiaires."),
    "Indigenous Screen Office (ISO)": ("Bureau de l'écran autochtone (BEA)",
        "Finance les créateurs de l'écran autochtones et les sociétés de production appartenant à des Autochtones, avec des programmes de développement et de production. Sa page renvoie aussi à des bailleurs de fonds externes."),
    "Black Screen Office (BSO)": ("Bureau de l'écran des Noirs (BEN)",
        "Organisme sans but lucratif qui dit exister pour appuyer les créateurs noirs, faire croître les entreprises dirigées par des Noirs et veiller à ce que les histoires noires soient créées et vues. Consultez son site pour les programmes en cours."),
    "CAVCO tax credits (Canadian Heritage)": ("Crédits d'impôt du BCPAC (Patrimoine canadien)",
        "Crédits d'impôt fédéraux : le crédit d'impôt pour production cinématographique ou magnétoscopique canadienne et le crédit d'impôt pour services de production cinématographique ou magnétoscopique. Ce sont des crédits d'impôt, et non des subventions, et ils sont réclamés par les sociétés de production."),
    "Bell Fund": ("Fonds Bell",
        "Soutient les producteurs indépendants canadiens. Ses programmes de financement comprennent un Programme de production pour les séries canadiennes et un programme de développement de portefeuille pour la propriété intellectuelle originale."),
    "TELUS STORYHIVE": ("TELUS STORYHIVE",
        "Financement, formation et distribution pour les créateurs nouveaux et émergents de la C.-B. et de l'Alberta, y compris des courts métrages et des séries non fictionnelles. Sa page d'accueil présente chaque édition en cours et ce qu'elle verse."),
    "Canadian Independent Screen Fund": ("Canadian Independent Screen Fund",
        "Une base de données de financement destinée aux cinéastes indépendants, qui répertorie les programmes par organisme et indique les règles d'admissibilité de chacun."),
    "Ontario Creates": ("Ontario Creates",
        "L'organisme de la province pour le cinéma et la télévision, les médias numériques interactifs, le livre, le magazine et la musique. Il gère des programmes de financement et administre les crédits d'impôt ontariens pour le cinéma et l'interactif. Les demandes passent par son portail de demandes en ligne."),
    "Ontario Creates: IP Fund, Interactive Stream": ("Ontario Creates : Fonds de PI, volet interactif",
        "Ontario Creates finance les jeux vidéo et les expériences de RX par son Fonds de propriété intellectuelle, avec un soutien additionnel des programmes de développement des marchés mondiaux, Futures Forward et de développement de l'industrie. Les lignes directrices 2026-2027 indiquent deux dates limites par année."),
    "Creative BC": ("Creative BC",
        "L'organisme de la C.-B. pour le cinéma, les médias numériques interactifs, la musique, le livre et le magazine. Il gère des subventions pour les créateurs et les entreprises, la commission du film et les crédits d'impôt provinciaux pour le cinéma."),
    "Creative BC: games and interactive": ("Creative BC : jeux et interactif",
        "Le Fonds interactif (avec le BC Arts Council) s'adresse aux projets de médias numériques interactifs. Selon sa FAQ, les jeux conventionnels, principalement commerciaux, ne sont pas admissibles cette année, car les jeux ont leurs propres fonds : les programmes de développement des affaires et de croissance en phase de démarrage des jeux vidéo. Au moment de lire les pages, le Fonds interactif et le projet pilote de croissance en phase de démarrage (subventions jusqu'à 50 000 $) étaient fermés."),
    "Alberta Media Fund": ("Alberta Media Fund",
        "Subventions pour la production à l'écran, y compris l'Alberta Made Production Grant pour les productions à plus petit budget et une subvention de postproduction. La page de financement de l'Alberta indique que la subvention de postproduction couvre jusqu'à 18 % des coûts de postproduction, y compris les effets visuels et l'animation numérique, jusqu'à un maximum de 200 000 $ par année. Sa subvention de développement de scénario classe les jeux vidéo sur console et en ligne parmi les projets non admissibles."),
    "Edmonton Screen Industries Office": ("Edmonton Screen Industries Office",
        "Financement et soutien pour les productions télévisuelles et de médias numériques interactifs de la région métropolitaine d'Edmonton, par l'entremise de l'Edmonton Screen Media Fund."),
    "Creative Saskatchewan": ("Creative Saskatchewan",
        "Organisme provincial qui investit dans les industries créatives. Son soutien au cinéma et à la télévision couvre la production de longs métrages et de télévision, et sa subvention de développement de jeux numériques comporte un volet de préproduction et un volet de production, avec des subventions allant jusqu'à 50 000 $ ou 50 % du budget en espèces par exercice, selon le moindre des deux (une propriété saskatchewanaise de 51 % est exigée)."),
    "Manitoba Film & Music": ("Manitoba Film & Music",
        "La commission du film du Manitoba, administratrice du crédit d'impôt manitobain pour la production cinématographique et vidéo, et bailleur de fonds de projets de cinéma et de musique. Elle a aussi mené un fonds manitobain pour courts métrages autochtones avec le Bureau de l'écran autochtone."),
    "SODEC": ("SODEC",
        "L'organisme québécois pour les entreprises culturelles. Il appuie le développement de scénarios, la production et la mise en marché de films, et administre les crédits d'impôt du Québec pour le cinéma et la télévision. Son site est principalement en français."),
    "PictureNL": ("PictureNL",
        "L'organisme principal de la province pour l'écran. Son Programme d'investissement en capital investit dans des productions de Terre-Neuve-et-Labrador; l'investissement est récupérable et peut être combiné au crédit d'impôt provincial pour le cinéma."),
    "Nova Scotia: Film and Television Production Incentive Fund": ("Nouvelle-Écosse : Fonds d'incitation à la production cinématographique et télévisuelle",
        "Le fonds d'incitation de la province pour la production cinématographique et télévisuelle. L'association de l'industrie Screen Nova Scotia gère un Content Creator Fund qui complète le financement des productions admissibles de la Nouvelle-Écosse."),
    "New Brunswick: film and TV programs": ("Nouveau-Brunswick : programmes de cinéma et de télévision",
        "Les programmes du gouvernement provincial pour le développement et la production de films, d'émissions de télévision et de nouveaux médias. L'ACPM indique un incitatif au développement et un incitatif à la production."),
    "PEI Film Production Fund": ("Fonds de production cinématographique de l'Î.-P.-É.",
        "Remises financières sur les dépenses pour les travaux réalisés à l'Î.-P.-É., afin d'encourager le développement, la formation et l'embauche de personnel de cinéma de l'Î.-P.-É."),
    "Yukon Location Incentive Program": ("Programme d'incitation au tournage du Yukon",
        "L'incitatif du Yukon pour les productions : une remise sur les déplacements, une remise sur les dépenses au Yukon et un volet de formation."),
    "NWT Film Commission": ("Commission du film des T.N.-O.",
        "La commission du film du territoire, qui gère une remise pour le cinéma destinée aux productions tournées dans les Territoires du Nord-Ouest."),
    "Nunavut Film Development Corporation": ("Société de développement du cinéma du Nunavut",
        "Organisme sans but lucratif qui offre du financement, de la formation et des services de commission du film au Nunavut, avec une série d'incitatifs financiers pour les cinéastes."),
    "Interactive digital media tax credits": ("Crédits d'impôt pour les médias numériques interactifs",
        "Crédits d'impôt provinciaux pour les studios de jeux et d'interactif. Le crédit ontarien (OIDMTC) est un crédit remboursable pouvant atteindre 40 % des dépenses admissibles en Ontario. Le crédit multimédia du Québec peut atteindre 37,5 % de la main-d'œuvre admissible, Investissement Québec délivrant l'attestation d'admissibilité. La C.-B., le Manitoba, Terre-Neuve-et-Labrador et la Nouvelle-Écosse publient chacun leur propre crédit."),
}

CHIPS = {"All": "Tous", "Film": "Cinéma", "TV": "Télé", "Documentary": "Documentaire", "Short film": "Court métrage",
         "Games and interactive": "Jeux et interactif", "Post-production": "Postproduction", "Indigenous": "Autochtone", "Tax credits": "Crédits d'impôt"}

PAIRS = [
    ("Funding and Tax Credits — Post Production Canada", TITLE),
    ("Jump to the funding agencies directory ↓", "Aller au répertoire des organismes de financement ↓"),
    ("Funding agencies for filmmakers and game makers", "Organismes de financement pour les cinéastes et les créateurs de jeux"),
    ("Every screen funder we could find in Canada, federal, provincial and territorial, with a link to the agency itself. Search by name or place, or filter by what you make. We describe each one as its own pages do. We leave out deadlines and amounts that change with each intake, so open the link for the current call.",
     "Tous les bailleurs de fonds de l'écran que nous avons trouvés au Canada, fédéraux, provinciaux et territoriaux, avec un lien vers l'organisme lui-même. Cherchez par nom ou par lieu, ou filtrez selon ce que vous créez. Nous décrivons chacun comme le font ses propres pages. Nous laissons de côté les dates limites et les montants qui changent à chaque appel : ouvrez le lien pour l'appel en cours."),
    ("Read on each agency's own pages in November 2026. Programs, rules and open dates change often, and some programs showed as closed or between intakes when we looked. If we missed a funder, tell us through the contact page. This is information, not advice.",
     "Lu sur les pages de chaque organisme en novembre 2026. Les programmes, les règles et les dates d'ouverture changent souvent, et certains programmes étaient fermés ou entre deux appels au moment de notre lecture. Si nous avons oublié un bailleur de fonds, dites-le-nous par la page de contact. Ce sont des renseignements, et non des conseils."),
] + list(CHIPS.items()) + list(WHERE.items()) + list(LABELS.items())

for a in agencies.AGENCIES:
    n, d = FR[a[0]]
    PAIRS.append((a[0], n))
    PAIRS.append((a[3], d))

# Strings inside the filter script, which the translator skips.
SCRIPT_FIXES = [('+" of "+cards.length+" shown"', '+" sur "+cards.length+" affichés"')]
