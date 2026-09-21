#!/usr/bin/env python3
"""
Build the multi-page site.

Each nav entry is its own HTML file. Shared chrome (head, nav, drawer, footer,
lightbox) lives in this file; the body of each page is assembled from the
partials in tools/partials/.
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, 'assets', 'icons')
PARTS = os.path.join(ROOT, 'tools', 'partials')

# ---------------------------------------------------------------- sprites
names = sorted(n[:-4] for n in os.listdir(ICONS) if n.endswith('.svg'))
symbols = []
for n in names:
    svg = open(os.path.join(ICONS, n + '.svg')).read()
    body = re.sub(r'^<svg[^>]*>|</svg>$', '', svg)
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    symbols.append(f'<symbol id="i-{n}" viewBox="{vb}">{body}</symbol>')
SPRITES = ('<svg class="sprite-defs" aria-hidden="true" focusable="false" '
           'shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">'
           + ''.join(symbols) + '</svg>')

# ---------------------------------------------------------------- gallery
GALLERY = [
    ('materials-jars',          'Everything laid out before the first step.',
     'Glass jars, measuring spoons and containers of rice water and milk on a counter.'),
    ('materials-ingredients',   'Dry ingredients and molasses, ready to go.',
     'Bags of rice husk and dry ingredients next to a bowl of molasses.'),
    ('step1-rice-water',        'Step 1 — rice soaking, two parts water to one part rice.',
     'A jar of water beside a measuring cup of rice.'),
    ('step2-setup',             'Step 2 — jars and measuring cups for separating the rice water.',
     'A sealed jar, a measuring spoon and a glass measuring cup.'),
    ('step2-pouring',           'Step 2 — pouring off the collected rice water.',
     'A person pouring rice water from one jar into another.'),
    ('step3-resting',           'Step 3 — sealed and left to rest for 15 days.',
     'A sealed jar with a checked lid next to a bag of rice husk.'),
    ('step4-whey-jar',          'Step 3 — casein separated from the whey.',
     'Hands holding a jar showing the separated milk mixture.'),
    ('step4-bowl-molasses',     'Step 4 — molasses measured into the bowl.',
     'A metal bowl with a spoonful of dark molasses.'),
    ('step4-molasses-pour',     'Step 4 — molasses poured in with the whey.',
     'Molasses being poured from a spoon into a mixing bowl.'),
    ('step4-mixing-spoon',      'Step 4 — stirring it through.',
     'Hands stirring molasses in a metal bowl with a wooden spatula.'),
    ('step4-mixture',           'Step 4 — the finished liquid, left for a week.',
     'A bowl of dark brown liquid mixture.'),
    ('step5-pouring-liquid',    'Step 5 — the liquid poured over 2 kg of rice husk.',
     'Liquid poured from a blue jug into a bag of rice husk.'),
    ('step5-mixing-bag',        'Step 5 — mixing the husk through by hand.',
     'A person stirring rice husk inside a lined bag.'),
    ('step5-husk-bag',          'Step 5 — the dry husk before mixing.',
     'Dry rice husk in a black lined bag with a wooden spoon.'),
    ('step5-hands-husk',        'Step 5 — worked until evenly damp.',
     'Two hands mixing damp rice husk inside a bag.'),
    ('step6-bokashi-a',         'Step 6 — fermented bokashi after 15 days.',
     'Dark brown fermented bokashi in a large metal bowl.'),
    ('step6-bokashi-b',         'Step 6 — dark, crumbly, faintly sweet.',
     'Close view of the crumbly texture of the bokashi.'),
    ('step6-bokashi-husk',      'Step 6 — fresh husk folded into the batch.',
     'Pale fresh rice husk on top of dark bokashi.'),
    ('step6-bokashi-ready',     'Step 6 — ready to start composting with.',
     'A wooden spoon resting in a bowl of finished bokashi.'),
    ('setup-balcony',           'The composter in place, with its leachate bucket.',
     'A turquoise composter with a drainage tap on a balcony beside potted plants.'),
    ('daily-food-scraps',       'A day of kitchen waste going in.',
     'Eggshells, kale and vegetable scraps layered over rice husk.'),
    ('daily-husk-layer',        'A layer of bokashi over the fresh waste.',
     'Pale rice husk covering dark compost in the composter.'),
    ('layer-greens',            'Greens spread across the surface.',
     'A layer of chopped green leaves inside the composter.'),
    ('layer-mixed',             'Husk and greens layered together.',
     'Rice husk mixed with green kitchen scraps.'),
    ('layer-husk-tray',         'Husk and dried peel between layers.',
     'Rice husk and dried fruit peel spread in a tray.'),
    ('daily-drain-tap',         'The drainage tap, opened every day.',
     "Close-up of the composter's drainage tap above a bowl."),
    ('result-composter-full',   'The composter full, 15 days before harvest.',
     'A composter filled with alternating layers of compost and husk.'),
    ('result-white-mycelium',   'White mycelium — a healthy ferment.',
     'White fungal growth spreading across the compost surface.'),
    ('result-draining',         'Drawing off the leachate.',
     'Hands opening the composter tap to drain liquid into a cup.'),
    ('result-leachate',         'The leachate, before dilution.',
     'A white bowl holding dark brown liquid leachate.'),
    ('result-watering-plants',  'Diluted leachate used for the daily watering.',
     'Leachate poured from a bowl onto bright green leaves.'),
    ('result-finished-compost', 'The finished compost, ready for the garden.',
     'Dark finished compost poured into a storage box.'),
    ('team-photo',              'David and Andrés, six weeks later.',
     'Two people crouching beside the composter on a plant-filled balcony.'),
]

GALLERY_TILES = '\n      '.join(
    f'<button class="shot" data-full="assets/photos/{s}.jpg" data-cap="{html.escape(c, quote=True)}">'
    f'<img src="assets/thumbs/{s}.jpg" loading="lazy" decoding="async" alt="{html.escape(a, quote=True)}"></button>'
    for s, c, a in GALLERY)

# ---------------------------------------------------------------- nav
NAV = [
    ('index.html',     'Home',      'sprout',  'Home'),
    ('about.html',     'About',     'book',    'About bokashi'),
    ('materials.html', 'Materials', 'jar',     'Materials'),
    ('process.html',   'Process',   'gear',    'Process'),
    ('results.html',   'Results',   'chart',   'Results'),
    ('benefits.html',  'Benefits',  'warning', 'Benefits &amp; challenges'),
    ('gallery.html',   'Gallery',   'globe',   'Gallery'),
]

def nav_links(current):
    out = []
    for href, label, _icon, _full in NAV:
        cls = ' class="is-active"' if href == current else ''
        aria = ' aria-current="page"' if href == current else ''
        out.append(f'<li><a href="{href}"{cls}{aria}>{label}</a></li>')
    return '\n        '.join(out)

def drawer_links(current):
    out = []
    for href, _label, icon, full in NAV:
        cls = ' class="is-active"' if href == current else ''
        aria = ' aria-current="page"' if href == current else ''
        out.append(f'<li><a href="{href}"{cls}{aria}>'
                   f'<svg class="icon pixel" aria-hidden="true"><use href="#i-{icon}"></use></svg>{full}</a></li>')
    return '\n    '.join(out)

def prevnext(current):
    """Pager linking to the neighbouring pages."""
    hrefs = [h for h, *_ in NAV]
    i = hrefs.index(current)
    prev = NAV[i - 1] if i > 0 else None
    nxt = NAV[i + 1] if i < len(NAV) - 1 else None
    parts = ['<nav class="pager" aria-label="Page navigation">']
    if prev:
        parts.append(f'<a class="pager__link pager__link--prev" href="{prev[0]}">'
                     f'<span>Previous</span><b>{prev[1]}</b></a>')
    else:
        parts.append('<span></span>')
    if nxt:
        parts.append(f'<a class="pager__link pager__link--next" href="{nxt[0]}">'
                     f'<span>Next</span><b>{nxt[1]}</b></a>')
    else:
        parts.append('<span></span>')
    parts.append('</nav>')
    return '\n'.join(parts)

# ---------------------------------------------------------------- layout
LAYOUT = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="David Zuluaga Henao &amp; Andrés G. García M.">
<meta name="theme-color" content="#140e33">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/photos/setup-balcony.jpg">
<link rel="icon" href="assets/icons/leaf.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/press-start-2p-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
</head>
<body>

<div class="progress" id="progress" aria-hidden="true"></div>

{sprites}

<a class="sr-only" href="#main">Skip to content</a>

<header class="nav">
  <div class="nav__inner">
    <a class="brand" href="index.html">
      <svg class="icon pixel" aria-hidden="true"><use href="#i-leaf"></use></svg>
      <span>Everyday Ecology</span>
    </a>
    <nav aria-label="Main">
      <ul class="nav__links">
        {nav}
      </ul>
    </nav>
    <button class="nav__toggle" id="navToggle" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer">
  <ul>
    {drawer}
  </ul>
</div>

<main id="main">
{body}
{pager}
</main>

<div class="footer-ground" aria-hidden="true"></div>
<footer class="footer">
  <div class="wrap footer__inner">
    <p>
      <svg class="icon pixel" aria-hidden="true"><use href="#i-leaf"></use></svg>
      Everyday Ecology Challenge — Composting
    </p>
    <p>People + Plants + A healthier planet</p>
  </div>
</footer>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lightbox__close" id="lbClose" aria-label="Close">✕</button>
  <button class="lightbox__nav lightbox__nav--prev" id="lbPrev" aria-label="Previous photo">‹</button>
  <button class="lightbox__nav lightbox__nav--next" id="lbNext" aria-label="Next photo">›</button>
  <div class="lightbox__inner">
    <img id="lbImg" src="" alt="">
    <p class="lightbox__cap" id="lbCap"></p>
  </div>
</div>

<script src="script.js" defer></script>
</body>
</html>
'''

def part(name):
    return open(os.path.join(PARTS, name + '.html')).read()

def retarget(s):
    """Rewrite the one-pager's in-page anchors to real page links."""
    mapping = {
        '#about': 'about.html', '#materials': 'materials.html', '#process': 'process.html',
        '#results': 'results.html', '#lessons': 'benefits.html', '#gallery': 'gallery.html',
        '#routine': 'process.html#routine', '#closing': 'index.html#closing', '#home': 'index.html',
    }
    for a, b in mapping.items():
        s = s.replace(f'href="{a}"', f'href="{b}"')
    return s

