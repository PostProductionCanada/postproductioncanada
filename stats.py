"""By the Numbers: charts built only from figures printed on the publisher's own page.

Source check (our rule): every number below was read on the page it links to, on AS_OF.
A figure we worked out ourselves (a remainder, for example) is labelled "our arithmetic".
Nothing is estimated, projected or rounded by us. Edit the constants, then rebuild.
"""
import html
import topics

e = html.escape
AS_OF = "November 21, 2026"

STATCAN = "https://www150.statcan.gc.ca/n1/daily-quotidien/261009/dq261009d-eng.htm"
STATCAN_TABLE = "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2110006601"
BD = "https://broadcastdialogue.com/canadian-production-hits-10-17b-driven-by-foreign-services-telefilm-report/"

QC, BC, REST, INK2 = "#2f6fd0", "#0a8a6a", "#9aa1ad", "#d52b1e"

CSS = """<style>
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:16px 0}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.kpi b{display:block;font-size:30px;line-height:1.1;letter-spacing:-.02em}.kpi span{color:var(--mute);font-size:13px}
.kpi.dn b{color:var(--red)}.kpi.up b{color:#0a8a6a}
.fig{margin:0}.fig figcaption{color:var(--mute);font-size:13.5px;margin-top:8px}
.pies{display:flex;gap:22px;flex-wrap:wrap;justify-content:center;margin:8px 0}.pie{text-align:center;font-size:14px}
.pie svg{width:170px;height:170px;display:block;margin:0 auto 4px}.pie .yr{font-weight:800;font-size:17px}
.donut-bg{stroke:var(--line)}.dtxt{fill:var(--ink);font:800 6.4px ui-sans-serif,sans-serif;text-anchor:middle}.dsub{fill:var(--mute);font:4px ui-sans-serif,sans-serif;text-anchor:middle}
.leg{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;font-size:13.5px;margin:6px 0}.leg i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.bar{margin:10px 0}.bar .lb{display:flex;justify-content:space-between;font-size:14px;margin-bottom:3px}.bar .lb b{font-variant-numeric:tabular-nums}
.track{height:18px;background:var(--chip);border-radius:9px;overflow:hidden;display:flex}.track>span{display:block;height:100%}
.dv{display:grid;grid-template-columns:1fr 1fr;gap:0;align-items:center;margin:8px 0}.dv .neg,.dv .pos{height:22px;display:flex;align-items:center;font-size:13.5px;font-weight:700}
.dv .neg{justify-content:flex-end}.dv .neg span{display:block;height:22px;background:#d52b1e;border-radius:6px 0 0 6px}.dv .pos span{display:block;height:22px;background:#0a8a6a;border-radius:0 6px 6px 0}
.dv .t{grid-column:1 / -1;font-size:14px;margin:8px 0 2px}.dv .v{padding:0 8px}
.src li{margin:4px 0}table.dt{border-collapse:collapse;width:100%;font-size:14px;margin-top:8px}table.dt td,table.dt th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}
details.raw summary{cursor:pointer;color:var(--mute);font-size:13.5px}
.chk{border-left:4px solid #0a8a6a}
</style>"""


def donut(parts, centre, sub, label):
    """parts: [(value, color)] summing to 100. Circumference is 100 so a value is its own dash length."""
    r = 15.915
    off, segs = 25.0, ""
    for v, c in parts:
        segs += (f'<circle cx="21" cy="21" r="{r}" fill="none" stroke="{c}" stroke-width="7" '
                 f'stroke-dasharray="{v:.2f} {100 - v:.2f}" stroke-dashoffset="{off:.2f}"/>')
        off -= v
    return (f'<svg viewBox="0 0 42 42" role="img" aria-label="{e(label)}"><circle class="donut-bg" cx="21" cy="21" r="{r}" fill="none" stroke-width="7"/>{segs}'
            f'<text class="dtxt" x="21" y="22.4">{e(centre)}</text><text class="dsub" x="21" y="27.4">{e(sub)}</text></svg>')


def legend(items):
    return '<div class="leg">' + "".join(f'<span><i style="background:{c}"></i>{e(t)}</span>' for t, c in items) + '</div>'


def bar(label, value_txt, parts):
    segs = "".join(f'<span style="width:{w:.1f}%;background:{c}" title="{e(t)}"></span>' for w, c, t in parts)
    return f'<div class="bar"><div class="lb"><span>{e(label)}</span><b>{e(value_txt)}</b></div><div class="track">{segs}</div></div>'


def src(txt, url, extra=""):
    return f'<p class="note">Source: <a href="{e(url)}" target="_blank" rel="noopener">{e(txt)}</a>{extra}</p>'


