"""Composers: well-known Canadian screen composers and what they do. Facts read from the linked pages on AS_OF."""
import html
import topics, provinces

e = html.escape
AS_OF = "November 20, 2026"

WHAT = ("A screen composer writes the original score for a film, series or game, and usually records, orchestrates and delivers it too. "
        "That is different from a music supervisor, who finds and clears existing songs. For an Editor, the composer's score often arrives late in the cut, "
        "which is why temp music and the final score are such a big conversation in post.")

# (name, provinces, what they do, [(label, url)])
COMPOSERS = [
    ("Howard Shore", ["ON"],
     "Born in Toronto in 1946. Composer, conductor and orchestrator who has scored over 80 films. Best known for the scores of Peter Jackson's The Lord of the Rings and The Hobbit film trilogies. "
     "He has scored all but one of David Cronenberg's films since 1979, and has worked with Martin Scorsese on six films. His concert work includes the opera The Fly.",
     [("Official site", "https://howardshore.com"), ("Wikipedia", "https://en.wikipedia.org/wiki/Howard_Shore")]),
    ("Mychael Danna", ["MB", "ON"],
     "Born in Winnipeg, raised in Toronto, and a University of Toronto graduate. Composer of film and television scores. He won both the Golden Globe and the Oscar for Best Original Score for Life of Pi, "
     "and an Emmy for Outstanding Music Composition for a miniseries, movie or special.",
     [("Official site", "https://www.mychaeldanna.com/"), ("Wikipedia", "https://en.wikipedia.org/wiki/Mychael_Danna")]),
    ("Jeff Danna", ["ON"],
     "Born in Burlington, Ontario, and the younger brother of Mychael Danna. A film and television composer whose credits include The Boondock Saints, Silent Hill, The Good Dinosaur, The Addams Family, "
     "Onward and My Father's Dragon, and Guillermo del Toro's Tales of Arcadia. He and Mychael have shared Emmy nominations for Camelot, Tyrant and Alias Grace.",
     [("Official site", "https://www.jeffdanna.com"), ("Wikipedia", "https://en.wikipedia.org/wiki/Jeff_Danna")]),
    ("Christophe Beck", ["QC"],
     "Born and raised in Montréal. Best known for his work with Disney and its subsidiaries, including Frozen and Frozen 2, the Muppets films, and Marvel's Ant-Man films and the series WandaVision, Hawkeye and Agatha All Along. "
     "He also scored The Hangover films and Buffy the Vampire Slayer, which won him a Primetime Emmy.",
     [("Wikipedia", "https://en.wikipedia.org/wiki/Christophe_Beck")]),
    ("Mark Korven", ["SK", "ON"],
     "Born in Swift Current, Saskatchewan, and based in Toronto since 1987, where his first film score was Patricia Rozema's I've Heard the Mermaids Singing. "
     "His work includes the cult sci-fi horror film Cube and director Robert Eggers' period horror films The Witch and The Lighthouse.",
     [("Official site", "https://www.markkorven.com"), ("Wikipedia", "https://en.wikipedia.org/wiki/Mark_Korven")]),
    ("Lesley Barber", ["ON"],
     "Born in Toronto in 1962, with a master's in music composition from the University of Toronto. She scores film and writes for theatre, chamber and orchestral ensembles, and conducts. "
     "Best known for Manchester by the Sea, Late Night and You Can Count on Me, and for the animated series Little Bear.",
     [("Official site", "https://lesleybarber.com"), ("Wikipedia", "https://en.wikipedia.org/wiki/Lesley_Barber")]),
]

GUILD = [
    ("Screen Composers Guild of Canada (SCGC)", "National association of composers and music producers",
     "A national association of professional composers and music producers for film, television and media. It is certified under the federal Status of the Artist Act to represent composers in Canada working on English-language productions. "
     "It began in 1980 as the Guild of Canadian Film Composers, founded by composer and jingle producer Ben McPeek.",
     "https://screencomposers.ca/about-scgc/"),
]


def render(leaf, favicon, updated):
    cards = ""
    for name, provs, what, links in COMPOSERS:
        badges = " ".join(provinces.badge(p) for p in provs)
        lk = " · ".join('<a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a>' for t, u in links)
        cards += ('<article class="box"><div>' + badges + '</div><h3>' + e(name) + '</h3><p>' + e(what) + '</p><p class="note">' + lk + '</p></article>')
    guild = "".join('<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a></h3><p class="note">' + e(w) + '</p><p>' + e(x) + '</p></article>'
                    for t, w, x, u in GUILD)
    body = ('<p>' + e(WHAT) + '</p><p class="note">Facts were read on ' + e(AS_OF) + ' from the linked pages. Wikipedia is used for summaries; awards come from the composers\' own sites or the awards bodies where we could reach them. '
            'Every name links out. This is a short list, not the full list: send us a Canadian composer to add.</p>'
            '<h2>Canadian screen composers</h2>' + cards
            + '<h2>The guild</h2>' + guild
            + '<h2>Send us a composer</h2><p>Email <a href="mailto:hello@postproductioncanada.ca?subject=Composer">hello@postproductioncanada.ca</a> with a link and we will check it before it goes up.</p>')
    return topics._page(leaf, favicon, updated, "Canadian Screen Composers",
                        "Well-known Canadian film and television composers and what they do, with links.",
                        "🎼 Composers", "The Canadians who write the music for the screen.", body)
