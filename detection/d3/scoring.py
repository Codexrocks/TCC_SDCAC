"""Exposicao acumulada e postura de seguranca — as duas parcelas da D3.

A **D-25** e a **D-30** fixam que esta dimensao reporta **duas parcelas
separadas**, cada uma de 0 a 100, e que elas **nao sao somadas** num valor
unico. O motivo esta na propria decisao: a agregacao exigiria um peso relativo
entre conduta e postura sem justificativa defensavel, e a separacao preserva a
decomponibilidade do risco que a usabilidade exige.

**Conduta** e o que a pessoa fez: a soma do risco dos eventos anteriores dela,
com decaimento por dia, numa janela deslizante. **Postura** e o estado da conta
e do equipamento na data do evento — segundo fator, privilegio, atualizacao,
antivirus, conduta em campanha de phishing, uso de dispositivo removivel e
navegacao de risco.

**O evento atual nao entra na conduta (D-18).** A funcao recusa receber um risco
anterior com instante maior ou igual ao do evento avaliado: assim a dupla
contagem que a decisao descreve nao depende de quem chama lembrar dela. Sem
isso, o peso efetivo do evento atual seria a soma do peso dele com o da
exposicao, e nenhum dos dois seria interpretavel.

**A postura e lida como estava naquele dia.** O retrato carrega a data, e a
funcao recusa retrato de outro dia. Ler o estado final seria a falha da D-17 por
outro caminho: o resultado ficaria bom porque o futuro vazou para o passado.
"""

from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

from detection.configuration import Configuration, ConfigurationError
from detection.model import Catalog, DimensionScore, Event, Privilege, RuleHit

# Desfechos de campanha de phishing, do melhor ao pior caso. A ordem e a fonte
# da verdade, pela D-42 — reportar e melhor que ignorar.
DESFECHOS_DE_PHISHING = ("reported", "ignored", "clicked", "submitted_credentials")


@dataclass(frozen=True, slots=True)
class PriorScore:
    """O risco de um evento anterior da mesma pessoa.

    Quem pontua um evento guarda o par (instante, pontos) e passa adiante: a D3
    nao repontua o passado, soma o que ja foi medido. Em `points` vai a soma das
    dimensoes de evento daquele evento — D1, ou D1 mais D2, conforme a
    configuracao em execucao.
    """

    occurred_at: datetime
    points: int


@dataclass(frozen=True, slots=True)
class Posture:
    """O estado de conta e equipamento num dia, com a data que o torna valido.

    Attributes:
        as_of: O dia a que este retrato se refere, no fuso do funcionario.
        mfa_enabled: Segundo fator ligado na conta.
        privilege: Nivel de privilegio vigente.
        patch_age_days: Dias desde a ultima atualizacao do equipamento.
        antivirus_on: Antivirus ativo no equipamento.
        phishing_outcome: Desfecho da ultima campanha, ou None se nao houve.
        removable_uses: Usos de dispositivo removivel na janela.
        risky_browsing: Acessos a categoria de risco na janela.
    """

    as_of: date
    mfa_enabled: bool
    privilege: Privilege
    patch_age_days: int
    antivirus_on: bool
    phishing_outcome: str | None = None
    removable_uses: int = 0
    risky_browsing: int = 0


@dataclass(frozen=True, slots=True)
class ThirdDimension:
    """As duas parcelas da D3, lado a lado e nunca somadas aqui.

    Quem decide como as duas entram na nota final e a integracao, com pesos
    declarados — e mesmo lá elas continuam gravadas em colunas separadas.
    """

    conduct: DimensionScore
    posture: DimensionScore


def _confere_anteriores(event: Event, priors: tuple[PriorScore, ...]) -> None:
    for anterior in priors:
        if anterior.occurred_at >= event.occurred_at:
            raise ValueError(
                "a janela de exposicao recebeu risco de instante maior ou igual "
                f"ao do evento {event.event_id}: a D-18 manda excluir o evento "
                "atual da janela, e dupla contagem nao e aviso, e erro"
            )


