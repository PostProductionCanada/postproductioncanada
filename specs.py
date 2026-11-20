"""Delivery specs and tech: where the specs live, a codec chart, and a storage chart.
Codec data rates are from Apple (ProRes) and Avid (DNxHR). Storage hours are our own arithmetic from those rates."""
import html
import topics

e = html.escape
AS_OF = "November 20, 2026"

INTRO = ("A delivery spec is the buyer's rulebook for what you hand over: the file format, resolution, frame rate, audio layout, colour and paperwork. "
         "Every network and streamer has its own, they change, and the one that counts is always the version your buyer sends you. This page points to where the public ones live, "
         "then gives you two reference charts you can use at the start of a job: which codec is which, and how much footage a drive holds.")

SPECS = [
    ("CBC/Radio-Canada: technical specifications for program delivery", "CBC/Radio-Canada",
     "The public program delivery document. The English version we found is Version 5.1 from September 2016. A French version, 6.0 from December 2020, was prepared by CBC/Radio-Canada's UHD/HD/SD working group, so the English file may be out of date. Ask CBC for the version in force on your show.",
     "https://cbc.radio-canada.ca/_files/cbcrc/documents/reporting-to-canadians/tech-standards/technical-specs-for-program-delivery.pdf"),
    ("CBC/Radio-Canada: normes techniques de livraison des programmes, version 6.0", "CBC/Radio-Canada, December 2, 2020 (French)",
     "The newer program delivery standards, covering UHD, HD and SD.",
     "https://site-cbc.radio-canada.ca/documents/impact-and-accountability/technology-norms/Normes%20techniques%20de%20livraison%20des%20programmes_%20version%206_0%20%20%202_dec_2020.pdf"),
    ("Bell Media video specifications", "Bell Media (file dated January 2026 in its web address)",
     "Bell Media's published video specifications for delivery, in English. Confirm with your Bell Media contact which edition applies.",
     "https://www.bellmedia.ca/lede/wp-content/uploads/2026/01/Bell-Media-Video-Specifications-MultiLanguage-EN.pdf"),
    ("Netflix Backlot help center", "Netflix",
     "Netflix publishes its specs here, including the IMF specification (Version 5.1) and its servicing and turnover pages. Netflix describes IMF as the final delivery format for originals, made by a Netflix-approved vendor, and its Content Hub pages list ProRes 422 HQ for servicing turnovers. Netflix notes some specs may not apply to every production, so confirm with your Netflix post team.",
     "https://backlothelp.netflix.com/hc/en-us/articles/7262346654995"),
    ("Prime Video: video requirements", "Amazon Prime Video",
     "Amazon's video delivery requirements for its Prime Video catalogue.",
     "https://videocentral.amazon.com/support/delivery-experience/videos/video-requirements"),
]

# Apple ProRes target data rates, Mb/s at 1920x1080, 29.97 fps (Apple ProRes white paper / support page)
PRORES = [
    ("XDCAM HD422 (50 Mbps) ⭐", "CBC's preferred delivery format and Bell Media's broadcast-ready format (MXF)", 50),
    ("ProRes 422 Proxy", "Offline editing at full resolution", 45),
    ("ProRes 422 LT", "Smaller files for editing and some delivery", 102),
    ("ProRes 422", "Everyday editing and finishing", 147),
    ("ProRes 422 HQ ⭐", "High-quality 4:2:2 finishing and mastering; Bell Media's first choice for HD and UHD delivery", 220),
    ("ProRes 4444", "4:4:4 sources, graphics and alpha channels, nearly lossless", 330),
    ("ProRes 4444 XQ", "The highest-quality 4:4:4 for demanding colour and VFX work", 500),
]
# Avid DNxHR, MiB/s at UHD 3840x2160, 23.976 fps (Avid knowledge base)
DNXHR = [
    ("DNxHR LB", "Low bandwidth, for offline editing", 17.14),
    ("DNxHR SQ", "Standard quality", 55.07),
    ("DNxHR HQ", "High quality, standard broadcast uses", 83.26),
    ("DNxHR HQX", "High quality extended, for high-end broadcast production and delivery", 83.26),
    ("DNxHR 444", "4:4:4 and RGB, for VFX work and cinema delivery", 166.61),
]

