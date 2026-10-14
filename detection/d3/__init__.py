"""D3 — exposicao acumulada e postura de seguranca.

A contribuicao original do trabalho, e a unica dimensao que reporta **duas
parcelas separadas**, pela D-25 e pela D-30: conduta e postura nao se somam num
numero so, porque o peso relativo entre as duas nao teria como ser justificado.

Duas recusas moram aqui, e as duas sao decisoes virando codigo:

- a janela de exposicao **nao aceita** o evento atual, pela D-18 — dupla
  contagem nao e aviso, e erro;
- o retrato de postura **nao aceita** data diferente do dia do evento, porque
  ler o estado final e a falha da D-17 por outro caminho.
"""

from detection.d3.posture import build_posture
from detection.d3.scoring import (
    DESFECHOS_DE_PHISHING,
    Posture,
    PriorScore,
    ThirdDimension,
    score_conduct,
    score_d3,
    score_posture,
)

__all__ = [
    "DESFECHOS_DE_PHISHING",
    "Posture",
    "PriorScore",
    "ThirdDimension",
    "build_posture",
    "score_conduct",
    "score_d3",
    "score_posture",
]
