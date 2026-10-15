"""O lado de leitura do adaptador de arquivo — o que a API serve.

Cumpre `detection.ports.ScoreRepository` contra o mesmo diretorio que o
executor escreveu. Enquanto o `sdcac` nao existe, e isto que o painel consome; o
dia em que existir, entra o adaptador de PostgreSQL e **nenhuma rota muda**.

**O que este arquivo pode fazer e o que nao pode.** Pode selecionar, ordenar,
paginar e juntar: `risk_scores` nao guarda `employee_id`, e descobrir de quem e
cada nota exige ir ao evento — no banco e um `JOIN`, aqui e um dicionario. O que
ele **nao** pode e calcular: media, taxa, faixa, contagem derivada. Se a leitura
calculasse, o painel mostraria numero que o motor nunca produziu, e a tabela do
artigo e a tela passariam a dizer coisas diferentes.

**Paginacao em tudo.** Lista sem limite deixaria uma requisicao puxar dois
milhoes de eventos — negacao de servico de graca, e nenhuma tela precisa disso.
Cada metodo devolve `(pagina, total)`: o total e o que permite ao painel dizer
"1 a 50 de 12.431" sem puxar o resto.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from detection.integracao import RiskScore
from storage.arquivos import ArquivoStorage

# Teto duro de pagina. Nem o painel nem ninguem pede mais que isto de uma vez, e
# o parametro vindo do cliente nao pode ser quem decide.
LIMITE_MAXIMO = 200


@dataclass(frozen=True, slots=True)
class EmployeeScore:
    """A nota mais recente de uma pessoa, com o evento que a produziu."""

    employee_id: int
    event_id: str
    occurred_at: datetime
    score: RiskScore


@dataclass(frozen=True, slots=True)
class EventScore:
    """Uma nota com o contexto minimo do evento que a gerou."""

    employee_id: int
    occurred_at: datetime
    event_type: str
    score: RiskScore


def _pagina(itens: Sequence, limit: int, offset: int) -> tuple[Sequence, int]:
    """Recorta a pagina e devolve o total, que e o que o painel precisa.

    O recorte e feito depois da ordenacao, sempre: paginar antes de ordenar
    devolveria paginas que se sobrepoem e itens que nunca aparecem.
    """
    limite = max(1, min(int(limit), LIMITE_MAXIMO))
    inicio = max(0, int(offset))
    return itens[inicio : inicio + limite], len(itens)


class ArquivoRepository(ArquivoStorage):
    """O `ScoreRepository` sobre o diretorio de arquivos."""

    # ------------------------------------------------------------ execucoes

    def list_runs(self, *, limit: int = 50, offset: int = 0):
        """Execucoes, da mais recente para a mais antiga."""
        registros = sorted(
            self._registros(), key=lambda r: r["scoring_run_id"], reverse=True
        )
        return _pagina(registros, limit, offset)

    # ---------------------------------------------------------- juncao base

    def _eventos_por_id(self, scoring_run_id: int) -> dict[str, object]:
        """Mapa evento → evento daquela semente.

        E a juncao que `risk_scores` precisa: a tabela guarda a nota, e de quem
        ela e esta no evento. No banco isto e um `JOIN`; aqui, um dicionario.
        """
        run_id = int(self.run(scoring_run_id)["run_id"])
        return {e.event_id: e for e in self.events(run_id)}

    # --------------------------------------------------------- funcionarios

    def list_employee_scores(
        self, scoring_run_id: int, *, limit: int = 50, offset: int = 0
    ):
        """A nota mais recente de cada pessoa, pela D-36.

        "Mais recente" e selecao, nao calculo: e o maior `occurred_at` daquela
        pessoa naquela execucao.
        """
        eventos = self._eventos_por_id(scoring_run_id)
        por_pessoa: dict[int, EmployeeScore] = {}

        for nota in self.load_scores(scoring_run_id):
            evento = eventos.get(nota.event_id)
            if evento is None:
                continue
            atual = por_pessoa.get(evento.employee_id)
            if atual is None or evento.occurred_at > atual.occurred_at:
                por_pessoa[evento.employee_id] = EmployeeScore(
                    employee_id=evento.employee_id,
                    event_id=nota.event_id,
                    occurred_at=evento.occurred_at,
                    score=nota,
                )

        ordenado = sorted(por_pessoa.values(), key=lambda e: e.employee_id)
        return _pagina(ordenado, limit, offset)

    def employee_history(
        self, scoring_run_id: int, employee_id: int, *, limit: int = 50, offset: int = 0
    ):
        """O historico de notas de uma pessoa, da mais recente para a mais antiga."""
        eventos = self._eventos_por_id(scoring_run_id)
        historico = [
            EventScore(
                employee_id=employee_id,
                occurred_at=eventos[nota.event_id].occurred_at,
                event_type=eventos[nota.event_id].event_type.value,
                score=nota,
            )
            for nota in self.load_scores(scoring_run_id)
            if nota.event_id in eventos
            and eventos[nota.event_id].employee_id == employee_id
        ]
        historico.sort(key=lambda e: (e.occurred_at, e.score.event_id), reverse=True)
        return _pagina(historico, limit, offset)

    # -------------------------------------------------------------- alertas

    def list_alerts(
        self,
        scoring_run_id: int,
        *,
        band: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ):
        """Alertas filtraveis por faixa e periodo, do mais recente ao mais antigo."""
        alertas = []
        for alerta in self.load_alerts(scoring_run_id):
            levantado = datetime.fromisoformat(str(alerta["raised_at"]))
            if band is not None and alerta["band"] != band:
                continue
            if since is not None and levantado < since:
                continue
            if until is not None and levantado > until:
                continue
            alertas.append({**alerta, "raised_at": levantado})

        alertas.sort(
            key=lambda a: (a["raised_at"], str(a.get("event_id"))), reverse=True
        )
        return _pagina(alertas, limit, offset)

    # --------------------------------------------------------------- evento

    def event_score(self, scoring_run_id: int, event_id: str) -> EventScore | None:
        """A nota de um evento, decomposta, ou None se nao houver."""
        for nota in self.load_scores(scoring_run_id):
            if nota.event_id != event_id:
                continue
            evento = self._eventos_por_id(scoring_run_id).get(event_id)
            if evento is None:
                return None
            return EventScore(
                employee_id=evento.employee_id,
                occurred_at=evento.occurred_at,
                event_type=evento.event_type.value,
                score=nota,
            )
        return None

    # ------------------------------------------------------------- metricas

    def list_metrics(self, scoring_run_id: int, *, limit: int = 50, offset: int = 0):
        """O que o avaliador gravou — e ele ainda nao existe.

        Devolve pagina vazia, e isso e resposta, nao falha: a API **nao calcula
        metrica**. Precisao e revocacao saem do avaliador, que e o unico que
        enxerga o gabarito, e que entra na S11. Se a API calculasse aqui, ela
        precisaria do rotulo — e o usuario da aplicacao nao tem permissao de
        conectar no `ground_truth`.
        """
        import json

        caminho = self.raiz / "sdcac" / "metricas" / f"{scoring_run_id}.json"
        if not caminho.exists():
            return [], 0
        linhas = json.loads(caminho.read_text(encoding="utf-8"))
        return _pagina(linhas, limit, offset)
