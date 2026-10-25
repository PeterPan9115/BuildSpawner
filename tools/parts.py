"""Wiederverwendbare Bauteile. Koordinaten: x=Ost, z=Süd (Vorderseite = +z), y=hoch. y=0 ist die Bodenebene."""
import math
from vox import *

class T:
    """Theme / Material-Palette"""
    def __init__(s, **k):
        s.timber = False; s.shutters = True; s.glass = 'glass_pane'; s.win_h = 2
        s.__dict__.update(k)
    # kleine Helfer
    def stairs(s, f, half='bottom'): return stair(s.roof, f, half)
    def rslab(s, t='bottom'): return slab(s.roof, t)
    @property
    def rblock(s): return B(s.roof_block)

# ------------------------------------------------------------------ Dächer
def roof_gable(v, t, x1, x2, z1, z2, y, ridge='z', over=1, over_b=1, fill=None, ridge_cap=True):
    """Satteldach. (x1..x2,z1..z2)=Gebäude, y=Oberkante der Wandplatte. Dachbeginn y+1."""
    if ridge == 'z':
        a1, a2, b1, b2 = x1 - over, x2 + over, z1 - over_b, z2 + over_b
        lo, hi = 'east', 'west'; wa1, wa2, wb1, wb2 = x1, x2, z1, z2
        co = lambda a, b: (a, b)
    else:
        a1, a2, b1, b2 = z1 - over, z2 + over, x1 - over_b, x2 + over_b
        lo, hi = 'south', 'north'; wa1, wa2, wb1, wb2 = z1, z2, x1, x2
        co = lambda a, b: (b, a)
    n = (a2 - a1 + 1) // 2           # Stair-Schichten pro Seite
    odd = (a2 - a1 + 1) % 2 == 1
    for i in range(n):
        for b in range(b1, b2 + 1):
            for a, f in ((a1 + i, lo), (a2 - i, hi)):
                x, z = co(a, b)
                v.s(x, y + 1 + i, z, stair(t.roof, f))
    if odd:
        a = a1 + n
        for b in range(b1, b2 + 1):
            x, z = co(a, b)
            v.s(x, y + 1 + (n - 1), z, B(t.roof_block))
            if ridge_cap:
                v.s(x, y + 1 + n, z, slab(t.roof))
    # Giebelwand füllen
    fillb = B(fill or t.wall)
    for b in (wb1, wb2):
        for a in range(wa1, wa2 + 1):
            ia = min(a - a1, a2 - a)
            top = y + 1 + min(ia, n - 1) - 1
            for yy in range(y + 1, top + 1):
                x, z = co(a, b)
                v.s(x, yy, z, fillb)
    return n

def roof_hip(v, t, x1, x2, z1, z2, y, over=1, cap=None):
    xa, xb, za, zb = x1 - over, x2 + over, z1 - over, z2 + over
    i = 0
    while True:
        ya = y + 1 + i
        wx, wz = xb - xa + 1, zb - za + 1
        if wx <= 2 or wz <= 2:
            v.fill(xa, ya - 1, za, xb, ya - 1, zb, cap or B(t.roof_block))
            if wx <= 2 and wz <= 2: pass
            break
        for x in range(xa, xb + 1):
            v.s(x, ya, za, stair(t.roof, 'south')); v.s(x, ya, zb, stair(t.roof, 'north'))
        for z in range(za + 1, zb):
            v.s(xa, ya, z, stair(t.roof, 'east')); v.s(xb, ya, z, stair(t.roof, 'west'))
        xa += 1; xb -= 1; za += 1; zb -= 1; i += 1
    return i

def roof_pyramid_tower(v, t, cx, cz, r, y, over=1, tip='lightning_rod'):
    """Pyramidendach über quadratischem Turm (Halbbreite r)"""
    n = roof_hip(v, t, cx - r, cx + r, cz - r, cz + r, y, over=over)
    top = y + 1 + n
    if tip: v.s(cx, top, cz, B(tip))
    return n

