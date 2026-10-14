"""As regras fixas da linha de base.

Tres das quatro regras da **D-31** estao aqui. A quarta — contagem de falhas de
autenticacao — **nao esta, e a falta e deliberada**: as duas paginas que a
definem discordam entre si.

- A **D-31**, em docs/banco-simulado.md, mantem "mais de N falhas de
  autenticacao em 2 minutos na mesma conta, com N fixo".
- A **Metodologia**, secao 3.3, afirma que a C0 e puramente estatica e que
  "duas das quatro regras da linha de base — a nocao de endereco de origem
  habitual e a janela de contagem de falhas de autenticacao — utilizavam
  historico individual", e que mante-las contaminaria o grupo de controle.

Uma janela de dois minutos sobre a mesma conta olha o passado daquela conta.
Entao a invariante que a propria D-31 declara — "embaralhar o historico nao
pode mudar nota nenhuma" — seria falsa com a regra ligada. Implementar uma das
duas versoes agora seria escolher pelo Davi qual texto esta certo, e o que esta
em disputa aparece no artigo. A escolha esta no Pull Request, a decidir.

As tres regras implementadas sao estaticamente verificaveis: nenhuma delas
recebe o funcionario.
"""

from zoneinfo import ZoneInfo

from detection.configuration import Configuration, ConfigurationError
from detection.model import (
    Catalog,
    DimensionScore,
    Event,
    NetworkKind,
    RuleHit,
    Sensitivity,
)

FAIXAS_CORPORATIVAS = (NetworkKind.OFFICE, NetworkKind.VPN)


def off_hours(event: Event, config: Configuration) -> RuleHit | None:
    """Evento fora do horario comercial, no fuso da SEDE.

    O fuso e o da sede de proposito, e nao o do funcionario: a C0 e generica
    por definicao. Quem trabalha em outro fuso aparece aqui fora de hora sem
    ter feito nada de errado, e esse falso positivo legitimo e justamente o que
    a D1 corrige — e o que a pergunta de pesquisa mede.

    Args:
        event: O evento a avaliar.
        config: Configuracao com `site_timezone` e o horario comercial.

    Returns:
        A regra disparada, ou None.
    """
    parametros = config.dimension("c0")
    fuso = ZoneInfo(parametros["site_timezone"])
    inicio = parametros["business_hour_start"]
    fim = parametros["business_hour_end"]

    hora_local = event.occurred_at.astimezone(fuso)
    if inicio <= hora_local.hour < fim:
        return None

    return RuleHit(
        rule="off_hours",
        points=parametros["points"]["off_hours"],
        reason=(
            f"evento as {hora_local:%H:%M} no fuso da sede, "
            f"fora da janela de {inicio}h as {fim}h"
        ),
    )


def external_origin(
    event: Event, catalog: Catalog, config: Configuration
) -> RuleHit | None:
    """Origem fora das faixas corporativas cadastradas.

    Lista estatica, e nao "o IP habitual daquela pessoa" — a diferenca e o que
    separa a C0 do que a D2 faz.

    Raises:
        ValueError: Se nenhuma faixa corporativa estiver cadastrada. Sem elas
            todo IP pareceria externo, e a regra alarmaria em cima de um
            catalogo vazio em vez de falhar.
    """
    corporativas = catalog.ranges_of(*FAIXAS_CORPORATIVAS)
    if not corporativas:
        raise ValueError(
            "nenhuma faixa de rede corporativa cadastrada: a regra de origem "
            "nao tem como distinguir dentro de fora"
        )

    for faixa in corporativas:
        if event.ip_address in faixa.cidr:
            return None

    parametros = config.dimension("c0")
    return RuleHit(
        rule="external_origin",
        points=parametros["points"]["external_origin"],
        reason=f"origem {event.ip_address} fora das faixas corporativas",
    )


def restricted_access(
    event: Event, catalog: Catalog, config: Configuration
) -> RuleHit | None:
    """Acesso a recurso classificado como restrito.

    A sensibilidade vem do catalogo de recursos, nunca do `attributes` do
    evento: ela e atributo do recurso e precisa valer igual em todo tipo de
    evento. O banco proibe a outra forma por restricao.
    """
    if event.resource_id is None:
        return None

    recurso = catalog.resource(event.resource_id)
    if recurso.sensitivity is not Sensitivity.RESTRICTED:
        return None

    parametros = config.dimension("c0")
    return RuleHit(
        rule="restricted_access",
        points=parametros["points"]["restricted_access"],
        reason=f"acesso ao recurso restrito {recurso.name!r}",
    )


def score_c0(event: Event, catalog: Catalog, config: Configuration) -> DimensionScore:
    """Soma os pontos das regras fixas disparadas pelo evento.

    Nao ha teto: o score bruto e o que a avaliacao usa, porque faixa empatada
    no teto viraria degrau na curva precisao-revocacao da D-14. O teto de 100
    existe so na faixa de exibicao.

    Args:
        event: O evento a avaliar.
        catalog: Recursos e faixas de rede. O funcionario nao e consultado.
        config: Um preset que ligue a dimensao `c0`.

    Returns:
        A nota da C0, com as regras que a formaram.

    Raises:
        ConfigurationError: Se a configuracao nao ligar a dimensao `c0`.
    """
    if not config.enables("c0"):
        raise ConfigurationError(f"a configuracao {config.name} nao liga a dimensao c0")

    hits = [
        off_hours(event, config),
        external_origin(event, catalog, config),
        restricted_access(event, catalog, config),
    ]
    disparadas = tuple(hit for hit in hits if hit is not None)
    return DimensionScore(
        points=sum(hit.points for hit in disparadas),
        hits=disparadas,
    )
