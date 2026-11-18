"""Plain-language privacy page. Not legal advice: have it reviewed before you rely on it."""
import html
e = html.escape


def render(leaf, favicon, updated, cfg):
    contact = (f'<p>Questions or want your email removed? Write to <a href="mailto:{e(cfg["contact_email"])}">{e(cfg["contact_email"])}</a>.</p>'
               if cfg.get("contact_email") else "")
    sender = ""
    if cfg.get("mailing_address"):
        sender = f'<p>The newsletter is sent by {e(cfg.get("sender_name") or "Post Production Canada")}, {e(cfg["mailing_address"])}.</p>'
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{CONTACT}}", contact)
            .replace("{{SENDER}}", sender).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy — Post Production Canada</title>
<meta name="robots" content="index,follow">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}.wrap{max-width:720px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink)}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none}
h1{font-size:34px;letter-spacing:-.02em;margin:30px 0 8px}h2{font-size:20px;margin:28px 0 6px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/">← Latest news</a></div></header>
<main class="wrap">
<h1>Privacy</h1>
<p>Short version: we collect almost nothing, we don't run ads, and we never sell anything about you.</p>

<h2>Visiting the site</h2>
<p>This site counts visits with a privacy-friendly tool that uses no cookies and does not build profiles of individual visitors. It records things like which pages are viewed, where visitors came from and what kind of browser they use. There are no accounts, no ads and no advertising trackers.</p>

<h2>The newsletter</h2>
<p>If you subscribe, we collect your email address so we can send you the newsletter, and nothing else. By subscribing you agree to receive it. Your address is held by the email service we use to send it, and it is used only for the newsletter. We do not sell or share it. Every email has an unsubscribe link, and we stop sending within 10 business days of your request, usually immediately.</p>
{{SENDER}}

<h2>Links to other sites</h2>
<p>Most stories link to the original publisher. Once you click through, that site's own privacy practices apply.</p>

{{CONTACT}}
<p style="color:var(--mute);font-size:14px">This page is a plain-language summary and is not legal advice. Updated {{UPDATED}}.</p>
</main>
<footer><div class="wrap">Post Production Canada is independent.</div></footer>
</body>
</html>
"""
