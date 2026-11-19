#!/usr/bin/env python3
# /// script
# dependencies = ["fonttools", "brotli"]
# ///
"""Generate fetch.svg: an animated, Catppuccin Mocha fastfetch readout for the profile README.

Edit LINES below, then run:  uv run scripts/gen_fetch.py
  --static  writes the finished frame (no animation), for checking the layout.

The font (DejaVu Sans Mono, subset) is embedded in the SVG, so the layout is the
same on every machine instead of depending on the viewer's installed fonts.
"""
import base64
import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ART = (ROOT / "scripts" / "pikachu.txt").read_text(encoding="utf-8").splitlines()
STATIC = "--static" in sys.argv
OUT = ROOT / ("fetch-static.svg" if STATIC else "fetch.svg")
FONT_FILES = {
    400: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    700: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
}

# Catppuccin Mocha (same palette as ~/.config/fastfetch/config.jsonc)
C = dict(
    crust="#11111b", mantle="#181825", base="#1e1e2e", surface="#313244",
    overlay="#7f849c", subtext="#a6adc8", text="#cdd6f4",
    mauve="#cba6f7", pink="#f5c2e7", red="#f38ba8", peach="#fab387",
    yellow="#f9e2af", green="#a6e3a1", teal="#94e2d5", sky="#89dceb",
    blue="#89b4fa", lavender="#b4befe",
)

# Each line is a list of (column, text, color, bold).
def kv(key, value, color):
    return [(0, key, color, True), (10, value, C["text"], False)]

def item(glyph, name, value, color):
    return [(0, glyph, C["overlay"], False), (2, name, color, False), (15, value, C["subtext"], False)]

def head(text, color):
    return [(0, text, color, True)]

LINES = [
    [(0, "ivan", C["mauve"], True), (4, "@", C["overlay"], False), (5, "github", C["blue"], True)],
    [(0, "─" * 34, C["overlay"], False)],
    kv("OS", "Computer Engineering @ UBC", C["mauve"]),
    kv("Site", "ivanluo.xyz", C["pink"]),
    kv("Kernel", "software + embedded, both ends of the wire", C["red"]),
    [],
    head("Jobs", C["peach"]),
    item("├", "AMD", "incoming firmware engineer, summer 2027", C["peach"]),
    item("├", "Apera AI", "helping robots see and pick stuff up (fast)", C["peach"]),
    item("├", "Leanpub", "shipped their first iOS app in 7 weeks, 1k+ downloads", C["peach"]),
    item("└", "UBC Rocket", "ground station + firmware for jigs on the MCU", C["peach"]),
    [],
    head("Projects", C["green"]),
    item("├", "Roomie", "floor plan in -> furnished 3D home, real IKEA stuff", C["green"]),
    item("└", "Gravity", "N-body gravity sandbox in your browser", C["green"]),
    [],
    head("Hobbies", C["sky"]),
    item("├", "running", "chasing a sub-2 half marathon", C["sky"]),
    item("├", "snowboard", "CASI level 2 instructor", C["sky"]),
    item("├", "hiking", "wherever the trail goes", C["sky"]),
    item("└", "gaming", "League of Legends & CS", C["sky"]),
    [],
    kv("Packages", "C, C++, Python, TypeScript, Swift, SystemVerilog", C["blue"]),
    kv("Status", "always down to chat projects, internships, collabs", C["lavender"]),
]
DOTS = [C[k] for k in ("red", "peach", "yellow", "green", "teal", "blue", "mauve", "pink")]

# Geometry
FONT = 14
CW = FONT * 1233 / 2048   # DejaVu Sans Mono advance (1233 of 2048 units)
LH = 21             # line height
PAD = 28
BAR = 34            # title bar height
CELL_W, CELL_H = 9, 18    # one braille character
ART_W = 30 * CELL_W
GAP = 44
CMD = "fastfetch"

# Timeline (seconds)
T_TYPE = 0.5        # typing starts
T_KEY = 0.085       # per keystroke
T_OUT = T_TYPE + len(CMD) * T_KEY + 0.35   # output starts after "enter"
T_LINE = 0.055      # stagger between output lines

prompt_y = BAR + PAD + FONT
body_top = prompt_y + 18
info_x = PAD + ART_W + GAP
n_info = len(LINES) + 2           # + blank + colour dots
info_h = n_info * LH
art_h = len(ART) * CELL_H
body_h = max(info_h, art_h)
final_prompt_y = body_top + body_h + 26
info_cols = max(col + len(txt) for segs in LINES for col, txt, *_ in segs)
W = int(info_x + info_cols * CW + PAD + 4)
H = int(final_prompt_y + PAD - 6)


def font_face(weight, path, chars):
    """Subset a font to the characters used and return an @font-face rule with it inlined."""
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = []
    opts.name_IDs = [0, 1, 2, 3]   # keep copyright + family names
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    data = base64.b64encode(buf.getvalue()).decode()
    return (f"@font-face{{font-family:FetchMono;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")


def braille_dots(ch):
    """Yield (dx, dy) dot positions in a 2x4 grid for one braille character."""
    bits = ord(ch) - 0x2800
    if not 0 <= bits <= 0xFF:
        return
    layout = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 3), (1, 3)]
    for i, (cx, cy) in enumerate(layout):
        if bits & (1 << i):
            yield cx, cy


def prompt(y, cls=""):
    return (
        f'<text class="mono {cls}" x="{PAD}" y="{y}">'
        f'<tspan fill="{C["blue"]}" font-weight="700">~</tspan>'
        f'<tspan x="{PAD + 2 * CW:.1f}" fill="{C["green"]}">❯</tspan></text>'
    )


