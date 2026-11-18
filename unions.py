"""'Who represents editors, by province' page: a clickable tile map of Canada.

Every entry comes from a public source listed beside it. Where I could not confirm something it says so.
Coverage depends on the production: many editors work non-union, and some work under more than one
agreement. This is a starting point, not a substitute for asking the union or guild directly.
The CCE is a non-profit association and is NOT a union, so it appears only under "post community".
"""
import html, json

e = html.escape

DGC_CORE = "https://cmpa.ca/wp-content/uploads/2023/10/2023-2025-DGC-Core-Agreement-FULLY-EXECUTED.pdf"
DGC_MAR = "https://cmpa.ca/wp-content/uploads/2024/01/2023-2025-DGC-Schedule-2-DGC-Martimes-FULLY-EXECUTED-revised-01.11.2024.pdf"
AB_PAGE = "https://www.alberta.ca/film-production-resources"
YTG = "https://emrlibrary.gov.yk.ca/EcDev/film-production-guide-yukon-2010.pdf"
CP = "https://creativepathwayscanada.com/about/people/unions-and-guilds"
CORE_NOTE = "Signatory to the DGC–CMPA Core Agreement, which has Picture Editing Department provisions."

# tile position (col, row) on an approximate grid
PROV = {
    "YT": {"name": "Yukon", "pos": (0, 0)}, "NT": {"name": "Northwest Territories", "pos": (1, 0)},
    "NU": {"name": "Nunavut", "pos": (2, 0)},
    "BC": {"name": "British Columbia", "pos": (0, 1)}, "AB": {"name": "Alberta", "pos": (1, 1)},
    "SK": {"name": "Saskatchewan", "pos": (2, 1)}, "MB": {"name": "Manitoba", "pos": (3, 1)},
    "ON": {"name": "Ontario", "pos": (4, 1)}, "QC": {"name": "Québec", "pos": (5, 1)},
    "NL": {"name": "Newfoundland & Labrador", "pos": (7, 1)},
    "NB": {"name": "New Brunswick", "pos": (6, 2)}, "PE": {"name": "Prince Edward Island", "pos": (7, 2)},
    "NS": {"name": "Nova Scotia", "pos": (8, 2)},
}

U = lambda name, role, url: {"name": name, "role": role, "url": url}

MARITIMES = [
    U("DGC Maritimes Regional Council", "Covers New Brunswick, Nova Scotia and PEI. Its agreement with the CMPA includes a Picture Editing Department.", DGC_MAR),
    U("IATSE Local 849", "Represents motion picture technicians in Nova Scotia, New Brunswick and PEI. Editing coverage not confirmed.", "https://www.iatse849.com/"),
]

