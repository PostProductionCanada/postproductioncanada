"""Directory of Canadian screen funding agencies, for filmmakers and game makers.

Every entry was read on the agency's own site or on a page it publishes (Nov 2026). We describe what the
agency says it does and link to it. We do not copy deadlines or amounts that change each intake, except
where the agency page states a fixed cap. Tags: film, tv, doc, games, post, indigenous, short, tax.
"""
import html

e = html.escape

# (name, where, tags, what it is, [(link label, url), ...])
AGENCIES = [
    # ---------------- Federal and national ----------------
    ("Telefilm Canada", "Federal", "film indigenous",
     "Federal funder of Canadian feature films. Its Production Program finances features at the production or post-production stage, and it runs separate Indigenous development and production streams.",
     [("Production Program", "https://telefilm.ca/en/programmes/production-program"), ("Indigenous funding", "https://telefilm.ca/en/we-finance-and-support/indigenous-funding")]),
    ("Canada Media Fund (CMF)", "Federal", "tv doc games",
     "Funds Canadian television and digital content, and runs the main federal programs for interactive projects. Its program list covers linear production, plus interactive digital media programs.",
     [("All CMF programs", "https://cmf-fmc.ca/our-programs"), ("Program deadlines", "https://cmf-fmc.ca/our-programs/program-deadlines")]),
    ("CMF, game and interactive programs", "Federal", "games",
     "The CMF's interactive digital media streams: Conceptualization, Prototyping, Innovation & Experimentation (software applications that are innovative and leading-edge) and Commercial Projects (projects with a greater probability of commercial success), plus the CMF and Creative BC Video Games Business Development Program for B.C.-owned and controlled game companies.",
     [("Prototyping", "https://cmf-fmc.ca/program/prototyping-program"), ("Innovation & Experimentation", "https://cmf-fmc.ca/program/innovation-experimentation-program"), ("Commercial Projects", "https://cmf-fmc.ca/program/commercial-projects-program"), ("Video Games Business Development", "https://cmf-fmc.ca/program/video-games-business-development-program")]),
    ("National Film Board: Filmmaker Assistance Program", "Federal", "film doc short post",
     "Reimburses selected independent filmmakers for post-production costs. The page sets the cap at $7,500 per filmmaker for a short film and $15,000 for a feature. Filmmakers in Montreal or within 150 km of it can instead get post-production services in NFB studios, paying 10% of the cost.",
     [("FAP program page", "https://www.nfb.ca/fap")]),
    ("Canada Council for the Arts: Explore and Create", "Federal", "film short games",
     "Grants for research, development, creation, production and sharing of work, including media and digital arts, plus professional development. The program page shows film and documentary projects among its funded recipients.",
     [("Explore and Create", "https://canadacouncil.ca/funding/grants/explore-and-create")]),
    ("Indigenous Screen Office (ISO)", "National", "film tv doc indigenous",
     "Funds Indigenous screen creators and Indigenous-owned production companies, with development and production programs. Its page also points to outside funders.",
     [("ISO funding opportunities", "https://iso-bea.ca/funding-opportunities")]),
    ("Black Screen Office (BSO)", "National", "film tv",
     "Non-profit that says it exists to champion Black creators, grow Black-led businesses and make sure Black stories are made and seen. Check its site for current programs.",
     [("Black Screen Office", "https://bso-ben.ca")]),
    ("CAVCO tax credits (Canadian Heritage)", "Federal", "tax film tv post",
     "Federal tax credits: the Canadian Film or Video Production Tax Credit and the Film or Video Production Services Tax Credit. These are credits against tax, not grants, and are claimed by production companies.",
     [("Canadian Film or Video Production Tax Credit", "https://www.canada.ca/en/canadian-heritage/services/funding/cavco-tax-credits/canadian-film-video-production.html")]),
    ("Bell Fund", "National", "tv doc",
     "Supports Canadian independent producers. Its funding programs include a Production Program for Canadian series and a Slate Development program for original IP.",
     [("Funding programs", "https://bellfund.ca/funding-programs")]),
    ("TELUS STORYHIVE", "B.C. and Alberta", "short doc",
     "Funding, training and distribution for new and emerging creators in B.C. and Alberta, including short films and non-fiction series. Its homepage lists each current edition and what it pays.",
     [("STORYHIVE", "https://www.storyhive.com")]),
    ("Canadian Independent Screen Fund", "National", "film short doc",
     "A funding database aimed at independent filmmakers, listing programs by agency and showing the eligibility rules for each.",
     [("Canadian Independent Screen Fund", "https://independentfund.org/")]),

    # ---------------- Provincial and territorial ----------------
    ("Ontario Creates", "Ontario", "film tv games tax",
     "The province's agency for film and television, interactive digital media, book, magazine and music. It runs funding programs and administers Ontario's film and interactive tax credits. Applications go through its Online Application Portal.",
     [("Ontario Creates", "https://www.ontariocreates.ca/"), ("Film and TV tax credit (OFTTC)", "https://www.ontariocreates.ca/tax-incentives/ofttc")]),
    ("Ontario Creates: IP Fund, Interactive Stream", "Ontario", "games",
     "Ontario Creates funds video games and XR experiences through its IP Fund, with extra support from Global Market Development, Futures Forward and Industry Development programs. The 2026-27 guidelines list two intake deadlines a year.",
     [("Interactive sector page", "https://www.ontariocreates.ca/our-sectors/interactive"), ("Interactive digital media page", "https://www.ontariocreates.ca/investment-programs/content-creation/idm-fund")]),
    ("Creative BC", "British Columbia", "film tv games tax",
     "B.C.'s agency for motion picture, interactive digital media, music, book and magazine. It runs grants for creators and companies, the film commission and the provincial motion picture tax credits.",
     [("Funding programs", "https://creativebc.com/funding-programs"), ("Creative BC", "https://creativebc.com/")]),
    ("Creative BC: games and interactive", "British Columbia", "games",
     "The Interactive Fund (with the BC Arts Council) is for interactive digital media projects; its FAQ says conventional, primarily commercial games are not eligible this year because games have their own funds. Those are the Video Games Business Development and Video Games Early Stage Growth programs. When we read the pages, the Interactive Fund and Early Stage Growth pilot (grants up to $50,000) showed as closed.",
     [("Interactive Fund", "https://creativebc.com/funding-program/interactive-digital-media/interactive-fund"), ("Early Stage Growth", "https://creativebc.com/funding-program/interactive-digital-media/video-games-early-stage-growth")]),
    ("Alberta Media Fund", "Alberta", "film tv post tax",
     "Grants for screen-based production, including the Alberta Made Production Grant for smaller-budget productions and a Post-Production Grant. Alberta's funding page says the Post-Production Grant covers up to 18% of post cost, including visual effects and digital animation, to a maximum of $200,000 a year. Its Project Script Development Grant lists console and online video games as ineligible.",
     [("Alberta Media Fund", "https://www.alberta.ca/alberta-media-fund"), ("Funding and incentives for film", "https://www.alberta.ca/funding-and-incentives-for-film-projects"), ("Alberta Made Production Grant", "https://www.alberta.ca/alberta-made-production-grant")]),
    ("Edmonton Screen Industries Office", "Alberta (Edmonton)", "tv games",
     "Funding and support for television and interactive digital media productions in the Metro Edmonton area, through the Edmonton Screen Media Fund.",
     [("Edmonton Screen Industries", "https://www.edmontonscreen.com")]),
    ("Creative Saskatchewan", "Saskatchewan", "film tv games tax",
     "Provincial agency that invests in the creative industries. Its film and TV support covers feature and television production, and its Digital Game Development Grant has a pre-production and a production stream, with grants of up to $50,000 or 50% of the cash budget a fiscal year, whichever is less (51% Saskatchewan ownership is required).",
     [("Film and TV production", "https://www.creativesask.ca/our-support/film-tv/feature-film-tv-production/"), ("Digital Game Development", "https://www.creativesask.ca/our-support/digital-game-development/digital-game-development")]),
    ("Manitoba Film & Music", "Manitoba", "film tv games tax",
     "Manitoba's film commission, administrator of the Manitoba Film and Video Production Tax Credit, and a funder of film and music projects. It has also run a Manitoba Indigenous Short Film Fund with the Indigenous Screen Office.",
     [("Manitoba Film & Music", "https://mbfilmmusic.ca/en/")]),
    ("SODEC", "Québec", "film tv tax",
     "Québec's agency for cultural enterprises. It supports script development, production and marketing of films, and administers Québec's film and television tax credits. Its site is mostly in French.",
     [("SODEC", "https://sodec.gouv.qc.ca/")]),
    ("PictureNL", "Newfoundland and Labrador", "film tv tax",
     "The province's lead screen agency. Its Equity Investment Program invests in Newfoundland and Labrador productions; the investment is recoupable and can be combined with the provincial film tax credit.",
     [("Equity Investment Program", "https://picturenl.smapply.ca/prog/equity_investment_program")]),
    ("Nova Scotia: Film and Television Production Incentive Fund", "Nova Scotia", "film tv tax",
     "The province's incentive fund for film and television production. The industry association Screen Nova Scotia runs a Content Creator Fund as a top-up for qualifying Nova Scotia productions.",
     [("Incentive Fund", "https://cch.novascotia.ca/film-and-television-production-incentive-fund"), ("Screen Nova Scotia", "https://screennovascotia.com")]),
    ("New Brunswick: film and TV programs", "New Brunswick", "film tv",
     "The provincial government's programs for development and production of film, television and new media. The CMPA lists a Development Incentive and a Production Incentive.",
     [("Province of New Brunswick", "https://www.gnb.ca"), ("CMPA: provinces and territories", "https://cmpa.ca/funding-opportunities/provincial-territories")]),
    ("PEI Film Production Fund", "Prince Edward Island", "film tv",
     "Financial rebates on spending for work completed in PEI, to encourage development, training and hiring of PEI film personnel.",
     [("PEI Film Production Fund", "https://www.princeedwardisland.ca/en/service/prince-edward-island-film-production-fund")]),
    ("Yukon Location Incentive Program", "Yukon", "film tv",
     "Yukon's incentive for productions: a travel rebate, a Yukon spend rebate and a training component.",
     [("Program framework", "https://yukon.ca/en/yukon-location-incentive-program-framework")]),
    ("NWT Film Commission", "Northwest Territories", "film tv",
     "The territory's film commission, which runs a film rebate for productions shooting in the Northwest Territories.",
     [("Film rebate", "https://www.nwtfilm.com/en/film-rebate")]),
    ("Nunavut Film Development Corporation", "Nunavut", "film tv indigenous",
     "Non-profit that provides funding, training and film commission services in Nunavut, with a series of funding incentives for filmmakers.",
     [("Funding programs", "https://www.nunavutfilm.ca/funding")]),

    # ---------------- Game tax credits ----------------
    ("Interactive digital media tax credits", "By province", "games tax",
     "Provincial tax credits for game and interactive studios. Ontario's OIDMTC is a refundable credit of up to 40% of eligible Ontario spending. Québec's multimedia credit is up to 37.5% of eligible labour, with Investissement Québec issuing the eligibility certificate. B.C., Manitoba, Newfoundland and Labrador and Nova Scotia each publish their own credit.",
     [("Ontario", "https://www.ontariocreates.ca/tax-incentives/oidmtc"), ("Québec", "https://www.investquebec.com/quebec/fr/financement/production-de-titres-multimedias.html"), ("B.C.", "https://www2.gov.bc.ca/gov/content/taxes/income-taxes/corporate/credits/interactive-digital-media"), ("Manitoba", "https://www.gov.mb.ca/jec/busdev/financial/midmtc/index.html"), ("Newfoundland and Labrador", "https://www.gov.nl.ca/fin/tax-programs-incentives/business/idmtc/"), ("Nova Scotia", "https://www.novascotia.ca/finance/en/home/taxation/tax101/businesstax/corporateincometax/digitalmediataxcredit.aspx.html")]),
]

