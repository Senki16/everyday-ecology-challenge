#!/usr/bin/env python3
"""Generate crisp pixel-art sprites as SVG (rect runs) + a PNG preview sheet."""
from PIL import Image, ImageDraw
import os, json

OUT = '/home/claude/work/site/assets/icons'
os.makedirs(OUT, exist_ok=True)

# ---------- palette ----------
P = dict(
    leafD='#1d6b34', leaf='#4fd67a', leafL='#9cf0b4', leafX='#2f9b52',
    soilD='#5a2f14', soil='#8a4a1f', soilL='#b06a30',
    woodD='#6b3a14', wood='#a4652a', woodL='#c98a48',
    blueD='#17476e', blue='#3d8fd6', blueL='#8fd0f7',
    skyD='#2b1f6b', sky='#4a3bb0',
    redD='#8f1f2e', red='#e0394f', redL='#ff7a8a',
    white='#ffffff', cream='#f6efdc', gray='#8b86a8', grayD='#4a4466',
    yellowD='#a97f16', yellow='#f5c445', yellowL='#ffe38a',
    purpD='#4a2f8f', purp='#8a6ae0', purpL='#c0aaf7',
    pinkD='#a23c6c', pink='#ef6fa5', pinkL='#ffa9c9',
    inkD='#161029', ink='#2a2050',
    brownD='#3d2410', brown='#6b4220', brownL='#9a6634',
    tealD='#136b63', teal='#2fc0ae',
)

SPRITES = {}

def sprite(name, size=16):
    def deco(fn):
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        fn(ImageDraw.Draw(img), img)
        SPRITES[name] = img
        return fn
    return deco

def px(d, x, y, c):
    d.point((x, y), fill=c)

def rect(d, x0, y0, x1, y1, c):
    d.rectangle([x0, y0, x1, y1], fill=c)

def outline_ellipse(d, box, fill, out):
    d.ellipse(box, fill=out)
    d.ellipse([box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1], fill=fill)



def from_grid(grid, pal):
    """Build a sprite from an ASCII grid; '.' = transparent."""
    rows = [r for r in grid.strip('\n').split('\n')]
    h = len(rows); w = max(len(r) for r in rows)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.':
                d.point((x, y), fill=pal[ch])
    return img


LEAF_GRID = """
.......DDD......
.....DDGGGDD....
....DGGGGGGGD...
...DGGGGGGLGGD..
..DGGGGGGLGGGD..
..DGGGGGGLGGGD..
.DGGGGGGLGGGGGD.
.DGGGGGLGGGGGGD.
.DGGGGLGGGGGGGD.
.DGGGLGGGGGGGD..
..DGLLGGGGGGD...
..DDLGGGGGGD....
...DLGGGGDD.....
...DLLGDD.......
....DLDD........
.....DD.........
"""

RECYCLE_GRID = """
.......DD.......
......DGGD......
.....DGGGGD.....
....DGGGGGGD....
...DDDGGGDDD....
.....DGGGD......
.....DGGGD......
DD...DGGGD...DD.
DGD..DGGGD..DGD.
DGGD.DDDDD.DGGD.
DGGGD.....DGGGD.
DGGGGDDDDDGGGGD.
DGGGGGGGGGGGGGD.
DDDGGGGGGGGGDDD.
..DDGGGGGGGDD...
....DDDDDDD.....
"""

# ================= sprites =================

@sprite('sprout')
def _(d, im):
    rect(d, 7, 7, 8, 13, P['leafD'])          # stem
    # left leaf
    d.ellipse([1, 4, 8, 9], fill=P['leafD'])
    d.ellipse([2, 5, 7, 8], fill=P['leaf'])
    # right leaf
    d.ellipse([7, 3, 14, 8], fill=P['leafD'])
    d.ellipse([8, 4, 13, 7], fill=P['leaf'])
    px(d, 11, 5, P['leafL']); px(d, 4, 6, P['leafL'])
    # soil mound
    d.ellipse([1, 11, 14, 17], fill=P['soilD'])
    d.ellipse([2, 12, 13, 16], fill=P['soil'])
    rect(d, 0, 15, 15, 15, P['soilD'])
    px(d, 4, 13, P['soilL']); px(d, 10, 13, P['soilL'])


