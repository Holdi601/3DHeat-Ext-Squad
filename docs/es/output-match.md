---
title: El documento de la partida y los auxiliares
nav_order: 5
lang: es
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# El documento de la partida y los auxiliares {#the-match-document-and-sidecars}

Junto a la tabla, cada demo obtiene `<demo>.match.json` y dos auxiliares,
`<demo>.entities.parquet` y `<demo>.packets.parquet`. El visor lee el documento de la partida en su
pestaña Partida.

## El documento de la partida {#the-match-document}

`<demo>.match.json` (el documento de la partida) contiene en su nivel superior `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` y `selfCheck` (la lista completa: [Referencia de comandos](../cli-reference.md)). En palabras: el mapa y la capa, las versiones del juego y del motor, la hora de la grabación, la duración, y:

- **los equipos**: número, facción y todo lo que su estado replicó (tickets, disponibilidades, comandante) a medida que cambiaba;
- **las escuadras**: número, equipo, nombre, creador, líder, miembros;
- **el estado de la partida**: nombre y ajustes del servidor, modo de juego, estado y identificador de la partida, rotaciones de mapas y capas, votaciones, temporizadores, el mensaje del día;
- **los actores**: cada vehículo, elemento desplegable, emplazamiento, caja de munición y helicóptero: clase, dónde y cuándo apareció, cuándo se fue, de quién era, y su estado replicado (salud, estado de construcción, asientos...);
- **una línea por jugador**: muestras a pie y en vehículos, distancia recorrida, clases de soldado jugadas, vehículos usados, cambios de equipo, asientos ocupados, y todo lo que replicó el estado del jugador (ping, nivel, rol, asiento actual...); y una línea por cada bot;
- **los eventos** contados, el **censo de propiedades** (cuántas veces se envió cada propiedad de cada clase) y el **censo de llamadas remotas**, los disparos e impactos, lo que **no** se leyó, y los diagnósticos del lector;
- **el archivo y la cabecera**: cada campo del bloque de información y de la cabecera de la demo, la tabla de fragmentos, las tablas de exportación de campos de red (`net_field_exports`), los motivos de cierre de los canales, y las clases encontradas para objetos que las exportaciones no nombran (`stream.class_resolution`);
- **la autocomprobación** (`selfCheck.completeness`, ver [Completitud](#completeness)).

Los identificadores en línea (Steam, EOS) se dejan fuera a propósito.

Un vistazo rápido a una demo convertida:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Completitud {#completeness}

Este lector sigue la regla que comparten todos los convertidores de 3DHeat: decodificar lo que se puede leer ahora, guardar el resto completo, y decir cuánto hay de cada tipo ([Los convertidores lo guardan todo](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Cada documento de la partida tiene `selfCheck.completeness`: por cada tipo de elemento encontrado en la demo, cuántos fueron `seen` (vistos), `decoded` (decodificados), `partial` (decodificados en parte y guardados completos), `raw` (guardados completos solamente) y `lost` (debe ser 0). Los tipos se cuentan donde el lector los encuentra: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

En las demos reales leídas, `lost` es 0: sus elementos van de cientos de miles a millones; alrededor de la mitad se decodifica por completo, el resto es parcial o bruto.

**Se lee** (a la tabla y al documento de la partida):

- el bloque de información, la cabecera de la demo (cada campo; dos bytes finales no conocidos se guardan en hexadecimal), la tabla de fragmentos;
- cada trama, paquete y bunch (divididos enteros en lo que contienen), cada actor abierto (con su ubicación de aparición, rotación, escala y velocidad) y cerrado (con el motivo: `Destroyed`, `Dormancy`...);
- cada propiedad replicada, hasta donde indican sus bits ([Decodificar propiedades](how-it-works.md#decoding-properties)), posiciones desde `FRepMovement` y desde el componente de movimiento de los helicópteros, las bajas, la salud de los vehículos, los asientos;
- cada llamada remota por nombre, con sus parámetros allí donde la demo exporta el grupo de la función: disparos (`fire`) y golpes a vehículos (`hit`) a la tabla;
- las tablas de exportación de campos de red y los GUID de red (su número; las rutas están en el auxiliar de entidades).

**Se guarda en bruto** (completo, con lo que se lee de él al lado):

- `<demo>.entities.parquet`, columnas `time`, `type` (`<class>.<property>`, `<class>.<call>`, o el nombre del objeto), `name` (la clase del actor), `entity` (el GUID de red del actor, como la `entity` de la tabla), `kind`, `object` (el subobjeto), `channel`, `handle`, `group` (la ruta de clase del grupo de exportación), `decoded` (JSON), `bits` y `payload` (los bits, del menos significativo, rellenados hasta bytes completos):
  - cada actualización de propiedad (`kind` `property`), incluido el movimiento, con lo que se decodifica; en bruto solo donde no se decodifica nada (manejadores sin nombre, estructuras como `RotationReplicatedMovement` de torretas, y propiedades que quedan como bits);
  - cada llamada remota y campo de delta personalizado (`rpc`), con los parámetros decodificados donde se exportó el grupo de la función; en bruto donde no (`RepInventory`, `PlayerStateData`);
  - cada bloque de contenido de un objeto cuya clase no se pudo encontrar (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), con su cabecera decodificada;
  - cada canal de actor abierto y cerrado (`open`, `close`), cada subobjeto eliminado o destruido;
  - el contexto que un decodificador posterior necesita para leer el archivo por sí solo: cada exportación de campo de red (`export.field`: ruta del grupo, manejador, nombre de propiedad, suma de comprobación) y cada GUID de red exportado (`export.guid`: su ruta, su exterior e indicadores), en el momento en que el flujo los dio.
- `<demo>.packets.parquet`, columnas `time`, `type`, `name`, `channel`, `offset` (en el archivo), `decoded`, `bits`, `payload`: el bloque de información, el fragmento de cabecera, cada fragmento de punto de control (un punto de control es el estado de cada actor en su momento, que el flujo desde el principio también contiene), cada fragmento de eventos, y cada trama, paquete o bunch que no se lee (un bunch por demo: el bunch de apertura del propio actor espectador del grabador), completo.

Las filas de entidades se agrupan por `kind`, `type` y `entity`, cada una en orden de tiempo; ordena por `time` para el orden del flujo.

**No disponible:**

- lo que una demo de servidor no registra: las entradas de los clientes, lo que veía un jugador;
- efectos del lado del cliente: marcadores de impacto, sonidos, el texto del registro de bajas (el servidor envía las llamadas, no su visualización);
- identificadores en línea decodificados: se guardan solo como bits (ver [Datos personales](limits.md#personal-data)).
