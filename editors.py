"""Builds the 'Canadian editors' page: a Canadian Cinema Editors (CCE) section, the Vancouver Post
Alliance on the west coast, and a reading list of articles about Canadian editors.

The CCE is a non-profit professional association. It is NOT a union, and this page never files it
under unions. Facts below were checked against the CCE's own pages, Playback and other sources.
"""
import html
from datetime import datetime

e = html.escape

CCE_SITE = "https://cceditors.ca/"

# Verified against cceditors.ca/2026-awards
CCE_AWARDS_2026 = [
    ("Lifetime Achievement Award", "Annie Jean, CCE"),
    ("Career Achievement Award", "Didier Kennel"),
    ("Best Editing in TV Drama / Mini Series", "Véronique Barbe, CCE, Heated Rivalry, ep. 105"),
    ("Best Editing in Feature Film", "Yvann Thibaudeau, CCE and Dorian Rigal-Ansous, Ma mère, Dieu et Sylvie Vartan"),
    ("Best Editing in Web Series / Digital Content", "Zoé Guèvremont, Fleur de peau, ep. 105"),
]

CCE_LINKS = [
    ("CCE website", CCE_SITE),
    ("2026 CCE Awards, full nominees and winners", "https://cceditors.ca/2026-awards"),
    ("EditCon 2026, the annual picture-editing conference", "https://cceditors.ca/editcon-2026"),
    ("The Editor's Cut (English) and L'Art du montage (French) podcasts", "https://cceditors.ca/what-we-do/podcasts/"),
    ("The Editor's Taskbook", "https://cceditors.ca/taskbook"),
    ("Find an editor (member directory)", "https://cceditors.ca/membership-account/directory/"),
    ("Become a member", "https://cceditors.ca/become-a-member/"),
    ("Friends of the CCE", "https://cceditors.ca/friends-of-the-cce/"),
    ("CCE newsletter", "http://eepurl.com/hHgqSH"),
]

# (title, source, date, url, note). Only items I opened or saw in search results.
ARTICLES = [
    ("Canadian Cinema Editors names 2026 winners", "Playback", "2026-05-25",
     "https://playbackonline.ca/2026/05/25/canadian-cinema-editors-names-2026-winners",
     "Trade coverage of the 16th CCE Awards, held in Toronto on May 22."),
    ("Heated Rivalry: local talent, Véronique Barbe, editor", "AQTIS 514 IATSE", "2026-01-23",
     "https://aqtis514iatse.com/en/why-choose-montreal/spotlight-on-our-members/5327/heated-rivalry-local-talent-veronique-barbe-editor",
     "An interview with the editor behind one of the year's biggest Canadian series, on how editing finds a story's emotion."),
    ("Company 3 projects recognized with CCE Awards nominations", "Company 3", "2026-04-16",
     "https://www.company3.com/2026-cce-awards-nominations",
     "A post house's view of the nominees, with the colourists and finishing editors credited alongside the editors."),
    ("'Heated Rivalry' tops Canadian Screen Awards with 16 wins", "Deadline", "2026-06-01",
     "https://deadline.com/2026/06/heated-rivalry-tops-canadian-screen-awards-1236931778",
     "Full winners list, including the editing categories."),
    ("Canadian Cinema Editors", "Wikipedia", "",
     "https://en.wikipedia.org/wiki/Canadian_Cinema_Editors",
     "Background on the association: founding, membership levels and past awards."),
]

VPA_SITE = "https://vancouverpostalliance.com/"

