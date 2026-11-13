"""Grava as figuras da Secao 4 a partir do agregado das sementes.

    python -m evaluator.figuras_cli
    python -m evaluator.figuras_cli --agregado results/agregado.json --saida results/figuras

O SVG e o que se versiona: e texto, e o diff mostra o que mudou. O PNG que entra
no documento sai dele, e a conversao nao e feita aqui -- esta descrita em
`results/figuras/README.md`, porque depende de ferramenta de fora.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluator.figuras import figura_fpr


def monta_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m evaluator.figuras_cli",
        description="Grava as figuras da Secao 4 em SVG.",
    )
    parser.add_argument(
        "--agregado",
        type=Path,
        default=Path("results/agregado.json"),
        help="o agregado das sementes (por omissao, results/agregado.json)",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("results/figuras"),
        help="diretorio das figuras (por omissao, results/figuras)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Grava os SVG e devolve o codigo de saida do processo."""
    args = monta_parser().parse_args(argv)
    if not args.agregado.exists():
        print(f"agregado nao encontrado: {args.agregado}")
        return 1

    agregado = json.loads(args.agregado.read_text(encoding="utf-8"))
    args.saida.mkdir(parents=True, exist_ok=True)

    destino = args.saida / "fpr-por-revocacao.svg"
    destino.write_text(figura_fpr(agregado), encoding="utf-8")
    print(f"gravado: {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
