---
title: "Omezení, aktualizace a podmínky"
nav_order: 7
lang: cs
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Omezení, aktualizace a podmínky {#limits-updates-and-terms}

## Nečte se {#not-read}

- **Kdo koho zabil a poškození vojáků zásahem.** Ty putují ve výsledcích zásahů vzdálených volání zbraní a stavů hráčů (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), jejichž strukturu nečteme; zůstávají celé v doplňkových datech entit. Dekóduje se jen zdraví obětí.
- **Tým bota.** Stav bota nese číslo, které může být jeho týmem; nepotvrzeno, nepoužito.
- **Kam voják kouká do strany** za rámec natočení těla.

## Aktualizace hry {#game-updates}

Čtečka závisí na formátu replayů enginu a na hrstce názvů tříd a vlastností Squadu. Nezávisí na rozložení vlastností, které nevidí: ta si replay pojmenovává sám.

**Co se může s aktualizací Squadu rozbít:**

- **Aktualizace enginu.** Squad přešel na UE 5.7 ve verzi v10.4 a tady to není otestováno. Aktualizace může změnit hlavičku svazku, data vzniku nebo `FRepMovement`. Ty jsou v kódu vázány na verzi tam, kde je krok znám. Neznámé kroky (`ENG_PARTIAL_CUSTOM_EXPORTS`, koncový bit pohybu) jsou ukotveny podle toho, co dělá v10.3.1.
- **Replikace Iris.** Kdyby Squad přešel na Iris, stream uvnitř částí by byl nový a tato čtečka by ho nečetla. Squad v10.3.1 používá klasický systém (běží na ReplicationGraph).
- **Přejmenované třídy nebo vlastnosti.** Kdyby Squad přejmenoval své třídy hráčů, týmů nebo oddílů nebo jejich vlastnosti, chyběla by jména nebo týmy, ale pozice by nechyběla.
- **Co se stane při selhání.** Když se formát změní, čtečka hlasitě selže chybami streamu nebo chybami pohybu v diagnostice. Tiše nevyrobí špatné pozice: `FRepMovement` se přijme jen tehdy, když jeho bity přesně sedí.

## Osobní údaje {#personal-data}

Demo obsahuje jména a online ID všech na serveru. Tabulka a dokument zápasu nesou jména, ne ID. Doplňková data uchovávají bity každé vlastnosti, takže ID obsahují tak, jak je obsahuje demo (nedekódovaná). S všemi zacházejte stejně jako s demem samotným.

## Licence a zdroje {#licence-and-sources}

MIT; viz [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Všechno zde bylo napsáno pro tento balíček. Nejsou zahrnuty ani nepropojeny žádné kódy třetích stran: jedinými závislostmi jsou pyarrow (Apache-2.0) a numpy (BSD-3-Clause).

Údaje o formátu pocházejí z těchto zdrojů:

- **Unreal.Core** v [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Popisuje obecné rozložení replayů Unreal: informační blok, části, rámce, svazky a exporty síťových polí.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Jeho čtečka byla přečtena kvůli rozložení, jak ho Squad v10.3.1 zapisuje, kvůli kontrolám verzí a kvůli tomu, které třídy Squadu nesou údaje o soupisce. Jeho zveřejněná testovací dema a počty ze snímků sloužily jako nezávislá kontrola. Žádný jeho kód nebyl zkopírován ani přeložen: tato čtečka je postavená jinak (bitový archiv v Pythonu nad celými pakety, částečné svazky se spojují po bitech, vlastnosti se rozdělují podle jména), a dvě věci, které nedělá, byly zjištěny přímo na demech: třetí příznak částečného svazku a koncový bit pohybu.

Squad je ochranná známka společnosti Offworld Industries. Tento balíček čte soubory, které zapisuje server Squadu; se hrou, jejím kódem ani archivy nijak nezasahuje. Pravidla pro licencování a správu serverů Offworld nic neříkají o nahrávání nebo analýze dem. EULA Squadu zakazuje zpětné inženýrství samotné hry, což tento balíček nedělá.
