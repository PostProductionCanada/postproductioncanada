"""Builds the 'Canadian editors' page: a Canadian Cinema Editors (CCE) section, the Vancouver Post
Alliance on the west coast, and a reading list of articles about Canadian editors.

The CCE is a non-profit professional association. It is NOT a union, and this page never files it
under unions. Facts below were checked against the CCE's own pages, Playback and other sources.
"""
import html
from datetime import datetime

e = html.escape

CCE_SITE = "https://cceditors.ca/"

# Verified against cceditors.ca/2026-awards
CCE_AWARDS_2026 = [
    ("Lifetime Achievement Award", "Annie Jean, CCE"),
    ("Career Achievement Award", "Didier Kennel"),
    ("Best Editing in TV Drama / Mini Series", "Véronique Barbe, CCE, Heated Rivalry, ep. 105"),
    ("Best Editing in Feature Film", "Yvann Thibaudeau, CCE and Dorian Rigal-Ansous, Ma mère, Dieu et Sylvie Vartan"),
    ("Best Editing in Web Series / Digital Content", "Zoé Guèvremont, Fleur de peau, ep. 105"),
]

CCE_LINKS = [
    ("CCE website", CCE_SITE),
    ("2026 CCE Awards, full nominees and winners", "https://cceditors.ca/2026-awards"),
    ("EditCon 2026, the annual picture-editing conference", "https://cceditors.ca/editcon-2026"),
]

# (title, source, date, url, note). Only items I opened or saw in search results.
ARTICLES = [
    ("Canadian Cinema Editors names 2026 winners", "Playback", "2026-05-25",
     "https://playbackonline.ca/2026/05/25/canadian-cinema-editors-names-2026-winners",
     "Trade coverage of the 16th CCE Awards, held in Toronto on May 22."),
    ("Heated Rivalry: local talent, Véronique Barbe, editor", "AQTIS 514 IATSE", "2026-01-23",
     "https://aqtis514iatse.com/en/why-choose-montreal/spotlight-on-our-members/5327/heated-rivalry-local-talent-veronique-barbe-editor",
     "An interview with the editor behind one of the year's biggest Canadian series, on how editing finds a story's emotion."),
    ("Company 3 projects recognized with CCE Awards nominations", "Company 3", "2026-04-16",
     "https://www.company3.com/2026-cce-awards-nominations",
     "A post house's view of the nominees, with the colourists and finishing editors credited alongside the editors."),
    ("'Heated Rivalry' tops Canadian Screen Awards with 16 wins", "Deadline", "2026-06-01",
     "https://deadline.com/2026/06/heated-rivalry-tops-canadian-screen-awards-1236931778",
     "Full winners list, including the editing categories."),
    ("Canadian Cinema Editors", "Wikipedia", "",
     "https://en.wikipedia.org/wiki/Canadian_Cinema_Editors",
     "Background on the association: founding, membership levels and past awards."),
]

VPA_SITE = "https://vancouverpostalliance.com/"


def feed_list(items, n=8):
    if not items:
        return "<p class=\"note\">Nothing to show right now.</p>"
    rows = []
    for i in items[:n]:
        d = i["date"].strftime("%b %-d, %Y") if isinstance(i["date"], datetime) else ""
        rows.append(f'<li><a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["title"])}</a> <span class="when">{e(d)}</span></li>')
    return "<ul class=\"feed\">" + "".join(rows) + "</ul>"


def render(leaf, favicon, updated, cce_items, vpa_items):
    awards = "".join(f"<li><b>{e(a)}:</b> {e(w)}</li>" for a, w in CCE_AWARDS_2026)
    links = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in CCE_LINKS)
    arts = "".join(
        f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(s)}{", " + e(d) if d else ""}</span>'
        f'<div class="note">{e(n)}</div></li>' for t, s, d, u, n in ARTICLES)
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{AWARDS}}", awards)
            .replace("{{CCELINKS}}", links).replace("{{ARTICLES}}", arts).replace("{{CCEFEED}}", feed_list(cce_items))
            .replace("{{VPAFEED}}", feed_list(vpa_items, 5)).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Canadian editors, the CCE and the Vancouver Post Alliance — Post Production Canada</title>
