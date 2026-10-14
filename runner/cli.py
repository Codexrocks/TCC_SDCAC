"""Linha de comando do executor.

```bash
python -m runner --dados dados/semente-1 --run-id 1 \
    --treino 2026-01-01:2026-03-31 --avaliacao 2026-04-01:2026-12-31
```

**Por que linha de comando, e nao rota HTTP.** A **D-35**: pontuar milhoes de
eventos dentro de uma requisicao nao existe, e a fila de job entra na v2, quando
a interface passa a disparar execucao. Na v1 quem executa e quem tem acesso ao
terminal, e isso e suficiente para o experimento do artigo.

**O que esta CLI nao faz:** nao calcula metrica. Precisao e revocacao saem do
avaliador, que e o unico que enxerga o gabarito — e o usuario da aplicacao nao
tem permissao de conectar no `ground_truth`.
"""

import argparse
import sys
from datetime import UTC, date, datetime
from pathlib import Path

from detection.configuration import ConfigurationError, load_canonical, load_implemented
from runner.experiment import run_experiment
from storage.arquivos import ArquivoStorage, StorageError


def _par_de_datas(texto: str) -> tuple[date, date]:
    try:
        inicio, fim = texto.split(":", 1)
        return date.fromisoformat(inicio), date.fromisoformat(fim)
    except ValueError as erro:
        raise argparse.ArgumentTypeError(
            f"{texto!r} nao e um par de datas AAAA-MM-DD:AAAA-MM-DD"
        ) from erro


def monta_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="runner",
        description="Executa o experimento: constroi os padroes e pontua os eventos.",
    )
    parser.add_argument(
        "--dados",
        required=True,
        type=Path,
        help="diretorio com corp/ e sdcac/, no formato do adaptador de arquivo",
    )
    parser.add_argument("--run-id", required=True, type=int, help="a semente a pontuar")
    parser.add_argument(
        "--treino",
        required=True,
        type=_par_de_datas,
        help="janela de treino do passo 1, inclusive nas duas pontas",
    )
    parser.add_argument(
        "--avaliacao",
        required=True,
        type=_par_de_datas,
        help="janela de avaliacao do passo 2, inclusive no inicio",
    )
    parser.add_argument(
        "--configuracoes",
        nargs="+",
        default=None,
        metavar="C",
        help="quais configuracoes rodar; por omissao, todas as que tem parametro",
    )
    parser.add_argument(
        "--limiar",
        type=float,
        default=None,
        help="corte de alerta; por omissao, o teto da faixa normal da configuracao",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Roda o experimento e devolve o codigo de saida do processo."""
    args = monta_parser().parse_args(argv)

    try:
        if args.configuracoes:
            configs = tuple(load_canonical(nome) for nome in args.configuracoes)
        else:
            configs = load_implemented()
    except ConfigurationError as erro:
        print(f"configuracao: {erro}", file=sys.stderr)
        return 2

    if not configs:
        print("nenhuma configuracao com parametro para rodar", file=sys.stderr)
        return 2

    treino_inicio, treino_fim = args.treino
    avaliacao_inicio, avaliacao_fim = args.avaliacao
    limiar = args.limiar
    if limiar is None:
        limiar = float(configs[0].parameters.get("bands", {}).get("normal_max", 20))

    storage = ArquivoStorage(args.dados)
    try:
        resumos = run_experiment(
            storage,
            run_id=args.run_id,
            configs=configs,
            training=(treino_inicio, treino_fim),
            evaluation=(
                datetime.combine(avaliacao_inicio, datetime.min.time(), tzinfo=UTC),
                datetime.combine(avaliacao_fim, datetime.max.time(), tzinfo=UTC),
            ),
            threshold=limiar,
        )
    except (StorageError, ValueError) as erro:
        print(f"execucao interrompida: {erro}", file=sys.stderr)
        return 1

    largura = max(len(r.configuration) for r in resumos)
    print(f"semente {args.run_id} · limiar de alerta {limiar:g}")
    for resumo in resumos:
        print(
            f"  {resumo.configuration:<{largura}}  execucao {resumo.scoring_run_id}"
            f"  {resumo.scored} eventos  {resumo.alerts} alertas"
            f"  hash {resumo.config_hash[:12]}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
