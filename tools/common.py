from parts import *

def attach_front_tower(v, t, w, l, r, h, roof='pyramid'):
    n = 2 * r + 1; x0 = (w - n) // 2
    tw = tower(t, r, h, roof=roof, door=True, windows=True, ladders=False)
    v.paste(tw, x0, 0, l - 1)
    dc = x0 + r
    v.clear(dc, 1, l - 1, dc, 2, l - 1)
    return v

def banner(color, f): return B(color + '_wall_banner', facing=f)

def tavern(t, big=True, col='yellow'):
    w, l = (13, 9) if big else (11, 8)
    v = house(t, w, l, floors=2, ridge='x', porch=True, balcony=True, door_col=w // 2, lamp=True)
    y = 1
    # Tresen
    for x in range(2, w - 4):
        v.s(x, y, 2, B(t.fence) if False else slab(t.wood_slab, 'top')) if False else v.s(x, y, 3, stair(t.wood_stair, 'south', 'top'))
        v.s(x, y + 1, 3, B('stone_pressure_plate')) if x % 2 == 0 else None
    for x in range(2, w - 4):
        v.s(x, y, 1, B('barrel', facing='up')); v.s(x, y + 1, 1, B('barrel', facing='south')) if x % 2 else None
    v.s(w - 3, y, 2, B('furnace', facing='west', lit='true'))
    for i, x in enumerate(range(3, w - 3, 3)):
        v.s(x, y, l - 3, B(t.fence)); v.s(x, y + 1, l - 3, B('stone_pressure_plate'))
        v.s(x - 1, y, l - 3, stair(t.wood_stair, 'east')); v.s(x + 1, y, l - 3, stair(t.wood_stair, 'west'))
    v.s(w // 2 - 2, 2, l, banner(col, 'south')) if False else None
    v.s(w // 2 + 2, 3, l - 1, banner(col, 'south'))
    v.s(w // 2 - 2, 3, l - 1, banner(col, 'south'))
    barrel_stack(v, w - 1, l, 1, 1) if False else None
    v.s(w, 1, l - 1, B('barrel', facing='up')); v.s(w, 1, l - 2, B('barrel', facing='up'))
    return v

def town_hall(t, w=15, l=11, col='white'):
    v = house(t, w, l, floors=2, ridge='x', porch=False, chimney=False, door_col=w // 2, lamp=True, over=1)
    attach_front_tower(v, t, w, l, 2, 13)
    # Treppe vor dem Turm
    dc = w // 2
    for k, wd in enumerate((2, 1)):
        for x in range(dc - 2 - wd + 1, dc + 3 + wd):
            v.s(x, 0, l + 4 + k, B(t.found2)) if False else None
    for x in range(dc - 3, dc + 4):
        v.s(x, -1, l + 4, B(t.found))
        v.s(x, 0, l + 4, stair(t.found_stair, 'south'))
    # Tresen + Bänke
    for x in range(2, w - 2, 3):
        v.s(x, 1, 2, B('lectern', facing='south'))
    for x in range(1, w - 1):
        v.s(x, 3, 2, B('red_carpet')) if False else None
    v.s(dc - 4, 3, l, banner(col, 'south')) if False else None
    v.s(dc - 3, 3, l - 1, banner('red', 'south')); v.s(dc + 3, 3, l - 1, banner('red', 'south'))
    v.fill(dc - 3, 1, 2, dc + 3, 1, 5, B('red_carpet'))
    return v

def smithy(t, extra_h=0):
    v = house(t, 9, 7, floors=1, ridge='z', porch=False, chimney=True, lamp=True)
    # Schmiedeanbau (Ost)
    v.fill(9, 0, 0, 14, 0, 6, B(t.found2))
    v.fill(9, -3, 0, 14, -1, 6, B(t.found))
    for (x, z) in ((14, 0), (14, 6), (14, 3)):
        v.fill(x, 1, z, x, 3, z, B(t.fence))
    v.fill(9, 4, 0, 14, 4, 6, slab(t.wood_slab, 'bottom'))
    v.fill(9, 3, 0, 14, 3, 0, B(t.fence)) if False else None
    v.s(10, 1, 1, B('anvil', facing='south')); v.s(12, 1, 1, B('blast_furnace', facing='south', lit='true'))
    v.s(13, 1, 1, B('furnace', facing='south', lit='true')); v.s(10, 1, 4, B('grindstone', face='floor', facing='east'))
    v.s(12, 1, 4, B('cauldron')); v.s(13, 1, 4, B('lava_cauldron')); v.s(10, 1, 6, B('smithing_table'))
    v.s(12, 1, 6, chest('north')); v.s(11, 1, 6, B('barrel', facing='up'))
    v.s(11, 3, 3, lantern(True)) if False else v.s(11, 3, 3, lantern(True))
    v.fill(9, 1, 0, 9, 2, 0, B(t.fence)) if False else None
    v.s(9, 3, 3, B('iron_bars')) if False else None
    # Essen-Kamin außen hoch
    v.fill(14, 1, 1, 14, 6, 1, B(t.found)); v.s(14, 7, 1, B('cobblestone_wall')); v.s(14, 8, 1, B('campfire', lit='true', signal_fire='false'))
    v.s(14, 1, 1, B('blast_furnace', facing='west', lit='true')) if False else None
    v.s(9, 1, 3, B(t.floor)) if False else None
    return v

def shop(t, w=9, l=7, col=('red', 'white'), floors=1):
    v = house(t, w, l, floors=floors, ridge='x', porch=False, chimney=False, door_col=w // 2, lamp=True)
    # Markise
    for x in range(1, w - 1):
        for z in range(l, l + 2):
            v.s(x, 4 if False else 3, z, stair(t.wood_stair, 'south', 'top') if False else B(col[(x) % 2] + '_carpet')) if False else None
    for x in range(0, w):
        v.s(x, 3, l, B(col[x % 2] + '_wool'))
        v.s(x, 3, l + 1, B(col[x % 2] + '_wool'))
    for x in (0, w - 1):
        v.fill(x, 1, l + 1, x, 2, l + 1, B(t.fence))
    v.s(w // 2, 0, l + 1, B(t.found2)) if False else None
    v.s(1, 1, l, B('barrel', facing='up')); v.s(w - 2, 1, l, B('hay_block', axis='y'))
    return v

def warehouse(t, w=11, l=13, fh=6):
    v = house(t, w, l, floors=1, fh=fh, ridge='z', porch=False, chimney=False, door_col=w // 2, windows=False, lamp=False, interior=False)
    # Großes Tor
    dc = w // 2
    v.clear(dc - 1, 1, l - 1, dc + 1, 4, l - 1)
    for x in (dc - 1, dc + 1):
        v.fill(x, 1, l - 1, x, 4, l - 1, B(t.fence)) if False else None
    v.fill(dc - 1, 1, l - 1, dc, 3, l - 1, B(t.floor)) if False else None
    for dx in (-1, 0):
        v.s(dc + dx, 1, l - 1, door(t.door, 'south', 'lower', 'left' if dx == -1 else 'right'))
        v.s(dc + dx, 2, l - 1, door(t.door, 'south', 'upper', 'left' if dx == -1 else 'right'))
    v.s(dc + 1, 1, l - 1, B(t.wall)); v.s(dc + 1, 2, l - 1, B(t.wall))
    v.fill(dc - 1, 3, l - 1, dc + 1, 4, l - 1, B(t.wall)) if False else None
    v.s(dc, 4, l - 1, B(t.beam, axis='x')) if False else None
    # Fenster hoch
    for z in (3, 6, 9):
        v.s(0, 4, z, B(t.glass)); v.s(w - 1, 4, z, B(t.glass))
    # Fracht
    for x in range(1, w - 1, 2):
        v.s(x, 1, 1, B('barrel', facing='up')); v.s(x, 2, 1, B('barrel', facing='up'))
        v.s(x, 1, 2, chest('south'))
    for z in range(4, 10, 2):
        v.s(w - 2, 1, z, B('hay_block', axis='y')); v.s(w - 2, 2, z, B('hay_block', axis='y'))
        v.s(1, 1, z, B('barrel', facing='up')); v.s(2, 1, z, chest('east'))
    v.s(dc, 5, l // 2, lantern(True)); v.s(dc, 5, 3, lantern(True))
    # Dachluke-Kran
    v.fill(dc, 6, l, dc, 8, l, B(t.fence)) if False else None
    return v

def barn(t, w=9, l=13, fh=6, accent='red'):
    v = warehouse(t, w, l, fh)
    return v

def stable(t, w=11, d=7):
    v = V()
    v.fill(0, -2, 0, w - 1, -1, d - 1, B(t.found)); v.fill(0, 0, 0, w - 1, 0, d - 1, B('dirt_path') if False else B('coarse_dirt'))
    v.fill(0, 0, 0, w - 1, 0, 1, B(t.floor))
    for x in range(0, w, 5):
        for z in (0, d - 1):
            v.fill(x, 1, z, x, 3, z, log(t.log))
    v.fill(0, 4, 0, w - 1, 4, d - 1, B(t.roof_block)) if False else None
    roof_gable(v, t, 0, w - 1, 0, d - 1, 3, ridge='x', over=1, fill=t.wall)
    # Boxen
    for x in (2, 4, 7, 9):
        v.fill(x, 1, 2, x, 1, d - 2, B(t.fence)) if False else None
    for x in (3, 7):
        for z in range(2, d):
            v.s(x, 1, z, B(t.fence))
    for x in (1, 5, 9):
        v.s(x, 1, d - 2, B('hay_block', axis='y')); v.s(x + 0, 1, 2, B('water_cauldron', level=3) if False else B('cauldron'))
    v.fill(0, 1, 1, w - 1, 1, 1, B(t.fence)) if False else None
    v.s(w // 2, 3, 3, lantern(True))
    return v

def chapel(t, w=7, l=13, h=14, col='white'):
    v = house(t, w, l, floors=1, fh=7, ridge='z', porch=False, chimney=False, door_col=w // 2, windows=False, lamp=False, interior=False)
    attach_front_tower(v, t, w, l, 2, h)
    # hohe Fenster
    for z in range(2, l - 2, 3):
        for yy in (3, 4, 5):
            v.s(0, yy, z, B('light_blue_stained_glass_pane') if False else B(t.glass)); v.s(w - 1, yy, z, B(t.glass))
    # Bänke + Altar
    for z in range(3, l - 3, 2):
        v.s(1, 1, z, stair(t.wood_stair, 'east')); v.s(2, 1, z, stair(t.wood_stair, 'east')) if False else None
        v.s(w - 2, 1, z, stair(t.wood_stair, 'west'))
    v.fill(2, 1, 1, w - 3, 1, l - 4, B('red_carpet'))
    v.s(w // 2, 1, 1, B('smooth_stone_slab') if False else B('lectern', facing='south'))
    v.s(w // 2, 5, 1, B('gold_block')) if False else None
    v.s(w // 2, 3, 0, B(t.glass)); v.s(w // 2, 4, 0, B(t.glass)); v.s(w // 2, 5, 0, B(t.glass))
    for z in (3, 7):
        v.s(1, 4, z, lantern(True)); v.s(w - 2, 4, z, lantern(True))
    return v

def lighthouse(t, h=17, r0=3, bands=('white', 'red')):
    v = V()
    v.disc(r0, r0, r0 + 1, -1, B(t.found)) if False else None
    for y in range(-3, 1):
        v.disc(r0 + 1, r0 + 1, r0 + 1, y, B(t.found))
    cx = cz = r0 + 1
    for y in range(1, h):
        rr = r0 if y < h * 0.5 else r0 - 1
        col = bands[(y // 3) % 2]
        v.disc(cx, cz, rr, y, B(col + '_concrete'), hollow=True)
    # Boden
    for y in range(4, h, 5):
        v.disc(cx, cz, r0 - 1, y, B(t.floor))
        v.clear(cx - 1, y, cz - 1, cx - 1, y, cz - 1)
        for q in range(y - 4, y + 1):
            v.s(cx - 1, q, cz - 1, B('ladder', facing='east'))
    # Tür
    v.clear(cx, 1, cz + r0, cx, 2, cz + r0)
    v.s(cx, 1, cz + r0, door(t.door, 'south', 'lower')); v.s(cx, 2, cz + r0, door(t.door, 'south', 'upper'))
    # Galerie + Laterne
    v.disc(cx, cz, r0 + 1, h, B('dark_oak_slab') if False else slab(t.wood_slab), hollow=False)
    for x in range(cx - r0 - 1, cx + r0 + 2):
        for z in range(cz - r0 - 1, cz + r0 + 2):
            if (x - cx) ** 2 + (z - cz) ** 2 in range(int((r0 + 1) ** 2 - 2), int((r0 + 1) ** 2 + r0 + 1)) and (x, h, z) in v.b:
                v.s(x, h + 1, z, B('iron_bars'))
    v.disc(cx, cz, 2, h + 1, B('glass'), hollow=True); v.disc(cx, cz, 2, h + 2, B('glass'), hollow=True); v.disc(cx, cz, 2, h + 3, B('glass'), hollow=True)
    v.s(cx, h + 1, cz, B('sea_lantern')); v.s(cx, h + 2, cz, B('sea_lantern'))
    v.disc(cx, cz, 3, h + 4, B('red_concrete'))
    v.disc(cx, cz, 2, h + 5, B('red_concrete')); v.disc(cx, cz, 1, h + 6, B('red_concrete')); v.s(cx, h + 7, cz, B('lightning_rod'))
    return v

def windmill(t, h=14, r0=3, cap='spruce'):
    v = V(); cx = cz = r0 + 1
    for y in range(-3, 1): v.disc(cx, cz, r0 + 1, y, B(t.found))
    for y in range(1, h):
        rr = r0 if y < h * 0.45 else (r0 - 1 if y < h * 0.8 else r0 - 1)
        v.disc(cx, cz, rr, y, B(t.wall), hollow=True)
    for y in (1, h // 2, h - 1):
        v.disc(cx, cz, r0 - 1 if y > 1 else r0, y, B(t.floor))
    for x in (cx - r0, cx + r0):
        for y in range(1, h, 1):
            pass
    v.clear(cx, 1, cz + r0, cx, 2, cz + r0)
    v.s(cx, 1, cz + r0, door(t.door, 'south', 'lower')); v.s(cx, 2, cz + r0, door(t.door, 'south', 'upper'))
    for yy in (5, 9):
        for (dx, dz) in ((r0, 0), (-r0, 0), (0, -r0)):
            v.s(cx + dx, yy, cz + dz, B(t.glass))
    # Kuppeldach
    for i, rr in enumerate((r0 + 1, r0, r0 - 1, 1, 0)):
        v.disc(cx, cz, rr, h + i, B(t.roof_block)) if rr > 0 else v.s(cx, h + i, cz, B(t.roof_block))
    v.s(cx, h + 5, cz, B('lightning_rod'))
    # Flügel (an der Südseite, y=h-4)
    hy = h - 5; fz = cz + r0 + 1
    v.fill(cx, hy, cz + r0, cx, hy, fz, log(t.beam, 'z'))
    for k in range(1, 8):
        for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if k % 1 == 0:
                bx, by = cx + dx * k, hy + dy * k
                v.s(bx, by, fz, B(t.fence) if k < 2 else B(t.beam, axis='x' if dx else 'y'))
    for k in range(3, 8):
        for (dx, dy, ex, ey) in ((1, 0, 0, 1), (-1, 0, 0, -1), (0, 1, -1, 0), (0, -1, 1, 0)):
            bx, by = cx + dx * k, hy + dy * k
            v.s(bx + ex, by + ey, fz, B('white_wool')); v.s(bx + 2 * ex, by + 2 * ey, fz, B('white_wool')) if k > 3 else None
    return v

def greenhouse(t, w=9, l=11):
    v = V()
    v.fill(0, -2, 0, w - 1, -1, l - 1, B(t.found)); v.fill(0, 0, 0, w - 1, 0, l - 1, B(t.found2))
    v.walls(0, 1, 0, w - 1, 3, l - 1, B('glass'))
    for (x, z) in ((0, 0), (w - 1, 0), (0, l - 1), (w - 1, l - 1)):
        v.fill(x, 1, z, x, 3, z, log(t.log))
    for z in range(3, l - 1, 4):
        for x in (0, w - 1): v.fill(x, 1, z, x, 3, z, log(t.log))
    roof_gable(v, T(roof='oak', roof_block='glass', wall='glass'), 0, w - 1, 0, l - 1, 3, ridge='z', over=0, over_b=0, fill='glass') if False else None
    n = (w + 1) // 2
    for i in range(n):
        for z in range(0, l):
            v.s(i, 4 + i, z, B('glass')); v.s(w - 1 - i, 4 + i, z, B('glass'))
    for i in range(0, l, 4):
        for k in range(n):
            v.s(k, 4 + k, i, log(t.log, 'z') if False else B(t.fence)); v.s(w - 1 - k, 4 + k, i, B(t.fence))
    v.clear(w // 2, 1, l - 1, w // 2, 2, l - 1)
    v.s(w // 2, 1, l - 1, door(t.door, 'south', 'lower')); v.s(w // 2, 2, l - 1, door(t.door, 'south', 'upper'))
    for z in range(2, l - 3):
        for x in (1, 2, w - 3, w - 2):
            v.s(x, 0, z, B('grass_block')); v.s(x, 1, z, B(['wheat', 'carrots', 'potatoes', 'beetroots'][(x + z) % 4], age=7 if False else 3) if False else B(['poppy', 'dandelion', 'cornflower', 'oxeye_daisy'][(x + z) % 4]))
    v.fill(w // 2, 0, 2, w // 2, 0, l - 4, B('dirt_path'))
    v.s(w // 2, 4, 3, lantern(True)) if False else None
    return v
