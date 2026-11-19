"""Vibe Cutting: editing by telling the software what you want, and how AI connects to editing software.

Every item links to its source. Items marked "vendor" come from companies selling a related product, so read them as such.
"""
import html

e = html.escape

INTRO = ("Vibe cutting is editing by describing what you want in plain language and letting an AI carry out the steps in the software. "
         "The name borrows from \"vibe coding,\" the idea of building software by describing it instead of writing the code. "
         "In editing, the editor still decides what the cut should feel like. The AI takes on the mechanical work: organizing bins, "
         "making transcripts, building a first assembly, cleaning up.")

# (title, source, date, url, note, vendor?)
SECTIONS = [
    ("What people mean by vibe editing", [
        ("What is vibe editing?", "Tellers.AI glossary", "", "https://tellers.ai/video-editing-glossary/vibe-editing",
         "A short definition: expressing editorial intent in natural language while an AI video agent does the production work.", True),
        ("Vibe Editing: the complete guide to AI-driven video editing", "Pexo", "", "https://pexo.ai/blog/vibe-editing-complete-guide-2477",
         "Describes re-editing existing footage by describing the mood and style you want, and traces the term back to vibe coding.", True),
        ("You can use AI to edit videos for you, here's how", "Forward Future", "", "https://forwardfuture.com/newsletter/originals/you-can-use-ai-to-edit-videos-for-you-here-s-how",
         "A professional editor's guide to handing AI the busywork, directing it in plain English and keeping your taste in charge.", False),
        ("Vibe editing turns the video editor into a conversation", "TechBullion", "", "https://techbullion.com/vibe-editing-turns-the-video-editor-into-a-conversation",
         "A startup that edits by chat shows its plan before applying it and lets you undo each step. Treat it as company coverage.", True),
    ]),
    ("The software is opening up to AI", [
        ("Premiere AI Assistant (beta) overview", "Adobe Help", "2026-06-18", "https://helpx.adobe.com/premiere/desktop/premiere-ai-assistant/overview.html",
         "Adobe's own description: with plain-language prompts the assistant organizes bins, makes transcripts, detects slates, adds markers and builds stringouts and rough assemblies inside Premiere.", False),
        ("Adobe's Premiere updates bring more AI into the editing timeline", "DPReview", "", "https://www.dpreview.com/news/adobes-premiere-updates-bring-more-ai-into-the-editing-timeline",
         "The assistant gets more capable, editors can save repeatable instructions as slash-command \"skills,\" and Adobe previews local MCP connections so third-party AI agents can work in native Premiere projects.", False),
        ("Adobe Premiere Pro gets an AI agent, generative media and a new Color Mode", "Creative Bloq", "", "https://www.creativebloq.com/news/adobe-premiere-pro-is-getting-an-ai-agent-to-do-the-boring-editing-jobs",
         "A hands-on look at the agent applying effects across a whole sequence, plus the question of who used to do that repetitive work.", False),
        ("A quick look at how Adobe's new AI Assistant could streamline your workflows in Premiere", "No Film School", "", "https://nofilmschool.com/adobe-premiere-ai-assistant",
         "A practical take that notes the assistant uses Firefly generative credits, so it isn't free.", False),
        ("DaVinci Resolve 21.1 uses MCP to let AI assistants control the edit", "YMCinema", "2026-09-17", "https://ymcinema.com/2026/09/17/davinci-resolve-21-1-mcp-ai-assistants-control-edit/",
         "Resolve Studio now has a built-in MCP server, so an AI assistant can drive Resolve through its API.", False),
        ("DaVinci Resolve 21.1: AI editing with Claude and ChatGPT, tested", "YouTube", "", "https://www.youtube.com/watch?v=yRxmdTUh7GU",
         "A hands-on test. It explains that the agent works through Resolve's API, not the on-screen interface, so it can only do what the API allows, and that this needs the Studio version.", False),
        ("What's new in Avid Media Composer 2026.8", "Avid", "2026-08-31", "https://www.avid.com/resource-center/whats-new-avid-media-composer-2026-8",
         "Multicam Auto Cut driven by who is speaking, plus better transcript tools. Avid calls the direction agentic editing.", True),
        ("Autodesk adds AI assistant, MCP servers and Arnold viewport updates", "Post Perspective", "2026-11-18", "https://postperspective.com/",
         "Autodesk joins the move to AI assistants and MCP connections. See Post Perspective's latest for the full story.", False),
        ("IBC2026: A-Z of exhibitor news", "SVG Europe", "", "https://www.svgeurope.org/blog/headlines/ibc2026-a-z-of-exhibitor-news",
         "Shows how widespread the shift is: for example, SNS's on-premise AI suite takes plain-language requests and can assemble an EDL from matching clips.", False),
    ]),
    ("What it means for editors", [
        ("AI in post-production: how to use it and where it saves time", "Runway", "", "https://runway.com/resources/ai-post-production",
         "Argues AI saves the most time on ingest, assembly and cleanup, while picture lock and the final mix stay mostly human decisions.", True),
        ("Will AI replace video editors? What the post-production data shows", "Coursiv", "2026-09-10", "https://coursiv.io/blog/will-ai-replace-video-editors",
         "Argues the mechanical layer of editing has largely been automated, and the market is splitting. It uses US employment figures.", True),
    ]),
    ("The Canadian angle", [
        ("Directors Guild of Canada calls for AI protections", "The Hollywood Reporter", "", "https://www.hollywoodreporter.com/business/business-news/directors-guild-canada-ai-protections-1236623437",
         "The DGC, which represents editors among others, issued a manifesto at the Banff World Media Festival on consent, attribution and control over creative work in the age of AI.", False),
    ]),
]