# DaVinci Resolve Studio: the latest. (title, source, date, url, note). Only items opened or seen in search results.
RESOLVE_ARTICLES = [
    ("DaVinci Resolve Gets AI Assistant Integration and Other New Features With Latest 21.1 Update", "No Film School", "2026-09-08",
     "https://nofilmschool.com/davinci-resolve-update-21-1",
     "The headline story on 21.1: AI assistant integration plus over 100 new tools and controls."),
    ("Blackmagic Design DaVinci Resolve 21.1", "Newsshooter", "2026-09-07",
     "https://www.newsshooter.com/2026/09/07/blackmagic-design-davinci-resolve-21-1",
     "A page-by-page rundown of what's new, including multicam controls, the updated trim editor and scripting API changes."),
    ("DaVinci Resolve 21.1.2", "Newsshooter", "2026-10-26",
     "https://www.newsshooter.com/2026/10/26/davinci-resolve-21-1-2",
     "The latest point release: faster AI tools, better timeline edit-point selection and faster OGraf playback."),
    ("DaVinci Resolve 21 review: Blackmagic turns its editor into a full creative hub", "Videomaker", "",
     "https://www.videomaker.com/reviews/software/davinci-resolve-21-review-blackmagic-turns-its-editor-into-a-full-creative-hub",
     "A full review with strengths and weaknesses. It notes that many of the new AI tools need Studio."),
    ("DaVinci Resolve 21 (2026) video editing software review", "TechRadar", "",
     "https://www.techradar.com/pro/software-services/davinci-resolve-21-2026-video-editing-software-review",
     "A 4.5 out of 5 review that focuses on the new Photo page and the AI tools reserved for Studio owners."),
    ("In Depth: DaVinci Resolve Studio vs Free (Updated for 21)", "Toolfarm", "",
     "https://www.toolfarm.com/tutorial/in-depth-davinci-resolve-studio-vs-the-free-version",
     "What Studio adds over the free version, updated for version 21. Useful before you decide to buy."),
    ("DaVinci Resolve 21.1 Uses MCP to Let AI Assistants Control the Edit", "YMCinema", "2026-09-17",
     "https://ymcinema.com/2026/09/17/davinci-resolve-21-1-mcp-ai-assistants-control-edit/",
     "Explains the new MCP server in Resolve Studio and what an AI assistant can do inside your project."),
    ("Release of DaVinci Resolve Studio 21.1 (release notes)", "Blackmagic Forum", "2026-09-08",
     "https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=239823",
     "Official notes. Back up your project library first: projects opened in 21.1 can't be opened in 20.3.2. Python scripting also moved to Studio."),
    ("Release of DaVinci Resolve Studio 21.1.1 (release notes)", "Blackmagic Forum", "",
     "https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=240579",
     "Official notes for the first point release after 21.1."),
    ("Release of DaVinci Resolve Studio 21.1.2 (release notes)", "Blackmagic Forum", "2026-10-27",
     "https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=241166",
     "Official notes for the newest release, with the full list of fixes."),
]
RESOLVE_VIDEOS = [
    ("What's New in DaVinci Resolve 21.1", "Blackmagic Design (YouTube)", "2026-09-07",
     "https://www.youtube.com/watch?v=Wi44XLKQ3YA", "The official walkthrough of 21.1, including setting up an AI assistant."),
    ("NEW! DaVinci Resolve 21.1 Details YOU NEED TO KNOW", "YouTube", "",
     "https://www.youtube.com/watch?v=2cJoshmcYxo", "Chaptered tour of the edit page, trim editor, multicam, Fusion and the MCP integration."),
    ("DaVinci Resolve 21.1 Update: What's New & What You Need to Know", "YouTube", "",
     "https://www.youtube.com/watch?v=wW70K9gGPPY", "A long, detailed look at the update, including the manual and new log format support."),
    ("DaVinci Resolve 21 Multicam Editing Tutorial (New UI & Timeline Layout)", "YouTube", "",
     "https://www.youtube.com/watch?v=Sqc0_t9SRn0", "Hands-on multicam in version 21: syncing, the dual viewer and angle switching."),
    ("DaVinci Resolve 21 STUDIO - Best features for Creators", "YouTube", "",
     "https://www.youtube.com/watch?v=ubvYuipEz-0", "The Studio AI tools in action, including IntelliSearch and slate reading."),
    ("Before You Update to DaVinci Resolve 21, Watch This", "YouTube", "",
     "https://www.youtube.com/watch?v=IjZ0ExUBtfo", "A colourist's take on whether to update now or wait."),
]