DATA = {
    "BC": {"unions": [
        U("IATSE Local 891", "Represents motion picture workers in BC and the Yukon. Editing is one of its 19 departments. Over 9,000 members (its own pages give figures from 9,000 to over 10,000).", "https://www.iatse.com/"),
        U("ACFC West, Local 2020 Unifor", "A technical film union recognized by the BC Labour Board, with Editing among its departments. Supplies crew for smaller-budget features and movies of the week.", "https://www.acfcwest.com/about-us"),
        U("DGC British Columbia", "Covers directors, assistant directors, production and location managers and PAs. Editors are not on that list.", CP)],
        "post": [U("Vancouver Post Alliance", "Non-profit association for BC's post-production industry.", "https://vancouverpostalliance.com/"),
                 U("LOOK 891", "IATSE 891's showcase of its picture and sound editors.", "https://damngoodeditors.com")],
        "read": [("Local 891 Editor Gary Lam Talks Career and Pride in His Asian Heritage", "IATSE", "2021-05-27",
                  "https://iatse.net/local-891-editor-gary-lam-talks-career-and-pride-in-his-asian-heritage",
                  "A profile of a Local 891 first assistant editor who co-chairs its Editing Department and sits on its negotiating committee."),
                 ("Editing Department application: First Assistant Editor", "IATSE 891", "",
                  "https://iatse.com/_content/documents/public/Application%20forms/EDT_FIRST%20ASSIST%20EDITOR.pdf",
                  "What Local 891 asks for to join as a first assistant editor, including paid days worked and Avid skills."),
                 ("About ACFC West", "ACFC West", "", "https://www.acfcwest.com/about-us", "How the union describes itself and the departments it represents.")],
        "note": "Some BC workers hold cards in more than one union (\"dual card\"), according to Creative Pathways."},
    "YT": {"unions": [U("IATSE Local 891", "Its charter covers British Columbia and the Yukon. Editing-specific coverage in the Yukon not confirmed.", "https://www.iatse.com/")],
        "post": [U("Northern Film and Video Industry Association (NFVIA)", "Works to supply trained crew and gear for Yukon productions.", YTG),
                 U("Yukon Film Society", "Supports Yukon media artists with equipment and workshops, including editing courses, and runs the Available Light Film Festival.", YTG)],
        "read": [("Yukon Film Production Guide", "Government of Yukon", "2010", YTG, "An older guide to Yukon's film organizations. The groups may have changed, so check their current status.")]},
    "AB": {"unions": [
        U("DGC Alberta", "The Alberta government describes it as covering all areas of production, design and editing. " + CORE_NOTE, AB_PAGE),
        U("IATSE Locals 210 (Edmonton) and 212 (Calgary)", "Represent stage and film technicians across Alberta, per the Alberta government. Editing coverage not confirmed.", AB_PAGE)],
        "post": [U("Alberta Post Production Association", "Non-profit association. The Alberta government points producers to it for finding a post facility. Its own site would not load for me, so I haven't linked it.", AB_PAGE)],
        "read": [("We'll Fix It in Post: Post-Production in Alberta (panel)", "Calgary International Film Festival", "2026",
                  "https://www.ciffcalgary.ca/films/2026/well-fix-it-in-post-post-production-in-alberta",
                  "A 2026 industry panel on mentorship, paid assisting roles, a more connected post community and AI in the edit suite."),
                 ("Local film and television sector thriving with help of Alberta Media Fund grants", "CTV News", "",
                  "https://www.ctvnews.ca/calgary/article/local-film-and-television-sector-thriving-with-help-of-alberta-media-fund-grants",
                  "Covers Alberta's screen program, which has a stream for post-production."),
                 ("Film production resources", "Alberta.ca", "", AB_PAGE, "The government's guide to Alberta's unions, post community and incentives.")]},
    "SK": {"unions": [U("DGC Saskatchewan District Council", CORE_NOTE, DGC_CORE)], "post": [], "read": []},
    "MB": {"unions": [
        U("DGC Manitoba District Council", "Film Training Manitoba says DGC Manitoba represents sound and picture editors, along with directors, assistant directors, locations and production office. About 200 members and 250 permittees across all its classifications, per Manitoba Film & Music. " + CORE_NOTE, "https://www.getonsetmanitoba.com/dgc-mb"),
        U("IATSE Local 856", "Represents Manitoba crafts such as art, costume, grip, lighting and sound, but Editing is not among its listed departments. About 543 members and 964 permittees across all departments.", "https://www.iatse856.com")],
        "post": [U("On Screen Manitoba", "The industry association for 2,000+ filmmakers, crew, unions and service suppliers. Its members include DGC Manitoba and IATSE 856.", "https://www.onscreenmanitoba.com"),
                 U("Film Training Manitoba", "Non-profit sector council that runs the courses required for DGC Manitoba and IATSE 856 membership. Partner for EditCon in Winnipeg.", "https://filmtraining.mb.ca/entry-workshops"),
                 U("Urban Post Production", "A Toronto post house with a sister location in Winnipeg (sound editorial, mixing, picture finishing and more).", "https://urbanpost.ca")],
        "read": [("Entry-level tips: getting a job on a DGC Manitoba or IATSE 856 shoot", "Film Training Manitoba", "",
                  "https://filmtraining.mb.ca/entry-workshops",
                  "A plain explanation of which departments each union covers in Manitoba, including editors under the DGC."),
                 ("Key contacts: local unions and guilds", "Manitoba Film & Music", "", "https://www.mbfilmmusic.ca/film-commission/key-contacts",
                  "The provincial agency's list of Manitoba's unions with membership numbers."),
                 ("EditCon 2026: Winnipeg, in conversation with Matthew Hannam", "Film Training Manitoba", "2026",
                  "https://filmtraining.mb.ca/editcon-2026-winnipeg-in-conversation-with-matthew-hannam-in-partnership-with-film-training-manitoba",
                  "The Winnipeg stop of the CCE's EditCon, run with Film Training Manitoba.")],
        "note": "I found no Manitoba post-production association. On Screen Manitoba is the closest industry-wide body."},
    "ON": {"unions": [
        U("DGC Ontario", "Represents picture and sound editors, post-production supervisors and their departmental assistants, according to DGC Ontario. " + CORE_NOTE, DGC_CORE),
        U("IATSE Local 873", "Toronto motion picture technicians. Editing coverage not confirmed.", "https://www.iatse873.com/node/15000016")],
        "post": [U("Canadian Cinema Editors (CCE)", "A non-profit professional association based in Toronto. It is not a union.", "editors.html")], "read": []},
    "QC": {"unions": [
        U("AQTIS 514 IATSE", "Represents about 8,000 freelance professionals in more than 200 audiovisual trades, including post-production. Québec's status of the artist law gives it a bargaining framework.", "https://aqtis514iatse.com/")],
        "post": [], "read": [("Heated Rivalry: local talent, Véronique Barbe, editor", "AQTIS 514 IATSE", "2026-01-23",
                              "https://aqtis514iatse.com/en/why-choose-montreal/spotlight-on-our-members/5327/heated-rivalry-local-talent-veronique-barbe-editor",
                              "An interview with the editor, on how editing finds a story's emotion.")],
        "note": "See the Status of the Artist page for how Québec's law works."},
    "NB": {"unions": MARITIMES, "post": [], "read": []},
    "NS": {"unions": MARITIMES, "post": [], "read": []},
    "PE": {"unions": MARITIMES, "post": [], "read": []},
    "NL": {"unions": [U("DGC Newfoundland and Labrador District Council", CORE_NOTE, DGC_CORE)], "post": [], "read": []},
    "NT": {"unions": [],
        "post": [U("NWT Film Commission", "The territorial government's film office, a liaison for productions and local crew.", "https://www.nwtfilm.com/en/local-industry"),
                 U("Western Arctic Moving Pictures (WAMP)", "Non-profit that runs workshops, rents gear and presents the Yellowknife International Film Festival.", "https://www.nwtfilm.com/en/local-industry"),
                 U("Northwest Territories Media Producers Association", "Industry professionals working to build a sustainable NWT media industry.", "https://www.nwtfilm.com/en/local-industry")],
        "read": [("Rolling, Action! The NWT Film and Media Sector Strategy and Action Plan, 2021–2026", "Government of the Northwest Territories", "2021",
                  "https://www.ntlegislativeassembly.ca/sites/default/files/legacy/td_415-192.pdf", "The territory's plan, including crew training and workforce gaps."),
                 ("NWT Film Rebate Program", "Government of the Northwest Territories", "2015",
                  "https://www.castandcrew.com/wp-content/uploads/2018/05/NWTFilmRebateProgramFINALFeb2015docx0.pdf", "An older program document that lists film editor, sound editor and visual effects editor among its recognized positions.")],
        "note": "I found no union local for editors in the Northwest Territories. IATSE's District 12 includes the NWT and Nunavut, but I found no local. Confirm directly."},
    "NU": {"unions": [],
        "post": [U("Nunavut Film Development Corporation", "Keeps a directory of Nunavut technicians and producers, including editors.", "https://www.nunavutfilm.ca/technicians-producers"),
                 U("Isuma", "Inuit-owned production company and media collective based in Igloolik.", "https://en.wikipedia.org/wiki/Isuma")],
        "read": [("Thinking About Isuma", "POV Magazine", "", "https://povmagazine.com/thinking-about-isuma",
                  "How Isuma works. It notes the production employed Inuit people in their own communities, with some post-production done in Isuma's Montreal office.")],
        "note": "I found no union local for editors in Nunavut. Confirm directly."},
}

