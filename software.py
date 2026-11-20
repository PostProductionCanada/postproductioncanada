"""Editing software page: a short history, the main tools by picture / sound / VFX, Canadian-made software,
VFX Editors and the VFX houses, and where Assistant Editors can start.

Every line links to a source. Versions and news were read on AS_OF. Hand-maintained.
Icons are simple emoji, not company logos (logos are trademarks).
"""
import html
import topics, provinces

e = html.escape
AS_OF = "November 19, 2026"

HISTORY = [
    ("Before 1971", "🎞️", "Film editing was a mechanical craft: Editors cut and joined strips of celluloid by hand, on tools such as the Moviola and the flatbed.",
     "https://www.local695.com/magazine/nonlinear-editing-platforms", "IATSE Local 695"),
    ("1971", "🖥️", "The CMX 600, a joint venture of CBS and Memorex, is the first truly non-linear editor. It has two monitors, a light pen and disk packs the size of washing machines.",
     "https://en.wikipedia.org/wiki/Non-linear_editing", "Wikipedia"),
    ("1984", "💽", "Lucasfilm's EditDroid, built on a bank of LaserDiscs, shows at NAB. It lays the groundwork for bins and a timeline.",
     "https://www.simonsaysai.com/blog/the-history-of-non-linear-editing", "Simon Says"),
    ("1989", "🧲", "The EMC2 and then Avid's Avid/1, the first Media Composer, arrive within weeks of each other. Lightworks is also created this year, in the UK, by Paul Bamborough, Nick Pollock and Neil Harris.",
     "https://en.wikipedia.org/wiki/Non-linear_editing", "Wikipedia"),
    ("1991", "🍁", "Discreet Logic is founded in Montréal. Its Flame, Inferno and Smoke systems become a mainstay of visual effects and finishing. Lightworks appears in a London facility the same year.",
     "https://en.wikipedia.org/wiki/Autodesk_Media_and_Entertainment", "Wikipedia"),
    ("1992 to 93", "📀", "Storage is the barrier. Until 1992 a Mac could reach only about 50 GB at once. By February 1993 a Disney Channel team had Media Composer reaching over seven terabytes, and long-form feature editing became possible. Within a year thousands of systems had replaced 35mm editing equipment in studios and TV stations.",
     "https://en.wikipedia.org/wiki/Non-linear_editing", "Wikipedia"),
    ("1999", "🤝", "Autodesk agrees to buy Discreet Logic for about US$520 million. The unit stays in Montréal.",
     "https://www.techmonitor.ai/analysis/discreet_logic_to_be_acquired_by_autodesk_for_520m", "Tech Monitor"),
    ("2014", "🍁", "Blackmagic Design buys eyeon Software of Toronto, maker of the Fusion compositor. Fusion now lives inside DaVinci Resolve.",
     "https://www.fxguide.com/quicktakes/eyeon-software-acquired-by-blackmagic-design", "fxguide"),
    ("2026", "🤖", "Agentic and AI-assisted tools arrive in every major editor, and Premiere, Resolve, Media Composer and Final Cut all shipped major updates this year.",
     "#now", "See below"),
]

