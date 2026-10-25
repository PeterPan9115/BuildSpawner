package de.buildspawner;

import java.io.IOException;
import java.io.InputStream;
import java.util.Map;

/** Sponge-Schematic (.schem) Version 2 und 3. */
final class Schematic {
    final int width, height, length;
    final int[] blocks;      // Index = x + z*width + y*width*length
    final String[] palette;  // Palette-ID -> Blockstate-String
    final boolean[] air;

    private Schematic(int w, int h, int l, int[] blocks, String[] palette) {
        this.width = w; this.height = h; this.length = l;
        this.blocks = blocks; this.palette = palette;
        this.air = new boolean[palette.length];
        for (int i = 0; i < palette.length; i++) {
            String p = palette[i];
            air[i] = p != null && (p.startsWith("minecraft:air") || p.startsWith("minecraft:cave_air") || p.startsWith("minecraft:void_air"));
        }
    }

    int volume() { return width * height * length; }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> map(Object o) { return (Map<String, Object>) o; }

    private static int num(Map<String, Object> m, String k) {
        Object o = m.get(k);
        if (!(o instanceof Number)) throw new IllegalArgumentException("Feld fehlt: " + k);
        return ((Number) o).intValue();
    }

    static Schematic load(InputStream in) throws IOException {
        Map<String, Object> root = Nbt.read(in);
        if (root.containsKey("Schematic")) root = map(root.get("Schematic"));
        if (!root.containsKey("Width")) throw new IOException("Nicht unterstütztes Format (nur Sponge .schem v2/v3)");
        int version = root.get("Version") instanceof Number n ? n.intValue() : 2;
        int w = num(root, "Width"), h = num(root, "Height"), l = num(root, "Length");
        Map<String, Object> pal;
        byte[] data;
        if (version >= 3) {
            Map<String, Object> blocks = map(root.get("Blocks"));
            pal = map(blocks.get("Palette"));
            data = (byte[]) blocks.get("Data");
        } else {
            pal = map(root.get("Palette"));
            data = (byte[]) root.get("BlockData");
        }
        if (pal == null || data == null) throw new IOException("Schematic enthält keine Blockdaten");
        int max = 0;
        for (Object v : pal.values()) max = Math.max(max, ((Number) v).intValue());
        String[] palette = new String[max + 1];
        for (Map.Entry<String, Object> e : pal.entrySet()) palette[((Number) e.getValue()).intValue()] = e.getKey();
        int total = w * h * l;
        int[] blocks = new int[total];
        int pos = 0;
        for (int i = 0; i < total; i++) {
            int value = 0, shift = 0;
            while (true) {
                if (pos >= data.length) throw new IOException("Blockdaten zu kurz");
                int b = data[pos++];
                value |= (b & 0x7F) << shift;
                if ((b & 0x80) == 0) break;
                shift += 7;
            }
            blocks[i] = value;
        }
        return new Schematic(w, h, l, blocks, palette);
    }
}
