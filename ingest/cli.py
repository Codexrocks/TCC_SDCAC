"""Linha de comando da ingestao.

```bash
python -m ingest --origem out/run_001 --destino dados/semente-1
```

Depois disso o executor roda sobre dado gerado, e nao sobre *fixture*:

```bash
python -m runner --dados dados/semente-1 --run-id 1 \
    --treino 2026-01-01:2026-03-31 --avaliacao 2026-04-01:2026-12-31
```

A janela de treino sao os tres primeiros meses da **D-24**, que e tambem o
`EVAL_START_DAY` do gerador — e e por isso que ele tem uma checagem que deriva
os tres meses da data de inicio em vez de conferir a constante contra si mesma.
"""

import argparse
import sys
from pathlib import Path

from ingest.corp import IngestError, converte_run


def monta_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ingest",
        description="Converte o CSV do gerador para o formato do adaptador de arquivo.",
    )
    parser.add_argument(
        "--origem",
        required=True,
        type=Path,
        help="o run_NNN/ que o gerador escreveu, com corp/ dentro",
    )
    parser.add_argument(
        "--destino",
        required=True,
        type=Path,
        help="diretorio de dados do adaptador; corp/ e criado dentro dele",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Converte e devolve o codigo de saida do processo."""
    args = monta_parser().parse_args(argv)
    try:
        contagem = converte_run(args.origem, args.destino)
    except IngestError as erro:
        print(f"ingestao recusada: {erro}", file=sys.stderr)
        return 1

    print(f"{args.origem} -> {args.destino}")
    for nome, quantos in contagem.items():
        print(f"  {nome}: {quantos:,}".replace(",", "."))
    return 0
