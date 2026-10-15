"""As regras fixas da linha de base.

As quatro regras da **D-31**, com a quarta decidida pela **D-42**: a janela de
contagem de falhas **fica**, e o texto da Metodologia foi corrigido para dizer
com precisao o que "estatica" significa aqui.

A distincao que a D-42 fixa, e que vale repetir onde o codigo mora:

- **Parametro aprendido** — media, mediana, conjunto de recursos habituais,
  endereco de origem habitual — e o que a C0 nao tem. Isso e padrao individual,
  e medir a contribuicao dele e o objetivo do experimento. Pontuar o controle
  com a mesma informacao seria contaminar a comparacao.
- **Correlacao de curto prazo** e outra coisa: a janela de dois minutos aplica o
  mesmo limiar as 250 pessoas, nao estima nada de ninguem, e nao guarda
  informacao alem do proprio intervalo. Sem ela, o grupo de controle nao
  detectaria tentativa sucessiva de autenticacao — cenario que regra fixa pega
  com facilidade —, e o ganho apareceria nas dimensoes por falta de adversario.

Tres das quatro regras nao recebem nem o funcionario nem o passado. A quarta
recebe eventos recentes **da mesma conta**, e recusa receber de outra conta ou
do futuro: as duas recusas sao verificadas em teste.
"""

from datetime import timedelta
from zoneinfo import ZoneInfo

from detection.configuration import Configuration, ConfigurationError
from detection.model import (
    Catalog,
    DimensionScore,
    Event,
    EventResult,
    EventType,
    NetworkKind,
    RuleHit,
    Sensitivity,
)

FAIXAS_CORPORATIVAS = (NetworkKind.OFFICE, NetworkKind.VPN)

# Eventos de autenticacao, que e onde a contagem de falhas faz sentido.
AUTENTICACAO = (EventType.LOGIN,)


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


def brute_force(
    event: Event, recent: tuple[Event, ...], config: Configuration
) -> RuleHit | None:
    """Falhas de autenticacao acima do limite, na mesma conta, em janela fixa.

    A regra dispara **no evento que cruza o limite**, e so em evento de
    autenticacao que falhou: e a forma literal da D-31, e e como regra de
    correlacao de SIEM funciona. Acesso bem-sucedido depois de uma rajada nao
    dispara aqui — quem avalia sequencia e a D2.

    O limiar e a janela vem da configuracao e sao iguais para todos. Nada e
    estimado do comportamento de ninguem: e isso que mantem a C0 sem parametro
    aprendido, pela **D-42**.

    Args:
        event: O evento a avaliar.
        recent: Eventos anteriores **da mesma conta**, em qualquer ordem. Quem
            chama decide de onde eles vem; a contagem e a janela sao daqui.
        config: Um preset que ligue a dimensao `c0`.

    Returns:
        A regra disparada, ou None.

    Raises:
        ValueError: Se `recent` trouxer evento de outra conta, ou evento
            posterior ao avaliado. A primeira recusa pega mistura de contas; a
            segunda e a regra de nao olhar para o futuro, aplicada na fronteira
            em vez de confiada a quem chama.
    """
    if event.event_type not in AUTENTICACAO or event.result is not EventResult.FAILURE:
        return None

    parametros = config.dimension("c0")
    janela = timedelta(minutes=parametros["auth_failure_window_minutes"])
    limite = parametros["auth_failure_threshold"]
    inicio = event.occurred_at - janela

    falhas = 1  # o proprio evento, que e uma falha
    for anterior in recent:
        if anterior.employee_id != event.employee_id:
            raise ValueError(
                f"janela de falhas do funcionario {event.employee_id} recebeu "
                f"evento do funcionario {anterior.employee_id}"
            )
        if anterior.occurred_at > event.occurred_at:
            raise ValueError(
                f"janela de falhas recebeu evento posterior ao avaliado: "
                f"{anterior.event_id} ocorreu depois de {event.event_id}"
            )
        if anterior.event_id == event.event_id:
            continue
        if anterior.event_type not in AUTENTICACAO:
            continue
        if anterior.result is not EventResult.FAILURE:
            continue
        if anterior.occurred_at >= inicio:
            falhas += 1

    if falhas <= limite:
        return None

    return RuleHit(
        rule="brute_force",
        points=parametros["points"]["brute_force"],
        reason=(
            f"{falhas} falhas de autenticacao em "
            f"{parametros['auth_failure_window_minutes']} min, acima do limite "
            f"de {limite}"
        ),
    )


def score_c0(
    event: Event,
    catalog: Catalog,
    config: Configuration,
    recent: tuple[Event, ...],
) -> DimensionScore:
    """Soma os pontos das regras fixas disparadas pelo evento.

    Nao ha teto: o score bruto e o que a avaliacao usa, porque faixa empatada
    no teto viraria degrau na curva precisao-revocacao da D-14. O teto de 100
    existe so na faixa de exibicao.

    Args:
        event: O evento a avaliar.
        catalog: Recursos e faixas de rede. O funcionario nao e consultado.
        config: Um preset que ligue a dimensao `c0`.
        recent: Eventos anteriores da mesma conta, para a janela de falhas.
            E obrigatorio de proposito: com valor padrao, quem esquecesse de
            passar desligaria a quarta regra em silencio.

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
        brute_force(event, recent, config),
    ]
    disparadas = tuple(hit for hit in hits if hit is not None)
    return DimensionScore(
        points=sum(hit.points for hit in disparadas),
        hits=disparadas,
    )