NORMAL = [
    ("CBC/Radio-Canada (v5.1, 2016)", "MXF, XDCAM HD422 50 Mbps (preferred)", "Accepts 29.97i, plus 23.976p, 25i, 25p and 29.97p; the frame rate must stay constant", "Timecode continuous; drop frame for 29.97"),
    ("Bell Media (revision November 2025)", "HD: MOV or MXF; ProRes HQ or better, then DNxHD 175x, then XDCAM 50. UHD SDR: ProRes HQ or better, or DNxHR HQ or better. The broadcast-ready profile accepts only XDCAM HD 50 Mbps MXF.", "1920x1080 (23.976p preferred, 29.97i second) or 3840x2160 (23.976p); BT.709. UHD HDR (BT.2020) needs prior approval", "Timecode starts at 00:00:00:00"),
]
AUDIO = [
    ("CBC/Radio-Canada (v5.1, 2016)", "PCM, 24-bit, 48 kHz", "-24 LKFS +/- 2 LU, integrated and dialogue", "-2 dBTP maximum", "2 tracks (stereo) up to 6 (5.1), plus described video. CBC layout: 8 channels (L, R, C, LFE, Ls, Rs, DV-L, DV-R)"),
    ("Bell Media (revision November 2025)", "48 kHz, 24-bit", "-24 LKFS +/- 2 LU (ITU-R BS.1770-4)", "-2 dBFS maximum", "Surround and stereo track layouts are specified in its document"),
    ("Netflix (sound mix specs v1.5)", "48 kHz, 24-bit, discrete LPCM .wav or .bwav; no lossy audio", "-27 LKFS +/- 2 LU, dialogue-gated (ITU-R BS.1770-1)", "-2 dB true peak maximum", "5.1 or 2.0 near-field mixes, with stems that add up to the mix"),
]
DRIVES = [1, 2, 4, 8, 16]  # terabytes, decimal


def _gbph(mbps):
    return mbps * 3600 / 8 / 1000


def _table(head, rows):
    h = "".join("<th>" + e(x) + "</th>" for x in head)
    r = "".join("<tr>" + "".join("<td>" + e(str(c)) + "</td>" for c in row) + "</tr>" for row in rows)
    return '<div style="overflow-x:auto"><table class="spec"><thead><tr>' + h + '</tr></thead><tbody>' + r + '</tbody></table></div>'