# area -> list of (icon, name, status line, official link, link label, canadian?)
PICTURE = [
    ("🅰️", "Avid Media Composer", "Media Composer 2026.8 shipped Aug 31, 2026, with Shared Projects, an AI multicam auto cut and a free Media Composer First tier. Third-party bin locking moved to the Enterprise tier, so check storage before upgrading.",
     "https://www.avid.com/resource-center/whats-new-avid-media-composer-2026-8", "Avid: what's new", False),
    ("🅿️", "Adobe Premiere", "Premiere 27.0 arrived Nov 10, 2026. Color Mode is a new grading workspace next to the edit, and the Lumetri Color panel is retired.",
     "https://helpx.adobe.com/premiere/desktop/whats-new/whats-new.html", "Adobe: what's new", False),
    ("🟦", "DaVinci Resolve", "Resolve 21 went final in June 2026, with the Photo page, new AI tools and Fairlight folder tracks. The free version is a full editor; Studio is a one-time $295 US licence.",
     "https://www.blackmagicdesign.com/products/davinciresolve", "Blackmagic Design", False),
    ("🍎", "Final Cut Pro", "Now part of Apple Creator Studio ($12.99 a month, from Jan 28, 2026), and still sold once for $299.99. October 2026 added AI and cross-app tools.",
     "https://www.apple.com/final-cut-pro", "Apple", False),
    ("💡", "Lightworks", "Owned by LWKS Software since September 2020. Free, Create and Pro versions; 2025.1 was a major release. Created in the UK in 1989.",
     "https://lwks.com", "Lightworks", False),
]
SOUND = [
    ("🎚️", "Avid Pro Tools", "Pro Tools 2026.11 (Nov 3, 2026; 2026.11.1 on Nov 18) adds Extensions, a built-in Stem Separator and High DPI on Windows. Earlier in 2026, 2026.4 added MPEG-H immersive mixing.",
     "https://www.avid.com/pro-tools/whats-new", "Avid: what's new", False),
    ("🟦", "Fairlight (in DaVinci Resolve)", "The audio post page inside Resolve. Resolve 21 added Fairlight folder tracks.",
     "https://www.blackmagicdesign.com/products/davinciresolve/fairlight", "Blackmagic Design", False),
    ("🎼", "Steinberg Nuendo", "A post-sound workstation used for film, TV and games. Current version not checked this round.",
     "https://www.steinberg.net/nuendo/", "Steinberg", False),
    ("🔊", "REAPER", "A low-cost workstation many sound Editors use. Current version not checked this round.",
     "https://www.reaper.fm", "REAPER", False),
]
VFX = [
    ("☢️", "Foundry Nuke", "Nuke 17.0 came out Feb 26, 2026 (Gaussian Splat support, a USD-based 3D system). Nuke 18.0 entered open beta in October 2026.",
     "https://www.foundry.com/news-and-awards/foundry-releases-nuke-17-advancing-compositing-workflows", "Foundry", False),
    ("🍁", "Blackmagic Fusion", "Fusion Studio 21.1 shipped Sept 9, 2026. It began as eyeon Fusion in Toronto and is also built into Resolve.",
     "https://www.cgchannel.com/2026/09/blackmagic-design-releases-fusion-studio-21", "CG Channel", True),
    ("🍁", "SideFX Houdini", "Made by Side Effects Software of Toronto. Houdini 21 is current; SideFX previewed Houdini 22 in June 2026, according to a market report.",
     "https://www.sidefx.com", "SideFX", True),
    ("🔥", "Autodesk Flame", "The descendant of Discreet Logic's Flame, born in Montréal. Flame 2026.2 is the latest we found, with OpenColorIO support.",
     "https://www.autodesk.com/products/flame", "Autodesk", True),
    ("🍁", "Autodesk Maya", "The 3D package that grew out of Alias, a Toronto company, and Wavefront.",
     "https://www.autodesk.com/products/maya", "Autodesk", True),
    ("🎬", "Adobe After Effects", "The layer-based compositor that pairs with Premiere.",
     "https://www.adobe.com/products/aftereffects.html", "Adobe", False),
]

# Video shelf: (title as on YouTube, channel, kind, why it is here, url). Link cards only: no embeds, no thumbnails,
# so a visitor's browser does not contact YouTube until they click. Added from titles and channel names; not every claim in a video is checked.
VIDEOS = [
    ("Avid's Ready to Edit helps editors sync media, transcribe and align dialogue, and organize bins", "Avid", "Official",
     "Ready to Edit is a new Media Composer 2026.8 feature, so this is the maker explaining its own tool.", "https://www.youtube.com/watch?v=fsgiOpNZDEM"),
    ("DaVinci Resolve Motion Graphics will never be the same...", "MrAlexTech", "Creator's opinion",
     "Resolve 21 added a large set of motion graphics tools to Fusion. This is one creator's take on them, not an official source.", "https://www.youtube.com/watch?v=Txilg-667Ac"),
]

HOUSES = [
    ("BC", "Image Engine (founded in Vancouver in 1995, merged with Cinesite in 2015), The Embassy, Zoic Studios, plus Vancouver outposts of Wētā FX, ILM, Framestore, DNEG, Pixomondo, Sony Imageworks, Digital Domain and Scanline VFX (owned by Netflix)."),
    ("QC", "Rodeo FX (Montréal, with a Québec City studio), plus Montréal branches of Framestore, DNEG, MPC, Pixomondo, Sony Imageworks, Digital Domain, Crafty Apes and Scanline VFX."),
    ("ON", "Spin VFX, Rocket Science VFX, Soho VFX, Folks VFX and Guru Studio in Toronto, a Rodeo FX studio (opened in Toronto's Liberty Village in 2022), plus DNEG, Tippett Studio and Ghost VFX."),
]

