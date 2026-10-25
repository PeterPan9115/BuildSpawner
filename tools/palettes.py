"""Blockpaletten: Mischungen je Kategorie (Block -> {Variante: Gewicht}) + Sockel-Material."""
import cat_a, cat_b

def fam(base, *variants):
    """{stairs/slab/block}-Varianten für Familien erzeugen"""
    return {base: dict(variants)}

STONE = {
    'stone_bricks': {'stone_bricks': 5, 'cracked_stone_bricks': 2, 'mossy_stone_bricks': 2, 'cobblestone': 1},
    'cobblestone': {'cobblestone': 5, 'mossy_cobblestone': 2, 'andesite': 1, 'stone': 1},
    'mossy_cobblestone': {'mossy_cobblestone': 5, 'cobblestone': 2, 'moss_block': 1},
}

def woods(main, others):
    """planks/stairs/slab-Mischung: main mit anderen Holzarten"""
    r = {}
    for suf in ('planks', 'stairs', 'slab'):
        d = {f'{main}_{suf}': 6}
        for o, wgt in others.items(): d[f'{o}_{suf}'] = wgt
        r[f'{main}_{suf}'] = d
    return r

RULES = {}
RULES['pirate'] = {**STONE,
    **woods('dark_oak', {'spruce': 2}),
    **woods('spruce', {'dark_oak': 2}),
}
RULES['cozy'] = {**STONE,
    'white_terracotta': {'white_terracotta': 5, 'calcite': 3, 'smooth_quartz': 1},
    'brick_stairs': {'brick_stairs': 5, 'mud_brick_stairs': 3},
    'brick_slab': {'brick_slab': 5, 'mud_brick_slab': 3},
    'bricks': {'bricks': 5, 'mud_bricks': 3},
    **woods('oak', {'birch': 2, 'spruce': 1}),
}
RULES['medieval'] = {**STONE,
    'white_terracotta': {'white_terracotta': 5, 'calcite': 2, 'light_gray_terracotta': 1},
    'stone_brick_stairs': {'stone_brick_stairs': 5, 'cobblestone_stairs': 2, 'mossy_stone_brick_stairs': 1, 'andesite_stairs': 1},
    'stone_brick_slab': {'stone_brick_slab': 5, 'cobblestone_slab': 2, 'mossy_stone_brick_slab': 1, 'andesite_slab': 1},
    **woods('oak', {'spruce': 2, 'birch': 1}),
}
RULES['viking'] = {**STONE,
    **woods('spruce', {'dark_oak': 2, 'oak': 1}),
    'mossy_cobblestone_stairs': {'mossy_cobblestone_stairs': 5, 'cobblestone_stairs': 2, 'mossy_stone_brick_stairs': 2},
    'mossy_cobblestone_slab': {'mossy_cobblestone_slab': 5, 'cobblestone_slab': 2, 'mossy_stone_brick_slab': 2},
    'mossy_cobblestone': {'mossy_cobblestone': 4, 'moss_block': 3, 'cobblestone': 1},
}
RULES['modern'] = {
    'white_concrete': {'white_concrete': 7, 'smooth_quartz': 2, 'calcite': 1},
    'gray_concrete': {'gray_concrete': 6, 'light_gray_concrete': 2, 'stone': 1},
    'light_gray_concrete': {'light_gray_concrete': 6, 'smooth_stone': 2, 'stone': 1},
    'stone': {'stone': 5, 'smooth_stone': 2, 'andesite': 1},
    'smooth_stone_slab': {'smooth_stone_slab': 6, 'stone_slab': 2},
    'black_concrete': {'black_concrete': 7, 'deepslate': 1},
}
RULES['west'] = {**STONE,
    'acacia_planks': {'acacia_planks': 5, 'oak_planks': 2, 'spruce_planks': 2, 'birch_planks': 1},
    'sandstone': {'sandstone': 5, 'smooth_sandstone': 2, 'cut_sandstone': 2},
    'smooth_sandstone': {'smooth_sandstone': 5, 'sandstone': 2, 'cut_sandstone': 1},
    **woods('spruce', {'dark_oak': 2, 'oak': 1}),
    'red_terracotta': {'red_terracotta': 6, 'terracotta': 1, 'brown_terracotta': 1},
}
RULES['asia'] = {**STONE,
    'white_terracotta': {'white_terracotta': 6, 'calcite': 2},
    'deepslate_tile_stairs': {'deepslate_tile_stairs': 6, 'deepslate_brick_stairs': 3, 'cobbled_deepslate_stairs': 1},
    'deepslate_tile_slab': {'deepslate_tile_slab': 6, 'deepslate_brick_slab': 3, 'cobbled_deepslate_slab': 1},
    'deepslate_tiles': {'deepslate_tiles': 5, 'deepslate_bricks': 3, 'cracked_deepslate_tiles': 1},
    **woods('spruce', {'jungle': 2, 'bamboo': 1}),
    **woods('dark_oak', {'spruce': 2}),
}
RULES['fantasy'] = {**STONE,
    'mossy_stone_bricks': {'mossy_stone_bricks': 5, 'stone_bricks': 2, 'mossy_cobblestone': 1, 'moss_block': 1},
    'birch_planks': {'birch_planks': 5, 'bamboo_planks': 2, 'oak_planks': 1},
    'warped_stairs': {'warped_stairs': 5, 'prismarine_brick_stairs': 2, 'dark_prismarine_stairs': 1},
    'warped_slab': {'warped_slab': 5, 'prismarine_brick_slab': 2, 'dark_prismarine_slab': 1},
    'warped_planks': {'warped_planks': 5, 'prismarine_bricks': 2},
    'white_concrete': {'white_concrete': 5, 'calcite': 3, 'quartz_block': 1},
}

# Sockelreihe (unterste Wandreihe) je Theme
cat_a.PIRATE.base = 'stone_bricks'; cat_a.COZY.base = 'cobblestone'; cat_a.MED.base = 'cobblestone'; cat_a.VIK.base = 'cobblestone'
cat_b.WEST.base = 'sandstone'; cat_b.AS.base = 'stone_bricks'; cat_b.FAN.base = 'mossy_stone_bricks'

# Hauptblock dominanter machen (ruhigere Optik, Varianten nur als Akzent)
for _cat in RULES.values():
    for _k, _v in _cat.items():
        _first = next(iter(_v)); _v[_first] *= 2
