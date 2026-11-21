"""House style applied to our own text: the word Editor and the phrase Post Production are always capitalized."""
import re

_ED = re.compile(r"(?<![\w/.@#\-])editor(s?)(?![\w/@]|\.[a-z])")
_PP = re.compile(r"(?<![\w/.@#\-])post([ -])production(?![\w/@]|\.[a-z])", re.I)


def _pp(m):
    return m.group(0) if m.group(0).isupper() else "Post" + m.group(1) + "Production"


def cap_text(s):
    return _PP.sub(_pp, _ED.sub(lambda m: "Editor" + m.group(1), s))


import json as _json
from pathlib import Path as _Path

_REG = None


def registry():
    global _REG
    if _REG is None:
        try:
            d = _json.loads((_Path(__file__).resolve().parent / "imdb_people.json").read_text(encoding="utf-8"))
        except Exception:
            d = {}
        _REG = {k: v for k, v in d.items() if not k.startswith("_")}
    return _REG


IMDB_STYLE = "font-size:.72em;font-weight:800;background:#f5c518;color:#000;border-radius:4px;padding:1px 5px;text-decoration:none;font-family:ui-sans-serif,-apple-system,sans-serif"


def imdb_badge(name):
    reg = registry()
    if name not in reg:
        return ""
    return '<a class="imdbl" href="https://www.imdb.com/name/' + reg[name] + '/" target="_blank" rel="noopener" style="' + IMDB_STYLE + '">IMDb</a>'


def link_people(t):
    """Add a small IMDb link after the first mention, on each page or article, of every verified person.
    Skips headings, existing links, scripts and third-party headline cards."""
    reg = registry()
    if not reg:
        return t
    names = sorted(reg, key=len, reverse=True)
    pat = re.compile("(" + "|".join(re.escape(n) for n in names) + ")")
    seen, out = set(), []
    depth_a = depth_h = 0
    pname = False
    mode = None
    for seg in re.split(r"(<[^>]*>)", t):
        if seg.startswith("<"):
            low = seg.lower()
            if re.match(r"<(script|style|title|option|button)\b", low):
                mode = "skip"
            elif re.match(r"</(script|style|title|option|button)\b", low):
                mode = None
            elif re.match(r'<article class="(card|pick|frame)\b', low):
                mode = "card"
            elif low.startswith("</article") and mode == "card":
                mode = None
            elif re.match(r"<a\b", low):
                depth_a += 1
            elif low.startswith("</a"):
                depth_a = max(0, depth_a - 1)
            elif low.startswith('<h3 class="pname"'):
                depth_h += 1
                pname = True
            elif pname and low.startswith("</h3"):
                depth_h = max(0, depth_h - 1)
                pname = False
            elif re.match(r"<h[12]\b", low):
                depth_h += 1
            elif re.match(r"</h[12]\b", low):
                depth_h = max(0, depth_h - 1)
            out.append(seg)
        elif mode is None and not depth_a and not depth_h:
            def rep(m):
                n = m.group(1)
                if n in seen:
                    return n
                seen.add(n)
                return (n + ' <a class="imdbl" href="https://www.imdb.com/name/' + reg[n] + '/" target="_blank" rel="noopener" '
                        'style="' + IMDB_STYLE + '">IMDb</a>')
            out.append(pat.sub(rep, seg))
        else:
            out.append(seg)
    return "".join(out)


# Guild letters, only where a source confirms them. CCE: cceditors.ca and the Canadian Editors profiles (canadians.py).
# ACE: americancinemaeditors.org lists Schoonmaker and Murch as ACE. Add more only after checking a source.
CREDENTIALS = {
    "Ronald Sanders": "CCE", "Jay Prychidny": "CCE", "Don Cassidy": "CCE", "Cam McLauchlin": "CCE",
    "Wendy Hallam Martin": "CCE, ACE", "Thelma Schoonmaker": "ACE", "Walter Murch": "ACE",
}

# Other people named in the Originals: coloured like the rest, no letters or IMDb link unless verified above.
PEOPLE_EXTRA = {"Tim Burton", "Martin Scorsese", "Joe Walker", "Jennifer Lame", "Hal Ashby", "Steven Soderbergh", "Chloé Zhao", "John Grierson", "Brock Mitchell", "Mark Robson"}


# Companies, studios, agencies, guilds and institutions named in the Originals (purple). Each name was found in the article text.
COMPANIES = {
    "Deluxe Toronto", "Deluxe", "Technicolor Canada", "Technicolor Group", "Technicolor", "Adobe", "Blackmagic", "Frame.io", "Netflix", "Autodesk",
    "DNEG", "Digital Domain", "Sony Pictures Imageworks", "Rodeo FX", "Mikros Animation", "Mikros", "MPC", "Method Studios",
    "Rainmaker Digital Effects", "Citelab", "Urban Post Production", "Niagara Custom Lab", "Gaumont Pictures", "Bell Media", "Astral Media",
    "National Film Board", "CAVCO", "Creative BC", "Ontario Creates", "IATSE", "Motion Picture Editors Guild", "Canadian Cinema Editors",
    "American Cinema Editors", "Motion Picture Association", "Boris FX", "ILM", "Mr. X", "Documentary Organization of Canada", "Hot Docs",
    "Canadian Pacific Railway", "Associated Screen News", "Bellevue-Humphries", "Global Vision", "Revenu Québec", "Orphiq", "LIFT", "MELS",
    "Guild of Music Supervisors", "ACMI", "Berklee", "HBO", "Quebecor",
}


def mark_people(t):
    """Wrap verified people's names in a coloured span and add guild letters after the first mention in each article.
    Skips links, headings, scripts and styles. Run after link_people so the IMDb badge stays after the letters."""
    names = sorted(set(registry()) | set(CREDENTIALS) | PEOPLE_EXTRA | COMPANIES, key=len, reverse=True)
    pat = re.compile("(?<![\\w])(" + "|".join(re.escape(n) for n in names) + ")(?![\\w])")
    seen, out = set(), []
    depth_a = depth_h = 0
    mode = None
    for seg in re.split(r"(<[^>]*>)", t):
        if seg.startswith("<"):
            low = seg.lower()
            if re.match(r"<(script|style|title)\b", low):
                mode = "skip"
            elif re.match(r"</(script|style|title)\b", low):
                mode = None
            elif re.match(r"<a\b", low):
                depth_a += 1
            elif low.startswith("</a"):
                depth_a = max(0, depth_a - 1)
            elif re.match(r"<h[1-3]\b", low):
                depth_h += 1
            elif re.match(r"</h[1-3]\b", low):
                depth_h = max(0, depth_h - 1)
            out.append(seg)
        elif mode is None and not depth_a and not depth_h:
            def rep(m):
                n = m.group(1)
                extra = ""
                if n not in seen and n in CREDENTIALS:
                    extra = ", " + CREDENTIALS[n]
                seen.add(n)
                return '<span class="' + ("co" if n in COMPANIES else "pn") + '">' + n + extra + "</span>"
            out.append(pat.sub(rep, seg))
        else:
            out.append(seg)
    return "".join(out)