used = set(CMD + "~❯ivan@github: ")
for segs in LINES:
    for _, txt, *_ in segs:
        used |= set(txt)
chars = "".join(sorted(used))

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'role="img" aria-label="fastfetch readout for Ivan Luo">')
a("<style>"
  + "".join(font_face(w, p, chars) for w, p in FONT_FILES.items())
  + f".mono{{font-family:FetchMono,monospace;font-size:{FONT}px}}"
  + (".in{opacity:1}" if STATIC else ".in{opacity:0;animation:in .18s ease-out forwards}") +
  "@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}"
  ".blink{animation:blink 1.05s steps(1) infinite}"
  "@keyframes blink{50%{opacity:0}}"
  "@media (prefers-reduced-motion:reduce){.in{animation:none;opacity:1}}"
  "</style>")

# Window
a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{C["base"]}" stroke="{C["surface"]}"/>')
a(f'<path d="M12.5 .5h{W-25}a12 12 0 0 1 12 12V{BAR}H.5V12.5a12 12 0 0 1 12-12z" fill="{C["mantle"]}"/>')
for i, col in enumerate((C["red"], C["yellow"], C["green"])):
    a(f'<circle cx="{22 + i*20}" cy="{BAR/2}" r="6" fill="{col}"/>')
a(f'<text class="mono" x="{W/2}" y="{BAR/2 + 4.5}" text-anchor="middle" fill="{C["overlay"]}" '
  f'font-size="12">ivan@github: ~</text>')

# Prompt + typed command (revealed by a clip that grows one character per keystroke)
cmd_x = PAD + 4 * CW
steps = len(CMD)
widths = ";".join(f"{max(0, i * CW - 1.5):.2f}" for i in range(steps + 1))
keytimes = ";".join(f"{i / steps:.4f}" for i in range(steps + 1))
dur = steps * T_KEY
if STATIC:
    a(prompt(prompt_y))
    a(f'<text class="mono" x="{cmd_x}" y="{prompt_y}" fill="{C["text"]}">{CMD}</text>')
else:
    a(f'<clipPath id="type"><rect x="{cmd_x}" y="{prompt_y - FONT}" width="0" height="{FONT + 6}">'
      f'<animate attributeName="width" values="{widths}" keyTimes="{keytimes}" calcMode="discrete" '
      f'begin="{T_TYPE}s" dur="{dur:.3f}s" fill="freeze"/></rect></clipPath>')
    a(prompt(prompt_y))
    a(f'<text class="mono" x="{cmd_x}" y="{prompt_y}" fill="{C["text"]}" clip-path="url(#type)">{CMD}</text>')
    # Cursor: follows the typing, then disappears on enter
    xs = ";".join(f"{cmd_x + i * CW:.2f}" for i in range(steps + 1))
    a(f'<rect x="{cmd_x}" y="{prompt_y - FONT + 1}" width="{CW}" height="{FONT + 3}" fill="{C["text"]}" opacity=".85">'
      f'<animate attributeName="x" values="{xs}" keyTimes="{keytimes}" calcMode="discrete" '
      f'begin="{T_TYPE}s" dur="{dur:.3f}s" fill="freeze"/>'
      f'<animate attributeName="opacity" values=".85;0;.85" keyTimes="0;.5;1" dur="1.05s" '
      f'calcMode="discrete" repeatCount="indefinite" end="{T_OUT - 0.2:.2f}s"/>'
      f'<set attributeName="visibility" to="hidden" begin="{T_OUT - 0.2:.2f}s"/></rect>')

# Pikachu: braille dots drawn as circles, one row at a time
for r, line in enumerate(ART):
    delay = T_OUT + r * T_LINE
    a(f'<g class="in" style="animation-delay:{delay:.3f}s" fill="{C["yellow"]}">')
    for c, ch in enumerate(line):
        for dx, dy in braille_dots(ch):
            x = PAD + c * CELL_W + 2.5 + dx * 4.5
            y = body_top + r * CELL_H + 2.5 + dy * 4.4
            a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.7"/>')
    a("</g>")

# Info column
for i, segs in enumerate(LINES):
    if not segs:
        continue
    y = body_top + i * LH + FONT
    delay = T_OUT + i * T_LINE
    # Keep the whole <text> on one source line: whitespace between tspans is rendered
    # by some browsers (Safari/Firefox) as line breaks or extra spaces.
    spans = "".join(
        f'<tspan x="{info_x + col * CW:.1f}" fill="{color}"{" font-weight=\"700\"" if bold else ""}>'
        f'{escape(txt)}</tspan>'
        for col, txt, color, bold in segs
    )
    a(f'<g class="in" style="animation-delay:{delay:.3f}s"><text class="mono" y="{y}">{spans}</text></g>')

# Colour dots
i = len(LINES) + 1
y = body_top + i * LH + FONT / 2 + 1
a(f'<g class="in" style="animation-delay:{T_OUT + i * T_LINE:.3f}s">')
for k, col in enumerate(DOTS):
    a(f'<circle cx="{info_x + 7 + k * 22}" cy="{y}" r="7" fill="{col}"/>')
a("</g>")

# Fresh prompt with a blinking cursor once everything has printed
t_end = T_OUT + (n_info + 1) * T_LINE
a(f'<g class="in" style="animation-delay:{t_end:.3f}s">{prompt(final_prompt_y)}'
  f'<rect class="blink" x="{cmd_x}" y="{final_prompt_y - FONT + 1}" width="{CW}" height="{FONT + 3}" '
  f'fill="{C["text"]}" opacity=".85"/></g>')

a("</svg>")
OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} ({W}x{H}, {OUT.stat().st_size // 1024} KB)")