# Storytelling and creativity in Resolve. Only items seen in search results or opened. Notes paraphrase what each page says.
RESOLVE_CREATIVE_ARTICLES = [
    ("DaVinci Resolve (official)", "Blackmagic Design", "", "https://www.blackmagicdesign.com/products/davinciresolve/",
     "The official overview of the pages: Cut and Edit for building the story, Fusion for effects and motion graphics, Color, and Fairlight for sound."),
    ("Advanced Editing with DaVinci Resolve (training book)", "Blackmagic Design", "", "https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-15-Advanced-Editing.pdf",
     "Dialogue editing is about more than the words: the eyes, mouths and body language carry the emotion. It shows how to audition alternate takes with the Take Selector and how to cut on action. Written for Resolve 15, so the interface has changed."),
    ("The Visual Effects Guide to DaVinci Resolve 20 (training book)", "Blackmagic Design", "", "https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-Visual-Effects.pdf",
     "Official lessons on Fusion, with keying, tracking and masking, for Editors who want to do their own effects without leaving Resolve."),
    ("Master Pacing in Video Editing for Maximum Story Impact", "Inside the Edit", "", "https://www.insidetheedit.com/blog/pacing-in-video-editing",
     "Start with the emotion you want the audience to feel, then choose a tempo. Includes a practice exercise: cut a scene one way, duplicate it and cut it the opposite way."),
    ("Mastering film editing: essential techniques for storytelling", "Artlist", "", "https://artlist.io/blog/editing-techniques",
     "Timing, J and L cuts, match cuts, smash cuts and sound bridges, with the advice to practice them in an editor such as Resolve."),
    ("How to Tell a Story in Film and Video With Colour Grading in DaVinci Resolve", "Envato Tuts+", "", "https://photography.tutsplus.com/articles/how-to-tell-a-story-in-film-and-video-with-colour-grading-in-davinci-resolve--cms-39975",
     "Natural colour reinforces a story, but sometimes you need a stronger, stylised touch. A look at both approaches in Resolve."),
    ("Everything you need to know to color grade in DaVinci Resolve", "Storyblocks", "", "https://www.storyblocks.com/resources/tutorials/davinci-resolve-color-grading",
     "Explains the difference between colour correction and colour grading, and how grading sets mood, marks time and place and shapes emotion."),
    ("Advanced Audio Editing in DaVinci Resolve", "Pro Sound Effects", "", "https://blog.prosoundeffects.com/advanced-audio-editing-in-davinci-resolve",
     "Fairlight as a full audio workstation. Creative uses of automation include muffling dialogue behind a closed door with a high-pass filter and changing reverb as a character moves through spaces."),
    ("Doing It All In DaVinci, Part 6: Overview of Audio in Fairlight", "Filmmakers Academy", "", "https://www.filmmakersacademy.com/blog-doing-it-all-in-davinci-part-6-overview-of-audio-in-fairlight",
     "A sound-minded take on mixing in Fairlight, including panning a passing car's sound across the screen to knit it to the picture."),
]

RESOLVE_CREATIVE_ARTICLES += [
    ("The Colorist Guide to DaVinci Resolve 20 (official training guide)", "Blackmagic Design", "", "https://www.blackmagicdesign.com/products/davinciresolve/training",
     "Hands-on exercises in colour correction, workflows and effects, with free lesson files. The same page lists Blackmagic's training videos on the Color page and says it has over 100 training centres and 250 certified trainers worldwide."),
    ("What Is a LUT? Technical vs. Creative LUTs Explained", "DFI Rentals", "", "https://www.dfirentals.com/news/what-is-a-lut-technical-vs-creative",
     "Log and LUTs in plain terms: a technical LUT normalizes log footage first, then a creative LUT or a manual grade shapes the look."),
    ("The Fairlight Audio Guide to DaVinci Resolve 20 (official training guide)", "Blackmagic Design", "", "https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fairlight-Audio-Post.pdf",
     "Lessons on editing dialogue, sound effects and music, recording voiceover, ADR and Foley, repairing audio, mixing with buses and the immersive sound tools."),
    ("Free Certified Fairlight Audio Training For DaVinci Resolve Users", "Production Expert", "", "https://www.production-expert.com/production-expert-1/free-certified-fairlight-audio-training-for-davinci-resolve-users",
     "Reports on Blackmagic's free live online certification classes that walk through the Fairlight Audio Guide. Check the dates, as it lists specific sessions."),
]

