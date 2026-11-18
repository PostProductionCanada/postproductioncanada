#!/usr/bin/env python3
"""Post Production Canada - fetch feeds, build a static site into ./public.

Python 3 standard library only. Run:  python3 build.py
Headlines + short excerpts only; every item links back to the original publisher.
"""
import html, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
OUT = ROOT / "public"
SITE_URL = "https://postproductioncanada.ca"
MAX_AGE_DAYS = 21
MAX_ITEMS = 180
UA = "Mozilla/5.0 (compatible; PostProductionCanadaBot/1.0; +https://postproductioncanada.ca)"

CANADA_RE = re.compile(
    r"\b(canada|canadian|canadians|toronto|vancouver|montreal|montr[eé]al|ottawa|calgary|winnipeg|halifax|"
    r"ontario|qu[eé]bec|british columbia|alberta|manitoba|saskatchewan|nova scotia|new brunswick|"
    r"newfoundland|telefilm|cmf|dgc|cmpa|actra|iatse 873|unifor|creative bc|omdc|cbc|crtc|"
    r"cineplex|bell media|corus|rogers)\b", re.I)
POST_RE = re.compile(
    r"\b(post[- ]?production|editor|editing|edit|colou?r|grade|grading|dit|vfx|visual effects|compositing|"
    r"animation|sound|mix|mixing|audio|dubbing|davinci|resolve|avid|premiere|after effects|nuke|flame|"
    r"workflow|render|pipeline|finishing|dolby|hdr|lut|footage|camera|cinematograph\w*|studio|production|"
    r"film|tv|television|series|documentary|streaming|tax credit|union|guild|funding)\b", re.I)

SCREEN_RE = re.compile(
    r"\b(film\w*|movie\w*|tv|television|series|show|vfx|visual effects|animat\w+|post[- ]?production|"
    r"production\w*|studio\w*|streaming|streamer|screen\w*|cinema\w*|broadcast\w*|editor\w*|editing|"
    r"cinematograph\w*|director\w*|actor\w*|actra|iatse|dgc|telefilm|cmf|netflix|disney|paramount|"
    r"documentar\w+|festival|tiff|box office|sound|audio|colou?r|davinci|avid|adobe|content|crew|"
    r"tax credit|soundstage|set|shoot\w*|casting|screenwrit\w+|writers?)\b", re.I)
EXCLUDE_RE = re.compile(
    r"\b(radio stations?|earnings|tsx|nasdaq|stock\w*|shares|ammunition|air defen[cs]e|tariffs?|"
    r"auto industry|mortgage|real estate|hockey|nhl|wildfire|weather forecast|horoscope|crypto\w*)\b", re.I)

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "media": "http://search.yahoo.com/mrss/",
}

