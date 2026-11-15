---
title: Ograničenja, ažuriranja i uvjeti
nav_order: 7
lang: "hr"
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Ograničenja, ažuriranja i uvjeti {#limits-updates-and-terms}

## Nije pročitano {#not-read}

- **Tko je koga ubio i šteta vojnicima po pogotku.** Ovo putuje u rezultatima pogodaka udaljenih poziva oružja i stanja igrača (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), čija struktura nije pročitana; sačuvani su cijeli u pratećoj datoteci entiteta. Dekodirano je samo zdravlje žrtava.
- **Tim bota.** Stanje bota nosi broj koji bi mogao biti njegov tim; nije potvrđeno, nije korišteno.
- **Gdje vojnik gleda postrance** izvan yawa tijela.

## Ažuriranja igre {#game-updates}

Čitač ovisi o formatu replaya motora i o nekoliko imena Squad klasa i svojstava. Ne ovisi o rasporedima svojstava koje ne može vidjeti: replay ih imenuje sam.

**Što može pući pri Squad ažuriranju:**

- **Nadogradnja motora.** Squad je prešao na UE 5.7 s v10.4, a to ovdje nije testirano. Nadogradnja može promijeniti zaglavlje snopa, podatke o pojavi ili `FRepMovement`. Ti dijelovi su u kodu vezani uz verziju tamo gdje je korak poznat. Nepoznati koraci (`ENG_PARTIAL_CUSTOM_EXPORTS`, završni bit kretanja) postavljeni su prema onome što v10.3.1 radi.
- **Iris replikacija.** Ako je Squad prešao na Iris, tok unutar dijelova bio bi nov i ovaj čitač ga ne bi čitao. Squad v10.3.1 koristi klasični sustav (pokreće ReplicationGraph).
- **Preimenovane klase ili svojstva.** Ako je Squad preimenovao svoje klase igrača, tima ili odreda ili njihova svojstva, imena ili timovi bi nestali, ali položaji ne bi.
- **Što se događa pri kvaru.** Kad se format promijeni, čitač glasno javlja pogrešku toka ili pogrešku kretanja u dijagnostici. Ne proizvodi tiho krive položaje: `FRepMovement` se prihvaća samo kad se bitovi točno zbroje.

## Osobni podaci {#personal-data}

Demo sadrži imena i mrežne ID-jeve svih na serveru. Tablica i dokument meča sadrže imena, ne ID-jeve. Prateće datoteke čuvaju bitove svakog svojstva, pa sadrže ID-jeve kako ih demo sadrži (nedekodirane). Postupajte sa svima njima kao s samim demoom.

## Licenca i izvori {#licence-and-sources}

MIT; vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Sve ovdje napisano je za ovaj paket. Nijedan kod trećih strana nije uključen ni povezan: jedine ovisnosti su pyarrow (Apache-2.0) i numpy (BSD-3-Clause).

Činjenice o formatu dolaze iz ovih izvora:

- **Unreal.Core** u [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Opisuje opći Unreal raspored replaya: informacijski blok, dijelove, okvire, snopove i izvoze mrežnih polja.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Njegov parser je pročitan zbog rasporeda kako ga Squad v10.3.1 piše, zbog provjera verzije i zbog toga koje Squad klase nose podatke o popisu igrača. Njegovi objavljeni testni demoi i brojevi snimki korišteni su kao neovisna unakrsna provjera. Nijedan njegov kod nije kopiran ni preveden: ovaj čitač je drukčije strukturiran (Python bitni arhiv nad cijelim paketima, djelomični snopovi spojeni bit po bit, svojstva raspoređena po imenu), a dvije stvari koje on ne radi pronađene su ovdje na samim demoima: treća zastavica djelomičnog snopa i završni bit kretanja.

Squad je zaštitni znak tvrtke Offworld Industries. Ovaj paket čita datoteke koje piše Squad server; ne dira igru, njezin kod ni njezine arhive. Offworldova pravila o licenciranju i administraciji servera ništa ne kažu o snimanju ili analizi demoa. Squadova EULA zabranjuje reverzni inženjering same igre, što ovo ne radi.
