"""Networking page: gatherings, screenings, trade shows and open houses for Canadian post production.

Every entry links to the organizer's own page. Dates were read from those pages on AS_OF.
Hand-maintained: edit EVENTS / RECURRING / WATCH below, then rebuild.
"""
import html
import topics, provinces

e = html.escape
AS_OF = "November 19, 2026"
CONTACT = "hello@postproductioncanada.ca"

# Featured: the event where the industry meets policymakers. Facts from the CMPA's Prime Time page and its November 2026 email.
FEATURED = {
    "title": "Prime Time 2027",
    "when": "January 27 to 29, 2027 · Ottawa",
    "who": "Canadian Media Producers Association (CMPA)",
    "url": "https://cmpa.ca/prime-time/",
    "text": ("The CMPA calls it Canada's leading screen industry conference: three days where 1,200+ producers, broadcasters, streamers, distributors, funders and policymakers connect, do deals and shape the future of content. "
             "It is held in Ottawa, where the policy that decides tax credits, Canadian content rules and funding gets made, so it is the room where the industry and government meet."),
    "points": [
        "Feature conversation: Bell Media President Sean Cohan and VP Global Content Justin Stockman on Canadian content, cultural sovereignty, and the role of streamers and broadcasters.",
        "The Bell Media Delegate Lounge is open all three days as a home base for meetings and breaks.",
        "Hotel: rooms at The Westin are sold out, but several nearby hotels still had Prime Time rates in the CMPA's latest email. Delegates also get reduced airfare and train rates.",
        "Breakfast, lunch, coffee breaks and evening receptions are included with the pass.",
    ],
}

