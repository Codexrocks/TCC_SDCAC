"""As portas: tudo que entra no motor e tudo que sai dele.

Este arquivo e o contrato que o resto do sistema tem de cumprir. Ele declara
**o que** o motor consome e produz, e **nao diz de onde vem** — PostgreSQL,
arquivo, memoria de teste, tanto faz. Enquanto o banco e o painel nao existem,
e aqui que eles ja estao previstos.

**Por que as portas moram no nucleo, e nao no adaptador.** Em `detection/` nao
entra `psycopg`, `fastapi` nem relogio — a regra de dependencia da arquitetura,
conferida no CI. Uma porta e so um `Protocol`: nome de metodo, tipo de entrada,
tipo de saida. Declara-la aqui mantem o nucleo dono do proprio contrato, e e o
que impede o inverso — o motor sendo moldado pelo formato de tabela que alguem
escolheu.

**O que isto compra, concretamente:**

- o executor roda hoje, contra arquivo, sem banco nenhum;
- quem escrever o adaptador de PostgreSQL tem **especificacao executavel**: o
  teste de contrato roda as mesmas assercoes contra qualquer implementacao, e
  reprova a que mentir;
- a API de leitura depende de `ScoreRepository`, e nao de SQL. O painel comeca
  contra o adaptador de arquivo e troca a fonte sem mudar uma rota.

**Dois lados, e eles nao se misturam.** As portas de **escrita** servem ao
executor, que calcula; as de **leitura** servem a API, que so mostra. Nenhuma
porta de leitura devolve algo que precise ser calculado na hora: se a API
pudesse somar, mediar ou classificar, o painel mostraria numero que o motor
nunca produziu — e a tabela do artigo e a tela diriam coisas diferentes.

**O gabarito nao tem porta.** Nao existe aqui nada que leia rotulo de cenario,
e isso e deliberado: o `ground_truth` e lido **so** pelo avaliador, e o usuario
da aplicacao nao tem permissao de conectar naquele banco. Porta de leitura de
rotulo seria o vazamento de rotulo com nome de arquitetura.
"""

from collections.abc import Iterable, Iterator, Mapping, Sequence
from datetime import date, datetime
from typing import Protocol, runtime_checkable

from detection.d2 import Baseline
from detection.integracao import Alert, RiskScore
from detection.model import AccountState, Catalog, DeviceState, Event

# ---------------------------------------------------------------------------
# Entrada — o que o motor consome do `corp`
# ---------------------------------------------------------------------------


@runtime_checkable
class CatalogSource(Protocol):
    """De onde vem o cadastro da organizacao.

    O catalogo nao muda durante uma execucao: funcionario, dispositivo, recurso
    e faixa de rede sao cadastro, e a pontuacao de dois eventos da mesma
    execucao nunca pode divergir porque o cadastro mudou no meio.
    """

    def catalog(self, run_id: int) -> Catalog:
        """O cadastro completo de uma semente."""
        ...


@runtime_checkable
class EventSource(Protocol):
    """De onde vem o fluxo de eventos.

    A ordem importa: a C0 precisa dos dois minutos anteriores, a D2 das janelas
    de sessao e de usuario-dia, a D3 da janela de exposicao. Por isso a porta
    promete **ordem cronologica crescente** — e e promessa do adaptador, nao
    esperanca de quem consome.
    """

    def events(
        self,
        run_id: int,
        *,
        start: datetime | None = None,
        end: datetime | None = None,
        employee_id: int | None = None,
    ) -> Iterator[Event]:
        """Eventos de uma semente, em ordem cronologica crescente.

        O recorte e inclusivo em `start` e exclusivo em `end`, para que janelas
        adjacentes nao contem o mesmo evento duas vezes.
        """
        ...


@runtime_checkable
class StateSource(Protocol):
    """De onde vem o estado de conta e de equipamento.

    Duas granularidades diferentes de proposito: a conta e por intervalo,
    porque privilegio muda no meio do dia; o equipamento e por dia, porque e
    assim que a tabela existe, e fingir precisao de hora ali seria inventar
    dado.

    Quem combina as duas em retrato de postura e `detection.d3.build_posture`,
    e nao o adaptador: se a combinacao fosse do adaptador, a nota mudaria com a
    fonte de dados em vez de com o comportamento.
    """

    def account_states(self, run_id: int, employee_id: int) -> tuple[AccountState, ...]:
        """Todos os estados de conta daquela pessoa, de qualquer periodo."""
        ...

    def device_states(
        self, run_id: int, *, device_id: int, day: date
    ) -> tuple[DeviceState, ...]:
        """Os estados de equipamento de um dia."""
        ...


