"""Os corpos que a API devolve — e a forma do contrato que o painel consome.

**Uma classe por recurso, e nenhuma delas e um modelo de dominio.** `RiskScore`
mora em `detection/`, e nao sabe o que e JSON; estes aqui existem para dizer ao
painel exatamente o que esperar, e para que o OpenAPI gerado seja util em vez de
`object`.

**As cinco parcelas, sempre, e nulo e diferente de zero.** `None` significa
"dimensao nao avaliada nesta configuracao"; `0` significa "avaliada e sem
risco". Devolver zero nos dois casos faria uma execucao da C1 ficar
indistinguivel de uma da C3 em que nada disparou — e e justamente a diferenca
entre as linhas da tabela de ablacao.

**Envelope de pagina em toda lista.** `items`, `total`, `limit` e `offset`. O
total e o que permite ao painel escrever "1 a 50 de 12.431" sem puxar o resto.

**Envelope de erro unico, e ele nao vaza nada.** `code`, `message`, `detail`.
Nenhuma mensagem carrega SQL, caminho de arquivo ou rastreio de pilha: o
repositorio e publico e a API vai rodar na maquina de quem analisa, mas isso nao
e motivo para contar como ela e feita por dentro.

**Todo exemplo deste arquivo saiu de uma execucao real, e nenhum foi inventado.**
Sao os valores da execucao 4 -- preset C3, semente 1 --, pontuada pelo runner e
lida pela propria API. Exemplo serve para o painel ser escrito antes de haver
dado de verdade, e exemplo inventado ensinaria a tela a esperar um formato que a
API nao devolve. A `Metrica` e a unica sem exemplo, porque nenhum avaliador
gravou metrica ainda: ali a ausencia e o recado.

Repare no `c0` do exemplo: ele e `null` na C3, e nao zero. Quem desenhar a tela
precisa distinguir os dois -- barra zerada no lugar de "nao avaliada" descreve
errado a tabela de ablacao, e a `docs/usabilidade.md` pede rotulo em texto junto
da cor justamente para casos assim.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Erro(BaseModel):
    """O corpo de toda resposta que nao e 2xx."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "code": "nao_encontrado",
                    "message": "execucao 999 nao existe",
                    "detail": None,
                }
            ]
        }
    )

    code: str = Field(
        description="Identificador estavel do erro, para o cliente tratar"
    )
    message: str = Field(description="Uma frase em portugues, para quem le")
    detail: str | None = Field(
        default=None, description="Contexto adicional, quando houver"
    )


class Pagina[T](BaseModel):
    """Envelope de toda lista."""

    items: list[T]
    total: int = Field(description="Quantos itens existem no total, nao nesta pagina")
    limit: int
    offset: int


class ParcelasDoRisco(BaseModel):
    """As cinco parcelas, como o motor as produziu.

    Espelha as colunas de `sdcac.risk_scores`. Nulo e "nao avaliada".
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "c0": None,
                    "d1": 0.0,
                    "d2": 0.0,
                    "d3_conduct": 34.0,
                    "d3_posture": 0.0,
                }
            ]
        }
    )

    c0: float | None = Field(
        default=None, description="Regras fixas. Nao-nulo so na C0"
    )
    d1: float | None = Field(default=None, description="Risco do evento individual")
    d2: float | None = Field(default=None, description="Desvio do padrao da pessoa")
    d3_conduct: float | None = Field(
        default=None, description="Exposicao acumulada — o que a pessoa fez"
    )
    d3_posture: float | None = Field(
        default=None,
        description="Postura de seguranca — o estado da conta e do equipamento",
    )


class MotivoDoRisco(BaseModel):
    """Uma regra que disparou, com o motivo em texto.

    Nao e enfeite: a decomponibilidade que a secao 3.9 do artigo promete comeca
    aqui. Score sem motivo obriga quem analisa a adivinhar o que o numero quis
    dizer.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "rule": "accumulated_exposure",
                    "points": 34,
                    "reason": "17 eventos nos ultimos 14 dias somam 103 pontos com decaimento, contra referencia de 300",
                }
            ]
        }
    )

    rule: str
    points: int
    reason: str


