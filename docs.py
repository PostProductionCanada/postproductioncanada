"""Documentary section: a sourced timeline of Canadian documentary and where to find the work today."""
import html
import graphics, topics, provinces

e = html.escape

TIMELINE = [
    ("1897", "James Freer, an English-born settler in Manitoba, gets equipment and films the Canadian West. His Ten Years in Manitoba is the first known film by a Canadian, made partly to attract British settlers.",
     "https://en.wikipedia.org/wiki/Cinema_of_Canada"),
    ("1918", "The federal government creates the Exhibits and Publicity Bureau, renamed the Canadian Government Motion Picture Bureau in 1923. By 1920 it ran the largest studio and post-production facility in Canada and made the Seeing Canada travelogue series.",
     "https://thecanadianencyclopedia.ca/en/article/canadian-government-motion-picture-bureau"),
    ("1920s–30s", "Associated Screen News of Montréal, backed by the CPR, makes newsreels and shorts, including the Canadian Cameo series (1932–53). In Québec, priests Albert Tessier and Maurice Proulx film rural life, work considered early documentary.",
     "https://thecanadianencyclopedia.ca/en/article/the-history-of-film-in-canada"),
    ("1939", "The National Film Act is given royal assent on May 2 and creates the National Film Board. John Grierson, who coined the word “documentary”, becomes its first commissioner.",
     "https://www.ebsco.com/research-starters/film/national-film-act-1939-canada"),
    ("1940s", "Wartime series such as Canada Carries On and The World in Action reach audiences of millions.",
     "https://thecanadianencyclopedia.ca/en/article/documentary-film"),
    ("1950s", "Young NFB filmmakers in Unit B make Corral (1954), City of Gold (1957) and Lonely Boy (1961), and the Candid Eye series for TV. Lightweight 16mm cameras and portable sound change how documentaries are shot.",
     "https://thecanadianencyclopedia.ca/en/article/documentary-film"),
    ("1956–63", "The NFB moves to Montréal. Direct cinema flowers in Québec with Les Raquetteurs (1958), La Lutte (1961) and Pour la suite du monde (1963) by Pierre Perrault and Michel Brault.",
     "https://thecanadianencyclopedia.ca/en/article/documentary-film"),
    ("1967–80", "Challenge for Change puts film and video in the hands of communities. Over 200 films come out of it, including 27 about Fogo Island, Newfoundland. The Indian Film Crew is Canada’s first all-Indigenous production unit.",
     "https://en.wikipedia.org/wiki/National_Film_Board_of_Canada"),
    ("1993", "Hot Docs is founded by the Documentary Organization of Canada. It is now the largest documentary festival in North America.",
     "https://en.wikipedia.org/wiki/Hot_Docs_Canadian_International_Documentary_Festival"),
    ("Today", "A distinct Indigenous cinematic voice has emerged, and Canadian documentary is made on video by independents as much as at the NFB. Editors are honoured with their own documentary categories at the CCE, Canadian Screen and DGC Awards.",
     "https://thecanadianencyclopedia.ca/en/article/documentary-film"),
]

# Where each step happened (only where the source text names the place); CA = national / federal.
PLACE = {"1897": ["MB"], "1918": ["CA"], "1920s–30s": ["QC"], "1939": ["CA"], "1940s": ["CA"], "1950s": ["CA"],
         "1956–63": ["QC"], "1967–80": ["NL", "CA"], "1993": ["ON"], "Today": ["CA"]}
PLACE_NAME = {"MB": "Manitoba", "QC": "Québec", "NL": "Newfoundland and Labrador", "ON": "Ontario", "CA": "Canada"}
PLACE_COL = {"MB": "#b8860b", "QC": "#1d4ed8", "NL": "#0f766e", "ON": "#b91c1c", "CA": "#d52b1e"}

