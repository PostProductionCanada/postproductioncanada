"""'Did you know that was cut in Canada?': screen projects whose editing, effects, sound or colour was done in Canada.

Every item links to its source; where a source is a directory or listicle, the item says so.
Add new ones by appending to ITEMS.
"""
import html, re

e = html.escape

ITEMS = [
    {"title": "Frankenstein (Guillermo del Toro, Netflix)", "prov": ["ON"], "tags": ["VFX", "Shot in Canada"],
     "what": "Toronto studio Mr. X delivered 950 effects shots over almost two years, November 2023 to September 2025, on del Toro's film. The opening ice scenes were filmed in a parking lot at Netflix's Toronto studio and finished with effects. Other studios, including ILM, also worked on the film.",
     "sources": [("Inside the VFX of Frankenstein with Mr. X", "Autodesk", "https://blogs.autodesk.com/media-and-entertainment/2026/04/02/inside-the-vfx-of-frankenstein-with-mr-x"),
                 ("Tamara Deverell on building Frankenstein", "Motion Picture Association", "https://www.motionpictures.org/2025/10/production-designer-tamara-deverell-on-building-the-gothic-grandeur-of-guillermo-del-toros-frankenstein"),
                 ("Behind the VFX of Frankenstein", "ILM", "https://www.ilm.com/frankenstein-ilm-vfx-ivan-busquets-interview")]},
    {"title": "The Shape of Water, Crimson Peak, Nightmare Alley", "prov": ["ON"], "tags": ["VFX"],
     "what": "Mr. X, the Toronto-based studio, did the effects on these earlier del Toro films too. Production visual effects supervisor Dennis Berardi is described as a longtime collaborator of del Toro's, and the studio relaunched as an independent brand in 2025.",
     "sources": [("MR. X returns: storied VFX studio relaunches as independent, artist-led brand", "Yahoo Finance", "https://ca.finance.yahoo.com/news/mr-x-returns-storied-vfx-140800608.html")]},
    {"title": "Heated Rivalry", "prov": ["QC"], "tags": ["Editing"],
     "what": "Québec editor Véronique Barbe cut the series and won Best Editing in a TV Drama or Mini Series at the 2026 CCE Awards, plus a Canadian Screen Awards sweep for the show.",
     "sources": [("Heated Rivalry: local talent, Véronique Barbe, editor", "AQTIS 514 IATSE", "https://aqtis514iatse.com/en/why-choose-montreal/spotlight-on-our-members/5327/heated-rivalry-local-talent-veronique-barbe-editor"),
                 ("2026 CCE Awards", "Canadian Cinema Editors", "https://cceditors.ca/2026-awards")]},
    {"title": "Tron: Ares, The Odyssey, The Fantastic Four: First Steps", "prov": ["BC"], "tags": ["VFX"],
     "what": "A Vancouver VFX studio guide lists these among recent studio features with effects work from Vancouver studios: ILM and Image Engine on Tron: Ares, DNEG on The Odyssey, and Digital Domain on The Fantastic Four: First Steps. It is a directory rather than a credits database, so confirm credits before you quote them.",
     "sources": [("Best VFX studios in Vancouver (2026)", "Fabric (directory)", "https://fabric.so/best/vfx-vancouver")]},
]

STUDIO_RE = re.compile(r"Rodeo FX|Image Engine|Spin VFX|\bMR?\. X\b|Folks VFX|Soho VFX|Hybride|Frima|Eyeline|DNEG|"
                       r"(Vancouver|Montr[eé]al|Toronto|Ottawa|Calgary|Halifax|Winnipeg).{0,60}(VFX|visual effects)|"
                       r"(VFX|visual effects).{0,60}(Vancouver|Montr[eé]al|Toronto)", re.I)


def render(leaf, favicon, updated, latest):
    cards = ""
    for it in ITEMS:
        tags = "".join(f'<span class="pill">{e(t)}</span> ' for t in it["tags"])
        pins = "".join(f'<span class="pill pin">📍 {e(p)}</span> ' for p in it["prov"])
        src = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(o)}</span></li>' for t, o, u in it["sources"])
        cards += (f'<article class="box"><div>🇨🇦 {pins}{tags}</div><h3>{e(it["title"])}</h3><p>{e(it["what"])}</p><ul class="src">{src}</ul></article>')
    lat = ""
    for i in latest[:10]:
        d = i["date"].strftime("%b %-d") if hasattr(i["date"], "strftime") else ""
        pins = "".join(f' <span class="pill pin">📍 {e(p)}</span>' for p in i.get("prov", []))
        lat += f'<li>🇨🇦 <a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["title"])}</a>{pins} <span class="when">{e(i["source"])}, {e(d)}</span></li>'
    lat = f'<ul class="src" style="border:0;padding:0;margin:0">{lat}</ul>' if lat else '<p class="note">Nothing matching right now. This fills in as studios and trades report.</p>'
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{CARDS}}", cards)
            .replace("{{LATEST}}", lat).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Did you know that was cut in Canada? — Post Production Canada</title>
<meta name="description" content="Movies and TV whose editing, visual effects, sound or colour was done in Canada, plus the latest from Canadian VFX studios.">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}.wrap{max-width:820px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0;flex-wrap:wrap;gap:10px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink);white-space:nowrap}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;white-space:nowrap}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}h2{font-size:22px;margin:34px 0 8px}h3{font-size:20px;margin:6px 0}
.lede{color:var(--mute);font-size:18px}.note{color:var(--mute);font-size:14px}.when{color:var(--mute);font-size:13px;margin-left:6px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin:14px 0}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700}
.pill.pin{color:var(--mute)}
ul.src{list-style:none;padding:12px 0 0;margin:12px 0 0;border-top:1px solid var(--line)}ul.src li{margin:6px 0;font-size:14.5px}
.add{border-left:4px solid #e0a100}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/">← Latest news</a></div></header>
<main class="wrap">
<h1>🎞️ Did you know that was cut in Canada?</h1>
<p class="lede">Movies and television whose editing, visual effects, sound or colour was done in Canada, often for directors and studios you wouldn't expect.</p>
{{CARDS}}
<h2>Latest from Canadian VFX studios</h2>
<div class="box">{{LATEST}}</div>
<div class="box add"><h3>Know one?</h3><p class="note" style="margin:6px 0 0">Send a title and what was done in Canada, and we'll check the credits and add it. Directors like Guillermo del Toro are a good start, but a great story about a small film is welcome too.</p></div>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent. Summaries are ours, and each item links to its source.</div></footer>
</body>
</html>
"""