RESOLVE_CREATIVE_VIDEOS = [
    ("Audio Storytelling and Editing in DaVinci Resolve 19: Audio Masterclass on a Real Project", "YouTube", "", "https://www.youtube.com/watch?v=flE3YU3Lirw",
     "Chapters cover building the story from voiceover, J and L cuts for audio, then Fairlight EQ, noise removal and dynamics."),
    ("DaVinci Resolve 17 Fairlight Training: Introduction to Sound Design", "YouTube", "", "https://www.youtube.com/watch?v=n4uTGns2z7c",
     "Explains why sounds the characters can hear are a priority, how non-diegetic sound can show what a character feels, and why sound design means crafting a sound to achieve a goal."),
    ("How to Start Color Grading in DaVinci Resolve: Total Beginner's Guide", "YouTube", "", "https://www.youtube.com/watch?v=Wc6EAZp7pzQ",
     "Grading as correction, as emotion and as a way to lead the viewer's eye through the frame."),
    ("Documentary Video Editing in DaVinci Resolve: Masking Reveal Tutorial", "YouTube", "", "https://www.youtube.com/watch?v=GWvTlWML4bw",
     "Documentary-style editing in Resolve, from story structure to cinematic pacing and colour."),
]
RESOLVE_CREATIVE_VIDEOS += [
    ("The Beginner's Guide to Color Management in DaVinci Resolve (2025)", "YouTube", "", "https://www.youtube.com/watch?v=zffM8_PaPCU",
     "Why log footage looks grey, how each camera builds its log image differently, and how colour management reverses it."),
    ("CST vs LUT: Why One Is Clearly Better for Most", "YouTube", "", "https://www.youtube.com/watch?v=pZxOR1kCDeE",
     "An argument for using Resolve's Color Space Transform instead of a LUT to move log footage to Rec. 709, and where to put it in the node tree."),
    ("Color Grading vs LUTs. Is there a case for each?", "Envato (YouTube)", "2026-08-05", "https://www.youtube.com/watch?v=X3caHWY5EVU",
     "The same log clip graded by hand and with a LUT, side by side. The takeaway: a LUT is a starting point, and the same fundamentals still apply."),
    ("The Complete Fairlight Audio Course in DaVinci Resolve 21, Part 1", "YouTube (Jason Yadlovski)", "2026-11-12", "https://www.youtube.com/watch?v=xoonrXhTEzg",
     "A long walk through Blackmagic's Fairlight guide: dialogue, sound effects and music, recording, balancing levels, repairing dialogue and sound design."),
    ("Record Voiceovers, ADR & Foley in DaVinci Resolve 21 Fairlight (Lesson 4)", "YouTube (Jason Yadlovski)", "2026-09-11", "https://www.youtube.com/watch?v=1kc7Z7-BNVc",
     "Setting up a mic, ADR cues and the Foley Sampler in Fairlight."),
]


def feed_list(items, n=8):
    if not items:
        return "<p class=\"note\">Nothing to show right now.</p>"
    rows = []
    for i in items[:n]:
        d = i["date"].strftime("%b %-d, %Y") if isinstance(i["date"], datetime) else ""
        rows.append(f'<li><a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["title"])}</a> <span class="when">{e(d)}</span></li>')
    return "<ul class=\"feed\">" + "".join(rows) + "</ul>"


