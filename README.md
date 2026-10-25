# BuildSpawner (Paper 26.3)

Platziere fertige Gebäude per Item – oder deine eigenen Schematics.

* **129 Gebäude in 8 Kategorien:** Piraten (dunkles Holz), Cozy, Mittelalter, Wikinger, Modern, Wild West, Asiatisch, Fantasy
* `/build` öffnet das Menü → Kategorie → Gebäude anklicken → du bekommst ein Item
* **Rechtsklick** auf den Boden: platzieren (Vorderseite zeigt zu dir) · **Linksklick:** um 90° drehen · **Schleichen + Rechtsklick:** Umriss anzeigen
* **Eigene Schematics:** `.schem`-Dateien (Sponge v2/v3, wie WorldEdit/FAWE sie speichern) in `plugins/BuildSpawner/schematics/` legen (der WorldEdit/FAWE-Ordner wird automatisch mitgelesen). Im Menü „Eigene Schematics": Linksklick = neues Item, Rechtsklick/Shift = an das Item in deiner Hand binden. Alternativ `/build schem Datei` und `/build bind Datei`.
* `/build undo` macht die letzten Platzierungen rückgängig (Gelände wird wiederhergestellt; Truhen-Inhalte nicht).

## Jar mit GitHub bauen
1. Neues Repo auf GitHub anlegen, diesen Ordner hochladen (`git init && git add . && git commit -m init && git push`).
2. Tab **Actions** → „Build plugin" läuft automatisch (oder „Run workflow").
3. Fertige `BuildSpawner-1.0.0.jar` unter dem Lauf bei **Artifacts** herunterladen.
4. Für ein Release: Tag `v1.0.0` pushen, dann hängt die Jar automatisch an der Release-Seite.

Lokal: Java 25 + Gradle 9.1+ → `gradle jar` → `build/libs/`.

## Blockpaletten
Jedes Gebäude nutzt eine gemischte Palette je Kategorie (z. B. Wände aus mehreren Holzarten, Steinsockel, Stein mit Moos/rissigen Steinen, gemischte Dachtreppen). Die Mischungen stehen in `tools/palettes.py` und lassen sich dort anpassen.

## Rechte
`buildspawner.use` / `buildspawner.place` (Standard: alle) · `buildspawner.schematics` / `buildspawner.admin` (Standard: OP)

## Gebäude neu erzeugen / ändern
`python3 tools/generate.py` (benötigt `pillow`) schreibt alle `.schem` nach `src/main/resources/builds/`, den Index und die Vorschaubilder nach `previews/`.
