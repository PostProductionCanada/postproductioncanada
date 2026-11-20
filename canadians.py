"""'Canadian Stories': editors, directors and craftspeople from Canada behind screens the world watches.

Every entry is built from the public sources linked on it, and the wording is our own summary.
To add one, append a dict to STORIES and rebuild.
"""
import html

e = html.escape

STORIES = [
    {"name": "Kubrick's Canadian connections", "roles": ["Directors", "Effects", "Voice"],
     "angle": "Work from the National Film Board of Canada that caught Stanley Kubrick's eye.",
     "story": ["Two NFB films found their way onto Stanley Kubrick's radar. Universe (1960), by Roman Kroitor and Colin Low, is reported to have been a touchstone while Kubrick and Arthur C. Clarke prepared 2001: A Space Odyssey, and Kubrick is said to have chosen its narrator, the Canadian actor Douglas Rain, as the voice of HAL 9000. He also hired Universe's effects designer, Wally Gentleman, though by one account Gentleman did not stay long.",
               "Earlier, for Dr. Strangelove, Kubrick wanted NFB filmmaker Arthur Lipsett, whose collage-style Very Nice, Very Nice (1961) was nominated for an Oscar, to direct the trailer."],
     "note": "These accounts come from memoirs, talks and articles, so treat the details as reported. If the story you have in mind is a different one, send us the name.",
     "sources": [("Stanley Kubrick, cinephile", "Sight and Sound (BFI)", "https://www.bfi.org.uk/sight-and-sound/stanley-kubrick-cinephile"),
                 ("How avant-garde NFB filmmaker Arthur Lipsett influenced Kubrick and Lucas", "NFB Blog", "https://blog.nfb.ca/blog/2012/10/03/how-lipsett-influenced-kubrick-lucas"),
                 ("The documentary roots of 2001 and the Canadian voice of HAL", "Gerry Flahive, Medium", "https://medium.com/@gflahive/im-sure-you-ll-agree-there-s-some-truth-in-what-i-say-the-documentary-roots-and-a-i-1eb994454d00")]},
    {"name": "Ronald Sanders", "letters": "CCE", "roles": ["Picture editor"], "prov": ["MB", "ON"],
     "angle": "Born in Winnipeg, based in Toronto, and David Cronenberg's regular editor since the late 1970s.",
     "story": ["Sanders came to picture editing through documentaries and sound editing, and cut his first feature in 1976. From the late 1970s he became the editor of most of David Cronenberg's films, a partnership that runs from Videodrome and The Fly through Crash, A History of Violence and Eastern Promises. He also cut the animated feature Coraline, which was nominated for an Oscar.",
               "His editing won Genie Awards for Dead Ringers, Crash, eXistenZ and Eastern Promises, and DGC Craft Awards for A History of Violence and Eastern Promises. He is a member of the Canadian Cinema Editors."],
     "credits": ["Videodrome", "The Dead Zone", "The Fly", "Dead Ringers", "Naked Lunch", "Crash", "eXistenZ", "Spider", "A History of Violence", "Eastern Promises", "Coraline", "A Dangerous Method", "Cosmopolis"],
     "sources": [("Ronald Sanders", "The Canadian Encyclopedia", "https://thecanadianencyclopedia.ca/en/article/ronald-sanders"),
                 ("Ronald Sanders (film editor)", "Wikipedia", "https://en.wikipedia.org/wiki/Ronald_Sanders_(film_editor)"),
                 ("Behind the Cut: Ronald Sanders", "ioncinema", "https://www.ioncinema.com/news/uncategorized/behind-the-cut-ronald-sanders-part-i")]},
    {"name": "Jean-Marc Vallée", "roles": ["Director", "Editor"], "prov": ["QC"],
     "angle": "Born in Montréal, and one of the few Canadian filmmakers to cross over to major Hollywood success.",
     "story": ["Vallée directed Dallas Buyers Club, Wild, Big Little Lies and Sharp Objects. He also edited much of his own work, credited under the name John Mac McMurphy, and under that name earned an Academy Award nomination for Best Film Editing on Dallas Buyers Club.",
               "He died in December 2021, aged 58."],
     "credits": ["C.R.A.Z.Y.", "The Young Victoria", "Dallas Buyers Club", "Wild", "Big Little Lies", "Sharp Objects"],
     "sources": [("Jean-Marc Vallée dies at 58", "ABC News", "https://abcnews.com/GMA/Culture/big-lies-director-jean-marc-vallee-dies-58/story?id=81955814"),
                 ("Jean-Marc Vallée", "Wikipedia", "https://en.wikipedia.org/wiki/Jean-Marc_Vall%C3%A9e"),
                 ("Jean-Marc Vallée (1963-2021)", "The Film Experience", "http://thefilmexperience.net/blog/2021/12/27/jean-marc-vallee-1963-2021.html")]},
    {"name": "Don Cassidy", "letters": "CCE", "roles": ["Picture editor"], "prov": ["ON"],
     "angle": "A Toronto-area editor who won a Primetime Emmy for cutting a HISTORY miniseries.",
     "story": ["Cassidy won the 2012 Primetime Emmy for Outstanding Single-Camera Picture Editing for a Miniseries or a Movie, for Part 2 of Hatfields & McCoys, produced for HISTORY. The Television Academy's database lists the win.",
               "Other credits include Rent-a-Goalie, The Kennedys and Vikings. IMDb lists him as a member of the Canadian Cinema Editors."],
     "credits": ["Rent-a-Goalie", "The Kennedys", "Hatfields & McCoys", "Vikings"],
     "sources": [("Don Cassidy: Emmy Awards and Nominations", "Television Academy", "https://emmys.com/node/224736"),
                 ("Don Cassidy", "IMDb", "https://www.imdb.com/name/nm0144183/")]},
    {"name": "Jay Prychidny", "letters": "CCE", "roles": ["Picture editor"], "prov": ["ON"],
     "angle": "A Canadian editor who cut Tim Burton's episodes of Wednesday and then Beetlejuice Beetlejuice.",
     "story": ["Prychidny edited all of Tim Burton's episodes of the Netflix series Wednesday and then reunited with Burton on the 2024 sequel Beetlejuice Beetlejuice. He won a Canadian Cinema Editors award for editing on Wednesday in 2023, according to the CCE's listing.",
               "Earlier, he won back-to-back Canadian Screen Awards in 2017 and 2018 for Orphan Black and The Amazing Race Canada, and a Gemini and a CCE award for Canada's Next Top Model in 2010/2011. He also produced on Orphan Black, The Next Step and Snowpiercer, and edited Scream VI, his first feature. We found no Emmy for him."],
     "credits": ["Orphan Black", "The Amazing Race Canada", "Wednesday", "Scream VI", "Beetlejuice Beetlejuice"],
     "sources": [("Jay Prychidny, CCE, joins Manhattan Edit Workshop as Artist in Residence", "MEWShop, Sept 2023", "https://www.mewshop.com/blog-news-and-press/wednesayr-editor-jay-prychidnyjoins-manhattan-edit-workshop-as-artist-in-residence-"),
                 ("Bringing Beetlejuice back from the afterlife with picture editor Jay Prychidny", "The Wider Lens", "https://thewiderlens.ca/series/creative-spotlight/bringing-beetlejuice-back-from-the-afterlife-with-picture-editor-jay-prychidny/")]},
    {"name": "Cam McLauchlin", "letters": "CCE", "roles": ["Picture editor"], "prov": ["ON"],
     "angle": "A Toronto editor who came up working with Guillermo del Toro and went on to cut Nightmare Alley.",
     "story": ["The CCE's Coffee with an Editor interview says McLauchlin spent his early career working with Guillermo del Toro as an assistant, associate editor and editor on Pacific Rim, Crimson Peak, The Strain and The Shape of Water, and was then cutting del Toro's Nightmare Alley.",
               "His other work includes The Void, Teen Spirit, The Kindness of Strangers and Clifton Hill, and the CCE credits him as editor on The Last Showgirl. He is a CSA and DGC nominated editor."],
     "credits": ["Pacific Rim", "Crimson Peak", "The Strain", "The Shape of Water", "Nightmare Alley", "Teen Spirit", "The Kindness of Strangers", "Clifton Hill", "The Last Showgirl"],
     "sources": [("Coffee with an Editor, Episode 009: Cam McLauchlin", "Canadian Cinema Editors", "https://cceditors.ca/2020/08/coffee-with-an-editor-cam-mclauchlin/")]},
    {"name": "Wendy Hallam Martin", "letters": "CCE, ACE", "roles": ["Picture editor"],
     "angle": "A Canadian editor, CCE and ACE, cutting one of the most talked-about series of its era.",
     "story": ["Hallam Martin won Best Editing in TV Drama at the 12th Canadian Cinema Editors Awards for The Handmaid's Tale, episode 403, \"The Crossing\"."],
     "credits": ["The Handmaid's Tale"],
     "sources": [("12th Annual CCE Awards nominees and winners", "Canadian Cinema Editors", "https://cceditors.ca/2022/05/the-12th-annual-cce-awards")]},
]