CSA_MIX_WINNER = ("Rudy Michael, Lucas Roveda, Dave Mercel and Adam Clark", "Nirvanna the Band the Show the Movie")
CSA_MIX_NOMINEES = [
    ("Matthew Chan", "Honey Bunch"),
    ("Michelle Irving, Jeremy Fong and Pablo Villegas", "Mile End Kicks"),
    ("Lou Solakofski and Maryan P'yatnochka", "Nika and Madison"),
    ("Brianna Todd and Carter Buckman", "Sway"),
]
MIX_LINKS = [
    ("Canadian Screen Award for Best Sound Mixing: full list of winners and nominees", "Wikipedia",
     "https://en.wikipedia.org/wiki/Canadian_Screen_Award_for_Best_Sound_Mixing"),
    ("'Heated Rivalry' tops Canadian Screen Awards with 16 wins (full winners list)", "Deadline",
     "https://deadline.com/2026/06/heated-rivalry-tops-canadian-screen-awards-1236931778"),
]


def render(leaf, favicon, updated, cce_items, vpa_items, audio_items=None):
    awards = "".join(f"<li><b>{e(a)}:</b> {e(w)}</li>" for a, w in CCE_AWARDS_2026)
    links = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in CCE_LINKS)
    arts = "".join(
        f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(s)}{", " + e(d) if d else ""}</span>'
        f'<div class="note">{e(n)}</div></li>' for t, s, d, u, n in ARTICLES)
    def _lst(items):
        return "".join(
            f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(s)}{", " + e(d) if d else ""}</span>'
            f'<div class="note">{e(n)}</div></li>' for t, s, d, u, n in items)
    noms = "".join(f"<li>{e(n)}, <i>{e(t)}</i></li>" for n, t in CSA_MIX_NOMINEES)
    mixlinks = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a> <span class="when">{e(s)}</span></li>' for t, s, u in MIX_LINKS)
    return (PAGE.replace("{{MIXWIN}}", f"<b>{e(CSA_MIX_WINNER[0])}</b>, <i>{e(CSA_MIX_WINNER[1])}</i>").replace("{{MIXNOMS}}", noms)
            .replace("{{MIXLINKS}}", mixlinks).replace("{{AUDIOFEED}}", feed_list(audio_items or [], 8))
            .replace("{{RESARTS}}", _lst(RESOLVE_ARTICLES)).replace("{{RESVIDS}}", _lst(RESOLVE_VIDEOS)).replace("{{RESCARTS}}", _lst(RESOLVE_CREATIVE_ARTICLES)).replace("{{RESCVIDS}}", _lst(RESOLVE_CREATIVE_VIDEOS)).replace("{{LEAF}}", leaf).replace("{{FAVICON}}", favicon).replace("{{AWARDS}}", awards)
            .replace("{{CCELINKS}}", links).replace("{{ARTICLES}}", arts).replace("{{CCEFEED}}", feed_list(cce_items))
            .replace("{{VPAFEED}}", feed_list(vpa_items, 5)).replace("{{UPDATED}}", updated))


PAGE = r"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Canadian editors, the CCE and the Vancouver Post Alliance — Post Production Canada</title>
<meta name="description" content="Canadian Cinema Editors news and awards, the Vancouver Post Alliance, and a reading list on Canadian picture editors.">
<link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}
.wrap{max-width:860px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}
.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em;font-size:20px;text-decoration:none;color:var(--ink)}
.logo{width:30px;height:30px;display:grid;place-items:center}.logo svg{width:28px;height:28px}
.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}
h2{font-size:24px;letter-spacing:-.02em;margin:40px 0 8px}
h3{font-size:17px;margin:18px 0 4px}
p{margin:0 0 12px}.lede{color:var(--mute);font-size:18px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:16px 0}
.cce{display:grid;grid-template-columns:230px 1fr;gap:20px;align-items:start}
.logobox{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;display:block}
.logobox img{width:100%;height:auto;display:block}
.credit{font-size:11.5px;color:var(--mute);margin-top:6px}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700;margin-bottom:6px}
ul{margin:6px 0 12px;padding-left:20px}li{margin:6px 0}
.feed,.arts{list-style:none;padding:0}.feed li,.arts li{padding:10px 0;border-bottom:1px solid var(--line);margin:0}
.feed li:last-child,.arts li:last-child{border-bottom:0}
.when{color:var(--mute);font-size:13px;margin-left:6px}
.note{color:var(--mute);font-size:13.5px;margin-top:2px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:640px){.cce,.cols{grid-template-columns:1fr}.logobox{max-width:260px}}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header><div class="wrap top">
  <a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a>
  <a class="btn" href="/">← Latest news</a>
