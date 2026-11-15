---
title: "Dokument zápasu a sprievodné súbory"
nav_order: 5
lang: sk
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Dokument zápasu a sprievodné súbory {#the-match-document-and-sidecars}

Vedľa tabuľky dostane každé demo `<demo>.match.json` a dva sprievodné súbory,
`<demo>.entities.parquet` a `<demo>.packets.parquet`. Prehliadač číta dokument zápasu
na karte Zápas.

## Dokument zápasu {#the-match-document}

`<demo>.match.json` (dokument zápasu) obsahuje na najvyššej úrovni `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` a `selfCheck` (úplný zoznam: [Referencia príkazov](../cli-reference.md)). Slovami: mapa a úroveň, verzie hry a motora, čas nahrávania, dĺžka a:

- **tímy**: číslo, frakcia a všetko, čo ich stav replikoval (tikety, dostupnosti, veliteľ), ako sa menilo;
- **družstvá**: číslo, tím, názov, tvorca, vodca, členovia;
- **stav hry**: názov servera a nastavenia, herný režim, stav a id zápasu, rotácie máp a úrovní, hlasovania, časovače, správa dňa;
- **aktéri**: každé vozidlo, rozmiestnený prvok, stanovište, muničná bedňa a helikoptéra – trieda, kde a kedy vznikla, kedy zanikla, čie bola a jej replikovaný stav (zdravie, stav stavby, sedadlá...);
- **riadok pre každého hráča**: vzorky pešo a vo vozidlách, prejdená vzdialenosť, triedy vojakov, ktorými hral, použité vozidlá, zmeny tímu, obsadené sedadlá a všetko, čo stav hráča replikoval (ping, úroveň, rola, aktuálne sedadlo...); a riadok pre každého bota;
- **udalosti** spočítané, **súpis vlastností** (ako často sa posielali vlastnosti každej triedy) a **súpis vzdialených volaní**, výstrely a zásahy, čo sa **nečítalo**, a diagnostiku čítačky;
- **súbor a hlavička**: každé pole informačného bloku a hlavičky dema, tabuľka častí, tabuľky exportu sieťových polí (`net_field_exports`), dôvody zatvorenia kanálov a triedy zistené pre objekty, ktorým exporty nedávajú meno (`stream.class_resolution`);
- **sebakontrolu** (`selfCheck.completeness`, pozri [Úplnosť](#completeness)).

Online identifikátory (Steam, EOS) sú vynechané úmyselne.

Rýchly pohľad na prevedené demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Úplnosť {#completeness}

Táto čítačka sa riadi pravidlom, ktoré zdieľajú všetky prevodníky 3DHeat: dekódovať, čo sa dá prečítať hneď, zvyšok zachovať celý a povedať, koľko z každého druhu sa dalo ([Prevodníky zachovávajú všetko](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Každý dokument zápasu má `selfCheck.completeness`: pre každý druh položky, ktorú demo obsahuje, koľko ich bolo `seen` (videné), `decoded` (dekódované), `partial` (čiastočne dekódované a zachované celé), `raw` (zachované len celé) a `lost` (musí byť 0). Druhy sa počítajú tam, kde na ne čítačka narazí: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Pri skutočných prečítaných demách je `lost` 0: ich položiek je od stoviek tisíc po milióny; asi polovica sa dekóduje úplne, zvyšok je čiastočný alebo surový.

**Prečítané** (do tabuľky a dokumentu zápasu):

- informačný blok, hlavička dema (každé pole; dva koncové bajty, ktoré nie sú známe, sa zachovajú ako hex), tabuľka častí;
- každý rámec, paket a zväzok (rozdelený celý na to, čo nesie), každý otvorený aktér (s polohou vzniku, natočením, mierkou a rýchlosťou) a každý zatvorený (s dôvodom: `Destroyed`, `Dormancy`...);
- každá replikovaná vlastnosť, až tak ďaleko, ako hovoria jej bity ([Dekódovanie vlastností](how-it-works.md#decoding-properties)), polohy z `FRepMovement` a z komponentu pohybu helikoptér, zranenia, zdravie vozidiel, sedadlá;
- každé vzdialené volanie menom, s jeho parametrami, kde demo exportuje skupinu funkcie: výstrely (`fire`) a zásahy vozidiel (`hit`) do tabuľky;
- tabuľky exportu sieťových polí a sieťové GUID (ich počet; cesty sú v sprievodnom súbore entít).

**Zachované surové** (celé, s tým, čo sa z nich prečítalo, vedľa):

- `<demo>.entities.parquet`, stĺpce `time`, `type` (`<class>.<property>`, `<class>.<call>`, alebo meno objektu), `name` (trieda aktéra), `entity` (sieťové GUID aktéra, ako `entity` tabuľky), `kind`, `object` (podobjekt), `channel`, `handle`, `group` (cesta triedy skupiny exportu), `decoded` (JSON), `bits` a `payload` (bity, od najnižšieho, doplnené na celé bajty):
  - každá aktualizácia vlastnosti (`kind` `property`), vrátane pohybu, s tým, čo sa dekódovalo; surová len tam, kde sa nič nedekódovalo (nepomenované handle, štruktúry ako `RotationReplicatedMovement` veží a vlastnosti zostavené len z bitov);
  - každé vzdialené volanie a vlastné delta pole (`rpc`), parametre dekódované tam, kde sa skupina funkcie exportovala; surové tam, kde nie (`RepInventory`, `PlayerStateData`);
  - každý blok obsahu objektu, ktorého trieda sa nedala nájsť (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), s dekódovanou hlavičkou;
  - každý kanál aktéra, ktorý sa otvoril a zatvoril (`open`, `close`), každý podobjekt, ktorý bol zmazaný alebo zničený;
  - kontext, ktorý neskorší dekodér potrebuje na čítanie samotného súboru: každé exportované sieťové pole (`export.field`: cesta skupiny, handle, názov vlastnosti, kontrolný súčet) a každé exportované sieťové GUID (`export.guid`: jeho cesta, nadradený objekt a príznaky), v čase, keď ich stream dal.
- `<demo>.packets.parquet`, stĺpce `time`, `type`, `name`, `channel`, `offset` (v súbore), `decoded`, `bits`, `payload`: informačný blok, hlavičková časť, každá kontrolná časť (kontrolný bod je stav každého aktéra v jeho čase, ktorý stream od začiatku tiež obsahuje), každá časť udalostí a každý rámec, paket alebo zväzok, ktorý sa nečíta (jeden zväzok na demo: úvodný zväzok vlastného diváka nahrávača), celé.

Riadky entít sú zoskupené podľa `kind`, `type` a `entity`, každá v časovom poradí; na poradie streamu zoraďte podľa `time`.

**Nie je k dispozícii:**

- to, čo serverové demo nenahráva: vstupy klientov, čo hráč videl;
- účinky na strane klienta: značky zásahu, zvuky, text killfeedu (server posiela volania, nie ich zobrazenie);
- dekódované online ID: zachované len ako bity (pozri [Osobné údaje](limits.md#personal-data)).
