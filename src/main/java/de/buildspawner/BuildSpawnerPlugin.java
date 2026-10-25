package de.buildspawner;

import org.bukkit.command.PluginCommand;
import org.bukkit.plugin.java.JavaPlugin;

public final class BuildSpawnerPlugin extends JavaPlugin {
    private BuildRegistry registry;
    private Items items;
    private Placer placer;
    private Menus menus;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        getDataFolder().mkdirs();
        new java.io.File(getDataFolder(), "schematics").mkdirs();
        registry = new BuildRegistry(this);
        registry.load();
        items = new Items(this);
        placer = new Placer(this);
        menus = new Menus(this);
        getServer().getPluginManager().registerEvents(menus, this);
        getServer().getPluginManager().registerEvents(new PlaceListener(this), this);
        PluginCommand cmd = getCommand("build");
        if (cmd != null) {
            BuildCommand bc = new BuildCommand(this);
            cmd.setExecutor(bc);
            cmd.setTabCompleter(bc);
        }
    }

    BuildRegistry registry() { return registry; }
    Items items() { return items; }
    Placer placer() { return placer; }
    Menus menus() { return menus; }
}
