---
title: "維護這些文件"
nav_order: 91
lang: zh-Hant
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# 維護這些文件 {#maintaining-these-docs}

每次發行版本時都要檢查的清單，確保文件永遠跟得上程式碼。

1. **重新產生參考資料。** `python tools/gen_docs_reference.py` 會根據程式自身的 `--help` 與輸出欄位，重寫[命令參考](../cli-reference.md)。
   `python tools/gen_docs_reference.py --check` 在已提交的頁面過時時會以結束碼 1 結束。
2. **列出有什麼改變。** `git log v<VERSION>..HEAD --oneline`，其中
   `<VERSION>` 是最近一次發行的版本（發行時的 `VERSION` 檔案）。每一項新功能、選項與輸出欄位，都要在某一頁中有對應的位置，並在 [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md) 的 **Docs** 區段中有一列。
3. **獨立審閱。** 由沒有撰寫這些頁面的人，把 README 與每一頁改動過的內容（包括圖片）各讀三遍：一次以從未用過終端機的初學者身分，一次以八歲孩子的身分，一次以逐項比對 `--help` 的專家身分。範例只使用虛構的名稱與數字。
4. **修正** 審閱找到的所有問題。
5. **翻譯。** 每個翻譯頁都會記錄它所依據的英文頁面雜湊值。英文來源有變動的頁面要重新翻譯，然後逐一審閱每種語言：文字清楚、圖表標籤正確，並與 3DHeat 檢視器的已翻譯介面使用相同的字詞。
6. **執行測試**（`pytest`）。
7. **推送** 只能在擁有者同意之後進行。

## 翻譯：命令 {#translations-the-commands}

本網站以 3DHeat 檢視器支援的 40 種語言翻譯：英文位於 `docs/`，其他每種語言位於 `docs/<lang>/`，檔名相同。`tools/docs_i18n.py` 負責記錄管理：

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

只翻譯 `todo` 列出的內容：保留 Markdown、連結、程式碼、檔案與欄位名稱不變，翻譯標題與圖片說明，並使用 3DHeat 檢視器自己的按鈕與面板用語（其 `src/i18n/locales/<lang>/`）。產生的參考頁面與終端機圖片維持英文。在網站上，過時的翻譯會註明並連結到英文頁面；缺少的翻譯會退回英文。標頭的語言選單與首頁依瀏覽器語言自動轉址，都來自 `docs/_includes/`。
