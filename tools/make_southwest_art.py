#!/usr/bin/env python3
"""Generate the Southwest decorative art used by the site theme.

Writes src/southwest/ridge.svg.html (inline ridge markup, three layered silhouettes
loosely after the Santa Rita and Tumacácori skyline seen from Río Rico) and
src/southwest/art.css (data-URI art: Talavera tile band, topographic contours,
sun mark, stucco grain). Deterministic: same output every run.
"""
import math, os, random, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "southwest")
os.makedirs(OUT, exist_ok=True)

def uri(svg):
    return "url(\"data:image/svg+xml," + urllib.parse.quote(" ".join(svg.split()), safe=" =:/'(),.-;") + "\")"

# ---------- ridges ----------
def ridge(seed, base, amp, peaks, rough, width=1440, height=150, step=12):
    rnd = random.Random(seed)
    pts = []
    for x in range(0, width + step, step):
        y = base
        for (px, ph, pw) in peaks:                        # broad summits (gaussian)
            y -= ph * math.exp(-((x - px) / pw) ** 2)
        y -= amp * (0.5 + 0.5 * math.sin(x / 210 + seed))  # long swell
        y += rough * (rnd.random() - 0.5)                  # rock texture
        pts.append((x, max(4, y)))
    d = "M0 %d " % height + " ".join("L%d %.1f" % p for p in pts) + " L%d %d Z" % (width, height)
    return d

far  = ridge(3, 92, 10, [(330, 66, 150), (520, 40, 90), (1080, 52, 170), (1290, 30, 70)], 9)
mid  = ridge(7, 116, 8, [(160, 30, 110), (760, 42, 140), (980, 26, 80), (1380, 22, 90)], 6)
near = ridge(11, 136, 4, [(420, 16, 160), (1150, 20, 200)], 3)
ridge_svg = (
  '<div class="ridge" aria-hidden="true"><svg viewBox="0 0 1440 150" preserveAspectRatio="none" focusable="false">'
  f'<path class="r1" d="{far}"/><path class="r2" d="{mid}"/><path class="r3" d="{near}"/></svg></div>'
)
open(os.path.join(OUT, "ridge.svg.html"), "w").write(ridge_svg)

# ---------- Talavera tile (one 28px tile, repeats along a band) ----------
CREAM, COBALT, TURQ, TERRA, GOLD = "#F6EEDF", "#25467A", "#2B8A86", "#B0492A", "#D59A38"
tile = f"""<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'>
<rect width='28' height='28' fill='{CREAM}'/>
<g fill='{TURQ}'><path d='M0 0h6.5A6.5 6.5 0 0 1 0 6.5z'/><path d='M28 0v6.5A6.5 6.5 0 0 1 21.5 0z'/>
<path d='M0 28v-6.5A6.5 6.5 0 0 1 6.5 28z'/><path d='M28 28h-6.5A6.5 6.5 0 0 1 28 21.5z'/></g>
<g fill='{COBALT}'><circle cx='14' cy='9.2' r='3.9'/><circle cx='18.8' cy='14' r='3.9'/><circle cx='14' cy='18.8' r='3.9'/><circle cx='9.2' cy='14' r='3.9'/></g>
<circle cx='14' cy='14' r='3.1' fill='{CREAM}'/><circle cx='14' cy='14' r='1.9' fill='{TERRA}'/>
<g fill='{GOLD}'><path d='M14 0l1.6 1.6L14 3.2l-1.6-1.6z'/><path d='M14 24.8l1.6 1.6L14 28l-1.6-1.6z'/>
<path d='M0 14l1.6-1.6L3.2 14l-1.6 1.6z'/><path d='M24.8 14l1.6-1.6L28 14l-1.6 1.6z'/></g>
<rect x='.5' y='.5' width='27' height='27' fill='none' stroke='{COBALT}' stroke-opacity='.18'/>
</svg>"""

# ---------- topographic contours (for dusk chapters) ----------
def blob(cx, cy, r, k, seed):
    rnd = random.Random(seed)
    n = 9
    rs = [r * (1 + k * (rnd.random() - 0.5)) for _ in range(n)]
    pts = [(cx + rs[i] * math.cos(2 * math.pi * i / n), cy + 0.72 * rs[i] * math.sin(2 * math.pi * i / n)) for i in range(n)]
    d = "M%.1f %.1f " % pts[0]
    for i in range(n):  # Catmull-Rom to bezier, closed
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += "C%.1f %.1f %.1f %.1f %.1f %.1f " % (c1 + c2 + p2)
    return d + "Z"
paths = []
for (cx, cy, rmax, seed) in [(210, 210, 165, 1), (640, 380, 150, 2), (700, 130, 105, 3)]:
    for j, f in enumerate([1, .8, .62, .45, .3, .17]):
        paths.append(blob(cx, cy, rmax * f, 0.24, seed * 10 + j))
topo = ("<svg xmlns='http://www.w3.org/2000/svg' width='900' height='560' viewBox='0 0 900 560' fill='none' "
        "stroke='#E2B66B' stroke-opacity='.075' stroke-width='1'>" + "".join(f"<path d='{p}'/>" for p in paths) + "</svg>")

# ---------- sun mark (used as a mask, so it takes any color) ----------
sun = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 18'><path d='M9 17.5a8 8 0 0 1 16 0z' fill='#000'/>
<g stroke='#000' stroke-width='1.7' stroke-linecap='round'><path d='M17 1.2v4.2M7.2 4.6l2.4 3.1M26.8 4.6l-2.4 3.1M1.6 11.2l3.8 1.2M32.4 11.2l-3.8 1.2'/></g></svg>"""

# ---------- stucco grain ----------
grain = """<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'>
<feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/>
<feColorMatrix values='0 0 0 0 .42  0 0 0 0 .3  0 0 0 0 .18  0 0 0 .085 0'/></filter>
<rect width='100%' height='100%' filter='url(#n)'/></svg>"""

css = f""":root{{--sw-tile:{uri(tile)};--sw-topo:{uri(topo)};--sw-sun:{uri(sun)};--sw-grain:{uri(grain)}}}
"""
open(os.path.join(OUT, "art.css"), "w").write(css)
print("ridge", len(ridge_svg), "bytes · art.css", len(css), "bytes")
