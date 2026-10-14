"""D2 — desvio em relacao ao padrao do proprio funcionario.

A unica dimensao que olha o passado, e e esse o ponto: a C2 mede o que o
contexto individual acrescenta sobre a C1. Dois passos, nesta ordem:

1. `build_baselines` constroi o padrao de cada pessoa na janela de treino — os
   tres primeiros meses, pela D-24, anteriores e disjuntos da janela de
   avaliacao, pela D-17.
2. `score_d2` compara cada evento com o padrao de quem o gerou.

O passo 1 nao pode ver a janela de avaliacao, e o passo 2 nao pode ver o futuro.
As duas recusas estao no codigo, nao no bom senso de quem chama.
"""

from detection.d2.baseline import Baseline, Spread, build_baseline, build_baselines
from detection.d2.scoring import score_d2

__all__ = [
    "Baseline",
    "Spread",
    "build_baseline",
    "build_baselines",
    "score_d2",
]
