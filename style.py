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