</div></header>
<main class="wrap">
<h1>✂️ Canadian editors</h1>
<p class="lede">The Canadian Cinema Editors, a west coast post community, the latest on DaVinci Resolve Studio, and a reading list on the people who cut Canada's screen stories.</p>

<h2>Canadian Cinema Editors (CCE)</h2>
<div class="box cce">
  <div>
    <a class="logobox" href="https://cceditors.ca/" target="_blank" rel="noopener"><img src="cce-logo.jpg" alt="Canadian Cinema Editors / Les Monteurs et Monteuses de cinéma canadien logo" width="900" height="240"></a>
    <div class="credit">Logo © Canadian Cinema Editors</div>
  </div>
  <div>
    <span class="pill">Non-profit professional association</span>
    <p>The CCE is a bilingual, not-for-profit professional, educational and cultural association for Canada-wide post-production people, founded in 2007 and based in Toronto. It exists to promote picture editing in film, television and new media, to educate peers and students, and to show Canadian editors' work to the world. <b>It is not a union.</b> It runs the CCE Awards, the annual EditCon conference, mentorship, two podcasts (one in English, one in French) and an editor directory.</p>
    <ul>{{CCELINKS}}</ul>
  </div>
</div>

<h3>2026 CCE Awards, a few highlights</h3>
<p class="note">The 16th CCE Awards were held May 22, 2026 at the Delta Hotel in Toronto, with 17 awards.</p>
<ul>{{AWARDS}}</ul>

<h3>Latest from the CCE</h3>
<div class="box">{{CCEFEED}}</div>

<h2>West coast: Vancouver Post Alliance</h2>
<div class="box">
  <span class="pill">Non-profit association, British Columbia</span>
  <p>The Vancouver Post Alliance (VPA) is a non-profit association that represents BC's post-production industry. It began as an ad hoc steering committee in spring 2013 and was established as a non-profit society a few months later. It promotes and markets BC's post talent, runs professional development and networking, and speaks for the industry to government. Its lobbying helped get post-production services added to BC's DAVE tax credit on March 1, 2015.</p>
  <ul>
    <li><a href="https://vancouverpostalliance.com/" target="_blank" rel="noopener">Vancouver Post Alliance website</a></li>
    <li><a href="https://vancouverpostalliance.com/our-story" target="_blank" rel="noopener">Its story and founding members</a></li>
  </ul>
  <h3>Latest from the VPA</h3>
  {{VPAFEED}}
</div>


