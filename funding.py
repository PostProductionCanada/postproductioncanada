"""Builds the 'Funding and Tax Credits' page.

Federal funding figures come from Canadian Heritage's Nov 8, 2026 backgrounder and a Canadian Press
story on Yahoo. Tax credit tables are shared with statuspage.py so there is one place to update them.
"""
import html
import statuspage as sp
import agencies

e = html.escape

BACKGROUNDER = ("https://www.canada.ca/en/canadian-heritage/news/2026/11/budget-2026-masters-of-our-destiny--backgrounder-"
                "administration-and-implementation-of-600-million-targeted-support-for-canadas-audio-and-audiovisua.html")
CP_YAHOO = "https://ca.finance.yahoo.com/news/ottawa-outlines-details-600m-cancon-184040035.html"
POLICY_OPTIONS = "https://policyoptions.irpp.org/2026/11/canadian-content-funding"
TELEFILM_FB = "https://www.facebook.com/telefilmcanada"
CMF_SITE = "https://cmf-fmc.ca/"
TELEFILM_SITE = "https://telefilm.ca/en"

# (recipient, what the backgrounder says it will do, amount as printed)
ALLOC = [
    ("Canada Media Fund", "Will rapidly deploy the new money through enhancements to existing programs and new initiatives across the industry's value chain, from training to creation, production, promotion and business development. Priority areas include francophone programming, children and youth content, interactive digital media, and distribution and export.", "$213.4M"),
    ("Independent production, news and radio funds", "Certified independent production funds ($44M), the Independent Local News Fund ($80M), the Commercial Radio News Fund ($11.5M), the Community Radio Fund ($7.5M) and services of exceptional importance such as CPAC, APTN and TV5 Québec Canada ($42.1M).", "$185.1M"),
    ("Telefilm Canada", "Supports the sustainability and growth of the audiovisual industry and the international reach of Canadian and Indigenous feature films, with an audience-driven approach.", "$68.5M"),
    ("Canada Music Fund", "Production and promotion of Canadian and Indigenous music, through FACTOR, Musicaction and three new recipients.", "$67M"),
    ("Indigenous Screen Office", "Supports the Indigenous audiovisual sector and the production, promotion and discoverability of Indigenous audiovisual content.", "$51M"),
    ("Northern Aboriginal Broadcasting", "Culturally relevant Indigenous radio and television content.", "$10M"),
    ("Canada History Fund", "Audiovisual programming and related costs.", "Up to $5M"),
]


def alloc_rows():
    return "".join(f'<tr><th scope="row">{e(r)}</th><td>{e(d)}</td><td style="white-space:nowrap"><b>{e(a)}</b></td></tr>' for r, d, a in ALLOC)


def lk(t, u):
    return f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>'


def money_section():
    return (
        '<h2>The $600 million: who gets what</h2>'
        '<p>On November 8, 2026, after Budget 2026, Culture Minister Marc Miller announced how the $600 million for Canada\'s audio and audiovisual sectors will be handed out. '
        'The government says the money is meant to provide stability while longer-term policy, regulatory and market conditions evolve. '
        'The list below is Canadian Heritage\'s own, in the order of the size of each share.</p>'
        '<div class="tw"><table><thead><tr><th>Recipient</th><th>What the government says it is for</th><th>Amount</th></tr></thead><tbody>'
        + alloc_rows() + '</tbody></table></div>'
        '<p class="note" style="margin-top:10px">Source: ' + lk("Canadian Heritage backgrounder, Nov 8, 2026", BACKGROUNDER) + '. The seven amounts add up to the $600 million total it prints for 2026-2027.</p>'
        '<div class="box warn"><h3>What is not settled</h3>'
        '<ul>'
        '<li><b>How long it lasts.</b> In June the government said it would provide $600 million in annual funding to replace payments from big streamers that the CRTC ordered under the Online Streaming Act. '
        'The Canadian Press reports the federal budget included only one year of the enhanced funding, and a government spokesperson said future amounts could vary once the new CRTC rules are final. (' + lk("Canadian Press, via Yahoo", CP_YAHOO) + ')</li>'
        '<li><b>What an analyst says.</b> Policy Options (Nov 24) reports the minister\'s position that, "once the new CRTC rules are finalized, the level of government investment will be adjusted as appropriate." '
        'Its author writes that the whole $600 million will not last, because it could be reduced by the amount streamers are required to reinvest in Canadian programming. (' + lk("Policy Options", POLICY_OPTIONS) + ')</li>'
        '<li><b>What it means for post.</b> The backgrounder does not name post-production. Most of the money goes to funds that pay for production and promotion, so the effect on post work will depend on how each fund writes its new programs. We have not seen those details yet.</li>'
        '<li><b>Telefilm.</b> Telefilm said on Nov 12 that its teams are mobilized to put the additional $68.5 million to work. (' + lk("Telefilm Canada on Facebook", TELEFILM_FB) + ') We will add details here once Telefilm publishes them.</li>'
        '</ul></div>'
        '<h3>Where to watch for the programs</h3>'
        '<ul><li>' + lk("Canada Media Fund", CMF_SITE) + '</li><li>' + lk("Telefilm Canada", TELEFILM_SITE) + '</li></ul>'
    )


