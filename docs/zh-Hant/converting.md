---
title: "轉換對戰"
nav_order: 3
lang: "zh-Hant"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# 轉換對戰 {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## 逐步說明 {#step-by-step}

第一次使用命令列？請先閱讀[開始之前](before-you-start.md)。

1. 安裝一次：`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`，
   在該資料夾中開啟終端機，執行 `python -m pip install -e .`
   （Python 3.10 或更新版本；它會一併安裝 pyarrow 和 numpy）。
2. 把 `.replay` 檔放進一個資料夾，或一個一個指定檔名。
3. 執行 `heat3d-squad-demo <folder> -o out`。
4. 你會看到每一場對戰各一行，顯示它的圖層、玩家、資料列數，以及表格寫到哪裡。每場對戰會在 `out/<map>/` 中變成四個獨立檔案（不是 `.3dheat` 容器）；請在 3DHeat 檢視器中載入 `.parquet`。

![在合成對戰上執行的結果](../assets/img/run.svg)

這張圖是在測試建立的對戰上執行的結果（`tests/test_stream.py`），
不是真實的比賽。

## 選項 {#options}

| 選項 | 預設 | 作用 |
|---|---|---|
| `demos`（一或多個） | - | `.replay` 檔，或放有這些檔案的資料夾 |
| `-o`、`--out` | 必填 | 寫入的資料夾；每場對戰會寫入 `<out>/<map>/` |
| `--flat` | 關閉 | 直接寫入該資料夾，不建立 `<map>/` 資料夾 |
| `--json` | 關閉 | 在標準輸出印出每場對戰一行 JSON（供呼叫此指令的程式使用）：`demo`、`ok`、`parquet`、`match`、`sidecars`、`lost`、`rows`、`players`、`layer`、`recorded_unix`；失敗的對戰則印出 `demo`、`ok: false` 與 `error` |
| `--version` | - | 印出版本並結束 |

程式列出的每個選項：[指令參考](../cli-reference.md)。

地圖資料夾的名稱取自對戰所記錄的關卡路徑
（`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` 會得到 `<Map>`）。

結束狀態：所有對戰都轉換成功時為 0；任何一場失敗（其他的仍會寫入）或找不到任何 `.replay` 檔時為 1。

## 會輸出什麼 {#what-comes-out}

| 檔案 | 內容 |
|---|---|
| `<demo>.parquet` | 表格：位置與事件，每筆一列（[表格](output-table.md)） |
| `<demo>.match.json` | 對戰文件（[對戰文件](output-match.md)） |
| `<demo>.entities.parquet` | 附屬檔：每一次屬性更新與遠端呼叫，完整保留 |
| `<demo>.packets.parquet` | 附屬檔：檔案的區塊，以及未能讀取的所有內容，完整保留 |

表格與對戰文件，與 3DHeat CS2 工具寫出的那一組相同。
載入整個資料夾時，檢視器會直接開啟表格，並忽略附屬檔。

## 範例 {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` 是 D 槽上的範例資料夾，請改用你自己的路徑。
