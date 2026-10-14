"""C0 — a linha de base do experimento.

Quatro regras fixas sobre o evento isolado, e e contra ela que as tres
dimensoes sao medidas. Por isso a C0 e a parte do codigo que menos pode mudar:
grupo de controle que alguem ajusta deixa de medir.

A assinatura das funcoes carrega a garantia: **nenhuma recebe o funcionario.**
Elas recebem o evento, o catalogo — recurso e faixa de rede, que sao cadastro —
e a configuracao. O padrao individual nao chega aqui, e e isso que a **D-42**
chama de "sem parametro aprendido".

A excecao e a janela de falhas, que recebe eventos recentes da mesma conta. Ela
nao estima nada: mesmo limiar para todos, memoria de dois minutos, e recusa
evento de outra conta ou do futuro.
"""

from detection.c0.rules import (
    brute_force,
    external_origin,
    off_hours,
    restricted_access,
    score_c0,
)

__all__ = [
    "brute_force",
    "external_origin",
    "off_hours",
    "restricted_access",
    "score_c0",
]
