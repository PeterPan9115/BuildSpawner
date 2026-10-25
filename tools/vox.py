"""Voxel-Kern: Blöcke setzen, Stairs/Zäune automatisch verbinden, als Sponge-.schem exportieren."""
import gzip, struct, re

CW = ['north', 'east', 'south', 'west']
VEC = {'north': (0, -1), 'east': (1, 0), 'south': (0, 1), 'west': (-1, 0)}
def opp(f): return CW[(CW.index(f) + 2) % 4]
def ccw(f): return CW[(CW.index(f) - 1) % 4]
def cw(f): return CW[(CW.index(f) + 1) % 4]

def B(name, **p):
    s = 'minecraft:' + name
    if p:
        s += '[' + ','.join(f'{k}={str(v).lower()}' for k, v in p.items()) + ']'
    return s

def parse(blk):
    m = re.match(r'minecraft:([a-z_0-9]+)(?:\[(.*)\])?$', blk)
    name = m.group(1)
    props = {}
    if m.group(2):
        for kv in m.group(2).split(','):
            k, v = kv.split('=')
            props[k] = v
    return name, props

def unparse(name, props):
    return B(name, **props)

def stair(m, f, half='bottom', shape=None):
    p = dict(facing=f, half=half)
    if shape: p['shape'] = shape
    return B(m + '_stairs', **p)
def slab(m, t='bottom'): return B(m + '_slab', type=t)
def log(m, axis='y'): return B(m, axis=axis)
def door(m, f, half, hinge='left', open_=False): return B(m, facing=f, half=half, hinge=hinge, open=open_)
def trap(m, f, half='bottom', open_=False): return B(m, facing=f, half=half, open=open_)
def leaves(m): return B(m, persistent=True)
def bed(color, f, part): return B(color + '_bed', facing=f, part=part)
def chest(f): return B('chest', facing=f, type='single')
def wall_torch(f): return B('wall_torch', facing=f)
def lantern(hanging=False, soul=False): return B('soul_lantern' if soul else 'lantern', hanging=hanging)

AIR = 'minecraft:air'

NONSOLID = ('torch', 'lantern', 'door', 'trapdoor', 'carpet', 'plate', 'button', '_slab', '_stairs', 'fence',
            'pane', 'bars', '_wall', 'sign', 'banner', 'flower', 'pot', 'candle', 'ladder', 'vine', 'bed',
            'chest', 'water', 'lava', 'cactus', 'campfire', 'anvil', 'bell', 'cauldron', 'lever', 'rail',
            'head', 'skull', 'leaves', 'glass', 'air', 'poppy', 'dandelion', 'tulip', 'orchid', 'rose',
            'fern', 'grass', 'bush', 'sapling', 'lightning', 'end_rod', 'rod', 'hanging', 'lily', 'cake',
            'snow', 'azalea', 'amethyst_cluster', 'bud', 'dripstone', 'sea_pickle', 'lectern', 'enchanting',
            'brewing', 'grindstone', 'loom_', 'stonecutter', 'scaffolding', 'barrier', 'light')

def is_solid(blk):
    if blk is None: return False
    n = parse(blk)[0]
    if n.endswith('_block') or n.endswith('planks') or n.endswith('bricks') or n.endswith('concrete'):
        return True
    if any(k in n for k in NONSOLID):
        return False
    return True

