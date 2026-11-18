#!/usr/bin/env python3
"""Draft the weekly newsletter from the site's own content.

Run after build.py:   python3 make_newsletter.py
Writes drafts/newsletter-YYYY-MM-DD.html and .md (drafts/ is never published). You review, tweak, paste
into your newsletter service, and send. Nothing is sent automatically.

Design rule: short (about 200 words) and built to send readers back to the site.
"""
import html, json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import buzz

ROOT = Path(__file__).parent
SITE = "https://postproductioncanada.ca"
UTM = "?utm_source=newsletter&utm_medium=email&utm_campaign={d}"
e = html.escape


def main():
    now = datetime.now(timezone.utc)
    d = now.strftime("%Y-%m-%d")
    utm = UTM.format(d=d)
    cfg = json.loads((ROOT / "site.json").read_text())
    stories = json.loads((ROOT / "public" / "stories.json").read_text())
    picks = json.loads((ROOT / "curated.json").read_text()).get("picks", [])
    picks = sorted(picks, key=lambda p: p["date"], reverse=True)
    pick = picks[0] if picks else None

    week = now - timedelta(days=8)
    canada = [s for s in stories if s.get("canada") and datetime.fromisoformat(s["date"]) >= week]
    skip = {pick["title"].lower()} if pick else set()
    def _ok(s):
        return ("news.google.com" not in s["url"] and s["source"].isascii() and s["title"].isascii() is not None
                and s["title"].lower() not in skip)
    also = [s for s in canada if _ok(s)][:3]

    items, _ = buzz.gather()
    soon = sorted([i for i in items if now <= i["end"] <= now + timedelta(days=21)], key=lambda i: i["end"])[:3]

    subject = f"Canadian post this week: {len(canada)} stories" + (f", {len(soon)} shows wrapping soon" if soon else "")
    alts = ["What's heading into post in Canada", "Wrapping soon, post next: this week in Canadian post"]

    # ---- plain/markdown version
    md = [f"Subject: {subject}", f"Alternates: {alts[0]} | {alts[1]}",
          f"Preheader: {len(canada)} Canadian stories this week, and what's about to land in post.", "", "---", ""]
    if pick:
        md += [f"**Pick of the week**", f"[{pick['title']}]({pick['url']}) ({pick['source']})", pick.get("note", ""), ""]
    if soon:
        md += ["**Wrapping soon, post next**"]
        md += [f"- {i['title']} ({i['city'] or i['region']}), wraps {i['end'].strftime('%b %-d')}" for i in soon]
        md += [f"[See the full list]({SITE}/buzz.html{utm})", ""]
    if also:
        md += ["**Also this week**"] + [f"- [{s['title']}]({s['url']}) ({s['source']})" for s in also]
        md += [f"[All {len(canada)} Canadian stories this week]({SITE}/{utm}#canada)", ""]
    md += ["<!-- SPONSOR SLOT (optional): \"Presented by ...\" one line, clearly labelled -->", "",
           "---", f"You're getting this because you subscribed at postproductioncanada.ca. "
           f"{cfg.get('sender_name') or 'Post Production Canada'}, {cfg.get('mailing_address') or '[MAILING ADDRESS: add your PO box before sending]'}. "
           "[Unsubscribe link: your newsletter service adds this] · " + f"[Privacy]({SITE}/privacy.html)"]

    # ---- html version (simple, inline-styled, email-safe)
    def link(u, t): return f'<a href="{e(u)}" style="color:#d52b1e">{e(t)}</a>'
    h = ['<div style="max-width:560px;margin:0 auto;font:16px/1.55 Arial,Helvetica,sans-serif;color:#16181d">',
         '<h2 style="margin:0 0 4px">Post Production <span style="color:#d52b1e">Canada</span></h2>',
         f'<p style="color:#69707d;margin:0 0 18px">{len(canada)} Canadian stories this week, and what is about to land in post.</p>']
    if pick:
        h += ['<h3 style="margin:18px 0 4px">Pick of the week</h3>',
              f'<p style="margin:0 0 4px"><b>{link(pick["url"], pick["title"])}</b> <span style="color:#69707d">({e(pick["source"])})</span></p>',
              f'<p style="margin:0;color:#444">{e(pick.get("note", ""))}</p>']
    if soon:
        h += ['<h3 style="margin:18px 0 4px">Wrapping soon, post next</h3><ul style="padding-left:18px;margin:0">']
        h += [f'<li>{e(i["title"])} <span style="color:#69707d">({e(i["city"] or i["region"])}), wraps {i["end"].strftime("%b %-d")}</span></li>' for i in soon]
        h += ['</ul>', f'<p style="margin:6px 0 0">{link(SITE + "/buzz.html" + utm, "See the full list on the site →")}</p>']
    if also:
        h += ['<h3 style="margin:18px 0 4px">Also this week</h3><ul style="padding-left:18px;margin:0">']
        h += [f'<li>{link(s["url"], s["title"])} <span style="color:#69707d">({e(s["source"])})</span></li>' for s in also]
        h += ['</ul>', f'<p style="margin:6px 0 0">{link(SITE + "/" + utm + "#canada", f"All {len(canada)} Canadian stories this week →")}</p>']
    h += ['<!-- SPONSOR SLOT (optional): "Presented by ..." one line, clearly labelled -->',
          '<hr style="border:0;border-top:1px solid #e4e0d6;margin:22px 0 10px">',
          '<p style="font-size:12px;color:#69707d">You are getting this because you subscribed at postproductioncanada.ca. '
          f'{e(cfg.get("sender_name") or "Post Production Canada")}, {e(cfg.get("mailing_address") or "[MAILING ADDRESS: add your PO box before sending]")}. '
          f'[Unsubscribe link: your newsletter service adds this] · {link(SITE + "/privacy.html", "Privacy")}</p></div>']

    out = ROOT / "drafts"
    out.mkdir(exist_ok=True)
    (out / f"newsletter-{d}.md").write_text("\n".join(md), encoding="utf-8")
    (out / f"newsletter-{d}.html").write_text("\n".join(h), encoding="utf-8")
    words = len(" ".join(md).split())
    print(f"drafts/newsletter-{d}.md and .html written (about {words} words)")
    print("Subject:", subject)


if __name__ == "__main__":
    main()
