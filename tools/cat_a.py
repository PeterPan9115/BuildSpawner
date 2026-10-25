from common import *

# ============================================================== PIRATEN (dunkles Holz)
PIRATE = T(log='dark_oak_log', beam='stripped_dark_oak_log', wall='dark_oak_planks', floor='spruce_planks',
           found='stone_bricks', found2='cobblestone', found_stair='stone_brick', roof='spruce', roof_block='spruce_planks',
           door='dark_oak_door', trap='dark_oak_trapdoor', fence='dark_oak_fence', wood_slab='dark_oak', wood_stair='dark_oak',
           hull='dark_oak_planks', hull2='spruce_planks', deck='spruce_planks', bedcolor='red', rug='red_carpet')
P = PIRATE

def pirate_fort(t):
    v = tower(t, r=3, h=10, roof='crenel', ladders=True)
    # Kanonen (Dispenser) auf der Plattform
    for (x, z) in ((1, 8), (3, 8), (5, 8)):
        v.s(x, 12, z, B('dispenser', facing='south')) if False else None
    for x in (1, 3, 5):
        v.s(x, 12, 7, B('dispenser', facing='south')); v.s(x, 12, 6, B('barrel', facing='up'))
    v.s(3, 12, 3, B('black_banner', rotation=0)) if False else v.s(3, 12, 3, B(t.fence)); v.s(3, 13, 3, B(t.fence)); v.s(3, 14, 3, B('black_wool'))
    v.s(4, 14, 3, B('black_wool')); v.s(2, 14, 3, B('black_wool')) if False else None
    return v

def jail(t):
    v = house(t, 9, 7, floors=1, ridge='x', porch=False, chimney=False, windows=False, interior=False, lamp=False)
    for x in (1, 2, 3, 4):
        pass
    for z in range(1, 6):
        v.s(4, 1, z, B('iron_bars')); v.s(4, 2, z, B('iron_bars')); v.s(4, 3, z, B('iron_bars'))
    for x in (2, 6): v.s(x, 2, 6, B('iron_bars'))
    v.s(6, 1, 1, bed('white', 'south', 'head')); v.s(6, 1, 2, bed('white', 'south', 'foot'))
    v.s(2, 1, 1, bed('white', 'south', 'head')); v.s(2, 1, 2, bed('white', 'south', 'foot'))
    v.s(7, 1, 4, B('crafting_table')); v.s(7, 1, 5, B('barrel', facing='up'))
    v.s(4, 3, 3, lantern(True)) if False else None
    v.s(2, 3, 3, lantern(True)); v.s(6, 3, 3, lantern(True))
    v.clear(4, 1, 3, 4, 2, 3); v.s(4, 1, 3, door('iron_door', 'east', 'lower')); v.s(4, 2, 3, door('iron_door', 'east', 'upper'))
    return v

def harbor_master(t):
    v = house(t, 9, 8, floors=2, ridge='x', porch=True, balcony=True, chimney=False)
    v.s(4, 6, 0, B('black_wool')) if False else None
    # Signalmast
    v.fill(8, 9, 4, 8, 14, 4, B(t.fence)); v.s(8, 13, 3, B('red_wool')); v.s(8, 14, 3, B('red_wool')); v.s(8, 13, 2, B('white_wool')); v.s(8, 14, 2, B('white_wool'))
    return v

def pirate_ship_small(t):
    return ship(t, length=19, beam=7, mast_h=11, masts=1, cabin=True)

def treasure_hut(t):
    v = house(t, 7, 7, floors=1, ridge='z', porch=False, chimney=False, windows=True, interior=False)
    v.s(3, 1, 1, chest('south')); v.s(2, 1, 1, chest('south')); v.s(4, 1, 1, chest('south'))
    v.s(3, 2, 1, B('gold_block')); v.s(2, 2, 1, B('gold_block'))
    v.s(5, 1, 1, B('barrel', facing='up')); v.s(1, 1, 5, B('barrel', facing='up')); v.s(5, 1, 5, B('hay_block', axis='y'))
    v.s(3, 3, 3, lantern(True))
    # Schädel-Zeichen
    v.s(3, 5, 7, B('skeleton_skull', rotation=8)) if False else None
    v.s(3, 4, 7, B('black_wool')) if False else None
    return v