<meta name="description" content="Canadian Cinema Editors news and awards, the Vancouver Post Alliance, and a reading list on Canadian picture editors.">
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
h3{font-size:17px;margin:18px 0 4px}
p{margin:0 0 12px}.lede{color:var(--mute);font-size:18px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:16px 0}
.cce{display:grid;grid-template-columns:230px 1fr;gap:20px;align-items:start}
.logobox{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;display:block}
.logobox img{width:100%;height:auto;display:block}
.credit{font-size:11.5px;color:var(--mute);margin-top:6px}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700;margin-bottom:6px}
ul{margin:6px 0 12px;padding-left:20px}li{margin:6px 0}
.feed,.arts{list-style:none;padding:0}.feed li,.arts li{padding:10px 0;border-bottom:1px solid var(--line);margin:0}
.feed li:last-child,.arts li:last-child{border-bottom:0}
.when{color:var(--mute);font-size:13px;margin-left:6px}
.note{color:var(--mute);font-size:13.5px;margin-top:2px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:640px){.cce,.cols{grid-template-columns:1fr}.logobox{max-width:260px}}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a>
  <a class="btn" href="/">← Latest news</a>
</div></header>
<main class="wrap">
<h1>Canadian editors</h1>
<p class="lede">The Canadian Cinema Editors, a west coast post community, and a reading list on the people who cut Canada's screen stories.</p>

<h2>Canadian Cinema Editors (CCE)</h2>
<div class="box cce">
  <div>
    <a class="logobox" href="https://cceditors.ca/" target="_blank" rel="noopener"><img src="cce-logo.jpg" alt="Canadian Cinema Editors / Les Monteurs et Monteuses de cinéma canadien logo" width="500" height="143"></a>
    <div class="credit">Logo © Canadian Cinema Editors</div>
  </div>
  <div>
    <span class="pill">Non-profit professional association</span>
    <p>The CCE is a bilingual, not-for-profit professional, educational and cultural association for Canada-wide post-production people, founded in 2007 and based in Toronto. It exists to promote picture editing in film, television and new media, to educate peers and students, and to show Canadian editors' work to the world. <b>It is not a union.</b> It runs the CCE Awards, the annual EditCon conference, mentorship, a podcast and an editor directory.</p>
    <ul>{{CCELINKS}}</ul>
  </div>
</div>

<h3>2026 CCE Awards, a few highlights</h3>
<p class="note">The 16th CCE Awards were held May 22, 2026 at the Delta Hotel in Toronto, with 17 awards.</p>
<ul>{{AWARDS}}</ul>

<h3>Latest from the CCE</h3>
<div class="box">{{CCEFEED}}</div>

<h2>West coast: Vancouver Post Alliance</h2>
<div class="box">
  <span class="pill">Non-profit association, British Columbia</span>
  <p>The Vancouver Post Alliance (VPA) is a non-profit association that represents BC's post-production industry. It began as an ad hoc steering committee in spring 2013 and was established as a non-profit society a few months later. It promotes and markets BC's post talent, runs professional development and networking, and speaks for the industry to government. Its lobbying helped get post-production services added to BC's DAVE tax credit on March 1, 2015.</p>
  <ul>
    <li><a href="https://vancouverpostalliance.com/" target="_blank" rel="noopener">Vancouver Post Alliance website</a></li>
    <li><a href="https://vancouverpostalliance.com/our-story" target="_blank" rel="noopener">Its story and founding members</a></li>
  </ul>
  <h3>Latest from the VPA</h3>
  {{VPAFEED}}
</div>

<h2>Reading list: Canadian editors in the news</h2>
<div class="box"><ul class="arts">{{ARTICLES}}</ul></div>
<p class="note">Headlines and links only. Each story belongs to its publisher. The CCE and VPA lists above update automatically from their own feeds.</p>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent and is not affiliated with the CCE or the VPA.</div></footer>
</body>
</html>
"""
