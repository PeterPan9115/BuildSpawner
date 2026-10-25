"""Isometrischer Voxel-Renderer: liest .schem-Dateien und erzeugt Vorschau-PNGs."""
import gzip, struct, re, math
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- NBT lesen
def read_nbt(path):
    data = gzip.open(path, 'rb').read()
    pos = [0]
    def u(fmt):
        n = struct.calcsize(fmt); v = struct.unpack_from(fmt, data, pos[0]); pos[0] += n; return v[0]
    def string():
        n = u('>H'); s = data[pos[0]:pos[0] + n].decode('utf-8'); pos[0] += n; return s
    def payload(t):
        if t == 1: return u('>b')
        if t == 2: return u('>h')
        if t == 3: return u('>i')
        if t == 4: return u('>q')
        if t == 8: return string()
        if t == 7:
            n = u('>i'); v = data[pos[0]:pos[0] + n]; pos[0] += n; return v
        if t == 11:
            n = u('>i'); return [u('>i') for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                tt = u('>B')
                if tt == 0: return d
                k = string(); d[k] = payload(tt)
        raise ValueError(t)
    t = u('>B'); string()
    return payload(t)

def load_schem(path):
    r = read_nbt(path)
    w, h, l = r['Width'], r['Height'], r['Length']
    pal = {v: k for k, v in r['Palette'].items()}
    raw = r['BlockData']; vals = []; i = 0
    while i < len(raw):
        v = 0; sh = 0
        while True:
            b = raw[i]; i += 1
            v |= (b & 0x7F) << sh
            if not b & 0x80: break
            sh += 7
        vals.append(v)
    blocks = {}
    for idx, v in enumerate(vals):
        if v == 0: continue
        x = idx % w; z = (idx // w) % l; y = idx // (w * l)
        blocks[(x, y, z)] = pal[v]
    return w, h, l, blocks

# ---------------------------------------------------------------- Farben
COLORS = [
    ('dark_oak', (68, 48, 26)), ('spruce', (112, 80, 46)), ('stripped_oak', (178, 144, 86)),
    ('oak', (160, 128, 76)), ('birch', (206, 190, 136)), ('acacia', (170, 92, 52)), ('cherry', (228, 176, 170)),
    ('mangrove', (118, 54, 48)), ('jungle', (160, 114, 80)), ('bamboo', (200, 190, 80)), ('crimson', (110, 50, 70)),
    ('warped', (40, 120, 120)), ('mossy_cobble', (95, 118, 85)), ('mossy_stone', (100, 120, 90)),
    ('deepslate', (70, 70, 76)), ('blackstone', (44, 40, 48)), ('cobblestone', (112, 112, 112)),
    ('stone_brick', (124, 124, 124)), ('smooth_stone', (160, 160, 160)), ('stone', (128, 128, 128)),
    ('white_terracotta', (209, 178, 161)), ('light_gray_terracotta', (135, 106, 97)), ('red_terracotta', (143, 61, 46)), ('brown_terracotta', (77, 51, 36)), ('purple_terracotta', (118, 70, 86)),
    ('red_sandstone', (186, 100, 36)), ('sandstone', (216, 202, 152)), ('red_sand', (190, 102, 33)),
    ('sand', (219, 207, 163)), ('terracotta', (152, 94, 68)), ('brick', (152, 98, 84)),
    ('quartz', (236, 230, 222)), ('calcite', (224, 224, 220)), ('purpur', (170, 126, 170)),
    ('amethyst', (150, 110, 200)), ('copper', (192, 110, 80)), ('iron_block', (216, 216, 216)),
    ('iron_bars', (150, 150, 150)), ('gold', (250, 220, 70)), ('prismarine', (80, 160, 140)),
    ('sea_lantern', (200, 230, 220)), ('glowstone', (240, 200, 110)), ('shroomlight', (240, 150, 70)),
    ('lantern', (240, 180, 80)), ('torch', (250, 200, 80)), ('campfire', (230, 120, 40)),
    ('glass', (170, 210, 235)), ('white_wool', (235, 235, 235)), ('black_wool', (28, 28, 32)),
    ('red_mushroom', (200, 40, 36)), ('mushroom_stem', (225, 220, 205)), ('brown_mushroom', (150, 110, 80)),
    ('moss', (90, 110, 40)), ('leaves', (62, 120, 44)), ('grass', (90, 140, 60)), ('dirt_path', (150, 120, 70)),
    ('dirt', (130, 92, 62)), ('podzol', (90, 62, 30)), ('hay', (200, 170, 20)), ('water', (50, 90, 200)),
    ('lava', (230, 100, 20)), ('cactus', (60, 120, 50)), ('white', (235, 235, 235)), ('light_gray', (160, 160, 160)),
    ('gray', (80, 84, 88)), ('black', (24, 24, 28)), ('red', (170, 50, 40)), ('orange', (216, 120, 30)),
    ('yellow', (236, 200, 50)), ('lime', (120, 190, 40)), ('green', (80, 110, 40)), ('cyan', (30, 140, 150)),
    ('light_blue', (80, 170, 220)), ('blue', (50, 70, 170)), ('purple', (120, 60, 160)),
    ('magenta', (180, 70, 180)), ('pink', (230, 140, 170)), ('brown', (110, 76, 50)),
    ('bookshelf', (130, 100, 60)), ('crafting', (140, 100, 60)), ('barrel', (120, 88, 50)),
    ('chest', (150, 105, 40)), ('furnace', (110, 110, 110)), ('anvil', (60, 60, 64)), ('bed', (180, 40, 40)),
    ('carpet', (170, 50, 40)), ('banner', (30, 30, 30)), ('bell', (240, 200, 60)), ('chain', (60, 60, 70)),
    ('ladder', (140, 110, 60)), ('snow', (245, 248, 250)), ('ice', (150, 190, 240)), ('end_rod', (240, 240, 240)),
    ('obsidian', (24, 18, 40)), ('netherrack', (110, 50, 50)), ('rail', (130, 120, 110)), ('wool', (220, 220, 220)),
    ('concrete', (200, 200, 200)), ('rod', (180, 180, 190)), ('cauldron', (60, 60, 70)), ('pot', (150, 80, 60)),
]
def color_of(name):
    for k, c in COLORS:
        if k in name:
            # Farbfamilie + Material (z.B. gray_concrete)
            return c
    h = abs(hash(name)) % 150 + 60
    return (h, h, h)

def shape_of(name, props):
    if name.endswith('_slab'):
        t = props.get('type', 'bottom')
        return {'bottom': (0, .5), 'top': (.5, 1), 'double': (0, 1)}[t], 1.0
    if name.endswith('_fence') or name.endswith('_wall') or name == 'iron_bars' or name.endswith('_pane'):
        return (0, 1), 0.3
    if any(k in name for k in ('torch', 'lantern', 'candle', 'end_rod', 'lightning_rod', 'flower', 'pot', 'poppy', 'bush', 'fern', 'sapling', 'tulip', 'dandelion', 'orchid', 'rose', 'azalea')):
        return (0, .55), 0.26
    if 'carpet' in name or 'pressure_plate' in name or name.endswith('rail'):
        return (0, .08), 1.0
    if 'door' in name and 'trap' not in name:
        return (0, 1), 0.35
    if 'trapdoor' in name:
        return (0, 1), 0.2 if props.get('open') == 'true' else 1.0
    if name.endswith('_bed'):
        return (0, .55), 1.0
    if name == 'ladder' or name.endswith('banner') or 'sign' in name:
        return (0, 1), 0.2
    if name in ('campfire', 'anvil', 'cauldron', 'chest', 'barrel_'):
        return (0, .6), 0.8
    return (0, 1), 1.0

TRANSPARENT = ('glass', 'pane', 'bars', 'leaves', 'fence', '_wall', 'torch', 'lantern', 'door', 'ladder', 'water')

def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)

def render(path, out, scale=None, maxpx=900, title=None, ground=0, bg=((196, 222, 245), (234, 244, 252))):
    w, h, l, blocks = load_schem(path)
    # Untergrund ausblenden, stattdessen Grasplatte
    blocks = {(x, y - ground + 1, z): b for (x, y, z), b in blocks.items() if y >= ground}
    for x in range(-1, w + 1):
        for z in range(-1, l + 1):
            if (x, 1, z) not in blocks or True:
                blocks.setdefault((x, 0, z), 'minecraft:grass_block')
    h = max(y for (_, y, _) in blocks) + 1
    w += 2; l += 2
    blocks = {(x + 1, y, z + 1): b for (x, y, z), b in blocks.items()}
    # Boden-Plattform: dünne Grasplatte als Orientierung (nur über Y>=ground sichtbar machen wir nichts extra)
    parsed = {}
    for pos, blk in blocks.items():
        m = re.match(r'minecraft:([a-z_0-9]+)(?:\[(.*)\])?$', blk)
        props = dict(kv.split('=') for kv in m.group(2).split(',')) if m.group(2) else {}
        parsed[pos] = (m.group(1), props)
    ss = 2
    span_x = (w + l) * 0.866
    span_y = (w + l) * 0.5 + h
    S = scale or max(4, min(22, int(maxpx / max(span_x, span_y * 1.0))))
    W = int((w + l) * 0.866 * S + 60); H = int(((w + l) * 0.5 + h) * S + 60)
    img = Image.new('RGB', (W * ss, H * ss), bg[0])
    d = ImageDraw.Draw(img)
    for yy in range(H * ss):  # Himmel-Verlauf
        t = yy / (H * ss)
        d.line([(0, yy), (W * ss, yy)], fill=tuple(int(bg[0][i] * (1 - t) + bg[1][i] * t) for i in range(3)))
    ox = (l * 0.866) * S + 30; oy = (h) * S + 30
    def proj(x, y, z):
        return ((x - z) * 0.866 * S + ox) * ss, (((x + z) * 0.5 - y) * S + oy) * ss
    # Bodenfläche
    gy = 0
    ground = None
    items = sorted(parsed.items(), key=lambda kv: (kv[0][0] + kv[0][2] + kv[0][1] * 1.0, kv[0][1]))
    def opaque(pos):
        p = parsed.get(pos)
        if not p: return False
        n, pr = p
        if any(k in n for k in TRANSPARENT): return False
        return shape_of(n, pr) == ((0, 1), 1.0)
    for (x, y, z), (n, pr) in items:
        (y0, y1), wd = shape_of(n, pr)
        c = color_of(n)
        inset = (1 - wd) / 2
        x0, x1, z0, z1 = x + inset, x + 1 - inset, z + inset, z + 1 - inset
        by0, by1 = y + y0, y + y1
        if 'door' in n and 'trap' not in n:
            f = pr.get('facing', 'north')
            if f in ('north', 'south'): x0, x1, z0, z1 = x, x + 1, z + .35, z + .65
            else: x0, x1, z0, z1 = x + .35, x + .65, z, z + 1
        # Dach: oben
        faces = []
        full = (wd == 1.0 and y0 == 0 and y1 == 1)
        if not (full and opaque((x, y + 1, z))): faces.append(('top', 1.0))
        if not (full and opaque((x, y, z + 1))): faces.append(('south', 0.8))
        if not (full and opaque((x + 1, y, z))): faces.append(('east', 0.62))
        for f, br in faces:
            if f == 'top':
                pts = [proj(x0, by1, z0), proj(x1, by1, z0), proj(x1, by1, z1), proj(x0, by1, z1)]
            elif f == 'south':
                pts = [proj(x0, by1, z1), proj(x1, by1, z1), proj(x1, by0, z1), proj(x0, by0, z1)]
            else:
                pts = [proj(x1, by1, z0), proj(x1, by1, z1), proj(x1, by0, z1), proj(x1, by0, z0)]
            col = shade(c, br)
            d.polygon(pts, fill=col)
            edge = shade(c, br * 0.82)
            d.line(pts + [pts[0]], fill=edge, width=1)
    img = img.resize((W, H), Image.LANCZOS)
    if title:
        dd = ImageDraw.Draw(img)
        try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        except Exception: f = ImageFont.load_default()
        dd.rectangle([0, 0, W, 30], fill=(30, 30, 34))
        dd.text((10, 5), title, fill=(255, 255, 255), font=f)
    img.save(out)
    return img

def sheet(images, out, cols=3, cell=(520, 400), title=None, labels=None):
    rows = math.ceil(len(images) / cols)
    th = 44 if title else 0
    S = Image.new('RGB', (cols * cell[0], rows * cell[1] + th), (24, 24, 28))
    dr = ImageDraw.Draw(S)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    except Exception:
        f = f2 = ImageFont.load_default()
    if title: dr.text((14, 8), title, fill=(255, 255, 255), font=f)
    for i, im in enumerate(images):
        r, c = divmod(i, cols)
        im = im.copy(); im.thumbnail((cell[0] - 8, cell[1] - 30))
        x = c * cell[0] + (cell[0] - im.width) // 2
        y = th + r * cell[1] + 4 + (cell[1] - 30 - im.height) // 2
        S.paste(im, (x, y))
        if labels: dr.text((c * cell[0] + 10, th + r * cell[1] + cell[1] - 24), labels[i], fill=(220, 220, 220), font=f2)
    S.save(out)
