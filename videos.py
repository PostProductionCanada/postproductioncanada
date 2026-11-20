"""Latest videos from official YouTube channels, read from each channel's public Atom feed at build time.
Link cards only: no embeds and no thumbnails, so a visitor's browser does not contact YouTube until they click.
Channel IDs were checked by reading each feed's author name."""
import html, re, urllib.request
from datetime import datetime

e = html.escape
UA = "Mozilla/5.0 (compatible; PostProductionCanadaBot/1.0; +https://postproductioncanada.ca)"

# (label, area, channel id, channel page)
CHANNELS = [
    ("Avid", "Picture and sound", "UCVITunXO_-YkVUx-DrshzDg", "https://www.youtube.com/@avid"),
    ("Avid Pro Tools", "Sound", "UCthklhp3GozCN3aeBfiGYHQ", "https://www.youtube.com/@avidprotools"),
    ("Blackmagic Design", "Picture, colour, sound and VFX (DaVinci Resolve)", "UCufB8sMVyP9JEScMjLz74YA", "https://www.youtube.com/@BlackmagicDesignOfficial"),
    ("Adobe Video", "Premiere and After Effects", "UCzgPg1KhiJTzkxy0IUciRaQ", "https://www.youtube.com/@AdobeVideo"),
    ("Canadian Cinema Editors", "Canadian Editors (CCE)", "UCwOcN6RcgzRvAddQ5JqN4NQ", "https://www.youtube.com/@CanadianCinemaEditors"),
    ("Foundry", "VFX (Nuke)", "UCxn8WbrqCJl7G6i-yI_mFyg", "https://www.youtube.com/@FoundryTeam"),
    ("Unreal Engine", "Real-time and virtual production", "UCBobmJyzsJ6Ll7UbfhI4iwQ", "https://www.youtube.com/@UnrealEngine"),
]


def _fetch(cid, n=3):
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + cid
    try:
        xml = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=15).read().decode("utf8", "ignore")
    except Exception:
        return []
    out = []
    for ent in re.findall(r"<entry>(.*?)</entry>", xml, flags=re.S)[:n]:
        t = re.search(r"<title>(.*?)</title>", ent, re.S)
        v = re.search(r"<yt:videoId>(.*?)</yt:videoId>", ent)
        d = re.search(r"<published>(.*?)</published>", ent)
        if not (t and v):
            continue
        try:
            when = datetime.fromisoformat(d.group(1)).strftime("%b %-d, %Y") if d else ""
        except Exception:
            when = ""
        out.append((html.unescape(t.group(1)).strip(), "https://www.youtube.com/watch?v=" + v.group(1), when))
    return out


def shelf():
    """HTML for the 'latest from the makers' block. Empty channels are skipped."""
    blocks = ""
    for label, area, cid, page in CHANNELS:
        vids = _fetch(cid)
        if not vids:
            continue
        li = "".join('<li><a href="' + e(u) + '" target="_blank" rel="noopener">▶ ' + e(t) + '</a> <span class="note">' + e(w) + "</span></li>" for t, u, w in vids)
        blocks += ('<article class="box"><h3><a href="' + e(page) + '" target="_blank" rel="noopener">' + e(label) + "</a></h3>"
                   '<p class="note">' + e(area) + '</p><ul style="margin:6px 0 4px;padding-left:18px;list-style:none">' + li + "</ul></article>")
    if not blocks:
        return ""
    return ('<h3>Latest from the makers</h3><p class="note">Updated automatically from each channel\'s public feed. These are the companies\' own videos, so they promote their own tools.</p>' + blocks)