# Names that are still legends of Canadian film and TV. Each line is checked against the linked page.
LEGENDS = [
    ("Norman McLaren", "NFB animator. His film Neighbours won the Academy Award for Best Documentary Short.", "https://en.wikipedia.org/wiki/Norman_McLaren"),
    ("Colin Low", "NFB filmmaker behind Corral (1954) and, with Wolf Koenig, City of Gold (1957).", "https://www.imdb.com/name/nm0522800/"),
    ("Roman Kroitor", "Co-directed Lonely Boy (1961) and later co-founded IMAX.", "https://en.wikipedia.org/wiki/Roman_Kroitor"),
    ("Michel Brault", "Cinematographer and director, and Pierre Perrault's partner on Pour la suite du monde (1963).", "https://en.wikipedia.org/wiki/Michel_Brault"),
    ("Pierre Perrault", "Québec poet and filmmaker, a founder of direct cinema in Canada.", "https://en.wikipedia.org/wiki/Pierre_Perrault"),
    ("Allan King", "Documentary director of Warrendale (1967).", "https://www.imdb.com/name/nm0454437/"),
    ("Evelyn Lambart", "NFB animator who worked alongside Norman McLaren.", "https://en.wikipedia.org/wiki/Evelyn_Lambart"),
    ("Nell Shipman", "Silent-era actor, writer and director, and an early Canadian woman filmmaker.", "https://en.wikipedia.org/wiki/Nell_Shipman"),
    ("David Cronenberg", "Toronto director whose films reshaped body horror and Canadian cinema.", "https://en.wikipedia.org/wiki/David_Cronenberg"),
    ("Ronald Sanders", "Editor of David Cronenberg's films.", "https://www.imdb.com/name/nm0761697/"),
    ("Denis Villeneuve", "Québec director of Incendies, Arrival and Dune.", "https://en.wikipedia.org/wiki/Denis_Villeneuve"),
    ("Jean-Marc Vallée", "Québec director and Editor of Dallas Buyers Club and Big Little Lies, who died in 2021.", "https://en.wikipedia.org/wiki/Jean-Marc_Vall%C3%A9e"),
]

LINKS = [
    ("National Film Board of Canada", "Streams a large catalogue of Canadian documentary for free.", "https://www.nfb.ca"),
    ("Hot Docs", "The Toronto festival, with the Hot Docs Ted Rogers Cinema. The 2027 festival runs April 23 to May 2.", "https://hotdocs.ca/festivals/hot-docs-festival"),
    ("Documentary Organization of Canada", "The national association of independent documentary makers. It also lists mental health resources for filmmakers.", "https://docorg.ca/mental-health-resources"),
    ("Awards for documentary Editors", "CCE, Canadian Screen and DGC documentary editing winners.", "awards.html"),
]


def render(leaf, favicon, updated):
    css = ("<style>" + graphics.CSS + ".tl{list-style:none;margin:20px 0;padding:0 0 0 26px;border-left:3px solid var(--red)}"
           ".tl li{position:relative;margin:0 0 22px;padding:0 0 0 14px}.tl li::before{content:'';position:absolute;left:-36px;top:5px;width:14px;height:14px;border-radius:50%;background:var(--bg);border:3px solid var(--red)}"
           ".tl b{font:800 18px ui-monospace,Menlo,monospace;color:var(--red)}.tl p{margin:4px 0 2px}.tl a{font-size:13px}.pv{display:inline-block;color:#fff;font:700 11px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.06em;padding:4px 8px;border-radius:999px;margin-left:8px;vertical-align:middle}.lg{columns:2 280px;column-gap:16px;padding:0;list-style:none}.lg li{break-inside:avoid;margin:0 0 12px}.lg a{font-weight:700}</style>")
    chip = lambda y: " " + "".join(provinces.badge(k) for k in PLACE.get(y, []))
    tl = "".join('<li><b>' + e(y) + '</b> ' + chip(y) + '<p>' + e(t) + '</p><a href="' + e(u) + '" target="_blank" rel="noopener">Source</a></li>' for y, t, u in TIMELINE)
    links = "".join('<article class="box"><h3><a href="' + e(u) + '"' + (' target="_blank" rel="noopener"' if u.startswith("http") else "") + '>' + e(n) + '</a></h3><p>' + e(t) + '</p></article>' for n, t, u in LINKS)
    legends = "".join('<li><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(n) + '</a><br>' + e(t) + '</li>' for n, t, u in LEGENDS)
    body = (css + graphics.banner("A CENTURY OF CANADIAN STORIES", "Documentary Editors find the story in the footage.")
            + '<h2>More than a century, in ten steps</h2><p class="note">Every step links to its source. This is a short list, not a full history.</p><ol class="tl" style="list-style:none">' + tl + '</ol>'
            + '<div class="box"><b>Why the Editor matters most here.</b><p style="margin:6px 0 0">In documentary there is no script to follow. The story is found in the cutting room, and the Editor shapes it from hours of real footage. A longer original article on this history is in the members section.</p></div>'
            + '<h2>Legends who still shape Canadian film and TV</h2><p class="note">Each name links to Wikipedia or IMDb. Know a name that belongs here? Send it with a source.</p><ul class="lg">' + legends + '</ul>'
            + '<h2>Where to watch and learn</h2>' + links)
    return topics._page(leaf, favicon, updated, "Documentary in Canada",
                        "A sourced timeline of Canadian documentary from 1897 to today, and where to find the work.",
                        "🎥 Documentary in Canada",
                        "Canadians have been telling their own stories on film for more than a century. Here is how it happened.", body)
