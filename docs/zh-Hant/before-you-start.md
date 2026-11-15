---
title: "開始之前"
nav_order: 1.5
lang: zh-Hant
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# 開始之前 {#before-you-start}

第一次使用命令列？這一頁會帶你從零開始完成第一次執行。
只要做一次，大約十分鐘。

## 1. 安裝 Python {#install-python}

這個工具需要 **Python 3.10 或更新版本**。

- **Windows：** 到 [python.org/downloads](https://www.python.org/downloads/) 下載 Python，然後執行安裝程式。
  在第一個畫面勾選 **Add python.exe to PATH**，
  再按 **Install Now**。
- **macOS 和 Linux：** Python 3 通常已經安裝好了。本頁若寫 `python`，請改輸入 `python3`。

## 2. 取得這個工具 {#get-this-tool}

開啟 [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad)，按綠色的 **Code** 按鈕，再按 **Download ZIP**，然後解壓縮到你選的資料夾。如果你用 git：`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`。

## 3. 在該資料夾開啟終端機 {#open-a-terminal-in-that-folder}

終端機是讓你輸入指令的視窗。

- **Windows：** 在檔案總管中打開該資料夾，點一下網址列，輸入
  `powershell` 再按 Enter。會開啟一個藍色或黑色的視窗，已經位於該資料夾中。
- **macOS：** 開啟**終端機**，輸入 `cd `（後面要有一個空格），把資料夾拖進視窗，再按 Enter。

`cd` 的意思是「切換資料夾」：`cd C:\Tools\3DHeat-Ext-Squad` 會前往那個資料夾。

## 4. 安裝這個工具 {#install-the-tool}

輸入以下內容，然後按 Enter：

```bash
python -m pip install -e .
```

最後你應該會看到：`Successfully installed heat3d-ext-squad-demo-...`。

## 5. 執行它 {#run-it}

```bash
heat3d-squad-demo --version
```

你應該會看到類似這樣的內容：

```text
heat3d-squad-demo 0.1.0
```

接下來：[錄製對戰](recording.md)，然後是[轉換對戰](converting.md)。

## 如何閱讀本頁的指令 {#how-to-read-the-commands-on-these-pages}

| 你看到的 | 意思 |
|---|---|
| `<folder>` | 佔位符：請改輸入你自己的值，不要輸入 `< >` |
| `[--force]` | 選用：可以不輸入，或照示輸入 |
| `a\|b` | 選擇：輸入 `a` 或 `b` |
| `# a note` | 給你看的註解：不要輸入 |
| `"C:\My Files\x"` | 路徑含有空格時，請用引號括起來 |
| `D:\Demos` | Windows 資料夾的範例：請改用你自己的 |

## 出問題時 {#when-something-goes-wrong}

| 訊息 | 該怎麼做 |
|---|---|
| `'python' is not recognized` | 尚未安裝 Python，或沒有勾選 PATH 選項：重新安裝並勾選（或改輸入 `py` 取代 `python`）。 |
| `'heat3d-squad-demo' is not recognized` | 在工具的資料夾中重新執行第 4 步，或改輸入 `python -m heat3d_ext_squad` 取代 `heat3d-squad-demo`：效果相同。 |
| `No module named heat3d_ext_squad` | 你不在工具的資料夾中，或第 4 步失敗：用 `cd` 前往該資料夾，再執行第 4 步。 |
| `No module named pip` | 執行 `python -m ensurepip`，然後執行第 4 步。 |
| 其他任何情況 | 看訊息的最後一行，然後附上它在 GitHub 上開一個 issue。 |

每個指令結束時都會有一個**結束狀態**：0 代表成功。要查看它，
在 PowerShell 中輸入 `echo $LASTEXITCODE`，在 macOS 和 Linux 中輸入 `echo $?`。
