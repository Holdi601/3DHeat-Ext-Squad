---
title: Convertir demos
nav_order: 3
lang: ca
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Convertir demos {#converting-demos}

```text
heat3d-squad-demo <demos o carpetes> -o <carpeta> [--flat] [--json]
python -m heat3d_ext_squad ...          el mateix, sense instal·lar-lo
```

## Pas a pas {#step-by-step}

Si ets nou amb la línia d'ordres, llegeix primer [Abans de començar](before-you-start.md).

1. Instal·la-la una vegada: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   obre una terminal en aquesta carpeta i executa `python -m pip install -e .`
   (Python 3.10 o posterior; porta pyarrow i numpy).
2. Posa els fitxers `.replay` en una carpeta, o anomena'ls un per un.
3. Executa `heat3d-squad-demo <carpeta> -o out`.
4. Hauries de veure una línia per demo: la seva capa, els jugadors i les files, i on
   ha anat la taula. Cada demo es converteix en quatre fitxers sols dins de `out/<mapa>/`
   (no en un contenidor `.3dheat`); carrega el `.parquet` al visualitzador de 3DHeat.

![Una execució sobre una demo sintètica](../assets/img/run.svg)

La imatge mostra una execució sobre una demo que construeixen les proves (`tests/test_stream.py`),
no sobre una partida real.

## Opcions {#options}

| Opció | Per defecte | Què fa |
|---|---|---|
| `demos` (una o més) | - | fitxers `.replay`, o carpetes que els contenen |
| `-o`, `--out` | obligatòria | la carpeta on escriure; cada demo va a `<out>/<mapa>/` |
| `--flat` | desactivada | escriu directament a la carpeta, sense la carpeta `<mapa>/` |
| `--json` | desactivada | imprimeix una línia de JSON per demo a la sortida (per als programes que criden l'ordre): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; una demo que ha fallat imprimeix `demo`, `ok: false` i `error` en lloc d'això |
| `--version` | - | imprimeix la versió i s'atura |

Totes les opcions, tal com les imprimeix el programa: [Referència de l'ordre](../cli-reference.md).

La carpeta del mapa és el nom del mapa, pres de la ruta del nivell que indica la demo
(`/Game/Maps/<Mapa>/Gameplay_Layers/<Capa>` dóna `<Mapa>`).

Estat de sortida: 0 quan s'han convertit totes les demos; 1 quan n'ha fallat alguna
(les altres s'escriuen igualment) o quan no s'ha trobat cap fitxer `.replay`.

## Què surt {#what-comes-out}

| Fitxer | Què conté |
|---|---|
| `<demo>.parquet` | la taula: posicions i esdeveniments, una fila cadascun ([La taula](output-table.md)) |
| `<demo>.match.json` | el document de partida ([El document de partida](output-match.md)) |
| `<demo>.entities.parquet` | annex: cada actualització de propietat i cada crida remota, senceres |
| `<demo>.packets.parquet` | annex: els blocs del fitxer i tot el que no s'ha llegit, sencer |

La taula i el document de partida són el mateix parell que escriu l'eina CS2 de 3DHeat.
El visualitzador obre la taula directament i deixa sense carregar els annexos
quan es carrega una carpeta sencera.

## Exemples {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # totes les demos d'una carpeta
heat3d-squad-demo one.replay two.replay -o out --flat  # directament a out/
heat3d-squad-demo D:\SquadDemos -o out --json          # una línia JSON per demo
```

`D:\SquadDemos` és una carpeta d'exemple de la unitat D: fes servir la teva.