def section_post():
    two = (f'<div class="pies"><div class="pie"><div class="yr">2023</div>'
           + donut([(49.0, QC), (28.7, BC), (22.3, REST)], "Record", "year, 2023", "2023 share of national post revenue: Quebec 49.0, British Columbia 28.7, all others 22.3")
           + '</div><div class="pie"><div class="yr">2025</div>'
           + donut([(40.7, QC), (36.8, BC), (22.5, REST)], "$2.4B", "StatCan", "2025 share of national post revenue: Quebec 40.7, British Columbia 36.8, all others 22.5")
           + '</div></div>'
           + legend([("Quebec 49.0% → 40.7%", QC), ("British Columbia 28.7% → 36.8%", BC), ("All other provinces and territories 22.3% → 22.5%", REST)]))
    return (
        '<h2>Who does Canada\'s post work</h2>'
        '<div class="box"><figure class="fig"><h3>Share of national post-production revenue</h3>' + two +
        '<figcaption>Quebec still leads, but its share is its lowest since 2017. British Columbia gained most. '
        'The grey slice is what remains after Quebec and B.C. (our arithmetic: 100 minus the two); StatCan\'s page does not break it out.</figcaption></figure>'
        + src("Statistics Canada, The Daily, Oct. 9, 2026", STATCAN) + '</div>'
        '<div class="box"><figure class="fig"><h3>Change in revenue, 2023 to 2025</h3>'
        '<div class="dv"><div class="t">Quebec: down 29.0%, <b>−$401.1 million</b></div><div class="neg"><span style="width:100%"></span></div><div class="pos"></div>'
        '<div class="t">British Columbia: now $884.4 million, <b>+$76.7 million</b></div><div class="neg"></div><div class="pos"><span style="width:19.1%"></span></div></div>'
        '<figcaption>Bars are drawn to the same scale. The national total fell 14.7%, so the decline was concentrated in Quebec.</figcaption></figure>'
        + src("Statistics Canada, The Daily, Oct. 9, 2026", STATCAN) + '</div>')


def section_vfx():
    return (
        '<h2>Visual effects and animation</h2>'
        '<div class="box"><figure class="fig"><h3>Visual effects and animation: share of national sales, 2025</h3>'
        + bar("British Columbia", "41.7%", [(41.7, BC, "British Columbia 41.7%"), (58.3, "transparent", "")])
        + bar("Quebec", "40.4% (was 51.0% in 2023)", [(40.4, QC, "Quebec 40.4%"), (59.6, "transparent", "")])
        + '<figcaption>British Columbia overtook Quebec as the leading province in this category. Its sales in the category grew 11.3% from 2023 to 2025. '
          'StatCan does not give B.C.\'s 2023 share on its page, so we do not show one.</figcaption></figure>'
        + src("Statistics Canada, The Daily, Oct. 9, 2026", STATCAN) + '</div>'
        '<div class="box"><figure class="fig"><h3>What the industry sells</h3>'
        + bar("Visual effects and animation services", "77.5% of industry sales (75.9% in 2023)", [(77.5, INK2, "VFX and animation 77.5%")])
        + '<figcaption>It is still the largest sales category. Total industry sales fell 16.8% from 2023 to 2025; '
          'visual effects and animation services fell 15.0% and 3D visual effects and animation services fell 26.0%, together 81.7% of the decrease.</figcaption></figure>'
        + src("Statistics Canada, The Daily, Oct. 9, 2026", STATCAN) + '</div>')


def section_money():
    return (
        '<h2>Where the money goes</h2>'
        '<div class="box"><figure class="fig"><h3>Operating expenses, 2025: $2.2 billion</h3>'
        + bar("Salaries, wages and benefits", "55.5%  ($1.2 billion, down 14.4% since 2023)", [(55.5, QC, "Salaries 55.5%")])
        + bar("Subcontracts", "11.2%", [(11.2, BC, "Subcontracts 11.2%")])
        + '<figcaption>The rest of the spending is not broken out on the page. Expenses fell 15.2% (−$403.5 million) from 2023, faster than revenue, so the operating profit margin rose from 6.0% to 6.7%.</figcaption></figure>'
        + src("Statistics Canada, The Daily, Oct. 9, 2026", STATCAN) + '</div>')


