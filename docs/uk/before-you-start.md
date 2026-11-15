---
title: Перш ніж почати
nav_order: 1.5
lang: uk
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Перш ніж почати {#before-you-start}

Ви лише починаєте працювати з командним рядком? Ця сторінка проведе вас від
нуля до першого запуску. Це займе близько десяти хвилин, один раз.

## 1. Встановіть Python {#install-python}

Для цього інструмента потрібен **Python 3.10 або новіший**.

- **Windows:** завантажте Python на [python.org/downloads](https://www.python.org/downloads/)
  і запустіть інсталятор. На його першому екрані позначте **Add python.exe to PATH**,
  потім натисніть **Install Now**.
- **macOS і Linux:** Python 3 часто вже є в системі. Там, де на цих сторінках
  написано `python`, введіть `python3`.

## 2. Отримайте цей інструмент {#get-this-tool}

Відкрийте [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad),
натисніть зелену кнопку **Code**, потім **Download ZIP**, і розпакуйте архів
в папку на свій вибір. Якщо ви користуєтеся git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Відкрийте термінал у цій папці {#open-a-terminal-in-that-folder}

Термінал — це вікно, в яке ви вводите команди.

- **Windows:** відкрийте папку в Провіднику, клацніть у рядок адреси, введіть
  `powershell` і натисніть Enter. Відкриється синє або чорне вікно, вже в цій папці.
- **macOS:** відкрийте **Terminal**, введіть `cd ` (з пробілом), перетягніть
  папку у вікно і натисніть Enter.

`cd` означає «змінити папку»: `cd C:\Tools\3DHeat-Ext-Squad` переходить до цієї папки.

## 4. Встановіть інструмент {#install-the-tool}

Введіть це і натисніть Enter:

```bash
python -m pip install -e .
```

Наприкінці ви маєте побачити: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Запустіть його {#run-it}

```bash
heat3d-squad-demo --version
```

Ви маєте побачити щось на кшталт:

```text
heat3d-squad-demo 0.1.0
```

Далі: [Запис демо](recording.md), потім [Перетворення демо](converting.md).

## Як читати команди на цих сторінках {#how-to-read-the-commands-on-these-pages}

| Ви бачите | Це означає |
|---|---|
| `<folder>` | заповнювач: введіть своє значення замість нього, без `< >` |
| `[--force]` | необов'язково: можна пропустити або ввести так, як показано |
| `a\|b` | вибір: введіть `a` або `b` |
| `# a note` | коментар для вас: не вводьте його |
| `"C:\My Files\x"` | шлях із пробілами беріть у лапки |
| `D:\Demos` | приклад папки у Windows: використовуйте свою |

## Якщо щось пішло не так {#when-something-goes-wrong}

| Повідомлення | Що робити |
|---|---|
| `'python' is not recognized` | Python не встановлено або не було позначено PATH: встановіть його знову і позначте (або введіть `py` замість `python`). |
| `'heat3d-squad-demo' is not recognized` | Виконайте крок 4 знову в папці інструмента або введіть `python -m heat3d_ext_squad` замість `heat3d-squad-demo`: результат той самий. |
| `No module named heat3d_ext_squad` | Ви не в папці інструмента або крок 4 не вдався: перейдіть туди командою `cd` і виконайте крок 4. |
| `No module named pip` | Виконайте `python -m ensurepip`, потім крок 4. |
| інше | Прочитайте останній рядок повідомлення і створіть issue на GitHub з цим рядком. |

Кожна команда також завершується **кодом виходу**: 0 означає, що все вдалося.
Щоб його побачити, введіть `echo $LASTEXITCODE` у PowerShell або `echo $?` на
macOS і Linux.
