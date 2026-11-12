"""Linha de comando do agregado.

```bash
python -m evaluator.agregado_cli results/semente-* --saida results/
```

Grava `agregado.json`, que e o dado, e `agregado.md`, que e a tabela pronta
para a Secao 4 do artigo. Sem `--saida`, imprime a tabela e nao grava nada.

Esta separado de `agregado.py` para que o `print` fique no arquivo que a regra
T201 do Ruff isenta por ser interface, e o modulo da estatistica siga sem
isencao nenhuma.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evaluator.agregado import AgregadoError, agrega_diretorios
from evaluator.agregado_md import escreve_markdown


def monta_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m evaluator.agregado_cli",
        description=("Agrega sementes ja avaliadas e aplica Wilcoxon pareado exato."),
    )
    parser.add_argument(
        "sementes",
        nargs="+",
        type=Path,
        help="os diretorios de semente, cada um com um metricas.json",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        help="onde gravar agregado.json e agregado.md; sem isso, so imprime",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Agrega e devolve o codigo de saida do processo."""
    args = monta_parser().parse_args(argv)
    try:
        resultado = agrega_diretorios(args.sementes)
    except AgregadoError as erro:
        print(f"agregacao recusada: {erro}", file=sys.stderr)
        return 1

    texto = escreve_markdown(resultado)
    if args.saida is None:
        print(texto)
        return 0

    args.saida.mkdir(parents=True, exist_ok=True)
    (args.saida / "agregado.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (args.saida / "agregado.md").write_text(texto, encoding="utf-8")
    print(f"{resultado['sementes']} sementes agregadas em {args.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
