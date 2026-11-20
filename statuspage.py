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
    ("British Columbia", "Film Incentive BC (basic 40%); Production Services Tax Credit (basic 36%), both raised in 2025 for productions "
                         "starting principal photography after Dec 31, 2024, per Creative BC; DAVE: 16% on digital animation, VFX and post-production labour.",
     [("Creative BC", LINKS["bc"]), fic("british-columbia")],
     "The DAVE credit is aimed squarely at post and VFX work. Older summaries still show the previous 35% and 28% rates."),
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
     [("SODEC", LINKS["qc"]), fic("quebec")], "Domestic credit rates not confirmed in our research. Check the program."),
    ("New Brunswick", "Production Incentive: CMPA lists service productions at 25% of all spend or 40% of labour, "
                      "and New Brunswick companies at 30% of all spend or 40% of labour.",
     [("CMPA overview", CMPA_HUB)], "filmincanada.com (2026) lists no service incentive for New Brunswick. The sources conflict, so confirm directly."),
    ("Nova Scotia", "Film and Television Production Incentive Fund, reported at about 25–26% of eligible spend.",
     [fic("nova-scotia"), ("CMPA overview", CMPA_HUB)], "An incentive fund, not a tax credit."),
    ("Newfoundland & Labrador", "Film and Video Tax Credit.", [("CMPA overview", CMPA_HUB)],
     "Rate not confirmed in our research."),
    ("Prince Edward Island", "Film and television incentive via the PEI Film & Television Office.",
     [("CMPA overview", CMPA_HUB)], "Details not confirmed in our research."),
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

import json
from pathlib import Path

PROV_NAMES = {"ON": "Ontario", "BC": "British Columbia", "QC": "Québec", "NS": "Nova Scotia", "MB": "Manitoba",
              "NL": "Newfoundland & Labrador", "AB": "Alberta", "SK": "Saskatchewan", "NB": "New Brunswick",
              "PE": "Prince Edward Island", "NU": "Nunavut", "NT": "Northwest Territories", "YT": "Yukon"}


def load_fic():
    try:
        return json.loads((Path(__file__).parent / "data" / "filmincanada.json").read_text())
    except Exception:
        return None


def tracked_chart(d):
    rows = []
    top = max(v["total"] for v in d["by_province"].values())
    for code, v in d["by_province"].items():
        seg = ""
        for st, cls in (("shooting", "s-shoot"), ("prep", "s-prep"), ("wrapping", "s-wrap")):
            n = v.get(st, 0)
            if n:
                seg += f'<div class="seg {cls}" style="width:{n / top * 100:.1f}%" title="{n} {st}"></div>'
        rows.append(f'<div class="row2"><div class="lab">{e(PROV_NAMES.get(code, code))}</div>'
                    f'<div class="track2">{seg}</div><div class="val">{v["total"]}</div></div>')
    return "\n".join(rows)


def incentive_chart(d):
    inc = d["incentives_net_effective_12m_series"]
    have = sorted(((c, v["name"], v["net_effective"]) for c, v in inc.items() if v["net_effective"] is not None),
                  key=lambda x: -x[2])
    none = [v["name"] for c, v in inc.items() if v["net_effective"] is None]
    top = max(h[2] for h in have)
    rows = "\n".join(
        f'<div class="row"><div class="lab">{e(n)}</div><div class="track"><div class="fill" style="width:{p / top * 100:.1f}%"></div></div>'
        f'<div class="val">{p:.1f}%</div></div>' for _, n, p in have)
    return rows, ", ".join(none)


def type_chart(d):
    labels = {"series": "Series", "feature": "Features", "mow": "Movies of the week", "unknown": "Not stated",
              "limited": "Limited series", "doc": "Documentary", "music_video": "Music video"}
    items = sorted(d["by_type"].items(), key=lambda kv: -kv[1])
    top = items[0][1]
    return "\n".join(
        f'<div class="row"><div class="lab">{e(labels.get(k, k))}</div><div class="track"><div class="fill dark" style="width:{n / top * 100:.1f}%"></div></div>'
        f'<div class="val">{n}</div></div>' for k, n in items)


