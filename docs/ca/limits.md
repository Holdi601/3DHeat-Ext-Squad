---
title: Límits, actualitzacions i condicions
nav_order: 7
lang: "ca"
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Límits, actualitzacions i condicions {#limits-updates-and-terms}

## No es llegeix {#not-read}

- **Qui va matar a qui, i el dany als soldats per impacte.** Això viatja als resultats d'impacte de les crides remotes de les armes i dels estats dels jugadors (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), l'estructura de les quals no es llegeix; es guarda sencera a l'annex d'entitats. Només es descodifica la salut de les víctimes.
- **L'equip del bot.** L'estat d'un bot porta un número que podria ser el seu equip; no confirmat, no utilitzat.
- **Cap a on mira un soldat de costat**, més enllà del guinyament del cos.

## Actualitzacions del joc {#game-updates}

El lector depèn del format de repetició del motor i d'un grapat de noms de classe i de propietat de Squad. No depèn de dissenys de propietats que no pot veure: la repetició els anomena ella mateixa.

**Què pot trencar-se amb una actualització de Squad:**

- **Una actualització del motor.** Squad va passar a UE 5.7 amb la v10.4, i això no s'ha provat allà. L'actualització pot canviar la capçalera del paquet, les dades d'aparició o `FRepMovement`. Aquests punts estan condicionats per versió al codi on es coneix el pas. Els passos desconeguts (`ENG_PARTIAL_CUSTOM_EXPORTS`, el bit de moviment final) estan fixats al que fa la v10.3.1.
- **Replicació Iris.** Si Squad hagués passat a Iris, el flux dins dels blocs seria nou i aquest lector no el llegiria. Squad v10.3.1 utilitza el sistema clàssic (funciona amb ReplicationGraph).
- **Classes o propietats reanomenades.** Si Squad reanomena les seves classes de jugador, d'equip o d'esquadró, o les seves propietats, els noms o els equips desapareixerien, però les posicions no.
- **Què passa quan falla.** Quan el format canvia, el lector falla en veu alta amb errors de flux o de moviment als diagnòstics. No produeix posicions errònies en silenci: `FRepMovement` només s'accepta quan els seus bits quadren exactament.

## Dades personals {#personal-data}

Una demo conté els noms i els identificadors en línia de tots els del servidor. La taula i el document de partida porten noms, no identificadors. Els annexos guarden els bits de cada propietat, de manera que contenen els identificadors tal com els té la demo (sense descodificar). Tracta-los tots com la pròpia demo.

## Llicència i fonts {#licence-and-sources}

MIT; mira [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Tot el que hi ha aquí s'ha escrit per a aquest paquet. No s'inclou ni s'enllaça cap codi de tercers: les úniques dependències són pyarrow (Apache-2.0) i numpy (BSD-3-Clause).

Les dades sobre el format provenen d'aquestes fonts:

- **Unreal.Core** a [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Descriu la disposició genèrica de les repeticions d'Unreal: el bloc d'informació, els blocs, els fotogrames, els paquets i les exportacions de camps de xarxa.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Se'n va llegir l'analitzador per a la disposició tal com l'escriu Squad v10.3.1, per a les comprovacions de versió, i per saber quines classes de Squad porten les dades de la plantilla. Les seves demos de prova publicades i els recomptes d'instantànies es van utilitzar com a verificació creuada independent. Cap dels seus codis no es va copiar ni traduir: aquest lector està estructurat d'una altra manera (un arxiu de bits en Python sobre paquets sencers, paquets parcials units bit a bit, propietats despatxades pel nom), i dues coses que no fa es van trobar aquí sobre les mateixes demos: el tercer indicador de paquet parcial i el bit de moviment final.

Squad és una marca registrada d'Offworld Industries. Aquest paquet llegeix fitxers que escriu un servidor de Squad; no toca el joc, el seu codi ni els seus arxius. La política de llicències i administració de servidors d'Offworld no diu res sobre la gravació o l'anàlisi de demos. El EULA de Squad prohibeix l'enginyeria inversa del propi joc, cosa que això no fa.