@sprite('bin')
def _(d, im):
    # body
    rect(d, 2, 5, 13, 14, P['woodD'])
    rect(d, 3, 6, 12, 13, P['wood'])
    for y in (8, 11):
        rect(d, 3, y, 12, y, P['woodD'])
    # lid
    rect(d, 1, 3, 14, 5, P['woodD'])
    rect(d, 2, 4, 13, 4, P['woodL'])
    px(d, 7, 2, P['woodD']); px(d, 8, 2, P['woodD'])
    # green recycle mark
    rect(d, 6, 9, 9, 10, P['leaf'])
    px(d, 5, 10, P['leaf']); px(d, 10, 10, P['leaf'])
    px(d, 7, 11, P['leafD']); px(d, 8, 11, P['leafD'])
    rect(d, 0, 15, 15, 15, P['woodD'])


@sprite('mushroom')
def _(d, im):
    d.ellipse([1, 2, 14, 11], fill=P['redD'])
    d.ellipse([2, 3, 13, 10], fill=P['red'])
    rect(d, 1, 8, 14, 11, (0, 0, 0, 0))
    d.ellipse([1, 2, 14, 10], fill=P['redD'])
    d.ellipse([2, 3, 13, 9], fill=P['red'])
    rect(d, 1, 9, 14, 11, (0, 0, 0, 0))
    # dots
    for (x, y) in [(4, 5), (9, 4), (11, 6), (6, 7)]:
        rect(d, x, y, x + 1, y + 1, P['white'])
    # stem
    rect(d, 6, 9, 9, 14, P['brownD'])
    rect(d, 7, 9, 8, 13, P['cream'])
    rect(d, 5, 14, 10, 14, P['brownD'])


@sprite('can')
def _(d, im):
    rect(d, 3, 6, 11, 14, P['blueD'])
    rect(d, 4, 7, 10, 13, P['blue'])
    px(d, 5, 8, P['blueL']); px(d, 5, 9, P['blueL'])
    # spout
    d.polygon([(11, 7), (15, 4), (15, 6), (12, 9), (11, 9)], fill=P['blueD'])
    d.polygon([(12, 8), (14, 6), (14, 5)], fill=P['blue'])
    # handle
    rect(d, 4, 4, 9, 5, P['blueD'])
    px(d, 3, 5, P['blueD']); px(d, 10, 5, P['blueD'])
    # flower detail
    rect(d, 6, 10, 8, 11, P['yellow'])
    rect(d, 3, 15, 11, 15, P['blueD'])


@sprite('jar')
def _(d, im):
    rect(d, 4, 1, 11, 3, P['grayD'])
    rect(d, 5, 2, 10, 2, P['gray'])
    rect(d, 3, 3, 12, 15, P['brownD'])
    rect(d, 4, 4, 11, 14, P['cream'])
    rect(d, 4, 6, 11, 14, P['brown'])
    for (x, y) in [(5, 8), (8, 7), (9, 11), (6, 12)]:
        px(d, x, y, P['brownL'])
    px(d, 4, 5, P['white'])


@sprite('globe')
def _(d, im):
    outline_ellipse(d, [0, 0, 15, 15], P['blue'], P['blueD'])
    d.polygon([(3, 4), (7, 3), (8, 6), (5, 8), (3, 7)], fill=P['leaf'])
    d.polygon([(9, 8), (12, 7), (12, 11), (9, 12)], fill=P['leaf'])
    d.polygon([(4, 11), (7, 10), (7, 13), (5, 13)], fill=P['leaf'])
    px(d, 4, 3, P['blueL']); px(d, 5, 2, P['blueL'])