# (date text, title, where, who, url, note)
EVENTS = [
    ("Application deadline Nov 23, 2026; market March 23 to 25, 2027", "Series Mania 2027: Canada and Quebec are the Guests of Honour",
     "Lille, France", "Series Mania, with Telefilm Canada and SODEC",
     "https://sodec.gouv.qc.ca/presence-internationale/series-mania/en",
     "The Directors Guild of Canada announced that Canada and Quebec were selected as the 2027 Guests of Honour, with Telefilm and SODEC representatives in Lille to build partnerships. DGC National's newsletter lists the Series Mania Market Accelerator application with a deadline of Monday, November 23, 2026, and market dates of March 23 to 25, 2027. Apply through the form below. The 2026 festival ran March 20 to 27."),
    ("Register by Dec 4, 2026; market Feb 10 to 16, 2027", "Canada Pavilion at the European Film Market (EFM)",
     "Berlin, Germany", "Telefilm Canada",
     "https://telefilm.ca/en",
     "Telefilm Canada's call for entry lists the Canada Pavilion at the EFM, with a deadline to register through Telefilm of December 4, 2026."),
    ("Register by Jan 17, 2027; market May 16 to 19, 2027", "Cannes 2027: the Short Film Corner",
     "Cannes, France", "Telefilm Canada",
     "https://telefilm.ca/en",
     "Telefilm Canada's call for entry for Canadian short films, all genres, with a deadline to register through Telefilm of January 17, 2027."),
    ("Nov 26, 2026, 7 p.m. AT", "NSCAD Public Lecture: Production Designer Tamara Deverell",
     "Paul O'Regan Hall, Halifax Central Library · free, no registration", "NSCAD University, with DGC Maritimes",
     "https://nscad.ca/pls/",
     "A free public lecture by Production Designer Tamara Deverell of Cape Breton, who worked on Guillermo del Toro's Frankenstein. The details come from the DGC Maritimes newsletter of November 20, 2026; we could not yet find the listing on NSCAD's own page, so confirm before you go."),
    ("Dec 17, 2026", "NDD Market Accelerator seminar: how to bring your series to the international market",
     "Online", "DGC National",
     "https://www.dgc.ca",
     "A seminar listed in DGC National's newsletter. Register through the DGC's email or website."),
    ("Jan 20, 2027", "NDD Market Accelerator seminar: how to bring your feature to the international market",
     "Online", "DGC National",
     "https://www.dgc.ca",
     "The companion seminar for features, listed in DGC National's newsletter. Register through the DGC's email or website."),
    ("Nov 20, 2026, 9 a.m. ET (14:00 GMT)", "DaVinci Resolve online seminar: Workflows from Camera to Delivery",
     "Online, free", "Blackmagic Design",
     "https://www.blackmagicdesign.com/event/davinci-resolve-online-seminars",
     "One of six free 90-minute seminars. Next: Nov 27 (AI tools), then Jan 29, Feb 19 and Feb 26, 2027 (Fairlight)."),
    ("Nov 24, 2026, 1 p.m. ET", "Free Demo Reel Masterclass with Allan McKay",
     "Online, free", "ActionVFX",
     "https://www.actionvfx.com",
     "A live webinar where VFX artists can submit a demo reel for live feedback from Allan McKay. Details come from ActionVFX's email to subscribers; we could not find a public listing, so register through ActionVFX. A related free two-hour talk, The New VFX Career Playbook, is meant to be watched before you submit."),
    ("Dec 1, 2026, 7 p.m. ET", "'Tis the Season to Make a MOW",
     "Online (Zoom)", "Canadian Cinema Editors",
     "https://cceditors.ca/events",
     "Editors Daria Ellerman, Saeed Vahidi and Arlein Wharf-Garcia on cutting holiday movies, often in midsummer."),
    ("Dec 2, 2026, 7 p.m.", "Edmonton Holiday Social", "RED STAR, 10534 Jasper Ave, Edmonton",
     "Canadian Cinema Editors", "https://cceditors.ca/events", "Non-members welcome. Members get a first drink free; RSVP so you're on the list."),
    ("Dec 3, 2026, 2 p.m. ET", "Telefilm Canada Annual Public Assembly",
     "Online, streamed on Telefilm Canada's YouTube channel", "Telefilm Canada",
     "https://broadcastdialogue.com/canadian-production-hits-10-17b-driven-by-foreign-services-telefilm-report/",
     "Broadcast Dialogue reports that CEO Julie Roy and Board Chair Sylvain Lafrance will answer industry questions and outline priorities for the coming fiscal year. The link goes to that report, which has the details; we have not yet found the listing on Telefilm's own site."),
    ("Dec 3, 2026", "Toronto Holiday Social", "Paupers Pub, 539 Bloor St W, Toronto",
     "Canadian Cinema Editors", "https://cceditors.ca/events", "Non-members welcome. RSVP on the CCE page."),
    ("Dec 3, 2026", "Ottawa Holiday Social", "National Gallery of Canada, then Pubwells",
     "Canadian Cinema Editors", "https://cceditors.ca/events", "Non-members welcome. RSVP on the CCE page."),
    ("Dec 4, 2026", "Calgary Holiday Social", "Veranda at the Stables, 200-2566 Flanders Ave",
     "Canadian Cinema Editors", "https://cceditors.ca/events", "Non-members welcome. RSVP on the CCE page."),
    ("Dec 6, 2026", "Halifax Holiday Social", "Antojo Tacos, 1667 Argyle St, Halifax",
     "Canadian Cinema Editors", "https://cceditors.ca/events", "Non-members welcome. RSVP on the CCE page."),
    ("2027, early in the year (dates not confirmed)", "EditCon 2027, the 10th annual",
     "Online, plus in-person events in several cities", "Canadian Cinema Editors",
     "https://cceditors.ca/sponsorship",
     "A conference on the art of picture editing. The 2026 edition ran Feb 6 to 8 in Toronto, Montreal, Vancouver, Edmonton, Halifax and Winnipeg. Check the CCE site for 2027 dates."),
]

# Extra action links on an event, keyed by its title: (label, url)
EXTRA = {"Series Mania 2027: Canada and Quebec are the Guests of Honour": ("Apply to join the delegation (form)", "https://tally.so/r/WJO6pv")}

