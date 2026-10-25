package de.buildspawner;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.zip.GZIPInputStream;

/** Minimaler NBT-Leser (gzip). Gibt verschachtelte Maps/Listen zurück. */
final class Nbt {
    private Nbt() {}

    static Map<String, Object> read(InputStream raw) throws IOException {
        try (DataInputStream in = new DataInputStream(new BufferedInputStream(new GZIPInputStream(raw)))) {
            int type = in.readUnsignedByte();
            if (type != 10) throw new IOException("Keine gültige NBT-Datei (Root ist kein Compound)");
            in.readUTF();
            return compound(in);
        }
    }

    private static Map<String, Object> compound(DataInputStream in) throws IOException {
        Map<String, Object> map = new HashMap<>();
        while (true) {
            int type = in.readUnsignedByte();
            if (type == 0) return map;
            String key = in.readUTF();
            map.put(key, payload(in, type));
        }
    }

    private static Object payload(DataInputStream in, int type) throws IOException {
        switch (type) {
            case 1: return in.readByte();
            case 2: return in.readShort();
            case 3: return in.readInt();
            case 4: return in.readLong();
            case 5: return in.readFloat();
            case 6: return in.readDouble();
            case 7: {
                byte[] b = new byte[in.readInt()];
                in.readFully(b);
                return b;
            }
            case 8: return in.readUTF();
            case 9: {
                int t = in.readUnsignedByte();
                int n = in.readInt();
                List<Object> list = new ArrayList<>(Math.max(0, n));
                for (int i = 0; i < n; i++) list.add(payload(in, t));
                return list;
            }
            case 10: return compound(in);
            case 11: {
                int[] a = new int[in.readInt()];
                for (int i = 0; i < a.length; i++) a[i] = in.readInt();
                return a;
            }
            case 12: {
                long[] a = new long[in.readInt()];
                for (int i = 0; i < a.length; i++) a[i] = in.readLong();
                return a;
            }
            default: throw new IOException("Unbekannter NBT-Tag: " + type);
        }
    }
}
