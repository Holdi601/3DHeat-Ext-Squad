---
title: Converter demos
nav_order: 3
lang: pt
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Converter demos {#converting-demos}

```text
heat3d-squad-demo <demos ou pastas> -o <pasta> [--flat] [--json]
python -m heat3d_ext_squad ...          o mesmo, sem instalar
```

## Passo a passo {#step-by-step}

Nunca usou a linha de comando? Leia primeiro [Antes de começar](before-you-start.md).

1. Instale uma vez: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   abra um terminal nessa pasta e execute `python -m pip install -e .`
   (Python 3.10 ou mais recente; ele instala pyarrow e numpy).
2. Coloque os arquivos `.replay` em uma pasta, ou indique-os um por um.
3. Execute `heat3d-squad-demo <pasta> -o out`.
4. Você deve ver uma linha por demo: a sua camada, os jogadores e as linhas, e para onde
   foi a tabela. Cada demo vira quatro arquivos soltos em `out/<mapa>/` (não um
   contêiner `.3dheat`); carregue o `.parquet` no visualizador 3DHeat.

![Uma execução em uma demo sintética](../assets/img/run.svg)

A imagem mostra uma execução em uma demo que os testes criam (`tests/test_stream.py`),
não uma partida real.

## Opções {#options}

| Opção | Padrão | O que faz |
|---|---|---|
| `demos` (uma ou mais) | - | arquivos `.replay`, ou pastas que os contenham |
| `-o`, `--out` | obrigatória | a pasta onde gravar; cada demo vai para `<out>/<mapa>/` |
| `--flat` | desligada | grava direto na pasta, sem a pasta `<mapa>/` |
| `--json` | desligada | imprime uma linha de JSON por demo na saída padrão (para programas que chamam o comando): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; uma demo que falhou imprime `demo`, `ok: false` e `error` no lugar |
| `--version` | - | mostra a versão e para |

Todas as opções, como o programa as mostra: [Referência de comandos](../cli-reference.md).

A pasta do mapa é o nome do mapa tirado do caminho do nível que a demo indica
(`/Game/Maps/<Mapa>/Gameplay_Layers/<Camada>` gera `<Mapa>`).

Código de saída: 0 quando todas as demos foram convertidas; 1 quando alguma falhou
(as outras são gravadas mesmo assim) ou quando nenhum arquivo `.replay` foi encontrado.

## O que sai {#what-comes-out}

| Arquivo | O que contém |
|---|---|
| `<demo>.parquet` | a tabela: posições e eventos, uma linha cada ([A tabela](output-table.md)) |
| `<demo>.match.json` | o documento da partida ([O documento da partida](output-match.md)) |
| `<demo>.entities.parquet` | arquivo auxiliar: cada atualização de propriedade e cada chamada remota, inteiras |
| `<demo>.packets.parquet` | arquivo auxiliar: os blocos do arquivo e tudo o que não foi lido, inteiro |

A tabela e o documento da partida são o mesmo par que a ferramenta CS2 do 3DHeat grava.
O visualizador abre a tabela diretamente e deixa os arquivos auxiliares de fora quando
uma pasta inteira é carregada.

## Exemplos {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # todas as demos de uma pasta
heat3d-squad-demo one.replay two.replay -o out --flat  # direto em out/
heat3d-squad-demo D:\SquadDemos -o out --json          # uma linha de JSON por demo
```

`D:\SquadDemos` é uma pasta de exemplo no drive D: use a sua.
