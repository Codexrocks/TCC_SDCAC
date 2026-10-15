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
"""

from datetime import datetime

from pydantic import BaseModel, Field


class Erro(BaseModel):
    """O corpo de toda resposta que nao e 2xx."""

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

    rule: str
    points: int
    reason: str


class NotaDoEvento(BaseModel):
    """A nota de um evento, decomposta."""

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

    employee_id: int
    event_id: str
    occurred_at: datetime
    configuration: str
    parcels: ParcelasDoRisco
    final_raw: float
    band: str


class Execucao(BaseModel):
    """Uma execucao de pontuacao, como ficou registrada."""

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

    name: str
    dimensions: list[str]
    config_hash: str
    exploratory: bool


class Alerta(BaseModel):
    """Um alerta levantado, por evento ou por pessoa numa janela (D-12)."""

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

    unit: str = Field(description="event, episode ou user_day (D-12)")
    threshold: float
    recall: float | None = None
    false_positive_rate: float | None = None
    detection_delay_days: float | None = None
    positives: int | None = None
    negatives: int | None = None


class Saude(BaseModel):
    """Resposta de `/health`, para o painel saber se vale tentar."""

    status: str
    adapter: str = Field(description="Qual adaptador esta servindo os dados")
    runs: int = Field(description="Quantas execucoes de pontuacao existem")
