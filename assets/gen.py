"""Generates every SVG in this folder. Run: python3 assets/gen.py"""
import random
from pathlib import Path

OUT = Path(__file__).parent
ACC = "#FF4D1A"
GRAY = "#8B949E"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# 5x7 dot-matrix glyphs
FONT = {
    "A": "01110 10001 10001 11111 10001 10001 10001",
    "B": "11110 10001 10001 11110 10001 10001 11110",
    "D": "11110 10001 10001 10001 10001 10001 11110",
    "E": "11111 10000 10000 11110 10000 10000 11111",
    "F": "11111 10000 10000 11110 10000 10000 10000",
    "G": "01110 10001 10000 10111 10001 10001 01111",
    "H": "10001 10001 10001 11111 10001 10001 10001",
    "I": "01110 00100 00100 00100 00100 00100 01110",
    "K": "10001 10010 10100 11000 10100 10010 10001",
    "L": "10000 10000 10000 10000 10000 10000 11111",
    "M": "10001 11011 10101 10101 10001 10001 10001",
    "N": "10001 10001 11001 10101 10011 10001 10001",
    "O": "01110 10001 10001 10001 10001 10001 01110",
    "R": "11110 10001 10001 11110 10100 10010 10001",
    "S": "01111 10000 10000 01110 00001 00001 11110",
    "T": "11111 00100 00100 00100 00100 00100 00100",
    "U": "10001 10001 10001 10001 10001 10001 01110",
    "W": "10001 10001 10001 10101 10101 10101 01010",
    "X": "10001 10001 01010 00100 01010 10001 10001",
    "Y": "10001 10001 01010 00100 00100 00100 00100",
    "3": "11111 00010 00100 00010 00001 10001 01110",
    "×": "00000 10001 01010 00100 01010 10001 00000",
    "↗": "00000 01111 00011 00101 01001 10000 00000",
    " ": "00000 00000 00000 00000 00000 00000 00000",
}


def dots(text, col0=0, row0=0):
    """Yield (col, row, char_index, char) for every lit dot in text."""
    for i, ch in enumerate(text):
        for r, bits in enumerate(FONT[ch].split()):
            for c, b in enumerate(bits):
                if b == "1":
                    yield col0 + i * 6 + c, row0 + r, i, ch


def svg(w, h, style, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}"><style>{style}</style>{body}</svg>\n')


