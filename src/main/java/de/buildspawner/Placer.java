package de.buildspawner;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.block.data.BlockData;
import org.bukkit.entity.Player;
import org.bukkit.scheduler.BukkitRunnable;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/** Setzt Schematics Tick für Tick und merkt sich Undo-Daten. */
final class Placer {
    private record Undo(World world, int[] xs, int[] ys, int[] zs, BlockData[] old, int count) {}

    private final BuildSpawnerPlugin plugin;
    private final Map<UUID, Deque<Undo>> undo = new HashMap<>();
    private final Map<UUID, Boolean> busy = new HashMap<>();

    Placer(BuildSpawnerPlugin plugin) { this.plugin = plugin; }

    static int[] dims(Schematic s, int rot) {
        return rot % 2 == 0 ? new int[]{s.width, s.length} : new int[]{s.length, s.width};
    }

    private BlockData[] palette(Schematic s, int rot) {
        BlockData[] out = new BlockData[s.palette.length];
        int failed = 0;
        for (int i = 0; i < out.length; i++) {
            String st = s.palette[i];
            if (st == null) continue;
            try {
                out[i] = Bukkit.createBlockData(Rotator.rotate(st, rot));
            } catch (IllegalArgumentException e) {
                failed++;
                plugin.getLogger().fine("Unbekannter Block übersprungen: " + st);
            }
        }
        if (failed > 0) plugin.getLogger().warning(failed + " unbekannte Blocktypen wurden übersprungen (siehe Debug-Log).");
        return out;
    }

    boolean isBusy(Player p) { return busy.getOrDefault(p.getUniqueId(), false); }

    /**
     * @param target  angeklickter Block
     * @param yOffset Welt-Y der Schematic-Ebene 0 relativ zum angeklickten Block (Gebäude: -ground, eigene: +1)
     * @return false, wenn nichts gestartet wurde
     */
    boolean place(Player p, Block target, Schematic s, int yOffset, int rot) {
        int max = plugin.getConfig().getInt("max-blocks", 100000);
        if (s.volume() > max) { Msg.send(p, "<red>Das Gebäude ist zu groß (" + s.volume() + " > " + max + " Blöcke)."); return false; }
        if (isBusy(p)) { Msg.send(p, "<yellow>Es wird noch ein Gebäude platziert – einen Moment."); return false; }
        if (plugin.getConfig().getStringList("disabled-worlds").contains(target.getWorld().getName())) {
            Msg.send(p, "<red>In dieser Welt ist das Platzieren deaktiviert."); return false;
        }
        final World world = target.getWorld();
        final boolean pasteAir = plugin.getConfig().getBoolean("paste-air", true);
        final int perTick = Math.max(200, plugin.getConfig().getInt("max-blocks-per-tick", 3000));
        final BlockData[] data = palette(s, rot);
        int[] d = dims(s, rot);
        final int ox = target.getX() - d[0] / 2;
        final int oz = target.getZ() - d[1] / 2;
        final int oy = target.getY() + yOffset;
        final int n = s.volume();
        final int minY = world.getMinHeight(), maxY = world.getMaxHeight();
        final int[] xs = new int[n], ys = new int[n], zs = new int[n];
        final BlockData[] old = new BlockData[n];
        busy.put(p.getUniqueId(), true);
        final UUID id = p.getUniqueId();

        new BukkitRunnable() {
            int i = 0, count = 0;
            @Override public void run() {
                int done = 0;
                try {
                    while (i < n && done < perTick) {
                        int idx = i++;
                        int st = s.blocks[idx];
                        BlockData bd = st < data.length ? data[st] : null;
                        if (bd == null) continue;
                        if (!pasteAir && s.air[st]) continue;
                        int x = idx % s.width;
                        int z = (idx / s.width) % s.length;
                        int y = idx / (s.width * s.length);
                        int[] r = Rotator.rotatePos(x, z, s.width, s.length, rot);
                        int wx = ox + r[0], wy = oy + y, wz = oz + r[1];
                        if (wy < minY || wy >= maxY) continue;
                        Block b = world.getBlockAt(wx, wy, wz);
                        BlockData prev = b.getBlockData();
                        if (prev.equals(bd)) continue;
                        xs[count] = wx; ys[count] = wy; zs[count] = wz; old[count] = prev; count++;
                        b.setBlockData(bd, false);
                        done++;
                    }
                } catch (RuntimeException e) {
                    plugin.getLogger().warning("Fehler beim Platzieren: " + e);
                    i = n;
                }
                if (i >= n) {
                    cancel();
                    busy.remove(id);
                    Deque<Undo> dq = undo.computeIfAbsent(id, k -> new ArrayDeque<>());
                    dq.push(new Undo(world, xs, ys, zs, old, count));
                    while (dq.size() > Math.max(1, plugin.getConfig().getInt("undo-steps", 5))) dq.removeLast();
                    Player pl = Bukkit.getPlayer(id);
                    if (pl != null) {
                        Msg.send(pl, "<green>Gebäude platziert <gray>(" + count + " Blöcke). <gray>Mit <white>/build undo <gray>rückgängig machen.");
                        pl.playSound(pl.getLocation(), Sound.BLOCK_ANVIL_PLACE, 0.6f, 1.2f);
                    }
                }
            }
        }.runTaskTimer(plugin, 0L, 1L);
        return true;
    }