PIRATE_BUILDS = [
    ('house_small', 'Piratenhütte', 'Kleines Haus aus dunklem Holz', 'DARK_OAK_DOOR', lambda: house(P, 7, 7, floors=1, ridge='z', chimney=True)),
    ('house_shack', 'Strandhütte', 'Kompakte Hütte mit Veranda', 'SPRUCE_DOOR', lambda: house(P, 7, 9, floors=1, ridge='z', porch=True, chimney=False)),
    ('house_medium', 'Seemannshaus', 'Zweistöckiges Wohnhaus mit Balkon', 'DARK_OAK_STAIRS', lambda: house(P, 9, 7, floors=2, ridge='x', balcony=True, chimney=True)),
    ('house_captain', 'Kapitänshaus', 'Großes Haus mit Veranda und Balkon', 'DARK_OAK_PLANKS', lambda: house(P, 11, 9, floors=2, ridge='x', balcony=True, porch=True, chimney=True)),
    ('house_row', 'Hafenhaus', 'Schmales hohes Haus für die Hafenzeile', 'SPRUCE_STAIRS', lambda: house(P, 7, 9, floors=3, ridge='z', chimney=True)),
    ('tavern', 'Piratenschenke', 'Große Taverne mit Tresen und Zimmern', 'BARREL', lambda: tavern(P, True, 'yellow')),
    ('tavern_small', 'Hafenkneipe', 'Kleine Kneipe am Kai', 'BEER' if False else 'COOKED_COD', lambda: tavern(P, False, 'red')),
    ('town_hall', 'Rathaus', 'Rathaus mit Glockenturm und Freitreppe', 'BELL', lambda: town_hall(P, 15, 11, 'red')),
    ('smithy', 'Waffenschmiede', 'Schmiede mit Esse, Amboss und offenem Anbau', 'ANVIL', lambda: smithy(P)),
    ('shop', 'Kaufmannsladen', 'Laden mit Markise', 'EMERALD', lambda: shop(P, 9, 7, ('red', 'white'))),
    ('warehouse', 'Lagerhaus', 'Großes Lager für Fracht und Fässer', 'CHEST', lambda: warehouse(P, 11, 13)),
    ('harbor_master', 'Hafenmeisterei', 'Büro mit Signalmast', 'SPYGLASS', lambda: harbor_master(P)),
    ('jail', 'Gefängnis', 'Zellen mit Eisengittern', 'IRON_BARS', lambda: jail(P)),
    ('treasure_hut', 'Schatzhütte', 'Versteck voller Truhen', 'GOLD_INGOT', lambda: treasure_hut(P)),
    ('fort', 'Kanonenfort', 'Wehrturm mit Kanonenplattform', 'TNT' if False else 'DISPENSER', lambda: pirate_fort(P)),
    ('lighthouse', 'Leuchtturm', 'Rot-weißer Leuchtturm', 'LANTERN', lambda: lighthouse(P, 17)),
    ('watchtower', 'Ausguck', 'Hoher Holzturm mit Plattform', 'LADDER', lambda: tower(P, 2, 14, roof='flat')),
    ('stall', 'Marktstand', 'Marktstand mit Fässern', 'HAY_BLOCK', lambda: stall(P, ('black', 'red'))),
    ('well', 'Brunnen', 'Dorfbrunnen mit Dach', 'WATER_BUCKET', lambda: well(P)),
    ('pier', 'Anlegesteg', 'Holzsteg mit Laternen', 'OAK_BOAT' if False else 'DARK_OAK_BOAT', lambda: pier(P, 17, 5)),
    ('ship_sloop', 'Schaluppe', 'Kleines Segelschiff', 'OAK_BOAT', lambda: pirate_ship_small(P)),
    ('ship_galleon', 'Piratengaleone', 'Großes Segelschiff mit zwei Masten', 'NAUTILUS_SHELL', lambda: ship(P, 29, 9, 15, masts=2)),
]

# ============================================================== COZY
COZY = T(log='spruce_log', beam='stripped_spruce_log', wall='white_terracotta', floor='oak_planks',
         found='cobblestone', found2='mossy_cobblestone', found_stair='cobblestone', roof='brick', roof_block='bricks',
         door='spruce_door', trap='spruce_trapdoor', fence='spruce_fence', wood_slab='spruce', wood_stair='oak',
         hull='spruce_planks', hull2='oak_planks', deck='oak_planks', bedcolor='pink', rug='orange_carpet', timber=True)
