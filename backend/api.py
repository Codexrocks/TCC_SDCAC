"""As rotas de leitura — os quatro grupos da D-36, mais saude e configuracoes.

**Somente leitura, e isso nao e provisorio.** Nenhuma rota escreve. Execucao e
disparada pela linha de comando, pela D-35; configuracao editavel, fila de job e
auditoria de consulta entram na v2, e nada da conclusao do artigo depende delas.

**A API serializa, nao calcula.** Faixa, parcela e motivo vem do motor; metrica
vem do avaliador. No dia em que uma rota somar ou mediar, o painel passa a
mostrar numero que o motor nunca produziu, e a tabela do artigo e a tela dizem
coisas diferentes sem que nada reclame.

**Duas proibicoes que vem de decisoes anteriores:**

- **nenhuma rota le o gabarito.** O `ScoreRepository` nao tem metodo para isso, e
  um teste reprova quem acrescentar;
- **nenhuma rota calcula metrica.** `/metrics` devolve o que o avaliador gravou,
  e pagina vazia enquanto ele nao existir — que e resposta, nao falha.

**O repositorio entra por injecao.** As rotas recebem o `ScoreRepository` por
dependencia do FastAPI, e nao importam `storage/`. E o que faz a troca do
adaptador de arquivo pelo de PostgreSQL nao tocar em rota nenhuma.
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.dependencies import repositorio
from backend.schemas import (
    Alerta,
    Configuracao,
    Erro,
    Execucao,
    Metrica,
    MotivoDoRisco,
    NotaDoEvento,
    NotaDoFuncionario,
    Pagina,
    ParcelasDoRisco,
    Saude,
)
from detection.configuration import load_implemented
from detection.ports import ScoreRepository

LIMITE = Annotated[
    int, Query(ge=1, le=200, description="Itens por pagina, no maximo 200")
]
DESLOCAMENTO = Annotated[int, Query(ge=0, description="Quantos itens pular")]
# `Annotated` em vez de valor padrao: `Depends()` como default e o idioma
# antigo do FastAPI, e o `B008` do Ruff reclama dele com razao — valor padrao
# avaliado na definicao da funcao e armadilha em qualquer outro contexto.
REPOSITORIO = Annotated[ScoreRepository, Depends(repositorio)]

router = APIRouter(prefix="/api/v1")

NAO_ENCONTRADO = {status.HTTP_404_NOT_FOUND: {"model": Erro}}


def _parcelas(nota) -> ParcelasDoRisco:
    return ParcelasDoRisco(
        c0=nota.c0,
        d1=nota.d1,
        d2=nota.d2,
        d3_conduct=nota.d3_conduct,
        d3_posture=nota.d3_posture,
    )


def _motivos(nota) -> list[MotivoDoRisco]:
    return [
        MotivoDoRisco(rule=h.rule, points=h.points, reason=h.reason) for h in nota.hits
    ]


def _execucao_ou_404(repo, scoring_run_id: int):
    try:
        return repo.run(scoring_run_id)
    except Exception as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"execucao {scoring_run_id} nao existe",
        ) from erro


# ---------------------------------------------------------------------------
# Saude e configuracoes
# ---------------------------------------------------------------------------


@router.get("/health", response_model=Saude, summary="A API esta de pe?")
def saude(repo: REPOSITORIO) -> Saude:
    """Diz se vale tentar, e quantas execucoes existem para consultar."""
    _, total = repo.list_runs(limit=1, offset=0)
    return Saude(status="ok", adapter=type(repo).__name__, runs=total)


@router.get(
    "/configurations",
    response_model=list[Configuracao],
    summary="Os presets canonicos da ablacao",
)
def configuracoes() -> list[Configuracao]:
    """As configuracoes com parametro, com o hash de cada uma.

    Sai dos presets versionados, e nao do banco: e o painel sabendo o que cada
    execucao ligou sem precisar deduzir do nome.
    """
    return [
        Configuracao(
            name=c.name,
            dimensions=list(c.dimensions),
            config_hash=c.config_hash,
            exploratory=c.exploratory,
        )
        for c in load_implemented()
    ]


# ---------------------------------------------------------------------------
# Execucoes
# ---------------------------------------------------------------------------


@router.get("/runs", response_model=Pagina[Execucao], summary="Execucoes de pontuacao")
def execucoes(
    repo: REPOSITORIO, limit: LIMITE = 50, offset: DESLOCAMENTO = 0
) -> Pagina[Execucao]:
    """Da mais recente para a mais antiga, com semente, commit e hash."""
    registros, total = repo.list_runs(limit=limit, offset=offset)
    return Pagina[Execucao](
        items=[Execucao(**r) for r in registros],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/runs/{scoring_run_id}",
    response_model=Execucao,
    responses=NAO_ENCONTRADO,
    summary="Uma execucao",
)
def execucao(scoring_run_id: int, repo: REPOSITORIO) -> Execucao:
    return Execucao(**_execucao_ou_404(repo, scoring_run_id))


# ---------------------------------------------------------------------------
# Funcionarios
# ---------------------------------------------------------------------------


@router.get(
    "/runs/{scoring_run_id}/employees",
    response_model=Pagina[NotaDoFuncionario],
    responses=NAO_ENCONTRADO,
    summary="A nota mais recente de cada pessoa",
)
def funcionarios(
    scoring_run_id: int,
    repo: REPOSITORIO,
    limit: LIMITE = 50,
    offset: DESLOCAMENTO = 0,
) -> Pagina[NotaDoFuncionario]:
    _execucao_ou_404(repo, scoring_run_id)
    linhas, total = repo.list_employee_scores(
        scoring_run_id, limit=limit, offset=offset
    )
    return Pagina[NotaDoFuncionario](
        items=[
            NotaDoFuncionario(
                employee_id=linha.employee_id,
                event_id=linha.event_id,
                occurred_at=linha.occurred_at,
                configuration=linha.score.configuration,
                parcels=_parcelas(linha.score),
                final_raw=linha.score.final_raw,
                band=linha.score.band.value,
            )
            for linha in linhas
        ],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/runs/{scoring_run_id}/employees/{employee_id}",
    response_model=Pagina[NotaDoEvento],
    responses=NAO_ENCONTRADO,
    summary="O historico de uma pessoa",
)
def historico(
    scoring_run_id: int,
    employee_id: int,
    repo: REPOSITORIO,
    limit: LIMITE = 50,
    offset: DESLOCAMENTO = 0,
) -> Pagina[NotaDoEvento]:
    _execucao_ou_404(repo, scoring_run_id)
    linhas, total = repo.employee_history(
        scoring_run_id, employee_id, limit=limit, offset=offset
    )
    return Pagina[NotaDoEvento](
        items=[
            NotaDoEvento(
                event_id=linha.score.event_id,
                employee_id=linha.employee_id,
                occurred_at=linha.occurred_at,
                event_type=linha.event_type,
                configuration=linha.score.configuration,
                config_hash=linha.score.config_hash,
                parcels=_parcelas(linha.score),
                final_raw=linha.score.final_raw,
                band=linha.score.band.value,
                hits=_motivos(linha.score),
            )
            for linha in linhas
        ],
        total=total,
        limit=limit,
        offset=offset,
    )


# ---------------------------------------------------------------------------
# Eventos e alertas
# ---------------------------------------------------------------------------


FAIXA = Annotated[
    str | None,
    Query(pattern="^(normal|low|medium|high)$", description="Faixa exata"),
]
INICIO = Annotated[datetime | None, Query(description="Inicio, em UTC")]
FIM = Annotated[datetime | None, Query(description="Fim, em UTC")]


@router.get(
    "/runs/{scoring_run_id}/alerts",
    response_model=Pagina[Alerta],
    responses=NAO_ENCONTRADO,
    summary="Alertas, filtraveis por faixa e periodo",
)
def alertas(
    scoring_run_id: int,
    repo: REPOSITORIO,
    band: FAIXA = None,
    since: INICIO = None,
    until: FIM = None,
    limit: LIMITE = 50,
    offset: DESLOCAMENTO = 0,
) -> Pagina[Alerta]:
    _execucao_ou_404(repo, scoring_run_id)
    linhas, total = repo.list_alerts(
        scoring_run_id,
        band=band,
        since=since,
        until=until,
        limit=limit,
        offset=offset,
    )
    return Pagina[Alerta](
        items=[Alerta(**linha) for linha in linhas],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/runs/{scoring_run_id}/events/{event_id}",
    response_model=NotaDoEvento,
    responses=NAO_ENCONTRADO,
    summary="A nota de um evento, decomposta",
)
def evento(scoring_run_id: int, event_id: str, repo: REPOSITORIO) -> NotaDoEvento:
    _execucao_ou_404(repo, scoring_run_id)
    linha = repo.event_score(scoring_run_id, event_id)
    if linha is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"evento {event_id} nao tem nota nesta execucao",
        )
    return NotaDoEvento(
        event_id=linha.score.event_id,
        employee_id=linha.employee_id,
        occurred_at=linha.occurred_at,
        event_type=linha.event_type,
        configuration=linha.score.configuration,
        config_hash=linha.score.config_hash,
        parcels=_parcelas(linha.score),
        final_raw=linha.score.final_raw,
        band=linha.score.band.value,
        hits=_motivos(linha.score),
    )


# ---------------------------------------------------------------------------
# Metricas
# ---------------------------------------------------------------------------


@router.get(
    "/runs/{scoring_run_id}/metrics",
    response_model=Pagina[Metrica],
    responses=NAO_ENCONTRADO,
    summary="O que o avaliador gravou",
)
def metricas(
    scoring_run_id: int,
    repo: REPOSITORIO,
    limit: LIMITE = 50,
    offset: DESLOCAMENTO = 0,
) -> Pagina[Metrica]:
    """Pagina vazia enquanto o avaliador nao existir — e isso e resposta.

    A API **nao calcula** precisao nem revocacao: calcular exigiria o rotulo, e
    o usuario da aplicacao nao tem permissao de conectar no `ground_truth`.
    """
    _execucao_ou_404(repo, scoring_run_id)
    linhas, total = repo.list_metrics(scoring_run_id, limit=limit, offset=offset)
    return Pagina[Metrica](
        items=[Metrica(**linha) for linha in linhas],
        total=total,
        limit=limit,
        offset=offset,
    )
