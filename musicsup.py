"""Music Supervisors in Canada. Facts read from the Guild of Music Supervisors, Canada's own site, CBC and Billboard Canada on AS_OF."""
import html
import topics

e = html.escape
AS_OF = "November 20, 2026"
GMSC = "https://guildofmusicsupervisors.ca"

WHAT = ("A music supervisor oversees the music side of a film, series, ad or game: finding and licensing songs, "
        "working with composers and artists, and handling clearances and budgets from development through post. "
        "That is the Guild's own definition of the job, paraphrased. For an Editor it matters because the song that lands "
        "in the cut has to be found, cleared and paid for by someone, and that someone is often the supervisor.")

# (title, who/when, text, url)
GUILD = [
    ("Guild of Music Supervisors, Canada (GMSC)", "Non-profit, Canadian chapter of the Guild of Music Supervisors",
     "A non-profit that promotes the craft of music supervision in film, television, games, advertising, trailers and emerging media. "
     "It is part of a worldwide community of music supervisor guilds in the United States and the UK and Europe. "
     "It offers Accredited, Associate and Friends of the Guild memberships; check its Memberships page for the rules and fees.",
     GMSC),
    ("How the Canadian chapter began", "Announced June 13, 2017, Toronto",
     "The Guild of Music Supervisors announced its Canadian chapter in Toronto on June 13, 2017. Michael A. Perlmutter, owner of "
     "Instinct Entertainment, was appointed its first President. In a note posted in February 2025, he said he was stepping down as President as of "
     "February 14, 2025, after leading the Guild since it began in 2016, and that membership had reached 33 accredited members.",
     "https://www.guildofmusicsupervisors.com/single-post/2017/06/14/THE-GUILD-OF-MUSIC-SUPERVISORS-LAUNCHES-A-CANADIAN-CHAPTER"),
    ("Today's board", "From the Guild's site on " + AS_OF,
     "The Guild's site lists Heather Gardner as President, with Andrea Higgins and Cody Partridge as Vice Presidents. "
     "It also lists its accredited members, and carries an \"in memory of David Hayman\" line.",
     GMSC),
]

EVENTS = [
    ("Canadian Sync Awards", "2026 awards held June 11, 2026, Toronto (NXNE)",
     "The Guild's yearly awards for music supervision in Canadian film, television, advertising and sports. The 2026 winners include Cody Partridge for Shoresy (Season 5), "
     "Scotty Taylor for Heated Rivalry (Season 1), and Mikaila Simmons for the feature Forbidden Fruits. Serena Ryder received the Impact Award. "
     "The 2027 date was not posted when this page was built.",
     GMSC + "/news/2026/6/12/congrats-to-the-2026-canadian-sync-awards-winners"),
    ("Sound + Vision", "Sync conference, June 10, 2026, The W Hotel, Toronto",
     "The Guild's education day for the sync sector, held in person for the first time in 2026, the day before the awards.",
     "https://ca.billboard.com/music/awards/canadian-sync-awards-2026-nominees"),
    ("Music in Motion: Sync Summit", "East Coast Music Association, May 2026",
     "Sessions that bring artists together with music supervisors, with a networking mixer. Check the ECMA site for what comes next.",
     "https://www.ecma.com/music-in-motion-2026/"),
]

READING = [
    ("The art of the needle drop: how TV shows and films find the perfect song", "CBC Music, Nov 6, 2023",
     "How supervisors such as Canada's Kaya Pino (Sort Of) and Cody Partridge (Letterkenny, BlackBerry) find and clear songs, "
     "including a clearance that took seven months to hear back.",
     "https://www.cbc.ca/lite/story/1.7016159"),
    ("The 2026 Canadian Sync Awards celebrate the best of music in TV, film and advertising", "Billboard Canada, May 13, 2026",
     "Partner content about the 2026 awards and the first in-person Sound + Vision conference.",
     "https://ca.billboard.com/music/awards/canadian-sync-awards-2026-nominees"),
]

RIGHTS = [
    ("Canada's Copyright Act: how long it lasts", "Changed December 30, 2022",
     "The general term of copyright in Canada went from the author's life plus 50 years to life plus 70 years on December 30, 2022. "
     "The change does not bring back works that were already in the public domain. Moral rights last as long as the copyright and stay with the author: they can be waived but not assigned. "
     "The Act's basic rule is that the author is the first owner of the copyright, subject to the rest of the Act. How commissioned or employee work is treated needs a lawyer or the Act itself.",
     "https://uwaterloo.ca/copyright-at-waterloo/news/copyright-term-changes-life-plus-70-years"),
    ("Music licensing in Canada: who licenses what", "DLA Piper, 2024",
     "A law-firm guide to the Canadian music licensing landscape. In general terms, SOCAN licenses the public performance of musical works, CMRRA licenses reproduction (mechanical) rights, "
     "and Re:Sound collects neighbouring-rights royalties for performers and the makers of sound recordings. A song in a cut can involve more than one of them, plus a direct sync licence from the publisher and the label.",
     "https://www.dlapiper.com/en/insights/publications/2024/01/music-licensing-in-canada"),
    ("CMRRA: what is music copyright?", "CMRRA, Canadian Musical Reproduction Rights Agency",
     "CMRRA's own explainer. It licenses and collects mechanical royalties for most songs recorded, sold and broadcast in Canada.",
     "https://cmrra.ca/?p=14"),
    ("SOCAN reported to have bought CMRRA", "Complete Music Update, July 30, 2026 (one report, not confirmed elsewhere)",
     "One trade report says SOCAN has bought CMRRA from SoundExchange, which would put performing and mechanical licensing under one Canadian organisation. "
     "We have not confirmed it with SOCAN or CMRRA, so check their sites before relying on it.",
     "https://completemusicupdate.com/canadas-socan-buys-cmrra-from-soundexchange-meaning-canadian-performing-and-mechanical-rights-will-now-be-licensed-through-one-organisation/"),
]

RELATED = ("A different group: the Screen Composers Guild of Canada represents composers and music producers for film and television, "
           "not music supervisors. Its site is screencomposers.ca.")


def _cards(rows):
    return "".join('<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a></h3>'
                   '<p class="note">' + e(w) + '</p><p>' + e(x) + '</p></article>' for t, w, x, u in rows)


def render(leaf, favicon, updated):
    body = ('<p>' + e(WHAT) + '</p><p class="note">Facts on this page were read on ' + e(AS_OF) + ' from the Guild\'s own site, CBC and Billboard Canada. '
            'Canadian only. If something is out of date or missing, send it to us.</p>'
            '<h2>The Canadian guild</h2>' + _cards(GUILD)
            + '<h2>Awards and events</h2>' + _cards(EVENTS)
            + '<h2>©️ Rights, copyright and ownership</h2><p class="note">General information from the sources linked, not legal advice. For a real clearance or ownership question, ask an entertainment lawyer.</p>' + _cards(RIGHTS)
            + '<h2>Reading</h2>' + _cards(READING)
            + '<p class="note">' + e(RELATED) + '</p>'
            '<h2>Send us a Canadian music supervisor story</h2><p>Know of an article, interview or event we missed? Email '
            '<a href="mailto:hello@postproductioncanada.ca?subject=Music%20supervision">hello@postproductioncanada.ca</a> with a link to the original and we will check it first.</p>')
    return topics._page(leaf, favicon, updated, "Music Supervisors in Canada",
                        "Canada's music supervisors: the Guild of Music Supervisors, Canada, the Canadian Sync Awards, events and reading.",
                        "🎸 Music Supervisors in Canada", "The people who find, clear and place the songs in your cut.", body)
