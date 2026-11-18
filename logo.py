"""Brand mark: a clapperboard with a maple leaf and mountain range on the slate."""
from urllib.parse import quote

LEAF = ("0,0 9,19 17,14 15,36 34,28 31,45 50,40 42,58 52,68 20,66 6,76 4,76 4,86 -4,86 -4,76 -6,76 "
        "-20,66 -52,68 -42,58 -50,40 -31,45 -34,28 -15,36 -17,14 -9,19")


def _svg(body, red, light, themed, attrs=""):
    def fill(c, extra=""):
        return f'style="fill:{c}{extra}"' if themed else f'fill="{c}"{(" " + extra) if extra else ""}'
    mtn = fill(light, ";opacity:.22") if themed else f'fill="{light}" opacity=".22"'
    stripes = "".join(f'<polygon points="{x},14 {x + 11},14 {x + 5},31 {x - 6},31" {fill(red)}/>' for x in (22, 42, 62, 82))
    leaf_attrs = (f'style="fill:{red};stroke:{red};stroke-width:3;stroke-linejoin:round"' if themed
                  else f'fill="{red}" stroke="{red}" stroke-width="3" stroke-linejoin="round"')
    return (f'<svg viewBox="0 0 100 100" {attrs}>'
            f'<g transform="rotate(-9 10 30)"><rect x="10" y="14" width="80" height="17" rx="3" {fill(body)}/>{stripes}</g>'
            f'<circle cx="14" cy="31" r="2.4" {fill(light)}/>'
            f'<rect x="10" y="34" width="80" height="54" rx="5" {fill(body)}/>'
            f'<polygon points="10,88 28,64 40,76 55,58 72,78 90,68 90,88 10,88" {mtn}/>'
            f'<g transform="translate(50 41) scale(.4)"><polygon points="{LEAF}" {leaf_attrs}/></g>'
            f'</svg>')


def inline():
    """For use inside the page: follows the light and dark theme."""
    return _svg("var(--ink)", "var(--red)", "var(--bg)", True, 'aria-hidden="true"')


def favicon():
    return "data:image/svg+xml," + quote(_svg("#16181d", "#d52b1e", "#f6f4ef", False, 'xmlns="http://www.w3.org/2000/svg"'))
