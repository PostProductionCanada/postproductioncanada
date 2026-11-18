#!/usr/bin/env python3
"""Post Production Canada - fetch feeds, build a static site into ./public.

Python 3 standard library only. Run:  python3 build.py
Headlines + short excerpts only; every item links back to the original publisher.
"""
import html, json, os, re, sys, time, logo
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
MAX_ITEMS = 600
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
        data = None
        for attempt in range(3):
            try:
                with urlopen(req, timeout=20) as r:
                    data = r.read()
                break
            except Exception as err:
                if attempt == 2 or "429" not in str(err):
                    raise
                time.sleep(4 * (attempt + 1) + (hash(feed["url"]) % 5))
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
                      "canada_only": feed.get("canada_only", False), "google": bool(feed.get("google")), "intl": bool(feed.get("intl")), "filter": bool(feed.get("google") or feed.get("filter")), "require": feed.get("require")})
    print(f"  ok   {feed['name']}: {len(items)}")
    return feed, items

ARCHIVE = ROOT / "data" / "archive.json"


def load_archive():
    try:
        rows = json.loads(ARCHIVE.read_text())
    except Exception:
        return []
    out = []
    for r in rows:
        try:
            r["date"] = datetime.fromisoformat(r["date"])
            out.append(r)
        except Exception:
            continue
    return out


def save_archive(items):
    ARCHIVE.parent.mkdir(exist_ok=True)
    ARCHIVE.write_text(json.dumps([{**i, "date": i["date"].isoformat()} for i in items],
                                  ensure_ascii=False, separators=(",", ":")))


_PROTECT = re.compile(r"(<head\b.*?</head>|<script\b.*?</script>|<style\b.*?</style>)", re.S | re.I)
_PP = re.compile(r"(?<![\w/.\-])([Pp]ost-production)(?![\w/\-])")


def nobreak(html_text):
    """Keep 'post-production' from splitting across lines, in page text only (never in attributes, scripts or URLs)."""
    out = []
    for part in _PROTECT.split(html_text):
        if _PROTECT.fullmatch(part or ""):
            out.append(part)
            continue
        out.append(re.sub(r"(>)([^<]+)(<)", lambda m: m.group(1) + _PP.sub(r'<span class="nb">\1</span>', m.group(2)) + m.group(3), part))
    return "".join(out)


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()

