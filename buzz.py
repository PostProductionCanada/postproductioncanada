"""Post Buzz page: productions that are wrapping (heading into post) or just wrapped,
built from the public production lists on hollywoodnorthbuzz.com.

Only titles, cities and shoot dates are shown, never cast, and every entry links to the source.
These are public listings, not rumours: nothing here is unverified hearsay about a person or company.
"""
import html, re, urllib.request
from datetime import datetime, timedelta, timezone

e = html.escape
UA = "Mozilla/5.0 (compatible; PostProductionCanadaBot/1.0; +https://postproductioncanada.ca)"
LISTS = [("Eastern Canada", "https://hollywoodnorthbuzz.com/production-list-east"),
         ("Western Canada", "https://hollywoodnorthbuzz.com/production-list-west")]
MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                           "August", "September", "October", "November", "December"])}
DATE_RE = re.compile(r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})")

CURATED = [
    ("A Cape Breton 'Thelma and Louise': how a viral comedy duo made a movie by accident", "CBC Arts", "2026-08-14",
     "https://www.cbc.ca/arts/tracy-martina-goin-out-west-9.7307669",
     "A TikTok duo's partly improvised feature, Tracy & Martina: Goin' Out West. A look at one indie path from viral clips to a feature."),
]


def _d(s):
    m = DATE_RE.search(s.replace("\xa0", " "))
    if not m or m.group(1) not in MONTHS:
        return None
    return datetime(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2)), tzinfo=timezone.utc)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf8", "ignore")


def parse(page, region, url):
    out = []
    for col in re.findall(r'<div class="wp-block-column[^"]*"[^>]*flex-basis:66\.66%">(.*?)</div>', page, flags=re.S):
        ps = [html.unescape(re.sub(r"<[^>]+>", " ", p)) for p in re.findall(r"<p>(.*?)</p>", col, flags=re.S)]
        ps = [re.sub(r"\s+", " ", p.replace("\xa0", " ")).strip() for p in ps]
        if not ps:
            continue
        link = re.search(r'<a href="([^"]+)"', col)
        title = re.sub(r"\(\s*(Wrapped|Final Season)\s*\)", "", ps[0], flags=re.I)
        title = re.sub(r"\s+", " ", title).strip(" .:")
        dates = next((p for p in ps if "filming dates" in p.lower()), None)
        if not dates:
            continue
        city = dates.split("filming dates")[0].strip(" :")
        found = [_d(x) for x in re.findall(r"[A-Z][a-z]+\s+\d{1,2},?\s+\d{4}", dates.replace("\xa0", " "))]
        found = [f for f in found if f]
        if len(found) < 2:
            continue
        out.append({"title": title, "city": city, "start": found[0], "end": found[1], "region": region,
                    "url": link.group(1) if link else url})
    return out


def gather():
    items, ok = [], []
    for region, url in LISTS:
        try:
            items += parse(fetch(url), region, url)
            ok.append((region, url))
        except Exception as err:
            print(f"buzz: {region} list unavailable: {err}")
    return items, ok


def row(i):
    s, en = i["start"].strftime("%b %-d"), i["end"].strftime("%b %-d, %Y")
    city = f" · {e(i['city'])}" if i["city"] else ""
    return (f'<li><a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["title"])}</a>'
            f'<div class="note">{e(i["region"])}{city} · shoots {s} to {en}</div></li>')


# Rumour mill by province: titles, studios and dates only, from unions' own public listings. Hand-maintained, dated.
RUMOURS_ASOF = "November 19, 2026"
RUMOURS = [
    ("British Columbia", "BC", "IATSE Local 891 Rumour Mill, November 5 and October 29, 2026",
     "https://iatse.com/_content/documents/public/RM_PS/2026-11-05_RM-PS.pdf",
     "IATSE 891's weekly bulletin says these details were approved for its Rumour Mill. Shoot dates are the union's, and some are still to be set.",
     [("Hexagram (feature, Paramount)", "Shoot Jan. 18 to Mar. 22, 2027. Office opens Nov. 23, 2026."),
      ("The Innocent (series, Netflix)", "Shoot from Apr. 12, 2027, end date to be set. Office opens Jan. 18."),
      ("Arrivals: A New Manifest Mystery, Season 1 (series, WB)", "Shoot Jan. 19 to Jun. 9, 2027. Office opens Dec. 14."),
      ("The Black Tapes (series, Amazon/MGM)", "Shoot from Jan. 20, 2027, end date to be set."),
      ("Anaheim Realm, Season 2 (series, Sony Pictures Television)", "Shoot Mar. 1 to Sept. 30, 2027. Office is open."),
      ("Coven Academy, Season 2 (series, Disney)", "Dates to be set.")]),
    ("Ontario", "ON", "DGC Ontario production list, November 18, 2026 (productions in pre-production)",
     "https://www.dgc.ca/en/ontario/production-list",
     "Pre-production means the shoot has not started yet. Titles, tiers and dates come from the guild's list.",
     [("Bannerman, Season 1 (series, Tier A, Toronto)", "Pre-production Oct. 22, 2026 to Jan. 13, 2027. Shoot Jan. 14 to Apr. 19, 2027."),
      ("Cutthroat (feature, Tier C, Mississauga)", "Shoot Nov. 25, 2026 to Jan. 7, 2027. Picture post is listed from Dec. 18, 2026 to Apr. 4, 2027."),
      ("Dark Horse (documentary, Toronto)", "Pre-production Sept. 28 to Dec. 6, 2026. Shoot Dec. 7, 2026 to May 19, 2027."),
      ("Mini (feature, Tier A, Toronto)", "Pre-production Nov. 2, 2026 to Feb. 7, 2027. Shoot from Feb. 8, 2027."),
      ("On Broadway (feature, Tier A, Toronto)", "Pre-production Jun. 15, 2026 to Jan. 3, 2027. Shoot Jan. 4 to Feb. 12, 2027.")]),
    ("Alberta", "AB", "DGC Alberta production list, November 6, 2026",
     "https://www.dgc.ca/en/alberta/production-list",
     "One feature listed in pre-production. Its schedule shows as adjusted.",
     [("A Tier F feature from Legends of Conquest Productions Inc. (Edmonton)", "Pre-production Sept. 1 to Nov. 29, 2026. Shoot Nov. 30, 2026 to Jan. 18, 2027, with a break Dec. 19 to Jan. 3.")]),
    ("Newfoundland and Labrador", "NL", "DGC Newfoundland & Labrador production list, November 18, 2026",
     "https://www.dgc.ca/en/newfoundland-labrador/production-list",
     "Two productions are listed, and both are shooting now, so any post would come after wrap.",
     [("Saint Pierre, Season 3 (series, Tier A, Mount Pearl)", "Shoot July 5 to Nov. 30, 2026."),
      ("Secrets and Light Part 1: Illuminations (TV movie, Tier F, St. John's)", "Shooting now. Dates not listed.")]),
]
NOT_YET = "Québec, the Maritimes, Manitoba and Saskatchewan are not covered yet. Send me a union rumour list for them and I will add it."