CHAIN = [
    ("1", "Cut with temps", "The Editor cuts with storyboards, previs and rough placeholders. A VFX Editor or Assistant builds quick temp composites, often called slap comps."),
    ("2", "Turnover", "The VFX Editor tracks every effects shot with an ID, then packages plates, frame handles, reference video, retime data, notes and count sheets for the vendor."),
    ("3", "Vendor works", "A VFX house (Rodeo FX, Image Engine, Folks and others) builds the shot in tools such as Nuke, Houdini, Flame or Fusion."),
    ("4", "Versions come back", "The VFX Editor cuts each version into the timeline, checks plate, length, colour and handles, and reviews it with the Editor and director."),
    ("5", "Notes and finals", "Notes go back to the vendor. Final shots are checked and sent to the colour finish (the DI), with the right version of every shot."),
]


def _row(items):
    out = ""
    for ic, nm, st, u, lb, ca in items:
        tag = ' <span style="background:#8a1710;color:#fff;border-radius:999px;font:700 11px/1 sans-serif;padding:3px 8px">🍁 Canadian-made</span>' if ca else ""
        out += ('<article class="box"><h3>' + ic + " " + e(nm) + tag + "</h3><p>" + e(st) + '</p><a href="' + e(u)
                + '" target="_blank" rel="noopener">' + e(lb) + " →</a></article>")
    return out


