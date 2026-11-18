"""Generates every SVG in this folder. Run: python3 assets/gen.py

Look: a dark profile card (night sky base) whose loud element is a
pixel-dithered sunset. Project cells show a full-viewport screenshot of each landing page.
Fonts (OFL, ASCII subsets in fonts/) are embedded so they render on GitHub:
Instrument Sans everywhere: 700 for names and values, 600 for labels.
"""
import base64
import math
import random
from pathlib import Path

OUT = Path(__file__).parent
BG, LINE, MARK = "#0E1324", "#323A5A", "#59638C"  # quiet guides, slightly brighter markers
FG, DIM = "#ECEEF6", "#8A91AB"
SUN = "#FFC857"
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
# dusk sky, zenith to horizon
SKY = ["#111836", "#1B2462", "#2E3192", "#55369F", "#8B3A99", "#C2427F", "#EC5A6A", "#FF8552", "#FFB24A", "#FFD27A"]
WATER = ["#0F1430", "#181E48", "#262A66", "#3A2F7A"]
CLOUD = ["#6B3F8F", "#B5559A", "#F27D8E", "#FFB07A", "#FFE1B0"]  # shade to sunlit rim

PROFILE = {
    "name": "Riyan",
    "role": "SWE, AI INFRA AND BLOCKCHAIN",
    "cells": [("Repositories", "62"), ("Handle", "@riyqnn"), ("Role", "Coffee")],
}
PROJECTS = [("morphic", "Morphic", "morphic.cloud"), ("tawf", "Tawf Finance", "tawf.finance")]  # shots/<slug>.jpg


def font_css():
    def face(family, file, weight):
        data = base64.b64encode((OUT / "fonts" / file).read_bytes()).decode()
        return f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}"
    return face("IS", "instrument-sans-600.woff2", 600) + face("IS", "instrument-sans-700.woff2", 700)


STYLE = font_css() + f"""
.s,.m,.lbl{{font-family:IS,'Segoe UI',Helvetica,Arial,sans-serif;font-weight:600}}
.lbl{{font-size:13px;letter-spacing:.1em;fill:{DIM};text-transform:uppercase}}
.drift{{animation:drift 120s steps(150) infinite}}@keyframes drift{{to{{transform:translateX(-1200px)}}}}
.sh{{animation:sh ease-in-out infinite}}@keyframes sh{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
"""