# ── 01 HERO ─────────────────────────────────────────────────────────────
def hero(theme):
    rnd = random.Random(7)  # same seed → both themes get identical choreography
    fg, grid, dim = ("#EDEDED", "#FFFFFF", "#6E7681") if theme == "dark" else ("#0A0A0A", "#000000", "#8C959F")
    P, W, H, T = 14, 1200, 476, 10  # pitch, canvas, loop seconds
    C0, R1, R2 = 10, 9, 19          # first column, row of each line
    X = lambda c: 7 + P * c
    span = 65                       # columns in "RIYAN AINUR"
    sweep = 1.6                     # seconds for the decode beam

    style = f"""
.d{{fill:{ACC};opacity:0;animation:d {T}s linear infinite backwards}}
@keyframes d{{0%{{opacity:0;fill:{ACC}}}.6%{{opacity:1}}1.2%{{opacity:.25}}1.8%{{opacity:1;fill:{ACC}}}5%{{fill:{fg}}}
78%{{opacity:1;fill:{fg}}}78.6%{{fill:{ACC}}}79.2%{{opacity:.2}}79.8%{{opacity:1}}82%{{opacity:0}}100%{{opacity:0}}}}
.beam{{animation:b {T}s linear infinite}}
@keyframes b{{0%{{transform:translateX(0);opacity:1}}16%{{transform:translateX({span*P}px);opacity:1}}16.5%,77.9%{{opacity:0;transform:translateX({span*P}px)}}
78%{{opacity:1;transform:translateX(0)}}94%{{opacity:1;transform:translateX({span*P}px)}}94.5%,100%{{opacity:0}}}}
.g1{{animation:g1 {T}s step-end infinite}}.g2{{animation:g2 {T}s step-end infinite}}
@keyframes g1{{0%{{transform:none}}44%{{transform:translateX({P}px)}}44.4%{{transform:translateX(-{P//2}px)}}44.8%{{transform:none}}}}
@keyframes g2{{0%{{transform:none}}61%{{transform:translateX(-{2*P}px)}}61.3%{{transform:translateX({P}px)}}61.7%{{transform:none}}}}
.tear{{opacity:0}}.t1{{animation:t1 {T}s step-end infinite}}.t2{{animation:t2 {T}s step-end infinite}}
@keyframes t1{{0%{{opacity:0}}44%{{opacity:.9}}44.8%{{opacity:0}}}}
@keyframes t2{{0%{{opacity:0}}61%{{opacity:.9}}61.7%{{opacity:0}}}}
.cur{{animation:c 1.1s step-end infinite}}@keyframes c{{50%{{opacity:0}}}}
.tw{{opacity:0;animation:tw linear infinite}}@keyframes tw{{0%,88%,100%{{opacity:0}}94%{{opacity:1}}}}
.lbl{{font:500 11px/1 {MONO};letter-spacing:.18em;fill:{dim}}}
.s1,.s2,.s3{{animation:{T}s step-end infinite}}.s1{{animation-name:s1}}.s2{{animation-name:s2}}.s3{{animation-name:s3}}
@keyframes s1{{0%{{opacity:1}}16%,100%{{opacity:0}}}}
@keyframes s2{{0%{{opacity:0}}16%{{opacity:1}}78%,100%{{opacity:0}}}}
@keyframes s3{{0%{{opacity:0}}78%,100%{{opacity:1}}}}
.pulse{{animation:p 1.1s ease-in-out infinite}}@keyframes p{{50%{{opacity:.2}}}}
"""
    b = [f'<defs><pattern id="g" width="{P}" height="{P}" patternUnits="userSpaceOnUse">'
         f'<circle cx="{P/2}" cy="{P/2}" r="1.1" fill="{grid}" fill-opacity=".09"/></pattern>'
         f'<linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="{ACC}" stop-opacity=".22"/></linearGradient>'
         f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>'
         f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#g)"/>']

    # ambient twinkles on the grid
    for _ in range(46):
        c, r = rnd.randrange(1, W // P - 1), rnd.randrange(1, H // P - 1)
        col = ACC if rnd.random() < .35 else fg
        b.append(f'<circle class="tw" cx="{X(c)}" cy="{X(r)}" r="1.8" fill="{col}" '
                 f'style="animation-duration:{rnd.uniform(4, 9):.2f}s;animation-delay:-{rnd.uniform(0, 9):.2f}s"/>')

    # tear lines flashed during glitches
    for cls, row in (("t1", R1), ("t2", R2)):
        b.append(f'<rect class="tear {cls}" x="0" y="{X(row + 3) - 1}" width="{W}" height="2" fill="{ACC}"/>')

    # the name
    hot = []
    for cls, text, row, lag in (("g1", "RIYAN AINUR", R1, 0), ("g2", "RAHMAN", R2, .18)):
        b.append(f'<g class="{cls}">')
        for c, r, _, _ in dots(text, C0, row):
            d = (c - C0) / span * sweep + rnd.uniform(0, .3) + lag
            b.append(f'<circle class="d" cx="{X(c)}" cy="{X(r)}" r="5" style="animation-delay:{d:.2f}s"/>')
            if rnd.random() < .06:
                hot.append((c, r))
        b.append('</g>')
    for c, r in hot:
        b.append(f'<circle class="tw" cx="{X(c)}" cy="{X(r)}" r="5" fill="{ACC}" '
                 f'style="animation-duration:{rnd.uniform(3, 6):.2f}s;animation-delay:-{rnd.uniform(0, 6):.2f}s"/>')

    # cursor block after RAHMAN
    cc = C0 + 6 * 6
    b.append(f'<g class="cur" fill="{ACC}" filter="url(#glow)">' + "".join(
        f'<circle cx="{X(c)}" cy="{X(r)}" r="5"/>' for c in range(cc, cc + 3) for r in range(R2, R2 + 7)) + '</g>')

    # decode beam
    y0, y1 = X(R1) - 40, X(R2 + 6) + 40
    b.append(f'<g class="beam"><rect x="{X(C0) - 160}" y="{y0}" width="160" height="{y1 - y0}" fill="url(#trail)"/>'
             f'<rect x="{X(C0) - 1}" y="{y0}" width="2" height="{y1 - y0}" fill="{ACC}" filter="url(#glow)"/></g>')

    # chrome: status + registration marks
    lx, ly = X(C0) - 5, 56
    b.append(f'<circle class="pulse" cx="{lx + 4}" cy="{ly - 4}" r="3.5" fill="{ACC}"/>')
    for i, s in enumerate(("DECODING", "ONLINE", "REBOOT"), 1):
        b.append(f'<text class="lbl s{i}" x="{lx + 18}" y="{ly}">{s}</text>')
    b.append(f'<text class="lbl" x="{X(C0 + span - 1) + 5}" y="{ly}" text-anchor="end">RAR/01</text>')
    m = 24
    for x, y, sx, sy in ((m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        b.append(f'<path d="M{x} {y + 14 * sy}V{y}H{x + 14 * sx}" fill="none" stroke="{dim}" stroke-width="1"/>')

    return svg(W, H, style, "".join(b), "RIYAN AINUR RAHMAN")


# ── 02 MICRO IDENTITY / 03 LINKS ───────────────────────────────────────
def line(text, pitch, r, start=0.0, step=0.05):
    cols = len(text) * 6 - 1
    pad = pitch
    w, h = cols * pitch + 2 * pad, 7 * pitch + 2 * pad
    style = (".c{opacity:0;animation:in .5s steps(3) forwards}"
             "@keyframes in{0%{opacity:0}40%{opacity:1}60%{opacity:.3}100%{opacity:1}}")
    body = []
    for c, row, i, ch in dots(text):
        fill = ACC if ch in "×↗" else GRAY
        body.append(f'<circle class="c" cx="{pad + c * pitch + pitch / 2:.1f}" cy="{pad + row * pitch + pitch / 2:.1f}" '
                    f'r="{r}" fill="{fill}" style="animation-delay:{start + i * step:.2f}s"/>')
    return svg(w, h, style, "".join(body), text.replace("↗", "").strip())


if __name__ == "__main__":
    files = {
        "hero-dark.svg": hero("dark"),
        "hero-light.svg": hero("light"),
        "identity.svg": line("SOFTWARE ENGINEER", 4, 1.5, start=1.8),
        "link-github.svg": line("GITHUB ↗", 3, 1.15, start=2.6),
        "link-x.svg": line("X ↗", 3, 1.15, start=2.8),
        "link-linkedin.svg": line("LINKEDIN ↗", 3, 1.15, start=3.0),
        "link-web.svg": line("WEB ↗", 3, 1.15, start=3.2),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
        print(f"{name:20} {len(content) / 1024:6.1f} KB")