CHIPS = [("all", "All"), ("film", "Film"), ("tv", "TV"), ("doc", "Documentary"), ("short", "Short film"), ("games", "Games and interactive"),
         ("post", "Post-production"), ("indigenous", "Indigenous"), ("tax", "Tax credits")]

CSS = (
    '<style>'
    '.ag-tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0 14px}'
    '.ag-tools input{flex:1 1 240px;padding:9px 12px;border:1px solid var(--line,#ccc);border-radius:8px;font:inherit;background:var(--panel,#fff);color:var(--ink,#16181d)}'
    '.ag-chip{border:1px solid var(--line,#ccc);background:var(--panel,#fff);color:var(--ink,#16181d);border-radius:999px;padding:6px 12px;font:inherit;font-size:.85rem;cursor:pointer}'
    '.ag-chip[aria-pressed="true"]{background:#d52b1e;border-color:#d52b1e;color:#fff}'
    '.ag-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}'
    '.ag{border:1px solid var(--line,#ddd);border-radius:10px;padding:12px 14px;background:var(--panel,#fff);color:var(--ink,#16181d)}'
    '.ag h3{margin:0 0 2px;font-size:1.02rem}.ag .where{font-size:.8rem;color:var(--mute,#69707d);margin-bottom:6px}'
    '.ag p{margin:0 0 8px;font-size:.92rem}.ag .links{font-size:.88rem;display:flex;flex-wrap:wrap;gap:4px 12px}'
    '.ag-count{font-size:.85rem;opacity:.75;margin:0 0 8px}'
    '</style>'
)

