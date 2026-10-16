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
    "es": ("Esplendor Resort en Río Rico · Español", "Resort de 179 habitaciones en 22.74 acres en Río Rico, Arizona, en venta tal como está o con un socio de capital.", None),
    "404": ("Page not found · Esplendor", "This page could not be found.", None),
}
# optional per-page overrides: src/<name>/nav.html replaces the desktop and mobile nav,
# src/<name>/footer.html replaces the footer, src/<name>/head.html adds to <head>,
# src/<name>/lang.txt sets the document language.
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
h0 = next(i for i, l in enumerate(idx) if l.startswith('<aside class="ribbon'))
h1 = next(i for i, l in enumerate(idx) if l.startswith("</header>"))
f0 = next(i for i, l in enumerate(idx) if l.startswith("<footer>"))
f1 = next(i for i, l in enumerate(idx) if l.startswith("</footer>"))
header = "\n".join(idx[h0:h1 + 1]).replace('href="#top"', 'href="index.html"')
header = re.sub(r'href="#([\w-]+)"', r'href="index.html#\1"', header)
footer = "\n".join(idx[f0:f1 + 1])
footer = re.sub(r'href="#([\w-]+)"', r'href="index.html#\1"', footer)
# footer scripts on the index (share, flyer) are not on sub-pages; drop share buttons that need them
footer = re.sub(r'<div class="share"[\s\S]*?</div>\s*', "", footer)
footer = re.sub(r"<a class=\"to-top\"[\s\S]*?</a>\s*", "", footer)

for name, (title, desc, current) in PAGES.items():
    body = read(f"src/{name}/body.html")
    if not body:
        continue
    h = header
    nav = read(f"src/{name}/nav.html")
    if nav:
        d, m = nav.split("<!-- mobile -->")
        h = re.sub(r'<nav class="links"[\s\S]*?</nav>', d.strip(), h, count=1)
        h = re.sub(r'(<nav class="m-nav"[^>]*>)[\s\S]*?(</nav>)', lambda mm: mm.group(1) + m.strip() + mm.group(2), h, count=1)
        for a, b in (("Request package", "Solicitar paquete"), ("<span class=\"sm\">Inquire</span>", "<span class=\"sm\">Contacto</span>"), ('href="index.html#inquire"', 'href="#contacto"'), ("Open menu", "Abrir menú"), ('href="es.html" lang="es" hreflang="es" title="Ver en español">ES</a>', 'href="index.html" lang="en" hreflang="en" title="View in English">EN</a>')):
            h = h.replace(a, b)
    if current:
        h = h.replace(f'<a href="land.html">{current}</a>', f'<a href="land.html" aria-current="page">{current}</a>')
    js = read(f"src/{name}/page.js")
    foot = read(f"src/{name}/footer.html") or footer
    lang = (read(f"src/{name}/lang.txt") or "en").strip()
    extra_head = read(f"src/{name}/head.html")
    if "menu-btn" not in js:
        js = MENU_JS + js
    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="{'index, follow' if name in ('land','es') else 'noindex'}">
<title>{title}</title>
<meta name="description" content="{desc}">
{extra_head}<link rel="icon" href="img/brand/favicon.svg" type="image/svg+xml">
{fonts}
{style}
[hidden]{{display:none!important}}
{read(f"src/{name}/page.css")}
</style>
</head>
<body>
{h}

{body}
{foot}
<script>
{js}</script>
</body>
</html>
"""
    open(os.path.join(ROOT, f"{name}.html"), "w", encoding="utf-8").write(doc)
    print("built", name + ".html", len(doc))
