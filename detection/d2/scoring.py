"""O desvio em relacao ao padrao do proprio funcionario.

E a dimensao que responde a parte da pergunta de pesquisa que fala em "desvio
comportamental do usuario". Ela compara o que aconteceu com o que aquela pessoa
costuma fazer — e so ela, entre as quatro, olha o passado.

**Duas janelas, e o maior desvio, nao a soma (D-28).** Sessao e usuario-dia. Um
componente que diverge nas duas e o mesmo desvio visto de dois recortes: somar
contaria duas vezes. Entao cada componente de agregado e calculado nas duas
janelas e entra pelo maior. A semana fica de fora de proposito — acumulacao ao
longo de dias e o que a D3 mede, e se a D2 tambem olhasse sete dias a ablacao
nao separaria a contribuicao das duas.

**Tres componentes nao dependem de janela:** hora incomum, recurso novo e
origem ou dispositivo novo sao propriedades do proprio evento contra o padrao.
Esses entram uma vez.

**Como o peso vira ponto.** Cada componente tem um peso, que e a contribuicao
**maxima** dele, e entra proporcional ao desvio ate o teto: desvio no teto rende
o peso inteiro, metade do teto rende metade. Sem o teto da **D-29** um atributo
sozinho dominaria a nota e os pesos da D-09 viriam enfeite.

**O que esta dimensao nao faz:** olhar para o futuro. A janela e sempre de
eventos com `occurred_at` menor ou igual ao do evento avaliado, e a funcao
recusa receber evento posterior — a falha da **D-17** aplicada na fronteira, em
vez de confiada a quem chama.
"""

from datetime import date
from zoneinfo import ZoneInfo

from detection.configuration import Configuration, ConfigurationError
from detection.d2.baseline import SENSIVEIS, Baseline
from detection.model import (
    Catalog,
    DimensionScore,
    Event,
    EventResult,
    EventType,
    RuleHit,
)


def _pontos(peso: int, desvio: float, teto: float) -> int:
    """Converte desvio em ponto, proporcional ao teto."""
    if desvio <= 0:
        return 0
    return int(round(peso * min(desvio, teto) / teto))


def _confere_janela(event: Event, recent: tuple[Event, ...]) -> None:
    for anterior in recent:
        if anterior.employee_id != event.employee_id:
            raise ValueError(
                f"janela da D2 do funcionario {event.employee_id} recebeu evento "
                f"do funcionario {anterior.employee_id}"
            )
        if anterior.occurred_at > event.occurred_at:
            raise ValueError(
                "janela da D2 recebeu evento posterior ao avaliado: "
                f"{anterior.event_id} ocorreu depois de {event.event_id}"
            )


def _hora_incomum(
    event: Event, baseline: Baseline, fuso: ZoneInfo, parametros, pontos
) -> RuleHit | None:
    """Hora em que aquela pessoa quase nunca trabalha.

    Nao e "fora do horario comercial" — isso a C0 e a D1 ja fazem. Aqui a
    referencia e a distribuicao de horas da propria pessoa: para quem faz
    plantao, tres da manha e hora de trabalho, e nao divergencia.
    """
    hora = event.occurred_at.astimezone(fuso).hour
    fracao = baseline.hour_share[hora]
    limite = parametros["unusual_hour_share"]
    if fracao >= limite:
        return None

    return RuleHit(
        rule="unusual_hour",
        points=pontos["unusual_hour"],
        reason=(
            f"hora {hora:02d}h responde por {fracao:.1%} do padrao da pessoa, "
            f"abaixo de {limite:.1%}"
        ),
    )


def _recurso_novo(
    event: Event, baseline: Baseline, catalog: Catalog, config: Configuration, pontos
) -> RuleHit | None:
    """Recurso que a pessoa nunca tocou na janela de treino.

    O peso cresce com o sigilo: area restrita que a pessoa nunca abriu pesa mais
    que uma pasta interna nova. E a parte "com peso maior quando o recurso e de
    sigilo alto" da D-29.
    """
    if event.resource_id is None or event.resource_id in baseline.resources:
        return None

    recurso = catalog.resource(event.resource_id)
    multiplicador = config.dimension("d2")["sensitivity_multiplier"][
        recurso.sensitivity.value
    ]
    return RuleHit(
        rule="new_resource",
        points=int(round(pontos["new_resource"] * multiplicador)),
        reason=(
            f"primeiro acesso de {event.employee_id} a {recurso.name!r} "
            f"({recurso.sensitivity.value})"
        ),
    )


def _origem_nova(
    event: Event, baseline: Baseline, catalog: Catalog, pontos
) -> RuleHit | None:
    faixa = catalog.range_of(event.ip_address)
    if faixa is None or faixa.range_id in baseline.ranges:
        return None

    return RuleHit(
        rule="new_origin",
        points=pontos["new_origin"],
        reason=f"origem em {faixa.city} ({faixa.kind.value}), nova para a pessoa",
    )


def _dispositivo_novo(event: Event, baseline: Baseline, pontos) -> RuleHit | None:
    if event.device_id in baseline.devices:
        return None

    return RuleHit(
        rule="new_device",
        points=pontos["new_device"],
        reason=f"dispositivo {event.device_id} nao aparece no padrao da pessoa",
    )


