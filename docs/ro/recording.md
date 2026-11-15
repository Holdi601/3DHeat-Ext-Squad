---
title: "Înregistrarea unui demo"
nav_order: 2
lang: "ro"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Înregistrarea unui demo {#recording-a-demo}

Demo-urile Squad se înregistrează **pe server**, nu de clientul jocului.

1. În `Admins.cfg` al serverului, dați grupului adminului permisiunea `demos`.
2. În consola jocului, rulați `AdminDemoRec <name>` când începe meciul.
   Un admin trebuie să scrie asta în jocul însuși; un raport spune că RCON nu o acceptă.
3. Jucați meciul, apoi rulați `AdminDemoStop`.
4. Demo-ul se scrie în `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Copiați-l de pe server pe calculatorul pe care îl convertiți.

`Server.cfg` are și o setare `RecordDemos`, dezactivată implicit. Așteptați-vă la aproximativ
70 până la 80 MB pe oră pentru un meci mic; dimensiunea pentru un server complet de 100 de jucători
nu a fost măsurată.

Un demo conține numele și ID-urile online ale tuturor celor de pe server: tratați-l ca pe date
personale ([Limite, actualizări și condiții](limits.md#personal-data)).

Mai departe: [Convertirea demo-urilor](converting.md).