    boolean undo(Player p) {
        Deque<Undo> dq = undo.get(p.getUniqueId());
        if (dq == null || dq.isEmpty()) { Msg.send(p, "<red>Nichts zum Rückgängigmachen."); return false; }
        if (isBusy(p)) { Msg.send(p, "<yellow>Es wird noch ein Gebäude platziert – einen Moment."); return false; }
        final Undo u = dq.pop();
        final int perTick = Math.max(200, plugin.getConfig().getInt("max-blocks-per-tick", 3000));
        busy.put(p.getUniqueId(), true);
        final UUID id = p.getUniqueId();
        new BukkitRunnable() {
            int i = u.count() - 1;
            @Override public void run() {
                int done = 0;
                while (i >= 0 && done < perTick) {
                    u.world().getBlockAt(u.xs()[i], u.ys()[i], u.zs()[i]).setBlockData(u.old()[i], false);
                    i--; done++;
                }
                if (i < 0) {
                    cancel(); busy.remove(id);
                    Player pl = Bukkit.getPlayer(id);
                    if (pl != null) Msg.send(pl, "<green>Gebäude entfernt, Gelände wiederhergestellt.");
                }
            }
        }.runTaskTimer(plugin, 0L, 1L);
        return true;
    }

    /** Zeigt den Umriss des Gebäudes kurz mit Partikeln. */
    void outline(Player p, Block target, Schematic s, int yOffset, int rot) {
        int[] d = dims(s, rot);
        final int x1 = target.getX() - d[0] / 2, z1 = target.getZ() - d[1] / 2;
        final int x2 = x1 + d[0], z2 = z1 + d[1];
        final int y1 = target.getY() + yOffset, y2 = y1 + s.height;
        final World w = target.getWorld();
        final UUID id = p.getUniqueId();
        new BukkitRunnable() {
            int ticks = 0;
            @Override public void run() {
                Player pl = Bukkit.getPlayer(id);
                if (pl == null || ++ticks > 12) { cancel(); return; }
                for (int y : new int[]{y1, y2}) {
                    for (int x = x1; x <= x2; x++) { dot(pl, w, x, y, z1); dot(pl, w, x, y, z2); }
                    for (int z = z1; z <= z2; z++) { dot(pl, w, x1, y, z); dot(pl, w, x2, y, z); }
                }
                for (int y = y1; y <= y2; y += 2) {
                    dot(pl, w, x1, y, z1); dot(pl, w, x2, y, z1); dot(pl, w, x1, y, z2); dot(pl, w, x2, y, z2);
                }
            }
        }.runTaskTimer(plugin, 0L, 10L);
    }

    private static void dot(Player p, World w, int x, int y, int z) {
        p.spawnParticle(Particle.END_ROD, new Location(w, x, y, z), 1, 0, 0, 0, 0);
    }
}