def render(leaf, favicon, updated):
    head = sp.PAGE.split('<main class="wrap">')[0]
    head = head.replace("Status of the Artist and production by region — Post Production Canada", "Funding and Tax Credits — Post Production Canada")
    head = head.replace("What Status of the Artist laws mean for Canadian editors, and where production happens.",
                        "Federal screen funding after Budget 2026, plus film and TV tax credits by province and the credits aimed at VFX and post-production.")
    body = (
        '<main class="wrap">'
        '<h1>💰 Funding and Tax Credits</h1>'
        '<p class="lede">Where Canadian screen money comes from and where it lands. Researched from public sources, listed at the bottom. This is information, not legal or tax advice.</p>'
        '<p><a href="#agencies">Jump to the funding agencies directory ↓</a></p>'
        + money_section() +
        agencies.section() +
        '<h2>Production tax credits, federal and by province</h2>'
        '<p>These credits go to production companies, not to individual Editors. They matter because they decide where work lands, and some target post directly: BC\'s DAVE credit covers post-production and VFX labour, and Saskatchewan adds a bonus for post done in-province.</p>'
        '<div class="tw"><table><thead><tr><th>Where</th><th>Program and headline rates, as reported</th><th>Official links</th></tr></thead><tbody>'
        + sp.credits_rows() +
        '</tbody></table></div>'
        '<p class="note" style="margin-top:10px">Rates come from CMPA, law-firm and consultant summaries, and change often. Confirm with the agency before you plan around any figure. Northwest Territories was not covered in our research.</p>'
        + sp.vfx_section() +
        '<p>For what a production gets back after credits are stacked, province by province, and where shoots are happening, see our <a href="status-of-the-artist.html">Status of the Artist page</a>.</p>'
        '<h2>Sources</h2><ul>'
        '<li>' + lk("Budget 2026 backgrounder on the $600 million (Canadian Heritage)", BACKGROUNDER) + '</li>'
        '<li>' + lk("Ottawa outlines details of $600M for CanCon (Canadian Press, via Yahoo)", CP_YAHOO) + '</li>'
        '<li>' + lk("Weighing Ottawa\'s $600-million alternative to the Netflix tax (Policy Options)", POLICY_OPTIONS) + '</li>'
        '<li>' + lk("Telefilm Canada on Facebook", TELEFILM_FB) + '</li>'
        '<li>' + lk("Tax credits and incentives across Canada (CMPA)", sp.CMPA_HUB) + '</li>'
        '<li>' + lk("Incentives by province (filmincanada.com, an independent guide)", "https://filmincanada.com/incentives/manitoba") + '</li>'
        '<li>' + lk("Producing in Canada (Dentons)", "https://www.dentons.com/-/media/pdfs/guides-reports-and-whitepapers/producing-in-canada-guide.pdf") + '</li>'
        '</ul></main>'
        '<footer><div class="wrap">Page built ' + e(updated) + '. Post Production Canada links to original publishers and official sources.</div></footer></body></html>'
    )
    return (head + body).replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon)