<h2 id="assistants">🎞️ Assistant Editors: the craft behind the cut</h2>
<p>Assistant Editors keep the cutting room running so the Editor can think about story. Here is what the guild agreement says the job is, what working assistants say it is like, and where the work leads. Everything links to its source.</p>
<h3>What the DGC agreement says</h3>
<div class="box"><ul class="arts">
<li><b>First Assistant Picture Editor.</b> Engaged by the producer in consultation with the head of the Picture Editing Department. Duties include liaising with production, transfer and visual effects houses, providing the Editor with dailies in a correct and organized format, rough assembly of scenes (including VFX) as the schedule permits, sourcing temp sound effects and temp music, providing EDLs for picture and sound post, and coordinating paperwork and supervising the other assistants and trainees. <span class="when">DGC–CMPA Core Agreement 11.34, 2023–25 text</span></li>
<li><b>Assistant Picture Editor.</b> Assists the first assistant while learning the craft of the first assistant. <span class="when">11.35</span></li>
<li><b>Trainee Assistant Picture Editor.</b> Trained as an assistant under the first assistant's supervision. <span class="when">11.36</span></li>
</ul><p class="note" style="margin:8px 0 0">Source: <a href="https://cmpa.ca/wp-content/uploads/2023/10/2023-2025-DGC-Core-Agreement-FULLY-EXECUTED.pdf" target="_blank" rel="noopener">2023–25 DGC Core Agreement (CMPA)</a>. A new 2026–28 agreement took effect January 1, 2026, so check current wording.</p></div>
<h3>The job, in assistants' words</h3>
<div class="box"><ul class="arts">
<li><a href="https://blog.frame.io/2021/05/26/art-of-the-cut-great-assistant-editor" target="_blank" rel="noopener">What Makes a Great Assistant Editor?</a> <span class="when">Frame.io Insider, 2021</span><div class="note">A working assistant, identified in the transcript as Antoine, says to learn what your Editor wants before they ask: read the script and anticipate the effects, sound and music the cut will need. He says never to pitch cuts unprompted, to ask permission, and that if you want to be an Editor you should edit, not assume assisting will turn into it. He also says the job is never advertised, so it comes through networking and word of mouth.</div></li>
<li><a href="https://blog.frame.io/2024/03/18/assistant-editor-job-career-advice" target="_blank" rel="noopener">Assistant Editing: Getting In (and Getting Out)</a> <span class="when">Frame.io Insider, 2024</span><div class="note">History and career advice: US union rules once required eight years as an assistant before you could edit. Today the scope of the job is larger and assistants often work in a separate suite. Its advice is to reach out to Editors on the kind of projects you want, build your technical skills and stay close to the industry.</div></li>
<li><a href="https://blog.frame.io/2019/01/22/the-most-direct-path-to-lead-editor-may-be-a-detour" target="_blank" rel="noopener">The Most Direct Path to Lead Editor May be a Detour to Indie Films</a> <span class="when">Frame.io Insider, 2019</span><div class="note">Three Editors on moving from assistant to lead. They say indies give more responsibility and more time actually cutting, and that editing is a different skill set from assisting.</div></li>
<li><a href="https://www.askthefonz.com/blog/2019/8/1/assistant-editor-interviews" target="_blank" rel="noopener">Assistant Editor Series: Interviews</a> <span class="when">Ask The Fonz, 2019</span><div class="note">Splits the job into three stages: dailies, the cuts for Editor, director, producer and studio, and finishing. On hiring, it says a producer or supervisor is asking whether they can be around you 12 to 14 hours a day, and that you should finish your to-do list before cutting a scene for practice.</div></li>
<li><a href="https://jonnyelwyn.co.uk/film-and-video-editing/what-do-assistant-editors-need-to-know" target="_blank" rel="noopener">What do Assistant Editors Have to Know?</a> <span class="when">Jonny Elwyn</span><div class="note">A task list: ingest, organize and sync dailies, keep the codebook and paperwork, assist with temp VFX, ADR and sound spotting sessions, and create turnovers for other departments.</div></li>
<li><a href="https://workflow.frame.io/guide/editorial-teams" target="_blank" rel="noopener">Editorial teams, Frame.io Workflow Guide</a><div class="note">Describes assistants as keeping everything organized and in sync so the Editor can focus on story, with deeper technical skills than the lead Editor.</div></li>
</ul></div>
<h3>Canadian stories</h3>
<div class="box">
<p><b>Annie Jean, CCE.</b> The CCE says she was a scholarship recipient of the Academy of Canadian Cinema &amp; Television's National Apprenticeship Program in 1988 and has never left the editing rooms since, going from sound to picture and from assistant to Editor, with more than 65 productions as chief Editor. In 2026 she received the CCE Lifetime Achievement Award. <a href="https://cceditors.ca/2026-awards" target="_blank" rel="noopener">Source</a></p>
<p><b>The 2026 Assistant Editor Recognition Award.</b> The CCE gives this award for assistants on nominated projects. The 2026 recipients, per the CCE and Playback, were Andrew Bukovac (<i>Wednesday</i>), Geneviève Roberge (<i>Heated Rivalry</i>), Majda Drinnan (<i>DMV</i>), Paul Kwan (<i>Celebrity IOU</i>) and Wesley Demkiw (<i>The Twisted Tale of Amanda Knox</i>). <a href="https://playbackonline.ca/2026/05/25/canadian-cinema-editors-names-2026-winners" target="_blank" rel="noopener">Playback</a></p>
<p class="note" style="margin-bottom:0">The CCE's EditCon 2026 also had a session called Assistant Editors: The Heart of Post-Production. See the reading list below.</p></div>
<h3>What to look for in a first assistant job (our reading of the sources)</h3>
<div class="box"><ul class="arts">
<li>An Editor who will let you learn the whole workflow: dailies, turnovers, temp sound and music, and the finishing handoff.</li>
<li>Shows with visual effects, sound and music work, because that is where assistants learn the most.</li>
<li>A mentor. The CCE mentorship program has an assistant editing category. See the Education page for how to apply.</li>
<li>A clear plan for what comes next. Several sources say assisting and editing are different skills, so cut on your own time.</li>
</ul></div>

