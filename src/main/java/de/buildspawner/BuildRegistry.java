package de.buildspawner;

import org.bukkit.Material;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** Lädt Kategorien/Gebäude aus builds/index.txt und verwaltet Schematic-Caches. */
final class BuildRegistry {
    record Build(String cat, String id, String name, String desc, Material icon, int w, int h, int l, int ground) {
        String key() { return cat + ":" + id; }
    }

    record Category(String id, String name, Material icon, String color, String desc, List<Build> builds) {}

    private final BuildSpawnerPlugin plugin;
    private final Map<String, Category> categories = new LinkedHashMap<>();
    private final Map<String, Build> byKey = new HashMap<>();
    private final Map<String, Schematic> builtinCache = new HashMap<>();
    private final Map<File, Schematic> fileCache = new HashMap<>();

    BuildRegistry(BuildSpawnerPlugin plugin) { this.plugin = plugin; }

    void load() {
        categories.clear(); byKey.clear(); builtinCache.clear(); fileCache.clear();
        try (InputStream in = plugin.getResource("builds/index.txt")) {
            if (in == null) { plugin.getLogger().severe("builds/index.txt fehlt im Plugin!"); return; }
            BufferedReader r = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8));
            String line;
            while ((line = r.readLine()) != null) {
                if (line.isBlank()) continue;
                String[] p = line.split("\\|");
                if (p[0].equals("C") && p.length >= 6) {
                    categories.put(p[1], new Category(p[1], p[2], mat(p[3]), p[4], p[5], new ArrayList<>()));
                } else if (p[0].equals("B") && p.length >= 10) {
                    Category c = categories.get(p[1]);
                    if (c == null) continue;
                    Build b = new Build(p[1], p[2], p[3], p[4], mat(p[5]), Integer.parseInt(p[6]), Integer.parseInt(p[7]),
                            Integer.parseInt(p[8]), Integer.parseInt(p[9]));
                    c.builds().add(b);
                    byKey.put(b.key(), b);
                }
            }
        } catch (IOException | RuntimeException e) {
            plugin.getLogger().severe("Konnte Index nicht laden: " + e);
        }
        plugin.getLogger().info(byKey.size() + " Gebäude in " + categories.size() + " Kategorien geladen.");
    }

    private static Material mat(String name) {
        Material m = Material.matchMaterial(name);
        return (m == null || !m.isItem()) ? Material.PAPER : m;
    }

    List<Category> categories() { return new ArrayList<>(categories.values()); }
    Category category(String id) { return categories.get(id); }
    Build build(String key) { return byKey.get(key); }
    int buildCount() { return byKey.size(); }

    Schematic schematic(Build b) {
        return builtinCache.computeIfAbsent(b.key(), k -> {
            try (InputStream in = plugin.getResource("builds/" + b.cat() + "/" + b.id() + ".schem")) {
                if (in == null) return null;
                return Schematic.load(in);
            } catch (IOException | RuntimeException e) {
                plugin.getLogger().warning("Schematic " + k + " defekt: " + e.getMessage());
                return null;
            }
        });
    }

    // ---------------------------------------------------------------- eigene Schematics
    List<File> folders() {
        List<File> out = new ArrayList<>();
        File own = new File(plugin.getDataFolder(), "schematics");
        own.mkdirs();
        out.add(own);
        File plugins = plugin.getDataFolder().getParentFile();
        if (plugins != null) {
            out.add(new File(plugins, "WorldEdit/schematics"));
            out.add(new File(plugins, "FastAsyncWorldEdit/schematics"));
        }
        for (String s : plugin.getConfig().getStringList("extra-schematic-folders")) out.add(new File(s));
        out.removeIf(f -> !f.isDirectory());
        return out;
    }

    List<File> schematicFiles() {
        List<File> out = new ArrayList<>();
        for (File f : folders()) {
            File[] arr = f.listFiles((d, n) -> n.toLowerCase(Locale.ROOT).endsWith(".schem"));
            if (arr != null) out.addAll(List.of(arr));
        }
        out.sort(Comparator.comparing(f -> f.getName().toLowerCase(Locale.ROOT)));
        return out;
    }

    File findSchematic(String name) {
        for (File f : schematicFiles()) if (f.getName().equalsIgnoreCase(name)) return f;
        return null;
    }

    Schematic schematic(File f) {
        long mod = f.lastModified();
        Schematic cached = fileCache.get(f);
        if (cached != null && cacheStamp.getOrDefault(f, 0L) == mod) return cached;
        try (InputStream in = Files.newInputStream(f.toPath())) {
            Schematic s = Schematic.load(in);
            fileCache.put(f, s); cacheStamp.put(f, mod);
            return s;
        } catch (IOException | RuntimeException e) {
            plugin.getLogger().warning("Schematic " + f.getName() + " konnte nicht geladen werden: " + e.getMessage());
            return null;
        }
    }
    private final Map<File, Long> cacheStamp = new HashMap<>();
}
