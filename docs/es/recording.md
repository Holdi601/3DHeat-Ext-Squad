---
title: Grabar una demo
nav_order: 2
lang: es
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Grabar una demo {#recording-a-demo}

Las demos de Squad se graban **en el servidor**, no por el cliente del juego.

1. En el `Admins.cfg` del servidor, dale al grupo del admin el permiso `demos`.
2. En la consola del juego, ejecuta `AdminDemoRec <name>` cuando empiece la partida.
   Un admin tiene que escribirlo en el propio juego; un informe dice que RCON no lo acepta.
3. Juega la partida y después ejecuta `AdminDemoStop`.
4. La demo se escribe en `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Cópiala desde el servidor a la máquina que la convierte.

`Server.cfg` también tiene un ajuste `RecordDemos`, desactivado por defecto. Cabe esperar unos 70 a 80 MB
por hora para una partida pequeña; el tamaño de un servidor completo de 100 jugadores no se ha medido.

Una demo contiene los nombres y los identificadores en línea de todas las personas del servidor:
trátala como dato personal ([Límites, actualizaciones y condiciones](limits.md#personal-data)).

Siguiente: [Convertir demos](converting.md).