# ---------------------------------------------------------------- pages
PAGES = {
    'index.html': dict(
        title='Everyday Ecology Challenge — Bokashi Composting at Home',
        description='A home composting experiment: turning everyday organic waste into nutrient-rich '
                    'bokashi compost and liquid fertiliser.',
        body=lambda: part('home') + part('cards') + part('closing'),
    ),
    'about.html': dict(
        title='What is bokashi? — Everyday Ecology Challenge',
        description='The Japanese fermentation method behind the experiment, and why it works indoors.',
        body=lambda: part('about'),
    ),
    'materials.html': dict(
        title='Materials — Everyday Ecology Challenge',
        description='Everything used to make bokashi at home: rice husk, molasses, water, milk and a '
                    'composter with drainage.',
        body=lambda: part('materials'),
    ),
    'process.html': dict(
        title='The process — Everyday Ecology Challenge',
        description='Six steps over six weeks, from soaking rice to a finished bokashi starter, plus the '
                    'daily composting routine.',
        body=lambda: part('process') + part('routine'),
    ),
    'results.html': dict(
        title='Results — Everyday Ecology Challenge',
        description='Nutrient-rich compost, liquid fertiliser, and plants that visibly benefited.',
        body=lambda: part('results'),
    ),
    'benefits.html': dict(
        title='Benefits & challenges — Everyday Ecology Challenge',
        description='What worked and what to plan for before starting bokashi composting at home.',
        body=lambda: part('lessons'),
    ),
    'gallery.html': dict(
        title='Gallery — Everyday Ecology Challenge',
        description='Every stage of the experiment, in order.',
        body=lambda: part('gallery'),
    ),
}

written = []
for href, cfg in PAGES.items():
    body = retarget(cfg['body']())
    body = body.replace('<!--GALLERY-->', GALLERY_TILES)
    page = LAYOUT.format(
        title=html.escape(cfg['title'], quote=True),
        description=html.escape(cfg['description'], quote=True),
        sprites=SPRITES,
        nav=nav_links(href),
        drawer=drawer_links(href),
        body=body,
        pager=prevnext(href),
    )
    open(os.path.join(ROOT, href), 'w').write(page)
    written.append((href, len(page) // 1024))

print(f'{len(names)} sprites, {len(GALLERY)} gallery photos')
for h, kb in written:
    print(f'  {h:<16} {kb:>3} KB')