def render(leaf, favicon, updated):
    css = ("<style>.sw{list-style:none;margin:20px 0;padding:0 0 0 26px;border-left:3px solid var(--red)}.sw li{position:relative;margin:0 0 20px;padding:0 0 0 14px}"
           ".sw li::before{content:'';position:absolute;left:-36px;top:5px;width:14px;height:14px;border-radius:50%;background:var(--bg);border:3px solid var(--red)}"
           ".sw b{font:800 17px ui-monospace,Menlo,monospace;color:var(--red)}.sw p{margin:4px 0 2px}.sw a{font-size:13px}"
           ".ch{counter-reset:c;list-style:none;padding:0}.ch li{margin:0 0 12px;padding:12px 14px 12px 54px;position:relative;background:var(--panel);border:1px solid var(--line);border-radius:12px}"
           ".ch li span{position:absolute;left:14px;top:10px;width:28px;height:28px;border-radius:50%;background:var(--red);color:#fff;display:grid;place-items:center;font-weight:800}"
           ".ch b{display:block}</style>")
    hist = "".join('<li><b>' + e(y) + '</b> ' + ic + '<p>' + e(t) + '</p><a href="' + e(u) + '"' + ('' if u.startswith('#') else ' target="_blank" rel="noopener"')
                   + '>' + e(l) + '</a></li>' for y, ic, t, u, l in HISTORY)
    vids = "".join('<article class="box"><h3>▶ <a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a></h3>'
                   '<p class="note">' + e(ch) + ' · <b>' + e(k) + '</b></p><p>' + e(w) + '</p></article>' for t, ch, k, w, u in VIDEOS)
    houses = "".join('<article class="box"><p>' + provinces.badge(p) + " " + e(t) + "</p></article>" for p, t in HOUSES)
    chain = "".join('<li><span>' + n + '</span><b>' + e(h) + '</b>' + e(t) + '</li>' for n, h, t in CHAIN)
    body = (css
            + '<p>Editing started as a hands-on craft and became a computer craft in a few years. This page tells that story, then lists the main tools for picture, sound and visual effects, with what is new in each. '
              'Versions and news were read from the makers\' own pages on ' + e(AS_OF) + '. Icons are simple emoji, not company logos.</p>'
            + '<h2>💻 A short history: from film to digital</h2><ol class="sw">' + hist + '</ol>'
            + '<div class="box"><b>About Lightworks.</b> It is often remembered as Canadian, but every source we found says it was created in the UK in 1989 and first appeared in a London facility in 1991. We could not find a source for a Canadian origin. If you have one, send it to '
              '<a href="mailto:hello@postproductioncanada.ca?subject=Lightworks">hello@postproductioncanada.ca</a> and we will add it.</div>'
            + '<h2 id="now">🎬 Picture editing</h2>' + _row(PICTURE)
            + '<h2>🔊 Sound</h2>' + _row(SOUND)
            + '<h2>✨ Visual effects</h2><p class="note">🍁 marks software with Canadian roots: Discreet Logic (Montréal), eyeon (Toronto), Side Effects (Toronto) and Alias (Toronto).</p>' + _row(VFX)
            + '<h2>📺 Watch</h2><p class="note">Links open YouTube in a new tab. Nothing loads from YouTube until you click. Know a good video? Send it to hello@postproductioncanada.ca.</p>' + vids
            + '<h2>🍁 Made in Canada</h2><div class="box"><ul>'
              '<li><b>Discreet Logic, Montréal, 1991.</b> Flame, Inferno and Smoke, later bought by Autodesk.</li>'
              '<li><b>Softimage, Montréal.</b> The 3D company Discreet Logic\'s founder came from.</li>'
              '<li><b>eyeon Software, Toronto.</b> Fusion, now owned by Blackmagic Design.</li>'
              '<li><b>Side Effects Software, Toronto, 1987.</b> Houdini.</li>'
              '<li><b>Alias, Toronto.</b> Merged with Wavefront; Maya came out of the merger.</li></ul>'
              '<p class="note">Sources: <a href="https://en.wikipedia.org/wiki/Autodesk_Media_and_Entertainment" target="_blank" rel="noopener">Wikipedia</a>, '
              '<a href="https://www.fxguide.com/quicktakes/eyeon-software-acquired-by-blackmagic-design" target="_blank" rel="noopener">fxguide</a>, '
              '<a href="https://www.sidefx.com" target="_blank" rel="noopener">SideFX</a>.</p></div>'
            + '<h2>🟩 VFX Editors and the VFX houses</h2>'
              '<p>A VFX Editor sits in editorial and is the link between the picture edit and the VFX houses. They track every effects shot, send the vendors what they need, and cut the returning versions into the timeline so the Editor and director can judge them. '
              'The role is described in detail in <a href="https://www.screenskills.com/media/wzebbx0u/vfx-editor-skills-checklist.pdf" target="_blank" rel="noopener">ScreenSkills\' VFX Editor skills checklist</a> and in '
              '<a href="https://www.evanschiff.com/articles/feature-turnover-guide-vfx" target="_blank" rel="noopener">Editor Evan Schiff\'s turnover guide</a>.</p>'
            + '<ol class="ch">' + chain + '</ol>'
            + '<h3>Where the VFX houses are</h3>' + houses
            + '<p class="note">Studio lists are from <a href="https://vfxvoice.com/vfx-in-canada-a-global-leader-continues-to-evolve" target="_blank" rel="noopener">VFX Voice\'s guide to VFX in Canada</a>. Studios open, merge and close often, so check each one\'s own site.</p>'
            + '<h2>🎓 For Assistant Editors</h2><div class="box"><ul>'
              '<li>Start with our <a href="editors.html#assistants">Assistant Editors section</a>: the Core Agreement rules, interviews and the 2026 Recognition winners.</li>'
              '<li>Learn for free: <a href="https://www.blackmagicdesign.com/event/davinci-resolve-online-seminars" target="_blank" rel="noopener">Blackmagic\'s online Resolve seminars</a>, the free tier of Resolve, and the free Media Composer First from Avid.</li>'
              '<li>Meet people: the <a href="networking.html">Networking page</a> lists CCE socials, talks and EditCon, and the CCE runs a mentorship program (see <a href="https://cceditors.ca" target="_blank" rel="noopener">cceditors.ca</a>).</li>'
              '<li>Know the VFX side: the ScreenSkills checklist above lists what a VFX Editor is expected to do, shot by shot.</li></ul></div>'
            + '<p class="note">Something out of date or missing? Email <a href="mailto:hello@postproductioncanada.ca?subject=Software">hello@postproductioncanada.ca</a> with a link to the maker\'s page.</p>')
    return topics._page(leaf, favicon, updated, "Editing Software",
                        "A short history of editing software from film to digital, plus the main picture, sound and VFX tools, what is new in each, and the Canadian-made ones.",
                        "💻 Editing Software", "From film strips to timelines, and what each tool is doing now.", body)