def _badge(name):
    try:
        import style
        b = style.imdb_badge(name)
        return "(" + b + ")" if b else ""
    except Exception:
        return ""


def card(s):
    roles = "".join(f'<span class="pill">{e(r)}</span> ' for r in s["roles"])
    paras = "".join(f"<p>{e(t)}</p>" for t in s["story"])
    cred = ""
    if s.get("credits"):
        cred = '<p class="note"><b>Credits:</b> ' + " · ".join(e(c) for c in s["credits"]) + "</p>"
    note = f'<p class="note">{e(s["note"])}</p>' if s.get("note") else ""
    src = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(o)}</span></li>' for t, o, u in s["sources"])
    pins = "".join(f'<span class="pill">📍 {e(p)}</span> ' for p in s.get("prov", []))
    return (f'<article class="box"><div>{roles}{pins}</div><h3 class="pname">{e(s["name"])}{(", " + e(s["letters"])) if s.get("letters") else ""} {_badge(s["name"])}</h3><p class="angle">🇨🇦 {e(s["angle"])}</p>'
            f'{paras}{cred}{note}<ul class="src">{src}</ul></article>')


def render(leaf, favicon, updated):
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon)
            .replace("{{CARDS}}", "".join(card(s) for s in STORIES)).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Canadian Stories: the editors and directors behind the screen — Post Production Canada</title>