def roof_flat(v, t, x1, x2, z1, z2, y, over=1, parapet=False):
    v.fill(x1 - over, y + 1, z1 - over, x2 + over, y + 1, z2 + over, slab(t.roof))
    v.fill(x1, y + 1, z1, x2, y + 1, z2, B(t.roof_block))
    if parapet:
        v.walls(x1, y + 2, z1, x2, y + 2, z2, slab(t.roof))

# ------------------------------------------------------------------ Fenster / Türen
def wincols(n, door=None):
    c = (n - 1) // 2
    base = set()
    for k in range(-4, 5):
        for cc in ({c, n - 1 - c}):
            i = cc + 3 * k
            base.add(i)
    cols = {i for i in base if 1 <= i <= n - 2}
    if door is not None:
        cols = {i for i in cols if abs(i - door) >= 2}
        cols |= {i for i in (door - 2, door + 2, door - 5, door + 5) if 1 <= i <= n - 2}
    return sorted(cols)

OUT = {'N': 'north', 'S': 'south', 'W': 'west', 'E': 'east'}

def window(v, t, x, y, z, out, shutters=None):
    """Fenster in Wand bei (x,y..y+h-1,z) mit Außenrichtung out"""
    for k in range(t.win_h):
        v.s(x, y + k, z, B(t.glass))
    dx, dz = VEC[out]
    sh = t.shutters if shutters is None else shutters
    if sh:
        side = cw(out)
        sx, sz = VEC[side]
        for sgn in (1, -1):
            px, pz = x + dx + sx * sgn, z + dz + sz * sgn
            # nur wenn Wand dahinter existiert
            wx, wz = x + sx * sgn, z + sz * sgn
            wall_blk = v.get(wx, y, wz)
            if wall_blk and parse(wall_blk)[0] == parse(B(t.wall))[0]:
                for k in range(t.win_h):
                    v.s(px, y + k, pz, trap(t.trap, out, 'bottom', True))