@sprite('sun')
def _(d, im):
    outline_ellipse(d, [3, 3, 12, 12], P['yellow'], P['yellowD'])
    px(d, 6, 5, P['yellowL']); px(d, 5, 6, P['yellowL'])
    for (x, y, w, h) in [(7, 0, 2, 2), (7, 14, 2, 2), (0, 7, 2, 2), (14, 7, 2, 2)]:
        rect(d, x, y, x + w - 1, y + h - 1, P['yellow'])
    for (x, y) in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        px(d, x, y, P['yellow'])


@sprite('cloud')
def _(d, im):
    d.ellipse([0, 5, 8, 13], fill=P['purpD'])
    d.ellipse([4, 2, 13, 12], fill=P['purpD'])
    d.ellipse([8, 6, 15, 13], fill=P['purpD'])
    d.ellipse([1, 6, 7, 12], fill=P['pink'])
    d.ellipse([5, 3, 12, 11], fill=P['pink'])
    d.ellipse([9, 7, 14, 12], fill=P['pink'])
    d.ellipse([6, 4, 10, 7], fill=P['pinkL'])
    rect(d, 0, 13, 15, 15, (0, 0, 0, 0))


@sprite('book')
def _(d, im):
    rect(d, 0, 3, 15, 13, P['purpD'])
    rect(d, 1, 4, 7, 12, P['cream'])
    rect(d, 8, 4, 14, 12, P['cream'])
    rect(d, 7, 3, 8, 13, P['purpD'])
    for y in (6, 8, 10):
        rect(d, 2, y, 6, y, P['purp'])
        rect(d, 9, y, 13, y, P['purp'])


@sprite('gear')
def _(d, im):
    outline_ellipse(d, [2, 2, 13, 13], P['purp'], P['purpD'])
    for (x, y) in [(6, 0), (6, 13), (0, 6), (13, 6)]:
        rect(d, x, y, x + 3, y + 2, P['purpD'])
    for (x, y) in [(2, 2), (12, 2), (2, 12), (12, 12)]:
        rect(d, x, y, x + 1, y + 1, P['purpD'])
    outline_ellipse(d, [5, 5, 10, 10], P['inkD'], P['purpD'])
    px(d, 5, 4, P['purpL'])


@sprite('chart')
def _(d, im):
    rect(d, 1, 9, 4, 15, P['blueD']); rect(d, 2, 10, 3, 14, P['blueL'])
    rect(d, 6, 5, 9, 15, P['blueD']); rect(d, 7, 6, 8, 14, P['blue'])
    rect(d, 11, 1, 14, 15, P['blueD']); rect(d, 12, 2, 13, 14, P['blueL'])
    rect(d, 0, 15, 15, 15, P['inkD'])


@sprite('warning')
def _(d, im):
    d.polygon([(7, 0), (8, 0), (15, 14), (15, 15), (0, 15), (0, 14)], fill=P['redD'])
    d.polygon([(7, 3), (8, 3), (13, 13), (2, 13)], fill=P['red'])
    rect(d, 7, 6, 8, 10, P['white'])
    rect(d, 7, 11, 8, 12, P['white'])


@sprite('mail')
def _(d, im):
    rect(d, 0, 3, 15, 12, P['tealD'])
    rect(d, 1, 4, 14, 11, P['teal'])
    for i in range(7):
        px(d, 1 + i, 4 + i, P['tealD']); px(d, 14 - i, 4 + i, P['tealD'])
    px(d, 8, 10, P['tealD'])


@sprite('download')
def _(d, im):
    rect(d, 6, 1, 9, 7, P['leafD'])
    rect(d, 7, 2, 8, 7, P['leafL'])
    d.polygon([(3, 7), (12, 7), (8, 12), (7, 12)], fill=P['leafD'])
    d.polygon([(5, 8), (10, 8), (8, 10), (7, 10)], fill=P['leaf'])
    rect(d, 1, 13, 14, 14, P['leafD'])


