"""C0 — a linha de base do experimento.

Quatro regras fixas sobre o evento isolado, e e contra ela que as tres
dimensoes sao medidas. Por isso a C0 e a parte do codigo que menos pode mudar:
grupo de controle que alguem ajusta deixa de medir.

A assinatura das funcoes aqui carrega a garantia principal: **nenhuma recebe o
funcionario.** Ela recebe o evento, o catalogo da organizacao e a
configuracao — e o catalogo so e consultado para recurso e faixa de rede, que
sao cadastro, nao historico. Nao ha como a C0 olhar o passado de quem gerou o
evento, porque o passado nao chega nela.
"""

from detection.c0.rules import (
    external_origin,
    off_hours,
    restricted_access,
    score_c0,
)

__all__ = ["external_origin", "off_hours", "restricted_access", "score_c0"]
