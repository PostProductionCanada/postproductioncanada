"""Schools across Canada for picture editing, sound and post-production.

Built from the schools' own program pages where I could reach them, and from listing sites where I could not.
Programs change every year: check each school before you apply. Listing here is not an endorsement.
Tags: picture (editing), sound (audio post and sound design), post (post-production, VFX, colour), music (music and audio production).
"""
import html

e = html.escape
TAGNAMES = {"picture": "Picture editing", "sound": "Sound and audio post", "post": "Post-production", "music": "Music and audio production", "vfx": "Visual effects", "colour": "Colour and finishing"}
ICONS = {"picture": "🎞️", "sound": "🎧", "post": "🧭", "music": "🎚️", "vfx": "🟩", "colour": "🎨"}
ORIG = "official"
REGION_CODE = {"Ontario": "ON", "British Columbia": "BC", "Alberta": "AB", "Saskatchewan": "SK", "Manitoba": "MB", "Québec": "QC", "Atlantic Canada": None}

REGIONS = [
    ("Online and nationwide", [
        {"school": "Blackmagic Design certified training", "city": "Online and training centres", "kind": "Vendor training", "programs": [
            ("DaVinci Resolve certified training and the Colorist Guide", ["colour", "picture", "sound", "vfx"], "Blackmagic says it has over 100 training centres and 250 certified trainers worldwide, and publishes free official guides for the Color, Fairlight and Fusion pages. It does not list Canadian centres on that page, so ask it for one near you.", "https://www.blackmagicdesign.com/products/davinciresolve/training")]},
        {"school": "Campus VFX (formerly Lost Boys School of VFX)", "city": "Vancouver and Montréal", "kind": "Private", "programs": [
            ("VFX Compositing (Nuke), Effects TD (Houdini), Digital Lighting (Katana)", ["vfx"], "Specialist VFX training from the school that began as Lost Boys in 2006. Vancouver offers 12-month diplomas on campus or online, plus a 4-month lighting certificate. Montréal programs are online. Check which are on offer now.", "https://campusvfx.com")]},
    ]),
    ("Ontario", [
        {"school": "Humber Polytechnic", "city": "Toronto", "kind": "College", "programs": [
            ("Bachelor of Film and Media Production", ["picture", "sound", "post"], "Eight semesters covering directing, picture and sound editing, cinematography and post-production.", "https://humber.ca/explore-programs/programs/bachelor-of-film-and-media-production"),
            ("Film and Television Production", ["picture", "sound", "post"], "A shorter program with career paths in editing, sound and post-production.", "https://humber.ca/explore-programs/programs/film-and-television-production")]},
        {"school": "George Brown Polytechnic", "city": "Toronto", "kind": "College", "programs": [
            ("Video Design & Production (2-year diploma)", ["picture", "sound", "post"], "Courses include Video Editing and Visual Effects and Audio Production Post I and II.", "https://www.georgebrown.ca/programs/video-design-production-program-p112"),
            ("Sound Design & Production (1-year postgraduate)", ["sound"], "Sound for film, television and games, including applied postproduction. Described by a listing site; check the school.", "https://www.coursecompare.ca/the-best-film-schools-in-canada")]},
        {"school": "Sheridan College", "city": "Oakville", "kind": "College", "programs": [
            ("Bachelor of Film and Television", ["picture", "sound", "post"], "Specializations in editing and in sound, with courses such as Assistant Editor, Advanced Sound Editing and Foley, Re-Recording and Mixing, and Post-Production Supervisor.", "https://www.sheridancollege.ca/programs/bachelor-of-film-and-television"),
            ("Advanced Television and Film (graduate certificate)", ["post"], "One year, with virtual production training.", "http://sheridancollege.ca/programs/advanced-television-and-film")]},
        {"school": "Fanshawe College", "city": "London", "kind": "College", "programs": [
            ("Audio Post-Production (graduate certificate)", ["sound"], "A 30-week program on creating sound for film, television and games: surround mixing, field recording, ADR and Foley.", "https://www.fanshawec.ca/programs/apr1-audio-post-production/next"),
            ("Music Industry Arts (diploma)", ["music", "sound"], "Covers audio recording and mixing, audio for picture and sound supervision. Fanshawe says graduates pursue music production, post-production and entry-level audio and sound design for film, web, games and television.", "https://www.fanshawec.ca/programs/mia2-music-industry-arts/next"),
            ("Broadcasting – Television and Film Production", ["picture", "post"], "Includes post-production editing and graphics, and says it has the largest TV and film studio outside Toronto.", "https://www.fanshawec.ca/programs/brt3-broadcasting-television-and-film-production")]},
        {"school": "Centennial College", "city": "Toronto", "kind": "College", "programs": [
            ("Broadcasting – Film, Television, Digital Media and Radio", ["picture", "sound", "post", "colour", "vfx"], "A three-year advanced diploma. Skills include post audio, advanced editing, compositing and colour correction.", "https://www.centennialcollege.ca/programs-courses/full-time/radio-television-film-digital-media")]},
        {"school": "Seneca Polytechnic", "city": "Toronto", "kind": "College", "programs": [
            ("Avid microcredentials for unscripted TV", ["picture"], "Media Organization and Output and Delivery for Unscripted TV, built with Centennial and Fanshawe in 2022. Check whether they are still offered.", "https://www.senecapolytechnic.ca/news-and-events/media-releases/2022/centennial-fanshawe-and-seneca-partner-with-government-and-industry-to-fill-skills-gap-in-ontarios-screen-sector.html")]},
        {"school": "Metalworks Institute", "city": "Mississauga", "kind": "Private", "programs": [
            ("Audio Production & Engineering; Music Mixing & Mastering", ["music", "sound"], "Diplomas and a postgraduate mixing and mastering program, plus online certificate courses including Audio Post and Pro Tools.", "https://metalworksinstitute.com")]},
        {"school": "Harris Institute", "city": "Toronto", "kind": "Private", "programs": [
            ("Audio Production Program", ["music"], "A 12-month diploma in the art, technology and business of audio production.", "https://harrisinstitute.com")]},
        {"school": "Recording Arts Canada", "city": "Toronto and Montréal", "kind": "Private", "programs": [
            ("Sound and Music Production", ["music", "sound"], "900+ hours in under a year, offered online and on campus. A diploma in Toronto.", "https://recordingarts.com")]},
        {"school": "Trebas Institute", "city": "Toronto and Montréal", "kind": "Private", "programs": [
            ("Sound Design and audio programs", ["sound", "music"], "Audio engineering and sound design programs. The Sound Design page is for the Québec campus, so confirm what each campus offers.", "https://www.trebas.com/programs/creative/sound-design")]},
        {"school": "OIART", "city": "London", "kind": "Private", "programs": [
            ("Audio Recording Technology", ["music"], "A recording and live sound school in London, Ontario.", "https://www.oiart.org")]},
    ]),
    ("British Columbia", [
        {"school": "Vancouver Film School", "city": "Vancouver", "kind": "Private", "programs": [
            ("Film Production (Post-Production specialization)", ["picture", "sound", "post", "colour", "vfx"], "A 12-month diploma where students choose two specializations. Post covers editing, sound design, VFX compositing and colour grading.", "https://vfs.edu/programs/film-production"),
            ("3D Animation & Visual Effects (12-month diploma)", ["vfx"], "A studio-style year ending in a demo reel. VFS lists Maya, Nuke, Houdini, ZBrush and Unreal Engine among the tools. On campus or online.", "https://vfs.edu/programs/3d-animation-vfx"),
            ("Sound Design for Visual Media", ["sound", "music"], "A 12-month diploma in film and TV post-production audio and game audio, with Foley and ADR rooms and mixing labs.", "https://vfs.edu/programs/sound-design")]},
        {"school": "Capilano University", "city": "North Vancouver", "kind": "University", "programs": [
            ("Bachelor of Motion Picture Arts", ["picture", "sound", "post"], "A four-year degree in the Bosa Centre, with sound and picture editing suites and courses such as Advanced Digital Editing and Sound Design for Film and Video.", "https://www.capilanou.ca/programs--courses/program-profiles/bachelor-of-motion-picture-arts-degree"),
            ("Animation and Digital VFX diplomas", ["vfx"], "A VFX school directory lists two-year diplomas in 2D animation, 3D animation and digital VFX. I could not open the program pages, so check Capilano.", "https://www.vfxengine.com/schools"),
            ("Documentary Certificate", ["post"], "Includes courses in documentary sound design and audio and video post-production.", "https://www.capilanou.ca/programs--courses/search--select/explore-our-areas-of-study/fine--applied-arts/school-of-motion-picture-arts")]},
        {"school": "UBC, SFU, Emily Carr, BCIT and InFocus", "city": "Various", "kind": "University and college", "programs": [
            ("Film programs at five BC schools", ["picture", "sound", "post"], "UBC Film Production (BFA), SFU Film, Emily Carr's Film + Screen Arts (BMA), BCIT's two-year Television & Video Production diploma (editing and audio included) and InFocus Film School's 12-month program. Details come from a guide, so check each school.", "https://creativepathwayscanada.com/your-first-steps-into-b-c-s-film-industry-schools-workshops-mentorship-programs")]},
    ]),
    ("Alberta", [
        {"school": "SAIT", "city": "Calgary", "kind": "College", "programs": [
            ("Film and Video Production", ["picture", "sound", "post"], "A program with an on-campus Mac lab for picture editing and post sound, according to students. Check the catalogue for current content.", "https://catalog.sait.ca/preview_program.php?catoid=180&poid=37655&print=")]},
        {"school": "NAIT", "city": "Edmonton", "kind": "College", "programs": [
            ("Digital Media & IT: Digital Cinema Concentration; Sound Design (short course)", ["picture", "sound"], "A digital cinema certificate and a part-time online sound design course, per career-resource listings. Check NAIT for details.", "https://reelcanada.ca/reel-opportunities/career-resources")]},
    ]),
    ("Alberta, continued", [
        {"school": "Bow Valley College, Centre for Entertainment Arts", "city": "Calgary", "kind": "College", "programs": [
            ("Diplomas in 3D animation, visual effects, virtual production and game development", ["vfx"], "Listed by a VFX school directory as a partnership between Bow Valley College and the Centre for Entertainment Arts since 2021. I have not opened the school's own pages, so check before you apply.", "https://www.vfxengine.com/schools")]},
    ]),
    ("Saskatchewan", [
        {"school": "Saskatchewan Polytechnic and University of Regina", "city": "Saskatoon and Regina", "kind": "College and university", "programs": [
            ("Media Production diploma; Film (University of Regina)", ["picture", "post"], "Listed in career-resource guides. I could not reach the program pages, so check each school.", "https://reelcanada.ca/reel-opportunities/career-resources")]},
    ]),
    ("Manitoba", [
        {"school": "Red River College Polytechnic", "city": "Winnipeg", "kind": "College", "programs": [
            ("Digital Film and Media Production (postgraduate diploma)", ["picture", "post"], "Videography, audio, lighting and post-production.", "https://www.rrc.ca/explore/program/digital-film-and-media-production"),
            ("Entertainment Production (certificate)", ["post"], "Career paths include post-production supervisor.", "https://www.rrc.ca/explore/program/entertainment-production")]},
        {"school": "Film Training Manitoba", "city": "Winnipeg", "kind": "Training council", "programs": [
            ("Courses and workshops", ["post"], "A non-profit that runs the courses needed for DGC Manitoba and IATSE 856 membership, and the EditCon stop in Winnipeg.", "https://filmtraining.mb.ca/entry-workshops")]},
    ]),
    ("Québec", [
        {"school": "Concordia University, Mel Hoppenheim School of Cinema", "city": "Montréal", "kind": "University", "programs": [
            ("BFA in Film Production", ["picture", "sound", "post"], "Covers soundscapes, post-production and digital finishing. Its facilities include Avid editing and Pro Tools sound editing and mixing studios.", "https://www.concordia.ca/finearts/cinema/programs/film-production.html")]},
        {"school": "Recording Arts Canada and Trebas Institute", "city": "Montréal", "kind": "Private", "programs": [
            ("Sound and music production; Sound Design", ["sound", "music"], "Both have Montréal campuses (see their Ontario entries above).", "https://recordingarts.com")]},
    ]),
    ("Québec, continued", [
        {"school": "Musitechnic", "city": "Montréal", "kind": "College", "programs": [
            ("Audio programs with studio internships", ["music", "sound"], "Its Stages et carrières page describes studio internships and careers after its AEC programs in recording, sound design, mixing and audio post-production. Check the page for current program details.", "https://musitechnic.com/en/stages-et-carrieres")]},
    ]),
    ("Atlantic Canada", [
        {"school": "College of the North Atlantic", "city": "Newfoundland and Labrador", "kind": "College", "programs": [
            ("Television and Film Post-Production (1-year certificate)", ["picture", "sound", "post", "colour", "vfx"], "A dedicated post program. Courses include Post-Production Supervision, Colour Grading, Compositing & Effects, Post-Production Audio, Dialogue Editing & Recording, Sound Effects & Foley, and Audio Mixing for TV & Film.", "https://www.cna.nl.ca/program/television-and-film-post-production")]},
        {"school": "Nova Scotia Community College", "city": "Halifax", "kind": "College", "programs": [
            ("Screen Arts", ["picture", "post"], "A film and video program. I could not confirm current details, so check the program page.", "https://www.nscc.ca/programs-and-courses/programs/plandescr.aspx/screen-arts")]},
    ]),
]


