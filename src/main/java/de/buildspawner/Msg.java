package de.buildspawner;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.TextDecoration;
import net.kyori.adventure.text.minimessage.MiniMessage;
import org.bukkit.command.CommandSender;

final class Msg {
    private Msg() {}
    static final String PREFIX = "<gradient:#f6c177:#eb6f92><bold>Build</bold></gradient> <dark_gray>» ";

    static Component mm(String s) { return MiniMessage.miniMessage().deserialize(s); }
    /** Ohne Kursiv (für Item-Namen/Lore). */
    static Component plain(String s) { return mm(s).decoration(TextDecoration.ITALIC, false); }
    static void send(CommandSender to, String s) { to.sendMessage(mm(PREFIX + s)); }
}
