---
title: "Snemanje posnetka"
nav_order: 2
lang: sl
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Snemanje posnetka {#recording-a-demo}

Posnetki Squad se snemajo **na strežniku**, ne v odjemalcu igre.

1. V datoteki strežnika `Admins.cfg` dodeli skupini skrbnika dovoljenje `demos`.
2. V konzoli igre ob začetku tekme zaženi `AdminDemoRec <ime>`.
   Skrbnik mora to vtipkati v sami igri; po enem poročilu RCON tega ne sprejme.
3. Odigraj tekmo, nato zaženi `AdminDemoStop`.
4. Posnetek se zapiše v `<strežnik>/SquadGame/Saved/Demos/<ime>.replay`.
   Prenesi ga s strežnika na računalnik, na katerem ga boš pretvoril.

V `Server.cfg` je tudi nastavitev `RecordDemos`, privzeto izklopljena. Za majhno
tekmo pričakuj približno 70 do 80 MB na uro; velikost za polni strežnik za 100
igralcev še ni bila izmerjena.

Posnetek vsebuje imena in spletne identifikatorje vseh na strežniku: obravnavaj ga
kot osebne podatke ([Omejitve, posodobitve in pogoji](limits.md#personal-data)).

Naprej: [Pretvarjanje posnetkov](converting.md).
