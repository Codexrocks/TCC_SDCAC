"""Testes da construcao do padrao — o passo 1 do sistema.

Se o padrao sair errado, a D2 erra sem reclamar: ela compara contra ele. Os dois
testes que mais importam aqui sao o do piso de dispersao, que impede o
funcionario mais regular de virar o mais alarmado, e o da janela, que impede o
futuro de entrar no padrao.
"""

from datetime import date, datetime, timedelta

import pytest
from fixtures_eventos import DIURNO, ERP, FOLHA, NOVATO, PLANTONISTA, catalogo, rotina

from detection.d2 import Spread, build_baseline, build_baselines

JANELA_INICIO = date(2026, 1, 1)
JANELA_FIM = date(2026, 3, 31)
TREINO = {"window_start": JANELA_INICIO, "window_end": JANELA_FIM}


def padrao(employee_id=DIURNO, eventos=None, **extras):
    if eventos is None:
        eventos = rotina(employee_id, primeiro_dia=JANELA_INICIO, dias=30)
    return build_baseline(
        employee_id,
        eventos,
        timezone="America/Sao_Paulo",
        catalog=catalogo(),
        **TREINO,
        **extras,
    )


# ---------------------------------------------------------------------------
# Dispersao robusta
# ---------------------------------------------------------------------------


def test_mediana_e_mad_de_uma_contagem_regular():
    base = padrao()

    assert base.active_days == 30
    assert base.daily_volume.median == 10
    assert base.daily_volume.mad == 0  # rotina perfeita: nenhum desvio


def test_o_piso_impede_a_divisao_explodir():
    """O caso que a D-29 existe para evitar.

    Funcionario perfeitamente regular tem MAD zero. Sem piso, o divisor seria
    zero e um evento a mais produziria desvio infinito — a D2 alarmaria
    justamente sobre quem e mais previsivel.
    """
    regular = Spread(median=10.0, mad=0.0)

    divisor = regular.divisor(floor_fraction=0.1, absolute_floor=1.0)

    assert divisor == 1.0  # maximo(1 evento; 10% de 10)
    assert regular.deviation(
        11, cap=6.0, floor_fraction=0.1, absolute_floor=1.0
    ) == pytest.approx(1.0)


def test_o_piso_cresce_com_a_mediana():
    """Dez por cento da mediana, para quem tem volume alto.

    Sem a fracao, um piso fixo de um evento faria dez eventos a mais parecerem
    dez desvios para quem gera mil por dia.
    """
    ocupado = Spread(median=200.0, mad=0.0)

    assert ocupado.divisor(floor_fraction=0.1, absolute_floor=1.0) == 20.0


def test_o_desvio_e_de_um_lado_so():
    """Menos evento que o habitual nao e risco.

    Contar isso como divergencia encheria a fila de alerta de gente de ferias.
    """
    base = Spread(median=10.0, mad=2.0)

    assert base.deviation(3, cap=6.0, floor_fraction=0.1, absolute_floor=1.0) == 0.0


def test_o_desvio_respeita_o_teto():
    """Sem teto, um atributo sozinho domina a nota e os pesos viram enfeite."""
    base = Spread(median=10.0, mad=1.0)

    assert (
        base.deviation(10_000, cap=6.0, floor_fraction=0.1, absolute_floor=1.0) == 6.0
    )


def test_mad_zero_e_mediana_zero_ainda_dao_divisor_util():
    """Falha de autenticacao: a mediana diaria de quem nao falha e zero."""
    sem_falha = Spread(median=0.0, mad=0.0)

    assert sem_falha.divisor(floor_fraction=0.1, absolute_floor=1.0) == 1.0
    assert (
        sem_falha.deviation(11, cap=6.0, floor_fraction=0.1, absolute_floor=1.0) == 6.0
    )


# ---------------------------------------------------------------------------
# As caracteristicas
# ---------------------------------------------------------------------------


def test_a_hora_do_padrao_e_a_hora_local_da_pessoa():
    base = padrao()

    # O turno comeca as 17h UTC, que sao 14h em Sao Paulo, e se espalha dali.
    assert base.hour_share[14] > 0
    assert base.hour_share[22] > 0  # fim do turno, 01h UTC do dia seguinte
    assert base.hour_share[3] == 0.0  # madrugada nao e hora dele
    assert sum(base.hour_share) == pytest.approx(1.0)


def test_o_padrao_guarda_recursos_origens_e_dispositivos():
    base = padrao()

    assert base.resources == frozenset({1})
    assert base.devices == frozenset({70})
    assert base.ranges == frozenset({1})


def test_proporcao_de_sigilo_sai_do_catalogo():
    eventos = rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=10, resource_id=ERP)

    assert padrao(eventos=eventos).sensitive_share == 1.0
    assert padrao().sensitive_share == 0.0


def test_dia_sem_evento_nao_entra_na_mediana():
    """Fim de semana de quem nao trabalha em fim de semana.

    Se o dia vazio entrasse, a mediana cairia para zero e qualquer terca-feira
    normal pareceria desvio.
    """
    duas_semanas = rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=5, por_dia=10)
    depois = rotina(
        DIURNO,
        primeiro_dia=JANELA_INICIO + timedelta(days=10),
        dias=5,
        por_dia=10,
        prefixo="b",
    )

    base = padrao(eventos=duas_semanas + depois)

    assert base.active_days == 10
    assert base.daily_volume.median == 10


