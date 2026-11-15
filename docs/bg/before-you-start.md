---
title: "Преди да започнете"
nav_order: 1.5
lang: "bg"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Преди да започнете {#before-you-start}

Нов ли сте в командния ред? Тази страница ви води от нищо до първо пускане.
Отнема около десет минути, веднъж.

## 1. Инсталирайте Python {#install-python}

Този инструмент изисква **Python 3.10 или по-нов**.

- **Windows:** изтеглете Python от [python.org/downloads](https://www.python.org/downloads/)
  и стартирайте инсталатора. На първия екран отметнете **Add python.exe to PATH**,
  после щракнете **Install Now**.
- **macOS и Linux:** Python 3 често вече е там. Където тези страници пишат
  `python`, напишете `python3`.

## 2. Вземете този инструмент {#get-this-tool}

Отворете [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), щракнете
зеления бутон **Code**, после **Download ZIP**, и разархивирайте в папка по ваш избор. Ако използвате git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Отворете терминал в тази папка {#open-a-terminal-in-that-folder}

Терминалът е прозорец, в който въвеждате команди.

- **Windows:** отворете папката в Explorer, щракнете в адресния ред, напишете
  `powershell` и натиснете Enter. Отваря се син или черен прозорец, вече в тази
  папка.
- **macOS:** отворете **Terminal**, напишете `cd ` (с интервал), плъзнете папката
  в прозореца и натиснете Enter.

`cd` означава „смени папката“: `cd C:\Tools\3DHeat-Ext-Squad` отива в тази папка.

## 4. Инсталирайте инструмента {#install-the-tool}

Напишете това и натиснете Enter:

```bash
python -m pip install -e .
```

В края трябва да видите: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Стартирайте го {#run-it}

```bash
heat3d-squad-demo --version
```

Трябва да видите нещо такова:

```text
heat3d-squad-demo 0.1.0
```

Следва: [Записване на демо](recording.md), после [Преобразуване на демота](converting.md).

## Как да четете командите на тези страници {#how-to-read-the-commands-on-these-pages}

| Виждате | Означава |
|---|---|
| `<folder>` | място за попълване: напишете своята стойност вместо това, без `< >` |
| `[--force]` | по желание: пропуснете го или го напишете, както е показано |
| `a\|b` | избор: напишете `a` или `b` |
| `# a note` | бележка за вас: не я пишете |
| `"C:\My Files\x"` | път с интервали заключете в кавички |
| `D:\Demos` | примерна папка в Windows: използвайте своя |

## Когато нещо се обърка {#when-something-goes-wrong}

| Съобщението | Какво да направите |
|---|---|
| `'python' is not recognized` | Python не е инсталиран или не е отметнато полето PATH: инсталирайте го отново и го отметнете (или напишете `py` вместо `python`). |
| `'heat3d-squad-demo' is not recognized` | Стартирайте стъпка 4 отново в папката на инструмента или напишете `python -m heat3d_ext_squad` вместо `heat3d-squad-demo`: действа същото. |
| `No module named heat3d_ext_squad` | Не сте в папката на инструмента или стъпка 4 не е минала: `cd` до нея и стартирайте стъпка 4. |
| `No module named pip` | Стартирайте `python -m ensurepip`, после стъпка 4. |
| всичко друго | Прочетете последния ред на съобщението, после отворете issue в GitHub с него. |

Всяка команда завършва и със **статус на изход**: 0 означава, че е минала. За да го видите,
напишете `echo $LASTEXITCODE` в PowerShell или `echo $?` в macOS и Linux.
