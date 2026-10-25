from common import *
import math

# ============================================================== MODERN
MOD = T(log='black_concrete', beam='gray_concrete', wall='white_concrete', floor='light_gray_concrete',
        found='gray_concrete', found2='smooth_stone', found_stair='smooth_quartz', roof='stone', roof_block='stone',
        door='iron_door', trap='iron_trapdoor', fence='iron_bars', wood_slab='smooth_stone', wood_stair='quartz',
        hull='gray_concrete', hull2='gray_concrete', deck='smooth_stone', bedcolor='gray', rug='light_gray_carpet', glass='glass_pane', shutters=False)
Md = MOD

def mbox(v, x1, z1, x2, z2, y0, h, wall='white_concrete', glass='glass', front=True, side_glass=False, roof='smooth_stone_slab', accent='black_concrete', floor='light_gray_concrete', lights=True):
    """Moderner Kasten. Boden bei y0, Dach bei y0+h. Vorderseite = z2 (Süden)."""
    v.fill(x1, y0, z1, x2, y0, z2, B(floor))
    v.walls(x1, y0 + 1, z1, x2, y0 + h - 1, z2, B(wall))
    for x in range(x1, x2 + 1):
        if front and x1 < x < x2:
            for y in range(y0 + 1, y0 + h):
                v.s(x, y, z2, B(glass) if (x - x1) % 4 != 0 else B(accent))
    if side_glass:
        for z in range(z1 + 2, z2 - 1, 2):
            for y in range(y0 + 2, y0 + h - 1):
                v.s(x1, y, z, B(glass)); v.s(x2, y, z, B(glass))
    for (x, z) in ((x1, z1), (x2, z1), (x1, z2), (x2, z2)):
        v.fill(x, y0 + 1, z, x, y0 + h - 1, z, B(accent))
    v.fill(x1 - 1, y0 + h, z1 - 1, x2 + 1, y0 + h, z2 + 1, B(roof))
    v.fill(x1, y0 + h, z1, x2, y0 + h, z2, B('smooth_quartz') if False else B(wall))
    if lights:
        for x in range(x1 + 2, x2 - 1, 4):
            for z in range(z1 + 2, z2 - 1, 4):
                v.s(x, y0 + h - 1, z, B('sea_lantern'))

def mdoor(v, x, y, z, f='south'):
    v.clear(x, y, z, x, y + 1, z)
    v.s(x, y, z, door('iron_door', f, 'lower')); v.s(x, y + 1, z, door('iron_door', f, 'upper'))

def pool(v, x1, z1, x2, z2):
    v.fill(x1 - 1, -3, z1 - 1, x2 + 1, 0, z2 + 1, B('smooth_quartz'))
    v.fill(x1, -2, z1, x2, 0, z2, B('water', level=0)); v.fill(x1, -3, z1, x2, -3, z2, B('light_blue_concrete'))
    for x in range(x1 - 1, x2 + 2):
        for z in range(z1 - 1, z2 + 2):
            if x in (x1 - 1, x2 + 1) or z in (z1 - 1, z2 + 1): v.s(x, 0, z, B('smooth_quartz'))