def svg(w, h, body, label, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><style>{STYLE}{extra}</style>{body}</svg>\n')


def runs(grid, px, x0=0, y0=0):
    """grid[r][c] = color or None -> one path per color, horizontal runs merged."""
    paths = {}
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            col = row[c]
            if col is None:
                c += 1
                continue
            s = c
            while c < len(row) and row[c] == col:
                c += 1
            paths.setdefault(col, []).append(f"M{x0 + s * px} {y0 + r * px}h{(c - s) * px}v{px}h-{(c - s) * px}z")
    return "".join(f'<path fill="{k}" d="{"".join(v)}"/>' for k, v in paths.items())


def dither(ramp, v, c, r):
    """Ordered-dither a continuous ramp position v (0..len-1) to a ramp color."""
    i = math.floor(v + (BAYER[r % 4][c % 4] + .5) / 16)
    return ramp[max(0, min(len(ramp) - 1, i))]


def pixel_grid(uid, x, y, w, h):
    return (f'<defs><pattern id="{uid}" width="8" height="8" patternUnits="userSpaceOnUse">'
            f'<path d="M0 .5H8M.5 0V8" stroke="{BG}"/></pattern></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{uid})"/>')


# ── pixel sunset ─────────────────────────────────────────────────────────
def sunset(x, y, cols=150, rows=22, px=8):
    sky_rows, sun_c, sun_r, sun_rad = 17, 108, 15.5, 6
    rnd = random.Random(5)
    sky = [[None] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r < sky_rows:
                d = math.hypot((c - sun_c) * .55, r - sun_r)
                v = r / (sky_rows - 1) * (len(SKY) - 1.2) + max(0, 1.6 - d / 6)  # warmer near the sun
                col = dither(SKY, v, c, r)
                if math.hypot(c - sun_c, (r - sun_r) * 1.15) < sun_rad:
                    col = "#FFF1C1" if math.hypot(c - sun_c, r - sun_r) < sun_rad - 1.6 else SUN
            else:
                col = dither(WATER, (r - sky_rows) / (rows - sky_rows) * 3, c, r)
            sky[r][c] = col

    # sunset streak clouds, lit from below; periodic in x so the drifting layer tiles seamlessly
    streaks = [(rnd.uniform(0, cols), rnd.uniform(1.5, sky_rows - 3), rnd.uniform(6, 26), rnd.uniform(.7, 1.4))
               for _ in range(14)]
    cloud = [[None] * cols for _ in range(rows)]
    for r in range(sky_rows - 1):
        for c in range(cols):
            best = None
            for sx, sy, half, th in streaks:
                dx = (c - sx + cols / 2) % cols - cols / 2
                edge = half * (1 + .18 * math.sin(r * 2.1 + sx))  # ragged ends
                k = (dx / edge) ** 2 + ((r - sy) / th) ** 2
                if k < 1:
                    lit = .5 + (r - sy) / (2 * th) + (1 - k) * .4  # underside catches the sun
                    best = max(best or 0, lit)
            if best is not None:
                warm = r / sky_rows  # low clouds glow gold, high ones stay violet
                cloud[r][c] = dither(CLOUD, best * 1.8 + warm * 1.6, c, r)

    W, H = cols * px, rows * px
    b = [f'<svg x="{x}" y="{y}" width="{W}" height="{H}" overflow="hidden">', runs(sky, px),
         f'<g class="drift"><g id="cl">{runs(cloud, px)}</g><use href="#cl" xlink:href="#cl" x="{W}"/></g>']
    for _ in range(36):  # sun glitter on the water, under the sun only
        c = sun_c + int(rnd.gauss(0, 7))
        r = rnd.randrange(sky_rows, rows)
        b.append(f'<rect class="sh" x="{c * px}" y="{r * px}" width="{px * rnd.choice((1, 2, 3))}" height="{px}" '
                 f'fill="{rnd.choice((SUN, "#FF8552", "#FFF1C1"))}" '
                 f'style="animation-duration:{rnd.uniform(2, 5):.1f}s;animation-delay:-{rnd.uniform(0, 5):.1f}s"/>')
    b.append(pixel_grid("px", 0, 0, W, H) + "</svg>")
    return "".join(b)


# ── header card ──────────────────────────────────────────────────────────
def header():
    p = PROFILE
    W, TOP, BAND, INFO = 1200, 52, 176, 132
    H = TOP + BAND + INFO
    y0, LX = TOP + BAND, 600
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{LINE}"/>',
         f'<text class="s" x="28" y="33" font-size="17" font-weight="700" fill="{FG}">riyqnn</text>'
         f'<rect x="102" y="21" width="9" height="9" fill="{SUN}"/>'
         f'<text class="lbl" x="120" y="31" style="fill:{FG}">building</text>'
         f'<text class="m" x="{W - 28}" y="33" font-size="15" fill="{DIM}" text-anchor="end">github.com/riyqnn</text>',
         sunset(1, TOP),
         f'<path d="M0 {TOP}.5H{W}M0 {y0}.5H{W}" stroke="{LINE}"/>',
         f'<text class="s" x="36" y="{y0 + 62}" font-size="44" font-weight="700" letter-spacing="-1" fill="{FG}">{p["name"]}</text>'
         f'<text class="s" x="37" y="{y0 + 96}" font-size="15" letter-spacing="1.5" fill="{DIM}">{p["role"]}</text>']
    cw = (W - LX) / len(p["cells"])
    b.append(f'<path d="' + "".join(f"M{LX + i * cw:.0f}.5 {y0}V{H}" for i in range(len(p["cells"]))) + f'" stroke="{LINE}"/>')
    for i, (k, v) in enumerate(p["cells"]):
        cx = LX + i * cw + 26
        b.append(f'<text class="lbl" x="{cx:.0f}" y="{y0 + 54}">{k}</text>'
                 f'<text class="s" x="{cx:.0f}" y="{y0 + 88}" font-size="20" font-weight="700" fill="{FG}">{v}</text>')
    return svg(W, H, "".join(b), f'{p["name"]}: {p["role"]}')


# ── project column ───────────────────────────────────────────────────────
# Two 600px halves sit flush in the README; together they form one ruled grid.
# Guide lines run edge to edge, small squares mark the intersections, and a
# sunset-dither strip along the bottom continues across both halves.
def column(side, slug, title, domain):
    W, INSET = 600, 32
    ys = [20, 76, 431, 471]                             # horizontal guides
    H = ys[-1] + 20
    outer, inner = (INSET, W) if side == 0 else (W - INSET, 0)
    lo, hi = min(outer, inner), max(outer, inner)
    tx = lo + 28
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<path d="' + "".join(f"M0 {y}.5H{W}" for y in ys) + f'M{outer}.5 0V{H}' + (f"M.5 0V{H}" if side else "")
         + f'" stroke="{LINE}"/>',
         f'<text class="s" x="{tx}" y="{ys[0] + 37}" font-size="16" font-weight="700" fill="{SUN}">0{side + 1}</text>'
         f'<text class="s" x="{tx + 32}" y="{ys[0] + 37}" font-size="22" font-weight="700" fill="{FG}">{title}</text>'
         f'<text class="m" x="{hi - 28}" y="{ys[0] + 36}" font-size="15" fill="{DIM}" text-anchor="end">{domain}</text>']
    shot = base64.b64encode((OUT / "shots" / f"{slug}.jpg").read_bytes()).decode()
    b.append(f'<image x="{lo + 1}" y="{ys[1] + 1}" width="{hi - lo - 1}" height="{ys[2] - ys[1] - 1}" '
             f'preserveAspectRatio="xMidYMin slice" href="data:image/jpeg;base64,{shot}"/>')
    # sunset strip, hue continues from the left half into the right half
    px, rows = 8, (ys[3] - ys[2]) // 8
    strip = [[None] * (W // px) for _ in range(rows)]
    for r in range(rows):
        for c in range(W // px):
            v = (side * W + c * px) / (2 * W) * (len(SKY) - 1) - (1 - r / (rows - 1)) * 2.5
            if v > -.4:
                strip[r][c] = dither(SKY, v, c, r)
    b.append(runs(strip, px, 0, ys[2] + 1) + pixel_grid(f"px{side}", 0, ys[2] + 1, W, rows * px))
    for y in ys:
        for x in (outer, inner):
            b.append(f'<rect x="{x - 3}" y="{y - 3}" width="7" height="7" fill="{BG}" stroke="{MARK}"/>')
    return svg(W, H, "".join(b), f"{title} ({domain}) landing page")


if __name__ == "__main__":
    files = {"header.svg": header()}
    for side, project in enumerate(PROJECTS):
        files[f"card-{project[0]}.svg"] = column(side, *project)
    for name, content in files.items():
        (OUT / name).write_text(content)
        print(f"{name:22} {len(content) / 1024:6.1f} KB")
