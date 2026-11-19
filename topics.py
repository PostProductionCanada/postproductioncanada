"""Two resource pages: Wellbeing (mental health, work-life balance) and Green Post (sustainability).
Every item links to its source. Add items by appending to the lists."""
import html

e = html.escape

# (title, org, url, text, prov, tags)
WELL = [
    ("Counselling, peer support and emergency aid", "AFC (Arts and entertainment charity)", "https://afchelps.ca",
     "A national charity for Canada's entertainment industry. It lists programs for mental health and wellness, peer support, financial wellness and career sustainability, plus emergency aid, and runs Mental Health First Aid courses. It has also run a subsidized short-term counselling pilot, but that has been limited by province and funding, and enrolment has been full at times, so check the site for the current round.",
     ["ON"], ["Support", "National"]),
    ("Mental Health in Focus", "Canada Media Fund", "https://cmf-fmc.ca/now-next/articles/hows-mental-health-in-the-film-and-tv-industry-professionals-weigh-in",
     "Nine people across production, direction, VFX, camera, set design and more were interviewed. The same themes kept coming up: isolation, invisible responsibilities, the pace of the work, and balancing work with home life. Their suggestions include better planning, adding people when needed, shorter days and building support roles in from the start of a project.",
     [], ["Reading", "Video"]),
    ("Safe Sets: Dying to Work in the Film Industry", "DGC Ontario screening and panel", "https://www.youtube.com/watch?v=FV8tuHUHmOM",
     "DGC Ontario presented the documentary's international premiere at TIFF Lightbox on May 12, followed by a panel about safety, well-being and work culture. A panelist noted that many Ontario unions and guilds have had daily and weekend turnaround rules for over 25 years, and that the film looks at how US crews won them.",
     ["ON"], ["Hours", "Film"]),
    ("Canada's first certified mental health coordinator for film", "HNMAG interview", "https://hnmag.ca/interview/exclusive-canadas-first-mental-health-coordinator-for-films",
     "Aryn Mott describes becoming Canada's first certified mental health coordinator for film and TV, training with a US association from 2021. The interview covers what the role is and the resources a production can bring in.",
     [], ["Role", "Reading"]),
    ("Mental health resources for documentary makers", "Documentary Organization of Canada", "https://docorg.ca/mental-health-resources",
     "A compiled list of Canadian counselling and support options aimed at documentary filmmakers, including sliding-scale therapists who know the industry and guidance on the emotional weight of difficult material.",
     [], ["Support", "Documentary"]),
    ("Behind the Scenes", "BTS (cited by IATSE)", "https://btshelp.org",
     "IATSE's support guide points IATSE members in the US and Canada to this charity for mental health resources, therapist searches, Mental Health First Aid and bystander-intervention training.",
     [], ["Support", "IATSE"]),
]

GREEN = [
    ("DGC Green", "Directors Guild of Canada", "https://dgcgreen.ca",
     "The guild's climate hub, with Top Tips for each department including Editors, a case study from the art department of the thriller Bed Rest, a DGC Materials Carbon Calculator, and a directory of Canadian and international programs. The DGC Green Award went to Peak Everything at the 2025 DGC Awards.",
     [], ["Union", "Editors tips"]),
    ("Reel Green", "Creative BC", "https://creativebc.com/bc-film-commission/reel-green",
     "Founded in 2006 at the BC Film Commission. It offers tools, training, vendor lists and clean-energy and circular-economy toolkits. A strategic plan for 2026 to 2029 is published.",
     ["BC"], ["Province"]),
    ("Ontario Green Screen", "Ontario Creates", "https://www.ontariocreates.ca",
     "Launched in 2020 with a framework for measuring and reporting environmental impact, best-practice guides and a map of grid tie-in points for clean power on location.",
     ["ON"], ["Province"]),
    ("Rolling Green / On Tourne Vert", "Québec", "https://dgcgreen.ca/resources",
     "Québec's initiative with a sourcebook of providers. DGC Green's resource list also links Manitoba Film & Music's Reel Green and the IATSE Green Committee.",
     ["QC", "MB"], ["Province"]),
    ("Greening our Story", "CBC/Radio-Canada", "https://spheresofinfluence.ca/lights-camera-emissions-how-the-u-s-uk-and-canadian-film-industries-are-acting-on-climate-change",
     "A five-year plan from 2021 committing in-house productions to the albert carbon calculator. In 2022 it expanded to require independent producers with budgets over $400,000 to use albert, with a sustainability plan expected on smaller projects, including post-production.",
     [], ["Broadcaster"]),
    ("Drawn to Change: animation toolkit", "Producing for the Planet", "https://rocketfund.ca/producing-for-the-planet-launches-drawn-to-change",
     "Launched September 22, 2026 with support from Rocket Fund Canada and Reel Green. It includes a guide and a carbon calculator built for animation, where emissions come mostly from render farms and compute hours, studio energy and distributed teams.",
     ["BC"], ["Animation", "Compute"]),
    ("The footprint numbers", "Producing for the Planet", "https://www.producingfortheplanet.com/guide/environmental-impact-of-our-industry",
     "A 2021 Sustainable Production Alliance report that included Canadian productions estimated a drama hour at 35 to 81 tonnes of CO2e, with tentpole features above 1,000 tonnes. The page also links a Telefilm study of Canada's audiovisual sector footprint by Green Spark Group.",
     [], ["Data"]),
    ("Sustainable Production Forum", "SPF25, Toronto", "https://ca.finance.yahoo.com/news/ten-years-strong-spf25-sets-193400122.html",
     "A ten-year-old industry forum. The 2025 Toronto edition launched the Green Frame Progress Report and the expanded DGC Materials Carbon Calculator, with partners including Ontario Creates, Creative BC and IATSE 891.",
     ["ON"], ["Event"]),
    ("VFX and the carbon question", "VFX Voice", "https://vfxvoice.com/vfx-and-sustainability-reducing-carbon-footprint-its-importance-and-more",
     "Notes that good figures on VFX's footprint barely exist. It cites a 2016 BAFTA finding that animation's emissions come mostly from production offices and post-production, and describes a studio that moved fully to cloud on a renewables-backed provider. A UK study adds that data movement and cloud rendering are poorly measured. This is not Canadian reporting.",
     [], ["Post", "International"]),
]

