"""Linha de comando do avaliador.

```bash
python -m evaluator --dados dados/semente-1 --gerado out/run_001 --run-id 1 \
    --limiar 20 --saida results/semente-1
```

Grava dois arquivos em `--saida`: o `metricas.json`, que e o dado, e o
`relatorio.md`, que e a leitura dele. O `.json` e o que a Secao 4 do artigo
cita; o `.md` existe para conferir sem abrir JSON.

**Por omissao avalia a ultima execucao concluida de cada configuracao.** Uma
configuracao reexecutada tem varias execucoes com o mesmo nome, e avaliar a
primeira que aparece seria avaliar o resultado antigo sem nada acusar.
"""

import argparse
import json
import sys
from pathlib import Path

from evaluator.metrics import EvaluatorError, avalia
from evaluator.relatorio import escreve_markdown


def execucoes_concluidas(dados: Path, run_id: int) -> dict[str, int]:
    """O `scoring_run_id` mais recente e concluido de cada configuracao."""
    caminho = dados / "sdcac" / "execucoes.json"
    if not caminho.exists():
        raise EvaluatorError(f"{caminho} nao existe: nada foi executado ainda")
    registros = json.loads(caminho.read_text(encoding="utf-8"))
    escolhidas: dict[str, int] = {}
    for registro in registros:
        if registro.get("run_id") != run_id or registro.get("status") != "done":
            continue
        nome = registro.get("config_name") or registro.get("config")
        atual = escolhidas.get(nome)
        if atual is None or registro["scoring_run_id"] > atual:
            escolhidas[nome] = registro["scoring_run_id"]
    if not escolhidas:
        raise EvaluatorError(
            f"nenhuma execucao concluida da semente {run_id}. Execucao com "
            "status 'running' ficou pela metade e nao se avalia"
        )
    return dict(sorted(escolhidas.items()))


def monta_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evaluator",
        description="Compara as notas com o gabarito e calcula as metricas da D-03.",
    )
    parser.add_argument(
        "--dados", required=True, type=Path, help="diretorio com sdcac/"
    )
    parser.add_argument(
        "--gerado",
        required=True,
        type=Path,
        help="run_NNN/ do gerador, com ground_truth/",
    )
    parser.add_argument("--run-id", required=True, type=int, help="a semente avaliada")
    parser.add_argument(
        "--limiar",
        required=True,
        type=float,
        help="o corte de alerta usado na execucao, para a matriz de confusao",
    )
    parser.add_argument("--saida", required=True, type=Path, help="onde gravar")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Avalia e devolve o codigo de saida do processo."""
    args = monta_parser().parse_args(argv)
    try:
        execucoes = execucoes_concluidas(args.dados, args.run_id)
        relatorio = avalia(args.dados, args.gerado, args.run_id, execucoes, args.limiar)
    except EvaluatorError as erro:
        print(f"avaliacao recusada: {erro}", file=sys.stderr)
        return 1

    args.saida.mkdir(parents=True, exist_ok=True)
    (args.saida / "metricas.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (args.saida / "relatorio.md").write_text(
        escreve_markdown(relatorio), encoding="utf-8"
    )
    print(f"semente {args.run_id} - {len(execucoes)} configuracoes avaliadas")
    for nome, dados_config in relatorio["configuracoes"].items():
        ev = dados_config["por_evento"]
        print(
            f"  {nome}  revocacao {ev['revocacao']:.3f}  FPR {ev['fpr']:.4f}  "
            f"precisao {ev['precisao']:.4f}"
        )
    print(f"gravado em {args.saida}")
    return 0