class NotaDoEvento(BaseModel):
    """A nota de um evento, decomposta."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "event_id": "ap-8-2-5",
                    "employee_id": 8,
                    "occurred_at": "2026-04-03T13:30:00Z",
                    "event_type": "FILE_ACCESS",
                    "configuration": "C3",
                    "config_hash": "7c224783ac832c1149b05f4a16a93194287e6c84b2a9b3ab9a926a6b93b9f855",
                    "parcels": {
                        "c0": None,
                        "d1": 0.0,
                        "d2": 0.0,
                        "d3_conduct": 34.0,
                        "d3_posture": 0.0,
                    },
                    "final_raw": 34.0,
                    "band": "low",
                    "hits": [
                        {
                            "rule": "accumulated_exposure",
                            "points": 34,
                            "reason": "17 eventos nos ultimos 14 dias somam 103 pontos com decaimento, contra referencia de 300",
                        }
                    ],
                }
            ]
        }
    )

    event_id: str
    employee_id: int
    occurred_at: datetime = Field(description="Sempre em UTC, com fuso explicito")
    event_type: str
    configuration: str
    config_hash: str = Field(
        description="O hash da configuracao que produziu esta nota (D-34)"
    )
    parcels: ParcelasDoRisco
    final_raw: float = Field(
        description="A nota bruta, sem teto. A faixa e para a tela; a avaliacao usa esta"
    )
    band: str
    hits: list[MotivoDoRisco]


class NotaDoFuncionario(BaseModel):
    """A nota mais recente de uma pessoa naquela execucao."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "employee_id": 8,
                    "event_id": "ap-8-2-5",
                    "occurred_at": "2026-04-03T13:30:00Z",
                    "configuration": "C3",
                    "parcels": {
                        "c0": None,
                        "d1": 0.0,
                        "d2": 0.0,
                        "d3_conduct": 34.0,
                        "d3_posture": 0.0,
                    },
                    "final_raw": 34.0,
                    "band": "low",
                }
            ]
        }
    )

    employee_id: int
    event_id: str
    occurred_at: datetime
    configuration: str
    parcels: ParcelasDoRisco
    final_raw: float
    band: str


class Execucao(BaseModel):
    """Uma execucao de pontuacao, como ficou registrada."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "scoring_run_id": 4,
                    "run_id": 1,
                    "config_name": "C3",
                    "config_hash": "7c224783ac832c1149b05f4a16a93194287e6c84b2a9b3ab9a926a6b93b9f855",
                    "code_sha": "6e578b2ea182725e23f605c41efab217e9707427",
                    "weights_version": "presets-v1",
                    "exploratory": False,
                    "status": "done",
                }
            ]
        }
    )

    scoring_run_id: int
    run_id: int = Field(description="A semente do gerador que foi pontuada")
    config_name: str
    config_hash: str
    code_sha: str
    weights_version: str
    exploratory: bool = Field(
        description="Verdadeiro quando a configuracao nao e um preset canonico. "
        "Resultado exploratorio nao vai ao artigo (D-33)"
    )
    status: str


class Configuracao(BaseModel):
    """Um dos presets canonicos, para o painel saber o que cada execucao ligou."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "C3",
                    "dimensions": ["d1", "d2", "d3"],
                    "config_hash": "7c224783ac832c1149b05f4a16a93194287e6c84b2a9b3ab9a926a6b93b9f855",
                    "exploratory": False,
                }
            ]
        }
    )

    name: str
    dimensions: list[str]
    config_hash: str
    exploratory: bool


class Alerta(BaseModel):
    """Um alerta levantado, por evento ou por pessoa numa janela (D-12)."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "band": "low",
                    "threshold": 20.0,
                    "raised_at": "2026-04-03T13:30:00Z",
                    "event_id": "ap-8-2-5",
                    "employee_id": None,
                    "window_start": None,
                    "window_end": None,
                }
            ]
        }
    )

    band: str
    threshold: float = Field(
        description="O corte que o levantou. Sem ele, 'quantos alertas' nao tem resposta"
    )
    raised_at: datetime
    event_id: str | None = None
    employee_id: int | None = None
    window_start: datetime | None = None
    window_end: datetime | None = None


class Metrica(BaseModel):
    """O que o avaliador gravou. A API nao calcula metrica."""

    # Sem exemplo, e de proposito: nenhum avaliador gravou metrica ainda, e
    # portanto nao existe valor real para mostrar aqui. Inventar um recall
    # plausivel seria publicar numero estimado como se fosse medido.
    unit: str = Field(description="event, episode ou user_day (D-12)")
    threshold: float
    recall: float | None = None
    false_positive_rate: float | None = None
    detection_delay_days: float | None = None
    positives: int | None = None
    negatives: int | None = None


class Saude(BaseModel):
    """Resposta de `/health`, para o painel saber se vale tentar."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"status": "ok", "adapter": "ArquivoRepository", "runs": 4}]
        }
    )

    status: str
    adapter: str = Field(description="Qual adaptador esta servindo os dados")
    runs: int = Field(description="Quantas execucoes de pontuacao existem")
