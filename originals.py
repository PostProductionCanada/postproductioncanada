"""Original articles: write Markdown files in articles/, the build turns them into pages.

No logins and no database. A file starting with "_" is ignored (templates). A file with `draft: true`
is not published (set INCLUDE_DRAFTS=1 when building locally to preview drafts).
Nothing appears on the site, not even a nav button, until at least one article is published.
"""
import html, os, re
from pathlib import Path

e = html.escape
TYPES = {"news": "News", "analysis": "Analysis", "opinion": "Opinion", "interview": "Interview"}


def parse(path):
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip('"\'')
        body = m.group(2)
    meta["slug"] = re.sub(r"[^a-z0-9-]+", "-", path.stem.lower()).strip("-")
    meta["draft"] = meta.get("draft", "").lower() in ("1", "true", "yes")
    meta["body"] = body
    return meta


def load(root):
    out = []
    d = Path(root) / "articles"
    if not d.exists():
        return out
    for p in sorted(d.glob("*.md")):
        if p.name.startswith("_"):
            continue
        a = parse(p)
        if a["draft"] and not os.environ.get("INCLUDE_DRAFTS"):
            continue
        if not a.get("title") or not a.get("date"):
            continue
        out.append(a)
    out.sort(key=lambda a: a["date"], reverse=True)
    return out


def count_published(root):
    return len(load(root))


def inline(s):
    s = e(s)
    def link(m):
        t, u = m.group(1), m.group(2)
        ext = ' target="_blank" rel="noopener"' if u.startswith("http") else ""
        return f'<a href="{u}"{ext}>{t}</a>'
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def md(text):
    out, para, items, quote = [], [], [], []

    def flush():
        nonlocal para, items, quote
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"); items = []
        if quote:
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>"); quote = []

    for line in text.splitlines():
        s = line.rstrip()
        if not s.strip():
            flush(); continue
        if s.startswith("### "):
            flush(); out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("## "):
            flush(); out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.strip() == "---":
            flush(); out.append("<hr>")
        elif s.startswith("- ") or s.startswith("* "):
            if para or quote: flush()
            items.append(s[2:])
        elif s.startswith("> "):
            if para or items: flush()
            quote.append(s[2:])
        else:
            if items or quote: flush()
            para.append(s.strip())
    flush()
    return "\n".join(out)


def render_all(leaf, favicon, updated, cfg, out_dir, root):
    arts = load(root)
    if not arts:
        return []
    byline_default = cfg.get("default_byline") or "Post Production Canada"
    contact = cfg.get("contact_email") or ""
    corr = (f'Spot a mistake? Email <a href="mailto:{e(contact)}">{e(contact)}</a> and we will correct it.' if contact
            else "Spot a mistake? A contact address for corrections is coming soon.")
    (Path(out_dir) / "originals").mkdir(exist_ok=True)
    cards = []
    for a in arts:
        typ = TYPES.get((a.get("type") or "analysis").lower(), "Analysis")
        by = a.get("byline") or byline_default
        disc = a.get("disclosure") or ""
        disc_html = f'<p class="disc"><b>Disclosure:</b> {inline(disc)}</p>' if disc else ""
        draft = '<span class="pill" style="background:#e0a100;color:#000">DRAFT</span> ' if a["draft"] else ""
        body = md(a["body"])
        page = (ART.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{TITLE}}", e(a["title"]))
                .replace("{{DESC}}", e(a.get("summary", ""))).replace("{{TYPE}}", e(typ)).replace("{{DRAFT}}", draft)
                .replace("{{BYLINE}}", e(by)).replace("{{DATE}}", e(a["date"])).replace("{{BODY}}", body)
                .replace("{{DISC}}", disc_html).replace("{{CORR}}", corr).replace("{{UPDATED}}", updated))
        (Path(out_dir) / "originals" / f'{a["slug"]}.html').write_text(page, encoding="utf-8")
        cards.append(f'<li><span class="pill">{e(typ)}</span> {draft}<a href="originals/{e(a["slug"])}.html"><b>{e(a["title"])}</b></a>'
                     f'<div class="note">{e(by)} · {e(a["date"])}</div><p>{e(a.get("summary", ""))}</p></li>')
    idx = (IDX.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{CARDS}}", "".join(cards))
           .replace("{{CORR}}", corr).replace("{{UPDATED}}", updated))
    (Path(out_dir) / "originals.html").write_text(idx, encoding="utf-8")
    return arts


CSS = """
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 ui-serif,Georgia,"Times New Roman",serif}
a{color:var(--red)}.wrap{max-width:720px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line);font-family:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink)}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none}
h1{font-family:ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:clamp(28px,5vw,40px);line-height:1.15;letter-spacing:-.02em;margin:30px 0 8px}
h2,h3{font-family:ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;letter-spacing:-.01em}
.pill{font:700 12px ui-sans-serif,sans-serif;background:var(--chip);border-radius:999px;padding:2px 10px;display:inline-block}
.meta,.note{color:var(--mute);font:14px ui-sans-serif,-apple-system,"Segoe UI",sans-serif}
blockquote{border-left:4px solid var(--red);margin:16px 0;padding:2px 16px;color:var(--mute)}
.badge{display:inline-block;font:700 11px ui-sans-serif,-apple-system,sans-serif;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--line);border-radius:99px;padding:2px 8px;margin-right:8px;color:var(--mute)}.badge.ed{color:#e8730c;border-color:#e8730c}.disc.legal{border-top:0;border-left:3px solid var(--line);padding:6px 12px;margin:0 0 18px}
.disc,.corr{font:14px/1.5 ui-sans-serif,-apple-system,sans-serif;color:var(--mute);border-top:1px solid var(--line);padding-top:12px;margin-top:28px}
ul.list{list-style:none;padding:0}ul.list li{padding:16px 0;border-bottom:1px solid var(--line)}ul.list a{text-decoration:none;font-size:20px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font:13px ui-sans-serif,sans-serif}
"""
HEAD = """<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLEFULL}}</title><meta name="description" content="{{DESC}}"><link rel="icon" href="{{FAVICON}}"><style>""" + CSS + """</style></head><body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/originals.html">Originals</a></div></header>"""
ART = HEAD.replace("{{TITLEFULL}}", "{{TITLE}} — Post Production Canada") + """
<main class="wrap"><p class="meta" style="margin:26px 0 0"><span class="pill">{{TYPE}}</span> {{DRAFT}}</p>
<h1>{{TITLE}}</h1><p class="meta">{{BYLINE}} · {{DATE}}</p>
{{BODY}}
{{DISC}}<p class="corr">{{CORR}}</p></main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent.</div></footer></body></html>"""
IDX = HEAD.replace("{{TITLEFULL}}", "Originals — Post Production Canada").replace("{{DESC}}", "Original articles on Canadian post-production.") + """
<main class="wrap"><h1>Originals</h1><p class="meta">Original writing on Canadian post-production.</p>
<ul class="list">{{CARDS}}</ul><p class="corr">{{CORR}}</p></main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent.</div></footer></body></html>"""