C = COZY

def garden(v, x1, z1, x2, z2):
    flowerbed(v, x1, z1, x2, z2, y=1, base='grass_block' if False else None)

def cozy_cottage(w, l, floors, ridge, flowers=True, **kw):
    v = house(C, w, l, floors=floors, ridge=ridge, **kw)
    if flowers:
        for x in range(1, w - 1, 2):
            v.s(x, 0, l + 1, B('grass_block')); v.s(x, 1, l + 1, B(['poppy', 'cornflower', 'dandelion', 'pink_tulip'][x % 4]))
        v.s(0, 1, l + 1, B('oak_leaves', persistent='true')); v.s(w - 1, 1, l + 1, B('oak_leaves', persistent='true'))
    return v

def bakery():
    v = shop(C, 9, 7, ('orange', 'white'))
    v.s(1, 1, 1, B('furnace', facing='south', lit='true')); v.s(2, 1, 1, B('smoker', facing='south', lit='true'))
    for x in (3, 4, 5): v.s(x, 1, 3, B('barrel', facing='up'))
    v.s(6, 1, 1, B('hay_block', axis='y'))
    return v

def flower_shop():
    v = shop(C, 7, 7, ('pink', 'white'))
    for x in range(0, 7): v.s(x, 1, 8, B(['poppy', 'blue_orchid', 'allium', 'azure_bluet', 'pink_tulip', 'oxeye_daisy', 'cornflower'][x % 7]))
    for x in range(0, 7): v.s(x, 0, 8, B('grass_block'))
    return v

def farm_barn():
    v = warehouse(C, 9, 13)
    return v

def cozy_cafe():
    v = tavern(C, False, 'orange')
    return v

def cozy_library():
    v = house(C, 9, 9, floors=2, ridge='z', chimney=True, balcony=False, porch=True)
    for z in range(2, 7):
        v.s(1, 1, z, B('bookshelf')); v.s(1, 2, z, B('bookshelf')); v.s(7, 1, z, B('bookshelf')); v.s(7, 2, z, B('bookshelf'))
    v.s(4, 1, 2, B('lectern', facing='south')); v.s(4, 1, 1, B('enchanting_table')) if False else None
    return v

def cozy_church():
    return chapel(C, 7, 13, 14)

COZY_BUILDS = [
    ('cottage_small', 'Kleines Cottage', 'Gemütliches Häuschen mit Blumenbeet', 'SPRUCE_DOOR', lambda: cozy_cottage(7, 7, 1, 'z')),
    ('cottage_medium', 'Landhaus', 'Fachwerkhaus mit Veranda', 'OAK_DOOR', lambda: cozy_cottage(9, 7, 1, 'x', porch=True)),
    ('cottage_two', 'Doppelstock-Cottage', 'Zwei Etagen mit Balkon', 'BRICK_STAIRS', lambda: cozy_cottage(9, 8, 2, 'x', balcony=True)),
    ('cottage_large', 'Großes Familienhaus', 'Drei-Zimmer-Haus mit Garten', 'BRICKS', lambda: cozy_cottage(11, 9, 2, 'x', balcony=True, porch=True)),
    ('cottage_tall', 'Schmales Stadthaus', 'Hohes Fachwerkhaus', 'SPRUCE_LOG', lambda: cozy_cottage(7, 9, 3, 'z')),
    ('bakery', 'Bäckerei', 'Bäckerei mit Öfen und Markise', 'BREAD', bakery),
    ('flower_shop', 'Blumenladen', 'Kleiner Laden mit Blumen', 'POPPY', flower_shop),
    ('cafe', 'Gemütliches Café', 'Café mit Terrasse', 'CAKE', cozy_cafe),
    ('library', 'Bibliothek', 'Bücherhaus mit Leseecke', 'BOOKSHELF', cozy_library),
    ('town_hall', 'Dorfhalle', 'Gemeindehaus mit Turm', 'BELL', lambda: town_hall(C, 13, 9, 'orange')),
    ('smithy', 'Dorfschmiede', 'Schmiede mit Anbau', 'ANVIL', lambda: smithy(C)),
    ('barn', 'Scheune', 'Landwirtschaftliche Scheune', 'HAY_BLOCK', farm_barn),
    ('stable', 'Pferdestall', 'Stall mit Boxen', 'SADDLE', lambda: stable(C)),
    ('windmill', 'Windmühle', 'Windmühle mit Flügeln', 'WHEAT', lambda: windmill(C)),
    ('greenhouse', 'Gewächshaus', 'Glashaus mit Beeten', 'GLASS', lambda: greenhouse(C)),
    ('chapel', 'Dorfkirche', 'Kapelle mit Turm', 'BELL', cozy_church),
    ('stall', 'Obststand', 'Marktstand', 'APPLE', lambda: stall(C, ('orange', 'white'))),
    ('well', 'Wunschbrunnen', 'Brunnen', 'WATER_BUCKET', lambda: well(C)),
]