def section_production():
    return (
        '<h2>The production side, which feeds post</h2>'
        '<p>Post work follows shooting by months, so production figures show what may reach post rooms next. '
        'StatCan makes the same point: its production survey for 2025 is due in early 2027. '
        'These numbers are from Telefilm Canada\'s 2025–26 annual report, as reported by Broadcast Dialogue. They are about production, not post.</p>'
        '<div class="box"><figure class="fig"><h3>Canadian production volume: $10.17 billion, up 4.6%</h3><div class="pies"><div class="pie">'
        + donut([(52, BC), (48, REST)], "52%", "foreign", "Foreign production and production services are 52 percent of total production volume")
        + '</div></div>'
        + legend([("Foreign production and production services 52% (up 9.5%)", BC), ("Everything else 48% (our arithmetic)", REST)])
        + '<figcaption>The rise came mainly from foreign production and services, following the resolution of U.S. labour strikes, with domestic broadcasters\' in-house spending up 5.4%.</figcaption></figure>'
        + src("Broadcast Dialogue, on Telefilm Canada's 2025–26 annual report", BD) + '</div>'
        '<div class="box"><figure class="fig"><h3>Jobs, 2025–26</h3>'
        '<div class="dv"><div class="t">All film and TV jobs: 181,360, <b>−0.3%</b></div><div class="neg"><span style="width:3.6%"></span></div><div class="pos"></div>'
        '<div class="t">Canadian television production, <b>−6.6%</b></div><div class="neg"><span style="width:78.6%"></span></div><div class="pos"></div>'
        '<div class="t">Canadian feature film, <b>−8.4%</b></div><div class="neg"><span style="width:100%"></span></div><div class="pos"></div></div>'
        '<figcaption>Canadian feature films: 132 made, down from 147 (−10%), with volume down 3.2% to $460 million and the average English and French fiction feature budget up 9% to $3.5 million.</figcaption></figure>'
        + src("Broadcast Dialogue, on Telefilm Canada's 2025–26 annual report", BD) + '</div>')


ESAC_PR = "https://finance.yahoo.com/news/canadas-video-game-industry-contributed-083000266.html"
ESAC_SITE = "https://videogamescanada.ca"
THR_GTA = "https://www.hollywoodreporter.com/business/business-news/gta-vi-day-one-sales-1236760139/"
NUMERIS = "https://www.numeris.ca/resources/numeris-insights/the-year-in-canadian-media-what-audiences-watched-heard-and-streamed"


def section_audience():
    return (
        '<h2>Where Canadians watch</h2>'
        '<p>This is audience data, not an industry statistic. It shows where finished work is seen, which matters for formats, delivery and deliverables.</p>'
        '<div class="box"><figure class="fig"><h3>Share of streaming viewing, 2025–26 broadcast year</h3>'
        + bar("YouTube, nationally", "35%", [(35, QC, "YouTube 35%")])
        + bar("Prime Video, fall", "15%", [(15, BC, "Prime Video fall 15%")])
        + bar("Prime Video, summer", "19%", [(19, BC, "Prime Video summer 19%")])
        + bar("Netflix, winter (its strongest season)", "11%", [(11, INK2, "Netflix winter 11%")])
        + '<figcaption>Social video (TikTok, Instagram Reels, Facebook Video and Snapchat) is nearly one-third of streaming in Quebec. '
          'YouTube is strongest in Ontario and Atlantic Canada, at around 37%. Numeris links the Netflix winter peak to the final season of Stranger Things.</figcaption></figure>'
        + src("Numeris, The Year in Canadian Media, Oct. 19, 2026", NUMERIS) + '</div>')


def section_games():
    tot = 34010
    prov = [("Quebec", 15220, QC), ("British Columbia", 10930, BC), ("Ontario", 6090, INK2)]
    bars = "".join(bar(n, f"{v:,}", [(v / tot * 100, c, f"{n} {v:,}"), (100 - v / tot * 100, "transparent", "")]) for n, v, c in prov)
    return (
        '<h2>Games: big money next door to post</h2>'
        '<p>Games use the same skills as screen work: cinematics, VFX, animation, sound and Editors. These figures are from the games industry\'s own association, so read them as the industry\'s numbers.</p>'
        '<div class="kpis"><div class="kpi"><b>$5.1B</b><span>contribution to Canada\'s GDP, 2024</span></div>'
        '<div class="kpi"><b>34,010</b><span>full-time-equivalent jobs</span></div>'
        '<div class="kpi"><b>821</b><span>active video game studios</span></div>'
        '<div class="kpi"><b>$102,000</b><span>average salary</span></div></div>'
        '<div class="box"><figure class="fig"><h3>Games jobs by province (full-time equivalents)</h3>' + bars +
        '<figcaption>Bar length is each province\'s share of the 34,010 total (our arithmetic). The release does not break out the remaining jobs. '
        'The study, by Nordicity for the Entertainment Software Association of Canada (ESAC), also reports 86% of employees working full-time and an average age of 34.</figcaption></figure>'
        + src("ESAC economic impact study, released Jan. 28, 2025 (CNW)", ESAC_PR, ' · <a href="' + e(ESAC_SITE) + '" target="_blank" rel="noopener">Video Games Canada (ESAC)</a>') + '</div>'
        '<div class="box"><h3 style="margin-top:0">Rockstar says: GTA VI sold $3.79 billion on day one</h3>'
        '<p>Rockstar Games reported $3.79 billion in "day one retail sales" for <i>Grand Theft Auto VI</i> through Nov. 19, 2026, and 32.5 million units sold before release. '
        'It calls this the biggest entertainment launch in history. This is Rockstar\'s own internal estimate, it includes pre-sales, and it is one game\'s retail sales, so it is not comparable to the GDP figure above. '
        'We have not confirmed where any of the work was done.</p>'
        + src("The Hollywood Reporter, on Rockstar's announcement", THR_GTA) + '</div>')