def render(leaf, favicon, updated):
    secs = []
    for head, items in SECTIONS:
        lis = "".join(
            f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(s)}{", " + e(d) if d else ""}</span>'
            + (' <span class="pill">vendor</span>' if v else "")
            + f'<div class="note">{e(n)}</div></li>' for t, s, d, u, n, v in items)
        secs.append(f"<h2>{e(head)}</h2><div class=\"box\"><ul class=\"arts\">{lis}</ul></div>")
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{INTRO}}", e(INTRO))
            .replace("{{SECTIONS}}", "".join(secs)).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vibe Cutting: AI and editing software — Post Production Canada</title>
<meta name="description" content="Editing by telling the software what you want: articles on AI assistants, agents and MCP in Premiere, Resolve and Avid, and what it means for editors.">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}.wrap{max-width:820px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0;flex-wrap:wrap;gap:10px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink);white-space:nowrap}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;white-space:nowrap}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}
h2{font-size:22px;letter-spacing:-.02em;margin:34px 0 8px}
.lede{color:var(--mute);font-size:18px}.note{color:var(--mute);font-size:14px;margin-top:2px}.when{color:var(--mute);font-size:13px;margin-left:6px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:6px 18px;margin:10px 0}
.arts{list-style:none;padding:0;margin:0}.arts li{padding:12px 0;border-bottom:1px solid var(--line)}.arts li:last-child{border-bottom:0}.arts a{font-weight:700;text-decoration:none}.arts a:hover{text-decoration:underline}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:1px 8px;font-size:11.5px;font-weight:700}
.add{border-left:4px solid #e0a100;padding:12px 18px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/">← Latest news</a></div></header>
<main class="wrap">
<h1>🎚️ Vibe Cutting</h1>
<p class="lede">{{INTRO}}</p>
<p class="note">Items marked <span class="pill">vendor</span> come from companies that sell a related product, so read them with that in mind. Summaries are mine, and each item links to its source.</p>
{{SECTIONS}}
<div class="box add"><b>Original articles on this are coming.</b> Have a view, a tool you've tried, or a story from the edit suite? Send it along and it may shape the first pieces.</div>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent and is not run by any software company listed.</div></footer>
</body>
</html>
"""