def fic_section(d):
    if not d:
        return ""
    inc_rows, none = incentive_chart(d)
    sh, pr, wr = (d["by_status"].get(k, 0) for k in ("shooting", "prep", "wrapping"))
    return f"""
<h2>Work heading toward post, by province</h2>
<p>Shoots are a leading indicator for post: a production that is wrapping is about to land in the edit, and one in prep will follow.
These are productions in prep, shooting or wrapping, counted from public listings by filmincanada.com. Snapshot of
<b>{e(d["now_shooting_last_run"] or "unknown date")}</b>: {d["records"]} productions, {wr} wrapping (closest to post), {sh} shooting and {pr} in prep.</p>
<div class="chart" role="img" aria-label="Stacked bar chart of productions heading toward post, by province">
<div class="legend"><span><i class="s-wrap"></i>Wrapping (post next)</span><span><i class="s-shoot"></i>Shooting</span><span><i class="s-prep"></i>In prep</span></div>
{tracked_chart(d)}
</div>
<p class="note" style="margin-top:10px">Treat this as a rough guide. The tracker draws on public listings such as ACTRA, UBCP and provincial agency pages, so it favours productions that appear there. It is not a complete count, and it was last updated in August, so a production's status will have moved on since. For where the money is spent, use the dollar chart above.</p>

<h3>By type of production</h3>
<div class="chart">
{type_chart(d)}
</div>

<h2>What a production gets back, by province</h2>
<p>Estimated net effective incentive on a $12M (USD) limited series made as a service production, as modelled by filmincanada.com. It combines provincial and federal credits, so it is a comparison tool, not a promise.</p>
<div class="chart" role="img" aria-label="Bar chart of estimated net effective incentive by province">
{inc_rows}
</div>
<p class="note" style="margin-top:10px">No service incentive listed for: {e(none)}.</p>

<div class="box"><h3>About this data</h3>
<p>Numbers in these three charts come from <a href="https://filmincanada.com/" target="_blank" rel="noopener">filmincanada.com</a>
(<a href="{e(d["source_urls"]["now_shooting"])}" target="_blank" rel="noopener">Now Shooting</a>,
<a href="{e(d["source_urls"]["incentives"])}" target="_blank" rel="noopener">incentives by province</a>), an independent guide. The site says it is run by a service production company with a commercial interest in production volume. I show counts only and link to the full detail on their site. Fetched {e(d["fetched_at"][:10])}.</p></div>
"""


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


VFX_ROWS = [
    ("Federal", "Film or Video Production Services Tax Credit (PSTC): 16% of qualified Canadian labour. No VFX-specific bonus.",
     [("PSTC (CAVCO)", LINKS["pstc"])]),
    ("British Columbia", "DAVE: 16% of eligible BC labour directly attributable to digital animation, visual effects and post-production. It is a bonus on top of the basic PSTC (36%) or Film Incentive BC (40%), and you must claim one of those first. Entertainment Partners notes that PSTC plus DAVE is available to productions with only VFX and post work done in BC, with no principal photography requirement.",
     [("DAVE bulletin (Creative BC)", "https://creativebc.com/wp-content/uploads/2025/07/DAVE_Tax_Credit_Info_Bulletin_FAQ.pdf"),
      ("PSTC rates (Creative BC)", "https://creativebc.com/motion-picture-tax-credits/production-services-tax-credit")]),
    ("Ontario", "OCASE: 18% of eligible Ontario labour on computer animation and special effects, no cap, claimed on top of the OFTTC (35%) or OPSTC (21.5%). Animation studios, VFX houses, post houses and 3D service providers can qualify. Ontario labour must exceed $25,000. Eligibility depends on several tests, so it is not a simple parallel to BC.",
     [("OCASE (Ontario Creates)", "https://www.ontariocreates.ca/tax-incentives/ocase")]),
    ("Québec", "On top of the Production Services Tax Credit (25% of qualified spend), an extra 16% on qualified labour for computer-aided special effects and animation, including chroma-key shooting. The domestic credit has a smaller bonus, reported at 10% with a cap.",
     [("Overview (Entertainment Partners)", "https://www.ep.com/blog/vfx-post-production-tax-incentives-guide"),
      ("Animation and effects credits (Time Consulting)", "https://timeconsulting.ca/animation-special-effects-tax-credits")]),
    ("Other provinces", "We found no VFX-specific credit in Alberta, Saskatchewan, Manitoba, the Atlantic provinces or the territories. Their general credits may still cover post spend, so check each program.",
     [("CMPA overview", CMPA_HUB)]),
]