class V:
    def __init__(s):
        s.b = {}
    def s(s, x, y, z, blk):
        s.b[(x, y, z)] = blk
    def get(s, x, y, z): return s.b.get((x, y, z))
    def rm(s, x, y, z): s.b.pop((x, y, z), None)
    def paste(s, o, dx, dy, dz):
        for (x, y, z), b in o.b.items():
            s.b[(x + dx, y + dy, z + dz)] = b
    def fill(s, x1, y1, z1, x2, y2, z2, blk):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    s.b[(x, y, z)] = blk
    def clear(s, x1, y1, z1, x2, y2, z2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    s.b.pop((x, y, z), None)
    def walls(s, x1, y1, z1, x2, y2, z2, blk):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if x in (x1, x2) or z in (z1, z2):
                        s.b[(x, y, z)] = blk
    def disc(s, cx, cz, r, y, blk, hollow=False):
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                d = (x - cx) ** 2 + (z - cz) ** 2
                if d <= r * r + r * 0.8 and (not hollow or d >= (r - 1) ** 2 + (r - 1) * 0.8 - 0.5):
                    s.b[(x, y, z)] = blk

    def mix(s, rules, seed=0):
        """Ersetzt Blöcke deterministisch durch passende Varianten (Blockpalette statt Einheitsblock)."""
        out = {}
        for (x, y, z), blk in s.b.items():
            n, p = parse(blk)
            r = rules.get(n)
            if r:
                h = ((x * 73856093) ^ (y * 19349663) ^ (z * 83492791) ^ (seed * 2654435761)) & 0xFFFFFFFF
                h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
                pick = (h ^ (h >> 16)) % sum(r.values())
                for name, wgt in r.items():
                    if pick < wgt:
                        blk = unparse(name, p); break
                    pick -= wgt
            out[(x, y, z)] = blk
        s.b = out

    # ------------------------------------------------------------ Nachbearbeitung
    def post(s):
        out = {}
        for (x, y, z), blk in s.b.items():
            n, p = parse(blk)
            if n.endswith('_stairs') and 'shape' not in p:
                p['shape'] = s._stair_shape(x, y, z, p)
                blk = unparse(n, p)
            elif (n.endswith('_fence') or n.endswith('_pane') or n == 'iron_bars' or n.endswith('_wall')) \
                    and not any(k in n for k in ('torch', 'sign', 'banner', 'skull', 'head')):
                for d in CW:
                    dx, dz = VEC[d]
                    nb = s.b.get((x + dx, y, z + dz))
                    conn = False
                    if nb:
                        nn = parse(nb)[0]
                        if n.endswith('_fence'):
                            conn = nn.endswith('_fence') or nn.endswith('_fence_gate') or is_solid(nb)
                        elif n.endswith('_wall'):
                            conn = nn.endswith('_wall') or is_solid(nb)
                        else:
                            conn = nn.endswith('_pane') or nn == 'iron_bars' or nn.endswith('_wall') or is_solid(nb)
                    if n.endswith('_wall'):
                        p[d] = 'low' if conn else 'none'
                    else:
                        p[d] = 'true' if conn else 'false'
                if n.endswith('_wall'):
                    p['up'] = 'true'
                blk = unparse(n, p)
            out[(x, y, z)] = blk
        s.b = out

    def _stair_shape(s, x, y, z, p):
        f, half = p['facing'], p['half']
        def same_stair(xx, yy, zz):
            b = s.b.get((xx, yy, zz))
            if b is None: return None
            n, q = parse(b)
            if not n.endswith('_stairs'): return None
            return q
        def can_take(d):
            dx, dz = VEC[d]
            q = same_stair(x + dx, y, z + dz)
            return q is None or q['facing'] != f or q['half'] != half
        fx, fz = VEC[f]
        q = same_stair(x + fx, y, z + fz)
        if q and q['half'] == half:
            d1 = q['facing']
            if CW.index(d1) % 2 != CW.index(f) % 2 and can_take(opp(d1)):
                return 'outer_left' if d1 == ccw(f) else 'outer_right'
        q = same_stair(x - fx, y, z - fz)
        if q and q['half'] == half:
            d2 = q['facing']
            if CW.index(d2) % 2 != CW.index(f) % 2 and can_take(d2):
                return 'inner_left' if d2 == ccw(f) else 'inner_right'
        return 'straight'

    # ------------------------------------------------------------ Export
    def bounds(s):
        xs = [k[0] for k in s.b]; ys = [k[1] for k in s.b]; zs = [k[2] for k in s.b]
        return min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)

    def export(s, path):
        """Schreibt Sponge-Schematic v2. Gibt (w,h,l,ground) zurück (ground = Index der Boden-Ebene y=0)."""
        s.post()
        x0, y0, z0, x1, y1, z1 = s.bounds()
        w, h, l = x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1
        pal = {AIR: 0}
        data = bytearray()
        arr = [0] * (w * h * l)
        for (x, y, z), blk in s.b.items():
            if blk not in pal: pal[blk] = len(pal)
            arr[(x - x0) + (z - z0) * w + (y - y0) * w * l] = pal[blk]
        for v in arr:
            while True:
                if v & ~0x7F:
                    data.append((v & 0x7F) | 0x80); v >>= 7
                else:
                    data.append(v); break
        root = {
            'Version': ('int', 2), 'DataVersion': ('int', 4800),
            'Width': ('short', w), 'Height': ('short', h), 'Length': ('short', l),
            'Offset': ('intarray', [0, 0, 0]),
            'PaletteMax': ('int', len(pal)),
            'Palette': ('compound', {k: ('int', v) for k, v in pal.items()}),
            'BlockData': ('bytearray', bytes(data)),
        }
        with gzip.open(path, 'wb') as fh:
            fh.write(_nbt_named('Schematic', ('compound', root)))
        return w, h, l, -y0

_ID = {'short': 2, 'int': 3, 'bytearray': 7, 'string': 8, 'compound': 10, 'intarray': 11}
def _nbt_payload(t, v):
    if t == 'int': return struct.pack('>i', v)
    if t == 'short': return struct.pack('>h', v)
    if t == 'string':
        b = v.encode('utf-8'); return struct.pack('>H', len(b)) + b
    if t == 'bytearray': return struct.pack('>i', len(v)) + v
    if t == 'intarray': return struct.pack('>i', len(v)) + b''.join(struct.pack('>i', i) for i in v)
    if t == 'compound':
        out = b''
        for k, (tt, vv) in v.items():
            out += bytes([_ID[tt]]) + _nbt_payload('string', k) + _nbt_payload(tt, vv)
        return out + b'\x00'
    raise ValueError(t)
def _nbt_named(name, tv):
    t, v = tv
    return bytes([_ID[t]]) + _nbt_payload('string', name) + _nbt_payload(t, v)
