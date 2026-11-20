"""Sound editing and sound design in Canada. Facts read from the linked pages on AS_OF."""
import html
import topics

e = html.escape
AS_OF = "November 20, 2026"

WHAT = ("Sound editing and sound design is the part of post where dialogue is cleaned and replaced, effects and Foley are built and cut, and the world "
        "of the film or series is made audible, before a re-recording mixer balances it all in the final mix. In Canada the work is celebrated in its own awards: "
        "the Canadian Screen Awards have separate categories for Best Sound Editing and Best Sound Mixing.")

# (name, role/line, text, url, link label)
PEOPLE = [
    ("Jane Tattersall", "Supervising sound editor and sound designer, Toronto",
     "Born in England, she moved to Canada as a child and studied at Queen's University. She worked as a researcher on TVOntario documentaries before apprenticing as a sound editor, "
     "then formed her own company, Tattersall Sound. Wikipedia describes her as a six-time Genie Award and Canadian Screen Award winner for Best Sound Editing. "
     "Her first Genie win was for Naked Lunch, where she reportedly had to put her hand in a jar of cockroaches to get the hissing sound she wanted. "
     "In January 2023, Streamland Media named her managing director of Picture Shop and senior vice president of Formosa Group in Toronto.",
     "https://en.wikipedia.org/wiki/Jane_Tattersall"),
    ("Christian Cooke and Brad Zoern", "Re-recording mixers, Toronto: Oscar-nominated twice",
     "Cooke and Zoern were nominated for the Academy Award for Best Sound Mixing for The Shape of Water at the 90th Academy Awards, along with production mixer Glen Gauthier. "
     "KawarthaNOW, Cooke's hometown outlet in Lindsay, Ontario, reported that Cooke and Zoern work as re-recording mixers at Deluxe Toronto. "
     "They were nominated again for Frankenstein in Best Sound at the 98th Academy Awards. F1 won that category. Zoern was born in Windsor, Ontario.",
     "https://kawarthanow.com/2018/01/23/lindsays-christian-cooke-gets-an-oscar-nomination-on-his-birthday/"),
    ("Glen Gauthier", "Production sound mixer, Ontario",
     "A Canadian location sound mixer who has worked since 1978 and was nominated alongside Cooke and Zoern for The Shape of Water. His Wikipedia entry lists Academy Award, BAFTA, Gemini and Genie nominations.",
     "https://en.wikipedia.org/wiki/Glen_Gauthier"),
]

READING = [
    ("Jane Tattersall takes positions at Streamland Media's picture and sound divisions", "Post Magazine, January 2023",
     "The announcement of her move to Picture Shop and Formosa Group in Toronto.",
     "https://www.postmagazine.com/Press-Center/Daily-News/2023/Jane-Tattersall-takes-positions-at-Streamland-Me.aspx"),
    ("Canadian Screen Award for Best Sound Editing", "Wikipedia",
     "Winners and nominees of Canada's top sound editing award, from the Genies to the Canadian Screen Awards.",
     "https://en.wikipedia.org/wiki/Canadian_Screen_Award_for_Best_Sound_Editing"),
    ("Canadian Screen Award for Best Sound Mixing", "Wikipedia",
     "The matching list for sound mixing.",
     "https://en.wikipedia.org/wiki/Canadian_Screen_Award_for_Best_Sound_Mixing"),
]


def _cards(rows):
    return "".join('<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a></h3>'
                   '<p class="note">' + e(w) + '</p><p>' + e(x) + '</p></article>' for t, w, x, u in rows)


def render(leaf, favicon, updated):
    body = ('<p>' + e(WHAT) + '</p><p class="note">Facts on this page were read on ' + e(AS_OF) + ' from the pages linked. Canadian only. '
            'If something is out of date, or you know a Canadian sound editor, designer or mixer with a story worth telling, send it to us.</p>'
            '<h2>Canadian sound people</h2>' + _cards(PEOPLE)
            + '<h2>Reading</h2>' + _cards(READING)
            + '<h2>Send us a name or a story</h2><p>Email <a href="mailto:hello@postproductioncanada.ca?subject=Sound">hello@postproductioncanada.ca</a> '
              'with a link to the original and we will check it before it goes up.</p>')
    return topics._page(leaf, favicon, updated, "Sound & Emotion: sound editing and design in Canada",
                        "Canadian sound editors, designers and mixers, and the awards that celebrate their work.",
                        "🎶 Sound & Emotion", "Sound editing and design, and the people who make Canadian film and television feel right.", body)
