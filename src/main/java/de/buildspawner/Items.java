package de.buildspawner;

import net.kyori.adventure.text.Component;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.persistence.PersistentDataContainer;
import org.bukkit.persistence.PersistentDataType;

import java.util.ArrayList;
import java.util.List;

/** Erzeugt und liest die Platzier-Items (Daten liegen im PersistentDataContainer). */
final class Items {
    private final NamespacedKey keyBuild, keySchem, keyRot;
    private final BuildSpawnerPlugin plugin;

    Items(BuildSpawnerPlugin plugin) {
        this.plugin = plugin;
        keyBuild = new NamespacedKey(plugin, "build");
        keySchem = new NamespacedKey(plugin, "schem");
        keyRot = new NamespacedKey(plugin, "rot");
    }

    ItemStack buildItem(BuildRegistry.Build b, String color, String catName) {
        ItemStack it = new ItemStack(b.icon());
        ItemMeta m = it.getItemMeta();
        m.displayName(Msg.plain(color + "<bold>" + b.name()));
        m.lore(loreFor(catName, b.desc(), b.w() + "x" + b.l() + " Blöcke, " + b.h() + " hoch"));
        m.setEnchantmentGlintOverride(true);
        PersistentDataContainer pdc = m.getPersistentDataContainer();
        pdc.set(keyBuild, PersistentDataType.STRING, b.key());
        pdc.set(keyRot, PersistentDataType.INTEGER, 0);
        it.setItemMeta(m);
        return it;
    }

    ItemStack schematicItem(String file, Material mat) {
        ItemStack it = new ItemStack(mat);
        bindSchematic(it, file);
        return it;
    }

    /** Bindet eine Schematic an ein beliebiges Item (Name bleibt erhalten, falls vorhanden). */
    void bindSchematic(ItemStack it, String file) {
        ItemMeta m = it.getItemMeta();
        if (!m.hasDisplayName()) m.displayName(Msg.plain("<aqua><bold>" + file));
        List<Component> lore = new ArrayList<>();
        lore.add(Msg.plain("<gray>Eigene Schematic: <white>" + file));
        lore.addAll(usage());
        m.lore(lore);
        m.setEnchantmentGlintOverride(true);
        PersistentDataContainer pdc = m.getPersistentDataContainer();
        pdc.remove(keyBuild);
        pdc.set(keySchem, PersistentDataType.STRING, file);
        pdc.set(keyRot, PersistentDataType.INTEGER, 0);
        it.setItemMeta(m);
    }

    private List<Component> loreFor(String cat, String desc, String size) {
        List<Component> l = new ArrayList<>();
        l.add(Msg.plain("<dark_gray>" + cat));
        l.add(Msg.plain("<gray>" + desc));
        l.add(Msg.plain("<dark_gray>" + size));
        l.add(Component.empty());
        l.addAll(usage());
        return l;
    }

    private List<Component> usage() {
        return List.of(
                Msg.plain("<yellow>Rechtsklick<gray> auf Boden: platzieren"),
                Msg.plain("<yellow>Linksklick<gray>: um 90° drehen"),
                Msg.plain("<yellow>Schleichen + Rechtsklick<gray>: Umriss zeigen"));
    }

    String buildKey(ItemStack it) { return read(it, keyBuild); }
    String schemFile(ItemStack it) { return read(it, keySchem); }
    boolean isPlaceItem(ItemStack it) { return buildKey(it) != null || schemFile(it) != null; }

    private String read(ItemStack it, NamespacedKey k) {
        if (it == null || !it.hasItemMeta()) return null;
        return it.getItemMeta().getPersistentDataContainer().get(k, PersistentDataType.STRING);
    }

    int rotation(ItemStack it) {
        if (it == null || !it.hasItemMeta()) return 0;
        Integer r = it.getItemMeta().getPersistentDataContainer().get(keyRot, PersistentDataType.INTEGER);
        return r == null ? 0 : ((r % 4) + 4) % 4;
    }

    void setRotation(ItemStack it, int rot) {
        ItemMeta m = it.getItemMeta();
        m.getPersistentDataContainer().set(keyRot, PersistentDataType.INTEGER, ((rot % 4) + 4) % 4);
        it.setItemMeta(m);
    }
}
