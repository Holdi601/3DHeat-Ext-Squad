---
title: Manutenção destas páginas
nav_order: 91
lang: "pt"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Manutenção destas páginas {#maintaining-these-docs}

Uma lista de verificação para cada versão, para que as páginas nunca fiquem para trás do código.

1. **Regenerar a referência.** `python tools/gen_docs_reference.py` reescreve
   [Referência de comandos](../cli-reference.md) a partir do próprio `--help` do programa e das colunas de saída.
   `python tools/gen_docs_reference.py --check` sai com código 1 quando a página commitada está desatualizada.
2. **Listar o que mudou.** `git log v<VERSÃO>..HEAD --oneline`, onde
   `<VERSÃO>` é a última versão lançada (o arquivo `VERSION` no lançamento). Dê a cada nova função, opção e coluna de saída um lugar em uma página, e uma linha na seção **Docs** do [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Revisão independente.** Alguém que não escreveu as páginas lê o README e cada página alterada, as imagens inclusive, três vezes: como um iniciante que nunca usou um terminal, como uma criança de 8 anos, e como um especialista que confere cada opção com o `--help`. Os exemplos usam apenas nomes e números inventados.
4. **Corrigir** tudo o que a revisão encontrar.
5. **Traduções.** Cada página traduzida registra o hash da página em inglês a partir da qual foi feita. Traduza de novo as páginas cuja fonte em inglês mudou, depois revise cada idioma: texto claro, rótulos corretos nos diagramas, as mesmas palavras da interface traduzida do visualizador 3DHeat.
6. **Rodar os testes** (`pytest`).
7. **Enviar** somente depois do aval do responsável.

## Traduções: os comandos {#translations-the-commands}

O site é traduzido para os 40 idiomas do visualizador 3DHeat: o inglês em `docs/`, cada outro idioma em `docs/<idioma>/` com os mesmos nomes de arquivo. `tools/docs_i18n.py` faz a contabilidade:

```bash
python tools/docs_i18n.py hashes             # após qualquer mudança em inglês: registra o hash de cada página
python tools/docs_i18n.py svg-strings        # após qualquer mudança em imagem: os rótulos a traduzir
python tools/docs_i18n.py status             # por idioma: páginas atuais, desatualizadas, faltando
python tools/docs_i18n.py todo --lang de     # as páginas em alemão a (re)traduzir
python tools/docs_i18n.py svg-build --lang de    # as imagens em alemão a partir de docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # marca as páginas em alemão com o hash do inglês
python tools/docs_i18n.py check              # sai com código 1 quando hashes ou rótulos estão desatualizados
```

Traduza apenas o que `todo` lista: mantenha Markdown, links, código, nomes de arquivo e de colunas como estão,
traduza os títulos e as descrições das imagens, e use as palavras do próprio visualizador 3DHeat para seus botões
e painéis (em `src/i18n/locales/<idioma>/`). As páginas de referência geradas e as imagens de terminal continuam
em inglês. No site, uma tradução desatualizada avisa e aponta para a página em inglês; uma página sem tradução
volta ao inglês. O menu de idiomas do cabeçalho e o redirecionamento da página inicial pelo idioma do navegador
vêm de `docs/_includes/`.
