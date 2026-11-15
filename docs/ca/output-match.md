---
title: El document de partida i els annexos
nav_order: 5
lang: ca
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# El document de partida i els annexos {#the-match-document-and-sidecars}

Al costat de la taula, cada demo obté `<demo>.match.json` i dos annexos,
`<demo>.entities.parquet` i `<demo>.packets.parquet`. El visualitzador llegeix el
document de partida a la seva pestanya Partida.

## El document de partida {#the-match-document}

`<demo>.match.json` (el document de partida) conté al seu nivell superior `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` i `selfCheck` (la llista completa: [Referència de l'ordre](../cli-reference.md)). Amb paraules: el mapa i el nivell, les versions del joc i del motor, el moment de la gravació, la durada, i:

- **els equips**: número, facció i tot el que han replicat els seus estats (tiquets, disponibilitats, comandant) a mesura que canviava;
- **els esquadrons**: número, equip, nom, creador, líder, membres;
- **l'estat del joc**: nom i opcions del servidor, mode de joc, estat i identificador de la partida, rotacions de mapes i de nivells, votacions, temporitzadors, el missatge del dia;
- **els actors**: cada vehicle, element desplegable, emplaçament, caixa de munició i helicòpter: classe, on i quan va aparèixer, quan va marxar, de qui era, i el seu estat replicat (salut, estat de construcció, seients...);
- **una línia per a cada jugador**: mostres a peu i en vehicles, distància recorreguda, classes de soldat jugades, vehicles utilitzats, canvis d'equip, seients ocupats, i tot el que ha replicat l'estat del jugador (ping, nivell, rol, seient actual...); i una línia per a cada bot;
- **els esdeveniments** comptats, el **cens de propietats** (quantes vegades es va enviar cada propietat de cada classe) i el **cens de crides remotes**, els trets i impactes, el que **no** es va llegir, i els diagnòstics del lector;
- **el fitxer i la capçalera**: cada camp del bloc d'informació i de la capçalera de la demo, la taula de blocs, les taules d'exportació de camps de xarxa (`net_field_exports`), els motius de tancament dels canals, i les classes trobades per als objectes que les exportacions no anomenen (`stream.class_resolution`);
- **la comprovació** (`selfCheck.completeness`, mira [Completesa](#completeness)).

Els identificadors en línia (Steam, EOS) s'han deixat fora a propòsit.

Una ullada ràpida a una demo convertida:

```bash
python -c "import json; d = json.load(open('out/<mapa>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Completesa {#completeness}

Aquest lector segueix la regla que comparteixen tots els convertidors de 3DHeat: descodificar el que es pot llegir ara, guardar la resta sencera, i dir quanta part de cada tipus ha fet ([Els convertidors ho guarden tot](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Cada document de partida té `selfCheck.completeness`: per a cada tipus d'element trobat a la demo, quants han estat `seen` (vists), `decoded` (descodificats), `partial` (descodificats en part i guardats sencers), `raw` (només guardats sencers) i `lost` (perduts, ha de ser 0). Els tipus es compten on el lector els troba: `file.info`, `chunk.<tipus>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<classe>`, `rpc:<classe>`, `block:<objecte>`, `subobject.*`.

A les demos reals llegides, `lost` és 0: els seus elements van de centenars de milers a milions; uns la meitat es descodifiquen del tot, la resta són parcials o crues.

**Llegit** (a la taula i al document de partida):

- el bloc d'informació, la capçalera de la demo (cada camp; dos bytes finals que no es coneixen es guarden en hexadecimal), la taula de blocs;
- cada fotograma, paquet i paquet (dividit sencer en el que porta), cada actor obert (amb la seva ubicació d'aparició, rotació, escala i velocitat) i tancat (amb el motiu: `Destroyed`, `Dormancy`...);
- cada propietat replicada, fins on diguin els seus bits ([Descodificar propietats](how-it-works.md#decoding-properties)), posicions de `FRepMovement` i del component de moviment dels helicòpters, les baixes, la salut dels vehicles, els seients;
- cada crida remota pel nom, amb els seus paràmetres quan la demo exporta el grup de la funció: trets (`fire`) i impactes en vehicles (`hit`) a la taula;
- les taules d'exportació de camps de xarxa i els GUID de xarxa (el seu recompte; les rutes són a l'annex d'entitats).

**Guardat cru** (sencer, amb el que s'ha llegit al costat):

- `<demo>.entities.parquet`, columnes `time`, `type` (`<classe>.<propietat>`, `<classe>.<crida>`, o el nom de l'objecte), `name` (la classe de l'actor), `entity` (el GUID de xarxa de l'actor, com el `entity` de la taula), `kind`, `object` (el subobjecte), `channel`, `handle`, `group` (la ruta de classe del grup d'exportació), `decoded` (JSON), `bits` i `payload` (els bits, el més baix primer, completats fins a bytes sencers):
  - cada actualització de propietat (`kind` `property`), el moviment inclòs, amb el que es descodifica; crua només on no n'hi ha res descodificat (identificadors sense nom, estructures com `RotationReplicatedMovement` de torretes, i propietats deixades com a bits);
  - cada crida remota i camp de delta personalitzat (`rpc`), amb els paràmetres descodificats quan es va exportar el grup de la funció; crua on no (`RepInventory`, `PlayerStateData`);
  - cada bloc de contingut d'un objecte la classe del qual no es va trobar (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), amb la seva capçalera descodificada;
  - cada canal d'actor obert i tancat (`open`, `close`), cada subobjecte esborrat o destruït;
  - el context que necessita un descodificador posterior per llegir el fitxer sol: cada exportació de camp de xarxa (`export.field`: ruta del grup, identificador, nom de propietat, suma de verificació) i cada GUID de xarxa exportat (`export.guid`: la seva ruta, extern i indicadors), en el moment en què el flux els va donar.
- `<demo>.packets.parquet`, columnes `time`, `type`, `name`, `channel`, `offset` (al fitxer), `decoded`, `bits`, `payload`: el bloc d'informació, el bloc de capçalera, cada bloc de punt de control (un punt de control és l'estat de cada actor en el seu moment, que el flux des de l'inici també conté), cada bloc d'esdeveniment, i cada fotograma, paquet o paquet que no es llegeix (un paquet per demo: el paquet d'obertura de l'espectador propi del gravador), sencer.

Les files de les entitats s'agrupen per `kind`, `type` i `entity`, cada una en ordre de temps; ordena per `time` per a l'ordre del flux.

**No disponible:**

- el que una demo de servidor no grava: les entrades dels clients, el que veia un jugador;
- els efectes del costat del client: marques d'impacte, sons, el text del registre de baixes (el servidor envia les crides, no la seva visualització);
- els identificadors en línia descodificats: guardats només com a bits (mira [Dades personals](limits.md#personal-data)).
