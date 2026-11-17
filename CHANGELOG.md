# Changelog

## 0.1.0

- Squad server demos (`.replay`) into a heatmap table and a match document.
- Everything a demo holds: bots, health, wounds, revives, deaths, vehicles,
  deployables, seats, shots and vehicle hits.
- Nothing lost: a completeness self-check and two raw sidecars.
- `--flat`, `--json`, `--version`.
- Installs with one pip line from the release zip, no Git needed; a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

## Docs

Where each feature is documented
([holdi601.github.io/3DHeat-Ext-Squad](https://holdi601.github.io/3DHeat-Ext-Squad/)):

| Feature | Page |
|---|---|
| Installing, a first run | [Before you start](docs/before-you-start.md) |
| Recording a demo on the server | [Recording a demo](docs/recording.md) |
| The command and its options (`-o`, `--flat`, `--json`, `--version`) | [Converting demos](docs/converting.md), [Command reference](docs/cli-reference.md) |
| The table: columns and events | [The table](docs/output-table.md) |
| The match document, the sidecars, the self-check | [The match document and sidecars](docs/output-match.md) |
| How a demo is read, and how it was checked | [How a demo is read](docs/how-it-works.md) |
| What is not read, game updates, personal data, licence | [Limits, updates and terms](docs/limits.md) |
| Release checklist for the docs | [Maintaining these docs](docs/maintaining.md) |
