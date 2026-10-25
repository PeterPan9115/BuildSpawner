package de.buildspawner;

import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.ClickType;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import java.util.function.IntConsumer;

/** Alle Menüs: Hauptmenü, Kategorien, eigene Schematics. */
final class Menus implements Listener {
    static final class Holder implements InventoryHolder {
        Inventory inv;
        final Map<Integer, Consumer<ClickType>> actions = new HashMap<>();
        @Override public Inventory getInventory() { return inv; }
    }

    private record Entry(ItemStack icon, Consumer<ClickType> action) {}

    private final BuildSpawnerPlugin plugin;

    Menus(BuildSpawnerPlugin plugin) { this.plugin = plugin; }

    // ------------------------------------------------------------------ Hilfen
    private ItemStack icon(Material m, String name, String... lore) {
        ItemStack it = new ItemStack(m);
        ItemMeta meta = it.getItemMeta();
        meta.displayName(Msg.plain(name));
        List<Component> l = new ArrayList<>();
        for (String s : lore) l.add(Msg.plain(s));
        if (!l.isEmpty()) meta.lore(l);
        it.setItemMeta(meta);
        return it;
    }

    private Holder holder(Inventory[] out, int size, Component title) {
        Holder h = new Holder();
        h.inv = Bukkit.createInventory(h, size, title);
        out[0] = h.inv;
        ItemStack filler = icon(Material.GRAY_STAINED_GLASS_PANE, " ");
        for (int i = 0; i < size; i++) h.inv.setItem(i, filler);
        return h;
    }

    private void later(Runnable r) { Bukkit.getScheduler().runTask(plugin, r); }

    void give(Player p, ItemStack it) {
        Map<Integer, ItemStack> left = p.getInventory().addItem(it);
        for (ItemStack rest : left.values()) p.getWorld().dropItem(p.getLocation(), rest);
        p.playSound(p.getLocation(), org.bukkit.Sound.ENTITY_ITEM_PICKUP, 0.8f, 1.1f);
    }

    // ------------------------------------------------------------------ Hauptmenü
    void openMain(Player p) {
        Inventory[] ref = new Inventory[1];
        Holder h = holder(ref, 54, Msg.mm("<gradient:#f6c177:#eb6f92><bold>Build-Menü</bold></gradient>"));
        int[] slots = {10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34};
        int i = 0;
        for (BuildRegistry.Category c : plugin.registry().categories()) {
            if (i >= slots.length) break;
            int slot = slots[i++];
            h.inv.setItem(slot, icon(c.icon(), c.color() + "<bold>" + c.name(),
                    "<gray>" + c.desc(), "<dark_gray>" + c.builds().size() + " Gebäude", "", "<yellow>Klicken zum Öffnen"));
            h.actions.put(slot, click -> later(() -> openCategory(p, c, 0)));
        }
        if (p.hasPermission("buildspawner.schematics")) {
            h.inv.setItem(46, icon(Material.FILLED_MAP, "<aqua><bold>Eigene Schematics",
                    "<gray>Schematic wählen und als Item nutzen", "<gray>oder an ein Item in deiner Hand binden", "", "<yellow>Klicken zum Öffnen"));
            h.actions.put(46, click -> later(() -> openSchematics(p, 0)));
        }
        h.inv.setItem(49, icon(Material.BARRIER, "<red>Schließen"));
        h.actions.put(49, click -> later(p::closeInventory));
        h.inv.setItem(52, icon(Material.CLOCK, "<gold><bold>Rückgängig", "<gray>Letztes platziertes Gebäude entfernen"));
        h.actions.put(52, click -> later(() -> { p.closeInventory(); plugin.placer().undo(p); }));
        p.openInventory(h.inv);
    }

    // ------------------------------------------------------------------ Kategorie
    void openCategory(Player p, BuildRegistry.Category c, int page) {
        List<Entry> entries = new ArrayList<>();
        for (BuildRegistry.Build b : c.builds()) {
            ItemStack ic = icon(b.icon(), c.color() + "<bold>" + b.name(), "<gray>" + b.desc(),
                    "<dark_gray>" + b.w() + "x" + b.l() + " Blöcke, " + b.h() + " hoch", "", "<yellow>Klick<gray>: Item erhalten");
            entries.add(new Entry(ic, click -> later(() -> {
                give(p, plugin.items().buildItem(b, c.color(), c.name()));
                Msg.send(p, "<green>" + b.name() + " <gray>erhalten. Rechtsklick auf den Boden zum Platzieren.");
                p.closeInventory();
            })));
        }
        openList(p, Msg.mm(c.color() + "<bold>" + c.name()), entries, page, () -> openMain(p), np -> openCategory(p, c, np));
    }

