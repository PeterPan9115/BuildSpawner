package de.buildspawner;

import java.util.LinkedHashMap;
import java.util.Map;

/** Dreht Blockstate-Strings um Vielfache von 90° im Uhrzeigersinn (von oben gesehen). */
final class Rotator {
    private Rotator() {}

    private static final String[] DIRS = {"north", "east", "south", "west"};

    private static int idx(String d) {
        for (int i = 0; i < 4; i++) if (DIRS[i].equals(d)) return i;
        return -1;
    }

    static String rotate(String state, int quarter) {
        quarter = ((quarter % 4) + 4) % 4;
        if (quarter == 0) return state;
        int br = state.indexOf('[');
        if (br < 0 || !state.endsWith("]")) return state;
        String name = state.substring(0, br);
        String[] kv = state.substring(br + 1, state.length() - 1).split(",");
        Map<String, String> props = new LinkedHashMap<>();
        for (String s : kv) {
            int eq = s.indexOf('=');
            if (eq > 0) props.put(s.substring(0, eq), s.substring(eq + 1));
        }
        Map<String, String> out = new LinkedHashMap<>(props);
        for (Map.Entry<String, String> e : props.entrySet()) {
            String k = e.getKey(), v = e.getValue();
            switch (k) {
                case "facing": {
                    int i = idx(v);
                    if (i >= 0) out.put(k, DIRS[(i + quarter) % 4]);
                    break;
                }
                case "rotation": {
                    try { out.put(k, String.valueOf((Integer.parseInt(v) + quarter * 4) % 16)); } catch (NumberFormatException ignored) {}
                    break;
                }
                case "axis": {
                    if (quarter % 2 == 1) {
                        if (v.equals("x")) out.put(k, "z");
                        else if (v.equals("z")) out.put(k, "x");
                    }
                    break;
                }
                case "north": case "east": case "south": case "west": {
                    int i = idx(k);
                    out.put(DIRS[(i + quarter) % 4], v);
                    break;
                }
                default: break;
            }
        }
        StringBuilder sb = new StringBuilder(name).append('[');
        boolean first = true;
        for (Map.Entry<String, String> e : out.entrySet()) {
            if (!first) sb.append(',');
            sb.append(e.getKey()).append('=').append(e.getValue());
            first = false;
        }
        return sb.append(']').toString();
    }

    /** Dreht eine Position (x,z) innerhalb einer w*l-Box um quarter Schritte; Ergebnis: {x', z'}. */
    static int[] rotatePos(int x, int z, int w, int l, int quarter) {
        quarter = ((quarter % 4) + 4) % 4;
        for (int i = 0; i < quarter; i++) {
            int nx = (l - 1) - z;
            int nz = x;
            x = nx; z = nz;
            int t = w; w = l; l = t;
        }
        return new int[]{x, z};
    }
}
