#!/usr/bin/env python3
"""Apply the Southwest layer and the Harbor-parity sections to index.html.

Idempotent: every insertion is wrapped in SW markers and replaced on re-run, so the
source files in src/southwest/ stay the single place to edit.
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SW = os.path.join(ROOT, "src", "southwest")
P = os.path.join(ROOT, "index.html")
s = open(P, encoding="utf-8").read()
rd = lambda n: open(os.path.join(SW, n), encoding="utf-8").read()

def block(tag, body, html=True):
    return (f"<!-- SW:{tag} -->\n{body}\n<!-- /SW:{tag} -->\n") if html else (f"/* SW:{tag} */\n{body}\n/* /SW:{tag} */\n")

def strip_all(text):
    text = re.sub(r"<!-- SW:([\w-]+) -->.*?<!-- /SW:\1 -->\n?", "", text, flags=re.S)
    text = re.sub(r"/\* SW:([\w-]+) \*/.*?/\* /SW:\1 \*/\n?", "", text, flags=re.S)
    return text

def once(text, needle, insert, before=True):
    n = text.count(needle)
    if n != 1: sys.exit(f"anchor found {n}x: {needle[:70]!r}")
    return text.replace(needle, (insert + needle) if before else (needle + insert))

s = strip_all(s)
# undo earlier one-off attribute edits so re-runs start clean
s = s.replace('<section id="process" aria-labelledby="pr-title">', '<section id="process" class="band" aria-labelledby="pr-title">')
s = s.replace('<section id="sources" class="sources band" aria-labelledby="src-title">', '<section id="sources" class="sources" aria-labelledby="src-title">')

# 1. stylesheet
css = rd("art.css") + rd("theme.css")
idx = s.index("</style>")
s = s[:idx] + block("css", css, html=False) + s[idx:]

# 2. tile bands and ridges
tile = '<div class="tile-band" aria-hidden="true"></div>'
ridge = rd("ridge.svg.html")
s = once(s, '  <div class="deed">', block("tile-hero", "  " + tile))
s = once(s, '<footer>', block("tile-foot", tile))
s = once(s, '  <section class="reveal" id="reveal"', block("ridge-reveal", "  " + ridge.replace('class="ridge"', 'class="ridge from-paper"')))
s = once(s, '  <section id="vision" class="vision">', block("ridge-vision", "  " + ridge.replace('class="ridge"', 'class="ridge from-paper"')))
s = once(s, '  <section id="inquire" class="night">', block("ridge-inquire", "  " + ridge.replace('class="ridge"', 'class="ridge from-paper"')))

# 3. new sections
s = once(s, '  <section id="returns">', block("terms", rd("terms.html")))
s = once(s, '  <section id="process" class="band"', block("risks", rd("risks.html")))
# keep bands alternating: news(band) risks(band) parties(plain) process(plain) sources(band)
s = s.replace('<section id="process" class="band" aria-labelledby="pr-title">', '<section id="process" aria-labelledby="pr-title">')
s = s.replace('<section id="sources" class="sources" aria-labelledby="src-title">', '<section id="sources" class="sources band" aria-labelledby="src-title">')

# 4. FAQ: two new answers + glossary beside it
faq_open = '      <div class="faq" id="faq">'
s = once(s, faq_open, '<!-- SW:qa-open -->\n      <div class="qa-grid">\n<!-- /SW:qa-open -->\n')
new_q = ('        <details><summary>Will the seller finance the purchase?</summary><p>Yes, for qualified buyers. The owner will carry part of the price, or up to all of it, at prevailing hard-money rates. Down payment, rate and term are negotiated per buyer and subject to credit approval. Try a structure in <a href="#terms">Run the numbers</a>.</p></details>\n'
         '        <details><summary>How does the 50/50 partnership work?</summary><p>An investor commits $15 million, which funds the $11&ndash;13 million completion plus reserves. The owner contributes the property and five years of pre-development, and the two end up 50/50 owners of the finished resort. Governance, distributions and exit terms would be set in definitive documents, offered only to eligible investors.</p></details>\n')
s = once(s, '        <details><summary>Are brokers welcome?</summary>', block("faq-new", new_q.rstrip("\n")))
gloss = '''      <div>
        <h3 style="margin-bottom:14px">Hotel and deal terms</h3>
        <dl class="gloss">
          <div><dt>Key</dt><dd>One rentable guest room or suite.</dd></div>
          <div><dt>ADR</dt><dd>Average daily rate: room revenue divided by rooms sold.</dd></div>
          <div><dt>Occupancy</dt><dd>Share of available rooms sold.</dd></div>
          <div><dt>RevPAR</dt><dd>Revenue per available room: ADR × occupancy.</dd></div>
          <div><dt>NOI</dt><dd>Net operating income: revenue minus operating costs, before debt and taxes.</dd></div>
          <div><dt>Cap rate</dt><dd>NOI divided by value; at 8.5%, $1 of NOI supports about $11.76 of value.</dd></div>
          <div><dt>Seller carry</dt><dd>Part of the price paid over time to the seller instead of a bank.</dd></div>
          <div><dt>Hard money</dt><dd>Short-term, asset-backed lending priced above bank rates.</dd></div>
          <div><dt>Balloon</dt><dd>The unpaid loan balance due in one payment at the end of the term.</dd></div>
          <div><dt>FF&amp;E</dt><dd>Furniture, fixtures and equipment.</dd></div>
          <div><dt>Phase I ESA</dt><dd>Environmental site assessment of a property&rsquo;s history and conditions.</dd></div>
          <div><dt>B-2</dt><dd>Santa Cruz County General Business zoning; hotels are permitted by right.</dd></div>
        </dl>
      </div>
      </div>'''
# close the qa-grid right after the faq div closes (first </div> after the brokers question)
m = re.search(r'(<details><summary>Are brokers welcome\?</summary>.*?</details>\n      </div>\n)', s, flags=re.S)
if not m: sys.exit("faq end not found")
s = s[:m.end()] + block("gloss", gloss) + s[m.end():]

# 5. navigation
old_nav = '''      <a href="#today">Today</a>
      <a href="#vision">Vision</a>
      <a href="#site">Site</a>
      <a href="walkthrough.html">3D tour</a>
      <a href="land.html">Land</a>
      <a href="#market">Market</a>
      <a href="#news">News</a>'''
new_nav = '''      <a href="#vision">Vision</a>
      <a href="walkthrough.html">3D tour</a>
      <a href="land.html">Land</a>
      <a href="#market">Market</a>
      <a href="#risks">Risks</a>
      <a href="#news">News</a>'''
if old_nav in s:
    s = s.replace(old_nav, new_nav)
if '<a href="#terms">Terms</a>' not in s:
    s = once(s, '      <a href="#returns">Returns</a>\n', '      <a href="#terms">Terms</a>\n')
mob_old = '<a href="#paths">Two paths</a><a href="#returns">Returns</a>'
if mob_old in s:
    s = s.replace(mob_old, '<a href="#paths">Two paths</a><a href="#terms">Run your terms</a><a href="#returns">Returns</a>')
mob_old2 = '<a href="#news">News</a><a href="es.html" lang="es">Español</a>'
if mob_old2 in s:
    s = s.replace(mob_old2, '<a href="#news">News</a><a href="#risks">Risks</a><a href="#parties">Who is involved</a><a href="es.html" lang="es">Español</a>')

# 6. script
s = s.rstrip("\n") + "\n" + block("js", "<script>\n" + rd("terms.js") + "</script>")

open(P, "w", encoding="utf-8").write(s)
print("southwest applied ·", len(s), "bytes")
