---
title: "デモの録画"
nav_order: 2
lang: ja
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# デモの録画 {#recording-a-demo}

Squadのデモは、ゲームのクライアントではなく、**サーバー上で** 録画します。

1. サーバーの `Admins.cfg` で、管理者のグループに `demos` の権限を与えます。
2. 試合が始まったら、ゲームのコンソールで `AdminDemoRec <name>` を実行します。管理者は、ゲーム自体でこれを入力しなければなりません。RCONでは受け付けないという報告があります。
3. 試合をプレイし、`AdminDemoStop` を実行します。
4. デモは `<server>/SquadGame/Saved/Demos/<name>.replay` に書き出されます。変換するマシンへ、サーバーからコピーしてください。

`Server.cfg` には `RecordDemos` という設定もあり、既定ではオフです。小さな試合では、1時間あたりおよそ 70 から 80 MB を見込んでください。100人の完全なサーバーでのサイズは、まだ測っていません。

デモには、サーバー上の全員の名前とオンラインIDが入っています。個人データとして扱ってください（[制限、更新、利用条件](limits.md#個人データ)）。

次へ: [デモの変換](converting.md)。
