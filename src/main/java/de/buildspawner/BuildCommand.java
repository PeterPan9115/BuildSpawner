package de.buildspawner;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

final class BuildCommand implements CommandExecutor, TabCompleter {
    private final BuildSpawnerPlugin plugin;

    BuildCommand(BuildSpawnerPlugin plugin) { this.plugin = plugin; }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] a) {
        if (a.length == 0) {
            if (!(sender instanceof Player p)) { Msg.send(sender, "Nur Spieler können das Menü öffnen."); return true; }
            if (!p.hasPermission("buildspawner.use")) { Msg.send(p, "<red>Dafür fehlt dir die Berechtigung."); return true; }
            plugin.menus().openMain(p);
            return true;
        }
        switch (a[0].toLowerCase(Locale.ROOT)) {
            case "undo" -> {
                if (sender instanceof Player p && p.hasPermission("buildspawner.use")) plugin.placer().undo(p);
                else Msg.send(sender, "<red>Nicht möglich.");
            }
            case "reload" -> {
                if (!sender.hasPermission("buildspawner.admin")) { Msg.send(sender, "<red>Dafür fehlt dir die Berechtigung."); return true; }
                plugin.reloadConfig();
                plugin.registry().load();
                Msg.send(sender, "<green>Neu geladen: " + plugin.registry().buildCount() + " Gebäude.");
            }
            case "schem" -> {
                if (!(sender instanceof Player p) || !p.hasPermission("buildspawner.schematics")) { Msg.send(sender, "<red>Dafür fehlt dir die Berechtigung."); return true; }
                if (a.length < 2) { Msg.send(p, "<gray>Benutzung: <white>/build schem [Datei]"); return true; }
                File f = plugin.registry().findSchematic(withExt(a[1]));
                if (f == null) { Msg.send(p, "<red>Schematic nicht gefunden."); return true; }
                Material m = Material.matchMaterial(plugin.getConfig().getString("schematic-item", "PAPER"));
                plugin.menus().give(p, plugin.items().schematicItem(f.getName(), m == null ? Material.PAPER : m));
                Msg.send(p, "<green>" + f.getName() + " <gray>erhalten.");
            }
            case "bind" -> {
                if (!(sender instanceof Player p) || !p.hasPermission("buildspawner.schematics")) { Msg.send(sender, "<red>Dafür fehlt dir die Berechtigung."); return true; }
                if (a.length < 2) { Msg.send(p, "<gray>Benutzung: <white>/build bind [Datei] <gray>(bindet an das Item in deiner Hand)"); return true; }
                File f = plugin.registry().findSchematic(withExt(a[1]));
                ItemStack hand = p.getInventory().getItemInMainHand();
                if (f == null) { Msg.send(p, "<red>Schematic nicht gefunden."); return true; }
                if (hand.getType().isAir()) { Msg.send(p, "<red>Du hältst kein Item in der Hand."); return true; }
                plugin.items().bindSchematic(hand, f.getName());
                Msg.send(p, "<green>" + f.getName() + " <gray>an dein Item gebunden.");
            }
            case "give" -> {
                if (!sender.hasPermission("buildspawner.admin")) { Msg.send(sender, "<red>Dafür fehlt dir die Berechtigung."); return true; }
                if (a.length < 3) { Msg.send(sender, "<gray>Benutzung: <white>/build give [Spieler] [kategorie:gebäude]"); return true; }
                Player t = Bukkit.getPlayerExact(a[1]);
                BuildRegistry.Build b = plugin.registry().build(a[2]);
                if (t == null || b == null) { Msg.send(sender, "<red>Spieler oder Gebäude nicht gefunden."); return true; }
                BuildRegistry.Category c = plugin.registry().category(b.cat());
                plugin.menus().give(t, plugin.items().buildItem(b, c.color(), c.name()));
                Msg.send(sender, "<green>" + b.name() + " <gray>an " + t.getName() + " gegeben.");
            }
            default -> Msg.send(sender, "<gray>/build <dark_gray>| <gray>undo <dark_gray>| <gray>schem [Datei] <dark_gray>| <gray>bind [Datei] <dark_gray>| <gray>give [Spieler] [id] <dark_gray>| <gray>reload");
        }
        return true;
    }

    private static String withExt(String s) { return s.toLowerCase(Locale.ROOT).endsWith(".schem") ? s : s + ".schem"; }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command cmd, String label, String[] a) {
        List<String> out = new ArrayList<>();
        if (a.length == 1) {
            for (String s : new String[]{"undo", "schem", "bind", "give", "reload"}) if (s.startsWith(a[0].toLowerCase(Locale.ROOT))) out.add(s);
        } else if (a.length == 2 && (a[0].equalsIgnoreCase("schem") || a[0].equalsIgnoreCase("bind"))) {
            for (File f : plugin.registry().schematicFiles()) if (f.getName().toLowerCase(Locale.ROOT).startsWith(a[1].toLowerCase(Locale.ROOT))) out.add(f.getName());
        } else if (a.length == 2 && a[0].equalsIgnoreCase("give")) {
            for (Player p : Bukkit.getOnlinePlayers()) if (p.getName().toLowerCase(Locale.ROOT).startsWith(a[1].toLowerCase(Locale.ROOT))) out.add(p.getName());
        } else if (a.length == 3 && a[0].equalsIgnoreCase("give")) {
            for (BuildRegistry.Category c : plugin.registry().categories())
                for (BuildRegistry.Build b : c.builds()) if (b.key().startsWith(a[2].toLowerCase(Locale.ROOT))) out.add(b.key());
        }
        return out;
    }
}
