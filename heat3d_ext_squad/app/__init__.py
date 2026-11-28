"""
The standalone 3DHeat extractor app: the same few modules in every extractor
repository (copied, never shared as a package, so each tool stays its own
project). The tool's own part is its `standalone_spec.py`.

- entry.py     the executable's command line (GUI without arguments)
- gui.py       the window (Tkinter)
- spec.py      what a tool declares: games, checks, maps, tasks
- manifest.py  what was extracted, so new and changed maps (and other content, new items) are found
- guard.py     check-new's manners: skip a game that runs or updates, low priority
- update.py    updates from the tool's GitHub releases, asked first, verified
- paths.py     levels folder, settings, Steam libraries on every system
"""

TEMPLATE = "1"
