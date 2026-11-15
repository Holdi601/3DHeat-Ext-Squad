---
title: "對戰文件與附屬檔"
nav_order: 5
lang: zh-Hant
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# 對戰文件與附屬檔 {#the-match-document-and-sidecars}

每場轉換後的對戰，除了表格之外，還會產生 `<demo>.match.json` 與兩個附屬檔，
`<demo>.entities.parquet` 與 `<demo>.packets.parquet`。檢視器會在它的對戰分頁中讀取對戰文件。

## 對戰文件 {#the-match-document}

`<demo>.match.json`（對戰文件）的頂層包含 `map`、`layer`、`level_path`、`game_version`、`engine_version`、`recorded_unix`、`duration_s`、`teams`、`squads`、`game_state`、`actors`、`players`、`rows`、`events`、`not_read`、`file`、`header`、`chunks`、`stream`、`shots` 與 `selfCheck`（完整清單：[指令參考](../cli-reference.md)）。簡單來說：地圖與圖層、遊戲與引擎版本、錄製時間、長度，以及：

- **隊伍**：編號、陣營，以及其狀態所複製的所有內容（點數、可用性、指揮官），依變動時間排列；
- **小隊**：編號、隊伍、名稱、建立者、隊長、成員；
- **遊戲狀態**：伺服器名稱與設定、遊戲模式、比賽狀態與 ID、地圖與圖層輪替、投票、計時器、每日訊息；
- **actor**：每一輛載具、可部署物、砲台、彈藥箱與直升機，包括其類別、位置與生成時間、消失時間、所有者，以及其複製的狀態（生命值、建造狀態、座位……）；
- **每位玩家一行**：步行與乘坐載具時的取樣、步行距離、所扮演的士兵類別、所使用的載具、隊伍變更、所坐的座位，以及玩家狀態所複製的一切（延遲、等級、角色、目前座位……）；每個機器人也各一行；
- **事件**的計數、**屬性普查**（每個類別的屬性被送出的頻率）與**遠端呼叫普查**、射擊與命中、**未被讀取**的內容，以及讀取器的診斷；
- **檔案與標頭**：資訊區塊與對戰標頭的每個欄位、區塊表、網路欄位匯出表（`net_field_exports`）、通道的關閉原因，以及為匯出資料未指名的物件所找到的類別（`stream.class_resolution`）；
- **自我檢查**（`selfCheck.completeness`，見[完整性](#completeness)）。

線上 ID（Steam、EOS）刻意不包含在內。

快速查看一場已轉換的對戰：

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## 完整性 {#completeness}

本讀取器遵循所有 3DHeat 轉換器共同的規則：能現在解碼的就解碼，其餘完整保留，並說明每一類各保留了多少（[轉換器會保留一切](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)）。每份對戰文件都有 `selfCheck.completeness`：依每一類在對戰中遇到的項目，列出 `seen`（看到）、`decoded`（已解碼）、`partial`（部分解碼並完整保留）、`raw`（僅完整保留）與 `lost`（遺失，必須為 0）的數量。這些類別是在讀取器遇到時計數的：`file.info`、`chunk.<kind>`、`frame`、`packet`、`bunch`、`open`、`close`、`export.field`、`export.guid`、`external`、`property:<class>`、`rpc:<class>`、`block:<object>`、`subobject.*`。

在所讀取的真實對戰中，`lost` 為 0：它們的項目數從數十萬到數百萬不等；約一半完整解碼，其餘為部分或僅完整保留。

**已讀取**（進入表格與對戰文件）：

- 資訊區塊、對戰標頭（每個欄位；兩個未知的尾端位元組以十六進位保留）、區塊表；
- 每一個影格、封包與 bunch（完整拆分成其所承載的內容），每一個被開啟的 actor（包含其生成位置、旋轉、比例與速度）以及被關閉的 actor（附原因：`Destroyed`、`Dormancy`……）；
- 每一個複製屬性，只要其位元所能說明的部分（[解碼屬性](how-it-works.md#decoding-properties)）；來自 `FRepMovement` 的位置，以及來自直升機移動元件的位置、傷亡、載具生命值、座位；
- 每一個依名稱的遠端呼叫；若對戰匯出了該函式的群組，則附帶其參數：射擊（`fire`）與載具命中（`hit`）會進入表格；
- 網路欄位匯出表與網路 GUID（其數量；路徑在實體附屬檔中）。

**以原始形式保留**（完整保留，並在旁邊附上已讀取的部分）：

- `<demo>.entities.parquet`，欄位包括 `time`、`type`（`<class>.<property>`、`<class>.<call>`，或物件的名稱）、`name`（actor 的類別）、`entity`（actor 的網路 GUID，即表格中的 `entity`）、`kind`、`object`（子物件）、`channel`、`handle`、`group`（匯出群組的類別路徑）、`decoded`（JSON）、`bits` 與 `payload`（位元，由最低位元開始，補齊為完整位元組）：
  - 每一次屬性更新（`kind` 為 `property`），包括移動在內，並附上已解碼的內容；只有在沒有任何可解碼內容時才以原始形式保留（未命名的 handle、如砲塔的 `RotationReplicatedMovement` 等結構，以及仍以位元形式保留的屬性）；
  - 每一個遠端呼叫與自訂 delta 欄位（`rpc`），在函式群組已匯出時解碼其參數；未匯出時以原始形式保留（`RepInventory`、`PlayerStateData`）；
  - 每一個其類別無法找到的物件的內容區塊（`block`：`Buoyancy`、`GameplayTasksComponent`、`AmmoRackComponent`……），並解碼其標頭；
  - 每一個被開啟與關閉的 actor 通道（`open`、`close`），每一個被刪除或摧毀的子物件；
  - 後續解碼器只讀取該檔案就需要的上下文：每一個網路欄位匯出（`export.field`：群組路徑、handle、屬性名稱、校驗和），以及每一個被匯出的網路 GUID（`export.guid`：其路徑、外部物件與旗標），皆為串流給出時的時間點。
- `<demo>.packets.parquet`，欄位包括 `time`、`type`、`name`、`channel`、`offset`（在檔案中的位置）、`decoded`、`bits` 與 `payload`：資訊區塊、標頭區塊、每一個檢查點區塊（檢查點是每個 actor 在其時間點的狀態，從頭開始的串流也包含它）、每一個事件區塊，以及每一個無法讀取的影格、封包或 bunch（每場對戰一個 bunch：錄製者自己的觀戰者的開頭 bunch），完整保留。

實體附屬檔的列依 `kind`、`type` 與 `entity` 分組，每組內依時間排序；若要依串流的順序排列，請以 `time` 排序。

**不可用：**

- 伺服器對戰未記錄的內容：客戶端的輸入、玩家所看到的畫面；
- 客戶端的效果：命中標記、音效、擊殺提示的文字（伺服器傳送的是呼叫，而非其顯示畫面）；
- 已解碼的線上 ID：只以位元形式保留（見[個人資料](limits.md#personal-data)）。
