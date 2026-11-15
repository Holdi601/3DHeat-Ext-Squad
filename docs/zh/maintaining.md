---
title: 维护这些文档
nav_order: 91
lang: "zh"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# 维护这些文档 {#maintaining-these-docs}

每次发布时的检查清单，确保页面永远不会落后于代码。

1. **重新生成参考页。** `python tools/gen_docs_reference.py` 会根据程序自身的 `--help` 和输出列重写 [命令参考](../cli-reference.md)。`python tools/gen_docs_reference.py --check` 在已提交的页面过时时退出并返回 1。
2. **列出变更内容。** `git log v<VERSION>..HEAD --oneline`，其中 `<VERSION>` 是最近一次发布的版本（发布时的 `VERSION` 文件）。确保每一项新功能、选项和输出列都在某个页面上有位置，并在 [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md) 的 **Docs** 部分中有一行记录。
3. **独立审阅。** 没有编写这些页面的人，阅读 README 和每个有变动的页面，包括图片，共三遍：一遍以从未用过终端的初学者的身份，一遍以八岁孩子的身份，一遍以专家的身份逐项对照 `--help` 检查每个选项。示例只使用虚构的名称和数字。
4. **修正**审阅中发现的所有问题。
5. **翻译。** 每个翻译页面都记录了其所依据的英文页面的哈希值。对英文源文件已变更的页面重新翻译，然后逐种语言审阅：文字清晰、图表标签正确，并且与查看器自身翻译后的界面使用相同的词汇。
6. **运行测试**（`pytest`）。
7. **推送**，且只有在所有者同意之后。

## 翻译：命令 {#translations-the-commands}

本站点已翻译为 3DHeat 查看器支持的 40 种语言：英文位于 `docs/`，其他每种语言位于 `docs/<lang>/`，文件名相同。`tools/docs_i18n.py` 负责相关的记录工作：

```bash
python tools/docs_i18n.py hashes             # 英文有任何变更后：记录每个页面的哈希值
python tools/docs_i18n.py svg-strings        # 图片有任何变更后：需要翻译的标签
python tools/docs_i18n.py status             # 按语言：当前、过时和缺失的页面
python tools/docs_i18n.py todo --lang de     # 需要（重新）翻译的德语页面
python tools/docs_i18n.py svg-build --lang de    # 根据 docs/assets/i18n/svg/de.json 生成德语图片
python tools/docs_i18n.py finish --lang de   # 用英文哈希值标记德语页面
python tools/docs_i18n.py check              # 哈希或标签过时时退出并返回 1
```

只翻译 `todo` 列出的内容：保持 Markdown、链接、代码、文件名和列名不变，翻译标题和图片说明，并使用 3DHeat 查看器自己的词汇来表示其按钮和面板（即其 `src/i18n/locales/<lang>/`）。生成的参考页和终端图片保持英文。在站点上，过时的翻译会提示并链接到英文页面；缺失的翻译会回退为英文。页眉的语言菜单和主页的浏览器语言重定向来自 `docs/_includes/`。