# ---------------------------------------------------------------------------
# Saida — o que o motor grava no `sdcac`
# ---------------------------------------------------------------------------


@runtime_checkable
class RunRegistry(Protocol):
    """O registro de execucao, que e a trava da D-34.

    `open_run` **exige** o hash da configuracao. Quem grava uma execucao sem
    ele nao consegue — nao por disciplina, por falta do argumento.
    """

    def open_run(
        self,
        *,
        run_id: int,
        config_name: str,
        config_hash: str,
        code_sha: str,
        weights_version: str,
        exploratory: bool,
    ) -> int:
        """Abre uma execucao de pontuacao e devolve o identificador dela."""
        ...

    def close_run(self, scoring_run_id: int, *, status: str) -> None:
        """Fecha a execucao, com o estado final."""
        ...

    def run(self, scoring_run_id: int) -> Mapping[str, object]:
        """O registro de uma execucao, como foi gravado."""
        ...


@runtime_checkable
class BaselineStore(Protocol):
    """Onde ficam os padroes do passo 1.

    Gravar o padrao nao e cache: e o que permite reexecutar o passo 2 sem
    reconstruir o passo 1, e e o que torna o padrao auditavel depois. Padrao
    que so existiu em memoria nao e verificavel por ninguem.
    """

    def save_baselines(
        self, scoring_run_id: int, baselines: Mapping[int, Baseline]
    ) -> None: ...

    def load_baselines(self, scoring_run_id: int) -> dict[int, Baseline]: ...


@runtime_checkable
class ScoreSink(Protocol):
    """Onde ficam as notas e os alertas.

    As notas vao em lote, e nao uma por uma: sao milhoes, e a porta precisa
    permitir que o adaptador de banco use `COPY` sem que o executor saiba disso.
    """

    def save_scores(self, scoring_run_id: int, scores: Iterable[RiskScore]) -> None: ...

    def save_alerts(self, scoring_run_id: int, alerts: Iterable[Alert]) -> None: ...


# ---------------------------------------------------------------------------
# Leitura — o que a API mostra
# ---------------------------------------------------------------------------


@runtime_checkable
class ScoreRepository(Protocol):
    """O lado de leitura, que e o contrato do painel.

    Todo metodo de lista recebe `limit` e `offset` e devolve pagina. Lista sem
    paginacao aqui deixaria uma requisicao puxar dois milhoes de eventos, que e
    a negacao de servico mais barata que existe — e nenhuma tela precisa disso.

    **Nenhum metodo calcula.** As metricas vem como o avaliador gravou; as notas
    vem como o motor produziu, decompostas nas cinco parcelas. A API serializa.
    """

    def list_runs(self, *, limit: int, offset: int) -> tuple[Sequence[object], int]:
        """Execucoes de pontuacao, da mais recente para a mais antiga."""
        ...

    def list_employee_scores(
        self, scoring_run_id: int, *, limit: int, offset: int
    ) -> tuple[Sequence[object], int]:
        """Funcionarios com a nota mais recente de cada dimensao."""
        ...

    def employee_history(
        self, scoring_run_id: int, employee_id: int, *, limit: int, offset: int
    ) -> tuple[Sequence[object], int]:
        """O historico de notas de uma pessoa naquela execucao."""
        ...

    def list_alerts(
        self,
        scoring_run_id: int,
        *,
        band: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int,
        offset: int,
    ) -> tuple[Sequence[object], int]:
        """Alertas filtraveis por faixa e periodo."""
        ...

    def event_score(self, scoring_run_id: int, event_id: str) -> RiskScore | None:
        """A nota de um evento, decomposta, ou None se nao houver."""
        ...

    def list_metrics(
        self, scoring_run_id: int, *, limit: int, offset: int
    ) -> tuple[Sequence[object], int]:
        """O que o avaliador gravou. A API nao calcula metrica."""
        ...