def render(leaf, favicon, updated):
    secs = []
    for region, schools in REGIONS:
        cards = []
        for s in schools:
            progs = ""
            for title, tags, note, url in s["programs"]:
                chips = "".join(f'<span class="pill t-{t}">{ICONS[t]} {e(TAGNAMES[t])}</span> ' for t in tags)
                progs += (f'<div class="prog" data-tags="{" ".join(tags)}"><div>{chips}</div>'
                          f'<a href="{e(url)}" target="_blank" rel="noopener">{e(title)}</a><div class="note">{e(note)}</div></div>')
            code = REGION_CODE.get(region) or ("NL" if "North Atlantic" in s["school"] else "NS")
            cards.append(f'<article class="box" data-tags="{" ".join({t for p in s["programs"] for t in p[1]})}"><h3>{e(s["school"])}</h3>'
                         f'<div class="meta">🍁 📍 {code} · {e(s["city"])} · {e(s["kind"])}</div>{progs}</article>')
        secs.append(f'<h2 id="{e(region.lower().replace(" ", "-"))}">{e(region)}</h2>{"".join(cards)}')
    return (PAGE.replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{SECTIONS}}", "".join(secs)).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Schools for picture editing, sound and post across Canada — Post Production Canada</title>
<meta name="description" content="Colleges, universities and private schools across Canada that teach picture editing, sound and post-production.">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}.wrap{max-width:860px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0;flex-wrap:wrap;gap:10px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink);white-space:nowrap}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;white-space:nowrap;cursor:pointer;font-family:inherit}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}
h2{font-size:24px;letter-spacing:-.02em;margin:34px 0 8px}h3{font-size:18px;margin:0}
.lede{color:var(--mute);font-size:18px}.note{color:var(--mute);font-size:14px}.meta{color:var(--mute);font-size:13.5px;margin-bottom:6px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin:10px 0}
.prog{padding:10px 0;border-top:1px solid var(--line)}.prog:first-of-type{border-top:0}.prog a{font-weight:700;text-decoration:none}.prog a:hover{text-decoration:underline}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 9px;font-size:12px;font-weight:700;margin:0 2px 4px 0}
.t-picture{background:#d52b1e22;color:var(--red)}.t-sound{background:#2f7de122;color:#2f7de1}.t-post{background:#12a37f22;color:#0f8c6c}.t-music{background:#e0900b22;color:#b97500}.t-vfx{background:#8b5cf622;color:#7c4dff}.t-colour{background:#e11d8f22;color:#c4137a}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0;position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:3}
.filters .btn.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/">← Latest news</a></div></header>
<main class="wrap">
<h1>🎓 Schools across Canada</h1>
<p class="lede">Where to learn picture editing, sound and post-production, from Newfoundland to Vancouver. Colleges, universities and private schools.</p>
<p class="note">Programs change every year, so check each school before you apply. Being listed is not an endorsement. Where I couldn't reach a school's own page, the entry says so. Visual effects, colour and music programs have been added, but the list is not complete, and I don't know the full count of Canadian schools that teach these. New Brunswick, PEI and the territories aren't covered yet.</p>
<h2 id="learn-on-the-job">🛠️ Learn on the job: mentorships, trainee roles and internships</h2>
<p class="note">I found few public sound or colour internship programs run by Canadian facilities. Most of this work is learned as an assistant or trainee and comes through word of mouth. Here is what is documented.</p>
<div class="box"><div class="prog" style="border-top:0"><div><span class="pill t-picture">🎞️ Picture</span><span class="pill t-sound">🎧 Sound</span><span class="pill t-post">🧭 Post supervision</span></div><b>DGC trainee positions in post</b><div class="note">The 2023–25 DGC Ontario schedule has a letter agreeing that a Tier A production doing post in Ontario will engage a trainee from one of three streams (picture editing, sound editing, or post-production supervision and coordination) for six weeks or the length of post, whichever is less. A matching letter is in the 2026–28 Maritimes agreement. <a href="https://cmpa.ca/wp-content/uploads/2024/02/2023-2025-DGC-Schedule-5-DGC-Ontario-FULLY-EXECUTED-READABLE.pdf" target="_blank" rel="noopener">Source</a></div></div>
<div class="prog"><div><span class="pill t-picture">🎞️ Picture</span><span class="pill t-post">🧭 Post producing</span></div><b>CCE Mentorship Program</b><div class="note">A one-year program. Mentee categories are assistant editing, VFX editing, scripted picture editing, documentary picture editing and post-producing. The FAQ says it is open to CCE Associate or Full Members who live in Ontario, with at least two years in film and television, and who are not in school. The CCE also runs speed-mentoring and small-group sessions for emerging and mid-career Editors and assistants. <a href="https://cceditors.ca/what-we-do/mentorship-program" target="_blank" rel="noopener">Source</a></div></div>
<div class="prog"><div><span class="pill t-picture">🎞️ Picture</span><span class="pill t-sound">🎧 Sound</span><span class="pill t-vfx">🟩 VFX</span></div><b>Vancouver Post Alliance mentorship</b><div class="note">Includes Speed Mentoring, where mentees rotate through picture Editors, re-recording mixers, VFX producers, post producers and composers, a Spring Mentorship Program, and a year-round Coffee With a Mentor program that it says is open to members and non-members with no minimum experience. <a href="https://vancouverpostalliance.com/resources/mentorship" target="_blank" rel="noopener">Source</a>. Its <a href="https://vancouverpostalliance.com/career-pathways/post-audio" target="_blank" rel="noopener">post audio career page</a> says supervisors, sound designers and re-recording mixers need the most experience, while sound assistants are entry level.</div></div>
<div class="prog"><div><span class="pill t-colour">🎨 Colour</span><span class="pill t-sound">🎧 Sound</span><span class="pill t-post">🧭 Finishing</span></div><b>Company 3 NExT internship</b><div class="note">A paid, 10-week, full-time summer internship with tracks that include post-production finishing (colour and finishing), VFX and sound. Positions may be on site, remote or hybrid. Company 3 also lists a NExT Apprenticeship Program. I could not confirm that Toronto positions are offered, so ask the company. <a href="https://www.company3.com/next-summer-internship-program" target="_blank" rel="noopener">Source</a></div></div>
<div class="prog"><div><span class="pill t-colour">🎨 Colour</span></div><b>How one Canadian colourist started</b><div class="note">Company 3's biography of Toronto senior colourist Dave Muscat says he joined what was then Deluxe Toronto in 2000 as a colour assist, learned foundational techniques from senior artists, then worked as a finishing editor on many shows before becoming a colourist. It is one documented path, not the only one. <a href="https://www.company3.com/artists/dave-muscat" target="_blank" rel="noopener">Source</a></div></div>
<div class="prog"><div><span class="pill t-picture">🎞️ Picture</span><span class="pill t-sound">🎧 Sound</span></div><b>An Academy apprenticeship, 1988</b><div class="note">The CCE says Annie Jean, its 2026 Lifetime Achievement recipient, began as a scholarship recipient of the Academy of Canadian Cinema &amp; Television's National Apprenticeship Program in 1988. I could not confirm whether that program is still running. <a href="https://cceditors.ca/2026-awards" target="_blank" rel="noopener">Source</a></div></div></div>
<div class="filters" id="filters">
  <button class="btn on" data-f="all">All</button><button class="btn" data-f="picture">🎞️ Picture editing</button><button class="btn" data-f="sound">🎧 Sound</button>
  <button class="btn" data-f="post">🧭 Post-production</button><button class="btn" data-f="music">🎚️ Music and audio production</button><button class="btn" data-f="vfx">🟩 Visual effects</button><button class="btn" data-f="colour">🎨 Colour</button>
</div>
{{SECTIONS}}
<div class="box" style="border-left:4px solid #e0a100"><h3>Know a school or program that's missing?</h3><p class="note" style="margin:6px 0 0">Send me the name and I'll check its program page and add it.</p></div>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent. Summaries are mine, and each entry links to its source.</div></footer>
<script>
(function(){
  var bs=document.querySelectorAll('#filters .btn'),boxes=document.querySelectorAll('.box[data-tags]'),heads=document.querySelectorAll('main h2');
  function apply(f){
    bs.forEach(function(b){b.classList.toggle('on',b.dataset.f===f)});
    boxes.forEach(function(bx){
      var any=false;
      bx.querySelectorAll('.prog').forEach(function(p){var ok=f==='all'||p.dataset.tags.split(' ').indexOf(f)>-1;p.style.display=ok?'':'none';if(ok)any=true});
      bx.style.display=any?'':'none';
    });
    heads.forEach(function(h){var n=h.nextElementSibling,vis=false;while(n&&n.tagName!=='H2'){if(n.classList&&n.classList.contains('box')&&n.hasAttribute('data-tags')&&n.style.display!=='none')vis=true;n=n.nextElementSibling}h.style.display=vis?'':'none'});
  }
  bs.forEach(function(b){b.addEventListener('click',function(){apply(b.dataset.f)})});
})();
</script>
</body>
</html>
"""
