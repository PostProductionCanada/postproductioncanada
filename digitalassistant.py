"""The Digital Assistant Editor: AI agents taking on assistant-editor tasks, and what it means for learning the craft.
Facts read from the linked pages on AS_OF. Questions are marked as questions, not conclusions."""
import html
import topics

e = html.escape
AS_OF = "November 20, 2026"

INTRO = ("Editors can now hand an AI agent some of the work an Assistant Editor used to do: organizing media, finding duplicates, applying changes across a whole sequence. "
         "This page is a working file. It collects what the software makers have actually announced, what the Assistant Editor's job and training path look like today, "
         "and the question underneath it all: if the prep work is done by an agent, where does the next generation learn the craft of storytelling?")

NEWS = [
    ("DaVinci Resolve 21.1 lets AI assistants act inside Resolve", "YMCinema and Digital Production, September 2026",
     "Blackmagic's 21.1 update adds a built-in MCP server (the standard that lets an AI agent control other software). From File > Setup AI Assistants, Resolve detects compatible assistants such as Claude and ChatGPT's Codex and sets them up, "
     "and you then work through the assistant's own chat. Coverage describes the aim as executing, organizing and automating tasks inside Resolve. It needs DaVinci Resolve Studio.",
     "https://ymcinema.com/2026/09/17/davinci-resolve-21-1-mcp-ai-assistants-control-edit/"),
    ("Adobe MAX 2026: Premiere's AI Assistant and MCP", "RedShark News, November 2026",
     "Adobe's AI Assistant in Premiere is in beta: you describe what you need and it carries out multi-step tasks, such as applying effects across every clip in a sequence, tracking a masked subject through a frame, and adjusting colour and exposure across a whole sequence. "
     "MCP integrations, in preview, let third-party agents such as Claude and ChatGPT work in Premiere and other Adobe apps, locally, in native project files where bins and sequences stay editable. They are due to Creative Cloud customers in early 2027.",
     "https://www.redsharknews.com/adobe-max-2026-premiere-color-mode-mcp"),
    ("Always-on agents for the boring background work", "RedShark News, November 2026 (a preview, beta due early 2027)",
     "RedShark reports that Adobe previewed always-on agents that take on recurring background work. On a multi-week video project, an agent could organize incoming footage, remove duplicate clips, and flag camera shake or audio issues for review. "
     "That list reads a lot like an Assistant Editor's first week.",
     "https://www.redsharknews.com/adobe-max-2026-premiere-color-mode-mcp"),
    ("Adobe MCP: private beta in early 2027, and what works today", "The Post Flow",
     "A practical breakdown of Adobe's three routes: connectors in chat assistants (available now), Adobe's own AI Assistant (the only one that works inside Premiere today), and the MCP integrations still to come. "
     "Its advice to editors is to try the beta on a duplicate of a real project. It also notes that an agent that rearranges a sequence or moves media between bins is harder to trust until Adobe says exactly what it may touch.",
     "https://thepostflow.com/post-production/software-plugins/adobe-mcp/"),
]

JOB = [
    ("Assistant Editing: Getting In (and Getting Out)", "Frame.io Insider, 2024",
     "Describes how the job changed. Being an assistant used to be an editing apprenticeship: years in the room hearing the Editor and director shape the story. "
     "Today, the article says, there are no more formal editing apprenticeships, the scope of the work has grown, and assistants usually sit in a separate suite and check in with the Editor from time to time. "
     "It says second assistants take on ingest, sync, prep and turnovers, while firsts handle offline sound effects and VFX, assembling, tracking and whatever else the Editor needs.",
     "https://blog.frame.io/2024/03/18/assistant-editor-job-career-advice/"),
]

PATHS = [
    ("Apprentice Editor Pilot Program", "Motion Picture Editors Guild (IATSE Local 700, US)",
     "A Guild program that lets Apprentice Editors and Editing Room Assistants perform Assistant Editor duties in order to learn the job in picture, music or sound. Employers need the Guild's approval before hiring into it.",
     "https://www.editorsguild.com/Main-Menu/Employers/Apprentice-Editor-Pilot-Program"),
    ("ACE Internship Program", "American Cinema Editors",
     "Places interns in editing rooms to shadow assistant editors on scripted TV, features and reality, with tours of post facilities.",
     "https://americancinemaeditors.org/ed-center/ace-internship-program/"),
    ("CCE Mentorship Program", "Canadian Cinema Editors",
     "A one-year Canadian program with an assistant editing category among its mentee streams.",
     "https://cceditors.ca/what-we-do/mentorship-program"),
]

QUESTIONS = [
    "If an agent does ingest, sync, organizing and prep, what does a second assistant do on day one?",
    "Does the Assistant Editor now spend less time in the Editor's room, or more, because the grunt work is gone?",
    "Do Editors still want to pass on what they know, and do they have the time?",
    "Is the real craft learned from watching the Editor shape a scene, and can that be taught any other way?",
]


def _cards(rows):
    return "".join('<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a></h3>'
                   '<p class="note">' + e(w) + '</p><p>' + e(x) + '</p></article>' for t, w, x, u in rows)


def render(leaf, favicon, updated):
    q = "".join("<li>" + e(x) + "</li>" for x in QUESTIONS)
    body = ('<p>' + e(INTRO) + '</p><p class="note">Facts were read on ' + e(AS_OF) + ' from the linked pages. The questions further down are ours, not findings.</p>'
            '<h2>What the software makers announced</h2>' + _cards(NEWS)
            + '<h2>What the Assistant Editor does now</h2>' + _cards(JOB)
            + '<div class="box"><h3>Our observation</h3><p>The tasks Frame.io lists for second assistants (ingest, sync, prep) and the tasks Adobe says its agents could take on (organizing footage, removing duplicates, flagging problems) overlap. '
              'That is our reading of two separate sources, not something either one says.</p></div>'
            + '<h2>The open question</h2><div class="box"><p>Where does the next generation learn storytelling?</p><ul>' + q + '</ul>'
              '<p>We do not have the answers, and we do not want to guess. If you are an Assistant Editor or an Editor, tell us what you are seeing. Anonymous is fine.</p>'
              '<p><a class="btn" href="mailto:hello@postproductioncanada.ca?subject=Assistant%20Editors%20and%20AI">Send us your view →</a></p></div>'
            + '<h2>Where people learn the job today</h2>' + _cards(PATHS))
    return topics._page(leaf, favicon, updated, "The Digital Assistant Editor",
                        "AI agents are taking on Assistant Editor tasks. What was announced, how the job works today, and where the next Editors will learn the craft.",
                        "🤖 The Digital Assistant Editor", "If an agent does the prep, where does the craft get passed on?", body)
