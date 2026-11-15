---
title: Before you start
nav_order: 1.5
---

# Before you start

New to the command line? This page takes you from nothing to a first run.
It takes about ten minutes, once.

## 1. Install Python

This tool needs **Python 3.10 or later**.

- **Windows:** download Python from [python.org/downloads](https://www.python.org/downloads/)
  and run the installer. On its first screen, tick **Add python.exe to PATH**,
  then click **Install Now**.
- **macOS and Linux:** Python 3 is often there already. Where these pages say
  `python`, type `python3`.

## 2. Get this tool

Open [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), click the
green **Code** button, then **Download ZIP**, and unzip it into a folder of your
choice. If you use git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Open a terminal in that folder

A terminal is a window where you type commands.

- **Windows:** open the folder in Explorer, click into the address bar, type
  `powershell` and press Enter. A blue or black window opens, already in that
  folder.
- **macOS:** open **Terminal**, type `cd ` (with a space), drag the folder into
  the window and press Enter.

`cd` means "change folder": `cd C:\Tools\3DHeat-Ext-Squad` goes to that folder.

## 4. Install the tool

Type this and press Enter:

```bash
python -m pip install -e .
```

You should see, at the end: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Run it

```bash
heat3d-squad-demo --version
```

You should see something like:

```text
heat3d-squad-demo 0.1.0
```

Next: [Recording a demo](recording.md), then [Converting demos](converting.md).

## How to read the commands on these pages

| You see | It means |
|---|---|
| `<folder>` | a placeholder: type your own value instead, without the `< >` |
| `[--force]` | optional: leave it out, or type it as shown |
| `a\|b` | a choice: type `a` or `b` |
| `# a note` | a comment for you: do not type it |
| `"C:\My Files\x"` | put a path that has spaces in quotes |
| `D:\Demos` | an example Windows folder: use your own |

## When something goes wrong

| The message | What to do |
|---|---|
| `'python' is not recognized` | Python is not installed, or the PATH box was not ticked: install it again and tick it (or type `py` instead of `python`). |
| `'heat3d-squad-demo' is not recognized` | Run step 4 again in the tool's folder, or type `python -m heat3d_ext_squad` instead of `heat3d-squad-demo`: it does the same. |
| `No module named heat3d_ext_squad` | You are not in the tool's folder, or step 4 failed: `cd` there and run step 4. |
| `No module named pip` | Run `python -m ensurepip`, then step 4. |
| anything else | Read the last line of the message, then open an issue on GitHub with it. |

Every command also ends with an **exit status**: 0 means it worked. To see it,
type `echo $LASTEXITCODE` in PowerShell or `echo $?` on macOS and Linux.
