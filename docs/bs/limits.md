---
title: "Ograničenja, ažuriranja i uvjeti"
nav_order: 7
lang: "bs"
source: limits.md
source_hash: "8a9c7c448411"
nav_exclude: true
search_exclude: true
---
# Ograničenja, ažuriranja i uvjeti {#limits-updates-and-terms}

## Ne čita se {#not-read}

- **Ko je koga ubio i šteta vojnicima po pogotku.** Ovo putuje u rezultatima pogodaka udaljenih poziva oružja i stanja igrača (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), čija se struktura ne čita; cjelovito se čuvaju u pomoćnoj datoteci entiteta. Dekodira se samo zdravlje žrtava.
- **Tim bota.** Stanje bota nosi broj koji bi mogao biti njegov tim; nije potvrđeno, ne koristi se.
- **Kamo vojnik gleda postrance** izvan skretanja tijela.

## Ažuriranja igre {#game-updates}

Čitač zavisi od formata replaya u engineu i od nekoliko Squadovih naziva klasa i svojstava. Ne zavisi od rasporeda svojstava koje ne može vidjeti: replay ih sam imenuje.

**Šta se može pokvariti sa Squad ažuriranjem:**

- **Nadogradnja engina.** Squad je s v10.4 prešao na UE 5.7, a ovo tamo nije testirano. Nadogradnja može promijeniti zaglavlje bunch-a, podatke o spawnu ili `FRepMovement`. Oni su u kodu vezani uz verziju gdje je korak poznat. Nepoznati koraci (`ENG_PARTIAL_CUSTOM_EXPORTS`, završni bit kretanja) vezani su za ono što radi v10.3.1.
- **Iris replikacija.** Da je Squad prešao na Iris, tok unutar chunk-ova bio bi nov i ovaj čitač ga ne bi čitao. Squad v10.3.1 koristi klasični sistem (koristi ReplicationGraph).
- **Preimenovane klase ili svojstva.** Da je Squad preimenovao klase igrača, tima ili odreda ili njihova svojstva, nestala bi imena ili timovi, ali pozicije ne.
- **Šta se dešava pri neuspjehu.** Kad se format promijeni, čitač glasno pada uz greške toka ili greške kretanja u dijagnostici. Ne proizvodi tiho pogrešne pozicije: `FRepMovement` se prihvata samo kad se njegovi bitovi tačno slažu.

## Lični podaci {#personal-data}

Demo sadrži imena i online ID-ove svih na serveru. Tabela i dokument meča nose imena, a ne ID-ove. Pomoćne datoteke čuvaju bitove svakog svojstva, pa sadrže ID-ove kakve demo ima (nedekodirane). Tretiraj ih sve kao sam demo.

## Licenca i izvori {#licence-and-sources}

MIT; vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Sve ovdje je napisano za ovaj paket. Nikakav kod treće strane nije uključen ni povezan: jedine zavisnosti su pyarrow (Apache-2.0) i numpy (BSD-3-Clause).

Činjenice o formatu potiču iz ovih izvora:

- **Unreal.Core** u [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Opisuje opći raspored Unreal replaya: blok informacija, chunk-ove, frameove, bunch-eve i izvoze mrežnih polja.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Njegov parser je čitan radi rasporeda kako ga piše Squad v10.3.1, radi provjera verzije i radi toga koje Squad klase nose podatke o popisu igrača. Njegovi objavljeni testni demoi i brojevi snimaka korišteni su kao nezavisna unakrsna provjera. Nijedan njegov kod nije kopiran ni preveden: ovaj čitač je drukčije građen (Python bitni arhiv preko cijelih paketa, djelomični bunch-evi spojeni bit po bit, svojstva raspoređena po imenu), a dvije stvari koje on ne radi pronađene su ovdje na samim demoima: treća zastavica djelomičnog bunch-a i završni bit kretanja.

Ovaj paket čita demo datoteke koje piše Squad server; ne dira igru, njen kod ni arhive, i ništa iz igre nije uključeno niti se dalje distribuira. Ono što zapiše ostaje na vašem računaru.

3DHeat nije povezan sa kompanijom Offworld Industries niti ga ona podržava. Squad i povezani nazivi i zaštitni znakovi pripadaju njihovim vlasnicima.

Nosioci prava: otvorite issue na <https://github.com/Holdi601/3DHeat-Ext-Squad/issues> - brzo odgovaramo i na zahtjev uklanjamo bilo šta.
