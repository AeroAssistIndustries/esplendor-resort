#!/usr/bin/env python3
"""Wrap index.html (artifact body) into a full HTML document and copy assets into _site/ for GitHub Pages."""
import os, re, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
BASE = "https://aeroassistindustries.github.io/esplendor-resort/"
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
body = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="canonical" href="{BASE}">
<link rel="alternate" hreflang="en" href="{BASE}">
<link rel="alternate" hreflang="es" href="{BASE}es.html">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}">
<meta property="og:site_name" content="Esplendor Resort at Río Rico">
<meta property="og:title" content="Esplendor Resort at Río Rico — 179-room resort for sale">
<meta property="og:description" content="179-room hilltop resort on 22.74 acres in Río Rico, Arizona. Fully planned and fire-department approved. Offered as is or with a capital partner.">
<meta property="og:image" content="{BASE}img/brand/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="es_MX">
<link rel="icon" type="image/svg+xml" href="img/brand/favicon.svg">
<link rel="icon" type="image/png" href="img/brand/favicon.png">
<link rel="apple-touch-icon" href="img/brand/favicon.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Esplendor Resort at Río Rico — 179-room resort for sale">
<meta name="twitter:description" content="22.74 acres above the Santa Cruz Valley, fully planned and fire-department approved. $9–11M as is, or finish it with the owner.">
<meta name="twitter:image" content="{BASE}img/brand/og.jpg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"RealEstateListing","name":"Esplendor Resort at Río Rico","url":"{BASE}","image":"{BASE}img/brand/og.jpg","datePosted":"2026-10-16","inLanguage":["en","es"],"description":"179-room hilltop resort on 22.74 acres in Río Rico, Arizona, closed since 2015 and fully planned for renovation. Offered as is for $9–11M, or for completion with a capital partner.","about":{{"@type":"Place","name":"Esplendor Resort at Río Rico","address":{{"@type":"PostalAddress","streetAddress":"1069 Camino Caralampi","addressLocality":"Rio Rico","addressRegion":"AZ","postalCode":"85648","addressCountry":"US"}},"geo":{{"@type":"GeoCoordinates","latitude":31.472,"longitude":-110.9805}}}},"offers":{{"@type":"Offer","priceCurrency":"USD","priceSpecification":{{"@type":"PriceSpecification","minPrice":9000000,"maxPrice":11000000,"priceCurrency":"USD"}},"availability":"https://schema.org/InStock","seller":{{"@type":"Organization","name":"MC Business Group LLC","email":"sales@esplendorproject.com"}}}}}}
</script>
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px/1.4 system-ui,-apple-system,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
"""
# move the page's own <title>/<meta>/<link>/<style> block into <head>: everything before the first <aside class="ribbon"
cut = body.find('<aside class="ribbon')
if cut < 0: sys.exit("ribbon marker not found")
doc = head + body[:cut] + "</head>\n<body>\n" + body[cut:] + "\n</body>\n</html>\n"
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(doc)
for name in ("img", "walkthrough.html", "model-data.js", "land.html", "privacy.html", "terms.html", "es.html", "404.html", "robots.txt", "sitemap.xml", "CNAME"):
    src = os.path.join(ROOT, name)
    if os.path.isdir(src): shutil.copytree(src, os.path.join(OUT, name))
    elif os.path.isfile(src): shutil.copy2(src, os.path.join(OUT, name))
open(os.path.join(OUT, ".nojekyll"), "w").close()
print("built", OUT)
