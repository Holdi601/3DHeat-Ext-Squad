---
title: Tirrekordja demo
nav_order: 2
lang: mt
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Tirrekordja demo {#recording-a-demo}

Id-demos ta' Squad jiġu rrekordjati **fuq is-server**, mhux mill-klijent tal-logħba.

1. Fil-`Admins.cfg` tas-server, agħti lill-grupp tal-admin il-permess
   `demos`.
2. Fil-console tal-logħba, ħaddem `AdminDemoRec <name>` meta tibda l-partita.
   Admin irid jittajpja dan fil-logħba nnifisha; rapport wieħed jgħid li r-RCON
   ma jaċċettahx.
3. Illogħob il-partita, imbagħad ħaddem `AdminDemoStop`.
4. Id-demo tinkiteb f'`<server>/SquadGame/Saved/Demos/<name>.replay`.
   Ikkopjaha minn fuq is-server għall-magna li tikkonverti.

`Server.cfg` għandu wkoll setting `RecordDemos`, mitfi b'mod awtomatiku. Stenna madwar
70 sa 80 MB fis-siegħa għal partita żgħira; id-daqs għal server sħiħ
ta' 100 plejer għadu ma tkejjilx.

Demo fiha l-ismijiet u l-online ids ta' kulħadd fuq is-server: ittrattaha bħala
dejta personali ([Limiti, aġġornamenti u termini](limits.md#personal-data)).

Li jmiss: [Tikkonverti demos](converting.md).
