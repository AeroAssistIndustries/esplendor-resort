#!/usr/bin/env python3
"""Build the standalone sub-pages (land, privacy, terms) from src/<name>/ using the
main site's stylesheet, header and footer from index.html, so every page shares one look.

src/<name>/body.html  page content (starting with <main>)
src/<name>/page.css   optional page-specific styles
src/<name>/page.js    optional page-specific script
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
    "land": ("Land Potential · Esplendor", "Open acreage at Esplendor Resort, Río Rico, Arizona: mapped areas, add-on ideas, B-2 zoning and regional benchmarks.", "Land"),
    "privacy": ("Privacy Policy · Esplendor", "How the Esplendor Resort property website handles information.", None),
    "terms": ("Terms of Use · Esplendor", "Terms of use for the Esplendor Resort property website.", None),
}
MENU_JS = """(function(){var b=document.getElementById('menu-btn'),n=document.getElementById('m-nav');if(!b||!n)return;
function set(o){b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Close menu':'Open menu');n.hidden=!o}
b.addEventListener('click',function(){set(n.hidden)});n.addEventListener('click',function(e){if(e.target.tagName==='A')set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!n.hidden){set(false);b.focus()}})})();
"""

def read(p, default=""):
    p = os.path.join(ROOT, p)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else default

idx = read("index.html").split("\n")
s0 = next(i for i, l in enumerate(idx) if l.startswith("<style>"))
s1 = next(i for i, l in enumerate(idx) if l.startswith("</style>"))
style = "\n".join(idx[s0:s1])
fonts = "\n".join(l for l in idx[:s0] if "fonts.g" in l)
h0 = next(i for i, l in enumerate(idx) if l.startswith('<div class="ribbon">'))
h1 = next(i for i, l in enumerate(idx) if l.startswith("</header>"))
f0 = next(i for i, l in enumerate(idx) if l.startswith("<footer>"))
f1 = next(i for i, l in enumerate(idx) if l.startswith("</footer>"))
header = "\n".join(idx[h0:h1 + 1]).replace('href="#top"', 'href="index.html"')
header = re.sub(r'href="#([\w-]+)"', r'href="index.html#\1"', header)
footer = "\n".join(idx[f0:f1 + 1])
footer = re.sub(r'href="#([\w-]+)"', r'href="index.html#\1"', footer)
# footer scripts on the index (share, flyer) are not on sub-pages; drop share buttons that need them
footer = re.sub(r'<div class="share"[\s\S]*?</div>\s*', "", footer)

for name, (title, desc, current) in PAGES.items():
    body = read(f"src/{name}/body.html")
    if not body:
        continue
    h = header
    if current:
        h = h.replace(f'<a href="land.html">{current}</a>', f'<a href="land.html" aria-current="page">{current}</a>')
    js = read(f"src/{name}/page.js")
    if "menu-btn" not in js:
        js = MENU_JS + js
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="img/brand/favicon.svg" type="image/svg+xml">
{fonts}
{style}
[hidden]{{display:none!important}}
{read(f"src/{name}/page.css")}
</style>
</head>
<body>
{h}

{body}
{footer}
<script>
{js}</script>
</body>
</html>
"""
    open(os.path.join(ROOT, f"{name}.html"), "w", encoding="utf-8").write(doc)
    print("built", name + ".html", len(doc))
