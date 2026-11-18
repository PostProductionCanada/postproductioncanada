"""Builds the 'Status of the Artist, tax credits and production by region' page.

Everything here was researched from public sources (listed on the page). Figures are as
reported by those sources and change; the page says so. Edit the data below to update.
"""
import html

# CMPA Profile 2025 (April 2024 - March 2025), total film & TV production volume, $ millions.
# CMPA publishes 2023/24 totals plus growth; these are 2023/24 + growth (cross-checked against
# CMPA's stated 2024/25 totals for Ontario $3.84B, BC $2.69B, Quebec $2.69B, Canada $10.17B).
VOLUME = [
    ("Ontario", 3844, 18.5),
    ("British Columbia", 2691, 6.3),
    ("Québec", 2689, -6.2),
    ("Prairies & Territories", 599, -21.4),
    ("Atlantic Canada", 342, 7.9),
]

CMPA_HUB = "https://cmpa.ca/tax-credits-and-incentives"
LINKS = {
    "cptc": "https://www.canada.ca/en/canadian-heritage/services/funding/cavco-tax-credits/canadian-film-video-production.html",
    "pstc": "https://www.canada.ca/en/canadian-heritage/services/funding/cavco-tax-credits/film-video-production-services.html",
    "t1131": "https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/rc4164/canadian-film-video-production-tax-credit-guide-form-t1131.html",
    "bc": "https://creativebc.com/motion-picture-tax-credits",
    "on": "https://www.ontariocreates.ca/",
    "sk": "https://www.creativesask.ca/",
    "mb": "https://mbfilmmusic.ca/",
    "qc": "https://www.sodec.gouv.qc.ca/",
    "fic": "https://filmincanada.com/incentives/",
}


def fic(slug):
    return ("filmincanada.com", LINKS["fic"] + slug)


# (jurisdiction, program(s) and headline rates as reported, link label, url, note)
CREDITS = [
    ("Federal", "Canadian Film or Video Production Tax Credit (CPTC): 25% of qualified labour. "
                "Production Services Tax Credit (PSTC): 16% of qualified Canadian labour.",
     [("CPTC (CAVCO)", LINKS["cptc"]), ("PSTC (CAVCO)", LINKS["pstc"]), ("CRA guide, form T1131", LINKS["t1131"])],
     "Run jointly by CAVCO and the Canada Revenue Agency. A production can claim one of the two, not both."),
    ("British Columbia", "Film Incentive BC (basic 35%); Production Services Tax Credit (basic 36% per filmincanada.com, 2026; "
                         "an older CMPA summary lists 28%); DAVE: 16% on digital animation, VFX and post-production labour.",
     [("Creative BC", LINKS["bc"]), fic("british-columbia")],
     "The DAVE credit is aimed squarely at post and VFX work. The sources disagree on the basic rate, so confirm it with Creative BC."),
    ("Alberta", "Film and Television Tax Credit, reported at 22% or 30%.", [fic("alberta"), ("CMPA overview", CMPA_HUB)], ""),
    ("Saskatchewan", "Production grant (service stream: 25% of eligible spend, up to $5M), with a 5% bonus "
                     "when most post-production happens in the province.",
     [("Creative Saskatchewan", LINKS["sk"]), fic("saskatchewan")], "A grant program rather than a tax credit."),
    ("Manitoba", "Cost-of-Salaries credit 45% (up to 65% with bonuses) or Cost-of-Production credit 30% (up to 38%).",
     [("Manitoba Film & Music", LINKS["mb"]), fic("manitoba")], ""),
    ("Ontario", "Ontario Film and Television Tax Credit (35% of eligible labour); "
                "Ontario Production Services Tax Credit (21.5%).",
     [("Ontario Creates", LINKS["on"]), fic("ontario")], ""),
    ("Québec", "Film and Television Production Tax Credit and Production Services Tax Credit "
                       "(reported at 25% of spend, plus 16% on computer-aided effects and animation, per filmincanada.com).",
     [("SODEC", LINKS["qc"]), fic("quebec")], "Domestic credit rates not confirmed in my research. Check the program."),
    ("New Brunswick", "Production Incentive: CMPA lists service productions at 25% of all spend or 40% of labour, "
                      "and New Brunswick companies at 30% of all spend or 40% of labour.",
     [("CMPA overview", CMPA_HUB)], "filmincanada.com (2026) lists no service incentive for New Brunswick. The sources conflict, so confirm directly."),
    ("Nova Scotia", "Film and Television Production Incentive Fund, reported at about 25–26% of eligible spend.",
     [fic("nova-scotia"), ("CMPA overview", CMPA_HUB)], "An incentive fund, not a tax credit."),
    ("Newfoundland & Labrador", "Film and Video Tax Credit.", [("CMPA overview", CMPA_HUB)],
     "Rate not confirmed in my research."),
    ("Prince Edward Island", "Film and television incentive via the PEI Film & Television Office.",
     [("CMPA overview", CMPA_HUB)], "Details not confirmed in my research."),
    ("Yukon", "Yukon Location Incentive Program: travel rebate, Yukon spend rebate and a training component.",
     [("CMPA overview", CMPA_HUB)], ""),
    ("Nunavut", "Labour rebate of 17% or 27% of eligible costs, plus bonuses.", [("CMPA overview", CMPA_HUB)],
     "A rebate, not a tax credit."),
]

