"""Awards that honour Editors, VFX, sound and music supervision. Every winner is from a linked public source.
IMDb links are included only where the IMDb page was found and checked against the credit. Others say so."""
import html
import graphics, topics

e = html.escape


def imdb(nm):
    return "https://www.imdb.com/name/" + nm + "/"


# (name, nm or None)
P = {
    "Simone Smith": "nm5250826", "Nicole Bazuin": "nm2760209", "Ed Douglas": "nm0235036", "Dermain Finlayson": "nm3569344",
    "Dev Singh": "nm0998030", "Sandy Pereira": "nm1484806", "Yvann Thibaudeau": "nm0002502", "Dorian Rigal-Ansous": "nm0726513",
    "Eui Yong Zong": "nm6510738", "Martin Edralin": "nm3520753", "Meagan Oravec": "nm2746006", "Pauline Decroix": "nm1936809",
    "Aaron Marshall": "nm0550719", "Julia Blua": "nm1193876", "Jane Tattersall": "nm0002938",
}

SHOWS = [
    ("Canadian Cinema Editors Awards", "CCE", "https://cceditors.ca/2026-awards",
     "Canada's Editors honour their own. The 16th edition in 2026 presented 17 awards, including a Lifetime Achievement Award and a Career Achievement Award."),
    ("Canadian Screen Awards", "Academy of Canadian Cinema & Television", "https://www.academy.ca/wp-content/uploads/2025/09/2026-Canadian-Screen-Awards-Film-Rules-Regulations.pdf",
     "Best Editing has been presented since 1966, first under the Canadian Film Awards. There is a separate documentary editing category, plus sound editing and visual effects. Nominees in editing are chosen by the Academy's Cinema Editors branch. The rules say Post Production Supervisor is not an eligible credit for sound mixing or sound editing."),
    ("DGC Awards", "Directors Guild of Canada", "https://www.newswire.ca/news-releases/winners-announced-for-25th-annual-dgc-awards-897936645.html",
     "The guild's awards, including picture editing and sound editing categories for film and TV. The 25th edition was presented November 14, 2026 at the Chan Centre for the Performing Arts in Vancouver. The 24th was held November 8, 2025 at Koerner Hall in Toronto."),
    ("Canadian Sync Awards", "Guild of Music Supervisors, Canada", "https://www.guildofmusicsupervisors.ca/news/2026/6/12/congrats-to-the-2026-canadian-sync-awards-winners",
     "Honours music supervision in Canadian film, TV and media. The 2026 awards took place June 11 in Toronto."),
    ("Eddie Awards", "American Cinema Editors", "https://www.americancinemaeditors.org/", "The American Cinema Editors' awards for editing. International."),
    ("Academy Awards: Film Editing", "Academy of Motion Picture Arts and Sciences", "https://www.oscars.org/", "The Oscar for Best Film Editing. International."),
    ("VES Awards", "Visual Effects Society", "https://www.vesglobal.org/", "International awards for visual effects."),
]


def person(n):
    nm = P.get(n)
    if nm:
        return '<a href="' + e(imdb(nm)) + '" target="_blank" rel="noopener">' + e(n) + '</a> <span class="ib">IMDb</span>'
    return e(n) + ' <span class="when">(IMDb link not confirmed)</span>'


def people(names):
    return ", ".join(person(n) for n in names)


