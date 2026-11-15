---
title: "デモの変換"
nav_order: 3
lang: "ja"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# デモの変換 {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          同じ。インストールせずに実行
```

## 手順 {#step-by-step}

コマンドラインは初めてですか？ まず [始める前に](before-you-start.md) を読んでください。

1. 一度だけインストール: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`、そのフォルダーでターミナルを開き、`python -m pip install -e .` を実行します（Python 3.10 以降。pyarrowとnumpyも入ります）。
2. `.replay` ファイルをフォルダーに入れるか、一つずつ名前で指定します。
3. `heat3d-squad-demo <folder> -o out` を実行します。
4. デモごとに1行ずつ表示されます。その行には、レイヤー、プレイヤー数と行数、そしてテーブルの書き出し先が示されます。各デモは `out/<map>/` の中に、4つの独立したファイルとして書き出されます（`.3dheat` コンテナではありません）。`.parquet` を3DHeatビューアで読み込んでください。

![合成デモでの実行](../assets/img/run.svg)

この絵は、テストが作ったデモ（`tests/test_stream.py`）での実行を示しています。実際の試合ではありません。

## オプション {#options}

| オプション | 既定値 | 働き |
|---|---|---|
| `demos`（一つ以上） | - | `.replay` ファイル、またはそれを入れたフォルダー |
| `-o`, `--out` | 必須 | 書き出し先のフォルダー。各デモは `<out>/<map>/` に入ります |
| `--flat` | オフ | `<map>/` フォルダーを作らず、そのフォルダーに直接書き出します |
| `--json` | オフ | デモごとに1行のJSONを標準出力に表示します（このコマンドを呼び出すプログラム向け）: `demo`、`ok`、`parquet`、`match`、`sidecars`、`lost`、`rows`、`players`、`layer`、`recorded_unix`。失敗したデモは、`demo`、`ok: false`、`error` を表示します |
| `--version` | - | バージョンを表示して終了します |

プログラムが表示する通りのすべてのオプション: [コマンドリファレンス](../cli-reference.md)。

マップのフォルダー名は、デモが指定しているレベルのパスから取ったマップ名です（`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` なら `<Map>`）。

終了ステータス: すべてのデモを変換できたら 0。一つでも失敗したら 1（ほかは書き出されます）。`.replay` ファイルが見つからなかった場合も 1。

## 出力されるもの {#what-comes-out}

| ファイル | 中身 |
|---|---|
| `<demo>.parquet` | テーブル：位置と出来事、1行ずつ（[テーブル](output-table.md)） |
| `<demo>.match.json` | マッチドキュメント（[マッチドキュメント](output-match.md)） |
| `<demo>.entities.parquet` | サイドカー：すべてのプロパティ更新と遠隔呼び出し、そのままの形 |
| `<demo>.packets.parquet` | サイドカー：ファイルのチャンクと、読めなかったものすべて、そのままの形 |

テーブルとマッチドキュメントは、3DHeat CS2ツールが書き出すものと同じペアです。ビューアはテーブルを直接開き、フォルダー全体を読み込むときはサイドカーを除きます。

## 例 {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # フォルダー内のすべてのデモ
heat3d-squad-demo one.replay two.replay -o out --flat  # out/ に直接
heat3d-squad-demo D:\SquadDemos -o out --json          # デモごとに1行のJSON
```

`D:\SquadDemos` はDドライブの例のフォルダーです。自分のものを使ってください。