<h2 id="ai">Editors and AI: what one survey found</h2>
<p>In November, Variety reported on a survey of 120 members of American Cinema Editors, which has about 1,200 members. Avid ran the survey. Avid makes Media Composer and Pro Tools. It covers American editors, not Canadian ones, and the company that sells editing tools did the asking. We include it because it is one of the few sets of numbers on how working editors use AI.</p>
<div class="box"><ul>
<li>77.5% use AI to some extent in post.</li>
<li>The top uses are transcription (60%), audio cleanup (55%) and searching footage for specific shots (39.2%).</li>
<li>Only 7.5% want AI to help assemble shots or rough cuts.</li>
<li>Ethical, copyright and security concerns make up nearly half of what holds editors back from using AI.</li>
</ul></div>
<p class="note">Source: <a href="https://variety.com/2026/biz/news/surveyed-ace-editors-using-ai-avid-data-finds-1236947004" target="_blank" rel="noopener">Variety</a>.</p>

<h2 id="resolve">DaVinci Resolve Studio: the latest</h2>
<p>Resolve 21.1 added AI assistant integration, and 21.1.2 is the newest point release. Here is a reading list of reviews, release notes and videos.</p>
<h3>Articles and release notes</h3>
<div class="box"><ul class="arts">{{RESARTS}}</ul></div>
<h3>Videos on YouTube</h3>
<div class="box"><ul class="arts">{{RESVIDS}}</ul></div>

<h2 id="resolve-story">Storytelling and creativity in Resolve</h2>
<p>Resolve is a tool, and the craft is knowing what the audience should feel. These reads and videos cover pacing, performance, colour, sound and effects with a story in mind. Check the version a tutorial was written for, as Resolve changes often.</p>
<h3>Articles and official guides</h3>
<div class="box"><ul class="arts">{{RESCARTS}}</ul></div>
<h3>Videos on YouTube</h3>
<div class="box"><ul class="arts">{{RESCVIDS}}</ul></div>

<h2 id="sound">Sound mixing in Canada</h2>
<h3>Canadian Screen Awards: Achievement in Sound Mixing, 2026</h3>
<div class="box">
  <p><span class="pill">Winner</span><br>{{MIXWIN}}</p>
  <p class="note" style="margin-bottom:4px">Also nominated:</p>
  <ul>{{MIXNOMS}}</ul>
  <ul class="arts">{{MIXLINKS}}</ul>
</div>
<h3>Latest stories on mixing and film audio</h3>
<div class="box">{{AUDIOFEED}}</div>
<p class="note">Stories update automatically from audio and post-production news sources.</p>

<h2>Reading list: Canadian editors in the news</h2>
<div class="box"><ul class="arts">{{ARTICLES}}</ul></div>
<p class="note">Headlines and links only. Each story belongs to its publisher. The CCE and VPA lists above update automatically from their own feeds.</p>
</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent and is not run by, or an official publication of, the CCE or the VPA.</div></footer>
</body>
</html>
"""