def vfx_section():
    rows = []
    for j, txt, links in VFX_ROWS:
        ls = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a>' for l, u in links)
        rows.append(f'<tr><th scope="row">{e(j)}</th><td>{e(txt)}</td><td>{ls}</td></tr>')
    return ('<h2>Credits for VFX, animation and post</h2>'
            '<p>Three places run credits aimed squarely at visual effects, animation and post-production work: British Columbia, Ontario and Québec. '
            'These go to production and post companies, not individual artists, but they decide where VFX and post work gets booked.</p>'
            '<div class="tw"><table><thead><tr><th>Where</th><th>What it adds</th><th>Official sources</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>'
            '<p class="note" style="margin-top:10px">Rates checked against Creative BC and Ontario Creates on Nov 18, 2026. Budgets change these, so confirm with the agency before you plan around a figure.</p>'
            '<div class="box"><h3 style="margin-top:0">Further reading</h3><ul>'
            '<li><a href="https://www.fixersincanada.ca/blog/film-tax-incentives-guide/" target="_blank" rel="noopener">Film tax credits in Canada: CPTC and provincial stacking guide</a> <span class="pill">vendor</span> Fixers in Canada'
            '<div class="note">A production-services company\'s explainer on how federal and provincial credits combine. Its figures may lag the official pages, so check them against the agencies above.</div></li>'
            '<li><a href="https://www.fixersincanada.ca/blog/post-production-facilities-guide/" target="_blank" rel="noopener">Post-production facilities guide: local vs international</a> <span class="pill">vendor</span> Fixers in Canada'
            '<div class="note">A service company\'s view on choosing between local and international post facilities. It sells production services, so read it as a vendor guide.</div></li>'
            '</ul></div>')


def render(leaf, favicon, updated):
    fic_html = fic_section(load_fic())
    srcs = "\n".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES)
    return PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{VFX}}", vfx_section()).replace("{{CHART}}", chart()).replace("{{FIC}}", fic_html)\
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
.fill.dark{background:var(--ink)}
.row2{display:grid;grid-template-columns:150px 1fr 40px;gap:10px;align-items:center;margin:8px 0}
.track2{display:flex;height:22px;background:var(--chip);border-radius:8px;overflow:hidden}
.seg{height:100%}.s-shoot{background:var(--red)}.s-prep{background:#e0a100}.s-wrap{background:#2f7de1}
.legend{display:flex;gap:16px;font-size:13px;color:var(--mute);margin-bottom:6px;flex-wrap:wrap}
.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.row2 .val{text-align:right}
@media (max-width:560px){.row{grid-template-columns:1fr;gap:4px}.row2{grid-template-columns:110px 1fr 34px}}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a>
  <a class="btn" href="/">← Latest news</a>
</div></header>
<main class="wrap">
<h1>⚖️ Status of the Artist, tax credits and where Canada produces</h1>
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
<div class="box warn"><h3>What we could not confirm</h3>
<p>We could not confirm that picture editors are named in Québec's law or covered by a federal certification. Before you rely on any of this, check with AQTIS (Québec), your union local, or the Canada Industrial Relations Board's certification register. I'm also not certain of the details of every provincial act.</p></div>

<h2>Production tax credits, federal and by province</h2>
<p>These credits go to production companies, not to individual editors. They matter because they decide where work lands, and some target post directly: BC's DAVE credit covers post-production and VFX labour, and Saskatchewan adds a bonus for post done in-province.</p>
<div class="tw"><table>
<thead><tr><th>Where</th><th>Program and headline rates, as reported</th><th>Official links</th></tr></thead>
<tbody>
{{CREDITS}}
</tbody></table></div>
<p class="note" style="margin-top:10px">Rates come from CMPA, law-firm and consultant summaries, and change often. Confirm with the agency before you plan around any figure. Northwest Territories was not covered in our research.</p>

{{VFX}}

<h2>Where production happens</h2>
<p>Total film and television production volume by region, April 2024 to March 2025, in dollars, with the change from the year before. Canada's total was $10.17 billion.</p>
<div class="chart" role="img" aria-label="Bar chart of production volume by region">
{{CHART}}
</div>
<p class="note" style="margin-top:10px">Source: CMPA Profile 2025, estimates based on CAVCO data. Includes Canadian production, foreign location and service work, and broadcaster in-house production. CMPA reports the Prairies and Territories together and the Atlantic provinces together, so we can't split them further. We used dollars because it's the only figure published on the same basis for every region. Counts of productions aren't published consistently by province.</p>

{{FIC}}

<h2>Sources</h2>
<ul>
{{SOURCES}}
</ul>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada links to original publishers and official sources.</div></footer>
</body>
</html>
"""