def render(leaf, favicon, updated):
    css = ("<style>table.spec{border-collapse:collapse;width:100%;font-size:14px}table.spec th,table.spec td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}"
           "table.spec th{font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--mute)}table.spec td:nth-child(n+3){white-space:nowrap}</style>")
    cards = "".join('<article class="box"><h3><a href="' + e(u) + '" target="_blank" rel="noopener">' + e(t) + '</a></h3><p class="note">' + e(w) + '</p><p>' + e(x) + '</p></article>' for t, w, x, u in SPECS)
    pr_rows = [(n, use, f"{m} Mbps", f"{_gbph(m):.0f} GB") for n, use, m in PRORES]
    dn_rows = [(n, use, f"{mib * 8.388608:.0f} Mbps", f"{_gbph(mib * 8.388608):.0f} GB") for n, use, mib in DNXHR]
    hd = _table(["Codec", "What it is for", "Data rate", "Per hour"], pr_rows)
    uhd = _table(["Codec", "What it is for", "Data rate", "Per hour"], dn_rows)
    head = ["Codec"] + [f"{d} TB" for d in DRIVES]
    st_hd = _table(head, [[n] + [f"{d * 1000 / _gbph(m):.1f} h" if d * 1000 / _gbph(m) < 10 else f"{d * 1000 / _gbph(m):.0f} h" for d in DRIVES] for n, use, m in PRORES])
    st_uhd = _table(head, [[n] + [(lambda v: f"{v:.1f} h" if v < 10 else f"{v:.0f} h")(d * 1000 / (_gbph(m) * 4)) for d in DRIVES] for n, use, m in PRORES])
    body = (css + '<p>' + e(INTRO) + '</p><p class="note">Facts read on ' + e(AS_OF) + '. Delivery specs change, so always confirm with the buyer.</p>'
            '<h2>Where the delivery specs live</h2>' + cards
            + '<h2>What is normal in Canadian delivery</h2><p>Read straight from the buyers\' own documents. The common thread: a broadcast-quality 4:2:2 file, ProRes HQ or XDCAM HD at 50 Mbps, at 1080, in the frame rate the show was shot.</p>' + _table(["Buyer", "File and codec", "Picture", "Timecode"], NORMAL)
            + '<h2>🔊 Audio specs</h2><p>The same pattern for sound: 48 kHz and 24-bit everywhere, a peak limit of -2, and a loudness target that differs by buyer. Canadian broadcasters ask for -24 LKFS; Netflix measures dialogue only and asks for -27. Mixing to the wrong one is the classic delivery rejection.</p>' + _table(["Buyer", "Sample rate and bit depth", "Loudness", "Peak", "Tracks"], AUDIO)
            + '<p class="note">LKFS is the loudness unit; LU is the tolerance around the target. Check the spec for how each buyer measures it. These tables come from the documents linked above, as read on ' + e(AS_OF) + '. A newer version may exist, so ask your buyer.</p>'
            + '<p><b>Further reading:</b> <a href="https://www.mixonline.com/post-and-broadcast/mixer-talks-tools-for-tv-docs" target="_blank" rel="noopener">Mixer Talks Tools for TV Docs</a> (Mix, June 4, 2026). A UK re-recording mixer on keeping documentary mixes inside loudness specs and upmixing library music into surround. It is a profile of Nugen Audio\'s plug-ins, so read it as a vendor-friendly view, and it is not Canadian.</p>'
            + '<h2>🎞️ Codec chart</h2><p>A codec is how the picture is squeezed into a file. These are the two main editing and finishing families. '
              'Higher data rate means bigger files and more headroom for grading and VFX.</p>'
              '<h3>XDCAM and Apple ProRes, at 1920 x 1080 and 29.97 fps (⭐ = named in the delivery specs we read)</h3>' + hd +
              '<p class="note">Data rates are Apple\'s target rates from its ProRes documentation, and the 50 Mbps for XDCAM HD422 comes from CBC\'s spec. "Per hour" is our arithmetic from that rate (Mbps x 3,600 seconds, divided by 8, in decimal gigabytes). Real files vary a little, and UHD files are much bigger: UHD has four times the pixels of 1080p.</p>'
              '<h3>Avid DNxHR, at UHD 3840 x 2160 and 23.976 fps</h3>' + uhd +
              '<p class="note">From Avid\'s DNxHR bandwidth table, which lists the rates in megabytes per second (MiB/s); we converted to Mbps and per-hour gigabytes. DNxHR also comes in HD, 2K and 4K sizes. Look up the exact one in Avid\'s table.</p>'
            + '<h2>💾 How much footage does a drive hold?</h2><p>Hours of one camera angle, edited straight from the drive, by codec. Decimal terabytes, as drive makers count them, so a real drive formats a little smaller. Audio, extra camera angles and a second backup copy all need more room.</p>'
              '<h3>HD (1920 x 1080, 29.97 fps)</h3>' + st_hd +
              '<h3>UHD (3840 x 2160), estimated</h3>' + st_uhd +
              '<p class="note">The UHD table simply divides the HD hours by four, because UHD has four times the pixels. It is an estimate: check Apple\'s documentation for exact UHD rates.</p>'
              '<h2>What is not here yet</h2><p>Delivery codecs such as H.264 and H.265, and camera RAW formats, vary too much by camera and settings for a single chart, and we have not found sources we trust for them yet. '
              'Tell us which you want next, and send any delivery spec you would like listed, at <a href="mailto:hello@postproductioncanada.ca?subject=Specs">hello@postproductioncanada.ca</a>.</p>')
    return topics._page(leaf, favicon, updated, "Delivery Specs and Tech",
                        "What is normal in Canadian delivery, video and audio, plus a codec chart and a storage chart for post.",
                        "📐 Delivery Specs and Tech", "What buyers actually ask for, the loudness targets, and how much drive you need.", body)