JS = (
    '<script>(function(){var q=document.getElementById("ag-q"),cards=[].slice.call(document.querySelectorAll(".ag")),'
    'chips=[].slice.call(document.querySelectorAll(".ag-chip")),cnt=document.getElementById("ag-n"),tag="all";'
    'function run(){var t=(q.value||"").toLowerCase(),n=0;cards.forEach(function(c){'
    'var ok=(tag==="all"||(" "+c.getAttribute("data-tags")+" ").indexOf(" "+tag+" ")>-1)&&(!t||c.textContent.toLowerCase().indexOf(t)>-1);'
    'c.style.display=ok?"":"none";if(ok)n++;});cnt.textContent=n+" of "+cards.length+" shown";}'
    'q.addEventListener("input",run);chips.forEach(function(b){b.addEventListener("click",function(){'
    'tag=b.getAttribute("data-tag");chips.forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});run();});});run();})();</script>'
)


def card(name, where, tags, what, links):
    ls = "".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a>' for l, u in links)
    return (f'<div class="ag" data-tags="{e(tags)}"><h3>{e(name)}</h3><div class="where">{e(where)}</div>'
            f'<p>{e(what)}</p><div class="links">{ls}</div></div>')


def section():
    chips = "".join(f'<button type="button" class="ag-chip" data-tag="{t}" aria-pressed="{"true" if t == "all" else "false"}">{e(l)}</button>' for t, l in CHIPS)
    return (
        CSS + '<h2 id="agencies">Funding agencies for filmmakers and game makers</h2>'
        '<p>Every screen funder we could find in Canada, federal, provincial and territorial, with a link to the agency itself. '
        'Search by name or place, or filter by what you make. We describe each one as its own pages do. '
        'We leave out deadlines and amounts that change with each intake, so open the link for the current call.</p>'
        '<div class="ag-tools"><input id="ag-q" type="search" placeholder="Search agencies: Alberta, games, short film, post..." aria-label="Search funding agencies">' + chips + '</div>'
        '<p class="ag-count" id="ag-n"></p>'
        '<div class="ag-list">' + "".join(card(*a) for a in AGENCIES) + '</div>'
        '<p class="note" style="margin-top:10px">Read on each agency\'s own pages in November 2026. Programs, rules and open dates change often, and some programs showed as closed or between intakes when we looked. '
        'If we missed a funder, tell us through the contact page. This is information, not advice.</p>'
        + JS
    )