# Festivals and markets across Canada: (province, name, city, dates, url). Dates from Playback's industry calendar.
FESTIVALS = [
    ("QC", "RIDM, Montreal International Documentary Festival", "Montréal", "Nov 19 to 29, 2026", "https://ridm.ca/en"),
    ("BC", "Whistler Film Festival", "Whistler", "Dec 2 to 6, 2026", "https://www.whistlerfilmfestival.com/"),
    ("ON", "Prime Time (Canadian Media Producers Association)", "Ottawa", "Jan 27 to 29, 2027", "https://cmpa.ca/prime-time/"),
    ("BC", "Victoria Film Festival", "Victoria", "Feb 5 to Mar 14, 2027", "https://film-fest-report.com/2027-film-festival-dates"),
    ("YT", "Available Light Film Festival", "Whitehorse", "Feb 11 to 27, 2027", "https://film-fest-report.com/2027-film-festival-dates"),
    ("ON", "Kingston Canadian Film Festival", "Kingston", "Feb 24 to 28, 2027", "https://filmfreeway.com/KingstonCanadianFilmFestival"),
    ("QC", "Regard, Saguenay International Short Film Festival", "Saguenay", "Mar 17 to 21, 2027", "https://festivalregard.com/en/call-for-entries"),
    ("YT", "Dawson City International Short Film Festival", "Dawson City", "Mar 25 to 28, 2027", "https://www.dawsonfilmfest.com/submit.html"),
    ("ON", "Canadian Film Fest", "Toronto", "Mar 30 to Apr 4, 2027", "https://www.canfilmfest.ca"),
    ("ON", "Hot Docs Festival", "Toronto", "Apr 23 to May 2, 2027", "https://hotdocs.ca/festivals/hot-docs-festival"),
    ("BC", "DOXA Documentary Film Festival", "Vancouver", "Apr 29 to May 9, 2027", "https://www.doxafestival.ca/"),
    ("QC", "Canadian Independent Film Festival", "Montréal", "May 21 to 23, 2027", "https://festhome.com/en/festival/canadian-independent-film-festival-ciff"),
    ("AB", "Banff World Media Festival", "Banff", "June 13 to 16, 2027 (Playback lists to June 17)", "https://banffmediafestival.playbackonline.ca/"),
    ("QC", "Fantasia International Film Festival", "Montréal", "July 15 to Aug 1, 2027", "https://fantasiafestival.com/en/"),
    ("MB", "Gimli International Film Festival", "Gimli", "July 21 to 25, 2027", "https://www.gimlifilm.com"),
    ("NS", "Atlantic International Film Festival", "Halifax", "Sept 15 to 22, 2027", "https://atlanticfilmfestival.ca/"),
    ("ON", "Cinéfest Sudbury International Film Festival", "Sudbury", "Sept 18 to 26, 2027", "https://cinefest.com/"),
    ("ON", "Forest City Film Festival", "London", "Oct 15 to 24, 2027", "https://fcff.ca"),
]
# Annual festivals that just ran, with next dates not posted yet when this page was built.
WRAPPED = [
    ("ON", "Toronto International Film Festival (TIFF)", "Toronto", "2026 ran Sept 10 to 20; 2027 dates not found", "https://tiff.net"),
    ("BC", "Vancouver International Film Festival (VIFF)", "Vancouver", "2026 ran Oct 1 to 11; 2027 dates not posted", "https://viff.org/festival/viff-2026"),
    ("SK", "Regina International Film Festival and Awards (RIFFA)", "Regina", "2026 ran Aug 12 to 22; 2027 dates not posted", "https://riffa.ca"),
    ("NB", "Silver Wave Film Festival", "Fredericton", "2026 ran Nov 5 to 12; 2027 dates not posted", "https://www.nbfilmcoop.com/silver-wave-film-festival"),
    ("NL", "St. John's International Women's Film Festival", "St. John's", "2026 ran Oct 20 to 24; 2027 dates not posted", "https://destinationfilmguide.com/top-north-american-film-festivals-2026-27"),
]
NO_FESTIVAL_YET = "Dates not found yet for the Charlottetown Film Festival (PEI), the Yellowknife International Film Festival (NWT), the Calgary International Film Festival (AB) or any festival in Nunavut. Send a festival with a link to the organizer's page and it goes on."