def _agregados(
    janela: tuple[Event, ...],
    rotulo: str,
    baseline: Baseline,
    catalog: Catalog,
    parametros,
    pontos,
) -> list[RuleHit]:
    """Volume, falhas e mistura de sigilo numa janela."""
    teto = parametros["deviation_cap"]
    fracao = parametros["volume_floor_fraction"]
    piso = parametros["volume_absolute_floor"]
    achados: list[RuleHit] = []

    desvio = baseline.daily_volume.deviation(
        len(janela), cap=teto, floor_fraction=fracao, absolute_floor=piso
    )
    ganho = _pontos(pontos["volume"], desvio, teto)
    if ganho:
        achados.append(
            RuleHit(
                rule="volume",
                points=ganho,
                reason=(
                    f"{len(janela)} eventos {rotulo}, contra mediana de "
                    f"{baseline.daily_volume.median:.0f} por dia"
                ),
            )
        )

    falhas = sum(
        1
        for e in janela
        if e.event_type is EventType.LOGIN and e.result is EventResult.FAILURE
    )
    desvio = baseline.daily_failures.deviation(
        falhas, cap=teto, floor_fraction=fracao, absolute_floor=piso
    )
    ganho = _pontos(pontos["failures"], desvio, teto)
    if ganho:
        achados.append(
            RuleHit(
                rule="failures",
                points=ganho,
                reason=(
                    f"{falhas} falhas de autenticacao {rotulo}, contra mediana de "
                    f"{baseline.daily_failures.median:.0f} por dia"
                ),
            )
        )

    sensiveis = sum(
        1
        for e in janela
        if e.resource_id is not None
        and catalog.resource(e.resource_id).sensitivity in SENSIVEIS
    )
    # Proporcao precisa de denominador. Com um evento na janela, a mistura e
    # sempre 0% ou 100%, e um unico acesso sigiloso num dia tranquilo apareceria
    # como divergencia maxima — falso positivo garantido, e dos caros.
    minimo = parametros["min_window_events_for_mix"]
    proporcao = sensiveis / len(janela) if janela else 0.0
    distancia = proporcao - baseline.sensitive_share
    if len(janela) >= minimo and distancia > 0:
        # A distancia e proporcao, nao desvio robusto: ela vale de 0 a 1, e o
        # teto dela e o proprio 1. Por isso entra normalizada por 1, e nao pelo
        # teto de desvio.
        ganho = _pontos(pontos["sensitive_mix"], distancia, 1.0)
        if ganho:
            achados.append(
                RuleHit(
                    rule="sensitive_mix",
                    points=ganho,
                    reason=(
                        f"{proporcao:.0%} dos eventos {rotulo} em recurso sigiloso, "
                        f"contra {baseline.sensitive_share:.0%} no padrao"
                    ),
                )
            )

    return achados


def score_d2(
    event: Event,
    recent: tuple[Event, ...],
    baseline: Baseline,
    catalog: Catalog,
    config: Configuration,
) -> DimensionScore:
    """Mede o quanto o evento diverge do padrao da propria pessoa.

    Args:
        event: O evento a avaliar.
        recent: Eventos anteriores da mesma conta, incluindo os da sessao e os
            do dia. Em qualquer ordem; o recorte das duas janelas e feito aqui.
        baseline: O padrao daquele funcionario, da janela de treino.
        catalog: Funcionarios, recursos e faixas de rede.
        config: Um preset que ligue a dimensao `d2`.

    Returns:
        A nota da D2, com as regras que a formaram.

    Raises:
        ConfigurationError: Se a configuracao nao ligar a dimensao `d2`.
        ValueError: Se `recent` trouxer evento de outra conta, evento posterior
            ao avaliado, ou se o padrao for de outro funcionario.
    """
    if not config.enables("d2"):
        raise ConfigurationError(f"a configuracao {config.name} nao liga a dimensao d2")

    if baseline.employee_id != event.employee_id:
        raise ValueError(
            f"padrao do funcionario {baseline.employee_id} usado para avaliar "
            f"evento do funcionario {event.employee_id}"
        )

    _confere_janela(event, recent)

    parametros = config.dimension("d2")
    pontos = parametros["points"]
    fuso = ZoneInfo(catalog.employee(event.employee_id).timezone)

    por_evento = [
        _hora_incomum(event, baseline, fuso, parametros, pontos),
        _recurso_novo(event, baseline, catalog, config, pontos),
        _origem_nova(event, baseline, catalog, pontos),
        _dispositivo_novo(event, baseline, pontos),
    ]
    achados = [hit for hit in por_evento if hit is not None]

    dia: date = event.occurred_at.astimezone(fuso).date()
    janela_dia = tuple(
        e for e in (*recent, event) if e.occurred_at.astimezone(fuso).date() == dia
    )
    janela_sessao = tuple(
        e for e in (*recent, event) if e.session_id == event.session_id
    )

    no_dia = _agregados(janela_dia, "no dia", baseline, catalog, parametros, pontos)
    na_sessao = _agregados(
        janela_sessao, "na sessao", baseline, catalog, parametros, pontos
    )

    # O maior de cada componente, nunca a soma dos dois recortes (D-28).
    por_regra: dict[str, RuleHit] = {}
    for hit in (*no_dia, *na_sessao):
        atual = por_regra.get(hit.rule)
        if atual is None or hit.points > atual.points:
            por_regra[hit.rule] = hit
    achados.extend(por_regra.values())

    return DimensionScore(
        points=sum(hit.points for hit in achados),
        hits=tuple(achados),
    )