@sprite('drop')
def _(d, im):
    d.polygon([(7, 0), (8, 0), (13, 9), (2, 9)], fill=P['blueD'])
    d.ellipse([2, 5, 13, 15], fill=P['blueD'])
    d.polygon([(7, 3), (8, 3), (11, 9), (4, 9)], fill=P['blue'])
    d.ellipse([3, 6, 12, 14], fill=P['blue'])
    px(d, 5, 10, P['blueL']); px(d, 5, 11, P['blueL']); px(d, 6, 12, P['blueL'])


@sprite('clock')
def _(d, im):
    outline_ellipse(d, [0, 0, 15, 15], P['cream'], P['inkD'])
    rect(d, 7, 4, 8, 8, P['inkD'])
    rect(d, 8, 8, 11, 9, P['inkD'])
    px(d, 4, 4, P['gray'])


@sprite('sign')
def _(d, im):
    rect(d, 1, 2, 14, 10, P['woodD'])
    rect(d, 2, 3, 13, 9, P['wood'])
    for y in (5, 7):
        rect(d, 4, y, 11, y, P['woodD'])
    rect(d, 7, 10, 8, 15, P['woodD'])
    rect(d, 7, 10, 7, 15, P['woodL'])


@sprite('star')
def _(d, im):
    d.polygon([(8, 1), (10, 6), (15, 6), (11, 9), (13, 14), (8, 11), (3, 14), (5, 9), (1, 6), (6, 6)],
              fill=P['yellow'])
    px(d, 7, 5, P['yellowL']); px(d, 8, 5, P['yellowL'])


SPRITES['leaf'] = from_grid(LEAF_GRID, {'D': P['leafD'], 'G': P['leaf'], 'L': P['leafL']})
def _make_recycle():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tri = [(8, 2), (14, 13), (2, 13)]
    d.line(tri + [tri[0]], fill=P['leafD'], width=3, joint=None)
    d.line(tri + [tri[0]], fill=P['leaf'], width=1)
    # break the loop near each corner so the arms read as separate arrows
    for (x, y) in [(8, 1), (8, 2), (8, 3), (13, 12), (13, 13), (14, 12), (2, 12), (2, 13), (3, 12)]:
        d.point((x, y), fill=(0, 0, 0, 0))
    # arrowheads
    d.polygon([(5, 6), (9, 6), (7, 9)], fill=P['leafD'])
    d.polygon([(6, 7), (8, 7), (7, 8)], fill=P['leaf'])
    d.polygon([(12, 8), (15, 11), (11, 12)], fill=P['leafD'])
    d.polygon([(12, 9), (13, 11), (12, 11)], fill=P['leaf'])
    d.polygon([(0, 11), (4, 8), (5, 12)], fill=P['leafD'])
    d.polygon([(2, 11), (3, 9), (4, 11)], fill=P['leaf'])
    return im

SPRITES['recycle'] = _make_recycle()

# ================= export =================

def to_svg(img, name):
    w, h = img.size
    px_ = img.load()
    parts = []
    for y in range(h):
        x = 0
        while x < w:
            r, g, b, a = px_[x, y]
            if a < 128:
                x += 1
                continue
            run = 1
            while x + run < w and px_[x + run, y] == (r, g, b, a):
                run += 1
            parts.append(f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="#{r:02x}{g:02x}{b:02x}"/>')
            x += run
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{name}">' + ''.join(parts) + '</svg>')


manifest = {}
for name, img in SPRITES.items():
    svg = to_svg(img, name)
    with open(f'{OUT}/{name}.svg', 'w') as f:
        f.write(svg)
    manifest[name] = svg

with open('/home/claude/work/sprites.json', 'w') as f:
    json.dump(manifest, f)

# preview sheet
cols = 7
cell = 64
rows = (len(SPRITES) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * cell, rows * cell), (26, 18, 64, 255))
for i, (name, img) in enumerate(SPRITES.items()):
    big = img.resize((cell - 8, cell - 8), Image.NEAREST)
    sheet.paste(big, ((i % cols) * cell + 4, (i // cols) * cell + 4), big)
sheet.save('/home/claude/work/sprite_sheet.png')
print('sprites:', len(SPRITES), list(SPRITES))