def house(t, w, l, floors=1, roof='gable', ridge='z', fh=4, porch=False, chimney=True,
          balcony=False, flat_color=None, door_col=None, plinth=True, walls_blk=None, interior=True,
          gable_wall=None, dormers=False, over=1, windows=True, lamp=True):
    v = V()
    top = floors * fh
    W = walls_blk or t.wall
    dcol = (w - 1) // 2 if door_col is None else door_col
    # Fundament + Boden
    v.fill(0, -3, 0, w - 1, -1, l - 1, B(t.found))
    v.fill(0, 0, 0, w - 1, 0, l - 1, B(t.floor))
    if plinth:
        v.walls(0, 0, 0, w - 1, 0, l - 1, B(t.found2))
    # Wände
    for k in range(floors):
        v.walls(0, k * fh + 1, 0, w - 1, k * fh + fh - 1, l - 1, B(W))
    if getattr(t, 'base', None):
        v.walls(0, 1, 0, w - 1, 1, l - 1, B(t.base))
    # Balken (Geschossdecken) + Eckpfosten
    for k in range(1, floors + 1):
        yy = k * fh
        v.fill(0, yy, 0, w - 1, yy, 0, log(t.beam, 'x')); v.fill(0, yy, l - 1, w - 1, yy, l - 1, log(t.beam, 'x'))
        v.fill(0, yy, 0, 0, yy, l - 1, log(t.beam, 'z')); v.fill(w - 1, yy, 0, w - 1, yy, l - 1, log(t.beam, 'z'))
        if k < floors or roof != 'none':
            v.fill(1, yy, 1, w - 2, yy, l - 2, B(t.floor))
    for (px, pz) in ((0, 0), (w - 1, 0), (0, l - 1), (w - 1, l - 1)):
        v.fill(px, 1, pz, px, top, pz, log(t.log))
    # Fenster
    if windows:
        for k in range(floors):
            y0 = k * fh + 2
            for (axis_len, fixed, outd, horizontal) in ((w, l - 1, 'south', True), (w, 0, 'north', True),
                                                       (l, 0, 'west', False), (l, w - 1, 'east', False)):
                dc = dcol if (outd == 'south' and k == 0) else None
                for i in wincols(axis_len, dc):
                    if horizontal: x, z = i, fixed
                    else: x, z = fixed, i
                    if outd == 'south' and k == 0 and i == dcol: continue
                    window(v, t, x, y0, z, outd)
        if t.timber:
            for k in range(floors):
                for (axis_len, fixed, horizontal) in ((w, l - 1, True), (w, 0, True), (l, 0, False), (l, w - 1, False)):
                    cols = wincols(axis_len, dcol if (fixed == l - 1 and horizontal and k == 0) else None)
                    for i in cols:
                        for d in (-1, 1):
                            j = i + d
                            if 1 <= j <= axis_len - 2 and j not in cols and not (horizontal and fixed == l - 1 and k == 0 and j == dcol):
                                x, z = (j, fixed) if horizontal else (fixed, j)
                                v.fill(x, k * fh + 1, z, x, k * fh + fh - 1, z, log(t.log))
    # Tür
    v.clear(dcol, 1, l - 1, dcol, 2, l - 1)
    v.s(dcol, 1, l - 1, door(t.door, 'south', 'lower', 'left'))
    v.s(dcol, 2, l - 1, door(t.door, 'south', 'upper', 'left'))
    v.s(dcol, 0, l, B(t.found2))
    for sx in (-1, 1):
        if dcol + sx * 1 < w - 1 and dcol + sx * 1 > 0:
            v.s(dcol + sx, 2, l, wall_torch('south'))
    # Dach
    ry = top
    if roof == 'gable':
        roof_gable(v, t, 0, w - 1, 0, l - 1, ry, ridge=ridge, over=over, fill=gable_wall or W)
        for (a, b, c2, d2) in ((0, 0, 0, 0),):
            pass
    elif roof == 'hip':
        roof_hip(v, t, 0, w - 1, 0, l - 1, ry, over=over)
    elif roof == 'flat':
        roof_flat(v, t, 0, w - 1, 0, l - 1, ry, over=over, parapet=True)
    # Kamin
    if chimney and roof != 'flat':
        cx = 1 if ridge == 'z' else 1
        cz = 2
        hh = top + (w // 2) + 2 if ridge == 'z' else top + (l // 2) + 2
        hh = top + 3 + (1 if floors == 1 else 0) + (w // 2 if ridge == 'z' else 0) // 2
        v.fill(cx, top - 1, cz, cx, hh, cz, B(t.found))
        v.s(cx, hh + 1, cz, B('cobblestone_wall'))
        v.s(cx, hh + 2, cz, B('campfire', lit='true', signal_fire='false'))
        if interior:
            v.s(1, 1, 2, B('furnace', facing='south', lit='true'))
    # Innenleben
    if interior:
        for k in range(floors):
            furnish(v, t, w, l, k * fh, 'bed' if k > 0 or floors == 1 and w * l < 60 else 'living', dcol)
        if floors > 1:
            for k in range(floors - 1):
                yy = (k + 1) * fh
                v.clear(w - 2, yy, 1, w - 2, yy, 1)
                for q in range(k * fh + 1, yy + 2):
                    v.s(w - 2, q, 1, B('ladder', facing='south'))
        if lamp:
            for k in range(floors):
                v.s(w // 2, k * fh + fh - 1, l // 2, lantern(True))
    # Balkon
    if balcony and floors >= 2:
        yy = fh
        cx = dcol
        v.fill(cx - 1, yy, l, cx + 1, yy, l + 1, slab(t.wood_slab, 'bottom'))
        v.walls(cx - 1, yy + 1, l, cx + 1, yy + 1, l + 1, B(t.fence)) if False else None
        for x in range(cx - 1, cx + 2):
            v.s(x, yy + 1, l + 1, B(t.fence))
        v.s(cx - 1, yy + 1, l, B(t.fence)); v.s(cx + 1, yy + 1, l, B(t.fence))
        v.clear(cx, yy + 1, l - 1, cx, yy + 2, l - 1)
        v.s(cx, yy + 1, l - 1, door(t.door, 'south', 'lower', 'left'))
        v.s(cx, yy + 2, l - 1, door(t.door, 'south', 'upper', 'left'))
        v.s(cx - 1, yy - 1, l + 1, stair(t.wood_stair, 'north', 'top')); v.s(cx + 1, yy - 1, l + 1, stair(t.wood_stair, 'north', 'top'))
    # Veranda
    if porch:
        pd = 3
        px1, px2 = dcol - 2, dcol + 2
        px1 = max(px1, 0); px2 = min(px2, w - 1)
        v.fill(px1, 0, l, px2, 0, l + pd - 1, B(t.floor))
        for px in (px1, px2):
            v.fill(px, 1, l + pd - 1, px, 3, l + pd - 1, B(t.fence))
        v.fill(px1, 4, l, px2, 4, l + pd - 1, slab(t.wood_slab, 'bottom'))
        v.fill(px1, 4, l + pd - 1, px2, 4, l + pd - 1, log(t.beam, 'x'))
        v.s(dcol, 3, l + pd - 1, lantern(True))
        v.s(dcol, 4, l + pd - 1, log(t.beam, 'x'))
        v.fill(px1 + 1, 1, l + pd - 1, px2 - 1, 1, l + pd - 1, B(t.fence)) if False else None
    return v

def furnish(v, t, w, l, y0, kind, dcol):
    y = y0 + 1
    c = getattr(t, 'bedcolor', 'red')
    if kind == 'bed':
        v.s(1, y, l - 3, bed(c, 'north', 'foot')) if False else None
        v.s(w - 2, y, l - 2, bed(c, 'north', 'foot')); v.s(w - 2, y, l - 3, bed(c, 'north', 'head'))
        v.s(w - 3, y, l - 3, chest('north') if False else B('barrel', facing='up'))
        v.s(1, y, l - 2, B('crafting_table'))
        v.s(1, y, l - 3, B('bookshelf')); v.s(1, y + 1, l - 3, B('bookshelf'))
        v.fill(2, y, 2, 3, y, 3, B(getattr(t, 'rug', 'red_carpet'))) if w > 6 and l > 6 else None
    else:
        v.s(1, y, 1, chest('south')) if False else None
        v.s(w - 2, y, l - 2, B('crafting_table'))
        v.s(w - 3, y, l - 2, B('barrel', facing='up'))
        cx, cz = w // 2, l // 2
        v.s(cx, y, cz, B(t.fence)); v.s(cx, y + 1, cz, B('oak_pressure_plate') if False else B('stone_pressure_plate'))
        v.s(cx - 1, y, cz, stair(t.wood_stair, 'east')); v.s(cx + 1, y, cz, stair(t.wood_stair, 'west'))
        v.s(2, y, l - 2, chest('north'))
        v.fill(max(1, cx - 1), y, max(1, cz + 1), min(w - 2, cx + 1), y, min(l - 2, cz + 2), B(getattr(t, 'rug', 'red_carpet')))
        v.s(w - 2, y, 2, bed(c, 'north', 'foot')) if False else None

# ------------------------------------------------------------------ Deko
def lamp_post(v, t, x, z, h=3):
    v.fill(x, 0, z, x, h, z, B(t.fence))
    v.s(x, h + 1, z, lantern(False))

def barrel_stack(v, x, z, y=1, n=2):
    for i in range(n):
        v.s(x + i, y, z, B('barrel', facing='up'))
    v.s(x, y + 1, z, B('barrel', facing='up'))

def crate(v, x, y, z, t='barrel'):
    v.s(x, y, z, B(t, facing='up') if t == 'barrel' else B(t))

def flowerbed(v, x1, z1, x2, z2, y=1, base=None, plants=('poppy', 'dandelion', 'azure_bluet', 'cornflower', 'oxeye_daisy')):
    i = 0
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            if base: v.s(x, y - 1, z, B(base))
            v.s(x, y, z, B(plants[(x * 3 + z * 5 + i) % len(plants)]))
            i += 1

def tree(v, x, z, h=5, trunk='oak_log', lv='oak_leaves', r=2, y=1):
    v.fill(x, y, z, x, y + h - 1, z, log(trunk))
    for dy in range(-1, 3):
        rr = r if dy < 1 else r - dy + 1
        for dx in range(-rr, rr + 1):
            for dz in range(-rr, rr + 1):
                if abs(dx) + abs(dz) <= rr + (1 if dy < 1 else 0) and not (dx == 0 and dz == 0 and dy < 1):
                    if (x + dx, y + h + dy, z + dz) not in v.b:
                        v.s(x + dx, y + h + dy, z + dz, leaves(lv))

def fence_around(v, t, x1, z1, x2, z2, y=1, gap=None):
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            if x in (x1, x2) or z in (z1, z2):
                if gap and (x, z) in gap: continue
                v.s(x, y, z, B(t.fence))

def sign_board(v, x, y, z, t, out='south', w=3):
    """Schild aus Holz-Slab + Trapdoors"""
    for i in range(w):
        v.s(x + i, y, z, trap(t.trap, out, 'top', True) if False else B(t.wall))
    return

# ------------------------------------------------------------------ Türme / Brunnen / Stände
def tower(t, r=2, h=12, roof='pyramid', crenel=False, door=True, windows=True, base_w=None, ladders=True):
    """Quadratischer Turm, Halbbreite r (Breite 2r+1)"""
    v = V(); n = 2 * r + 1
    v.fill(0, -3, 0, n - 1, -1, n - 1, B(t.found))
    v.fill(0, 0, 0, n - 1, 0, n - 1, B(t.floor))
    v.walls(0, 1, 0, n - 1, h, n - 1, B(t.wall))
    for (px, pz) in ((0, 0), (n - 1, 0), (0, n - 1), (n - 1, n - 1)):
        v.fill(px, 1, pz, px, h, pz, log(t.log))
    for yy in range(4, h, 4):
        v.fill(1, yy, 1, n - 2, yy, n - 2, B(t.floor))
        v.walls(0, yy, 0, n - 1, yy, n - 1, log(t.beam, 'x')) if False else None
        for x in range(0, n):
            v.s(x, yy, 0, log(t.beam, 'x')); v.s(x, yy, n - 1, log(t.beam, 'x'))
        for z in range(0, n):
            v.s(0, yy, z, log(t.beam, 'z')); v.s(n - 1, yy, z, log(t.beam, 'z'))
        if ladders:
            v.clear(1, yy, 1, 1, yy, 1)
            for q in range(yy - 3, yy + 1):
                v.s(1, q, 1, B('ladder', facing='south'))
    if windows:
        c = r
        for yy in range(3, h - 1, 4):
            for (x, z, o) in ((c, 0, 'north'), (c, n - 1, 'south'), (0, c, 'west'), (n - 1, c, 'east')):
                if o == 'south' and yy < 5 and door: continue
                v.s(x, yy, z, B(t.glass)); v.s(x, yy + 1, z, B(t.glass))
    if door:
        c = r
        v.clear(c, 1, n - 1, c, 2, n - 1)
        v.s(c, 1, n - 1, door_blk(t, 'lower')); v.s(c, 2, n - 1, door_blk(t, 'upper'))
    if roof == 'pyramid':
        # Plattform-Überstand
        roof_pyramid_tower(v, t, r, r, r, h, over=1)
    elif roof == 'flat':
        v.fill(-1, h + 1, -1, n, h + 1, n, B(t.floor))
        v.walls(-1, h + 2, -1, n, h + 2, n, B(t.found_wall) if hasattr(t, 'found_wall') else B(t.fence))
        v.s(r, h + 2, r, lantern(False))
    elif roof == 'crenel':
        for x in range(-1, n + 1):
            for z in range(-1, n + 1):
                if x in (-1, n) or z in (-1, n):
                    v.s(x, h + 1, z, slab(t.found_slab, 'bottom')) if False else v.s(x, h + 1, z, B(t.found))
                    if (x + z) % 2 == 0: v.s(x, h + 2, z, B(t.found))
        v.fill(0, h + 1, 0, n - 1, h + 1, n - 1, B(t.floor))
    return v

def door_blk(t, half): return door(t.door, 'south', half, 'left')

def well(t, ground=None):
    v = V()
    v.fill(0, -3, 0, 4, -1, 4, B(t.found))
    v.fill(0, 0, 0, 4, 0, 4, B(t.found2))
    v.walls(1, 1, 1, 3, 1, 3, B(t.found))
    v.s(2, 1, 2, B('water', level=0))
    v.fill(2, 0, 2, 2, 0, 2, B('water', level=0))
    for (x, z) in ((1, 1), (3, 1), (1, 3), (3, 3)):
        v.fill(x, 2, z, x, 3, z, B(t.fence))
    v.fill(0, 4, 1, 4, 4, 3, slab(t.wood_slab)) if False else None
    for z in (0, 1, 2, 3, 4):
        v.s(1, 4, z, stair(t.roof, 'east')); v.s(3, 4, z, stair(t.roof, 'west'))
        v.s(2, 5, z, slab(t.roof)); v.s(2, 4, z, B(t.roof_block))
    v.s(2, 3, 2, B(t.fence)) if False else None
    v.s(2, 3, 1, B('barrel', facing='up')) if False else None
    v.s(2, 3, 2, lantern(True))
    return v

def stall(t, awning=('red', 'white'), w=5, d=4, goods=('barrel', 'hay_block')):
    v = V()
    v.fill(0, -2, 0, w - 1, -1, d - 1, B(t.found))
    v.fill(0, 0, 0, w - 1, 0, d - 1, B(t.floor))
    for (x, z) in ((0, 0), (w - 1, 0), (0, d - 1), (w - 1, d - 1)):
        v.fill(x, 1, z, x, 3, z, B(t.fence))
    for x in range(-1, w + 1):
        for z in range(-1, d):
            v.s(x, 4, z, B(awning[(x + 1) % 2] + '_wool'))
    for x in range(-1, w + 1):
        v.s(x, 3, d, B(awning[(x + 1) % 2] + '_carpet')) if False else None
    v.fill(1, 1, 0, w - 2, 1, 0, B(t.wall))
    v.fill(1, 2, 0, w - 2, 2, 0, slab(t.wood_slab, 'bottom'))
    for i, x in enumerate(range(1, w - 1)):
        v.s(x, 3, 0, B(['red_mushroom', 'apple'][0]) if False else B('flower_pot')) if False else None
    v.s(1, 3, 0, B('potted_poppy')) if False else None
    v.s(1, 1, 1, B('barrel', facing='up')); v.s(w - 2, 1, 1, B('hay_block', axis='y'))
    v.s(2, 1, 1, chest('south')) if w > 4 else None
    v.s(w // 2, 2, 0, B('melon') if False else B('barrel', facing='up'))
    v.s(w // 2, 3, 1, lantern(True))
    return v

# ------------------------------------------------------------------ Schiff
def ship(t, length=27, beam=9, mast_h=14, sail='white_wool', masts=2, flag='black_banner', cabin=True):
    """Segelschiff entlang z (Bug zeigt nach +z => Vorderseite zum Spieler). Länge in z, Breite in x."""
    v = V()
    cx = beam // 2
    hull_h = 5
    water_y = 1
    keel = 3
    L = length
    def half_w(z, y):
        # Breite des Rumpfs an Position z (0=Heck,L-1=Bug) auf Höhe y(0..hull_h)
        u = z / (L - 1)
        base = 1 - (abs(u - 0.4) / (0.6 if u > 0.4 else 0.5)) ** 2.2
        base = max(0.0, base)
        spread = 0.55 + 0.45 * (y / hull_h)
        return (beam / 2) * base * spread
    for y in range(0, hull_h + 1):
        for z in range(0, L):
            hw = half_w(z, y)
            for x in range(beam):
                dx = abs(x - cx)
                if dx <= hw - 0.2 or (hw > 0.3 and dx == 0):
                    edge = dx > hw - 1.2
                    v.s(x, y - 2, z, B(t.hull) if edge or y == 0 else B(t.hull2))
    # Kiel-Linie
    for z in range(2, L - 3):
        v.s(cx, -3, z, B(t.hull))
    # Deck
    for z in range(0, L):
        for x in range(beam):
            if v.get(x, 3, z):  # Rumpf-Oberkante
                pass
    deck_y = hull_h - 2
    for z in range(0, L):
        hw = half_w(z, hull_h)
        for x in range(beam):
            dx = abs(x - cx)
            if dx <= hw - 1.2:
                v.s(x, deck_y, z, B(t.deck))
    # Reling
    for z in range(0, L):
        hw = half_w(z, hull_h)
        for x in range(beam):
            dx = abs(x - cx)
            if hw - 1.2 < dx <= hw - 0.2 and hw > 1:
                v.s(x, deck_y + 1, z, B(t.fence))
    # Masten
    pos = [int(L * 0.62), int(L * 0.32)] if masts == 2 else [int(L * 0.5)]
    for mi, mz in enumerate(pos):
        mh = mast_h if mi == 0 else mast_h - 3
        v.fill(cx, deck_y + 1, mz, cx, deck_y + mh, mz, log(t.log))
        for k, (yy, wd) in enumerate(((deck_y + 4, beam + 2), (deck_y + mh - 3, beam))):
            if mh - 3 <= 4 and k == 1: continue
            h2 = wd // 2
            v.fill(cx - h2, yy, mz, cx + h2, yy, mz, log(t.beam, 'x'))
            top = deck_y + mh - 4 if k == 1 else deck_y + mh - 6
            if k == 0:
                for sx in range(cx - h2 + 1, cx + h2):
                    for sy in range(yy - 4 if False else deck_y + 2, yy):
                        v.s(sx, sy, mz + 1, B(sail))
                continue
            if k == 1:
                for sx in range(cx - h2 + 1, cx + h2):
                    for sy in range(deck_y + mh - 5 if False else deck_y + 5, yy):
                        v.s(sx, sy, mz + 1, B(sail))
        v.s(cx, deck_y + mh + 1, mz, B('black_wool') if False else B(t.fence))
        v.s(cx, deck_y + mh + 2, mz, B(flag, rotation=0) if flag.endswith('banner') and False else B('black_wool'))
        v.s(cx, deck_y + mh + 2, mz + 1, B('black_wool'))
    # Bugspriet
    for k in range(-3, 3):
        v.s(cx, deck_y + 1 + max(0, (k + 1) // 2), L - 3 + k, log(t.log, 'z') if k < 1 else B(t.fence))
    # Hecksaufbau (Kajüte)
    if cabin:
        z1, z2 = 0, min(7, L // 4)
        for z in range(z1, z2 + 1):
            for x in range(beam):
                dx = abs(x - cx)
                hw = half_w(z, hull_h)
                if dx <= hw - 1.2:
                    v.s(x, deck_y + 1, z, B(t.deck)) if False else None
        cw_ = max(2, int(half_w(z2, hull_h) - 1.6))
        for z in range(z1 + 1, z2 + 1):
            for x in range(cx - cw_ - 1, cx + cw_ + 2):
                for y in range(deck_y + 1, deck_y + 4):
                    edge = (x in (cx - cw_ - 1, cx + cw_ + 1)) or z in (z1 + 1, z2)
                    if edge:
                        v.s(x, y, z, B(t.wall))
        v.fill(cx - cw_ - 1, deck_y + 4, z1 + 1, cx + cw_ + 1, deck_y + 4, z2, B(t.deck))
        v.fill(cx - cw_ - 2, deck_y + 4, z1, cx + cw_ + 2, deck_y + 4, z2 + 1, slab(t.wood_slab, 'bottom')) if False else None
        v.walls(cx - cw_ - 1, deck_y + 5, z1 + 1, cx + cw_ + 1, deck_y + 5, z2, B(t.fence))
        for x in range(cx - cw_, cx + cw_ + 1):
            v.clear(x, deck_y + 1, z2, x, deck_y + 3, z2) if x == cx else None
        v.clear(cx, deck_y + 1, z2, cx, deck_y + 2, z2)
        v.s(cx, deck_y + 1, z2, door(t.door, 'south', 'lower')); v.s(cx, deck_y + 2, z2, door(t.door, 'south', 'upper'))
        for sx in (cx - cw_ - 1, cx + cw_ + 1):
            v.s(sx, deck_y + 2, (z1 + z2) // 2 + 1, B(t.glass))
        # Heckfenster
        for x in range(cx - cw_, cx + cw_ + 1, 2):
            v.s(x, deck_y + 2, z1 + 1, B(t.glass))
        v.s(cx, deck_y + 3, z2 - 1, lantern(True))
        v.s(cx - 1, deck_y + 1, z1 + 2, bed('red', 'north', 'foot')); v.s(cx - 1, deck_y + 1, z1 + 1, bed('red', 'north', 'head'))
        v.s(cx + 1, deck_y + 1, z1 + 2, chest('south'))
        v.s(cx + 1, deck_y + 1, z1 + 3, B('barrel', facing='up'))
    # Steuer
    v.s(cx, deck_y + 5, 4, B('black_wool')) if False else None
    # Laternen am Bug und Kanonen (Dispenser-Optik)
    for z in (int(L * 0.45), int(L * 0.65), int(L * 0.8)):
        hw = half_w(z, 2)
        for sgn in (-1, 1):
            x = int(round(cx + sgn * (hw - 0.5)))
            v.s(x, 1, z, B('dispenser', facing='east' if sgn > 0 else 'west'))
    v.s(cx, deck_y + 1, L - 3, lantern(False)) if False else None
    v.s(cx, deck_y + 2, L - 4, B('lantern', hanging='false')) if False else None
    v.s(cx, deck_y + 1, L - 3, B('barrel', facing='up'))
    v.s(cx, deck_y + 2, L - 3, lantern(False))
    return v

def pier(t, length=15, w=5):
    v = V()
    v.fill(0, 0, 0, w - 1, 0, length - 1, B(t.deck))
    for z in range(0, length, 4):
        for x in (0, w - 1):
            v.fill(x, -4, z, x, 1, z, log(t.log))
            v.s(x, 2, z, B(t.fence)) if False else None
        v.s(0, 2, z, lantern(False)) if False else None
    for z in range(0, length):
        for x in (0, w - 1):
            if z % 4 != 0: v.s(x, 1, z, B(t.fence))
    for z in range(0, length, 4):
        for x in (0, w - 1):
            v.s(x, 1, z, B(t.fence)); v.s(x, 2, z, B(t.fence)); v.s(x, 3, z, lantern(False))
    for z in range(1, length, 5):
        v.s(w // 2, 1, z, B('barrel', facing='up'))
    # Unterwasser-Stützen: Wasser außen herum nicht gesetzt (liegt im Gelände)
    return v
