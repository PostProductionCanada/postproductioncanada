#!/usr/bin/env python3
"""Post Production Canada - fetch feeds, build a static site into ./public.

Python 3 standard library only. Run:  python3 build.py
Headlines + short excerpts only; every item links back to the original publisher.
"""
import html, json, os, re, sys, time, logo, style
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
            if source.lower() == "playbackonline.ca":
                source = "Playback"
                if title.strip().lower() == "playback":
                    continue
        if not (title and link and date):
            continue
        items.append({"title": title, "url": link, "date": date, "source": source,
                      "excerpt": clip(strip_tags(desc)), "category": feed["category"],
                      "canada_only": feed.get("canada_only", False), "google": bool(feed.get("google")), "intl": bool(feed.get("intl")), "filter": bool((feed.get("google") or feed.get("filter")) and not feed.get("nofilter")), "require": feed.get("require")})
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


LEADER = ('<svg class="leader" viewBox="0 0 40 40" width="26" height="26" aria-hidden="true" style="vertical-align:middle">'
          '<circle cx="20" cy="20" r="17.5" fill="#14161a" stroke="#f6f4ef" stroke-width="2.5"/><circle cx="20" cy="20" r="11" fill="none" stroke="#f6f4ef" stroke-width="1.2"/>'
          '<path d="M2.5 20h35M20 2.5v35" stroke="#f6f4ef" stroke-width="1.2"/><path d="M20 20 L20 4.5 A15.5 15.5 0 0 1 33.4 12.3 Z" fill="#ffb000" opacity=".45"/>'
          '<text x="20" y="26.5" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-weight="900" font-size="19" fill="#ffb000" stroke="#14161a" stroke-width=".8">2</text></svg>')
HOME_FAB = ('<a class="homefab" href="/" title="Back to the home page (the 2 beep)" aria-label="Back to the home page">' + LEADER + '<span>Picture Start</span></a>'
            '<style>.homefab{position:fixed;left:14px;bottom:14px;z-index:60;display:flex;align-items:center;gap:8px;background:#14161a;color:#ffb000!important;'
            'font:800 14px/1 ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;padding:7px 14px 7px 8px;border-radius:999px;'
            'border:2px solid #ffb000;box-shadow:0 4px 14px rgba(0,0,0,.35)}.homefab:hover{background:#000}@media print{.homefab{display:none}}</style>')

GROUPS = [
    ("📰 News", [("buzz.html", "🎬 Post Buzz"), ("awards.html", "🏆 Awards"), ("canadians.html", "🇨🇦 Canadian Stories"), ("documentary.html", "🎥 Documentary")]),
    ("✂️ Craft", [("editors.html", "✂️ Editors"), ("cinematographers.html", "📷 Cinematographers"), ("digital-assistant-editor.html", "🤖 Digital Assistant Editor"), ("specs.html", "📐 Delivery Specs"), ("cut-in-canada.html", "🎞️ Cut in Canada"), ("vibe-cutting.html", "🎚️ Vibe Cutting"), ("software.html", "💻 Software"),
                   ("sound.html", "🎧 Sound"), ("composers.html", "🎼 Composers"), ("music-supervisors.html", "🎸 Music Supervisors")]),
    ("🎓 Learn and work", [("schools.html", "🎓 Education"), ("unions.html", "🗺️ Union Map"), ("status-of-the-artist.html", "⚖️ Status & Tax Credits"), ("networking.html", "🤝 Networking"), ("wellbeing.html", "💚 Wellbeing")]),
    ("🌍 Sustainability", [("green-post.html", "🌍 Green Post")]),
]
NAV_CSS = ("<style>.sitenav{border-bottom:1px solid var(--line);background:var(--bg)}.sitenav .snw{max-width:1080px;margin:0 auto;padding:8px 16px;display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start}"
           ".sitenav a,.sitenav summary{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font:13px ui-sans-serif,-apple-system,sans-serif;text-decoration:none;white-space:nowrap;cursor:pointer;list-style:none}"
           ".sitenav summary::-webkit-details-marker{display:none}.sitenav summary::after{content:' \\25BE';opacity:.6}"
           ".sitenav a.on,.sitenav summary.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}"
           ".sitenav details{position:relative}.sitenav details[open]{z-index:70}.sitenav .gp{position:absolute;top:calc(100% + 6px);left:0;min-width:210px;max-width:86vw;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:6px;display:flex;flex-direction:column;gap:4px;box-shadow:0 8px 24px rgba(0,0,0,.25)}"
           ".sitenav .gp a{border:0;border-radius:8px;background:transparent;white-space:normal}.sitenav .gp a:hover{background:var(--line)}</style>")


def menu_html(pre="", cur="", originals=False, home=True):
    def a(h, lbl):
        return '<a href="%s%s"%s>%s</a>' % (pre, h, ' class="on"' if h == cur else "", lbl.replace("&", "&amp;"))
    out = ""
    if home:
        out += a("index.html", LEADER + " Picture Start")
    for gl, items in GROUPS:
        its = list(items)
        if originals and gl.endswith("News"):
            its.insert(0, ("originals.html", "📝 Originals"))
        on = any(h == cur for h, _ in its)
        out += ('<details><summary%s>%s</summary><div class="gp">%s</div></details>' % (' class="on"' if on else "", gl, "".join(a(h, l) for h, l in its)))
    out += a("contact.html", "✉️ Contact")
    return out


