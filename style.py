"""House style applied to our own text: the word Editor and the phrase Post Production are always capitalized."""
import re

_ED = re.compile(r"(?<![\w/.@#\-])editor(s?)(?![\w/@]|\.[a-z])")
_PP = re.compile(r"(?<![\w/.@#\-])post([ -])production(?![\w/@]|\.[a-z])", re.I)


def _pp(m):
    return m.group(0) if m.group(0).isupper() else "Post" + m.group(1) + "Production"


def cap_text(s):
    return _PP.sub(_pp, _ED.sub(lambda m: "Editor" + m.group(1), s))
