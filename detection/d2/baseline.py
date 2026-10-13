"""O padrao de cada funcionario — o passo 1 do sistema.

A **D-24** diz que a dimensao 2 compara o funcionario com o proprio padrao dos
tres primeiros meses. Este modulo constroi esse padrao a partir de eventos, e
mais nada: nenhuma consulta a banco, nenhum relogio, nenhum estado global.
Entra uma lista de eventos, sai um `Baseline`.

As sete caracteristicas sao as da secao 5 da especificacao. Seis delas moram
aqui; a setima — conduta de higiene — e insumo da D3 e nao da D2.

Duas escolhas de estatistica, as duas da **D-29**:

- **Mediana e MAD, nao media e desvio padrao.** Um unico dia de pico dentro da
  janela de treino inflaria o desvio e mascararia divergencia real pelos nove
  meses seguintes.
- **Piso de dispersao.** Funcionario perfeitamente regular tem MAD zero, e sem
  piso a divisao explode: a D2 alarmaria justamente sobre as pessoas mais
  previsiveis da empresa.

E uma escolha que a D-29 nao fixa e que fica declarada aqui: **dia sem evento
nenhum nao entra na mediana de volume.** Fim de semana de quem nao trabalha em
fim de semana puxaria a mediana para zero, e a partir dai qualquer terca-feira
normal pareceria desvio. Dia com atividade e zero falhas, esse entra — porque a
pessoa estava trabalhando e nao falhou, o que e informacao.
"""

import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from zoneinfo import ZoneInfo

from detection.model import Catalog, Event, EventResult, EventType, Sensitivity

# Poe o MAD na escala de um desvio padrao, para distribuicao normal. E a
# constante usual, e sem ela o "desvio robusto" nao seria comparavel a nada.
ESCALA_MAD = 1.4826

SENSIVEIS = (Sensitivity.CONFIDENTIAL, Sensitivity.RESTRICTED)


@dataclass(frozen=True, slots=True)
class Spread:
    """Mediana e dispersao robusta de uma contagem diaria."""

    median: float
    mad: float

    def divisor(self, *, floor_fraction: float, absolute_floor: float) -> float:
        """O divisor do desvio, com o piso da D-29 aplicado."""
        piso = max(absolute_floor, floor_fraction * self.median)
        return max(self.mad, piso)

    def deviation(
        self,
        value: float,
        *,
        cap: float,
        floor_fraction: float,
        absolute_floor: float,
    ) -> float:
        """Quanto `value` esta acima da mediana, em dispersoes robustas.

        O desvio e **de um lado so**: menos eventos que o habitual nao e risco,
        e contar isso como divergencia encheria a fila de alerta de gente de
        ferias. Limitado ao teto, pela D-29.
        """
        divisor = self.divisor(
            floor_fraction=floor_fraction, absolute_floor=absolute_floor
        )
        return min(max(0.0, (value - self.median) / divisor), cap)


@dataclass(frozen=True, slots=True)
class Baseline:
    """O padrao de um funcionario numa janela de treino.

    Attributes:
        employee_id: De quem e o padrao.
        window_start: Primeiro dia da janela de treino, inclusive.
        window_end: Ultimo dia da janela de treino, inclusive.
        active_days: Dias com pelo menos um evento.
        peer_group: Verdadeiro quando o padrao e do grupo de pares, e nao da
            pessoa. Precisa aparecer no resultado: e limitacao declarada.
        daily_volume: Eventos por dia ativo.
        daily_failures: Falhas de autenticacao por dia ativo.
        hour_share: Proporcao de eventos em cada hora local, 24 posicoes.
        resources: Recursos que a pessoa tocou na janela.
        ranges: Faixas de rede de onde ela veio.
        devices: Dispositivos que ela usou.
        sensitive_share: Proporcao de eventos em recurso confidencial ou
            restrito.
    """

    employee_id: int
    window_start: date
    window_end: date
    active_days: int
    peer_group: bool
    daily_volume: Spread
    daily_failures: Spread
    hour_share: tuple[float, ...]
    resources: frozenset[int]
    ranges: frozenset[int]
    devices: frozenset[int]
    sensitive_share: float


def _spread(valores: list[int]) -> Spread:
    """Mediana e MAD escalado de uma lista de contagens."""
    if not valores:
        return Spread(median=0.0, mad=0.0)

    mediana = float(statistics.median(valores))
    desvios = [abs(valor - mediana) for valor in valores]
    return Spread(median=mediana, mad=float(statistics.median(desvios)) * ESCALA_MAD)


def _dia_local(event: Event, fuso: ZoneInfo) -> date:
    return event.occurred_at.astimezone(fuso).date()