SOURCES = [
    ("Status of the Artist Act, full text (Justice Canada)", "https://laws-lois.justice.gc.ca/eng/acts/s-19.6/fulltext.html"),
    ("Federal certification of artists' associations (Canada Industrial Relations Board)",
     "https://cirb-ccri.gc.ca/en/about-appeals-applications-complaints/status-artist-act-certification"),
    ("Status of the Artist in Canada, 2010 update", "https://www.ecthree.org/wp-content/uploads/2019/06/statusoftheartistreport1126101-copy.pdf"),
    ("Brief to the House of Commons Heritage Committee (Union des artistes)",
     "https://www.ourcommons.ca/Content/Committee/441/CHPC/Brief/BR11709766/br-external/UnionDesArtistes-10596615-e.pdf"),
    ("Québec's Bill 35 adopted, 2022 (UNEQ)", "https://www.uneq.qc.ca/2022/06/03/status-of-the-artist-act-historic-victory"),
    ("AQTIS 514 IATSE reacts to Bill 35", "https://aqtis514iatse.com/stream.php?page=60+&filename=AQTIS+514+IATSE+r%C3%A9action+loi+35_EN.pdf"),
    ("A brief history of status of the artist (Saskatchewan Arts Alliance)",
     "https://www.saskartsalliance.ca/facts/a-brief-history-of-status-of-the-artist-in-canada"),
    ("Incentives by province (filmincanada.com, an independent guide)", "https://filmincanada.com/incentives/manitoba"),
    ("Production volume by region, Profile 2025 (CMPA)", "https://profile.cmpa.ca/en/overview-of-the-screen-sector-in-canada/12-region"),
    ("Tax credits and incentives across Canada (CMPA)", CMPA_HUB),
    ("Producing in Canada (Dentons)", "https://www.dentons.com/-/media/pdfs/guides-reports-and-whitepapers/producing-in-canada-guide.pdf"),
]

e = html.escape


def chart():
    top = max(v for _, v, _ in VOLUME)
    rows = []
    for name, v, g in VOLUME:
        w = round(v / top * 100, 1)
        cls = "up" if g >= 0 else "down"
        arrow = "▲" if g >= 0 else "▼"
        rows.append(
            f'<div class="row"><div class="lab">{e(name)}</div>'
            f'<div class="track"><div class="fill" style="width:{w}%"></div></div>'
            f'<div class="val">${v/1000:.2f}B <span class="{cls}">{arrow} {abs(g):.1f}%</span></div></div>')
    return "\n".join(rows)


def credits_rows():
    out = []
    for j, prog, links, note in CREDITS:
        ls = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a>' for l, u in links)
        n = f'<div class="note">{e(note)}</div>' if note else ""
        out.append(f'<tr><th scope="row">{e(j)}</th><td>{e(prog)}{n}</td><td>{ls}</td></tr>')
    return "\n".join(out)


