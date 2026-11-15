---
title: "Dokument zápasu a doplňková data"
nav_order: 5
lang: "cs"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Dokument zápasu a doplňková data {#the-match-document-and-sidecars}

Vedle tabulky dostane každé demo soubor `<demo>.match.json` a dvě doplňková data,
`<demo>.entities.parquet` a `<demo>.packets.parquet`. Prohlížeč čte dokument zápasu
na své kartě Zápas.

## Dokument zápasu {#the-match-document}

`<demo>.match.json` (dokument zápasu) obsahuje na nejvyšší úrovni `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` a `selfCheck` (úplný seznam: [Přehled příkazů](../cli-reference.md)). Slovy: mapa a vrstva, verze hry a enginu, čas nahrání, délka a:

- **týmy**: číslo, frakce a vše, co jejich stav replikoval (lístky, dostupnosti, velitel), jak se měnil;
- **oddíly**: číslo, tým, název, zakladatel, vůdce, členové;
- **herní stav**: jméno serveru a nastavení, herní režim, stav zápasu a jeho id, rotace map a úrovní, hlasování, časovače, denní zpráva;
- **aktéři**: každé vozidlo, rozmístitelný prvek, stanoviště, bedna s municí a vrtulník - třída, kde a kdy vznikl, kdy zanikl, čí byl, a jeho replikovaný stav (zdraví, stav sestavení, sedadla...);
- **řádek pro každého hráče**: vzorky pěšky a ve vozidlech, ujitá vzdálenost, třídy vojáků, které hrál, použitá vozidla, změny týmu, obsazená sedadla a vše, co stav hráče replikoval (ping, úroveň, role, aktuální sedadlo...); a řádek pro každého bota;
- **události** spočítané, **soupis vlastností** (jak často se posílaly vlastnosti každé třídy) a **soupis vzdálených volání**, výstřely a zásahy, co se **nepřečetlo**, a diagnostiku čtečky;
- **soubor a hlavička**: každé pole informačního bloku a hlavičky dema, tabulku částí, tabulky exportovaných síťových polí (`net_field_exports`), důvody zavření kanálů a třídy nalezené pro objekty, které exporty nepojmenují (`stream.class_resolution`);
- **vlastní kontrola** (`selfCheck.completeness`, viz [Úplnost](#completeness)).

Online ID (Steam, EOS) jsou záměrně vynechána.

Rychlý pohled na převedené demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Úplnost {#completeness}

Tato čtečka se řídí pravidlem, které sdílejí všechny převodníky 3DHeat: přečíst, co lze přečíst hned, zbytek uchovat celý a říct, kolik čeho se přečetlo ([Převodníky zachovávají vše](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Každý dokument zápasu má `selfCheck.completeness`: pro každý druh položky, která se v demu potkala, kolik jich bylo `seen` (viděno), `decoded` (dekódováno), `partial` (dekódováno zčásti a uchováno celé), `raw` (uchováno jen celé) a `lost` (musí být 0). Druhy se počítají tam, kde je čtečka potká: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Na přečtených skutečných demech je `lost` 0: jejich položek je od stovek tisíc do milionů; zhruba polovina se dekóduje úplně, zbytek je částečný nebo surový.

**Čte se** (do tabulky a dokumentu zápasu):

- informační blok, hlavička dema (každé pole; dva koncové bajty, které neznáme, se uchovají v hexadecimálním tvaru), tabulka částí;
- každý rámec, paket a svazek (rozdělené celé na to, co nesou), každý otevřený aktér (s místem vzniku, natočením, měřítkem a rychlostí) a zavřený (s důvodem: `Destroyed`, `Dormancy`...);
- každá replikovaná vlastnost, tak daleko, jak to říkají její bity ([Dekódování vlastností](how-it-works.md#decoding-properties)), pozice z `FRepMovement` a z komponenty pohybu vrtulníků, zranění, zdraví vozidel, sedadla;
- každé vzdálené volání podle názvu, s parametry tam, kde demo exportuje skupinu funkce: výstřely (`fire`) a zásahy vozidel (`hit`) do tabulky;
- tabulky exportovaných síťových polí a síťové GUID (jejich počet; cesty jsou v doplňkových datech entit).

**Uchovává se surové** (celé, s tím, co se z něj přečetlo, vedle):

- `<demo>.entities.parquet`, sloupce `time`, `type` (`<class>.<property>`, `<class>.<call>`, nebo jméno objektu), `name` (třída aktéra), `entity` (síťové GUID aktéra, jako `entity` v tabulce), `kind`, `object` (podobjekt), `channel`, `handle`, `group` (cesta třídy skupiny exportu), `decoded` (JSON), `bits` a `payload` (bity, od nejnižšího, doplněné na celé bajty):
  - každá aktualizace vlastnosti (`kind` `property`), včetně pohybu, s tím, co je dekódováno; surově jen tam, kde se nic nedekóduje (nepojmenované handly, struktury jako `RotationReplicatedMovement` věží a vlastnosti ponechané jako bity);
  - každé vzdálené volání a vlastní delta pole (`rpc`), parametry dekódované tam, kde byla skupina funkce exportována; surově tam, kde ne (`RepInventory`, `PlayerStateData`);
  - každý blok obsahu objektu, jehož třída nebyla nalezena (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), s dekódovanou hlavičkou;
  - každý kanál aktéra otevřený a zavřený (`open`, `close`), každý podobjekt smazaný nebo zničený;
  - kontext, který pozdější dekodér potřebuje, aby četl soubor sám: každé exportované síťové pole (`export.field`: cesta skupiny, handle, název vlastnosti, kontrolní součet) a každé exportované síťové GUID (`export.guid`: jeho cesta, vnější objekt a příznaky), v čase, kdy je stream dal.
- `<demo>.packets.parquet`, sloupce `time`, `type`, `name`, `channel`, `offset` (v souboru), `decoded`, `bits` a `payload`: informační blok, hlavičková část, každá část kontrolního bodu (kontrolní bod je stav každého aktéra v jeho čase, který stream od začátku také obsahuje), každá část událostí a každý rámec, paket nebo svazek, který se nepřečte (jeden svazek na demo: úvodní svazek vlastního diváckého aktéra nahrávače), celé.

Řádky entit jsou seskupené podle `kind`, `type` a `entity`, každé v časovém pořadí; pro pořadí streamu řaďte podle `time`.

**Nedostupné:**

- co serverové demo nezaznamenává: vstupy klientů, co hráč viděl;
- efekty na straně klienta: značky zásahů, zvuky, text killfeedu (server posílá volání, ne jejich zobrazení);
- dekódovaná online ID: uchovávají se jen jako bity (viz [Osobní údaje](limits.md#personal-data)).
