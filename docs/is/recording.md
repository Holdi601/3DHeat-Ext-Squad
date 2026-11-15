---
title: "Upptaka á demo"
nav_order: 2
lang: "is"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Upptaka á demo {#recording-a-demo}

Squad demo eru tekin upp **á þjóninum**, ekki af leikjaforritinu.

1. Gefðu hópi stjórnandans heimildina `demos` í `Admins.cfg` þjónsins.
2. Keyrðu `AdminDemoRec <name>` í stjórnborði leiksins þegar leikurinn byrjar.
   Stjórnandi verður að skrifa þetta í leiknum sjálfum; ein skýrsla segir að RCON
   taki ekki við því.
3. Spilaðu leikinn og keyrðu síðan `AdminDemoStop`.
4. Demo-ið er skrifað í `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Afritaðu það af þjóninum yfir á tölvuna sem umbreytir því.

`Server.cfg` hefur líka stillinguna `RecordDemos`, sem er óvirk sjálfgefið. Búast má við um það bil
70 til 80 MB á klukkustund fyrir lítinn leik; stærðin fyrir fullan 100 manna þjón
hefur ekki verið mæld.

Demo geymir nöfn og nettengd auðkenni allra á þjóninum: farðu með það sem
persónuupplýsingar ([Takmarkanir, uppfærslur og skilmálar](limits.md#personal-data)).

Næst: [Umbreyting á demo](converting.md).