NUMBERS = [
    ("Directors Guild of Canada (DGC)", "5,500 to 7,000+ members, 48 occupations", "Sources differ on the total. Editors are one of those occupations. I found no editor-only count.",
     "https://en.wikipedia.org/wiki/Directors_Guild_of_Canada"),
    ("DGC Manitoba District Council", "About 200 members, 250 permittees", "Across all its classifications, including picture and sound editors. No editor-only count found.",
     "https://www.mbfilmmusic.ca/film-commission/key-contacts"),
    ("IATSE Local 891 (BC and Yukon)", "9,000+ members, 19 departments", "Editing is one department. Its pages say 9,000 to over 10,000, plus 5,000+ permittees per Creative Pathways. I found no Editing Department count.",
     "https://www.iatse.com/"),
    ("AQTIS 514 IATSE (Québec)", "About 8,000 freelancers, 200+ trades", "Includes post-production trades. No editor-only count found.",
     "https://aqtis514iatse.com/"),
]


def render(leaf, favicon, updated):
    for code, d in DATA.items():
        d["name"] = PROV[code]["name"]
        d["pos"] = PROV[code]["pos"]
    tiles = "".join(
        f'<button class="tile" data-c="{c}" style="grid-column:{p["pos"][0] + 1};grid-row:{p["pos"][1] + 1}" aria-label="{e(p["name"])}">'
        f'<b>{c}</b></button>' for c, p in PROV.items())
    nums = "".join(
        f'<tr><th scope="row"><a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a></th><td>{e(v)}</td><td>{e(note)}</td></tr>'
        for n, v, note, u in NUMBERS)
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{TILES}}", tiles)
            .replace("{{DATA}}", json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")).replace("{{NUMS}}", nums)
            .replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Who represents editors, by province — Post Production Canada</title>
<meta name="description" content="Pick a province to see which unions and guilds have agreements covering editors there, plus its post-production community.">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}.wrap{max-width:860px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink)}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}
h2{font-size:24px;letter-spacing:-.02em;margin:38px 0 8px}h3{font-size:17px;margin:16px 0 4px}
p{margin:0 0 12px}.lede{color:var(--mute);font-size:18px}.note{color:var(--mute);font-size:13.5px}
.map{display:grid;grid-template-columns:repeat(9,1fr);grid-auto-rows:54px;gap:6px;margin:18px 0}
.tile{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:10px;font:inherit;cursor:pointer;display:grid;place-items:center}
.tile b{font-size:15px}.tile:hover{border-color:var(--red)}.tile.on{background:var(--red);border-color:var(--red);color:#fff}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:12px 0}
.u{padding:10px 0;border-bottom:1px solid var(--line)}.u:last-child{border-bottom:0}.u a{font-weight:700;text-decoration:none}.u a:hover{text-decoration:underline}
.u div{color:var(--mute);font-size:14.5px;margin-top:2px}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700;margin:0 0 6px}
.when{color:var(--mute);font-size:13px;margin-left:6px}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:14.5px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}tr:last-child th,tr:last-child td{border-bottom:0}
.tw{overflow-x:auto}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/">← Latest news</a></div></header>
<main class="wrap">
<h1>Who represents editors, by province</h1>
<p class="lede">Pick a province to see which unions and guilds have agreements covering editors there, and its post-production community.</p>
<div class="map" role="group" aria-label="Map of Canada by province and territory (approximate layout)">{{TILES}}</div>
<p class="note">An approximate tile map, not a geographic one.</p>

