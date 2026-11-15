---
title: "Obmedzenia, aktualizácie a podmienky"
nav_order: 7
lang: sk
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Obmedzenia, aktualizácie a podmienky {#limits-updates-and-terms}

## Nečíta sa {#not-read}

- **Kto koho zabil a poškodenie vojaka zásahom.** Tieto údaje idú vo výsledkoch zásahov vzdialených volaní zbraní a stavov hráčov (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), ktorých štruktúra sa nečíta; zachovávajú sa celé v sprievodnom súbore entít. Dekóduje sa len zdravie obetí.
- **Tím bota.** Stav bota nesie číslo, ktoré môže byť jeho tím; nepotvrdené, nepoužité.
- **Kam sa vojak pozerá do strany** nad rámec uhla natočenia tela.

## Aktualizácie hry {#game-updates}

Čítačka závisí od formátu replayu motora a od hŕstky názvov tried a vlastností Squad. Nezávisí od rozloženia vlastností, ktoré nevidí: replay ich pomenúva sám.

**Čo sa môže pokaziť pri aktualizácii Squad:**

- **Aktualizácia motora.** Squad prešiel na UE 5.7 s verziou v10.4 a to nie je otestované. Aktualizácia môže zmeniť hlavičku zväzku, dáta vzniku alebo `FRepMovement`. Tieto sú v kóde viazané na verziu tam, kde je ten krok známy. Neznáme kroky (`ENG_PARTIAL_CUSTOM_EXPORTS`, koncový bit pohybu) sú pevne nastavené podľa toho, čo robí v10.3.1.
- **Replikácia Iris.** Keby Squad prešiel na Iris, stream vnútri častí by bol nový a táto čítačka by ho nečítala. Squad v10.3.1 používa klasický systém (beží na ReplicationGraph).
- **Premenované triedy alebo vlastnosti.** Ak by Squad premenoval svoje triedy hráča, tímu alebo družstva alebo ich vlastnosti, mená alebo tímy by chýbali, ale pozície by nie.
- **Čo sa stane pri chybe.** Keď sa formát zmení, čítačka hlasno zlyhá s chybami streamu alebo pohybu v diagnostike. Nevyrobí potichu nesprávne pozície: `FRepMovement` sa prijme len vtedy, keď sa jeho bity presne sčítajú.

## Osobné údaje {#personal-data}

Demo obsahuje mená a online identifikátory všetkých na serveri. Tabuľka a dokument zápasu nesú mená, nie identifikátory. Sprievodné súbory uchovávajú bity každej vlastnosti, takže obsahujú identifikátory tak, ako ich obsahuje demo (nie dekódované). Zaobchádzajte so všetkými ako s demom samotným.

## Licencia a zdroje {#licence-and-sources}

MIT; pozri [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Všetko tu bolo napísané pre tento balík. Nie je zahrnutý ani prepojený žiadny kód tretích strán: jedinými závislosťami sú pyarrow (Apache-2.0) a numpy (BSD-3-Clause).

Fakty o formáte pochádzajú z týchto zdrojov:

- **Unreal.Core** v [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Opisuje všeobecné rozloženie replayu Unreal: informačný blok, časti, rámce, zväzky a exporty sieťových polí.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Jeho čítačka bola prečítaná kvôli rozloženiu tak, ako ho Squad v10.3.1 zapisuje, kvôli kontrolám verzie a kvôli tomu, ktoré triedy Squad nesú údaje o súpiske. Jeho zverejnené testovacie demá a počty snímok sa použili ako nezávislá kontrola. Žiadny jeho kód sa nekopíroval ani neprekladal: táto čítačka je štruktúrovaná inak (bitový archív v Pythone nad celými paketmi, čiastočné zväzky spájané bitovo, vlastnosti rozdeľované podľa mena), a dve veci, ktoré nerobí, sa tu zistili na samotných demách: tretí príznak čiastočného zväzku a koncový bit pohybu.

Squad je ochranná známka spoločnosti Offworld Industries. Tento balík číta súbory, ktoré zapisuje server Squad; nezasahuje do hry, jej kódu ani jej archívov. Licenčná a administratívna politika serverov Offworld nehovorí nič o nahrávaní alebo analyzovaní dem. Licenčná zmluva Squad (EULA) zakazuje spätné inžinierstvo samotnej hry, čo tento balík nerobí.
