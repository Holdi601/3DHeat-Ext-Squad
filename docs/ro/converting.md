---
title: "Convertirea demo-urilor"
nav_order: 3
lang: "ro"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Convertirea demo-urilor {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Pas cu pas {#step-by-step}

Nu ați mai lucrat în linia de comandă? Citiți mai întâi [Înainte de a începe](before-you-start.md).

1. Instalați o singură dată: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   deschideți un terminal în acel dosar, rulați `python -m pip install -e .`
   (Python 3.10 sau mai nou; aduce cu el pyarrow și numpy).
2. Puneți fișierele `.replay` într-un dosar, sau numiți-le unul câte unul.
3. Rulați `heat3d-squad-demo <folder> -o out`.
4. Ar trebui să vedeți câte o linie pentru fiecare demo: stratul său, jucătorii și rândurile și
   unde a fost scris tabelul. Fiecare demo devine patru fișiere separate în `out/<map>/` (nu un
   container `.3dheat`); încărcați `.parquet` în vizualizatorul 3DHeat.

![O rulare pe un demo sintetic](../assets/img/run.svg)

Imaginea arată o rulare pe un demo pe care îl construiesc testele (`tests/test_stream.py`),
nu un meci real.

## Opțiuni {#options}

| Opțiune | Implicit | Ce face |
|---|---|---|
| `demos` (unul sau mai multe) | - | fișiere `.replay`, sau dosare care le conțin |
| `-o`, `--out` | obligatorie | dosarul în care se scrie; fiecare demo ajunge în `<out>/<map>/` |
| `--flat` | dezactivată | scrie direct în dosar, fără dosarul `<map>/` |
| `--json` | dezactivată | afișează câte o linie de JSON pentru fiecare demo, la ieșire standard (pentru programe care apelează comanda): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; un demo care a eșuat afișează `demo`, `ok: false` și `error` în schimb |
| `--version` | - | afișează versiunea și se oprește |

Fiecare opțiune, așa cum o afișează programul: [Referința comenzilor](../cli-reference.md).

Dosarul hărții este numele hărții luat din calea nivelului pe care o spune demo-ul
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` dă `<Map>`).

Codul de stare: 0 când fiecare demo a fost convertit; 1 când vreunul a eșuat (celelalte se scriu
oricum) sau când nu s-a găsit niciun fișier `.replay`.

## Ce iese {#what-comes-out}

| Fișier | Ce conține |
|---|---|
| `<demo>.parquet` | tabelul: pozițiile și evenimentele, câte un rând fiecare ([Tabelul](output-table.md)) |
| `<demo>.match.json` | documentul de meci ([Documentul de meci](output-match.md)) |
| `<demo>.entities.parquet` | fișier auxiliar: fiecare actualizare de proprietate și fiecare apel de la distanță, întregi |
| `<demo>.packets.parquet` | fișier auxiliar: bucățile fișierului și tot ce nu s-a citit, întreg |

Tabelul și documentul de meci sunt aceeași pereche pe care o scrie instrumentul 3DHeat CS2.
Vizualizatorul deschide tabelul direct și lasă fișierele auxiliare deoparte când se încarcă un dosar întreg.

## Exemple {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` este un dosar de exemplu de pe unitatea D: folosiți-l pe al dumneavoastră.
