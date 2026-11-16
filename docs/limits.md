---
title: Limits, updates and terms
nav_order: 7
---

# Limits, updates and terms

## Not read

- **Who killed whom, and damage to soldiers by hit.** These travel in the hit results of the weapons' and player states' remote calls (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), whose structure is not read; they are kept whole in the entities sidecar. Only the victims' health is decoded.
- **The bot's team.** A bot's state carries a number that may be its team; not confirmed, not used.
- **Where a soldier looks sideways** beyond the body's yaw.

## Game updates

The reader depends on the engine's replay format and a handful of Squad class and property names. It does not depend on property layouts it cannot see: the replay names those itself.

**What can break with a Squad update:**

- **An engine upgrade.** Squad moved to UE 5.7 with v10.4, and this is untested there. The upgrade can change the bunch header, the spawn data or `FRepMovement`. These are version-gated in the code where the step is known. Unknown steps (`ENG_PARTIAL_CUSTOM_EXPORTS`, the trailing movement bit) are pinned to what v10.3.1 does.
- **Iris replication.** If Squad switched to Iris, the stream inside the chunks would be new and this reader would not read it. Squad v10.3.1 uses the classic system (it runs ReplicationGraph).
- **Renamed classes or properties.** If Squad renamed its player, team or squad classes or their properties, names or teams would go missing, but positions would not.
- **What happens on failure.** When the format changes, the reader fails loudly with stream errors or movement errors in the diagnostics. It does not quietly produce wrong positions: `FRepMovement` is only accepted when its bits add up exactly.

## Personal data

A demo holds the names and online IDs of everyone on the server. The table and match document carry names, not IDs. The sidecars keep every property's bits, so they hold the IDs as the demo does (not decoded). Treat all of them like the demo itself.

## Licence and sources

MIT; see [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Everything here was written for this package. No third-party code is included or linked: the only dependencies are pyarrow (Apache-2.0) and numpy (BSD-3-Clause).

Facts about the format came from these sources:

- **Unreal.Core** in [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). It describes the generic Unreal replay layout: the info block, chunks, frames, bunches and net field exports.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Its parser was read for the layout as Squad v10.3.1 writes it, for the version checks, and for which Squad classes carry roster data. Its published test demos and snapshot counts were used as an independent cross-check. None of its code was copied or translated: this reader is structured differently (a Python bit archive over whole packets, partial bunches joined bitwise, properties dispatched by name), and two things it does not do were found here on the demos themselves: the third partial-bunch flag and the trailing movement bit.

This package reads the demo files a Squad server writes; it does not touch the game, its code or its archives, and nothing from the game is included or redistributed. What it writes stays on your machine.

3DHeat is not affiliated with or endorsed by Offworld Industries. Squad and related names and trademarks belong to their owners.

Rights holders: open an issue at <https://github.com/Holdi601/3DHeat-Ext-Squad/issues> - we respond quickly and remove anything on request.
