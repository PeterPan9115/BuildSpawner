"""Erzeugt alle Gebäude (.schem), den Index und die Vorschaubilder.  Aufruf: python3 tools/generate.py"""
import os, sys, traceback
sys.path.insert(0, os.path.dirname(__file__))
from cat_a import CATS_A
from cat_b import CATS_B
from render import render, sheet
import palettes

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RES = os.path.join(ROOT, 'src/main/resources/builds')
PV = os.path.join(ROOT, 'previews')
os.makedirs(RES, exist_ok=True); os.makedirs(PV, exist_ok=True)
lines = []; allimgs = []; alllabels = []; total = 0
for cid, cname, icon, col, desc, builds in CATS_A + CATS_B:
    lines.append(f'C|{cid}|{cname}|{icon}|{col}|{desc}')
    os.makedirs(f'{RES}/{cid}', exist_ok=True); os.makedirs(f'{PV}/{cid}', exist_ok=True)
    imgs = []; labels = []
    for bid, bn, bd, ic, fn in builds:
        try:
            v = fn(); v.mix(palettes.RULES.get(cid, {}), seed=sum(map(ord, cid + bid)))
            p = f'{RES}/{cid}/{bid}.schem'
            w, h, l, g = v.export(p)
            lines.append(f'B|{cid}|{bid}|{bn}|{bd}|{ic}|{w}|{h}|{l}|{g}')
            im = render(p, f'{PV}/{cid}/{bid}.png', ground=g, maxpx=520, title=f'{cname}: {bn}')
            imgs.append(im); labels.append(f'{bn} ({w}x{h}x{l})'); total += 1
        except Exception:
            print('FEHLER bei', cid, bid); traceback.print_exc()
    sheet(imgs, f'{PV}/_{cid}_uebersicht.png', cols=4, cell=(440, 420), title=f'{cname} – {len(imgs)} Gebäude', labels=labels)
    allimgs += imgs[:2]; alllabels += [f'{cname}: {l}' for l in labels[:2]]
open(f'{RES}/index.txt', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('Gebäude:', total)