PAGE = r"""<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLE}} — Post Production Canada</title><meta name="description" content="{{DESC}}"><link rel="icon" href="{{FAVICON}}">
<style>
:root{--bg:#f6f4ef;--panel:#fff;--ink:#16181d;--mute:#69707d;--line:#e4e0d6;--red:#d52b1e;--chip:#ece8dd}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--panel:#181b21;--ink:#eceae4;--mute:#9099a8;--line:#272b33;--red:#ff5a4d;--chip:#222630}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}.wrap{max-width:820px;margin:0 auto;padding:0 16px}header{border-bottom:1px solid var(--line)}
.top{display:flex;align-items:center;justify-content:space-between;padding:14px 0;flex-wrap:wrap;gap:10px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:var(--ink);white-space:nowrap}
.logo svg{width:28px;height:28px}.brand b{color:var(--red)}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;white-space:nowrap}
h1{font-size:clamp(28px,5vw,42px);line-height:1.1;letter-spacing:-.03em;margin:30px 0 8px}h2{font-size:22px;margin:34px 0 8px}h3{font-size:19px;margin:6px 0}
.lede{color:var(--mute);font-size:18px}.note{color:var(--mute);font-size:14px}.when{color:var(--mute);font-size:13px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin:14px 0}
.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700}
.help{border-left:4px solid var(--red)}footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;color:var(--mute);font-size:13px}
</style></head><body>
<header><div class="wrap top"><a class="brand" href="/"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></a><a class="btn" href="/">← Latest news</a></div></header>
<main class="wrap"><h1>{{H1}}</h1><p class="lede">{{LEDE}}</p>{{BODY}}</main>
<footer><div class="wrap">Page built {{UPDATED}}. Post Production Canada is independent. Summaries are mine and each item links to its source. {{FOOT}}</div></footer>
</body></html>"""


def _cards(items):
    out = ""
    for title, org, url, text, prov, tags in items:
        pins = "".join(f'<span class="pill">📍 {e(p)}</span> ' for p in prov)
        chips = "".join(f'<span class="pill">{e(t)}</span> ' for t in tags)
        out += (f'<article class="box"><div>🍁 {pins}{chips}</div><h3><a href="{e(url)}" target="_blank" rel="noopener">{e(title)}</a></h3>'
                f'<div class="when">{e(org)}</div><p>{e(text)}</p></article>')
    return out


def _page(leaf, fav, updated, title, desc, h1, lede, body, foot=""):
    return (PAGE.replace("{{TITLE}}", e(title)).replace("{{DESC}}", e(desc)).replace("{{FAVICON}}", fav).replace("{{LEAF}}", leaf)
            .replace("{{H1}}", h1).replace("{{LEDE}}", lede).replace("{{BODY}}", body).replace("{{UPDATED}}", updated).replace("{{FOOT}}", foot))


def wellbeing(leaf, fav, updated):
    body = ('<div class="box help"><h3>If you are in crisis, call or text 9-8-8</h3>'
            '<p style="margin:6px 0 0">9-8-8 is the national suicide crisis line in Canada, free, any time. If someone is in immediate danger, call 911.</p></div>'
            '<h2>Support and reading</h2>' + _cards(WELL) +
            '<div class="box"><h3>A note about post</h3><p class="note" style="margin:6px 0 0">Everything above is industry-wide. I have not found a Canadian resource written only for editors, colourists and sound people, who often work alone for long stretches. If you know one, send it and I will check it and add it.</p></div>')
    return _page(leaf, fav, updated, "Wellbeing and work-life balance",
                 "Mental health and work-life balance resources for Canadian screen workers.",
                 "💚 Wellbeing and work-life balance",
                 "Long days, tight deadlines and a lot of time alone in a room. Here is the support that exists for Canadian screen workers, and the conversations the industry is having.",
                 body, "This is information, not medical advice.")


def green(leaf, fav, updated):
    body = ('<h2>What Canada is doing</h2>' + _cards(GREEN) +
            '<div class="box"><h3>Honest scorecard</h3><p style="margin:6px 0 0">Five provinces have their own green-production programs and the DGC runs one of the most detailed guild hubs, but the UK\'s albert calculator is still the benchmark that Canadian programs build on. Canada has real momentum here. Calling it the world leader would be an overstatement, and the one gap everyone admits is data on post-production and cloud rendering.</p></div>'
            '<div class="box"><h3>Where post fits</h3><p class="note" style="margin:6px 0 0">Start with the Editors Top Tips on DGC Green. Beyond that, the biggest levers in post are compute and storage: where your cloud or render farm gets its power, how long machines run idle, and how much media you keep and move. Ask your facility for its numbers.</p></div>')
    return _page(leaf, fav, updated, "Green post-production",
                 "What the DGC, provinces and broadcasters are doing about sustainability in Canadian screen production and post.",
                 "🌱 Green post-production",
                 "What the DGC, the provinces and broadcasters are doing about the footprint of screen work, and what it means for post, from editing rooms to render farms.",
                 body)
