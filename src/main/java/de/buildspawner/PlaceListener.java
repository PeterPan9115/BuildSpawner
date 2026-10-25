package de.buildspawner;

import org.bukkit.GameMode;
import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;
import org.bukkit.entity.Player;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.ItemStack;

import java.io.File;

/** Rechtsklick = platzieren, Linksklick = drehen, Schleichen+Rechtsklick = Umriss. */
final class PlaceListener implements Listener {
    private final BuildSpawnerPlugin plugin;

    PlaceListener(BuildSpawnerPlugin plugin) { this.plugin = plugin; }

    @EventHandler(priority = EventPriority.HIGH)
    public void onInteract(PlayerInteractEvent e) {
        if (e.getHand() != EquipmentSlot.HAND) return;
        ItemStack item = e.getItem();
        Items items = plugin.items();
        if (item == null || !items.isPlaceItem(item)) return;

        e.setCancelled(true);
        e.setUseItemInHand(Event.Result.DENY);
        e.setUseInteractedBlock(Event.Result.DENY);
        Player p = e.getPlayer();
        Action a = e.getAction();

        if (a == Action.LEFT_CLICK_AIR || a == Action.LEFT_CLICK_BLOCK) {
            int rot = (items.rotation(item) + 1) % 4;
            items.setRotation(item, rot);
            p.getInventory().setItemInMainHand(item);
            p.sendActionBar(Msg.mm("<gold>Drehung: <white>" + (rot * 90) + "°"));
            return;
        }
        if (a != Action.RIGHT_CLICK_BLOCK && a != Action.RIGHT_CLICK_AIR) return;

        if (!p.hasPermission("buildspawner.place")) { Msg.send(p, "<red>Dafür fehlt dir die Berechtigung."); return; }

        Block target = a == Action.RIGHT_CLICK_BLOCK ? e.getClickedBlock() : p.getTargetBlockExact(60);
        if (target == null) { Msg.send(p, "<red>Kein Block im Blickfeld."); return; }

        // Schematic + Offset bestimmen
        Schematic s; int yOffset;
        String key = items.buildKey(item);
        if (key != null) {
            BuildRegistry.Build b = plugin.registry().build(key);
            if (b == null) { Msg.send(p, "<red>Dieses Gebäude gibt es nicht mehr."); return; }
            s = plugin.registry().schematic(b);
            yOffset = -b.ground();
        } else {
            String file = items.schemFile(item);
            File f = plugin.registry().findSchematic(file);
            if (f == null) { Msg.send(p, "<red>Schematic <white>" + file + "<red> nicht gefunden."); return; }
            s = plugin.registry().schematic(f);
            yOffset = 1;
        }
        if (s == null) { Msg.send(p, "<red>Die Schematic konnte nicht geladen werden (siehe Konsole)."); return; }

        int rot = (baseRotation(p) + items.rotation(item)) % 4;

        if (p.isSneaking()) {
            plugin.placer().outline(p, target, s, yOffset, rot);
            p.sendActionBar(Msg.mm("<gray>Umriss gezeigt – <yellow>Rechtsklick<gray> ohne Schleichen platziert."));
            return;
        }

        if (!plugin.placer().place(p, target, s, yOffset, rot)) return;

        boolean consume = plugin.getConfig().getBoolean("consume-item", true);
        if (consume && p.getGameMode() != GameMode.CREATIVE && key != null) {
            item.setAmount(item.getAmount() - 1);
            p.getInventory().setItemInMainHand(item.getAmount() <= 0 ? null : item);
        }
    }

    /** Vorderseite des Gebäudes (Süden) soll zum Spieler zeigen. */
    private static int baseRotation(Player p) {
        BlockFace f = p.getFacing();
        return switch (f) {
            case EAST -> 1;
            case SOUTH -> 2;
            case WEST -> 3;
            default -> 0;
        };
    }
}