    // ------------------------------------------------------------------ Eigene Schematics
    void openSchematics(Player p, int page) {
        if (!p.hasPermission("buildspawner.schematics")) { Msg.send(p, "<red>Dafür fehlt dir die Berechtigung."); return; }
        List<Entry> entries = new ArrayList<>();
        for (File f : plugin.registry().schematicFiles()) {
            String name = f.getName();
            ItemStack ic = icon(Material.PAPER, "<aqua><bold>" + name, "<gray>" + (f.length() / 1024 + 1) + " KB",
                    "", "<yellow>Linksklick<gray>: neues Item erhalten",
                    "<yellow>Rechtsklick / Shift<gray>: an Item in deiner Hand binden");
            entries.add(new Entry(ic, click -> later(() -> {
                if (click == ClickType.RIGHT || click == ClickType.SHIFT_LEFT || click == ClickType.SHIFT_RIGHT) {
                    ItemStack hand = p.getInventory().getItemInMainHand();
                    if (hand.getType().isAir()) { Msg.send(p, "<red>Du hältst kein Item in der Hand."); return; }
                    plugin.items().bindSchematic(hand, name);
                    Msg.send(p, "<green>" + name + " <gray>an dein Item gebunden.");
                    p.closeInventory();
                } else {
                    Material mat = Material.matchMaterial(plugin.getConfig().getString("schematic-item", "PAPER"));
                    give(p, plugin.items().schematicItem(name, mat == null ? Material.PAPER : mat));
                    Msg.send(p, "<green>" + name + " <gray>erhalten.");
                    p.closeInventory();
                }
            })));
        }
        if (entries.isEmpty()) {
            Msg.send(p, "<yellow>Keine Schematics gefunden. Lege <white>.schem<yellow>-Dateien in <white>plugins/BuildSpawner/schematics/<yellow> (oder den WorldEdit-Ordner).");
        }
        openList(p, Msg.mm("<aqua><bold>Eigene Schematics"), entries, page, () -> openMain(p), np -> openSchematics(p, np));
    }

    // ------------------------------------------------------------------ gemeinsame Listenansicht
    private void openList(Player p, Component title, List<Entry> entries, int page, Runnable back, IntConsumer pager) {
        final int per = 45;
        int pages = Math.max(1, (entries.size() + per - 1) / per);
        page = Math.max(0, Math.min(page, pages - 1));
        Inventory[] ref = new Inventory[1];
        Holder h = holder(ref, 54, title);
        for (int i = 0; i < per; i++) h.inv.setItem(i, null);
        for (int i = 0; i < per && page * per + i < entries.size(); i++) {
            Entry e = entries.get(page * per + i);
            h.inv.setItem(i, e.icon());
            h.actions.put(i, e.action());
        }
        h.inv.setItem(45, icon(Material.ARROW, "<yellow>Zurück"));
        h.actions.put(45, click -> later(back));
        h.inv.setItem(49, icon(Material.PAPER, "<gray>Seite " + (page + 1) + " / " + pages));
        final int cur = page;
        if (page > 0) {
            h.inv.setItem(48, icon(Material.SPECTRAL_ARROW, "<yellow>Vorherige Seite"));
            h.actions.put(48, click -> later(() -> pager.accept(cur - 1)));
        }
        if (page < pages - 1) {
            h.inv.setItem(50, icon(Material.SPECTRAL_ARROW, "<yellow>Nächste Seite"));
            h.actions.put(50, click -> later(() -> pager.accept(cur + 1)));
        }
        h.inv.setItem(53, icon(Material.CLOCK, "<gold><bold>Rückgängig"));
        h.actions.put(53, click -> later(() -> { p.closeInventory(); plugin.placer().undo(p); }));
        p.openInventory(h.inv);
    }

    // ------------------------------------------------------------------ Events
    @EventHandler
    public void onClick(InventoryClickEvent e) {
        if (!(e.getInventory().getHolder() instanceof Holder h)) return;
        e.setCancelled(true);
        if (e.getClickedInventory() != e.getInventory()) return;
        Consumer<ClickType> a = h.actions.get(e.getSlot());
        if (a != null) a.accept(e.getClick());
    }

    @EventHandler
    public void onDrag(InventoryDragEvent e) {
        if (e.getInventory().getHolder() instanceof Holder) e.setCancelled(true);
    }
}