<meta name="description" content="Stories of Canadian editors, directors and craftspeople behind movies and television the world watches.">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}.wrap{max-width:800px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0;flex-wrap:wrap;gap:10px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink);white-space:nowrap}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;white-space:nowrap}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}
h3{font-size:22px;margin:8px 0 2px;letter-spacing:-.01em}
.lede{color:var(--mute);font-size:18px}.nb{white-space:nowrap}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:16px 0}
.angle{color:var(--red);font-weight:600;margin:0 0 10px}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700}
.note{color:var(--mute);font-size:14px}.when{color:var(--mute);font-size:13px;margin-left:6px}
ul.src{list-style:none;padding:12px 0 0;margin:12px 0 0;border-top:1px solid var(--line)}ul.src li{margin:4px 0;font-size:14.5px}
.add{border-left:4px solid #e0a100}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/">← Latest news</a></div></header>
<main class="wrap">
<h1>🇨🇦 Canadian Stories</h1>
<p class="lede">Canadians have cut, directed and crafted a lot of the movies and television the world watches, often without anyone noticing. These are some of their stories.</p>
{{CARDS}}
<div class="box add"><h3>Got a story?</h3><p>If you know a Canadian editor, director or craftsperson with a great story, send us the name and we'll research it and add it here, with sources. A longer list is welcome too.</p></div>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent. Summaries are ours; every claim links to its source.</div></footer>
</body>
</html>
"""