def modern_house(w=11, l=9, upper=True, with_pool=True):
    v = V(); v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete'))
    mbox(v, 0, 0, w - 1, l - 1, 0, 4)
    mdoor(v, w // 2, 1, l - 1)
    if upper:
        mbox(v, 2, 1, w + 1, l + 1, 4, 4, wall='gray_concrete', accent='white_concrete', side_glass=True)
        v.fill(2, 3, l, 2, 3, l, B('black_concrete')) if False else None
        v.fill(w + 1, 0, l + 1, w + 1, 3, l + 1, B('black_concrete'))
        v.fill(2, 0, l + 1, 2, 3, l + 1, B('black_concrete'))
        v.fill(3, 5, 2, w, 5, 3, B('spruce_planks')) if False else None
        v.fill(3, 5, 2, 5, 5, 3, B('white_bed') if False else B('light_gray_carpet'))
        v.s(w, 5, 2, bed('white', 'north', 'foot')); v.s(w, 5, 1, bed('white', 'north', 'head'))
        v.fill(w - 2, 8, 1, w + 1, 8, l + 1, slab('smooth_stone', 'bottom')) if False else None
    v.fill(1, 1, 1, 3, 1, 3, B('light_gray_carpet')); v.s(w - 2, 1, 1, B('crafting_table')); v.s(w - 3, 1, 1, B('furnace', facing='south'))
    v.s(5, 1, 3, bed('gray', 'north', 'foot')) if False else None
    if with_pool:
        pool(v, 1, l + 2, w - 2, l + 5)
        v.fill(0, 0, l, w - 1, 0, l + 1, B('smooth_stone'))
    for x in (3, w - 4): v.s(x, 1, l, B('oak_leaves', persistent='true') if False else B('lantern', hanging='false')) if False else None
    return v

def modern_apartment(w=11, l=9, floors=4):
    v = V(); v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete'))
    for k in range(floors):
        mbox(v, 0, 0, w - 1, l - 1, k * 4, 4, wall='white_concrete' if k % 2 == 0 else 'light_gray_concrete', side_glass=True)
        # Balkone
        v.fill(1, k * 4, l, w - 2, k * 4, l + 1, B('smooth_quartz_slab') if False else slab('smooth_quartz'))
        for x in range(1, w - 1):
            v.s(x, k * 4 + 1, l + 1, B('glass_pane'))
        v.s(1, k * 4 + 1, l, B('glass_pane')); v.s(w - 2, k * 4 + 1, l, B('glass_pane'))
        v.clear(w // 2, k * 4 + 1, l - 1, w // 2, k * 4 + 2, l - 1)
        v.s(w // 2, k * 4 + 1, l - 1, door('iron_door', 'south', 'lower')); v.s(w // 2, k * 4 + 2, l - 1, door('iron_door', 'south', 'upper'))
    v.fill(-1, floors * 4, -1, w, floors * 4, l, slab('smooth_stone'))
    v.fill(2, floors * 4 + 1, 2, 4, floors * 4 + 2, 3, B('gray_concrete'))
    return v

def skyscraper(w=11, l=11, floors=9):
    v = V(); v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete'))
    v.fill(0, 0, 0, w - 1, 0, l - 1, B('smooth_stone'))
    for k in range(floors):
        y0 = k * 4
        v.fill(0, y0, 0, w - 1, y0, l - 1, B('light_gray_concrete'))
        for y in range(y0 + 1, y0 + 4):
            for x in range(w):
                for z in range(l):
                    if x in (0, w - 1) or z in (0, l - 1):
                        edge = (x in (0, w - 1)) and (z in (0, l - 1))
                        v.s(x, y, z, B('black_concrete') if edge or x % 3 == 0 and z in (0, l - 1) or z % 3 == 0 and x in (0, w - 1) else B('light_blue_stained_glass'))
        v.fill(0, y0 + 4, 0, w - 1, y0 + 4, l - 1, B('gray_concrete')) if k == floors - 1 else None
        for x in range(2, w - 2, 4):
            for z in range(2, l - 2, 4): v.s(x, y0 + 3, z, B('sea_lantern'))
    top = floors * 4
    v.fill(-1, top, -1, w, top, l, B('black_concrete'))
    v.fill(3, top + 1, 3, w - 4, top + 3, l - 4, B('gray_concrete'))
    v.fill(w // 2, top + 4, l // 2, w // 2, top + 12, l // 2, B('iron_bars'))
    v.s(w // 2, top + 13, l // 2, B('sea_lantern'))
    v.clear(w // 2 - 1, 1, l - 1, w // 2 + 1, 3, l - 1)
    v.s(w // 2, 1, l - 1, door('iron_door', 'south', 'lower')); v.s(w // 2, 2, l - 1, door('iron_door', 'south', 'upper'))
    v.s(w // 2 - 1, 1, l - 1, B('black_concrete')) if False else None
    return v

def modern_office():
    v = V(); w, l = 15, 11
    v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete'))
    for k in range(3):
        mbox(v, 0, 0, w - 1, l - 1, k * 4, 4, wall='white_concrete', side_glass=True)
    mdoor(v, w // 2, 1, l - 1); v.clear(w // 2 - 1, 1, l - 1, w // 2 - 1, 2, l - 1); v.s(w // 2 - 1, 1, l - 1, B('glass')); v.s(w // 2 - 1, 2, l - 1, B('glass'))
    for x in range(2, w - 2, 3):
        v.s(x, 1, 2, B('crafting_table') if False else B('smooth_stone_slab')); v.s(x, 2, 2, B('stone_pressure_plate')) if False else None
    v.fill(-1, 12, -1, w, 12, l, slab('gray_concrete')) if False else None
    return v

def modern_shop(w=13, l=9, col='orange'):
    v = V(); v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete'))
    mbox(v, 0, 0, w - 1, l - 1, 0, 5, wall='gray_concrete', accent=col + '_concrete', side_glass=True)
    mdoor(v, w // 2, 1, l - 1)
    for x in range(-1, w + 1):
        v.s(x, 4, l, B(col + '_concrete')); v.s(x, 4, l + 1, B(col + '_concrete'))
        v.s(x, 3, l + 1, B('black_concrete')) if x % 4 == 0 else None
    for x in range(2, w - 2, 2):
        v.s(x, 1, 2, B('smooth_stone_slab')) if False else v.s(x, 1, 2, B('barrel', facing='up')); v.s(x, 1, 5, B('quartz_slab') if False else slab('quartz', 'top'))
    return v

def modern_cafe():
    v = modern_shop(11, 9, 'red')
    for (x, z) in ((2, 11), (5, 11), (8, 11)):
        v.s(x, 0, z, B('smooth_quartz')) if False else None
        v.s(x, 1, z, B('iron_bars')); v.s(x, 2, z, B('white_carpet')); v.s(x - 1, 1, z, stair('quartz', 'east')); v.s(x + 1, 1, z, stair('quartz', 'west'))
    v.fill(-1, 0, 10, 11, 0, 12, B('smooth_stone'))
    for (x, z) in ((2, 11), (5, 11), (8, 11)):
        v.s(x, 1, z, B('iron_bars')); v.s(x, 2, z, B('white_carpet'))
    return v

def modern_garage(w=9, l=8):
    v = V(); v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete'))
    mbox(v, 0, 0, w - 1, l - 1, 0, 5, wall='gray_concrete', front=False, accent='black_concrete', lights=True)
    v.clear(1, 1, l - 1, w - 2, 3, l - 1)
    for x in range(1, w - 1):
        for y in range(1, 4): v.s(x, y, l - 1, B('light_gray_concrete') if y % 2 == 0 else B('white_concrete'))
    v.s(w // 2, 3, l, B('sea_lantern')) if False else None
    v.fill(0, 0, l, w - 1, 0, l + 3, B('light_gray_concrete')); v.fill(0, -3, l, w - 1, -1, l + 3, B('gray_concrete'))
    v.s(1, 1, 1, B('anvil', facing='east')) if False else None
    v.s(w - 2, 1, 1, B('barrel', facing='up')); v.s(w - 2, 1, 2, chest('west')); v.s(w - 2, 1, 3, B('smithing_table'))
    return v

def gas_station():
    v = V(); w, l = 13, 11
    v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete')); v.fill(0, 0, 0, w - 1, 0, l - 1, B('light_gray_concrete'))
    mbox(v, 0, 0, 6, 4, 0, 4, wall='white_concrete', accent='red_concrete', side_glass=True)
    mdoor(v, 3, 1, 4)
    for x in (7, 12):
        for z in (6, 10): v.fill(x, 1, z, x, 4, z, B('white_concrete'))
    v.fill(6, 5, 5, 13, 5, 11, B('red_concrete')); v.fill(7, 5, 6, 12, 5, 10, B('white_concrete')); v.fill(6, 6, 5, 13, 6, 11, slab('white_concrete')) if False else None
    for x in (8, 11):
        v.s(x, 1, 8, B('gray_concrete')); v.s(x, 2, 8, B('gray_concrete')); v.s(x, 3, 8, B('light_gray_concrete')) if False else None
        v.s(x, 3, 8, B('red_concrete'))
    for x in range(7, 13, 1): v.s(x, 4, 6, B('sea_lantern')) if x % 2 else None
    return v

def modern_hall():
    v = V(); w, l = 17, 11
    v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete'))
    mbox(v, 0, 0, w - 1, l - 1, 0, 6, wall='white_concrete', side_glass=True, accent='quartz_pillar' if False else 'smooth_quartz')
    mbox(v, 3, 1, w - 4, l - 2, 6, 5, wall='gray_concrete', side_glass=True)
    mdoor(v, w // 2, 1, l - 1)
    for x in range(1, w - 1, 3):
        v.fill(x, 0, l, x, 5, l, B('quartz_pillar', axis='y'))
    v.fill(0, 6, l, w - 1, 6, l + 1, slab('smooth_quartz')) 
    v.fill(0, 0, l + 1, w - 1, 0, l + 3, B('smooth_stone'))
    for x in range(0, w, 5): v.s(x, 7, l, B('white_concrete')) if False else None
    v.s(w // 2, 12, 5, B('iron_bars')) if False else None
    v.fill(w // 2, 12, 5, w // 2, 18, 5, B('iron_bars')); v.s(w // 2, 19, 5, B('sea_lantern'))
    return v

def glass_pavilion():
    v = V(); w, l = 11, 11
    v.fill(0, -3, 0, w - 1, -1, l - 1, B('gray_concrete')); v.fill(0, 0, 0, w - 1, 0, l - 1, B('smooth_quartz'))
    v.walls(0, 1, 0, w - 1, 4, l - 1, B('glass'))
    for (x, z) in ((0, 0), (w - 1, 0), (0, l - 1), (w - 1, l - 1), (5, 0), (5, l - 1), (0, 5), (w - 1, 5)): v.fill(x, 1, z, x, 4, z, B('black_concrete'))
    v.fill(-1, 5, -1, w, 5, l, slab('black_concrete'))
    v.clear(5, 1, l - 1, 5, 2, l - 1); v.s(5, 1, l - 1, door('iron_door', 'south', 'lower')); v.s(5, 2, l - 1, door('iron_door', 'south', 'upper'))
    for (x, z) in ((2, 2), (8, 2)): v.s(x, 1, z, B('oak_leaves', persistent='true')); v.s(x, 0, z, B('dirt')) 
    v.s(5, 1, 4, B('quartz_slab', type='top')) if False else None
    v.s(4, 1, 4, stair('quartz', 'east')); v.s(6, 1, 4, stair('quartz', 'west')); v.s(5, 1, 4, B('iron_bars')); v.s(5, 2, 4, B('white_carpet'))
    return v

MOD_BUILDS = [
    ('villa_small', 'Moderne Villa', 'Villa mit Glasfront und Pool', 'WHITE_CONCRETE', lambda: modern_house(11, 9, True, True)),
    ('villa_big', 'Große Villa', 'Breite Villa mit Obergeschoss', 'LIGHT_GRAY_CONCRETE', lambda: modern_house(15, 11, True, True)),
    ('house_flat', 'Bungalow', 'Eingeschossiges Haus mit Pool', 'GLASS', lambda: modern_house(11, 9, False, True)),
    ('apartment', 'Wohnhaus', 'Vierstöckiges Apartmenthaus mit Balkonen', 'IRON_DOOR', lambda: modern_apartment(11, 9, 4)),
    ('apartment_tall', 'Wohnturm', 'Sechsstöckiges Wohnhaus', 'GRAY_CONCRETE', lambda: modern_apartment(9, 9, 6)),
    ('skyscraper', 'Wolkenkratzer', 'Glas-Hochhaus mit Antenne', 'LIGHT_BLUE_STAINED_GLASS', lambda: skyscraper(11, 11, 9)),
    ('office', 'Bürogebäude', 'Dreistöckiges Büro', 'WHITE_CONCRETE', modern_office),
    ('shop', 'Laden', 'Moderner Laden mit Markise', 'EMERALD', lambda: modern_shop(13, 9, 'orange')),
    ('cafe', 'Café', 'Café mit Terrasse', 'CAKE', modern_cafe),
    ('garage', 'Garage', 'Garage mit Werkstatt', 'MINECART', modern_garage),
    ('gas', 'Tankstelle', 'Tankstelle mit Dach', 'FURNACE', gas_station),
    ('town_hall', 'Rathaus', 'Modernes Rathaus mit Säulen', 'BELL', modern_hall),
    ('pavilion', 'Glaspavillon', 'Pavillon aus Glas', 'GLASS_PANE', glass_pavilion),
    ('stall', 'Marktstand', 'Moderner Stand', 'HAY_BLOCK', lambda: stall(Md, ('light_blue', 'white'))),
]

# ============================================================== WILD WEST
WEST = T(log='dark_oak_log', beam='stripped_dark_oak_log', wall='acacia_planks', floor='spruce_planks',
         found='sandstone', found2='smooth_sandstone', found_stair='sandstone', roof='spruce', roof_block='spruce_planks',
         door='spruce_door', trap='spruce_trapdoor', fence='spruce_fence', wood_slab='spruce', wood_stair='spruce',
         hull='spruce_planks', hull2='spruce_planks', deck='spruce_planks', bedcolor='red', rug='brown_carpet', shutters=True)
Wt = WEST

def west_front(w, l, floors=2, porch=True, deco='saloon', balcony=True, wall=None):
    t = Wt
    v = house(t, w, l, floors=floors, roof='none', door_col=w // 2, chimney=False, windows=True, lamp=True, walls_blk=wall)
    top = floors * 4
    roof_flat(v, t, 0, w - 1, 0, l - 1, top, over=0, parapet=False)
    # Falsche Fassade
    v.fill(0, top + 1, l - 1, w - 1, top + 3, l - 1, B(wall or t.wall))
    v.fill(0, top + 1, l - 1, 0, top + 3, l - 1, log(t.log)); v.fill(w - 1, top + 1, l - 1, w - 1, top + 3, l - 1, log(t.log))
    c = w // 2
    for dx in range(-2, 3):
        v.s(c + dx, top + 4, l - 1, stair('spruce', 'south') if abs(dx) == 2 else B('spruce_planks'))
    v.s(c, top + 5, l - 1, slab('spruce')) 
    v.fill(1, top + 1, l - 1, w - 2, top + 1, l - 1, log(t.beam, 'x'))
    # Schildbrett (Schriftzug-Ersatz)
    for dx in range(-2, 3): v.s(c + dx, top + 2, l, B('spruce_planks') if False else trap(t.trap, 'south', 'top', True) if False else B('stripped_spruce_log', axis='x'))
    # Überdachter Gehweg
    if porch:
        pd = 4
        v.fill(0, 0, l, w - 1, 0, l + pd - 1, B(t.floor)); v.fill(0, -2, l, w - 1, -1, l + pd - 1, B(t.found))
        for x in range(0, w, 3):
            v.fill(x, 1, l + pd - 1, x, 3, l + pd - 1, B(t.fence))
        v.fill(0, 4, l, w - 1, 4, l + pd - 1, slab(t.wood_slab, 'bottom'))
        v.fill(0, 3, l + pd - 1, w - 1, 3, l + pd - 1, B(t.fence)) if False else None
        for x in range(1, w, 3): v.s(x, 3, l + pd - 1, lantern(True))
        if balcony and floors > 1:
            v.fill(0, 4, l, w - 1, 4, l + pd - 1, B(t.floor))
            for x in range(0, w): v.s(x, 5, l + pd - 1, B(t.fence))
            for z in range(l, l + pd): v.s(0, 5, z, B(t.fence)); v.s(w - 1, 5, z, B(t.fence))
            v.clear(c, 5, l - 1, c, 6, l - 1); v.s(c, 5, l - 1, door(t.door, 'south', 'lower')); v.s(c, 6, l - 1, door(t.door, 'south', 'upper'))
    # Haltebalken
    v.fill(1, 1, l + 5, w - 2, 1, l + 5, B(t.fence)) if False else None
    for x in (2, w - 3):
        v.s(x, 1, l + 5, B(t.fence)); v.s(x, 2, l + 5, B(t.fence)) if False else None
    v.fill(2, 2, l + 5, w - 3, 2, l + 5, B(t.fence)) if False else None
    v.s(1 if False else 3, 0, l + 4, B('coarse_dirt')) if False else None
    return v

def saloon():
    v = west_front(13, 10, 2, True, 'saloon')
    w, l = 13, 10
    for x in range(2, w - 3):
        v.s(x, 1, 2, stair('spruce', 'south', 'top'))
    for x in range(2, w - 3): v.s(x, 1, 1, B('barrel', facing='up'))
    v.s(w - 3, 1, 2, B('note_block'))
    for x in (3, 6): v.s(x, 1, 6, B('spruce_fence')); v.s(x, 2, 6, B('stone_pressure_plate')); v.s(x - 1, 1, 6, stair('spruce', 'east')); v.s(x + 1, 1, 6, stair('spruce', 'west'))
    # Schwingtüren
    c = w // 2
    v.clear(c, 1, l - 1, c, 2, l - 1)
    v.s(c, 1, l - 1, trap('spruce_trapdoor', 'south', 'bottom', True) if False else B('spruce_fence_gate', facing='south', open='true', in_wall='false', powered='false'))
    v.s(c, 2, l - 1, B('spruce_fence_gate', facing='south', open='true', in_wall='false', powered='false')) if False else None
    return v

def sheriff():
    v = west_front(11, 9, 1, True, 'sheriff')
    for z in range(1, 7): v.s(5, 1, z, B('iron_bars')); v.s(5, 2, z, B('iron_bars')); v.s(5, 3, z, B('iron_bars'))
    v.s(8, 1, 1, bed('white', 'south', 'head')); v.s(8, 1, 2, bed('white', 'south', 'foot')); v.s(2, 1, 2, B('crafting_table'))
    v.s(3, 1, 5, B('lectern', facing='south')); v.s(2, 1, 5, B('barrel', facing='up'))
    v.s(4, 3, 8, banner('yellow', 'south')) if False else None
    return v

def general_store(): 
    v = west_front(11, 9, 1, True, 'store')
    for x in range(2, 9, 2): v.s(x, 1, 2, B('barrel', facing='up')); v.s(x, 1, 1, chest('south'))
    v.s(9, 1, 5, B('hay_block', axis='y')); v.s(9, 2, 5, B('hay_block', axis='y'))
    return v

def bank():
    t = Wt
    v = west_front(11, 9, 1, True, 'bank', wall='stone_bricks')
    for z in range(1, 4):
        for x in (1, 2, 3): v.s(x, 1, z, chest('south')) if False else None
    v.fill(1, 1, 1, 4, 3, 1, B('iron_bars')) if False else None
    v.s(2, 1, 2, B('gold_block')); v.s(3, 1, 2, B('gold_block')); v.s(2, 2, 2, B('gold_block'))
    for z in (1, 2, 3, 4):
        v.s(5, 1, z, B('iron_bars')); v.s(5, 2, z, B('iron_bars')); v.s(5, 3, z, B('iron_bars'))
    for x in (1, 2, 3, 4): v.s(x, 1, 4, B('iron_bars')); v.s(x, 2, 4, B('iron_bars')) if False else None
    v.s(8, 1, 3, B('lectern', facing='south')); v.s(7, 1, 3, B('barrel', facing='up'))
    return v

def hotel():
    v = west_front(15, 11, 3, True, 'hotel')
    for k in range(3):
        for x in (2, 12):
            v.s(x, k * 4 + 1, 8, bed('red', 'north', 'foot')); v.s(x, k * 4 + 1, 7, bed('red', 'north', 'head'))
    return v

def west_smithy():
    t = Wt
    v = smithy(t)
    return v

def homestead():
    v = house(Wt, 9, 7, floors=1, ridge='x', porch=True, chimney=True)
    v.s(0, 1, 11, B('cactus')) if False else None
    for (x, z) in ((-2, 3), (11, 6)): v.s(x, 0, z, B('sand')); v.s(x, 1, z, B('cactus')); v.s(x, 2, z, B('cactus'))
    return v

def west_church():
    t = T(**{**Wt.__dict__, 'wall': 'white_concrete', 'roof': 'spruce', 'timber': False})
    v = chapel(t, 7, 13, 14)
    return v

def water_tower():
    v = V(); n = 7
    for (x, z) in ((0, 0), (n - 1, 0), (0, n - 1), (n - 1, n - 1)):
        v.fill(x, -3, z, x, 11, z, log('dark_oak_log'))
    for y in (3, 7):
        v.fill(0, y, 0, n - 1, y, 0, log('stripped_dark_oak_log', 'x')); v.fill(0, y, n - 1, n - 1, y, n - 1, log('stripped_dark_oak_log', 'x'))
        v.fill(0, y, 0, 0, y, n - 1, log('stripped_dark_oak_log', 'z')); v.fill(n - 1, y, 0, n - 1, y, n - 1, log('stripped_dark_oak_log', 'z'))
    # Tank
    for y in range(12, 18):
        v.walls(0, y, 0, n - 1, y, n - 1, B('spruce_planks'))
    v.fill(1, 12, 1, n - 2, 12, n - 2, B('spruce_planks')); v.fill(1, 13, 1, n - 2, 16, n - 2, B('water', level=0))
    v.fill(1, 17, 1, n - 2, 17, n - 2, B('spruce_planks'))
    for yy in (13, 15): 
        v.fill(0, yy, 0, n - 1, yy, 0, log('stripped_dark_oak_log', 'x')); v.fill(0, yy, n - 1, n - 1, yy, n - 1, log('stripped_dark_oak_log', 'x'))
    roof_hip(v, Wt, 0, n - 1, 0, n - 1, 17, over=0)
    for y in range(-2, 12): v.s(1, y, 1, B('ladder', facing='south')) if False else None
    for y in range(0, 12): v.s(3, y, n, B('ladder', facing='north')) if False else None
    for y in range(1, 17): v.s(3, y, n, B('ladder', facing='north')) if False else None
    for y in range(1, 17):
        v.s(3, y, n, B('ladder', facing='north'))
        v.s(3, y, n - 1, B('spruce_planks')) if y < 12 else None
    v.fill(0, 0, 0, n - 1, 0, n - 1, B('coarse_dirt')) if False else None
    return v

def red_barn():
    t = T(**{**Wt.__dict__, 'wall': 'red_terracotta'})
    v = warehouse(t, 9, 13)
    return v

WEST_BUILDS = [
    ('saloon', 'Saloon', 'Saloon mit Tresen und Balkon', 'BARREL', saloon),
    ('sheriff', 'Sheriff-Büro', 'Büro mit Gefängniszelle', 'IRON_BARS', sheriff),
    ('general_store', 'Gemischtwarenladen', 'Laden mit Vorräten', 'EMERALD', general_store),
    ('bank', 'Bank', 'Bank mit Tresor', 'GOLD_INGOT', bank),
    ('hotel', 'Hotel', 'Dreistöckiges Hotel', 'RED_BED', hotel),
    ('smithy', 'Schmiede', 'Schmiede mit Anbau', 'ANVIL', west_smithy),
    ('homestead', 'Farmhaus', 'Haus mit Veranda und Kakteen', 'SPRUCE_DOOR', homestead),
    ('house_two', 'Stadthaus', 'Zweistöckiges Holzhaus', 'ACACIA_PLANKS', lambda: house(Wt, 9, 8, floors=2, ridge='x', balcony=True, porch=True)),
    ('church', 'Westernkirche', 'Weiße Holzkirche mit Turm', 'BELL', west_church),
    ('water_tower', 'Wasserturm', 'Wasserturm auf Stelzen', 'WATER_BUCKET', water_tower),
    ('barn', 'Rote Scheune', 'Ranch-Scheune', 'HAY_BLOCK', red_barn),
    ('stable', 'Pferdestall', 'Stall mit Boxen', 'SADDLE', lambda: stable(Wt)),
    ('stall', 'Marktstand', 'Marktstand', 'HAY_BLOCK', lambda: stall(Wt, ('red', 'white'))),
    ('well', 'Ranchbrunnen', 'Brunnen', 'WATER_BUCKET', lambda: well(Wt)),
]

# ============================================================== ASIATISCH
AS = T(log='dark_oak_log', beam='stripped_dark_oak_log', wall='white_terracotta', floor='spruce_planks',
       found='stone_bricks', found2='polished_andesite', found_stair='stone_brick', roof='deepslate_tile', roof_block='deepslate_tiles',
       door='jungle_door', trap='jungle_trapdoor', fence='dark_oak_fence', wood_slab='dark_oak', wood_stair='dark_oak',
       hull='dark_oak_planks', hull2='spruce_planks', deck='spruce_planks', bedcolor='red', rug='red_carpet', glass='white_stained_glass_pane',
       timber=True, shutters=False)
A = AS

def asia_house(w, l, floors=1, over=2):
    v = house(A, w, l, floors=floors, roof='hip', over=over, chimney=False, door_col=w // 2)
    return v

def pagoda(tiers=5, base=11):
    v = V(); y0 = 0
    v.fill(-2, -3, -2, base + 1, -1, base + 1, B(A.found)); v.fill(-2, 0, -2, base + 1, 0, base + 1, B(A.found2))
    for i in range(tiers):
        n = base - 2 * i
        x1 = i; x2 = i + n - 1
        for (x, z) in ((x1, x1), (x2, x1), (x1, x2), (x2, x2)):
            v.fill(x, y0 + 1, z, x, y0 + 4, z, B('red_concrete') if False else log(A.log))
        v.walls(x1, y0 + 1, x1, x2, y0 + 3, x2, B(A.wall))
        v.fill(x1, y0, x1, x2, y0, x2, B(A.floor)) if i else None
        v.walls(x1, y0 + 4, x1, x2, y0 + 4, x2, log(A.beam, 'x'))
        for x in range(x1 + 1, x2, 2):
            for (xx, zz) in ((x, x1), (x, x2), (x1, x), (x2, x)):
                v.s(xx, y0 + 2, zz, B(A.glass))
        if i == 0:
            c = (x1 + x2) // 2
            v.clear(c, 1, x2, c, 2, x2); v.s(c, 1, x2, door(A.door, 'south', 'lower')); v.s(c, 2, x2, door(A.door, 'south', 'upper'))
        n_l = roof_hip(v, A, x1, x2, x1, x2, y0 + 4, over=2)
        v.s((x1 + x2) // 2, y0 + 4 + n_l + 1, (x1 + x2) // 2, lantern(False)) if False else None
        y0 = y0 + 4 + n_l
        # Hängelaternen an den Ecken
        for (x, z) in ((x1 - 2, x1 - 2), (x2 + 2, x1 - 2), (x1 - 2, x2 + 2), (x2 + 2, x2 + 2)):
            v.s(x, y0 - n_l + 3 if False else y0 - n_l + 3, z, lantern(True)) if False else None
    c = (base - 1) // 2
    v.fill(c, y0, c, c, y0 + 3, c, B('iron_bars')); v.s(c, y0 + 4, c, B('lightning_rod'))
    return v

def torii(w=9, h=8):
    v = V()
    v.fill(0, -2, 0, w - 1, -1, 2, B(A.found))
    for x in (1, w - 2):
        v.fill(x, 0, 1, x, h - 1, 1, B('red_concrete')); v.fill(x - 0, 0, 1, x, 0, 1, B('black_concrete'))
    v.fill(0, h, 0, w - 1, h, 2, B('black_concrete'))
    v.fill(0, h + 1, 0, w - 1, h + 1, 2, slab('black_concrete')) if False else None
    for x in (0, w - 1): v.s(x, h + 1, 1, stair('dark_oak', 'east' if x == 0 else 'west')) if False else v.s(x, h + 1, 1, slab('dark_oak'))
    v.fill(0, h + 1, 1, w - 1, h + 1, 1, B('black_concrete')) if False else None
    v.fill(1, h + 1, 1, w - 2, h + 1, 1, B('red_concrete'))
    v.fill(0, h - 2, 1, w - 1, h - 2, 1, B('red_concrete'))
    v.fill(0, h + 1, 0, w - 1, h + 1, 2, slab('black_concrete'))
    v.s(w // 2, h - 1, 1, B('dark_oak_planks')) if False else None
    for x in (3, w - 4): v.s(x, h - 3, 1, lantern(True)) if False else None
    v.fill(w // 2, 0, 0, w // 2, 0, 2, B('stone_bricks')) if False else None
    return v

def tea_house(n=9):
    v = V()
    v.fill(-1, -2, -1, n, -1, n, B(A.found)); v.fill(0, 0, 0, n - 1, 0, n - 1, B('spruce_planks'))
    v.fill(0, 1, 0, n - 1, 1, n - 1, B('green_carpet') if False else B('air')) if False else None
    for (x, z) in ((0, 0), (n - 1, 0), (0, n - 1), (n - 1, n - 1), (n // 2, 0), (0, n // 2), (n - 1, n // 2)):
        v.fill(x, 1, z, x, 3, z, log(A.log))
    v.walls(0, 4, 0, n - 1, 4, n - 1, log(A.beam, 'x'))
    for z in range(1, n - 1):
        v.s(0, 2, z, B(A.glass)) if z != n // 2 else None; v.s(n - 1, 2, z, B(A.glass)) if z != n // 2 else None
    for x in range(1, n - 1):
        v.s(x, 2, 0, B(A.glass)) if x != n // 2 else None
    roof_hip(v, A, 0, n - 1, 0, n - 1, 4, over=2)
    v.fill(2, 1, 2, n - 3, 1, n - 3, B('lime_carpet') if False else B('green_carpet'))
    for (x, z) in ((3, 4), (n - 4, 4)): v.s(x, 1, z, B('spruce_fence')) if False else v.s(x, 1, z, slab('dark_oak', 'bottom'))
    v.s(n // 2, 3, n // 2, lantern(True)); v.s(n // 2, 1, n // 2 + 1, B('campfire', lit='false', signal_fire='false')) if False else None
    v.s(n // 2, 1, n // 2, B('cauldron')) if False else v.s(n // 2, 1, n // 2, B('dark_oak_pressure_plate'))
    for x in (n // 2 - 2, n // 2 + 2): v.s(x, 1, n // 2, B('red_carpet'))
    # Steintreppe
    v.s(n // 2, 0, n, stair('stone_brick', 'south')); v.s(n // 2, -1, n, B(A.found))
    v.s(n // 2 - 1, 1, n, B('stone_brick_wall')) if False else None
    return v

def dojo():
    v = house(A, 13, 9, floors=1, roof='hip', over=2, chimney=False, door_col=6)
    v.fill(2, 0, 2, 10, 0, 6, B('birch_planks') if False else B('stripped_birch_log') if False else B('birch_planks'))
    for x in (2, 5, 8, 10): v.s(x, 1, 1, B('barrel', facing='up')) if False else None
    v.s(6, 1, 1, B('lectern', facing='south')) if False else None
    for x in range(1, 12, 2): v.s(x, 1, 1, B('red_carpet'))
    return v

def shrine():
    v = V()
    v.fill(-2, -3, -2, 14, -1, 18, B(A.found)); v.fill(-2, 0, -2, 14, 0, 18, B('gravel') if False else B('polished_andesite'))
    s = house(A, 7, 7, floors=1, roof='hip', over=2, chimney=False, door_col=3)
    v.paste(s, 3, 0, 0)
    v.fill(6, 0, 7, 6, 0, 18, B('stone_bricks'))
    t = torii(7, 7); v.paste(t, 3, 0, 15)
    for (x, z) in ((4, 10), (8, 10), (4, 13), (8, 13)):
        v.s(x, 1, z, B('stone_brick_wall')); v.s(x, 2, z, B('stone_brick_wall')); v.s(x, 3, z, B('lantern', hanging='false'))
    return v

def pagoda_castle():
    v = V(); base = 15
    v.fill(-1, -3, -1, base, -1, base, B(A.found)); 
    v.fill(0, 0, 0, base - 1, 6, base - 1, B('stone_bricks'))
    v.clear(1, 1, 1, base - 2, 6, base - 2)
    v.fill(0, 7, 0, base - 1, 7, base - 1, B('stone_bricks'))
    v.clear(7, 1, base - 1, 7, 3, base - 1)
    v.s(7, 1, base - 1, door(A.door, 'south', 'lower')); v.s(7, 2, base - 1, door(A.door, 'south', 'upper'))
    for i in range(1, 15, 2): pass
    p = pagoda(4, 11)
    p.clear(-2, -3, -2, 12, 0, 12)
    v.paste(p, 2, 7, 2)
    return v

def castle_gate():
    v = V(); w = 15
    v.fill(0, -3, 0, w - 1, -1, 4, B(A.found)); v.fill(0, 0, 0, w - 1, 6, 4, B('stone_bricks'))
    v.clear(5, 1, 0, 9, 5, 4); v.fill(5, 0, 0, 9, 0, 4, B('polished_andesite'))
    v.fill(0, 7, 0, w - 1, 7, 4, B('stone_bricks'))
    g = house(A, 11, 5, floors=1, roof='hip', over=2, chimney=False, windows=True)
    g.clear(0, -3, 0, 10, -1, 4)
    v.paste(g, 2, 7, 0)
    return v

def arch_bridge(l=17, w=5):
    v = V()
    mid = l // 2
    for z in range(l):
        h = round(3 * math.sin(math.pi * z / (l - 1)))
        for x in range(w):
            v.s(x, h, z, B('dark_oak_planks') if z % 2 else B('spruce_planks'))
            for yy in range(0, h): v.s(x, yy, z, B('dark_oak_planks')) if x in (0, w - 1) and False else None
        for x in (0, w - 1):
            v.s(x, h + 1, z, B('red_concrete') if z % 4 == 0 else B('dark_oak_fence'))
            if z % 4 == 0: v.s(x, h + 2, z, lantern(False))
    for z in range(l):
        h = round(3 * math.sin(math.pi * z / (l - 1)))
        for x in (0, w - 1):
            for yy in range(-1, h): v.s(x, yy, z, B('dark_oak_planks')) if yy >= h - 1 else None
    for z in (3, l - 4):
        for x in (0, w - 1): v.fill(x, -3, z, x, 0, z, log('dark_oak_log'))
    return v

def zen_garden():
    v = V(); n = 13
    v.fill(0, -2, 0, n - 1, -1, n - 1, B('dirt')); v.fill(0, 0, 0, n - 1, 0, n - 1, B('sand'))
    for x in range(0, n, 2):
        for z in range(0, n): v.s(x, 0, z, B('sandstone') if z % 2 and False else B('sand'))
    for (x, z) in ((3, 3), (9, 4), (5, 9)):
        v.s(x, 1, z, B('andesite')); v.s(x + 1, 1, z, B('stone')) if False else None
    v.fill(8, -1, 8, 11, 0, 11, B('water', level=0)) if False else None
    v.fill(8, 0, 8, 11, 0, 11, B('water', level=0)); v.fill(7, 0, 7, 12, 0, 7, B('stone_bricks')) if False else None
    v.fill(8, -1, 8, 11, -1, 11, B('light_blue_concrete')) if False else None
    tree(v, 2, 10, 4, 'cherry_log', 'cherry_leaves', 3)
    for x in (1, 11): v.s(x, 1, 1, B('stone_brick_wall')); v.s(x, 2, 1, B('stone_brick_wall')); v.s(x, 3, 1, B('lantern', hanging='false'))
    for z in (5,): 
        for k in range(4): v.fill(11, 1, 1 + k, 11, 1 + 3 + k, 1 + k, B('bamboo', age=1, leaves='large', stage=0)) if False else None
    for k, h in enumerate((4, 6, 5)):
        v.fill(10 + 0, 1, 2 + k, 10, h, 2 + k, B('bamboo', age=1, leaves='none', stage=0)) if False else None
    for k, h in enumerate((4, 6, 5)):
        v.fill(11, 1, 3 + k * 2, 11, h, 3 + k * 2, B('dark_oak_fence') if False else log('stripped_dark_oak_log'))
    return v

ASIA_BUILDS = [
    ('house_small', 'Reishaus', 'Kleines Haus mit Walmdach', 'JUNGLE_DOOR', lambda: asia_house(7, 7)),
    ('house_medium', 'Samuraihaus', 'Mittleres Haus', 'DARK_OAK_STAIRS', lambda: asia_house(9, 9)),
    ('house_two', 'Händlerhaus', 'Zweistöckiges Haus', 'DEEPSLATE_TILES', lambda: asia_house(9, 7, 2)),
    ('pagoda', 'Pagode', 'Fünfstöckige Pagode', 'LIGHTNING_ROD', lambda: pagoda(5, 11)),
    ('pagoda_small', 'Kleine Pagode', 'Dreistöckige Pagode', 'LANTERN', lambda: pagoda(3, 7)),
    ('torii', 'Torii', 'Rotes Tor', 'RED_CONCRETE', torii),
    ('tea_house', 'Teehaus', 'Offenes Teehaus', 'GREEN_CARPET', tea_house),
    ('dojo', 'Dojo', 'Trainingshalle', 'IRON_SWORD', dojo),
    ('shrine', 'Schrein', 'Schrein mit Torii und Laternen', 'BELL', shrine),
    ('castle', 'Burg', 'Burg mit Pagodenturm', 'SHIELD', pagoda_castle),
    ('gate', 'Burgtor', 'Tor mit Torhaus', 'IRON_BARS', castle_gate),
    ('bridge', 'Bogenbrücke', 'Rote Bogenbrücke', 'DARK_OAK_PLANKS', arch_bridge),
    ('garden', 'Zen-Garten', 'Garten mit Kirschbaum und Teich', 'CHERRY_SAPLING', zen_garden),
    ('stall', 'Marktstand', 'Stand mit Laternen', 'HAY_BLOCK', lambda: stall(A, ('red', 'white'))),
]

# ============================================================== FANTASY
FAN = T(log='birch_log', beam='stripped_birch_log', wall='birch_planks', floor='birch_planks',
        found='mossy_stone_bricks', found2='mossy_cobblestone', found_stair='mossy_stone_brick', roof='warped', roof_block='warped_planks',
        door='warped_door', trap='warped_trapdoor', fence='birch_fence', wood_slab='birch', wood_stair='birch',
        hull='birch_planks', hull2='birch_planks', deck='birch_planks', bedcolor='purple', rug='purple_carpet', glass='light_blue_stained_glass_pane', timber=True)
F = FAN

def sphere_dome(v, cx, cy, cz, r, blk, spots=None, hollow=True):
    for x in range(-r, r + 1):
        for y in range(0, r + 1):
            for z in range(-r, r + 1):
                d = x * x + y * y + z * z
                if d <= r * r + r and (not hollow or d >= (r - 1) ** 2):
                    b = blk
                    if spots and (x * 3 + y * 5 + z * 7) % 11 == 0 and y > 0: b = spots
                    v.s(cx + x, cy + y, cz + z, b)

def mushroom(cap='red_mushroom_block', r=5):
    v = V(); cx = cz = r + 1
    v.fill(0, -3, 0, 2 * r + 2, -1, 2 * r + 2, B('podzol'))
    for y in range(0, 5):
        v.disc(cx, cz, 3, y, B('mushroom_stem'), hollow=True)
    v.disc(cx, cz, 3, 0, B('oak_planks'))
    v.clear(cx, 1, cz + 3, cx, 2, cz + 3); v.s(cx, 1, cz + 3, door('oak_door', 'south', 'lower')); v.s(cx, 2, cz + 3, door('oak_door', 'south', 'upper'))
    for (dx, dz) in ((3, 0), (-3, 0), (0, -3)): v.s(cx + dx, 2, cz + dz, B('glass_pane'))
    sphere_dome(v, cx, 5, cz, r, B(cap), B('mushroom_stem') if cap.startswith('red') else B('brown_mushroom_block'))
    v.s(cx, 2, cz, B('crafting_table')); v.s(cx + 2, 1, cz, bed('red', 'west', 'foot')); v.s(cx + 1, 1, cz, bed('red', 'west', 'head')) if False else None
    v.s(cx, 4, cz, lantern(True)) if False else v.s(cx, 4, cz, B('shroomlight'))
    return v

def wizard_tower(h=20):
    v = V(); r = 3; c = 4
    for y in range(-3, 1): v.disc(c, c, 4, y, B(F.found))
    for y in range(1, h):
        rr = r if y < h * 0.75 else r + 1
        v.disc(c, c, rr, y, B('white_concrete') if y % 6 else B('purple_concrete'), hollow=True)
    for y in range(5, h, 5):
        v.disc(c, c, r - 1, y, B('birch_planks')); v.clear(c - 1, y, c - 1, c - 1, y, c - 1)
        for q in range(y - 4, y + 1): v.s(c - 1, q, c - 1, B('ladder', facing='east'))
    v.clear(c, 1, c + r, c, 2, c + r); v.s(c, 1, c + r, door('warped_door', 'south', 'lower')); v.s(c, 2, c + r, door('warped_door', 'south', 'upper'))
    for yy in range(4, h, 5):
        for (dx, dz) in ((r, 0), (-r, 0), (0, -r)): v.s(c + dx, yy, c + dz, B('light_blue_stained_glass')); v.s(c + dx, yy + 1, c + dz, B('light_blue_stained_glass'))
    v.disc(c, c, 5, h - 1, B('purple_concrete'))
    v.disc(c, c, 4, h, B('purple_terracotta')) 
    for i, rr in enumerate((4, 3, 3, 2, 2, 1, 1)):
        v.disc(c, c, rr, h + 1 + i, B('purple_concrete'), hollow=(i < 3 and rr > 1) and False)
    v.s(c, h + 8, c, B('end_rod', facing='up')); v.s(c, h + 9, c, B('amethyst_block')); v.s(c, h + 10, c, B('amethyst_cluster', facing='up'))
    v.s(c, 2, c, B('enchanting_table')); v.s(c + 2, 1, c, B('bookshelf'))
    for k in range(3): v.s(c - 2 + k, 1, c + 1, B('bookshelf')) if False else None
    v.s(c, h - 2, c, B('sea_lantern'))
    return v

def treehouse():
    v = V(); cx = cz = 7
    v.fill(0, -3, 0, 14, -1, 14, B('grass_block')) if False else None
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            v.fill(cx + dx, -3, cz + dz, cx + dx, 12, cz + dz, log('oak_log'))
    for (dx, dz) in ((-2, 0), (2, 0), (0, 2), (0, -2)): v.fill(cx + dx, -2, cz + dz, cx + dx, 1, cz + dz, log('oak_log'))
    # Krone
    for x in range(-7, 8):
        for y in range(8, 20):
            for z in range(-7, 8):
                d = x * x + (y - 14) ** 2 * 1.3 + z * z
                if d <= 42 and (cx + x, y, cz + z) not in v.b and (abs(x) > 1 or abs(z) > 1 or y > 12):
                    v.s(cx + x, y, cz + z, leaves('oak_leaves') if (x + y + z) % 7 else leaves('azalea_leaves'))
    # Plattform + Haus
    pf = 7
    v.fill(cx - 5, pf, cz - 5, cx + 5, pf, cz + 5, B('spruce_planks'))
    for x in range(cx - 5, cx + 6): 
        v.s(x, pf + 1, cz + 5, B('birch_fence')); v.s(x, pf + 1, cz - 5, B('birch_fence'))
    for z in range(cz - 5, cz + 6): v.s(cx - 5, pf + 1, z, B('birch_fence')); v.s(cx + 5, pf + 1, z, B('birch_fence'))
    t = T(**{**F.__dict__, 'found': 'spruce_planks', 'found2': 'spruce_planks'})
    h = house(t, 7, 5, floors=1, ridge='z', chimney=False, interior=True, door_col=3)
    h.clear(0, -3, 0, 6, -1, 4)
    h.clear(-2, -2, -2, -1, -1, -1)
    v.paste(h, cx - 3, pf + 1, cz - 5)
    for k in range(0, pf + 2): v.s(cx - 1, k - 3 + 1, cz + 6 - 0, B('ladder', facing='north')) if False else None
    for k in range(-2, pf + 1): v.s(cx + 3, k, cz + 4 - 0 + 1 if False else cz + 2, B('ladder', facing='east')) if False else None
    for y in range(-2, pf + 2):
        v.s(cx + 2, y, cz + 3, B('ladder', facing='west')) if False else None
    for y in range(-2, pf + 1): v.s(cx - 1, y, cz + 2, B('ladder', facing='north')) 
    v.s(cx - 1, pf + 1, cz + 2 + 0, B('air')) if False else None
    v.clear(cx - 1, pf, cz + 2, cx - 1, pf, cz + 2)
    v.fill(cx - 1, pf + 1, cz + 3, cx - 1, pf + 1, cz + 3, B('air')) if False else None
    v.s(cx - 4, pf + 1, cz + 3, lantern(False)) if False else None
    return v

def crystal_spire():
    v = V(); 
    v.fill(0, -3, 0, 12, -1, 12, B('stone')); v.fill(0, 0, 0, 12, 0, 12, B('deepslate'))
    cols = [(6, 6, 18), (3, 4, 10), (9, 3, 12), (4, 9, 8), (9, 9, 11), (6, 2, 7), (2, 7, 6), (10, 6, 7)]
    for (cx, cz, h) in cols:
        for y in range(1, h):
            w = 1 if h - y > 4 else 0
            for dx in range(-w, w + 1):
                for dz in range(-w, w + 1):
                    if abs(dx) + abs(dz) <= w:
                        v.s(cx + dx, y, cz + dz, B('amethyst_block') if y % 3 else B('purple_stained_glass'))
        v.s(cx, h, cz, B('amethyst_cluster', facing='up'))
        v.s(cx, 1, cz, B('sea_lantern'))
    return v

def fountain():
    v = V(); r = 5; c = 6
    for y in range(-3, 0): v.disc(c, c, r + 1, y, B(F.found))
    v.disc(c, c, r + 1, 0, B('stone_bricks')); v.disc(c, c, r, 1, B('mossy_stone_bricks'), hollow=True)
    v.disc(c, c, r - 1, 0, B('water', level=0)); v.disc(c, c, r - 1, 1, B('water', level=0)) if False else None
    v.disc(c, c, r - 1, 0, B('light_blue_concrete')) if False else None
    for y in range(0, 5): v.s(c, y, c, B('stone_bricks') if y < 4 else B('chiseled_stone_bricks'))
    v.disc(c, c, 2, 3, B('stone_brick_slab', type='bottom')) if False else None
    v.disc(c, c, 2, 3, B('mossy_stone_bricks'), hollow=True)
    v.disc(c, c, 1, 3, B('water', level=0)); v.s(c, 5, c, B('water', level=0)) if False else None
    v.s(c, 5, c, B('amethyst_cluster', facing='up')); v.s(c, 4, c, B('sea_lantern'))
    for (dx, dz) in ((r, 0), (-r, 0), (0, r), (0, -r)): v.s(c + dx, 2, c + dz, B('birch_fence')); v.s(c + dx, 3, c + dz, B('soul_lantern', hanging='false'))
    return v

def portal_arch():
    v = V(); w = 9
    v.fill(0, -2, 0, w - 1, -1, 3, B('stone_bricks')); v.fill(0, 0, 0, w - 1, 0, 3, B('mossy_stone_bricks'))
    for x in (1, w - 2): v.fill(x, 1, 1, x, 8, 1, B('obsidian'))
    v.fill(1, 9, 1, w - 2, 9, 1, B('obsidian'))
    for x in (1, w - 2): v.s(x, 3, 1, B('crying_obsidian')); v.s(x, 6, 1, B('crying_obsidian'))
    v.fill(2, 1, 1, w - 3, 8, 1, B('purple_stained_glass'))
    for x in (0, w - 1): v.fill(x, 1, 0, x, 3, 0, B('mossy_stone_brick_wall')); v.s(x, 4, 0, B('soul_lantern', hanging='false'))
    v.fill(1, 1, 0, 1, 1, 0, B('end_rod', facing='up')) if False else None
    return v

def mage_library():
    v = house(F, 9, 9, floors=2, ridge='z', chimney=False, balcony=True, porch=False)
    for z in range(2, 7):
        v.s(1, 1, z, B('bookshelf')); v.s(1, 2, z, B('bookshelf')); v.s(7, 1, z, B('bookshelf')); v.s(7, 2, z, B('bookshelf'))
    v.s(4, 1, 4, B('enchanting_table')); v.s(4, 1, 2, B('lectern', facing='south'))
    return v

def fairy_cottage():
    t = T(**{**F.__dict__, 'roof': 'cherry', 'roof_block': 'cherry_planks', 'wall': 'white_terracotta', 'door': 'cherry_door', 'trap': 'cherry_trapdoor'})
    v = house(t, 7, 7, floors=1, roof='hip', over=1, chimney=False, door_col=3)
    for x in range(1, 6, 2): v.s(x, 0, 8, B('grass_block')); v.s(x, 1, 8, B(['pink_tulip', 'allium', 'cornflower'][x % 3]))
    v.s(-1, 1, 4, B('red_mushroom')); v.s(8, 1, 3, B('brown_mushroom'))
    return v

FAN_BUILDS = [
    ('house_small', 'Elfenhaus', 'Kleines Haus mit Wirbeldach', 'WARPED_DOOR', lambda: house(F, 7, 7, floors=1, roof='hip', over=1, chimney=False)),
    ('house_medium', 'Zauberhaus', 'Zweistöckiges Haus', 'BIRCH_STAIRS', lambda: house(F, 9, 7, floors=2, ridge='x', chimney=True, balcony=True)),
    ('house_large', 'Gildenhaus', 'Großes Haus mit Veranda', 'BIRCH_PLANKS', lambda: house(F, 11, 9, floors=2, ridge='x', chimney=True, balcony=True, porch=True)),
    ('fairy_cottage', 'Feenhäuschen', 'Rosa Märchenhäuschen mit Blumen', 'PINK_TULIP', fairy_cottage),
    ('mushroom_red', 'Fliegenpilzhaus', 'Rotes Pilzhaus', 'RED_MUSHROOM_BLOCK', lambda: mushroom('red_mushroom_block', 5)),
    ('mushroom_brown', 'Steinpilzhaus', 'Braunes Pilzhaus', 'BROWN_MUSHROOM_BLOCK', lambda: mushroom('brown_mushroom_block', 5)),
    ('wizard_tower', 'Zauberturm', 'Hoher Magierturm', 'ENCHANTING_TABLE', wizard_tower),
    ('treehouse', 'Baumhaus', 'Riesenbaum mit Haus', 'OAK_LEAVES', treehouse),
    ('crystal', 'Kristallspitze', 'Amethyst-Kristalle', 'AMETHYST_SHARD', crystal_spire),
    ('library', 'Magische Bibliothek', 'Bücherhaus mit Zaubertisch', 'BOOKSHELF', mage_library),
    ('fountain', 'Zauberbrunnen', 'Leuchtender Brunnen', 'WATER_BUCKET', fountain),
    ('portal', 'Portalbogen', 'Mystischer Torbogen', 'OBSIDIAN', portal_arch),
    ('town_hall', 'Rathaus', 'Rathaus mit Turm', 'BELL', lambda: town_hall(F, 15, 11, 'purple')),
    ('stall', 'Marktstand', 'Magischer Stand', 'HAY_BLOCK', lambda: stall(F, ('purple', 'light_blue'))),
]

CATS_B = [
    ('modern', 'Modern', 'WHITE_CONCRETE', '<#cfd8dc>', 'Beton, Glas und Pools', MOD_BUILDS),
    ('west', 'Wild West', 'CACTUS', '<#d2a679>', 'Saloon, Sheriff und Prärie', WEST_BUILDS),
    ('asia', 'Asiatisch', 'LANTERN', '<#e57373>', 'Pagoden, Torii und Teehäuser', ASIA_BUILDS),
    ('fantasy', 'Fantasy', 'AMETHYST_SHARD', '<#ba68c8>', 'Zauberer, Pilze und Kristalle', FAN_BUILDS),
]
