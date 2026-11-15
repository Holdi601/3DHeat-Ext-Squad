---
title: "このドキュメントの保守"
nav_order: 91
lang: "ja"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# このドキュメントの保守 {#maintaining-these-docs}

リリースごとのチェックリストです。ページがコードに追いつかなくならないようにします。

1. **リファレンスを再生成。** `python tools/gen_docs_reference.py` は、プログラム自身の `--help` と出力の列から [コマンドリファレンス](../cli-reference.md) を書き直します。`python tools/gen_docs_reference.py --check` は、コミットされたページが古い場合に 1 で終了します。
2. **変更点を一覧にする。** `git log v<VERSION>..HEAD --oneline`。ここで `<VERSION>` は、最後にリリースされたバージョンです（リリース時の `VERSION` ファイル）。新しい機能、オプション、出力の列には、どれもページでの居場所を与え、[`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md) の **Docs** の節に行を加えてください。
3. **独立したレビュー。** ページを書いていない人が、READMEと変更されたすべてのページを、図も含めて、三回読みます。ターミナルを使ったことのない初心者として、8歳の子どもとして、そして `--help` と照らし合わせてすべてのオプションを確かめる専門家として。例では、作った名前と数字だけを使います。
4. **レビューで見つかったものをすべて直す。**
5. **翻訳。** 翻訳されたページは、それを作った英語ページのハッシュを記録しています。英語の元が変わったページは、もう一度翻訳します。そのうえで各言語をレビューします: 明確な文章、正しい図のラベル、ビューア自身の翻訳済みインターフェースと同じ言葉。
6. **テストを実行**（`pytest`）。
7. **プッシュ**は、オーナーの承認を得てから。

## 翻訳: コマンド {#translations-the-commands}

サイトは、3DHeatビューアの40言語に翻訳されています。英語は `docs/` に、その他の言語はそれぞれ `docs/<lang>/` に、同じファイル名で入ります。`tools/docs_i18n.py` が管理を行います:

```bash
python tools/docs_i18n.py hashes             # 英語の変更のあとに: 各ページのハッシュを記録
python tools/docs_i18n.py svg-strings        # 図の変更のあとに: 翻訳するラベル
python tools/docs_i18n.py status             # 言語ごと: 最新、古い、欠けているページ
python tools/docs_i18n.py todo --lang de     # ドイツ語で翻訳（再翻訳）するページ
python tools/docs_i18n.py svg-build --lang de    # docs/assets/i18n/svg/de.json からドイツ語の図
python tools/docs_i18n.py finish --lang de   # ドイツ語のページに英語のハッシュを押す
python tools/docs_i18n.py check              # ハッシュやラベルが古いと 1 で終了
```

`todo` が挙げたものだけを翻訳します。Markdown、リンク、コード、ファイル名、列名はそのままにします。タイトルと図の説明は翻訳します。ボタンやパネルの名前には、3DHeatビューア自身の言葉を使います（`src/i18n/locales/<lang>/`）。生成されたリファレンスのページと、ターミナルの画像は英語のままにします。サイト上では、古い翻訳には、その旨と英語のページへのリンクが出ます。欠けているものは英語に戻ります。ヘッダーの言語メニューと、ホームページのブラウザー言語へのリダイレクトは、`docs/_includes/` から来ます。