# Recurring, with no 2027 dates announced yet.
RECURRING = [
    ("ProFusion Expo", "Toronto, every November",
     "Canada's big photo, video and cinema show: free with registration, hands-on camera, audio and post tech, and talks. The 2026 show ran Nov 11 and 12 at the Metro Toronto Convention Centre. 2027 dates were not posted when this page was built.",
     "https://profusionexpo.com"),
    ("CCE Master Series, Behind the Screen and Offline", "Online and in person, through the year",
     "The Canadian Cinema Editors' talk series with Canadian and international Editors, plus the free Offline meetups held in cities across Canada (the 2026 round ran June 15 to 20).",
     "https://cceditors.ca/events"),
    ("Film London industry mixers", "London, Ontario, through the year",
     "The London Economic Development Corporation hosts evenings for the local film and television community. The Spring 2026 mixer ran May 29, 2026, from 6 to 10 p.m., and kicked off the Forest City 48. To attend, email the contact on the event page with a short description of what you do in London's film and TV industry. No later dates were posted when this page was built.",
     "https://www.ledc.com/event/film-industry-mixer-spring-2026"),
    ("Ontario Screen Creators Conference (OSCC)", "London, Ontario, usually in the fall",
     "A three-day conference in downtown London with workshops, panels, daily networking markets and pitch prizes of over $75,000. Past speakers include Aaron L. Gilbert, David Shore, Andrew Barnsley and Tamara Deverell. A listing reported the 2025 edition as October 23 to 25, 2025. We have not found 2026 or 2027 dates, so check the organizer's page.",
     "https://www.ledc.com/event/ontario-screen-creators-conference-1"),
    ("VES Montreal (Visual Effects Society section)", "Montréal, monthly events through the year",
     "An all-volunteer, bilingual section that runs free screenings, pub nights, technical talks, industry mixers and seasonal parties, with partners including the Cinémathèque québécoise, the National Film Board of Canada and Concordia University. Recent talks include Rodeo FX's Peter Nofz on AI for artists, with a fall session on agentic AI. The year ends with its Xmas Mega Party at the Théâtre Plaza. VFX Voice, which profiled the section in October 2026, calls Montréal one of the world's busiest visual effects communities, and says the local industry's peak came before the 2023 strikes and was followed by a challenging period shaped in part by changes to Québec's tax incentives.",
     "https://vfxvoice.com/ves-montreal-connects-a-world-class-vfx-community/"),
    ("Vancouver Post Alliance", "Vancouver, ongoing",
     "A BC post-production community group that runs and shares events, and promotes Women in Post, a Canadian Academy mentorship program for emerging and mid-level women-identifying and non-binary post professionals.",
     "https://vancouverpostalliance.com"),
    ("TIFF week", "Toronto, every September",
     "Toronto's big film festival, and a fixture on the calendar for Canada's screen community. Check the festival's site for dates.",
     "https://www.tiff.net"),
]

WATCH = [
    "Post houses and tech companies inviting people to an open house or demo night, including VR and virtual-production shops.",
    "Gear makers and software companies running training days or roadshows that stop in Toronto, Montreal or Vancouver.",
    "Unions and guilds holding screenings, panels or socials open to the wider post community.",
    "Schools running showcases or industry nights that welcome working post people.",
]


