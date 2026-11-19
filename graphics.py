"""Shared artwork that says what the site believes: the Editor is an artist and the cut is where a story is made.
Craft claims are paraphrased from the L.A. Film School's visual storytelling guide and a long-standing filmmaking adage."""

def banner(kicker, headline):
    frames = [
        ("RHYTHM", '<path d="M8 40 L20 40 L26 14 L34 52 L42 24 L48 40 L72 40" fill="none" stroke="#ff5a4d" stroke-width="3" stroke-linejoin="round"/>'),
        ("TAKE", '<rect x="10" y="12" width="52" height="16" rx="3" fill="#ff5a4d"/><rect x="10" y="32" width="34" height="16" rx="3" fill="#9aa0ab"/><rect x="48" y="32" width="14" height="16" rx="3" fill="#ffb000"/>'),
        ("CUT", '<line x1="36" y1="6" x2="36" y2="58" stroke="#ffb000" stroke-width="3" stroke-dasharray="5 4"/><rect x="8" y="22" width="24" height="20" rx="3" fill="#9aa0ab"/><rect x="40" y="22" width="24" height="20" rx="3" fill="#ff5a4d"/>'),
        ("STORY", '<path d="M36 10 L42 28 L62 28 L46 40 L52 58 L36 47 L20 58 L26 40 L10 28 L30 28 Z" fill="#ffb000"/>'),
    ]
    cells = ""
    for i, (label, art) in enumerate(frames):
        x = 20 + i * 150
        cells += ('<g transform="translate(' + str(x) + ',58)"><rect width="130" height="86" rx="6" fill="#1e2127" stroke="#3a3d44"/>'
                  '<g transform="translate(29,8) scale(.9)">' + art + '</g>'
                  '<text x="65" y="80" text-anchor="middle" fill="#ffb000" font-family="ui-monospace,Menlo,monospace" font-size="11" letter-spacing="2">' + label + '</text></g>')
    holes = "".join('<rect x="' + str(10 + k * 24) + '" y="{y}" width="12" height="8" rx="2" fill="#f6f4ef" opacity=".85"/>' for k in range(25))
    top, bot = holes.replace("{y}", "10"), holes.replace("{y}", "162")
    return ('<figure class="ed-banner"><svg viewBox="0 0 620 180" role="img" aria-label="' + headline + '" xmlns="http://www.w3.org/2000/svg">'
            '<rect width="620" height="180" rx="14" fill="#0e0f12"/>' + top + bot + cells +
            '<text x="310" y="40" text-anchor="middle" fill="#ffb000" font-family="ui-monospace,Menlo,monospace" font-size="12" letter-spacing="3">' + kicker + '</text>'
            '</svg><figcaption><b>' + headline + '</b></figcaption></figure>')


def craft_cards():
    items = [
        ("⏱️", "Rhythm", "The pacing of the cuts sets the mood: quick cuts build urgency, longer ones let a moment breathe."),
        ("🎭", "Performance", "Choosing which take, and when to cut to a reaction, can change what a line or a look means."),
        ("✂️", "What stays out", "Some of the biggest decisions are omissions. What an Editor leaves out can hit harder than what is shown."),
    ]
    h = "".join('<div class="craft"><div class="ci">' + a + '</div><h3>' + b + '</h3><p>' + c + '</p></div>' for a, b, c in items)
    return ('<h2>The Editor is an artist</h2><p class="lede" style="font-size:16px">Editing is not assembly. It is where a film’s story, rhythm and emotion are decided. A long-standing filmmaking adage calls editing the final rewrite.</p>'
            '<div class="craftgrid">' + h + '</div><p class="note">Paraphrased from <a href="https://www.lafilm.edu/blog/the-film-students-guide-to-visual-storytelling" target="_blank" rel="noopener">The Film Student’s Guide to Visual Storytelling</a> (L.A. Film School) and <a href="https://www.heidimarshall.com/your-performance-in-the-edit-room" target="_blank" rel="noopener">Your Performance in the Editing Room</a>.</p>')


CSS = """
.ed-banner{margin:18px 0 6px}.ed-banner svg{width:100%;height:auto;display:block;border-radius:14px}.ed-banner figcaption{font-size:14px;color:var(--mute);margin-top:6px;text-align:center}
.craftgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:12px 0}
.craft{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px}.craft .ci{font-size:28px}.craft h3{margin:4px 0}.craft p{margin:0;font-size:14.5px;color:var(--mute)}
"""