# ============================================================== MITTELALTER
MED = T(log='dark_oak_log', beam='stripped_dark_oak_log', wall='white_terracotta', floor='oak_planks',
        found='cobblestone', found2='stone_bricks', found_stair='stone_brick', roof='stone_brick', roof_block='stone_bricks',
        door='oak_door', trap='spruce_trapdoor', fence='oak_fence', wood_slab='oak', wood_stair='oak', hull='oak_planks', hull2='spruce_planks',
        deck='oak_planks', bedcolor='blue', rug='blue_carpet', timber=True)
M = MED

def keep():
    v = tower(M, r=5, h=20, roof='crenel', door=True)
    for (x, z) in ((-2, -2), (12, -2), (-2, 12), (12, 12)):
        t2 = tower(M, r=1, h=24, roof='pyramid', door=False, windows=True, ladders=False)
        v.paste(t2, x, 0, z)
    return v

def gatehouse():
    v = V()
    for x0 in (0, 10):
        v.paste(tower(M, r=2, h=14, roof='crenel', door=False), x0, 0, 0)
    # Torbogen-Block zwischen den Türmen
    v.fill(5, -3, 0, 9, -1, 4, B(M.found)); v.fill(5, 0, 0, 9, 0, 4, B(M.found2))
    v.fill(5, 1, 0, 9, 12, 4, B(M.found2))
    v.clear(6, 1, 0, 8, 5, 4)
    v.clear(7, 6, 0, 7, 6, 4)
    v.fill(5, 13, 0, 9, 13, 4, B(M.found)); 
    for x in range(5, 10):
        if x % 2 == 1: v.s(x, 14, 0, B(M.found)); v.s(x, 14, 4, B(M.found))
    for x in (6, 7, 8): v.s(x, 5, 0, B('iron_bars')); v.s(x, 4, 0, B('iron_bars'))
    for z in range(0, 5):
        for x in (6, 7, 8): v.s(x, 0, z, B('dirt_path') if False else B('stone_brick_slab', type='bottom') if False else B('cobblestone'))
    v.s(7, 4, 2, lantern(True)) if False else None
    v.s(6, 5, 2, lantern(True)); v.s(8, 5, 2, lantern(True))
    return v

def castle_wall():
    v = V()
    L = 15
    v.fill(0, -3, 0, L - 1, -1, 4, B(M.found)); v.fill(0, 0, 0, L - 1, 6, 4, B(M.found2))
    v.clear(0, 1, 1, L - 1, 6, 3); v.fill(0, 0, 1, L - 1, 0, 3, B(M.found2))
    v.fill(0, 7, 0, L - 1, 7, 4, B(M.found2)); v.fill(1, 7, 1, L - 2, 7, 3, B(M.floor)) if False else None
    for x in range(0, L, 2):
        v.s(x, 8, 0, B(M.found2)); v.s(x, 8, 4, B(M.found2))
    for x in range(2, L, 4):
        v.s(x, 5, 0, B('iron_bars')) if False else None
        v.s(x, 4, 4, B('iron_bars')) if False else None
    v.s(1, 1, 2, B('ladder', facing='east')) if False else None
    v.s(2, 1, 4, B('ladder', facing='north')) if False else None
    for x in range(2, L - 1, 3):
        v.s(x, 8, 0, B(M.found2)); v.s(x, 9, 0, B(M.found2)) if False else None
        v.s(x, 6, 0, B('air')) if False else None
    return v

def med_inn(): return tavern(M, True, 'red')
def med_chapel(): return chapel(M, 7, 15, 16)

def blacksmith(): return smithy(M)