def rumours_html():
    out = ""
    for prov, code, srcname, url, note, items in RUMOURS:
        lis = "".join(f"<li><b>{e(t)}</b><div class=\"note\">{e(d)}</div></li>" for t, d in items)
        out += (f'<div class="box"><h3 style="margin:0 0 4px">🍁 📍 {e(prov)}</h3><p class="note" style="margin:0 0 6px">{e(note)} '
                f'<a href="{e(url)}" target="_blank" rel="noopener">{e(srcname)}</a></p><ul class="arts">{lis}</ul></div>')
    return out + f'<p class="note">{e(NOT_YET)}</p>'


def render(leaf, favicon, updated, now):
    items, ok = gather()
    soon = sorted([i for i in items if now <= i["end"] <= now + timedelta(days=90)], key=lambda i: i["end"])[:12]
    just = sorted([i for i in items if now - timedelta(days=45) <= i["end"] < now], key=lambda i: i["end"], reverse=True)[:12]
    empty = '<p class="note">Nothing to show right now.</p>'
    soon_html = "<ul class=\"arts\">" + "".join(row(i) for i in soon) + "</ul>" if soon else empty
    just_html = "<ul class=\"arts\">" + "".join(row(i) for i in just) + "</ul>" if just else empty
    cur = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(s)}, {e(d)}</span>'
                  f'<div class="note">{e(n)}</div></li>' for t, s, d, u, n in CURATED)
    srcs = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(r)} list</a>' for r, u in ok) or "Hollywood North Buzz"
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{RUMOURS}}", rumours_html()).replace("{{ASOF}}", RUMOURS_ASOF).replace("{{SOON}}", soon_html)
            .replace("{{JUST}}", just_html).replace("{{CUR}}", cur).replace("{{SRCS}}", srcs)
            .replace("{{N}}", str(len(items))).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Post Buzz: what's heading into post in Canada — Post Production Canada</title>
<meta name="description" content="Canadian productions that are wrapping or just wrapped, so you can see what's heading into post.">
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
h2{font-size:24px;letter-spacing:-.02em;margin:36px 0 8px}
p{margin:0 0 12px}.lede{color:var(--mute);font-size:18px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:6px 18px;margin:12px 0}
.arts{list-style:none;padding:0;margin:0}.arts li{padding:12px 0;border-bottom:1px solid var(--line)}.arts li:last-child{border-bottom:0}
.arts a{font-weight:700;text-decoration:none}.arts a:hover{text-decoration:underline}
.when{color:var(--mute);font-size:13px;margin-left:6px}
.note{color:var(--mute);font-size:13.5px;margin-top:2px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a>
  <a class="btn" href="/">← Latest news</a>
</div></header>
<main class="wrap">
<h1>🎬 Post Buzz</h1>
<p class="lede">What's heading into post across Canada. When a production wraps, the edit, colour, sound and VFX come next, so end-of-shoot dates show where the work is about to land.</p>

<h2>🗣️ Rumour mill by province</h2>
<p>What might be coming, from the unions' own public listings. These are production titles, studios and dates only, as of {{ASOF}}. Schedules move, and a listing is not a promise of post work, so confirm with the production.</p>
{{RUMOURS}}

<h2>Wrapping in the next 90 days</h2>
<div class="box">{{SOON}}</div>

<h2>Wrapped in the last 45 days</h2>
<div class="box">{{JUST}}</div>
<p class="note">Shoot dates come from the public production lists on Hollywood North Buzz ({{SRCS}}), which are compiled by hand and can lag or change. Confirm with the production before you rely on a date. {{N}} productions were read for this page. Only public listings are used here, never unverified claims about people or companies.</p>

<h2>Worth a read</h2>
<div class="box"><ul class="arts">{{CUR}}</ul></div>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent and is not run by Hollywood North Buzz.</div></footer>
</body>
</html>
"""