def score_conduct(
    event: Event,
    priors: tuple[PriorScore, ...],
    catalog: Catalog,
    config: Configuration,
) -> DimensionScore:
    """Exposicao acumulada: o risco anterior da pessoa, com decaimento.

    Args:
        event: O evento a avaliar.
        priors: Risco dos eventos anteriores da mesma pessoa, todos com
            instante **estritamente menor** que o do evento avaliado.
        catalog: Para o fuso do funcionario, que define o dia do decaimento.
        config: Um preset que ligue a dimensao `d3`.

    Returns:
        A parcela de conduta, de 0 a 100.

    Raises:
        ValueError: Se algum risco anterior nao for anterior de fato.
    """
    _confere_anteriores(event, priors)

    parametros = config.dimension("d3")
    janela = parametros["window_days"]
    decaimento = parametros["decay_per_day"]
    referencia = parametros["exposure_reference"]

    fuso = ZoneInfo(catalog.employee(event.employee_id).timezone)
    dia_do_evento = event.occurred_at.astimezone(fuso).date()

    acumulado = 0.0
    contados = 0
    for anterior in priors:
        dias = (dia_do_evento - anterior.occurred_at.astimezone(fuso).date()).days
        if dias > janela:
            continue
        acumulado += anterior.points * (decaimento**dias)
        contados += 1

    if acumulado <= 0:
        return DimensionScore(points=0)

    pontos = min(100, int(round(100 * acumulado / referencia)))
    if pontos == 0:
        return DimensionScore(points=0)

    return DimensionScore(
        points=pontos,
        hits=(
            RuleHit(
                rule="accumulated_exposure",
                points=pontos,
                reason=(
                    f"{contados} eventos nos ultimos {janela} dias somam "
                    f"{acumulado:.0f} pontos com decaimento, contra referencia "
                    f"de {referencia}"
                ),
            ),
        ),
    )


def score_posture(
    event: Event,
    posture: Posture,
    catalog: Catalog,
    config: Configuration,
) -> DimensionScore:
    """Postura de seguranca: o estado da conta e do equipamento naquele dia.

    Args:
        event: O evento a avaliar.
        posture: O retrato do estado, com a data a que se refere.
        catalog: Para o fuso do funcionario, que define o dia.
        config: Um preset que ligue a dimensao `d3`.

    Returns:
        A parcela de postura, de 0 a 100.

    Raises:
        ValueError: Se o retrato for de outro dia. Ler o estado final seria a
            falha da D-17 por outro caminho.
    """
    fuso = ZoneInfo(catalog.employee(event.employee_id).timezone)
    dia = event.occurred_at.astimezone(fuso).date()
    if posture.as_of != dia:
        raise ValueError(
            f"retrato de postura de {posture.as_of} usado para avaliar evento de "
            f"{dia}: o estado precisa ser o do dia do evento"
        )

    pesos = config.dimension("d3")["posture"]
    achados: list[RuleHit] = []

    if not posture.mfa_enabled:
        achados.append(
            RuleHit(
                rule="mfa_disabled",
                points=pesos["mfa_disabled"],
                reason="conta sem segundo fator na data do evento",
            )
        )

    if posture.privilege is Privilege.ADMIN:
        achados.append(
            RuleHit(
                rule="privilege_admin",
                points=pesos["privilege_admin"],
                reason="conta com privilegio administrativo",
            )
        )

    limite = pesos["patch_age_days_limit"]
    if posture.patch_age_days > limite:
        achados.append(
            RuleHit(
                rule="patch_overdue",
                points=pesos["patch_overdue"],
                reason=(
                    f"equipamento com {posture.patch_age_days} dias sem "
                    f"atualizacao, acima de {limite}"
                ),
            )
        )

    if not posture.antivirus_on:
        achados.append(
            RuleHit(
                rule="antivirus_off",
                points=pesos["antivirus_off"],
                reason="antivirus inativo no equipamento",
            )
        )

    if posture.phishing_outcome == "clicked":
        achados.append(
            RuleHit(
                rule="phishing_clicked",
                points=pesos["phishing_clicked"],
                reason="clicou na ultima campanha de phishing",
            )
        )
    elif posture.phishing_outcome == "submitted_credentials":
        achados.append(
            RuleHit(
                rule="phishing_submitted",
                points=pesos["phishing_submitted"],
                reason="entregou credencial na ultima campanha de phishing",
            )
        )

    if posture.removable_uses:
        achados.append(
            RuleHit(
                rule="removable_use",
                points=pesos["removable_use"] * min(posture.removable_uses, 3),
                reason=(
                    f"{posture.removable_uses} usos de dispositivo removivel na janela"
                ),
            )
        )

    if posture.risky_browsing:
        achados.append(
            RuleHit(
                rule="risky_browsing",
                points=pesos["risky_browsing"] * min(posture.risky_browsing, 4),
                reason=(
                    f"{posture.risky_browsing} acessos a categoria de risco na janela"
                ),
            )
        )

    total = min(100, sum(hit.points for hit in achados))
    return DimensionScore(points=total, hits=tuple(achados))


def score_d3(
    event: Event,
    priors: tuple[PriorScore, ...],
    posture: Posture,
    catalog: Catalog,
    config: Configuration,
) -> ThirdDimension:
    """As duas parcelas da D3, calculadas e devolvidas separadas.

    Raises:
        ConfigurationError: Se a configuracao nao ligar a dimensao `d3`.
        ValueError: Se a janela incluir o evento atual, ou se o retrato de
            postura for de outro dia.
    """
    if not config.enables("d3"):
        raise ConfigurationError(f"a configuracao {config.name} nao liga a dimensao d3")

    return ThirdDimension(
        conduct=score_conduct(event, priors, catalog, config),
        posture=score_posture(event, posture, catalog, config),
    )
