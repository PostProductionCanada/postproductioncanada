"""Cinematographers: Canadian DPs, the CSC, and the DP/editor partnership. Facts read from the linked pages on AS_OF."""
import html
import topics, provinces

e = html.escape
AS_OF = "November 20, 2026"

WHAT = ("The cinematographer, also called the director of photography or DP, photographs the film and runs the camera and lighting teams. "
        "The Editor then shapes those images into the story. The two never work in the same room at the same time, but each depends on the other, "
        "and the best results come when they talk early.")

PEOPLE = [
    ("Paul Sarossy", ["ON"],
     "Born in Barrie, Ontario, and a York University graduate. He is credited CSC, BSC and ASC. He has shot fourteen features for director Atom Egoyan, among them Exotica, The Sweet Hereafter, Felicia's Journey and Ararat, "
     "and has won five Genie Awards for Best Achievement in Cinematography.",
     [("Official site", "http://paulsarossy.com/"), ("Wikipedia", "https://en.wikipedia.org/wiki/Paul_Sarossy")]),
    ("Guy Dufaux", ["QC"],
     "Born in Lille, France, in 1943. He immigrated to Canada in 1965 and became a Canadian citizen in 1971. Most of his work has been in Canadian cinema. "
     "Recognition includes a Genie nomination for Stardom and the Canadian Society of Cinematographers' Kodak New Century Award in 2002.",
     [("Wikipedia", "https://en.wikipedia.org/wiki/Guy_Dufaux")]),
    ("Nicolas Bolduc", ["QC"],
     "Born in Montréal in 1973. He won the Canadian Screen Award for Best Cinematography two years in a row, for War Witch (2012) and Enemy (2013), "
     "and won again for Hochelaga, Land of Souls at the 6th Canadian Screen Awards. He also won a Jutra Award for War Witch.",
     [("Wikipedia", "https://en.wikipedia.org/wiki/Nicolas_Bolduc")]),
    ("André Turpin", ["QC"],
     "A Québec cinematographer, director and screenwriter, born in 1966. As a cinematographer he has won over a dozen awards, including Canadian Screen Awards for Best Cinematography for his work on Xavier Dolan's films Mommy and It's Only the End of the World.",
     [("Wikipedia", "https://en.wikipedia.org/wiki/Andr%C3%A9_Turpin")]),
]

SOCIETY = [
    ("Canadian Society of Cinematographers (CSC)", "Toronto, founded 1957",
     "A not-for-profit organization dedicated to fostering cinematography in Canada since 1957. Its site lists a member directory, workshops, mentorship, a library of talks and podcasts, and its yearly CSC Awards. "
     "Wikipedia reports more than 800 members, and members use the letters CSC after their names.",
     "https://www.csc.ca"),
]

READING = [
    ("Effective pre-production collaboration between the cinematographer and editor", "PremiumBeat",
     "Argues that the DP and Editor work in different phases of a project, so collaborating early gives a better final film. A short guide to what each role does and how to plan the shots together.",
     "https://www.premiumbeat.com/blog/effective-pre-production-collaboration-between-the-cinematographer-and-editor/"),
    ("Dailies best practices", "Netflix Backlot",
     "Netflix's guide to dailies recommends workflow meetings that include cinematographers and editors, because the colour plan decides whether the dailies operator applies CDLs or LUTs.",
     "https://backlothelp.netflix.com/hc/en-us/articles/4415931246995-Dailies-Best-Practices"),
]


def _cards(rows):
    return "".join('<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a></h3>'
                   '<p class="note">' + e(w) + '</p><p>' + e(x) + '</p></article>' for t, w, x, u in rows)


def render(leaf, favicon, updated):
    cards = ""
    for name, provs, what, links in PEOPLE:
        badges = " ".join(provinces.badge(p) for p in provs)
        lk = " · ".join('<a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a>' for t, u in links)
        cards += '<article class="box"><div>' + badges + '</div><h3>' + e(name) + '</h3><p>' + e(what) + '</p><p class="note">' + lk + '</p></article>'
    body = ('<p>' + e(WHAT) + '</p><p class="note">Facts were read on ' + e(AS_OF) + ' from the linked pages. This is a short list, not the full list: send us a Canadian cinematographer to add.</p>'
            '<h2>Canadian cinematographers</h2>' + cards
            + '<h2>The society</h2>' + _cards(SOCIETY)
            + '<h2>DPs and Editors</h2><p>The image and the cut tell the story together. These guides are about getting the two crafts talking before the shoot, not after.</p>' + _cards(READING)
            + '<h2>Send us a cinematographer</h2><p>Email <a href="mailto:hello@postproductioncanada.ca?subject=Cinematographer">hello@postproductioncanada.ca</a> with a link and we will check it before it goes up.</p>')
    return topics._page(leaf, favicon, updated, "Canadian Cinematographers",
                        "Well-known Canadian cinematographers, the Canadian Society of Cinematographers, and how DPs and Editors work together.",
                        "📷 Cinematographers", "The Canadians who photograph the screen.", body)