def render(leaf, favicon, updated):
    ev = "".join(
        '<li><b>' + e(d) + '</b> <a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a>'
        '<div class="note">' + e(w) + ' · ' + e(o) + '</div><div class="note">' + e(n) + '</div>'
        + (('<div class="note"><a class="btn" href="' + e(EXTRA[t][1]) + '" target="_blank" rel="noopener">' + e(EXTRA[t][0]) + ' →</a></div>') if t in EXTRA else '') + '</li>'
        for d, t, w, o, u, n in EVENTS)
    rec = "".join(
        '<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(n) + '</a></h3>'
        '<p class="note">' + e(w) + '</p><p>' + e(t) + '</p></article>'
        for n, w, t, u in RECURRING)
    fest = "".join('<li>' + provinces.badge(p) + ' <a href="' + e(u) + '" target="_blank" rel="noopener">' + e(nm) + '</a>'
                   '<div class="note">' + e(c) + ' · ' + e(d) + '</div></li>' for p, nm, c, d, u in FESTIVALS)
    wrapped = "".join('<li>' + provinces.badge(p) + ' <a href="' + e(u) + '" target="_blank" rel="noopener">' + e(nm) + '</a>'
                      '<div class="note">' + e(c) + ' · ' + e(d) + '</div></li>' for p, nm, c, d, u in WRAPPED)
    watch = "".join("<li>" + e(x) + "</li>" for x in WATCH)
    css = ("<style>.ev{list-style:none;padding:0;margin:0}.ev li{padding:12px 0;border-bottom:1px solid var(--line)}"
           ".ev li:last-child{border-bottom:0}.ev b{display:inline-block;margin-bottom:4px;font:700 13px ui-monospace,Menlo,monospace;color:#fff;background:#0a7cff;border-radius:6px;padding:2px 9px}.fest .note:first-of-type{color:#0a7cff;font-weight:700}@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .fest .note:first-of-type{color:#4da3ff}}:root[data-theme=dark] .fest .note:first-of-type{color:#4da3ff}"
           ".ev a{font-weight:700;text-decoration:none}.ev a:hover{text-decoration:underline}</style>")
    body = (css
            + '<p>Post is a lonely job. This page is a gathering place: screenings, socials, talks, trade shows and open houses where Canada\'s Editors, colourists, sound people, VFX artists and Post Supervisors can meet. '
              'Every entry links to the organizer\'s own page. Dates were read from those pages on ' + e(AS_OF) + ', so confirm before you travel.</p>'
            + '<div class="box feat" style="border-left:5px solid var(--red)"><div class="note"><b>⭐ FEATURED · INDUSTRY AND GOVERNMENT</b></div><h2 style="margin:4px 0"><a href="' + e(FEATURED["url"]) + '" target="_blank" rel="noopener">' + e(FEATURED["title"]) + '</a></h2>'
              '<p><b>' + e(FEATURED["when"]) + '</b> · ' + e(FEATURED["who"]) + '</p><p>' + e(FEATURED["text"]) + '</p><ul>' + "".join("<li>" + e(x) + "</li>" for x in FEATURED["points"]) + '</ul>'
              '<p><a class="btn" href="' + e(FEATURED["url"]) + '" target="_blank" rel="noopener">Register and see the program →</a></p></div>'
            + '<h2>Coming up</h2><div class="box"><ul class="ev">' + ev + '</ul></div>'
            + '<h2>🎞️ Festivals across Canada</h2><div class="box"><ul class="ev fest">' + fest + '</ul></div><p class="note">' + e(NO_FESTIVAL_YET) + '</p><h3>Just wrapped, next dates not posted</h3><div class="box"><ul class="ev fest">' + wrapped + '</ul></div>'
            + '<h2>Regular gatherings</h2>' + rec
            + '<h2>🏠 Open houses and demo nights</h2>'
              '<div class="box"><p>None are listed yet. This is where a post house, a VR or virtual-production company, or a gear maker can show off its space and meet the community.</p>'
              '<p>Running one? Email <a href="mailto:' + e(CONTACT) + '?subject=Event">' + e(CONTACT) + '</a> with the date, place, whether it is free, and a link to the sign-up page. Events open to the post community are welcome; there is no charge to be listed.</p>'
              '<p class="note">What we would like to list:</p><ul>' + watch + '</ul></div>'
            + '<h2>Send us an event</h2><p>Know of one we missed? Email <a href="mailto:' + e(CONTACT) + '?subject=Event">' + e(CONTACT) + '</a>. '
              'Please include a link to the organizer\'s own page so it can be checked.</p>')
    return topics._page(leaf, favicon, updated, "Networking",
                        "Screenings, socials, talks, trade shows and open houses for Canada's post-production community.",
                        "🤝 Networking", "Where Canada's post people gather.", body)