def strip_tags(s):
    s = re.sub(r"<(script|style).*?</\1>", "", s or "", flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def clip(s, n=220):
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(",;:.") + "…"

def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except Exception:
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

def text(el, path):
    x = el.find(path, NS)
    return x.text.strip() if x is not None and x.text else ""

def fetch(feed):
    try:
        req = Request(feed["url"], headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
        with urlopen(req, timeout=20) as r:
            data = r.read()
        root = ET.fromstring(data)
    except Exception as e:
        print(f"  FAIL {feed['name']}: {e}", file=sys.stderr)
        return feed, []
    items = []
    entries = root.findall(".//item") or root.findall(".//atom:entry", NS)
    for e in entries:
        title = strip_tags(text(e, "title"))
        link = text(e, "link")
        if not link:
            le = e.find("atom:link", NS)
            link = le.get("href", "") if le is not None else ""
        desc = text(e, "description") or text(e, "atom:summary") or text(e, "content:encoded") or text(e, "atom:content")
        date = parse_date(text(e, "pubDate") or text(e, "dc:date") or text(e, "atom:published") or text(e, "atom:updated"))
        source = feed["name"]
        if feed.get("google"):
            se = e.find("source")
            if se is not None and se.text:
                source = se.text.strip()
            title = re.sub(r"\s+-\s+" + re.escape(source) + r"$", "", title)
            desc = ""  # Google News descriptions are just link lists
        if not (title and link and date):
            continue
        items.append({"title": title, "url": link, "date": date, "source": source,
                      "excerpt": clip(strip_tags(desc)), "category": feed["category"],
                      "canada_only": feed.get("canada_only", False), "google": bool(feed.get("google")), "filter": bool(feed.get("google") or feed.get("filter"))})
    print(f"  ok   {feed['name']}: {len(items)}")
    return feed, items

def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()

def main():
    feeds = json.loads((ROOT / "feeds.json").read_text())["feeds"]
    print(f"Fetching {len(feeds)} feeds…")
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(fetch, feeds))
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    now = datetime.now(timezone.utc)
    seen, seen_sets, items = set(), [], []
    for _, batch in results:
        for it in batch:
            if it["date"] < cutoff or it["date"] > now + timedelta(days=1):
                continue
            blob = f"{it['title']} {it['excerpt']} {it['source']}"
            if EXCLUDE_RE.search(it["title"]):
                continue
            if it["filter"] and not SCREEN_RE.search(it["title"]):
                continue
            if it["google"] and not CANADA_RE.search(blob):
                continue
            is_ca = it["category"] == "canada" or bool(CANADA_RE.search(blob))
            if it["canada_only"] and not (CANADA_RE.search(blob) and POST_RE.search(blob)):
                continue
            key = norm(it["title"])
            words = set(w for w in key.split() if len(w) > 3)
            if key in seen or any(len(words & s) >= 0.6 * max(len(words), len(s), 1) for s in seen_sets):
                continue
            seen.add(key)
            seen_sets.append(words)
            it["canada"] = is_ca
            if it["category"] in ("picture", "gear", "vfx"):
                if AUDIO_RE.search(it["title"]): it["category"] = "audio"
                elif VFX_RE.search(it["title"]): it["category"] = "vfx"
            items.append(it)
    items.sort(key=lambda i: i["date"], reverse=True)
    items = items[:MAX_ITEMS]
    sources = sorted({i["source"] for i in items})
    print(f"{len(items)} stories from {len(sources)} sources")

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(render(items, sources, now), encoding="utf-8")
    (OUT / "feed.xml").write_text(rss(items, now), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'<url><loc>{SITE_URL}/</loc><lastmod>{now.date()}</lastmod><changefreq>hourly</changefreq></url></urlset>')
    (OUT / "CNAME").write_text("postproductioncanada.ca\n")
    (OUT / "stories.json").write_text(json.dumps(
        [{**i, "date": i["date"].isoformat()} for i in items], ensure_ascii=False, indent=1))

def esc(s): return html.escape(s, quote=True)

CATS = {"canada": ("🍁", "Canada"), "picture": ("🎞️", "Picture & Editing"), "audio": ("🎧", "Audio"),
        "vfx": ("✨", "VFX & Animation"), "gear": ("🎥", "Gear & Software"), "business": ("💼", "Business & Unions")}
AUDIO_RE = re.compile(r"\b(audio|sound|mix(ing|er)?|microphones?|mic|dolby|atmos|loudness|podcast\w*|music|dialogue|foley|"
                      r"adr|dubbing|spatial|ambisonic|headphones?|speakers?|pro tools|reaper|ableton|aes)\b", re.I)
VFX_RE = re.compile(r"\b(vfx|visual effects|animat\w+|composit\w+|nuke|houdini|unreal|cgi|3d|motion graphics|"
                    r"after effects|maya|blender|virtual production|volume|mocap|pixar|dreamworks|weta|ilm)\b", re.I)

def card(i):
    cats = []
    if i["canada"]: cats.append("canada")
    cats.append(i["category"])
    iso = i["date"].isoformat()
    em, lab = CATS[i["category"]]
    chip = f'<span class="chip c-{i["category"]}">{em} {lab}</span>'
    if i["canada"] and i["category"] != "canada":
        chip += '<span class="chip c-canada">🍁</span>'
    ex = f'<p class="ex">{esc(i["excerpt"])}</p>' if i["excerpt"] else ""
    return (f'<article class="card k-{i["category"]}" data-cats="{" ".join(sorted(set(cats)))}" data-t="{esc(norm(i["title"] + " " + i["source"]))}">'
            f'<div class="chips">{chip}</div><div class="meta"><span class="src">{esc(i["source"])}</span>'
            f'<span class="dot">·</span><time datetime="{iso}">{iso[:10]}</time></div>'
            f'<h3><a href="{esc(i["url"])}" target="_blank" rel="noopener">{esc(i["title"])}</a></h3>{ex}</article>')

def render(items, sources, now):
    cards = "\n".join(card(i) for i in items)
    counts = {k: sum(1 for i in items if (k == "all") or (k == "canada" and i["canada"]) or i["category"] == k)
              for k in ["all", "canada", "picture", "audio", "vfx", "gear", "business"]}
    updated = now.strftime("%Y-%m-%d %H:%M UTC")
    tabs = [("all", "🎬 All")] + [(k, f"{e} {l}") for k, (e, l) in CATS.items()]
    tabhtml = "".join(f'<button class="tab{" on" if k=="all" else ""}" data-f="{k}">{l} <i>{counts[k]}</i></button>' for k, l in tabs)
    return TEMPLATE.replace("{{CARDS}}", cards).replace("{{TABS}}", tabhtml)\
        .replace("{{UPDATED}}", updated).replace("{{UPDATED_ISO}}", now.isoformat())\
        .replace("{{NSOURCES}}", str(len(sources))).replace("{{NSTORIES}}", str(len(items)))\
        .replace("{{SOURCES}}", " · ".join(esc(s) for s in sources)).replace("{{SITE}}", SITE_URL)

def rss(items, now):
    out = [f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Post Production Canada</title>'
           f'<link>{SITE_URL}</link><description>Latest Canadian post-production, VFX and screen-industry news.</description>']
    for i in items[:50]:
        out.append(f'<item><title>{esc(i["title"])}</title><link>{esc(i["url"])}</link><guid>{esc(i["url"])}</guid>'
                   f'<source url="{SITE_URL}">{esc(i["source"])}</source>'
                   f'<pubDate>{i["date"].strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate></item>')
    out.append("</channel></rss>")
    return "".join(out)

TEMPLATE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Post Production Canada — the latest news in one place</title>
<meta name="description" content="Every day's Canadian post-production, editing, VFX, sound and screen-industry news, gathered from across Canada and the world in one free feed.">
<link rel="canonical" href="{{SITE}}/">
<link rel="alternate" type="application/rss+xml" title="Post Production Canada" href="/feed.xml">
<meta property="og:title" content="Post Production Canada">
<meta property="og:description" content="The latest Canadian post-production, VFX and screen-industry news, all in one place.">
<meta property="og:url" content="{{SITE}}/">
<meta name="theme-color" content="#0f1115">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23d52b1e'/><path d='M38 28l34 22-34 22z' fill='white'/></svg>">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
:root[data-theme=dark]{--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}
.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em;font-size:20px;text-decoration:none}
.logo{width:30px;height:30px;border-radius:8px;background:var(--red);display:grid;place-items:center}
.logo svg{width:14px;height:14px;fill:#fff;margin-left:2px}
.brand b{color:var(--red)}
.tools{display:flex;gap:8px;align-items:center}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;cursor:pointer;text-decoration:none}
.hero{padding:34px 0 18px}
.hero h1{font-size:clamp(28px,5vw,46px);line-height:1.08;letter-spacing:-.03em;margin:0 0 10px;max-width:16em}
.hero h1 em{font-style:normal;color:var(--red)}
.hero p{color:var(--mute);margin:0;max-width:40em}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 0}
.bar .wrap{display:flex;flex-direction:column;gap:10px}
.tabs{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
.tab{white-space:nowrap;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:7px 14px;font-size:14px;cursor:pointer}
.tab i{font-style:normal;color:var(--mute);margin-left:4px;font-size:12px}
.tab.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.tab.on i{color:inherit;opacity:.7}
#q{width:100%;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:10px;padding:10px 14px;font-size:15px}
main{padding:20px 0 40px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:6px}
.card:hover{border-color:var(--red)}
.k-canada{--c:var(--ink)}.k-picture{--c:var(--red)}.k-audio{--c:#2f7de1}.k-vfx{--c:#12a37f}.k-gear{--c:#e0900b}.k-business{--c:#8a4fe0}
.card{border-top:3px solid var(--c,var(--line))}
.chips{display:flex;gap:6px;margin-bottom:2px}
.chip{font-size:11.5px;font-weight:700;letter-spacing:.02em;padding:2px 9px;border-radius:999px;background:color-mix(in srgb,var(--c) 14%,transparent);color:var(--c)}
.chip.c-canada{--c:var(--ink)}.chip.c-picture{--c:var(--red)}.chip.c-audio{--c:#2f7de1}.chip.c-vfx{--c:#12a37f}.chip.c-gear{--c:#e0900b}.chip.c-business{--c:#8a4fe0}
.meta{font-size:12.5px;color:var(--mute);display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.src{font-weight:700;color:var(--ink)}
.flag{font-size:13px}
.card h3{margin:0;font-size:17px;line-height:1.3;letter-spacing:-.01em}
.card h3 a{text-decoration:none}
.card h3 a:hover{text-decoration:underline}
.ex{margin:0;color:var(--mute);font-size:14px}
.empty{display:none;text-align:center;color:var(--mute);padding:50px 0}
footer{border-top:1px solid var(--line);padding:26px 0 40px;color:var(--mute);font-size:13px}
footer p{margin:0 0 8px;max-width:60em}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo"><svg viewBox="0 0 10 10"><path d="M0 0l10 5-10 5z"/></svg></span>Post Production <b>Canada</b></a>
  <div class="tools"><a class="btn" href="/feed.xml">RSS</a><button class="btn" id="theme" aria-label="Toggle theme">◐</button></div>
</div></header>

<section class="hero"><div class="wrap">
  <h1>All of Canada's post-production news, <em>in one place.</em></h1>
  <p>Editing, colour, sound, VFX, animation and the business behind them — gathered from {{NSOURCES}} sources, updated every few hours. Free, always.</p>
</div></section>

<div class="bar"><div class="wrap">
  <div class="tabs" id="tabs">{{TABS}}</div>
  <input id="q" type="search" placeholder="Search headlines — Resolve, Avid, Telefilm, Vancouver, tax credit…" aria-label="Search stories">
</div></div>

<main><div class="wrap">
  <div class="grid" id="grid">
{{CARDS}}
  </div>
  <div class="empty" id="empty">Nothing matches that. Try a different filter or search.</div>
</div></main>

<footer><div class="wrap">
  <p>Updated <time datetime="{{UPDATED_ISO}}">{{UPDATED}}</time> · {{NSTORIES}} stories from the last three weeks.</p>
  <p>Post Production Canada shows headlines and short excerpts only. Every story links to its original publisher — go read them. Sources: {{SOURCES}}.</p>
  <p>Run by DayDream Productions Inc. Want your outlet, guild or studio newsfeed added? Get in touch.</p>
</div></footer>

<script>
(function(){
  var tabs=document.querySelectorAll('.tab'),cards=[].slice.call(document.querySelectorAll('.card')),q=document.getElementById('q'),empty=document.getElementById('empty'),f='all';
  function apply(){
    var s=q.value.toLowerCase().trim(),n=0;
    cards.forEach(function(c){
      var ok=(f==='all'||c.dataset.cats.split(' ').indexOf(f)>-1)&&(!s||c.dataset.t.indexOf(s)>-1);
      c.style.display=ok?'':'none'; if(ok)n++;
    });
    empty.style.display=n?'none':'block';
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){
    tabs.forEach(function(x){x.classList.remove('on')});t.classList.add('on');f=t.dataset.f;apply();
  })});
  q.addEventListener('input',apply);
  cards.forEach(function(c){var t=c.querySelector('time');var d=new Date(t.getAttribute('datetime')),diff=(Date.now()-d)/36e5;
    t.textContent=diff<1?'just now':diff<24?Math.floor(diff)+'h ago':diff<48?'yesterday':d.toLocaleDateString('en-CA',{month:'short',day:'numeric'});});
  var r=document.documentElement;
  try{var s=localStorage.getItem('theme');if(s)r.setAttribute('data-theme',s)}catch(e){}
  document.getElementById('theme').addEventListener('click',function(){
    var dark=r.getAttribute('data-theme')?r.getAttribute('data-theme')==='dark':matchMedia('(prefers-color-scheme:dark)').matches;
    var n=dark?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}
  });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
