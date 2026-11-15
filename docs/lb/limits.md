---
title: "Grenzen, Updates a Bedingungen"
nav_order: 7
lang: lb
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Grenzen, Updates a Bedingungen {#limits-updates-and-terms}

## Net gelies {#not-read}

- **Wien wien ëmbruecht huet, a Schued u Zaldoten pro Treffer.** Dës reesen an den Hit-Resultater vun den Remote-Calls vun de Waffen a vun de Player-States (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), deenen hir Struktur net gelies gëtt; si ginn an der Entities-Niewendatei komplett opgehalen. Nëmmen d'Gesondheet vun den Affer gëtt dekodéiert.
- **D'Team vum Bot.** Dem Bot säin State huet eng Zuel, déi säin Team kéint sinn; net bestätegt, net benotzt.
- **Wouhin e Zaldot op d'Säit kuckt** iwwer de Yaw vum Kierper eraus.

## Spill-Updates {#game-updates}

De Reader hänkt vum Replay-Format vum Engine an engem Handvoll Squad-Klass- a Property-Nimm of. Hie hänkt net vu Property-Layouten of, déi e net gesäit: d'Replay nennt déi selwer.

**Wat mat engem Squad-Update futti goe kann:**

- **En Engine-Upgrade.** Squad ass mat v10.4 op UE 5.7 geplënnert, an dat ass dofir net getest. Den Upgrade kann de Bunch-Header, d'Spawn-Daten oder `FRepMovement` änneren. Dës si am Code no Versioun getrennt, wou de Schrëtt bekannt ass. Onbekannt Schrëtt (`ENG_PARTIAL_CUSTOM_EXPORTS`, dat hannescht Beweegungs-Bit) si festgehal op dat, wat v10.3.1 mécht.
- **Iris-Replikatioun.** Wann Squad op Iris wiesselt, wier de Stream an de Chunks nei an dëse Reader géif en net liesen. Squad v10.3.1 benotzt dat klassescht System (et leeft ReplicationGraph).
- **Ëmbenannte Klassen oder Properties.** Wann Squad seng Player-, Team- oder Squad-Klassen oder hir Properties ëmbenannt huet, géifen Nimm oder Teams feelen, awer Positioune géifen net feelen.
- **Wat bei engem Feeler geschitt.** Wann d'Format sech ännert, schléit de Reader haart fehl, mat Stream-Feeler oder Beweegungs-Feeler an den Diagnosen. Hie produzéiert net roueg falsch Positiounen: `FRepMovement` gëtt nëmmen ugeholl, wann seng Bits genau opgoen.

## Perséinlech Daten {#personal-data}

Eng Demo hält d'Nimm an Online-IDen vun allen um Server. D'Tabell an d'Match-Dokument droen Nimm, keng IDen. D'Niewendateien halen d'Bits vun all Property, sou halen se d'IDen esou wéi d'Demo (net dekodéiert). Behandelt se all wéi d'Demo selwer.

## Lizenz a Quellen {#licence-and-sources}

MIT; kuckt [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Alles hei gouf fir dëse Package geschriwwen. Keen Drëttcode ass abegraff oder verlinkt: déi eenzeg Ofhängegkeete sinn pyarrow (Apache-2.0) an numpy (BSD-3-Clause).

Fakte iwwer d'Format koumen aus dëse Quellen:

- **Unreal.Core** am [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Et beschreift dat generescht Unreal-Replay-Layout: den Info-Block, d'Chunks, d'Frames, d'Bunches an d'Net-Field-Exports.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Säi Parser gouf gelies fir d'Layout, wéi Squad v10.3.1 et schreift, fir d'Versiounscheken, a fir ze wëssen, wéi eng Squad-Klasse Roster-Daten droen. Seng publizéiert Test-Demoen a Snapshot-Zuelen goufen als onofhängege Géigecheck benotzt. Näischt vu sengem Code gouf kopéiert oder iwwersat: dëse Reader ass anescht opgebaut (e Python-Bit-Archiv iwwer ganz Packeten, deelweis Bunches bitweis zesummegesat, Properties no Numm verdeelt), an zwou Saachen, déi en net mécht, goufen hei op den Demoe selwer fonnt: dat drëtt Partial-Bunch-Flag an dat hannescht Beweegungs-Bit.

Squad ass eng Marque vun Offworld Industries. Dëse Package liest Dateien, déi e Squad-Server schreift; en huet näischt mam Spill, sengem Code oder senge Archiver ze dinn. Dem Offworld seng Politik zu Server-Lizenzéierung an Administratioun seet näischt iwwer d'Opnam oder d'Analyse vun Demoen. Dem Squad seng EULA verbitt Reverse Engineering vum Spill selwer, wat dëst net mécht.
