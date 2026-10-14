"""De onde sai o retrato de postura — e por que isso e dominio, nao adaptador.

**Nao existe tabela de postura.** O banco `corp` tem `account_state`, que e por
intervalo, `device_state_daily`, que e por dia, e os eventos. Os cinco sinais da
**D-30** saem da combinacao dos tres:

| Sinal | De onde vem |
|---|---|
| Segundo fator e privilegio | `account_state` vigente **no instante do evento** |
| Atualizacao e antivirus | `device_state_daily` do **dia local** do evento |
| Desfecho de phishing | ultimo `PHISHING_SIM` da pessoa na janela |
| Dispositivo removivel | `EXTERNAL_DEVICE` da pessoa na janela |
| Navegacao de risco | `WEB_BROWSING` de categoria de risco na janela |

Se essa combinacao morasse no adaptador, cada adaptador a faria a seu modo: o de
arquivo de um jeito, o de PostgreSQL de outro, e a nota mudaria com a fonte de
dados em vez de com o comportamento. **A derivacao e regra; buscar os dados e
adaptador.** O adaptador entrega as linhas; esta funcao decide o que elas
significam.

**O instante manda, nao o dia.** O estado da conta e lido no instante exato do
evento — `valid_from <= occurred_at < valid_to` —, porque alguem pode ter
perdido o privilegio no meio do dia e os eventos de antes e de depois nao podem
receber o mesmo retrato. Ja o equipamento e por dia, porque e assim que a tabela
existe; fingir precisao de hora ali seria inventar dado.

**A janela nao inclui o evento atual**, pela mesma razao da D-18: o evento sendo
avaliado ja pontua na D1 e na D2, e contar o uso de removivel dele outra vez na
postura seria dupla contagem com outro nome.
"""

from collections.abc import Iterable
from zoneinfo import ZoneInfo

from detection.configuration import Configuration, ConfigurationError
from detection.d1.scoring import CATEGORIAS_DE_RISCO
from detection.d3.scoring import DESFECHOS_DE_PHISHING, Posture
from detection.model import (
    AccountState,
    Catalog,
    DeviceState,
    Event,
    EventType,
)


def _conta_vigente(event: Event, estados: Iterable[AccountState]) -> AccountState:
    """O estado da conta no instante do evento, e nao o mais recente.

    Raises:
        ValueError: Se nenhum estado cobrir o instante, ou se um estado for de
            outra pessoa. Escolher "o mais proximo" esconderia carga incompleta
            e produziria retrato plausivel e errado.
    """
    candidatos = []
    for estado in estados:
        if estado.employee_id != event.employee_id:
            raise ValueError(
                f"estado da conta do funcionario {estado.employee_id} usado para "
                f"avaliar evento do funcionario {event.employee_id}"
            )
        if estado.covers(event.occurred_at):
            candidatos.append(estado)

    if not candidatos:
        raise ValueError(
            f"nenhum estado de conta cobre o instante do evento {event.event_id}: "
            "sem o estado vigente, a postura sairia de um retrato que nao e "
            "daquele momento"
        )
    # Mais de um estado cobrindo o mesmo instante e inconsistencia de carga; o
    # banco impede com a chave primaria, o arquivo nao, e aqui vale o ultimo a
    # comecar.
    return max(candidatos, key=lambda e: e.valid_from)


def _desfecho_de_phishing(janela: Iterable[Event]) -> str | None:
    """O desfecho da ultima campanha na janela, ou None se nao houve campanha.

    Nao e o pior desfecho da janela: e o mais recente. Quem clicou em marco e
    reportou em abril corrigiu a conduta, e guardar o pior congelaria a pessoa
    no erro mais antigo.
    """
    campanhas = [e for e in janela if e.event_type is EventType.PHISHING_SIM]
    if not campanhas:
        return None

    ultima = max(campanhas, key=lambda e: e.occurred_at)
    desfecho = ultima.attributes.get("outcome")
    if desfecho not in DESFECHOS_DE_PHISHING:
        raise ValueError(
            f"evento {ultima.event_id} tem desfecho de phishing {desfecho!r}, "
            f"fora da lista fechada {DESFECHOS_DE_PHISHING}"
        )
    return desfecho


def build_posture(
    event: Event,
    *,
    account_states: Iterable[AccountState],
    device_states: Iterable[DeviceState],
    recent: Iterable[Event],
    catalog: Catalog,
    config: Configuration,
) -> Posture:
    """Monta o retrato de postura do dia do evento, a partir das tres fontes.

    Args:
        event: O evento a avaliar. Define o instante e o dia local.
        account_states: Estados da conta daquela pessoa, de qualquer periodo. O
            vigente e escolhido aqui.
        device_states: Estados diarios de equipamento. O do dia local do evento
            e escolhido aqui.
        recent: Eventos anteriores da mesma pessoa. A janela de `[d3]` e
            recortada aqui, e o evento atual **nao** entra.
        catalog: Para o fuso do funcionario, que define o dia.
        config: Um preset que ligue a dimensao `d3`.

    Returns:
        O retrato, com `as_of` no dia local do evento — que e o unico valor que
        `score_posture` aceita.

    Raises:
        ConfigurationError: Se a configuracao nao ligar a dimensao `d3`.
        ValueError: Se faltar estado de conta vigente, se faltar estado do
            equipamento no dia, se algum insumo for de outra pessoa, ou se um
            desfecho de phishing estiver fora da lista fechada.
    """
    if not config.enables("d3"):
        raise ConfigurationError(f"a configuracao {config.name} nao liga a dimensao d3")

    fuso = ZoneInfo(catalog.employee(event.employee_id).timezone)
    dia = event.occurred_at.astimezone(fuso).date()

    conta = _conta_vigente(event, account_states)

    do_dia = [e for e in device_states if e.state_date == dia]
    equipamento = next((e for e in do_dia if e.device_id == event.device_id), None)
    if equipamento is None:
        raise ValueError(
            f"nenhum estado do equipamento {event.device_id} em {dia}: sem ele, "
            "atualizacao e antivirus sairiam como se estivessem em ordem"
        )

    janela_dias = config.dimension("d3")["window_days"]
    janela = [
        e
        for e in recent
        if e.employee_id == event.employee_id
        and e.occurred_at < event.occurred_at
        and (dia - e.occurred_at.astimezone(fuso).date()).days <= janela_dias
    ]

    removiveis = sum(1 for e in janela if e.event_type is EventType.EXTERNAL_DEVICE)
    arriscada = sum(
        1
        for e in janela
        if e.event_type is EventType.WEB_BROWSING
        and e.attributes.get("category") in CATEGORIAS_DE_RISCO
    )

    return Posture(
        as_of=dia,
        mfa_enabled=conta.mfa_enabled,
        privilege=conta.privilege,
        patch_age_days=equipamento.patch_age_days,
        antivirus_on=equipamento.antivirus_on,
        phishing_outcome=_desfecho_de_phishing(janela),
        removable_uses=removiveis,
        risky_browsing=arriscada,
    )