# (award, who list, work, extra)
WIN = {
    "Canadian Cinema Editors Awards 2026": [
        ("Best Editing in Feature Film", ["Yvann Thibaudeau", "Dorian Rigal-Ansous"], "Ma mère, Dieu et Sylvie Vartan (Once Upon My Mother)"),
        ("Best Editing in Documentary Feature", ["Eui Yong Zong"], "There Are No Words"),
        ("Best Editing in Documentary Short Form", ["Brendan Mills", "Martin Edralin"], "La Mayordomía"),
        ("Best Editing in Docu-series / Docu-drama", ["Amy Mielke"], "Absolutely Canadian: Apex: The Black Masters"),
        ("Best Editing in Lifestyle", ["Meagan Oravec"], "Queen of the Castle, EP 107"),
        ("Lifetime Achievement Award", ["Annie Jean"], "CCE"),
        ("Career Achievement Award", ["Didier Kennel"], "A freelance picture editor since 1985 who has taught visual post production at Sheridan College for 26 years, per the CCE."),
    ],
    "Canadian Screen Awards 2026 (film)": [
        ("Achievement in Editing", ["Simone Smith"], "Mile End Kicks"),
        ("Best Editing in a Feature Length Documentary", ["Nicole Bazuin"], "Modern Whore"),
        ("Achievement in Sound Editing", ["Ed Douglas", "Dermain Finlayson"], "40 Acres"),
        ("Achievement in Visual Effects", ["Tristan Zerafa", "Lou Gatti", "Mike Stadnyckyj", "Graham Houston", "James Soares", "Christopher Shewchuk", "Jeniree Bastidas", "Onur Can Yol", "Luca Tarantini"],
         "Nirvanna the Band the Show the Movie. A team of ten; we list nine names that match across sources, because one team member's first name is printed two ways. Credits on the IMDb event page below."),
    ],
    "DGC Awards 2026": [
        ("Best Picture Editing, Feature Film", ["Simone Smith"], "Mile End Kicks"),
        ("Best Picture Editing, Documentary", ["Eamonn O'Connor", "Omar Majeed"], "Lilith Fair: Building a Mystery, with Navin Harrilal and Peter Mishara"),
        ("Best Picture Editing, Dramatic Series", ["Ana Yavari"], "The Testaments, “Marat Sade”"),
        ("Best Picture Editing, Comedy or Family Series", ["Geoff Ashenhurst"], "Murderbot, “Escape Velocity Protocol”"),
        ("Best Picture Editing, Movies for TV and Mini-Series", ["Lara Johnston"], "The Twisted Tale of Amanda Knox, “Ci vediamo più tardi”"),
        ("Best Sound Editing, Feature Film", ["Nathan Robitaille"], "Frankenstein, with Nelson Ferreira, Danielle McBride, Jill Purdy, David McCallum, Stephen Barden, Dustin Harris, Craig MacLellan, Paul Germann, Dashen Naidoo, Robert Hegedus and Scott Hitchon"),
        ("Best Sound Editing, Dramatic Series", ["Tyler Whitham"], "Foundation, “A Song for the End of Everything”, with Joe Bracciale, Josh Brown, Alex Bullick, Nelson Ferreira, Gerald Trepy and Joe Mancuso"),
        ("Best Sound Editing, Movies for TV and Mini-Series", ["Jane Tattersall"], "Wayward, “Mirror”, with Martin Gwynn Jones, Brennan Mercer, Brent Pickett, Rachael Zerafa and Chris Cobain"),
        ("Best Sound Editing, Comedy or Family Series", ["Jill Purdy"], "Small Achievable Goals, “HRT, and Other Party Tricks”, with Stephen Barden, Faustine Pelipel and Chris Cobain"),
    ],
    "DGC Awards 2025": [
        ("Best Picture Editing, Feature Film", ["Dev Singh", "Sandy Pereira"], "40 Acres"),
        ("Best Picture Editing, Documentary", ["Pauline Decroix"], "The Nest"),
        ("Best Picture Editing, Dramatic Series", ["Aaron Marshall"], "The Handmaid's Tale, “Exodus”"),
        ("Best Picture Editing, Comedy or Family Series", ["Marianna Khoury", "Sam Thomson"], "North of North, “Top of the World”"),
        ("Best Picture Editing, Movies for TV and Mini-Series", ["Julia Blua", "Pete Watson"], "Terror Comes Knocking: The Marcela Borges Story"),
        ("Best Sound Editing, Feature Film", ["Ed Douglas", "Dermain Finlayson"], "40 Acres"),
        ("Best Sound Editing, Dramatic Series", ["Jane Tattersall"], "The Handmaid's Tale, “Execution”, with Brennan Mercer, David McCallum, Krystin Hunter, Dustin Harris, David Caporale, Nadya Hanlon, Abby Austria and Yuri Gorbachow"),
    ],
}


def table(rows):
    out = ""
    for award, who, work in rows:
        out += ('<div class="u"><b>' + e(award) + '</b><div>' + people(who) + ' · <i>' + e(work) + '</i></div></div>')
    return '<div class="box">' + out + '</div>'


def render(leaf, favicon, updated):
    css = "<style>" + graphics.CSS + ".ib{font-size:11px;border:1px solid var(--line);border-radius:6px;padding:0 5px;color:var(--mute)}.u{padding:10px 0;border-bottom:1px solid var(--line)}.u:last-child{border-bottom:0}.u div{color:var(--mute);font-size:14.5px;margin-top:2px}</style>"
    shows = "".join('<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(n) + '</a></h3><div class="when">' + e(o) + '</div><p>' + e(t) + '</p></article>' for n, o, u, t in SHOWS)
    wins = "".join('<h2>' + e(k) + '</h2>' + table(v) for k, v in WIN.items())
    body = (css + graphics.banner("THE CUT IS WHERE THE STORY IS MADE", "Editors are artists. These are the awards that say so.") + graphics.craft_cards()
            + '<h2>The awards that honour the craft</h2>' + shows
            + '<p class="note">We found no awards show that honours post supervisors specifically. If you know of one, send it and we will check it.</p>'
            + '<h2>Recent Canadian winners</h2><p class="note">Names are from the linked winner lists. A person’s IMDb link is shown only when we found the page and matched it to the credit. Otherwise it says so.</p>' + wins
            + '<p class="note">Sources: <a href="https://cceditors.ca/2026-awards" target="_blank" rel="noopener">CCE 2026 Awards</a>, <a href="https://deadline.com/2026/06/heated-rivalry-tops-canadian-screen-awards-1236931778" target="_blank" rel="noopener">Deadline, Canadian Screen Awards winners</a>, <a href="https://www.imdb.com/event/ev0001872/2026/1" target="_blank" rel="noopener">IMDb: Canadian Screen Awards 2026</a>, <a href="https://www.newswire.ca/news-releases/winners-announced-for-25th-annual-dgc-awards-897936645.html" target="_blank" rel="noopener">DGC Awards 2026 winners</a>, <a href="https://finance.yahoo.com/news/winners-announced-24th-annual-dgc-171800007.html" target="_blank" rel="noopener">DGC Awards 2025 winners</a>.</p>')
    return topics._page(leaf, favicon, updated, "Awards honouring Editors",
                        "Awards that honour Canadian Editors, sound Editors, VFX artists and music supervisors, with the winners and their IMDb pages.",
                        "🏆 Awards honouring Editors",
                        "The awards that celebrate the people who shape the story in post, and the recent Canadian winners.", body)