def build_baseline(
    employee_id: int,
    events: tuple[Event, ...],
    *,
    window_start: date,
    window_end: date,
    timezone: str,
    catalog: Catalog,
    peer_group: bool = False,
) -> Baseline:
    """Constroi o padrao de um funcionario a partir dos eventos da janela.

    Args:
        employee_id: De quem e o padrao.
        events: Eventos usados para treinar. Eventos fora da janela sao
            ignorados, e eventos de outra pessoa sao recusados.
        window_start: Primeiro dia da janela, inclusive.
        window_end: Ultimo dia da janela, inclusive.
        timezone: Fuso do funcionario, para o dia e a hora serem os dele.
        catalog: Recursos e faixas de rede, para classificar sigilo e origem.
        peer_group: Marque verdadeiro quando os eventos forem do grupo de
            pares, e nao da pessoa.

    Returns:
        O padrao, pronto para a D2 comparar.

    Raises:
        ValueError: Se algum evento for de outro funcionario — exceto quando
            `peer_group` for verdadeiro, que e o caso em que isso e esperado.
    """
    fuso = ZoneInfo(timezone)

    por_dia: defaultdict[date, int] = defaultdict(int)
    falhas_por_dia: defaultdict[date, int] = defaultdict(int)
    horas: Counter[int] = Counter()
    recursos: set[int] = set()
    faixas: set[int] = set()
    dispositivos: set[int] = set()
    sensiveis = 0
    total = 0

    for event in events:
        if not peer_group and event.employee_id != employee_id:
            raise ValueError(
                f"padrao do funcionario {employee_id} recebeu evento do "
                f"funcionario {event.employee_id}"
            )

        local = event.occurred_at.astimezone(fuso)
        dia = local.date()
        if dia < window_start or dia > window_end:
            continue

        total += 1
        por_dia[dia] += 1
        falhas_por_dia.setdefault(dia, 0)
        horas[local.hour] += 1
        dispositivos.add(event.device_id)

        if event.event_type is EventType.LOGIN and event.result is EventResult.FAILURE:
            falhas_por_dia[dia] += 1

        faixa = catalog.range_of(event.ip_address)
        if faixa is not None:
            faixas.add(faixa.range_id)

        if event.resource_id is not None:
            recursos.add(event.resource_id)
            if catalog.resource(event.resource_id).sensitivity in SENSIVEIS:
                sensiveis += 1

    hour_share = tuple(
        horas.get(hora, 0) / total if total else 0.0 for hora in range(24)
    )

    return Baseline(
        employee_id=employee_id,
        window_start=window_start,
        window_end=window_end,
        active_days=len(por_dia),
        peer_group=peer_group,
        daily_volume=_spread(list(por_dia.values())),
        daily_failures=_spread(list(falhas_por_dia.values())),
        hour_share=hour_share,
        resources=frozenset(recursos),
        ranges=frozenset(faixas),
        devices=frozenset(dispositivos),
        sensitive_share=sensiveis / total if total else 0.0,
    )


def build_baselines(
    events: tuple[Event, ...],
    *,
    window_start: date,
    window_end: date,
    catalog: Catalog,
    min_active_days: int,
) -> dict[int, Baseline]:
    """Constroi o padrao de cada funcionario do catalogo, com a regra do pares.

    Quem tiver menos de `min_active_days` dias com atividade na janela — porque
    foi admitido no meio dela, ou passou boa parte de ferias — **nao recebe
    padrao proprio**: recebe o do grupo de pares, mesmo departamento e mesma
    persona, com `peer_group` verdadeiro. E a regra da **D-29**, e sem ela todo
    funcionario novo viraria alarme no primeiro dia de avaliacao.

    Args:
        events: Eventos da janela de treino, de todos os funcionarios.
        window_start: Primeiro dia da janela, inclusive.
        window_end: Ultimo dia da janela, inclusive.
        catalog: Funcionarios, recursos e faixas de rede.
        min_active_days: Minimo de dias com atividade para ter padrao proprio.

    Returns:
        Um padrao por funcionario do catalogo.
    """
    por_funcionario: defaultdict[int, list[Event]] = defaultdict(list)
    for event in events:
        por_funcionario[event.employee_id].append(event)

    proprios: dict[int, Baseline] = {}
    for employee_id, funcionario in catalog.employees.items():
        proprios[employee_id] = build_baseline(
            employee_id,
            tuple(por_funcionario.get(employee_id, ())),
            window_start=window_start,
            window_end=window_end,
            timezone=funcionario.timezone,
            catalog=catalog,
        )

    sem_historico = [
        employee_id
        for employee_id, baseline in proprios.items()
        if baseline.active_days < min_active_days
    ]
    if not sem_historico:
        return proprios

    # O grupo de pares e departamento mais persona: cargo igual nem sempre
    # significa rotina igual, e e a rotina que a D2 compara. Quem faz plantao no
    # mesmo departamento de quem e diurno tem outro padrao de hora.
    pares: defaultdict[tuple[int, str], list[Event]] = defaultdict(list)
    for employee_id, funcionario in catalog.employees.items():
        if employee_id in sem_historico:
            continue
        chave = (funcionario.department_id, funcionario.persona.value)
        pares[chave].extend(por_funcionario.get(employee_id, ()))

    for employee_id in sem_historico:
        funcionario = catalog.employee(employee_id)
        chave = (funcionario.department_id, funcionario.persona.value)
        proprios[employee_id] = build_baseline(
            employee_id,
            tuple(pares.get(chave, ())),
            window_start=window_start,
            window_end=window_end,
            timezone=funcionario.timezone,
            catalog=catalog,
            peer_group=True,
        )

    return proprios