def add_nav(t, fname, has_originals):
    pre = "../" if fname.startswith("originals/") else ""
    nav = '<nav class="sitenav" aria-label="Sections"><div class="snw">' + menu_html(pre, fname, has_originals) + "</div></nav>"
    t = t.replace("</head>", NAV_CSS + "</head>", 1)
    return t.replace("</header>", "</header>" + nav, 1)


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
            it["vibe"] = bool(VIBE_RE.search(blob2) and VIBE_CTX.search(blob2))
            it["cce"] = bool(CCE_RE.search(blob2 + " " + it["source"] + " " + it["url"]))
            it["legal"] = bool(LEGAL_RE.search(blob2))
            it["tips"] = it["category"] in ("picture", "audio", "vfx", "gear") and bool(TIPS_RE.search(it["title"])) and not NOT_TIPS.search(it["title"])
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
        # archived stories may predate newer tags: fill in defaults and recompute the cheap text tags
        _b = a["title"] + " " + a.get("excerpt", "")
        a.setdefault("canada", False); a.setdefault("status", False); a.setdefault("prov", []); a.setdefault("source", "")
        a["ai"] = bool(AI_CS.search(_b) or AI_CI.search(_b))
        a["vibe"] = bool(VIBE_RE.search(_b) and VIBE_CTX.search(_b))
        a["legal"] = bool(LEGAL_RE.search(_b))
        a["tips"] = a.get("category") in ("picture", "audio", "vfx", "gear") and bool(TIPS_RE.search(a["title"])) and not NOT_TIPS.search(a["title"])
        a["cce"] = bool(CCE_RE.search(_b + " " + a["source"] + " " + a.get("url", "")))
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
        f'<url><loc>{SITE_URL}/</loc><lastmod>{now.date()}</lastmod><changefreq>hourly</changefreq></url><url><loc>{SITE_URL}/contact.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/awards.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/documentary.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/wellbeing.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/green-post.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/cut-in-canada.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/vibe-cutting.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/schools.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/canadians.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/unions.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/software.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/specs.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/digital-assistant-editor.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/cinematographers.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/composers.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/sound.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/music-supervisors.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/networking.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/buzz.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/editors.html</loc><lastmod>{now.date()}</lastmod></url><url><loc>{SITE_URL}/status-of-the-artist.html</loc><lastmod>{now.date()}</lastmod></url></urlset>')
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
    import didyouknow
    _dyk = [i for i in items if didyouknow.STUDIO_RE.search(i["title"] + " " + i.get("excerpt", ""))]
    (OUT / "cut-in-canada.html").write_text(didyouknow.render(_leaf, _fav, now.strftime("%Y-%m-%d"), _dyk), encoding="utf-8")
    import topics, awards, docs
    _em = _cfg.get("contact_email") or ""
    _mail = '<a href="mailto:' + _em + '">' + _em + '</a>' if _em else "a contact address is coming soon"
    _cbody = ('<div class="box"><h3>Email</h3><p style="font-size:20px;margin:6px 0">' + _mail + '</p>'
              '<p class="note" style="margin:0">One shared inbox, read by a person. Replies can take a few days.</p></div>'
              '<div class="box"><h3>Story tips and sources</h3><p style="margin:6px 0 0">Know about a Canadian post house, Editor, award, school or union item that belongs on the site? Send the name and a link to a public source, and it gets checked before it goes up.</p></div>'
              '<div class="box"><h3>Corrections and removals</h3><p style="margin:6px 0 0">If something is wrong, or you want an item changed or removed, tell us which page and what is wrong. We correct mistakes and honour removal requests.</p></div>'
              '<div class="box"><h3>Your outlet, guild or studio</h3><p style="margin:6px 0 0">Want a source or an organization added? Send the link. The site is independent and not run by any union, guild or company.</p></div>')
    (OUT / "contact.html").write_text(topics._page(_leaf, _fav, now.strftime("%Y-%m-%d"), "Contact", "How to contact Post Production Canada: story tips, corrections and removal requests.", "✉️ Contact", "Tips, corrections and requests are all welcome.", _cbody), encoding="utf-8")
    (OUT / "awards.html").write_text(awards.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    (OUT / "documentary.html").write_text(docs.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    (OUT / "wellbeing.html").write_text(topics.wellbeing(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    (OUT / "green-post.html").write_text(topics.green(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import vibecutting
    (OUT / "vibe-cutting.html").write_text(vibecutting.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import schools
    (OUT / "schools.html").write_text(schools.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import canadians
    (OUT / "canadians.html").write_text(canadians.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import originals
    _arts = originals.render_all(_leaf, _fav, now.strftime("%Y-%m-%d"), _cfg, OUT, ROOT)
    import specs
    (OUT / "specs.html").write_text(specs.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import digitalassistant
    (OUT / "digital-assistant-editor.html").write_text(digitalassistant.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import cinematographers
    (OUT / "cinematographers.html").write_text(cinematographers.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import composers
    (OUT / "composers.html").write_text(composers.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import soundpost
    (OUT / "sound.html").write_text(soundpost.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import musicsup
    (OUT / "music-supervisors.html").write_text(musicsup.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import software
    (OUT / "software.html").write_text(software.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
    import networking
    (OUT / "networking.html").write_text(networking.render(_leaf, _fav, now.strftime("%Y-%m-%d")), encoding="utf-8")
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
        t = style.link_people(cap_editor(nobreak(f.read_text(encoding="utf-8"))))
        _rel = f.relative_to(OUT).as_posix()
        if _rel == "index.html":
            t = t.replace("</head>", NAV_CSS + "</head>", 1)
        if _rel != "index.html":
            t = add_nav(t, _rel, bool(_arts))
        if _rel != "index.html" and "homefab" not in t:
            t = t.replace("</body>", HOME_FAB + "</body>", 1)
        if beacon and "cloudflareinsights" not in t:
            t = t.replace("</head>", beacon + "</head>", 1)
        if _rel == "editors.html" and "ed-banner" not in t:
            import graphics
            t = t.replace("</h1>", "</h1><style>" + graphics.CSS + "</style>" + graphics.banner("THE EDITOR IS AN ARTIST", "The Editor shapes the story.") + graphics.craft_cards(), 1)
        if "ppc-foot" not in t:
            t = t.replace("</body>", FOOT.replace("{{YEAR}}", str(now.year)) + "</body>", 1)
        f.write_text(t, encoding="utf-8")
    import members
    members.write(OUT, ROOT, _leaf, _fav)
    (OUT / "CNAME").write_text("postproductioncanada.ca\n")
    (OUT / "stories.json").write_text(json.dumps(
        [{**i, "date": i["date"].isoformat()} for i in items], ensure_ascii=False, indent=1))

FOOT = ('<div class="ppc-foot" style="border-top:1px solid rgba(128,128,128,.3);padding:22px 16px 34px;text-align:center;'
        'font-size:13px;line-height:1.7;opacity:.82"><div style="max-width:720px;margin:0 auto">'
        '<p style="margin:0 0 14px"><b>&copy; {{YEAR}} Post Production Canada.</b> All rights reserved.</p>'
        '<p style="margin:0 0 14px"><b>What we are.</b> A collective for Canada\'s post-production community. We compile publicly available information: news, resources and reference. '
        'We are always adding things, and we want to hear what is missing.</p>'
        '<p style="margin:0 0 14px"><b>Send it to us.</b> Story tips, events, festivals, schools, videos, corrections or removal requests are all welcome. '
        '<a href="contact.html" style="color:inherit">Contact us</a>.</p>'
        '<p style="margin:0 0 14px"><b>Rights.</b> Headlines and excerpts link to their original publishers, who keep all rights in their own work. '
        'Summaries and original text on this site are ours; please do not republish them without permission.</p>'
        '<p style="margin:0"><b>Please note.</b> Provided for information only, with no guarantee of accuracy or completeness, so check anything important with the source. '
        'We are independent, and not affiliated with or endorsed by any union, guild, association or company mentioned.</p>'
        '</div></div>')

_ED_RE = re.compile(r"(?<![\w/.@#\-])editor(s?)(?![\w/@]|\.[a-z])")


def cap_editor(t):
    """House style: the word Editor is always capitalized. Applies to our own text only, never to
    third-party headlines (cards, picks, the Morning Roll), attributes, URLs or scripts."""
    out, mode = [], None
    for seg in re.split(r"(<[^>]*>)", t):
        if seg.startswith("<"):
            low = seg.lower()
            if re.match(r"<(script|style)\b", low):
                mode = "json" if 'id="data"' in low else "skip"
            elif low.startswith("</script") or low.startswith("</style"):
                mode = None
            elif re.match(r'<article class="(card|pick|frame)\b', low):
                mode = "card"
            elif low.startswith("</article") and mode == "card":
                mode = None
            out.append(seg)
        elif mode in (None, "json"):
            out.append(style.cap_text(seg))
        else:
            out.append(seg)
    return "".join(out)


def esc(s): return html.escape(s, quote=True)

CATS = {"canada": ("🇨🇦", "Canada"), "picture": ("🎬", "Storytelling & Editing"), "audio": ("🎧", "Audio"),
        "vfx": ("🟩", "VFX & Animation"), "gear": ("🎥", "Gear & Software"), "business": ("💼", "Business & Unions"),
        "ai": ("🤖", "AI Filmmaking"),
        "cce": ("✂️", "CCE"),
        "vibe": ("🎚️", "Vibe Cutting"),
        "status": ("⚖️", "Status of the Artist"),
        "legal": ("©️", "Copyright & Legal"),
        "tips": ("💡", "Tips & Tricks")}
NOT_TIPS = re.compile(r"instagram|tiktok|campaign|fake website|black friday|\bcast(ing)? |rob a bank", re.I)
TIPS_RE = re.compile(r"(\bhow[- ]to\b|\bhow (to|i|we|they|it was|this was|that was|was)\b[^.]{0,60}\b(made|done|cut|edited|built|created|achieved|shot|mixed|graded|composited)\b|"
                     r"tutorials?|\btips?\b|tricks?\b|step[- ]by[- ]step|walk-?through|masterclass|breakdowns?|behind the (scenes|cut)|art of the cut|"
                     r"(editing|colou?r|grading|post|audio|sound|vfx|finishing) workflows?|techniques?|explained|a guide to|beginner'?s guide|cheat ?sheet|shortcuts?|best practices|under the hood)", re.I)
LEGAL_RE = re.compile(r"(copyright\w*|intellectual property|infring\w+|lawsuits?|\bsued?\b|\bsues\b|litigation|piracy|pirated|"
                      r"trade-?marks?|likeness|right of publicity|moral rights|fair dealing|neighbouring rights|\bSOCAN\b|\bCMRRA\b|re:sound|"
                      r"\bsync(hronization)? licen[cs]\w+|music licen[cs]\w+|licen[cs]ing (deal|agreement|rights)|training data|"
                      r"who owns|ownership of|rights holders?|rightsholders?|digital replicas?|work[- ]for[- ]hire)", re.I)
VIBE_RE = re.compile(r"vibe (cutting|editing)|agentic|\bMCP\b|AI assistant|natural[- ]language|creative agent|text-based editing|chat-?based", re.I)
VIBE_CTX = re.compile(r"\bedit|video|timeline|premiere|resolve|avid|filmmak|post-?production|final cut|media composer", re.I)
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

def _decor(r):
    """A leaf for anything Canadian and a pin for any province it connects to."""
    text = r.get("title", "") + " " + r.get("note", "")
    leaf = "🇨🇦 " if (CANADA_RE.search(text) or r.get("source") == "CMPA") else ""
    pins = "".join(f'<span class="chip c-prov">📍 {k}</span>' for k, rx in PROV_RE.items() if rx.search(text))
    return leaf, pins


TOPICS = [
    ("📷", "Camera", r"\bcameras?\b|\bARRI\b|alexa|\bred (komodo|v-raptor|raptor)|ursa|\bFX\d|mirrorless|camcorder|insta360|gopro|\bcinema line|sensor|\bX-T\d|\bZ ?\d{1,2}\b|\bR\d{1,2}\b"),
    ("🔭", "Lens", r"\blens(es)?\b|anamorphic|\bprimes?\b|zoom lens|\bNAMM"),
    ("🔦", "Lighting", r"\blighting\b|\bled panels?\b|aputure|nanlite|godox|\blight kit|\bnanlux|\bvela\b"),
    ("🚁", "Drone", r"\bdrones?\b|\bfpv\b|\bdji\b"),
    ("🎙️", "Mic", r"microphones?|\bmics?\b|lavalier|\bboom\b|field recorder|sound devices|shotgun"),
    ("💾", "Storage", r"\bstorage\b|\bssd\b|\bnas\b|hard drives?|\blto\b|\braid\b|\bbackups?\b|memory cards?|cfexpress"),
    ("🎨", "Colour", r"colou?r (grad|correct|manage|match|science)|davinci|\bluts?\b|\bhdr\b|dolby vision|colou?rist"),
    ("🧩", "Plugin", r"plug-?ins?|add-ons?|\bofx\b|\bextension\b"),
    ("🎞️", "Film stock", r"\b35mm\b|\b16mm\b|\b65mm\b|film stock|kodak|celluloid|\bimax\b"),
    ("🆕", "New", r"\blaunch(es|ed)?\b|announc|unveil|releas|introduc|new version|firmware|\bbeta\b|\bupdate[sd]?\b|\badds?\b"),
    ("🏷️", "Deal", r"\bprice|\bdeals?\b|\bsale\b|black friday|discount|cyber monday"),
    ("🎪", "Festival", r"festival"),
    ("🏆", "Awards", r"\bawards?\b|nominee|nominat|\bwins?\b|winners?"),
    ("💼", "Jobs", r"hiring|\bjobs?\b|layoffs?|job cuts|\bcareers?\b"),
]
TOPIC_RES = [(em, lab, re.compile(rx, re.I)) for em, lab, rx in TOPICS]


def topic_chips(title, url, skip=()):
    out, n = "", 0
    for em, lab, rx in TOPIC_RES:
        if lab in skip or not rx.search(title):
            continue
        out += f'<span class="chip c-topic" title="{lab}">{em} {lab}</span>'
        n += 1
        if n == 3:
            break
    if "youtube.com" in url or "youtu.be" in url:
        out += '<span class="chip c-topic" title="Video">▶️ Video</span>'
    return out


def card(i):
    cats = []
    if i["canada"]: cats.append("canada")
    cats.append(i["category"])
    if i["status"]: cats.append("status")
    if i.get("legal"): cats.append("legal")
    if i.get("tips"): cats.append("tips")
    if i["ai"]: cats.append("ai")
    if i["cce"]: cats.append("cce")
    if i["vibe"]: cats.append("vibe")
    iso = i["date"].isoformat()
    _lf = "🇨🇦 " if i["canada"] else ""
    em, lab = CATS[i["category"]]
    chip = f'<span class="chip c-{i["category"]}">{em} {lab}</span>'
    if i["canada"] and i["category"] != "canada":
        chip += '<span class="chip c-canada">🇨🇦</span>'
    if i["ai"]:
        chip += '<span class="chip c-ai">🤖 AI</span>'
    if i["vibe"]:
        chip += '<span class="chip c-vibe">🎚️ Vibe</span>'
    if i["cce"]:
        chip += '<span class="chip c-cce" title="Canadian Cinema Editors">CCE</span>'
    if i["status"]:
        chip += '<span class="chip c-status">⚖️ Status</span>'
    if i.get("legal"):
        chip += '<span class="chip c-legal">©️ Legal</span>'
    if i.get("tips"):
        chip += '<span class="chip c-tips">💡 Tips</span>'
    _tc = topic_chips(i["title"], i["url"])
    if i["category"] != "gear" and any(f'title="{g}"' in _tc for g in ("Camera", "Lens", "Lighting", "Drone", "Mic", "Storage")):
        chip += '<span class="chip c-gear">🎥 Gear</span>'
    chip += _tc
    for k in i["prov"]:
        chip += f'<span class="chip c-prov">📍 {k}</span>'
    ex = f'<p class="ex">{esc(i["excerpt"])}</p>' if i["excerpt"] else ""
    _wy = WHY.get(i["title"])
    if _wy:
        ex += f'<p class="why"><b>Why it matters:</b> {esc(_wy[0])} <a href="{esc(_wy[2])}" target="_blank" rel="noopener">{esc(_wy[1])}</a></p>'
    return (f'<article class="card k-{i["category"]}" data-cats="{" ".join(sorted(set(cats)))}" data-prov="{" ".join(i["prov"])}" data-t="{esc(norm(i["title"] + " " + i["source"]))}">'
            f'<div class="chips">{chip}</div><div class="meta"><span class="src">{_lf}{esc(i["source"])}</span>'
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
    _lf, _pn = _decor({**r, "source": src})
    return ('<article class="pick body"><div class="meta"><span class="src">' + _lf + esc(src) + "</span>" + by + when + _pn + "</div>"
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
        f'<article class="pick"><div class="meta"><span class="src">{_decor(r)[0]}{esc(r["source"])}</span><span class="dot">·</span>'
        f'<time datetime="{r["dt"].isoformat()}">{r["dt"].date()}</time>{_decor(r)[1]}</div>'
        f'<h3><a href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(r["title"])}</a></h3>'
        + (f'<p class="why"><b>Why it matters:</b> {esc(r["note"])}</p>' if r.get("note") else "") + '</article>'
        for r in picks)
    return f'<section class="picks" aria-label="Our picks"><h2>⭐ Our Picks</h2><div class="pgrid">{cards}</div></section>'


ROLL_FILE = ROOT / "data" / "roll.json"
ROLL_HOUR_ET = 8


def _et(now):
    try:
        from zoneinfo import ZoneInfo
        return now.astimezone(ZoneInfo("America/Toronto"))
    except Exception:
        return now - timedelta(hours=5)


HIST_FILE = ROOT / "data" / "roll_history.json"


def _pick_roll(items, ref, bounded=False):
    """The six stories for a roll compiled at `ref` (a UTC datetime). `bounded` ignores stories newer than ref (for rebuilding past days)."""
    def window(hours):
        return [i for i in items if i["date"] >= ref - timedelta(hours=hours) and (not bounded or i["date"] <= ref)]
    pool = window(24)
    if len(pool) < 5:
        pool = window(72)
    pool = [i for i in pool if i["canada"] or "news.google.com" not in i["url"]]
    pool.sort(key=lambda i: (i["canada"], i["date"]), reverse=True)
    pick, per = [], {}
    for i in pool:
        if per.get(i["source"], 0) >= 2:
            continue
        per[i["source"]] = per.get(i["source"], 0) + 1
        pick.append(i)
        if len(pick) == 6:
            break
    pick.sort(key=lambda i: i["date"], reverse=True)
    return [{"title": i["title"], "url": i["url"], "source": i["source"], "category": i["category"],
             "prov": i.get("prov", []), "canada": bool(i["canada"]), "date": i["date"].strftime("%b %-d")} for i in pick]


def _load_hist():
    try:
        return json.loads(HIST_FILE.read_text())
    except Exception:
        return {}


def _save_hist(h):
    HIST_FILE.parent.mkdir(exist_ok=True)
    keep = sorted(h)[-12:]
    HIST_FILE.write_text(json.dumps({k: h[k] for k in keep}, indent=1, ensure_ascii=False))


def get_roll(items, now):
    """The Morning Roll: compiled once a day, on the first build at or after 8:00 a.m. Eastern, then kept until the next one."""
    et = _et(now)
    today = et.strftime("%Y-%m-%d")
    old = None
    try:
        old = json.loads(ROLL_FILE.read_text())
    except Exception:
        pass
    due = old is None or (et.hour >= ROLL_HOUR_ET and old.get("date") != today)
    if not due:
        return old
    roll = {"date": today, "compiled": ("PREVIEW" if old is None else et.strftime("%-I:%M %p ET")), "day": et.strftime("%a %b %-d").upper(),
            "items": _pick_roll(items, now)}
    if os.environ.get("GITHUB_ACTIONS") or os.environ.get("ROLL_SAVE") or old is None:
        ROLL_FILE.parent.mkdir(exist_ok=True)
        ROLL_FILE.write_text(json.dumps(roll, indent=1, ensure_ascii=False))
        if old and old.get("date") and old["date"] != today:
            h = _load_hist()
            h[old["date"]] = {**old, "reconstructed": False}
            _save_hist(h)
    return roll


def roll_history(items, now, today_date):
    """The last ten days of rolls. Days with no saved roll are rebuilt from the story archive and labelled as such."""
    from datetime import date as _d
    et = _et(now)
    h = _load_hist()
    changed = False
    for k in range(1, 11):
        day = (et - timedelta(days=k)).date()
        key = day.isoformat()
        if key == today_date or key in h:
            continue
        try:
            from zoneinfo import ZoneInfo
            ref = datetime(day.year, day.month, day.day, ROLL_HOUR_ET, 0, tzinfo=ZoneInfo("America/Toronto")).astimezone(timezone.utc)
        except Exception:
            ref = datetime(day.year, day.month, day.day, ROLL_HOUR_ET + 5, 0, tzinfo=timezone.utc)
        pick = _pick_roll(items, ref, bounded=True)
        if pick:
            h[key] = {"date": key, "day": day.strftime("%a %b %-d").upper(), "items": pick, "reconstructed": True}
            changed = True
    if changed:
        _save_hist(h)
    return {k: v for k, v in h.items() if k != today_date and k >= (et - timedelta(days=10)).date().isoformat()}


def history_html(items, now, today_date):
    h = roll_history(items, now, today_date)
    if not h:
        return ""
    days = ""
    for key in sorted(h, reverse=True):
        r = h[key]
        rows = ""
        for n, s in enumerate(r["items"], 1):
            wy = WHY.get(s["title"])
            why = f'<div class="hwhy"><b>Why it matters:</b> {esc(wy[0])}</div>' if wy else ""
            leaf = "🇨🇦 " if s.get("canada") else ""
            pins = "".join(f'<span class="rpin">📍 {esc(PROV_LABEL.get(k, k))}</span>' for k in s.get("prov", []))
            rows += (f'<li><span class="hno">{MINIREEL} REEL {n}</span> {leaf}<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a> '
                     f'<span class="hsrc">{esc(s["source"])} · {esc(s["date"])}</span> {pins}{why}</li>')
        days += f'<details class="hday"><summary>{esc(r["day"])}</summary><ol>{rows}</ol></details>'
    recon = any(v.get("reconstructed") for v in h.values())
    note = ('<p class="hnote">Days marked here before the roll began saving itself were rebuilt from our story archive, so they may differ slightly from what ran that morning.</p>' if recon else "")
    return ('<section class="rollhist" aria-label="Past ten days of the Morning Roll"><div class="wrap"><h2>📼 Past 10 days of the Morning Roll</h2>'
            '<p class="hnote">Missed a morning? Open a day to see its six reels.</p>' + days + note + '</div></section>')


REEL = ('<svg class="reel" viewBox="0 0 100 100" aria-hidden="true"><g class="spin"><circle cx="50" cy="50" r="46" fill="#1b1d22" stroke="#9aa0ab" stroke-width="3"/>'
        + "".join(f'<circle cx="{50+27*__import__("math").cos(k*1.0472):.1f}" cy="{50+27*__import__("math").sin(k*1.0472):.1f}" r="9" fill="#f6f4ef"/>' for k in range(6))
        + '<circle cx="50" cy="50" r="8" fill="#9aa0ab"/><circle cx="50" cy="50" r="3" fill="#1b1d22"/></g></svg>')


_ROLL_JS = """<script>(function(){var s=document.getElementById('strip'),p=document.getElementById('rpause');if(!s)return;
var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,paused=rm,hold=false,last=0,wait=0;
function setb(){if(p){p.textContent=paused?'▶ Play scroll':'⏸ Pause scroll';p.setAttribute('aria-pressed',paused)}}
if(p)p.onclick=function(){paused=!paused;setb()};setb();
['pointerenter','touchstart','focusin','wheel'].forEach(function(e){s.addEventListener(e,function(){hold=true},{passive:true})});
['pointerleave','touchend','focusout'].forEach(function(e){s.addEventListener(e,function(){setTimeout(function(){hold=false},3500)},{passive:true})});
s.style.scrollSnapType='none';
function tick(t){var dt=Math.min(t-last,80);last=t;
if(!paused&&!hold&&s.scrollWidth>s.clientWidth){var max=s.scrollWidth-s.clientWidth;
if(wait>0){wait-=dt;if(wait<=0)s.scrollLeft=0}else if(s.scrollLeft>=max-1){wait=2500}else{s.scrollLeft+=dt*0.028}}
requestAnimationFrame(tick)}
requestAnimationFrame(tick)})();</script>"""


def _takeaways(items, now):
    """Key takeaways for Canada, computed from the stories on this page. Counts only, no opinions."""
    rec = [i for i in items if i["date"] >= now - timedelta(days=7)]
    if len(rec) < 5:
        return ""
    can = [i for i in rec if i["canada"]]
    pc = {}
    for i in rec:
        for k in i.get("prov", []):
            pc[k] = pc.get(k, 0) + 1
    cc = {}
    for i in rec:
        if i["category"] in CATS:
            cc[i["category"]] = cc.get(i["category"], 0) + 1
    li = [f"<li><b>{len(rec)}</b> stories in the last 7 days; <b>{len(can)}</b> have a Canadian angle.</li>"]
    if pc:
        top = sorted(pc.items(), key=lambda x: -x[1])[:3]
        li.append("<li>Most-mentioned places: " + ", ".join(f"<b>{esc(PROV_LABEL.get(k, k))}</b> ({n})" for k, n in top) + ".</li>")
    if cc:
        k, n = max(cc.items(), key=lambda x: x[1])
        li.append(f"<li>Busiest topic: <b>{CATS[k][0]} {esc(CATS[k][1])}</b> ({n} stories).</li>")
    return ('<div class="takes"><h3>🇨🇦 Key takeaways for Canada</h3><ul>' + "".join(li) +
            '</ul><p>Counted from the stories on this page, not opinion. Pick a province or tab below to dig in.</p></div>')


try:
    WHY = json.loads((ROOT / "data" / "why.json").read_text())
except Exception:
    WHY = {}

MINIREEL = ('<svg class="mreel" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="10.5" fill="none" stroke="#ffb000" stroke-width="2"/>'
            '<circle cx="12" cy="6" r="2.3" fill="#ffb000"/><circle cx="17.2" cy="15" r="2.3" fill="#ffb000"/><circle cx="6.8" cy="15" r="2.3" fill="#ffb000"/><circle cx="12" cy="12" r="1.6" fill="#ffb000"/></svg>')
ROLL_PHRASES = ["COLD OPEN", "ROLLING", "CLOSE-UP", "PLOT TWIST", "WIDE SHOT", "THAT'S A WRAP"]


def roll_html(items, now):
    r = get_roll(items, now)
    frames = ""
    byurl = {it["url"]: it for it in items}
    for n, s in enumerate(r["items"], 1):
        em = CATS.get(s["category"], ("🎬", ""))[0]
        leaf = "🇨🇦 " if (s["canada"] and s["category"] != "canada") else ""
        pins = "".join(f'<span class="rpin">📍 {esc(PROV_LABEL.get(k, k))}</span>' for k in s["prov"])
        ex = (s.get("excerpt") or (byurl.get(s["url"]) or {}).get("excerpt") or "").strip()
        ex = re.sub(r"This content is restricted to subscribers\.?", "", ex, flags=re.I)
        ex = re.split(r"\s+The post\s", ex)[0].split("appeared first on")[0].strip()
        if len(ex) < 40:
            ex = ""
        if len(ex) > 170:
            ex = ex[:170].rsplit(" ", 1)[0].rstrip(",;:.") + "…"
        wy = WHY.get(s["title"])
        if wy:
            gist = f'<div class="fgist"><b>Why it matters:</b> {esc(wy[0])} <a href="{esc(wy[2])}" target="_blank" rel="noopener">{esc(wy[1])}</a></div>'
        else:
            gist = f'<div class="fgist"><b>The gist:</b> {esc(ex)}</div>' if ex else ""
        if s["prov"]:
            ang = "🇨🇦 Canadian angle: " + ", ".join(PROV_LABEL.get(k, k) for k in s["prov"])
        elif s["canada"]:
            ang = "🇨🇦 Canadian angle: a Canadian story"
        else:
            ang = "🌐 Wider industry story"
        phrase = ROLL_PHRASES[(n - 1) % len(ROLL_PHRASES)]
        frames += (f'<article class="frame"><div class="fno">{MINIREEL} REEL {n}</div><div class="fmeta">{em} {leaf}{pins}</div>'
                   f'<a class="ftitle" href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>'
                   f'{gist}<div class="fang">{ang}</div>'
                   f'<div class="fsrc">{esc(s["source"])} · {esc(s["date"])}</div>'
                   f'<a class="fmore" href="{esc(s["url"])}" target="_blank" rel="noopener">Read the full article →</a></article>')
    if not frames:
        frames = '<article class="frame"><div class="ftitle">The roll is loading. Check back after 8 a.m. Eastern.</div></article>'
    return ('<section class="roll" aria-label="Morning Roll"><div class="wrap"><div class="rollhead">' + REEL +
            f'<div class="rtxt"><div class="rlcd">MORNING ROLL · {esc(r["day"])}</div>'
            f'<div class="rsub">☕ Your 8 a.m. rundown of the latest. {"Preview edition: the first full roll compiles at 8 a.m. Eastern." if r["compiled"] == "PREVIEW" else "Compiled " + esc(r["compiled"]) + "."} Read it with your first coffee or tea.</div></div>'
            + '<div class="coffee" aria-hidden="true">☕</div></div><div class="strip" id="strip">' + frames + '</div>'
            + _takeaways(items, now) + '</div></section>' + history_html(items, now, r["date"]))

def render(items, sources, now):
    picks = load_picks(now)
    ptitles = {norm(r["title"]) for r in picks}
    items = [i for i in items if norm(i["title"]) not in ptitles]
    cards = "\n".join(card(i) for i in items)
    counts = {k: sum(1 for i in items if (k == "all") or (k == "canada" and i["canada"]) or (k == "status" and i["status"]) or (k == "ai" and i["ai"]) or (k == "cce" and i["cce"]) or (k == "vibe" and i["vibe"]) or (k == "legal" and i.get("legal")) or (k == "tips" and i.get("tips")) or i["category"] == k)
              for k in ["all"] + list(CATS)}
    updated = now.strftime("%Y-%m-%d %H:%M UTC")
    tabs = [("all", "📰 All")] + [(k, f"{e} {l}") for k, (e, l) in CATS.items()]
    tabhtml = "".join(f'<button class="tab{" on" if k=="all" else ""}" data-f="{k}">{l} <i>{counts[k]}</i></button>' for k, l in tabs)
    popts = "".join(f'<option value="{k}">{PROV_LABEL[k]} ({sum(1 for i in items if k in i["prov"])})</option>' for k in PROV_LABEL)
    cfg = json.loads((ROOT / "site.json").read_text())
    sub, subbtn = "", ""
    _rss = ('<p class="consent" style="opacity:.9">📡 <b>RSS</b> is a free way to follow the site without email. Copy <b>postproductioncanada.ca/feed.xml</b> into a feed reader such as Feedly or NetNewsWire and new stories show up there. '
            '<a href="/feed.xml">Open the feed</a></p>')
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
               'Unsubscribe any time. <a href="privacy.html">Privacy</a></p>' + _rss + '</div></section>')
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
    _orig = '<a class="btn" href="originals.html">📝 Originals</a>' if _o.count_published(ROOT) else ""
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
    _fbu = (cfg.get("feedback_form_url") or "").strip()
    _fbm = (cfg.get("contact_email") or "").strip()
    _fb = ""
    if _fbu or _fbm:
        _href = _fbu or ("mailto:" + _fbm + "?subject=Post%20Production%20Canada%20feedback")
        _ext = ' target="_blank" rel="noopener"' if _fbu else ""
        _fb = ('<section class="res"><div class="wrap"><h2>Feedback and tips</h2><p>Spot something missing or wrong? Know a story, a source, or a Canadian editor or director we should feature? '
               '<a class="btn" href="' + esc(_href) + '"' + _ext + '>Send feedback</a></p></div></section>')
    return TEMPLATE.replace("{{MENU}}", '<span class="sitenav" style="display:contents">' + menu_html("", "", False, False) + "</span>").replace("{{VU}}", "<s><u></u><u></u><u></u><u></u><u></u><u></u></s><s><u></u><u></u><u></u><u></u><u></u><u></u></s><s><u></u><u></u><u></u><u></u><u></u><u></u></s><s><u></u><u></u><u></u><u></u><u></u><u></u></s><s><u></u><u></u><u></u><u></u><u></u><u></u></s><s><u></u><u></u><u></u><u></u><u></u><u></u></s><s><u></u><u></u><u></u><u></u><u></u><u></u></s><s><u></u><u></u><u></u><u></u><u></u><u></u></s>").replace("{{ROLL}}", roll_html(items, now)).replace("{{FEEDBACK}}", _fb).replace("{{BARS}}", _bars).replace("{{TODAYSTR}}", now.strftime("%A, %b %-d, %Y")).replace("{{BODIES}}", bodies_html(now)).replace("{{ORIG}}", _orig).replace("{{CCELOGO}}", _cl).replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{PICKS}}", picks_html(picks)).replace("{{FLAG}}", flag).replace("{{PROVOPTS}}", popts).replace("{{SUBSCRIBE}}", sub).replace("{{SUBBTN}}", subbtn).replace("{{LOOP}}", ("#subscribe" if (cfg.get("subscribe_embed_html") or cfg.get("subscribe_form_action")) else "mailto:" + (cfg.get("contact_email") or "") + "?subject=Keep%20me%20in%20the%20loop")).replace("{{CONTACT}}", contact)\
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
.hero p{color:var(--mute);margin:0;max-width:40em}.nw{white-space:nowrap}.nsrc{color:#0a7cff;font-weight:800}@media (prefers-color-scheme:dark){.nsrc{color:#4da3ff}}:root[data-theme="dark"] .nsrc{color:#4da3ff}:root[data-theme="light"] .nsrc{color:#0a7cff}.loopwrap{margin-top:14px!important}.loop{display:block;text-align:center;background:var(--red);color:#fff!important;font-weight:800;font-size:clamp(15px,2.6vw,19px);line-height:1.3;padding:12px 18px;border-radius:12px;text-decoration:none;box-shadow:0 4px 0 rgba(0,0,0,.25)}.loop:hover{filter:brightness(1.1)}.clap{font-size:1.25em;vertical-align:-2px}
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
.chip.c-cce{background:#fff url({{CCELOGO}}) center/contain no-repeat;border:1px solid var(--line);width:104px;height:28px;padding:0;color:transparent;overflow:hidden}
.chip.c-topic{--c:var(--mute);font-weight:600}.chip.c-tips{--c:#1a9d5a}.k-tips{--c:#1a9d5a}.chip.c-legal{--c:#b8860b}.k-legal{--c:#b8860b}.chip.c-vibe{--c:#8a4fe0}.k-vibe{--c:#8a4fe0}
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
.why{margin:0;font-size:14px;color:#4a3a00;background:#fff4cc;border-left:4px solid #e0a100;border-radius:4px;padding:8px 10px;line-height:1.45}.why b{color:#8a5d00}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .why{color:#fff1c2;background:#33290a;border-left-color:#ffcc33}:root:not([data-theme="light"]) .why b{color:#ffcc33}}:root[data-theme="dark"] .why{color:#fff1c2;background:#33290a;border-left-color:#ffcc33}:root[data-theme="dark"] .why b{color:#ffcc33}
@media (max-width:640px){.top{flex-wrap:wrap;gap:10px}.brand{white-space:nowrap;font-size:18px}.tools{width:100%;flex-wrap:wrap}.btn{white-space:nowrap}}
.res{border-top:1px solid var(--line);padding:26px 0 6px}.res h2{margin:0 0 8px;font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}.res ul{margin:0;padding-left:18px;max-width:60em}.res li{margin:6px 0;font-size:14.5px}.res a{color:var(--red)}
.nb{white-space:nowrap}
.filmframe{display:inline-block;position:relative;background:#14161a;color:#f6f4ef;font-size:.8em;letter-spacing:.05em;white-space:nowrap;padding:.42em .6em;margin:.18em 0;border-radius:3px;border:2px solid var(--ink)}
.filmframe::before,.filmframe::after{content:"";position:absolute;left:5px;right:5px;height:5px;background:repeating-linear-gradient(90deg,#f6f4ef 0 6px,transparent 6px 12px);opacity:.9}
.roll{background:#14161a;border-top:1px solid #2a2d34;border-bottom:1px solid #2a2d34;padding:18px 0 22px;color:#eceae4}
.rollhead{display:flex;align-items:center;gap:14px;justify-content:space-between;margin-bottom:12px}
.reel{width:64px;height:64px;flex:none}.reel .spin{transform-origin:50px 50px;animation:rspin 9s linear infinite}
@keyframes rspin{to{transform:rotate(360deg)}}@media (prefers-reduced-motion:reduce){.reel .spin{animation:none}}
.rtxt{flex:1;min-width:0;text-align:center}
.rlcd{display:inline-block;background:#0b0d0a;color:#ffb000;font:700 clamp(15px,3.2vw,24px)/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;padding:8px 14px;border-radius:6px;border:2px solid #3a3d44;text-shadow:0 0 8px rgba(255,176,0,.55)}
.rsub{color:#aab0bb;font-size:13.5px;margin-top:8px}
.strip{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:28px 12px;background:#0b0c0e;border-radius:6px}@media (max-width:760px){.strip{grid-template-columns:repeat(2,1fr)}}@media (max-width:520px){.strip{grid-template-columns:1fr}}
.strip::before,.strip::after{content:"";position:absolute;left:0;right:0;height:10px;background:repeating-linear-gradient(90deg,#f6f4ef 0 12px,transparent 12px 26px);opacity:.85}
.strip::before{top:6px}.strip::after{bottom:6px}
.frame{min-width:0;background:#1e2127;border:1px solid #30343c;border-radius:6px;padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.rctl{margin-top:8px;color:#8f96a3;font-size:12.5px}.rctl .btn{background:#1e2127;color:#eceae4;border-color:#30343c;font-size:12px;padding:3px 10px;cursor:pointer}
.takes{margin-top:14px;background:#1e2127;border:1px solid #30343c;border-radius:10px;padding:10px 16px;color:#eceae4}.takes h3{margin:2px 0 6px;font-size:16px}.takes ul{margin:0 0 6px;padding-left:20px}.takes p{margin:0;color:#8f96a3;font-size:12.5px}
.fgist{color:#fff1c2;font-size:14px;line-height:1.45;background:#33290a;border-left:4px solid #ffcc33;border-radius:4px;padding:8px 10px}.fgist b{color:#ffcc33}.fgist a{color:#ffd980;text-decoration:underline}.mreel{vertical-align:-4px;margin-right:4px}.fang{font-size:12.5px;color:#ffb347;font-weight:600}.fno{font:700 11px ui-monospace,Menlo,monospace;color:#ffb000;letter-spacing:.15em}
.rollhist{background:#14161a;color:#eceae4;padding:6px 0 22px}.rollhist h2{margin:14px 0 6px;font-size:18px}.hnote{color:#8f96a3;font-size:12.5px;margin:4px 0 10px}.hday{background:#1e2127;border:1px solid #30343c;border-radius:8px;margin:6px 0;padding:8px 14px}.hday summary{cursor:pointer;font:700 13px ui-monospace,Menlo,monospace;color:#ffb000;letter-spacing:.12em}.hday ol{margin:10px 0 4px;padding-left:0;list-style:none}.hday li{padding:7px 0;border-top:1px solid #30343c;font-size:14px;line-height:1.4}.hday li a{color:#fff;font-weight:600}.hno{font:700 11px ui-monospace,Menlo,monospace;color:#ffb000;letter-spacing:.12em;margin-right:6px}.hsrc{color:#8f96a3;font-size:12px}.hwhy{background:#33290a;border-left:4px solid #ffcc33;border-radius:4px;padding:6px 10px;margin-top:6px;color:#fff1c2;font-size:13.5px}.hwhy b{color:#ffcc33}.fmeta{font-size:13px}.rpin{background:#2a2e36;border-radius:999px;padding:1px 8px;font-size:11.5px;margin-left:4px}
.ftitle{color:#fff;font-weight:700;font-size:17px;line-height:1.3;text-decoration:none}.coffee{font-size:48px;line-height:1;width:64px;text-align:center;flex:none}.ftitle:hover{text-decoration:underline}
.fsrc{color:#8f96a3;font-size:12px}.fmore{color:#ff8a7f;font-size:13px;margin-top:auto;text-decoration:none}
.newsword{display:inline-block;background:var(--red);color:#fff;padding:0 .3em;margin:.12em 0;border-radius:3px;font-weight:900;letter-spacing:.05em;transform:rotate(-2deg);box-shadow:3px 3px 0 var(--ink)}
.filmframe::before{top:4px}.filmframe::after{bottom:4px}
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
.vu{display:inline-flex;gap:2px;align-items:flex-end;height:28px;opacity:0;width:0;overflow:hidden;transition:opacity .4s,width .4s,margin .4s}
body.charge .vu{opacity:1;width:46px;margin-right:4px}
.vu s{display:flex;flex-direction:column-reverse;gap:1px;width:4px;text-decoration:none}
.vu u{display:block;height:3px;border-radius:1px;background:#2a2d34;text-decoration:none}
.vu u.on{background:#2ecc71}.vu u.on.m{background:#ffb347}.vu u.on.h{background:#ff4d3a}
.finale{position:absolute;inset:0;z-index:4;display:none;grid-template-columns:repeat(9,1fr);grid-template-rows:repeat(3,1fr);gap:6px 10px;padding:14px 26px;background:linear-gradient(#14161a,#0b0c0e);border-radius:14px;align-items:center;justify-items:center}
.finale.go{display:grid}
.cb{position:relative;width:min(44px,100%);height:38px}
.cb .sl{position:absolute;top:11px;left:0;right:0;bottom:0;background:#e8e2d4;border-radius:3px;display:grid;place-items:center;font:700 11px ui-monospace,Menlo,monospace;color:#14161a}
.cb .arm{position:absolute;top:0;left:0;right:0;height:10px;background:repeating-linear-gradient(115deg,#14161a 0 6px,#f6f4ef 6px 12px);border:1px solid #888;border-radius:2px;transform-origin:left bottom;transform:rotate(-28deg)}
.finale.go .arm{animation:clap .2s ease-in forwards;animation-delay:var(--d)}
.finale.go .sl{animation:flash .5s ease-out var(--d)}
@keyframes clap{to{transform:rotate(0)}}
@keyframes flash{0%{background:#fff;box-shadow:0 0 14px #fff}100%{background:#e8e2d4;box-shadow:none}}
.fin-title{grid-column:1/-1;grid-row:3;justify-self:start;color:#ffb347;font:700 12px ui-monospace,Menlo,monospace;letter-spacing:.18em;opacity:0;animation:fin 4s forwards 2.2s}
@keyframes fin{0%{opacity:0}15%,85%{opacity:1}100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.finale.go .arm{animation:none;transform:rotate(0)}.finale.go .sl{animation:none}}
footer{border-top:1px solid var(--line);padding:26px 0 40px;color:var(--mute);font-size:13px}
footer p{margin:0 0 8px;max-width:60em}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo">{{LEAF}}</span><span class="vu" id="vu" aria-hidden="true">{{VU}}</span>Post Production <b>Canada</b></a>
  <div class="tools">{{SUBBTN}}{{ORIG}}{{MENU}}<a class="btn" href="/feed.xml">📡 RSS</a><button class="btn" id="theme" aria-label="Toggle theme">◐</button></div>
</div></header>

<section class="hero"><div class="wrap herogrid"><div>
  <h1>All of Canada's<br><span class="filmframe">POST PRODUCTION</span><br><span class="nw"><span class="newsword">NEWS</span> <em>in one place.</em></span></h1>
  <p>Editing, colour, sound, VFX, animation and the business behind them — gathered from <b class="nsrc">{{NSOURCES}} sources</b> and updated live every few hours. <span class="nw">Free, always.</span></p>
</div><img class="heroart" src="{{FLAG}}" alt="A Canadian flag built from a clapperboard, light, mixing console, location pin and maple leaf with a play button" width="640" height="340"></div>
<div class="wrap"><p class="loopwrap"><a class="loop" href="{{LOOP}}">Original articles and features are coming soon. Stay in the loop: <span class="clap">🎬</span> click here →</a></p></div></section>

{{ROLL}}

<section class="deck" aria-label="Update clock"><div class="wrap"><div class="synth">
  <div class="cell"><div class="lbl">TODAY</div><div class="lcd sm" id="today">{{TODAYSTR}}</div></div>
  <div class="cell"><div class="lbl">NEXT UPDATE IN</div><div class="lcd" id="cd">--:--:--</div></div>
  <div class="cell"><div class="lbl">LAST UPDATED</div><div class="lcd sm" id="lu">{{UPDATED}}</div></div>
  <div class="cell wide"><div class="lbl">LAST 21 DAYS <span id="range"></span><span class="now">● NOW</span></div><div class="meter" id="meter">{{BARS}}</div></div>
<div class="finale" id="finale" aria-hidden="true"><div class="cb" style="grid-column:1;grid-row:1;--d:0.00s"><div class="arm"></div><div class="sl"><span>YT</span></div></div><div class="cb" style="grid-column:2;grid-row:1;--d:0.30s"><div class="arm"></div><div class="sl"><span>NT</span></div></div><div class="cb" style="grid-column:3;grid-row:1;--d:0.60s"><div class="arm"></div><div class="sl"><span>NU</span></div></div><div class="cb" style="grid-column:1;grid-row:2;--d:0.00s"><div class="arm"></div><div class="sl"><span>BC</span></div></div><div class="cb" style="grid-column:2;grid-row:2;--d:0.30s"><div class="arm"></div><div class="sl"><span>AB</span></div></div><div class="cb" style="grid-column:3;grid-row:2;--d:0.60s"><div class="arm"></div><div class="sl"><span>SK</span></div></div><div class="cb" style="grid-column:4;grid-row:2;--d:0.90s"><div class="arm"></div><div class="sl"><span>MB</span></div></div><div class="cb" style="grid-column:5;grid-row:2;--d:1.20s"><div class="arm"></div><div class="sl"><span>ON</span></div></div><div class="cb" style="grid-column:6;grid-row:2;--d:1.50s"><div class="arm"></div><div class="sl"><span>QC</span></div></div><div class="cb" style="grid-column:8;grid-row:2;--d:2.10s"><div class="arm"></div><div class="sl"><span>NL</span></div></div><div class="cb" style="grid-column:7;grid-row:3;--d:1.80s"><div class="arm"></div><div class="sl"><span>NB</span></div></div><div class="cb" style="grid-column:8;grid-row:3;--d:2.10s"><div class="arm"></div><div class="sl"><span>PE</span></div></div><div class="cb" style="grid-column:9;grid-row:3;--d:2.40s"><div class="arm"></div><div class="sl"><span>NS</span></div></div><div class="fin-title">COAST TO COAST · ACTION!</div></div>
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

{{FEEDBACK}}
<section class="res"><div class="wrap">
  <h2>Resources</h2>
  <ul>
    <li><a href="https://www.productionlist.com/" target="_blank" rel="noopener">Production List</a> — a directory of film and TV productions and companies, including post and VFX houses. Mostly US-focused; contact details are for paying members.</li>
    <li><a href="https://postperspective.com/" target="_blank" rel="noopener">Post Perspective</a> — trade news and features on post-production, VFX, editing, colour and sound. Its stories also appear in the news feed above.</li>
    <li><a href="editors.html">Canadian Cinema Editors</a> — the non-profit association for Canadian picture editors, plus the Vancouver Post Alliance.</li>
    <li><a href="https://filmincanada.com/incentives" target="_blank" rel="noopener">filmincanada.com</a> — film incentives by province and a tracker of productions across Canada.</li>
    <li><a href="https://cmpa.ca/profile" target="_blank" rel="noopener">CMPA Profile</a> — the annual economic report on Canada's screen industry.</li>
    <li><a href="awards.html">Awards</a> — the awards that honour Editors, sound, VFX and music supervision, with winners and IMDb links.</li>
    <li><a href="documentary.html">Documentary in Canada</a> — a sourced timeline and where to watch.</li>
    <li><a href="wellbeing.html">Wellbeing</a> — mental health and work-life balance support for screen workers.</li>
    <li><a href="green-post.html">Green Post</a> — sustainability programs and what they mean for post.</li>
    <li><a href="cut-in-canada.html">Did you know that was cut in Canada?</a> — movies and TV whose editing, effects or sound was done in Canada.</li>
    <li><a href="vibe-cutting.html">Vibe Cutting</a> — editing by telling the software what you want, and how AI is wiring into editing software.</li>
    <li><a href="schools.html">Education across Canada</a> — colleges, universities and private schools teaching picture editing, sound and post.</li>
    <li><a href="canadians.html">Canadian Stories</a> — the editors and directors from Canada behind screens the world watches.</li>
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
  var vu=document.querySelectorAll('#vu s'),fin=document.getElementById('finale'),lastRemain=1e9,demoEnd=0,lastFin=0;
  function fire(){var n=Date.now();if(n-lastFin<20000)return;lastFin=n;fin.classList.remove('go');void fin.offsetWidth;fin.classList.add('go');setTimeout(function(){fin.classList.remove('go')},5200)}
  window.ppcFinale=fire;window.ppcDemo=function(sec){demoEnd=Date.now()+(sec||14)*1000};
  function meter(a){vu.forEach(function(col){var lvl=a>0?Math.round(Math.random()*(1+5*a)):0;if(lvl>6)lvl=6;col.querySelectorAll('u').forEach(function(u,i){var on=i<lvl;u.className=on?('on'+(i>=4?' h':i>=3?' m':'')):''})})}
  setInterval(function(){var r=demoEnd?(demoEnd-Date.now())/1000:lastRemain;var a=(r>0&&r<=12)?(12-r)/12:0;meter(a)},90);
  function chargeCheck(remain){document.body.classList.toggle('charge',remain>0&&remain<=12);
    if(lastRemain<=2&&remain>9000)fire();lastRemain=remain}
  var _tick=tick;tick=function(){_tick();var now=new Date(),t=nextRun(now),remain=(t-now)/1000;
    if(demoEnd){var dr=(demoEnd-Date.now())/1000;document.body.classList.toggle('charge',dr>0&&dr<=12);if(dr<=0){demoEnd=0;fire()}}
    else chargeCheck(remain)};
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