<div id="panel" class="box"><p>Choose a province above.</p></div>

<h2>How many editors?</h2>
<p>I looked for public counts of editors in each union and found only overall membership. Here is what's published.</p>
<div class="tw"><table><thead><tr><th>Union or guild</th><th>Members</th><th>About editors</th></tr></thead><tbody>{{NUMS}}</tbody></table></div>
<p class="note" style="margin-top:8px">If you have a public figure for editors in either the DGC or IATSE 891, send it with the source and I'll add it.</p>

<h2>How to read this</h2>
<p>Coverage depends on the production. Many editors work non-union, and some work under more than one agreement. "Not confirmed" means I couldn't verify it from a public source. Check with the local, guild or association before you rely on anything here. The Canadian Cinema Editors is a professional association, not a union, so it appears only under "post community".</p>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent and is not affiliated with any union, guild or association listed.</div></footer>
<script id="data" type="application/json">{{DATA}}</script>
<script>
(function(){
  var D=JSON.parse(document.getElementById('data').textContent),panel=document.getElementById('panel'),tiles=document.querySelectorAll('.tile');
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML}
  function link(u,t){var ext=/^https?:/.test(u);return '<a href="'+esc(u)+'"'+(ext?' target="_blank" rel="noopener"':'')+'>'+esc(t)+'</a>'}
  function show(c){
    var d=D[c];tiles.forEach(function(t){t.classList.toggle('on',t.dataset.c===c)});
    var h='<h3 style="margin-top:0">'+esc(d.name)+'</h3>';
    h+='<span class="pill">Unions and guilds with agreements covering editors</span>';
    if(d.unions.length){d.unions.forEach(function(u){h+='<div class="u">'+link(u.url,u.name)+'<div>'+esc(u.role)+'</div></div>'})}
    else h+='<p class="note">None confirmed.</p>';
    if(d.post.length){h+='<span class="pill" style="margin-top:12px">Post community</span>';d.post.forEach(function(u){h+='<div class="u">'+link(u.url,u.name)+'<div>'+esc(u.role)+'</div></div>'})}
    if(d.read.length){h+='<span class="pill" style="margin-top:12px">Reading</span>';d.read.forEach(function(r){h+='<div class="u">'+link(r[3],r[0])+'<span class="when">'+esc(r[1])+(r[2]?', '+esc(r[2]):'')+'</span><div>'+esc(r[4])+'</div></div>'})}
    if(d.note)h+='<p class="note" style="margin-top:10px">'+esc(d.note)+'</p>';
    panel.innerHTML=h;try{history.replaceState(null,'','#'+c)}catch(e){}
  }
  tiles.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.c)})});
  var h0=location.hash.slice(1).toUpperCase();show(D[h0]?h0:'BC');
})();
</script>
</body>
</html>
"""