def kpis():
    return ('<div class="kpis">'
            '<div class="kpi"><b>$2.4B</b><span>post-production revenue, 2025</span></div>'
            '<div class="kpi dn"><b>−14.7%</b><span>vs the 2023 record</span></div>'
            '<div class="kpi up"><b>+18.7%</b><span>vs 2019, before the pandemic</span></div>'
            '<div class="kpi"><b>6.7%</b><span>operating profit margin (6.0% in 2023)</span></div></div>')


def method():
    return ('<h2>How we check these</h2><div class="box chk"><p style="margin:0 0 8px">We publish a figure only if we read it on the publisher\'s own page, and the page is linked beside it. '
            'We do not estimate, project or round. When we work something out ourselves, such as a remainder, the chart says "our arithmetic". '
            'When a page leaves something out, we leave it out too. ' 'Figures were read on ' + e(AS_OF) + '.</p>'
            '<p class="note" style="margin:0">The post-production numbers are Statistics Canada\'s biennial survey, with 2021 and 2023 data revised. The next post release is scheduled for fall 2028. '
            'Spot an error? Email <a href="mailto:hello@postproductioncanada.ca?subject=Stats">hello@postproductioncanada.ca</a> with the page that shows it.</p></div>'
            '<h2>Sources</h2><ul class="src">'
            '<li><a href="' + e(STATCAN) + '" target="_blank" rel="noopener">Film, television and video post-production, 2025</a> · Statistics Canada, The Daily, released Oct. 9, 2026</li>'
            '<li><a href="' + e(STATCAN_TABLE) + '" target="_blank" rel="noopener">Table 21-10-0066-01</a> · Statistics Canada (the full data behind the release)</li>'
            '<li><a href="' + e(NUMERIS) + '" target="_blank" rel="noopener">The Year in Canadian Media: What Audiences Watched, Heard and Streamed</a> · Numeris, Oct. 19, 2026</li>'
            '<li><a href="' + e(ESAC_PR) + '" target="_blank" rel="noopener">Canada\'s Video Game Industry contributed $5.1 billion to GDP in 2024</a> · ESAC, via CNW, Jan. 28, 2025</li>'
            '<li><a href="' + e(THR_GTA) + '" target="_blank" rel="noopener">\'GTA VI\' Generates $3.79 Billion in "Day One" Sales</a> · The Hollywood Reporter</li>'
            '<li><a href="' + e(BD) + '" target="_blank" rel="noopener">Canadian production hits $10.17B driven by foreign services: Telefilm report</a> · Broadcast Dialogue, by Connie Thiessen</li></ul>')


def render(leaf, favicon, updated):
    body = (CSS + kpis()
            + '<p>Canada\'s post-production industry earned $2.4 billion in 2025. That is down from a record 2023 but still well above 2019. '
              'The change was uneven: British Columbia gained while Quebec fell. Every chart below comes from Statistics Canada or Telefilm Canada\'s own reporting.</p>'
            + section_post() + section_vfx() + section_money() + section_production() + section_audience() + section_games() + method())
    return topics._page(leaf, favicon, updated, "By the Numbers",
                        "Charts of Canadian post-production revenue, provinces, visual effects and production, from Statistics Canada and Telefilm Canada.",
                        "📊 By the Numbers", "Canada's post industry in charts, from Statistics Canada and Telefilm Canada.", body,
                        "Charts are drawn by us from the figures on the linked pages.")


def teaser():
    """Compact strip for the home page."""
    return (CSS + '<section class="picks"><h2>📊 By the numbers</h2>'
            '<div class="kpis" style="margin:8px 0"><div class="kpi"><b>$2.4B</b><span>post revenue in 2025, Statistics Canada</span></div>'
            '<div class="kpi dn"><b>−14.7%</b><span>since the 2023 record</span></div>'
            '<div class="kpi"><b>41.7%</b><span>of VFX and animation sales now in B.C., ahead of Quebec at 40.4%</span></div></div>'
            '<p class="note" style="margin:0 0 6px"><a href="stats.html">See the charts →</a></p></section>')