MED_BUILDS = [
    ('house_small', 'Bauernhaus', 'Fachwerkhaus für Bauern', 'OAK_DOOR', lambda: house(M, 7, 7, floors=1, ridge='z')),
    ('house_medium', 'Handwerkerhaus', 'Zweistöckiges Fachwerkhaus', 'OAK_STAIRS', lambda: house(M, 9, 7, floors=2, ridge='x', chimney=True)),
    ('house_merchant', 'Kaufmannshaus', 'Großes Fachwerkhaus mit Balkon', 'OAK_PLANKS', lambda: house(M, 11, 8, floors=2, ridge='x', balcony=True, porch=True)),
    ('house_tall', 'Stadthaus', 'Dreistöckiges Haus', 'DARK_OAK_LOG', lambda: house(M, 7, 9, floors=3, ridge='z', chimney=True)),
    ('inn', 'Gasthaus', 'Gasthaus mit Schankstube', 'BARREL', med_inn),
    ('town_hall', 'Rathaus', 'Stolzes Rathaus mit Turm', 'BELL', lambda: town_hall(M, 15, 11, 'blue')),
    ('smithy', 'Schmiede', 'Schmiede mit Esse', 'ANVIL', blacksmith),
    ('chapel', 'Kapelle', 'Steinkirche mit Turm', 'BELL', med_chapel),
    ('shop', 'Marktladen', 'Laden mit Markise', 'EMERALD', lambda: shop(M, 9, 7, ('blue', 'white'))),
    ('stable', 'Stall', 'Pferdestall', 'SADDLE', lambda: stable(M)),
    ('barn', 'Kornspeicher', 'Großer Speicher', 'WHEAT', lambda: warehouse(M, 9, 13)),
    ('watchtower', 'Wachturm', 'Steinerner Wachturm', 'CROSSBOW', lambda: tower(M, 2, 16, roof='crenel')),
    ('keep', 'Bergfried', 'Burgturm mit vier Ecktürmen', 'SHIELD', keep),
    ('gatehouse', 'Torhaus', 'Burgtor mit zwei Türmen', 'IRON_BARS', gatehouse),
    ('wall', 'Burgmauer', 'Mauerabschnitt mit Zinnen', 'STONE_BRICKS', castle_wall),
    ('windmill', 'Mühle', 'Getreidemühle', 'WHEAT', lambda: windmill(M)),
    ('stall', 'Marktstand', 'Marktstand', 'HAY_BLOCK', lambda: stall(M, ('blue', 'white'))),
    ('well', 'Dorfbrunnen', 'Brunnen', 'WATER_BUCKET', lambda: well(M)),
]

# ============================================================== WIKINGER
VIK = T(log='spruce_log', beam='stripped_spruce_log', wall='spruce_planks', floor='dark_oak_planks',
        found='cobblestone', found2='mossy_cobblestone', found_stair='cobblestone', roof='mossy_cobblestone', roof_block='mossy_cobblestone',
        door='spruce_door', trap='spruce_trapdoor', fence='spruce_fence', wood_slab='spruce', wood_stair='spruce',
        hull='spruce_planks', hull2='dark_oak_planks', deck='spruce_planks', bedcolor='white', rug='gray_carpet')
Vk = VIK

def longship():
    v = ship(Vk, 27, 7, 11, masts=1, sail='red_wool', cabin=False)
    cx = 3
    # Drachenkopf am Bug
    for k, (dy, dz) in enumerate(((0, 0), (1, 0), (2, 0), (3, 1), (3, 2))):
        v.s(cx, 2 + dy, 27 + dz - 1 + 0, B(Vk.hull2))
    v.s(cx, 6, 28, B('dark_oak_fence')); v.s(cx, 7, 28, B('dark_oak_planks')); v.s(cx, 7, 29, stair('dark_oak', 'south')) 
    v.s(cx - 1, 8, 28, B('end_rod', facing='up')); v.s(cx + 1, 8, 28, B('end_rod', facing='up'))
    for x in (1, 5):
        for z in range(6, 24, 4):
            v.s(x, 2, z, B('white_wool') if False else B('red_wool')) if False else None
    return v

