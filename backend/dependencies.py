"""De onde a API tira o repositorio, e como se troca isso.

A rota pede `Depends(repositorio)` e recebe algo que cumpre
`detection.ports.ScoreRepository`. Quem decide **qual** adaptador e esta funcao,
e trocar o de arquivo pelo de PostgreSQL mexe aqui e em nenhuma rota.

**O caminho vem do ambiente, e isso e deliberado.** `detection/` nao le ambiente
— e tem teste que reprova —, mas a API e adaptador: ela precisa saber onde estao
os dados, e passar isso por argumento de rota seria deixar o cliente escolher
qual diretorio o servidor abre. Caminho vindo da requisicao e leitura de arquivo
arbitrario com outro nome.
"""

import os
from functools import lru_cache
from pathlib import Path

from storage.leitura import ArquivoRepository

# Onde o executor gravou. Uma variavel de ambiente, com um padrao obvio: o
# diretorio `dados/` ao lado do projeto.
VARIAVEL = "SDCAC_DADOS"
PADRAO = "dados"


@lru_cache(maxsize=1)
def _repositorio(raiz: str) -> ArquivoRepository:
    return ArquivoRepository(Path(raiz))


def repositorio() -> ArquivoRepository:
    """O repositorio que serve esta instancia da API."""
    return _repositorio(os.environ.get(VARIAVEL, PADRAO))


def limpa_cache() -> None:
    """Esquece o repositorio em memoria.

    Serve ao teste, que troca o diretorio entre casos. Em producao o caminho nao
    muda durante a execucao do processo.
    """
    _repositorio.cache_clear()