def main():
    try:
        import refresh_filmincanada
        refresh_filmincanada.main()
    except Exception as err:
        print("filmincanada step skipped:", err, file=sys.stderr)
    feeds = json.loads((ROOT / "feeds.json").read_text())["feeds"]
    print(f"Fetching {len(feeds)} feeds…")
    with ThreadPoolExecutor(max_workers=6) as ex:
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
            req = it.get("require")
            if req:
                pats = req if isinstance(req, list) else [req]
                if not all(re.search(pt, it["title"] + " " + it["excerpt"], re.I) for pt in pats):
                    continue
            if it["filter"] and not SCREEN_RE.search(it["title"]):
                continue
            if it["google"] and not it["intl"] and not CANADA_RE.search(blob):
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
            blob2 = it["title"] + " " + it["excerpt"]
            it["ai"] = bool(AI_CS.search(blob2) or AI_CI.search(blob2))
            it["cce"] = bool(CCE_RE.search(blob2 + " " + it["source"] + " " + it["url"]))
            it["status"] = it["category"] in ("business", "canada") and bool(STATUS_RE.search(blob2))
            it["prov"] = [k for k, r in PROV_RE.items() if r.search(blob2)]
            if it["category"] in ("picture", "gear", "vfx"):
                if AUDIO_RE.search(it["title"]): it["category"] = "audio"
                elif VFX_RE.search(it["title"]): it["category"] = "vfx"
            items.append(it)
    # remember stories between builds so the window really is MAX_AGE_DAYS, not just what feeds show today
    fresh = {i["url"] for i in items}
    for a in load_archive():
        if a["url"] in fresh or a["date"] < cutoff or a["date"] > now + timedelta(days=1):
            continue
        key = norm(a["title"])
        if key in seen:
            continue
        seen.add(key)
        items.append(a)
    items.sort(key=lambda i: i["date"], reverse=True)
    if os.environ.get("GITHUB_ACTIONS"):
        save_archive(items)
    items = items[:MAX_ITEMS]
    sources = sorted({i["source"] for i in items})
    print(f"{len(items)} stories from {len(sources)} sources")

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(render(items, sources, now), encoding="utf-8")
    (OUT / "feed.xml").write_text(rss(items, now), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'<url><loc>{SITE_URL}/</loc><lastmod>{now.date()}</lastmod><changefreq>hourly</changefreq></url><url><loc>{SITE_URL}/unions.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/buzz.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/editors.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/status-of-the-artist.html</loc><lastmod>{now.date()}</lastmod></url></urlset>')
    import statuspage
    lf = re.search(r'points="([^"]+)"', (ROOT / "art" / "flag.svg").read_text()).group(1)
    from urllib.parse import quote as _q
    _leaf = logo.inline()
    _fav = logo.favicon()
    (OUT / "status-of-the-artist.html").write_text(statuspage.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import editors, shutil
    cce_items = sorted(fetch({"name": "CCE", "url": "https://cceditors.ca/feed/", "category": "picture"})[1], key=lambda i: i["date"], reverse=True)
    vpa_items = sorted(fetch({"name": "VPA", "url": "https://vancouverpostalliance.com/feed/", "category": "canada"})[1], key=lambda i: i["date"], reverse=True)
    import privacy
    _cfg = json.loads((ROOT / "site.json").read_text())
    (OUT / "privacy.html").write_text(privacy.render(_leaf, _fav, now.strftime("%Y-%m-%d"), _cfg), encoding="utf-8")
    import unions
    (OUT / "unions.html").write_text(unions.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import originals
    _arts = originals.render_all(_leaf, _fav, now.strftime("%Y-%m-%d"), _cfg, OUT, ROOT)
    import buzz
    (OUT / "buzz.html").write_text(buzz.render(_leaf, _fav, now.strftime("%Y-%m-%d"), now), encoding="utf-8")
    import base64 as _b64
    _logo = "data:image/jpeg;base64," + _b64.b64encode((ROOT / "art" / "cce-logo.jpg").read_bytes()).decode()
    (OUT / "editors.html").write_text(editors.render(_leaf, _fav, now.strftime("%Y-%m-%d"), cce_items, vpa_items, [i for i in items if i["category"] == "audio"][:8]).replace('src="cce-logo.jpg"', 'src="' + _logo + '"'), encoding="utf-8")
    shutil.copy(ROOT / "art" / "cce-logo.jpg", OUT / "cce-logo.jpg")
    (OUT / "flag.svg").write_text((ROOT / "art" / "flag.svg").read_text())
    (OUT / "build.json").write_text(json.dumps({"built": now.isoformat()}))
    tok = (_cfg.get("analytics_token") or "").strip()
    beacon = ("<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
              "data-cf-beacon='{\"token\": \"" + tok + "\"}'></script>") if tok else ""
    for f in list(OUT.glob("*.html")) + list(OUT.glob("originals/*.html")):
        t = nobreak(f.read_text(encoding="utf-8"))
        if beacon and "cloudflareinsights" not in t:
            t = t.replace("</head>", beacon + "</head>", 1)
        f.write_text(t, encoding="utf-8")
    (OUT / "CNAME").write_text("postproductioncanada.ca\n")
    (OUT / "stories.json").write_text(json.dumps(
        [{**i, "date": i["date"].isoformat()} for i in items], ensure_ascii=False, indent=1))

def esc(s): return html.escape(s, quote=True)

CATS = {"canada": ("🍁", "Canada"), "picture": ("🎞️", "Picture & Editing"), "audio": ("🎧", "Audio"),
        "vfx": ("✨", "VFX & Animation"), "gear": ("🎥", "Gear & Software"), "business": ("💼", "Business & Unions"),
        "ai": ("🤖", "AI Filmmaking"),
        "cce": ("✂️", "CCE"),
        "status": ("⚖️", "Status of the Artist")}
CCE_RE = re.compile(r"\bCCE\b|Canadian Cinema Editors|cceditors\.ca")
AI_CS = re.compile(r"\bAI\b|\bA\.I\.|\bGen-?AI\b|\bLLMs?\b")
AI_CI = re.compile(r"(artificial intelligence|generative|machine learning|\brunway\b|\bsora\b|\bveo\b|\bkling\b|midjourney|"
                   r"firefly|\bluma\b|\bpika\b|hailuo|seedance|comfyui|stable diffusion|text[- ]to[- ]video|image[- ]to[- ]video|"
                   r"synthetic (actors?|media|performers?)|deepfakes?|chatgpt|\bgemini\b|\bwan 2|\bflux\b|diffusion model|"
                   r"neural|ai[- ](generated|film\w*|actors?|video|tools?|studio|native))", re.I)
STATUS_RE = re.compile(r"(status of the artist|collective agreements?|collective bargaining|bargaining|ratif\\w+|strikes?|lockout|"
                       r"labou?r (board|code|standards|law|dispute|action|shortage)|freelanc\\w+|independent contractors?|"
                       r"self[- ]employed|minimum wage|artists?['’]? (rights|fees|status)|union (drive|vote|contract|deal|certif\\w+)|"
                       r"pay (rate|scale|equity)|residuals|royalt\\w+|layoffs?|job losses|working conditions)", re.I)
PROVS = {"BC": r"vancouver|british columbia|burnaby|victoria,? b|creative bc|\bB\.C\.|\bBC\b",
         "AB": r"calgary|edmonton|alberta|banff",
         "SK": r"saskatchewan|regina|saskatoon",
         "MB": r"winnipeg|manitoba",
         "ON": r"toronto|ontario|ottawa|hamilton|omdc|\bGTA\b|london, ont",
         "QC": r"montr[eé]al|qu[eé]bec|sodec|laval|gatineau",
         "ATL": r"halifax|nova scotia|new brunswick|moncton|fredericton|newfoundland|st\. john|prince edward|charlottetown|atlantic canada",
         "TERR": r"yukon|nunavut|northwest territories|whitehorse|yellowknife"}
PROV_RE = {k: re.compile(v, re.I if k != "BC" else 0) for k, v in PROVS.items()}
PROV_RE["BC"] = re.compile(PROVS["BC"], re.I)
PROV_LABEL = {"BC": "British Columbia", "AB": "Alberta", "SK": "Saskatchewan", "MB": "Manitoba", "ON": "Ontario",
              "QC": "Québec", "ATL": "Atlantic Canada", "TERR": "Territories"}
AUDIO_RE = re.compile(r"\b(audio|sound|mix(ing|er)?|microphones?|mic|dolby|atmos|loudness|podcast\w*|music|dialogue|foley|"
                      r"adr|dubbing|spatial|ambisonic|headphones?|speakers?|pro tools|reaper|ableton|aes)\b", re.I)
VFX_RE = re.compile(r"\b(vfx|visual effects|animat\w+|composit\w+|nuke|houdini|unreal|cgi|3d|motion graphics|"
                    r"after effects|maya|blender|virtual production|volume|mocap|pixar|dreamworks|weta|ilm)\b", re.I)

def card(i):
    cats = []
    if i["canada"]: cats.append("canada")
    cats.append(i["category"])
    if i["status"]: cats.append("status")
    if i["ai"]: cats.append("ai")
    if i["cce"]: cats.append("cce")
    iso = i["date"].isoformat()
    em, lab = CATS[i["category"]]
    chip = f'<span class="chip c-{i["category"]}">{em} {lab}</span>'
    if i["canada"] and i["category"] != "canada":
        chip += '<span class="chip c-canada">🍁</span>'
    if i["ai"]:
        chip += '<span class="chip c-ai">🤖 AI</span>'
    if i["cce"]:
        chip += '<span class="chip c-cce" title="Canadian Cinema Editors">CCE</span>'
    if i["status"]:
        chip += '<span class="chip c-status">⚖️ Status</span>'
    for k in i["prov"]:
        chip += f'<span class="chip c-prov">📍 {k}</span>'
    ex = f'<p class="ex">{esc(i["excerpt"])}</p>' if i["excerpt"] else ""
    return (f'<article class="card k-{i["category"]}" data-cats="{" ".join(sorted(set(cats)))}" data-prov="{" ".join(i["prov"])}" data-t="{esc(norm(i["title"] + " " + i["source"]))}">'
            f'<div class="chips">{chip}</div><div class="meta"><span class="src">{esc(i["source"])}</span>'
            f'<span class="dot">·</span><time datetime="{iso}">{iso[:10]}</time></div>'
            f'<h3><a href="{esc(i["url"])}" target="_blank" rel="noopener">{esc(i["title"])}</a></h3>{ex}</article>')

def load_picks(now):
    try:
        raw = json.loads((ROOT / "curated.json").read_text()).get("picks", [])
    except Exception:
        return []
    out = []
    for r in raw:
        d = parse_date(r.get("date", ""))
        if not d or not r.get("url") or not r.get("title"):
            continue
        if now - d > timedelta(days=int(r.get("expires_days", 30))):
            continue
        out.append({**r, "dt": d})
    out.sort(key=lambda r: r["dt"], reverse=True)
    return out[:8]

BODY_SECTIONS = {
    "CMPA": ("📢 Latest from the CMPA", "https://cmpa.ca/", "cmpa.ca", "Press releases from the Canadian Media Producers Association."),
    "LinkedIn": ("💼 Industry voices on LinkedIn", "https://www.linkedin.com/", "linkedin.com", "Articles from industry voices on LinkedIn. LinkedIn blocks automated readers, so these are added by hand and some show no date."),
    "Avid": ("🎛️ Latest from Avid", "https://www.avid.com/press-room", "avid.com", "Press releases and release notes from Avid, maker of Media Composer and Pro Tools."),
}


def _body_card(src, r):
    by = '<span class="dot">·</span>by ' + esc(r["by"]) if r.get("by") else ""
    when = ""
    if r.get("dt"):
        when = '<span class="dot">·</span><time datetime="' + r["dt"].isoformat() + '">' + str(r["dt"].date()) + "</time>"
    note = '<p class="why">' + esc(r["note"]) + "</p>" if r.get("note") else ""
    return ('<article class="pick body"><div class="meta"><span class="src">' + esc(src) + "</span>" + by + when + "</div>"
            '<h3><a href="' + esc(r["url"]) + '" target="_blank" rel="noopener">' + esc(r["title"]) + "</a></h3>" + note + "</article>")


def bodies_html(now):
    try:
        raw = json.loads((ROOT / "curated.json").read_text()).get("bodies", [])
    except Exception:
        return ""
    groups = {}
    for r in raw:
        d = parse_date(r.get("date", ""))
        if d is None or now - d <= timedelta(days=int(r.get("expires_days", 75))):
            groups.setdefault(r.get("source", "CMPA"), []).append({**r, "dt": d})
    out = []
    for src, (head, url, dom, blurb) in BODY_SECTIONS.items():
        rows = sorted(groups.get(src, []), key=lambda r: r["dt"] or datetime(1970, 1, 1, tzinfo=timezone.utc), reverse=True)[:5]
        if not rows:
            continue
        cards = "".join(_body_card(src, r) for r in rows)
        out.append(f'<section class="picks" aria-label="{esc(head)}"><h2>{head}</h2><div class="pgrid">{cards}</div>'
                   f'<p class="note" style="margin-top:8px">{esc(blurb)} From <a href="{esc(url)}" target="_blank" rel="noopener">{esc(dom)}</a>. This list is updated by hand.</p></section>')
    return "\n".join(out)


def picks_html(picks):
    if not picks:
        return ""
    cards = "".join(
        f'<article class="pick"><div class="meta"><span class="src">{esc(r["source"])}</span><span class="dot">·</span>'
        f'<time datetime="{r["dt"].isoformat()}">{r["dt"].date()}</time></div>'
        f'<h3><a href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(r["title"])}</a></h3>'
        + (f'<p class="why"><b>Why it matters:</b> {esc(r["note"])}</p>' if r.get("note") else "") + '</article>'
        for r in picks)
    return f'<section class="picks" aria-label="Editor\'s picks"><h2>⭐ Editor\'s Picks</h2><div class="pgrid">{cards}</div></section>'

def render(items, sources, now):
    picks = load_picks(now)
    ptitles = {norm(r["title"]) for r in picks}
    items = [i for i in items if norm(i["title"]) not in ptitles]
    cards = "\n".join(card(i) for i in items)
    counts = {k: sum(1 for i in items if (k == "all") or (k == "canada" and i["canada"]) or (k == "status" and i["status"]) or (k == "ai" and i["ai"]) or (k == "cce" and i["cce"]) or i["category"] == k)
              for k in ["all"] + list(CATS)}
    updated = now.strftime("%Y-%m-%d %H:%M UTC")
    tabs = [("all", "🎬 All")] + [(k, f"{e} {l}") for k, (e, l) in CATS.items()]
    tabhtml = "".join(f'<button class="tab{" on" if k=="all" else ""}" data-f="{k}">{l} <i>{counts[k]}</i></button>' for k, l in tabs)
    popts = "".join(f'<option value="{k}">{PROV_LABEL[k]} ({sum(1 for i in items if k in i["prov"])})</option>' for k in PROV_LABEL)
    cfg = json.loads((ROOT / "site.json").read_text())
    sub, subbtn = "", ""
    if cfg.get("subscribe_embed_html") or cfg.get("subscribe_form_action"):
        subbtn = '<a class="btn" href="#subscribe">Subscribe</a>'
        inner = cfg.get("subscribe_embed_html") or (
            f'<form method="post" action="{esc(cfg["subscribe_form_action"])}" target="_blank" class="sf">'
            '<input type="email" name="email" placeholder="you@email.com" required aria-label="Email address">'
            '<button class="btn go" type="submit">Subscribe free</button></form>')
        sub = ('<section id="subscribe" class="subbox"><div class="wrap"><h2>📬 Get the Canadian post news in your inbox</h2>'
               '<p>Free updates, plus original articles and interviews with Canada\'s editors, colourists, sound mixers and VFX artists. '
               'Unsubscribe any time.</p>' + inner +
               '<p class="consent">By subscribing you agree to receive the Post Production Canada newsletter by email. '
               'Unsubscribe any time. <a href="privacy.html">Privacy</a></p></div></section>')
    contact = (f'<p>Want your outlet, guild or studio added, or have a story tip? '
               f'<a href="mailto:{esc(cfg["contact_email"])}">{esc(cfg["contact_email"])}</a></p>') if cfg.get("contact_email") else ""
    import base64
    from urllib.parse import quote
    poly = re.search(r'points="([^"]+)"', (ROOT / "art" / "flag.svg").read_text()).group(1)
    leaf = logo.inline()
    fav_svg = None
    favicon = logo.favicon()
    flag = "data:image/svg+xml;base64," + base64.b64encode((ROOT / "art" / "flag.svg").read_bytes()).decode()
    _cl = "data:image/jpeg;base64," + base64.b64encode((ROOT / "art" / "cce-logo-small.jpg").read_bytes()).decode()
    import originals as _o
    _orig = '<a class="btn" href="originals.html">Originals</a>' if _o.count_published(ROOT) else ""
    _today = now.date()
    _counts = [0] * 21
    for _i in items:
        _k = (_today - _i["date"].date()).days
        if 0 <= _k < 21:
            _counts[20 - _k] += 1
    _mx = max(_counts) or 1
    _bars = "".join('<i style="height:%d%%" title="%s: %d stories"%s></i>' % (
        max(10, round(_c / _mx * 100)), (now - timedelta(days=20 - _n)).strftime("%b %-d"), _c, ' class="today"' if _n == 20 else "")
        for _n, _c in enumerate(_counts))
    return TEMPLATE.replace("{{BARS}}", _bars).replace("{{TODAYSTR}}", now.strftime("%A, %b %-d, %Y")).replace("{{BODIES}}", bodies_html(now)).replace("{{ORIG}}", _orig).replace("{{CCELOGO}}", _cl).replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{PICKS}}", picks_html(picks)).replace("{{FLAG}}", flag).replace("{{PROVOPTS}}", popts).replace("{{SUBSCRIBE}}", sub).replace("{{SUBBTN}}", subbtn).replace("{{CONTACT}}", contact)\
        .replace("{{CARDS}}", cards).replace("{{TABS}}", tabhtml)\
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
<link rel="icon" href="{{FAVICON}}">
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
.logo{width:30px;height:30px;display:grid;place-items:center}
.logo svg{width:28px;height:28px}
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
.subbox{background:var(--ink);color:var(--bg);padding:26px 0}.subbox .consent{font-size:12.5px;margin:10px 0 0;opacity:.75}.subbox .consent a{color:inherit}
.subbox h2{margin:0 0 6px;font-size:22px}.subbox p{margin:0 0 14px;opacity:.8;max-width:42em}.sf{display:flex;gap:8px;flex-wrap:wrap}.sf input{flex:1;min-width:220px;border:0;border-radius:10px;padding:11px 14px;font-size:15px}.btn.go{background:var(--red);color:#fff;border-color:var(--red);font-weight:700;padding:10px 18px}
.chip.c-cce{background:#fff url({{CCELOGO}}) center/contain no-repeat;border:1px solid var(--line);width:96px;height:28px;padding:0;color:transparent;overflow:hidden}
.chip.c-ai{--c:#0e8fb0}.k-ai{--c:#0e8fb0}.chip.c-status{--c:#8a4fe0}.chip.c-prov{--c:var(--mute);font-weight:600}.k-status{--c:#8a4fe0}
#prov{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:10px;padding:9px 12px;font-size:14px}
.chips{flex-wrap:wrap}
.herogrid{display:grid;grid-template-columns:1.25fr .75fr;gap:28px;align-items:center}.heroart{width:100%;height:auto;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
@media (max-width:760px){.herogrid{grid-template-columns:1fr}.heroart{max-width:380px}}
.picks{margin-bottom:26px}.picks h2{margin:0 0 10px;font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}
.pick{background:var(--panel);border:1px solid var(--line);border-left:4px solid #e0a100;border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:6px}
.pick.body{border-left-color:var(--red)}
.pick h3{margin:0;font-size:18px;line-height:1.3}.pick h3 a{text-decoration:none}.pick h3 a:hover{text-decoration:underline}
.why{margin:0;font-size:14px;color:var(--mute)}.why b{color:var(--ink)}
@media (max-width:640px){.top{flex-wrap:wrap;gap:10px}.brand{white-space:nowrap;font-size:18px}.tools{width:100%;flex-wrap:wrap}.btn{white-space:nowrap}}
.res{border-top:1px solid var(--line);padding:26px 0 6px}.res h2{margin:0 0 8px;font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}.res ul{margin:0;padding-left:18px;max-width:60em}.res li{margin:6px 0;font-size:14.5px}.res a{color:var(--red)}
.nb{white-space:nowrap}
.brand{white-space:nowrap}.btn{white-space:nowrap}.top{flex-wrap:wrap;gap:10px}.tools{flex-wrap:wrap}
.deck{padding:4px 0 18px}
.synth{position:relative;display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:12px 18px;align-items:end;background:linear-gradient(#1c1e24,#101216);color:#ffb347;border:1px solid #2c2f36;border-radius:14px;padding:16px 28px;box-shadow:inset 0 0 0 2px #0007,0 8px 22px rgba(0,0,0,.18);font-family:ui-monospace,Menlo,Consolas,monospace}
.synth::before,.synth::after{content:"";position:absolute;top:0;bottom:0;width:12px;background:repeating-linear-gradient(90deg,#6b3f1d,#8d5c2a 3px,#6b3f1d 6px);border-radius:14px 0 0 14px}
.synth::before{left:0}.synth::after{right:0;border-radius:0 14px 14px 0}
.cell .lbl{font-size:10.5px;letter-spacing:.16em;color:#c9a66b;margin-bottom:4px}
.lcd{font-size:34px;line-height:1;font-weight:700;color:#ff4d3a;text-shadow:0 0 10px rgba(255,77,58,.55);letter-spacing:.04em;background:#0b0c0e;border:1px solid #000;border-radius:8px;padding:8px 12px;box-shadow:inset 0 0 12px #000}
.lcd.sm{font-size:16px;color:#ffb347;text-shadow:0 0 8px rgba(255,179,71,.4);padding:12px 12px}
.cell.wide{grid-column:1/-1}.cell.wide .lbl{display:flex;justify-content:space-between;flex-wrap:wrap;gap:2px 10px}
.now{color:#ff4d3a;animation:blink 1s steps(2) infinite}
.meter{display:flex;align-items:flex-end;gap:3px;height:42px;background:#0b0c0e;border:1px solid #000;border-radius:8px;padding:6px 8px;box-shadow:inset 0 0 12px #000}
.meter i{flex:1;background:linear-gradient(#ffb347,#c9701b);border-radius:2px;min-height:3px;opacity:.8}
.meter i.today{background:linear-gradient(#ff6b57,#ff4d3a);opacity:1;animation:pulse 1.4s ease-in-out infinite}
.steps{grid-column:1/-1;display:flex;gap:7px;justify-content:center}
.steps b{width:14px;height:8px;border-radius:2px;background:#2a2d34;box-shadow:inset 0 0 2px #000}
.steps b.on{background:#ff4d3a;box-shadow:0 0 8px #ff4d3a}
@keyframes blink{50%{opacity:.25}}@keyframes pulse{50%{opacity:.55}}
@media (prefers-reduced-motion:reduce){.now,.meter i.today{animation:none}}
@media (max-width:720px){.synth{grid-template-columns:1fr 1fr;padding:14px 22px}.cell:nth-child(3){grid-column:1/-1}.lcd{font-size:28px}}
footer{border-top:1px solid var(--line);padding:26px 0 40px;color:var(--mute);font-size:13px}
footer p{margin:0 0 8px;max-width:60em}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a>
  <div class="tools">{{SUBBTN}}{{ORIG}}<a class="btn" href="unions.html">Union Map</a><a class="btn" href="buzz.html">Post Buzz</a><a class="btn" href="editors.html">Editors</a><a class="btn" href="status-of-the-artist.html">Status &amp; Tax Credits</a><a class="btn" href="/feed.xml">RSS</a><button class="btn" id="theme" aria-label="Toggle theme">◐</button></div>
</div></header>

<section class="hero"><div class="wrap herogrid"><div>
  <h1>All of Canada's <span class="nb">post-production</span> news, <em>in one place.</em></h1>
  <p>Editing, colour, sound, VFX, animation and the business behind them — gathered from {{NSOURCES}} sources and updated live every few hours. Original articles coming soon. Free, always.</p>
</div><img class="heroart" src="{{FLAG}}" alt="A Canadian flag built from a clapperboard, light, mixing console, location pin and maple leaf with a play button" width="640" height="340"></div></section>

<section class="deck" aria-label="Update clock"><div class="wrap"><div class="synth">
  <div class="cell"><div class="lbl">TODAY</div><div class="lcd sm" id="today">{{TODAYSTR}}</div></div>
  <div class="cell"><div class="lbl">NEXT UPDATE IN</div><div class="lcd" id="cd">--:--:--</div></div>
  <div class="cell"><div class="lbl">LAST UPDATED</div><div class="lcd sm" id="lu">{{UPDATED}}</div></div>
  <div class="cell wide"><div class="lbl">LAST 21 DAYS <span id="range"></span><span class="now">● NOW</span></div><div class="meter" id="meter">{{BARS}}</div></div>
  <div class="steps" id="steps" aria-hidden="true"><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b></div>
</div></div></section>

<div class="bar"><div class="wrap">
  <div class="tabs" id="tabs">{{TABS}}</div>
  <input id="q" type="search" placeholder="Search headlines — Resolve, Avid, Telefilm, Vancouver, tax credit…" aria-label="Search stories">
  <select id="prov" aria-label="Filter by province"><option value="">📍 All provinces</option>{{PROVOPTS}}</select>
</div></div>

{{SUBSCRIBE}}
<main><div class="wrap">
  {{PICKS}}
  {{BODIES}}
  <div class="grid" id="grid">
{{CARDS}}
  </div>
  <div class="empty" id="empty">Nothing matches that. Try a different filter or search.</div>
</div></main>

<section class="res"><div class="wrap">
  <h2>Resources</h2>
  <ul>
    <li><a href="https://www.productionlist.com/" target="_blank" rel="noopener">Production List</a> — a directory of film and TV productions and companies, including post and VFX houses. Mostly US-focused; contact details are for paying members.</li>
    <li><a href="https://postperspective.com/" target="_blank" rel="noopener">Post Perspective</a> — trade news and features on post-production, VFX, editing, colour and sound. Its stories also appear in the news feed above.</li>
    <li><a href="editors.html">Canadian Cinema Editors</a> — the non-profit association for Canadian picture editors, plus the Vancouver Post Alliance.</li>
    <li><a href="https://filmincanada.com/incentives" target="_blank" rel="noopener">filmincanada.com</a> — film incentives by province and a tracker of productions across Canada.</li>
    <li><a href="https://cmpa.ca/profile" target="_blank" rel="noopener">CMPA Profile</a> — the annual economic report on Canada's screen industry.</li>
    <li><a href="unions.html">Union Map</a> — pick a province to see which unions and guilds cover editors there.</li>
    <li><a href="privacy.html">Privacy</a> — what we collect (almost nothing) and how the newsletter works.</li>
    <li><a href="status-of-the-artist.html">Status of the Artist and tax credits</a> — what the laws mean for editors, with credits by province.</li>
  </ul>
</div></section>
<footer><div class="wrap">
  <p>Updated <time datetime="{{UPDATED_ISO}}">{{UPDATED}}</time> · {{NSTORIES}} stories from the last three weeks.</p>
  <p>Post Production Canada shows headlines and short excerpts only. Every story links to its original publisher — go read them. Sources: {{SOURCES}}.</p>
  {{CONTACT}}
</div></footer>

<script>
(function(){
  var tabs=document.querySelectorAll('.tab'),cards=[].slice.call(document.querySelectorAll('.card')),q=document.getElementById('q'),pv=document.getElementById('prov'),empty=document.getElementById('empty'),f='all';
  function apply(){
    var s=q.value.toLowerCase().trim(),n=0;
    cards.forEach(function(c){
      var ok=(f==='all'||c.dataset.cats.split(' ').indexOf(f)>-1)&&(!s||c.dataset.t.indexOf(s)>-1)&&(!pv.value||c.dataset.prov.split(' ').indexOf(pv.value)>-1);
      c.style.display=ok?'':'none'; if(ok)n++;
    });
    empty.style.display=n?'none':'block';
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){
    tabs.forEach(function(x){x.classList.remove('on')});t.classList.add('on');f=t.dataset.f;apply();try{history.replaceState(null,'',f==='all'?location.pathname:'#'+f)}catch(e){}
  })});
  q.addEventListener('input',apply);pv.addEventListener('change',apply);var h0=location.hash.slice(1);if(h0)tabs.forEach(function(t){if(t.dataset.f===h0)t.click()});
  cards.forEach(function(c){var t=c.querySelector('time');var d=new Date(t.getAttribute('datetime')),diff=(Date.now()-d)/36e5;
    t.textContent=diff<1?'just now':diff<24?Math.floor(diff)+'h ago':diff<48?'yesterday':d.toLocaleDateString('en-CA',{month:'short',day:'numeric'});});
  var r=document.documentElement;
  try{var s=localStorage.getItem('theme');if(s)r.setAttribute('data-theme',s)}catch(e){}
  document.getElementById('theme').addEventListener('click',function(){
    var dark=r.getAttribute('data-theme')?r.getAttribute('data-theme')==='dark':matchMedia('(prefers-color-scheme:dark)').matches;
    var n=dark?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}
  });
})();
(function(){
  var cd=document.getElementById('cd'); if(!cd) return;
  var built=new Date('{{UPDATED_ISO}}'),lu=document.getElementById('lu'),rg=document.getElementById('range'),td=document.getElementById('today'),
      steps=document.querySelectorAll('#steps b'),DAY=864e5,polling=false;
  function pad(n){return n<10?'0'+n:''+n}
  function fmt(d,o){try{return d.toLocaleDateString('en-CA',o)}catch(e){return d.toDateString()}}
  function nextRun(now){var d=new Date(Date.UTC(now.getUTCFullYear(),now.getUTCMonth(),now.getUTCDate(),0,17,0));
    for(var i=0;i<10;i++){var t=new Date(d.getTime()+i*3*36e5);if(t>now)return t}return d}
  try{lu.textContent=built.toLocaleString('en-CA',{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'})}catch(e){}
  function poll(){if(polling)return;polling=true;
    (function go(){fetch('build.json?'+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){
      if(new Date(j.built)>built){location.reload()}else{setTimeout(go,30000)}}).catch(function(){setTimeout(go,60000)})})()}
  function tick(){
    var now=new Date(),t=nextRun(now),diff=t-now,last=new Date(t.getTime()-3*36e5);
    td.textContent=fmt(now,{weekday:'long',month:'short',day:'numeric',year:'numeric'});
    rg.textContent=fmt(new Date(now-21*DAY),{month:'short',day:'numeric'})+' to '+fmt(now,{month:'short',day:'numeric'});
    if(now-last<8*60e3&&built<last){cd.textContent='UPDATING…';poll()}
    else{var s=Math.floor(diff/1000);cd.textContent=pad(Math.floor(s/3600))+':'+pad(Math.floor(s%3600/60))+':'+pad(s%60)}
    var k=now.getSeconds()%12;steps.forEach(function(b,i){b.classList.toggle('on',i===k)});
  }
  tick();setInterval(tick,1000);
  document.querySelectorAll('.card time').forEach(function(t){var d=new Date(t.getAttribute('datetime'));
    if(Date.now()-d>21*DAY){var c=t.closest('.card');if(c)c.style.display='none'}});
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