def longhouse(w=9, l=19):
    v = house(Vk, w, l, floors=1, ridge='z', porch=False, chimney=False, lamp=True, over=1, windows=True)
    # Feuerstelle in der Mitte
    cz = l // 2
    v.s(w // 2, 0, cz, B('netherrack')) if False else v.s(w // 2, 0, cz, B('cobblestone'))
    v.s(w // 2, 1, cz, B('campfire', lit='true', signal_fire='false'))
    for z in range(2, l - 2, 3):
        v.s(1, 1, z, bed('white', 'east', 'foot')); v.s(2, 1, z, bed('white', 'east', 'head'))
        v.s(w - 3, 1, z, bed('white', 'west', 'foot')); v.s(w - 2, 1, z, bed('white', 'west', 'head'))
    # Giebelverzierung (Drachenköpfe)
    v.s(w // 2, 7, l, B('spruce_fence')) if False else None
    return v

def mead_hall():
    v = longhouse(13, 25)
    for z in range(3, 22, 4):
        v.s(5, 1, z, B('spruce_fence')); v.s(7, 1, z, B('spruce_fence')); v.s(6, 1, z, slab('spruce', 'top'))
    return v

def boathouse():
    v = V()
    w, l = 11, 15
    v.fill(0, -2, 0, w - 1, -1, l - 1, B(Vk.found)); v.fill(0, 0, 0, w - 1, 0, l - 1, B(Vk.floor))
    for z in range(0, l, 4):
        for x in (0, w - 1): v.fill(x, 1, z, x, 5, z, log(Vk.log))
    for z in range(0, l):
        for x in (0, w - 1):
            if z % 4: v.fill(x, 1, z, x, 2, z, B(Vk.wall))
    v.fill(0, 5, 0, w - 1, 5, l - 1, B(Vk.floor)) if False else None
    roof_gable(v, Vk, 0, w - 1, 0, l - 1, 5, ridge='z', over=1, fill='spruce_planks')
    v.fill(4, 0, 0, 6, 0, l - 1, B('water', level=0)) if False else None
    for z in range(1, l - 1, 4): v.s(1, 1, z, B('barrel', facing='up')); v.s(w - 2, 1, z, chest('west'))
    for z in (2, 8, 13): v.s(5, 4, z, lantern(True))
    return v

def storehouse():
    v = V()
    w, l = 7, 9
    for (x, z) in ((0, 0), (w - 1, 0), (0, l - 1), (w - 1, l - 1), (3, 0), (3, l - 1)):
        v.fill(x, -3, z, x, 2, z, log(Vk.log))
    v.fill(0, 3, 0, w - 1, 3, l - 1, B(Vk.floor))
    v.walls(0, 4, 0, w - 1, 6, l - 1, B(Vk.wall))
    for (x, z) in ((0, 0), (w - 1, 0), (0, l - 1), (w - 1, l - 1)): v.fill(x, 4, z, x, 7, z, log(Vk.log))
    roof_gable(v, Vk, 0, w - 1, 0, l - 1, 7, ridge='z', over=1, fill='spruce_planks')
    v.clear(3, 4, l - 1, 3, 5, l - 1)
    v.s(3, 4, l - 1, door(Vk.door, 'south', 'lower')); v.s(3, 5, l - 1, door(Vk.door, 'south', 'upper'))
    for k in range(0, 3): v.s(3, 3 - k - 0, l, stair('spruce', 'south') if False else B('ladder', facing='south')) if False else None
    for y in range(0, 4): v.s(3, y, l, B('ladder', facing='north')) if False else None
    for i, y in enumerate(range(0, 4)):
        v.s(2 + 0, y - 0, l + 4 - i - 0, B('air')) if False else None
    v.fill(3, 3, l, 3, 3, l + 1, B(Vk.floor))
    for k in range(3):
        v.s(3, 2 - k, l + 2 + k, stair('spruce', 'south')) if False else v.s(3, 2 - k + 0, l + 2 + k, stair('spruce', 'south'))
    v.s(3, 3, l + 1, B(Vk.floor))
    for x in range(1, w - 1, 2):
        for z in (1, 3, 5): v.s(x, 4, z, B('barrel', facing='up'))
    v.s(3, 6, 4, lantern(True))
    return v

def runestone():
    v = V()
    v.fill(0, -2, 0, 6, -1, 6, B('cobblestone')); v.fill(0, 0, 0, 6, 0, 6, B('mossy_cobblestone'))
    v.fill(3, 1, 3, 3, 5, 3, B('chiseled_stone_bricks')); v.s(3, 6, 3, stair('stone_brick', 'south'))
    for (x, z) in ((1, 1), (5, 1), (1, 5), (5, 5)):
        v.s(x, 1, z, B('spruce_fence')); v.s(x, 2, z, B('lantern', hanging='false'))
    v.s(3, 3, 4, B('smooth_stone')) if False else None
    v.s(3, 2, 2, B('crying_obsidian')) if False else None
    v.s(3, 2, 4, B('stone_brick_wall')) if False else None
    return v

def drying_rack():
    v = V()
    v.fill(0, 0, 0, 8, 0, 4, B('coarse_dirt')) if False else None
    v.fill(0, -2, 0, 8, -1, 4, B('cobblestone')); v.fill(0, 0, 0, 8, 0, 4, B('spruce_planks'))
    for x in (0, 8):
        for z in (0, 4): v.fill(x, 1, z, x, 4, z, B('spruce_log'))
    for z in (0, 4): v.fill(0, 4, z, 8, 4, z, B('spruce_fence') if False else log('stripped_spruce_log', 'x'))
    for x in range(1, 8, 2):
        v.s(x, 3, 0, B('cod_bucket')) if False else None
        v.s(x, 3, 0, B('chain')) if False else None
        v.s(x, 3, 0, B('spruce_fence')); v.s(x, 2, 0, B('white_wool') if False else B('light_gray_wool'))
        v.s(x, 3, 4, B('spruce_fence')); v.s(x, 2, 4, B('light_gray_wool'))
    for x in range(1, 8, 3): v.s(x, 1, 2, B('barrel', facing='up'))
    return v

VIK_BUILDS = [
    ('house_small', 'Wikingerhütte', 'Kleines Haus mit Grasdach', 'SPRUCE_DOOR', lambda: house(Vk, 7, 9, floors=1, ridge='z', chimney=False)),
    ('house_medium', 'Bauernhof', 'Mittleres Haus', 'SPRUCE_STAIRS', lambda: house(Vk, 9, 11, floors=1, ridge='z', chimney=False, porch=True)),
    ('house_two', 'Händlerhaus', 'Zweistöckiges Haus', 'SPRUCE_PLANKS', lambda: house(Vk, 9, 9, floors=2, ridge='x', balcony=True, chimney=True)),
    ('longhouse', 'Langhaus', 'Klassisches Wikinger-Langhaus', 'MOSSY_COBBLESTONE', lambda: longhouse(9, 19)),
    ('mead_hall', 'Methalle', 'Große Halle des Häuptlings', 'HONEY_BOTTLE', mead_hall),
    ('smithy', 'Schmiede', 'Wikingerschmiede', 'ANVIL', lambda: smithy(Vk)),
    ('boathouse', 'Bootshaus', 'Offenes Bootshaus', 'SPRUCE_BOAT', boathouse),
    ('longship', 'Langschiff', 'Langschiff mit Drachenkopf', 'SPRUCE_BOAT', longship),
    ('storehouse', 'Vorratshaus', 'Speicher auf Stelzen', 'BARREL', storehouse),
    ('watchtower', 'Wachturm', 'Hölzerner Wachturm', 'CROSSBOW', lambda: tower(Vk, 2, 14, roof='crenel')),
    ('tower_big', 'Hügelfestung', 'Starker Turm', 'SHIELD', lambda: tower(Vk, 3, 12, roof='crenel')),
    ('drying', 'Fischtrockner', 'Gestell zum Trocknen', 'COD', drying_rack),
    ('runestone', 'Runenstein', 'Gedenkstein mit Laternen', 'CHISELED_STONE_BRICKS', runestone),
    ('stall', 'Marktstand', 'Händlerstand', 'HAY_BLOCK', lambda: stall(Vk, ('red', 'white'))),
    ('well', 'Brunnen', 'Brunnen', 'WATER_BUCKET', lambda: well(Vk)),
]

CATS_A = [
    ('pirate', 'Piraten', 'DARK_OAK_BOAT', '<#a0522d>', 'Dunkles Holz, Hafen und Schiffe', PIRATE_BUILDS),
    ('cozy', 'Cozy', 'CAMPFIRE', '<#f4a460>', 'Gemütliche Fachwerk-Cottages', COZY_BUILDS),
    ('medieval', 'Mittelalter', 'IRON_SWORD', '<#9aa0a6>', 'Fachwerk, Stein und Burgen', MED_BUILDS),
    ('viking', 'Wikinger', 'SHIELD', '<#6b8e23>', 'Langhäuser, Grasdächer, Langschiffe', VIK_BUILDS),
]