def render(leaf, favicon, updated):
    srcs = "\n".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES)
    return PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{CHART}}", chart())\
        .replace("{{CREDITS}}", credits_rows()).replace("{{SOURCES}}", srcs).replace("{{UPDATED}}", updated)


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Status of the Artist, tax credits and production by region — Post Production Canada</title>
<meta name="description" content="What Status of the Artist laws mean for Canadian editors, film and TV tax credits by province, and where production happens.">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}
.wrap{max-width:860px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}
.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em;font-size:20px;text-decoration:none;color:var(--ink)}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}
.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}
h2{font-size:24px;letter-spacing:-.02em;margin:40px 0 8px}
h3{font-size:17px;margin:22px 0 4px}
p{margin:0 0 12px}.lede{color:var(--mute);font-size:18px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:16px 0}
.box.warn{border-left:4px solid #e0a100}.box.ok{border-left:4px solid #12a37f}
.box h3{margin-top:0}
ul{margin:6px 0 12px;padding-left:20px}li{margin:4px 0}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:14.5px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
tr:last-child th,tr:last-child td{border-bottom:0}
th[scope=row]{white-space:nowrap;width:1%}
.note{color:var(--mute);font-size:13px;margin-top:4px}
.tw{overflow-x:auto}
.chart{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.row{display:grid;grid-template-columns:150px 1fr 130px;gap:10px;align-items:center;margin:10px 0}
.track{background:var(--chip);border-radius:8px;height:22px;overflow:hidden}
.fill{background:var(--red);height:100%;border-radius:8px}
.val{font-size:14px;font-weight:700;white-space:nowrap}.up{color:#12a37f;font-weight:600}.down{color:var(--red);font-weight:600}
.lab{font-size:14.5px}
@media (max-width:560px){.row{grid-template-columns:1fr;gap:4px}}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a>
  <a class="btn" href="/">← Latest news</a>
</div></header>
<main class="wrap">
<h1>Status of the Artist, tax credits and where Canada produces</h1>
<p class="lede">A plain-language guide for editors and other post-production freelancers. Researched from public sources, listed at the bottom. This is information, not legal or tax advice.</p>

<h2>What "status of the artist" means</h2>
<p>It is ordinary legislation, not part of the Constitution. Its main job is to let unions, guilds and professional associations be formally recognized so they can bargain collectively for self-employed artists, who normally cannot bargain as a group the way employees do.</p>

<h3>Federal</h3>
<p>The federal Status of the Artist Act (1992) covers self-employed artists and the people who contribute to their work, but only when they work for federally regulated producers such as federal departments and broadcasters. It does not apply to employees. A certified association gets the exclusive right to bargain for its sector and can negotiate scale agreements. The Canada Industrial Relations Board handles certification.</p>

<h3>Québec</h3>
<p>Québec passed Canada's first law in 1987, for performing, recording and film artists, and a second in 1988 for visual arts, crafts and literature. In 2022, Bill 35 merged the two. Those laws treat covered artists as independent contractors and give recognized associations bargaining rights. A brief to a House of Commons committee says the federal act and Québec's act are the only laws in the country that create a true bargaining system for artists. The union AQTIS 514 IATSE represents about 8,000 freelancers in more than 200 audiovisual trades, including post-production.</p>

<h3>Other provinces</h3>
<p>Saskatchewan passed a broad act in 2002 that works more as a statement of principles. Other provinces have studied the issue or passed recognition-style laws, but none of them has Québec's bargaining system.</p>

<div class="box ok"><h3>What this means for an editor</h3>
<ul>
<li><b>In Québec,</b> the law is the foundation for collective agreements covering freelance technicians, and post-production trades fall under AQTIS's coverage.</li>
<li><b>Everywhere else,</b> an editor's pay and conditions come from union agreements and individual contracts, not from a status law.</li>
<li><b>Federally,</b> the act could matter for a self-employed editor working for a broadcaster, but only if the editor's sector is certified.</li>
</ul></div>
<div class="box warn"><h3>What I could not confirm</h3>
<p>I could not confirm that picture editors are named in Québec's law or covered by a federal certification. Before you rely on any of this, check with AQTIS (Québec), your union local, or the Canada Industrial Relations Board's certification register. I'm also not certain of the details of every provincial act.</p></div>

<h2>Production tax credits, federal and by province</h2>
<p>These credits go to production companies, not to individual editors. They matter because they decide where work lands, and some target post directly: BC's DAVE credit covers post-production and VFX labour, and Saskatchewan adds a bonus for post done in-province.</p>
<div class="tw"><table>
<thead><tr><th>Where</th><th>Program and headline rates, as reported</th><th>Official links</th></tr></thead>
<tbody>
{{CREDITS}}
</tbody></table></div>
<p class="note" style="margin-top:10px">Rates come from CMPA, law-firm and consultant summaries, and change often. Confirm with the agency before you plan around any figure. Northwest Territories was not covered in my research.</p>

<h2>Where production happens</h2>
<p>Total film and television production volume by region, April 2024 to March 2025, in dollars, with the change from the year before. Canada's total was $10.17 billion.</p>
<div class="chart" role="img" aria-label="Bar chart of production volume by region">
{{CHART}}
</div>
<p class="note" style="margin-top:10px">Source: CMPA Profile 2025, estimates based on CAVCO data. Includes Canadian production, foreign location and service work, and broadcaster in-house production. CMPA reports the Prairies and Territories together and the Atlantic provinces together, so I can't split them further. I used dollars because it's the only figure published on the same basis for every region. Counts of productions aren't published consistently by province.</p>

<h2>Sources</h2>
<ul>
{{SOURCES}}
</ul>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada links to original publishers and official sources.</div></footer>
</body>
</html>
"""