def test_falhas_entram_por_dia_ativo():
    eventos = rotina(
        DIURNO, primeiro_dia=JANELA_INICIO, dias=20, por_dia=10, falhas_por_dia=1
    )

    assert padrao(eventos=eventos).daily_failures.median == 1


# ---------------------------------------------------------------------------
# A janela, que e a trava da D-17
# ---------------------------------------------------------------------------


def test_evento_fora_da_janela_de_treino_e_ignorado():
    """A trava da D-17, no passo 1.

    Se a janela de avaliacao entrasse no padrao, o comportamento anomalo entraria
    na definicao do que e normal — e o resultado ficaria bom pelo motivo errado.
    """
    treino = rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=10)
    avaliacao = rotina(
        DIURNO,
        primeiro_dia=date(2026, 6, 1),
        dias=10,
        por_dia=500,
        resource_id=FOLHA,
        prefixo="aval",
    )

    base = padrao(eventos=treino + avaliacao)

    assert base.active_days == 10
    assert base.daily_volume.median == 10
    assert FOLHA not in base.resources


def test_padrao_nao_aceita_evento_de_outra_pessoa():
    de_outro = rotina(PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=5)

    with pytest.raises(ValueError, match="funcionario 8"):
        padrao(DIURNO, eventos=de_outro)


# ---------------------------------------------------------------------------
# Grupo de pares
# ---------------------------------------------------------------------------


def test_quem_nao_tem_historico_cai_no_grupo_de_pares():
    """A regra da D-29, sem a qual todo funcionario novo vira alarme."""
    veteranos = rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=30)
    plantonista = rotina(
        PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=30, hora_utc=6, device_id=80
    )
    recem_chegado = rotina(
        NOVATO,
        primeiro_dia=JANELA_FIM - timedelta(days=2),
        dias=3,
        device_id=90,
        prefixo="n",
    )

    padroes = build_baselines(
        veteranos + plantonista + recem_chegado,
        catalog=catalogo(),
        min_active_days=20,
        **TREINO,
    )

    assert padroes[DIURNO].peer_group is False
    assert padroes[PLANTONISTA].peer_group is False
    assert padroes[NOVATO].peer_group is True


def test_o_grupo_de_pares_e_departamento_mais_persona():
    """Cargo igual nem sempre significa rotina igual, e a D2 compara rotina.

    O novato e administrativo diurno. O padrao de pares dele tem de sair do
    diurno, e nao do plantonista do mesmo departamento — senao a hora de
    trabalho dele viria errada.
    """
    diurno = rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=30, hora_utc=17)
    plantonista = rotina(
        PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=30, hora_utc=6, device_id=80
    )
    novato = rotina(NOVATO, primeiro_dia=JANELA_FIM, dias=1, device_id=90, prefixo="n")

    padroes = build_baselines(
        diurno + plantonista + novato,
        catalog=catalogo(),
        min_active_days=20,
        **TREINO,
    )

    pares = padroes[NOVATO]

    assert pares.hour_share[14] > 0  # turno do diurno, 17h UTC
    assert pares.hour_share[3] == 0.0  # turno do plantonista, 06h UTC


def test_sem_ninguem_sem_historico_ninguem_recebe_padrao_de_pares():
    eventos = (
        rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=30)
        + rotina(PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=30, device_id=80)
        + rotina(NOVATO, primeiro_dia=JANELA_INICIO, dias=30, device_id=90, prefixo="n")
    )

    padroes = build_baselines(eventos, catalog=catalogo(), min_active_days=20, **TREINO)

    assert not any(base.peer_group for base in padroes.values())


def test_funcionario_sem_evento_nenhum_recebe_padrao_vazio_ou_de_pares():
    """Carga incompleta nao pode estourar no meio da avaliacao."""
    padroes = build_baselines(
        rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=30),
        catalog=catalogo(),
        min_active_days=20,
        **TREINO,
    )

    assert padroes[PLANTONISTA].peer_group is True
    assert padroes[PLANTONISTA].active_days >= 0


def test_a_janela_do_padrao_fica_registrada():
    """Quem le o resultado precisa saber de que periodo o padrao saiu."""
    base = padrao()

    assert base.window_start == JANELA_INICIO
    assert base.window_end == JANELA_FIM
    assert base.employee_id == DIURNO


def test_o_padrao_e_imutavel():
    base = padrao()

    with pytest.raises(AttributeError):
        base.active_days = 99


def test_hora_de_quem_trabalha_de_madrugada_e_madrugada():
    """O padrao do plantonista, que e o caso que a D2 existe para acertar."""
    plantao = rotina(
        PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=30, hora_utc=6, device_id=80
    )

    base = build_baseline(
        PLANTONISTA,
        plantao,
        timezone="America/Sao_Paulo",
        catalog=catalogo(),
        **TREINO,
    )

    assert base.hour_share[3] > 0  # 06h UTC, inicio do turno dele
    assert base.hour_share[14] == 0.0  # a tarde do diurno nao e hora dele


def test_datetime_sem_fuso_nao_chega_ate_aqui():
    """O evento recusa na construcao, e o padrao nunca ve datetime ingenuo."""
    from detection.model import Event, EventResult, EventType

    with pytest.raises(ValueError, match="sem fuso"):
        Event(
            run_id=1,
            event_id="x",
            employee_id=DIURNO,
            occurred_at=datetime(2026, 1, 1, 10, 0),
            event_type=EventType.LOGIN,
            result=EventResult.SUCCESS,
            ip_address=__import__("ipaddress").ip_address("10.0.0.1"),
            device_id=70,
            session_id="s",
            is_vpn=False,
        )
