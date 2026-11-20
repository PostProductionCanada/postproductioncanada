"""Province emblems: a small emoji icon plus the two-letter code on a coloured pill.
These are simple original icons, not official flags or coats of arms."""
import html

P = {
    "BC": ("🌲", "#166534", "British Columbia"), "AB": ("🏔️", "#1e40af", "Alberta"), "SK": ("🌾", "#a16207", "Saskatchewan"),
    "MB": ("🦬", "#92400e", "Manitoba"), "ON": ("🗼", "#b91c1c", "Ontario"), "QC": ("⚜️", "#1d4ed8", "Québec"),
    "NB": ("🌊", "#0e7490", "New Brunswick"), "NS": ("⚓", "#4338ca", "Nova Scotia"), "PE": ("🥔", "#be123c", "Prince Edward Island"),
    "NL": ("🐋", "#0f766e", "Newfoundland and Labrador"), "YT": ("⛏️", "#6d28d9", "Yukon"), "NT": ("❄️", "#475569", "Northwest Territories"),
    "NU": ("🐻‍❄️", "#334155", "Nunavut"), "CA": ("🍁", "#d52b1e", "Canada"),
}


def badge(code, text=None):
    emoji, col, name = P[code]
    label = text or (code if code != "CA" else "Canada")
    return ('<span title="' + html.escape(name) + '" style="display:inline-block;background:' + col +
            ';color:#fff;font:700 11px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.06em;padding:4px 9px;border-radius:999px;margin:0 4px 0 0;vertical-align:middle">'
            + emoji + " " + html.escape(label) + "</span>")
