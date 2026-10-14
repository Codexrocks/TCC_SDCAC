"""Testes da dimensao 2.

O primeiro teste deste arquivo e o exemplo que a porta de entrada do projeto usa
para explicar o trabalho inteiro: regras fixas "alarmam o plantonista que sempre
entra as 3h, porque nao sabem que ele sempre entra as 3h". Aqui isso deixa de
ser frase e passa a ser verificavel — e e o que a C2 mede contra a C1.
"""

from datetime import UTC, date, datetime, timedelta
from ipaddress import ip_address

import pytest
from fixtures_eventos import (
    DIURNO,
    ERP,
    FOLHA,
    NOVATO,
    PLANTONISTA,
    PORTAL,
    catalogo,
    evento,
    rotina,
)

from detection.c0 import score_c0
from detection.configuration import ConfigurationError, load_canonical
from detection.d1 import score_d1
from detection.d2 import build_baseline, build_baselines, score_d2

C0 = load_canonical("C0")
C1 = load_canonical("C1")
C2 = load_canonical("C2")

JANELA_INICIO = date(2026, 1, 1)
JANELA_FIM = date(2026, 3, 31)
TREINO = {"window_start": JANELA_INICIO, "window_end": JANELA_FIM}

# Um dia da janela de avaliacao, depois do padrao e disjunto dele.
AVALIACAO = datetime(2026, 4, 1, 17, 30, tzinfo=UTC)  # 14:30 em Sao Paulo
MADRUGADA = datetime(2026, 4, 1, 6, 0, tzinfo=UTC)  # 03:00 em Sao Paulo


def padrao_de(employee_id, eventos, **extras):
    return build_baseline(
        employee_id,
        eventos,
        timezone="America/Sao_Paulo",
        catalog=catalogo(),
        **TREINO,
        **extras,
    )


def padrao_diurno(**kwargs):
    return padrao_de(
        DIURNO, rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=30, **kwargs)
    )


# ---------------------------------------------------------------------------
# O exemplo que o projeto inteiro usa
# ---------------------------------------------------------------------------


def test_o_plantonista_das_tres_da_manha():
    """A C0 e a D1 alarmam; a D2 nao.

    O plantonista entra as 3h todos os dias. As regras fixas disparam por
    horario atipico, e a D1 tambem — ela pondera o atributo, mas o limiar dela
    ainda e generico. A D2 e a primeira que sabe que, para aquela pessoa, 3h e
    hora de trabalho.

    Este teste e a reducao de falso positivo que a pergunta de pesquisa alega
    medir. Se ele cair, a C2 perdeu o motivo de existir.
    """
    plantao = rotina(
        PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=30, hora_utc=6, device_id=80
    )
    base = padrao_de(PLANTONISTA, plantao)

    entrada = evento(
        event_id="plantao-1",
        employee_id=PLANTONISTA,
        occurred_at=MADRUGADA,
        device_id=80,
        session_id="plantao-sessao",
    )

    assert score_c0(entrada, catalogo(), C0, ()).points > 0
    assert score_d1(entrada, catalogo(), C1).points > 0
    assert score_d2(entrada, (), base, catalogo(), C2).points == 0


def test_a_mesma_madrugada_e_desvio_para_quem_trabalha_de_dia():
    """Mesmo evento, pessoa diferente, nota diferente.

    E o outro lado do teste anterior: a D2 nao e mais permissiva, e mais
    precisa. Para quem nunca trabalhou de madrugada, a madrugada diverge.
    """
    entrada = evento(
        event_id="diurno-madrugada",
        employee_id=DIURNO,
        occurred_at=MADRUGADA,
        session_id="madrugada",
    )

    nota = score_d2(entrada, (), padrao_diurno(), catalogo(), C2)

    assert "unusual_hour" in nota.fired
    assert nota.points == 20


# ---------------------------------------------------------------------------
# Novidade
# ---------------------------------------------------------------------------


def test_recurso_novo_pesa_mais_quando_o_sigilo_e_alto():
    """A parte "com peso maior quando o recurso e de sigilo alto" da D-29."""
    base = padrao_diurno()

    interno = score_d2(
        evento(event_id="a", resource_id=ERP, occurred_at=AVALIACAO),
        (),
        base,
        catalogo(),
        C2,
    )
    restrito = score_d2(
        evento(event_id="b", resource_id=FOLHA, occurred_at=AVALIACAO),
        (),
        base,
        catalogo(),
        C2,
    )

    assert interno.points == 45  # 30 x 1,5 confidencial
    assert restrito.points == 60  # 30 x 2,0 restrito


def test_recurso_habitual_nao_e_novidade():
    nota = score_d2(
        evento(resource_id=PORTAL, occurred_at=AVALIACAO),
        (),
        padrao_diurno(),
        catalogo(),
        C2,
    )

    assert "new_resource" not in nota.fired


def test_origem_nova_para_a_pessoa_diverge():
    """Diferente da C0: aqui nao importa se a faixa e corporativa.

    Casa e faixa legitima, e ainda assim e novidade para quem sempre veio do
    escritorio. Quem decide se isso e risco e o peso, nao a regra.
    """
    nota = score_d2(
        evento(ip_address=ip_address("10.2.0.9"), occurred_at=AVALIACAO),
        (),
        padrao_diurno(),
        catalogo(),
        C2,
    )

    assert "new_origin" in nota.fired


def test_dispositivo_novo_para_a_pessoa_diverge():
    nota = score_d2(
        evento(device_id=71, occurred_at=AVALIACAO),
        (),
        padrao_diurno(),
        catalogo(),
        C2,
    )

    assert "new_device" in nota.fired


# ---------------------------------------------------------------------------
# Agregados, e o piso que decide se a D2 funciona
# ---------------------------------------------------------------------------


def dia_de(employee_id, quantos, *, sessao="dia-1", inicio=AVALIACAO):
    """Eventos do mesmo dia e da mesma sessao, um por minuto."""
    return tuple(
        evento(
            event_id=f"dia-{i}",
            employee_id=employee_id,
            occurred_at=inicio + timedelta(minutes=i),
            session_id=sessao,
        )
        for i in range(quantos)
    )


def test_um_evento_a_mais_que_o_habitual_nao_vira_alarme():
    """O piso da D-29 em acao, no caminho completo.

    Onze eventos contra mediana de dez, com MAD zero: sem piso o desvio seria
    infinito. Com piso, rende quatro pontos de vinte e cinco — divergencia
    pequena, como deve ser.
    """
    anteriores = dia_de(DIURNO, 10)
    alvo = evento(
        event_id="decimo-primeiro",
        occurred_at=AVALIACAO + timedelta(minutes=10),
        session_id="dia-1",
    )

    nota = score_d2(alvo, anteriores, padrao_diurno(), catalogo(), C2)

    assert nota.points == 4


def test_volume_muito_acima_do_habitual_satura_no_peso():
    setenta = dia_de(DIURNO, 70)
    alvo = setenta[-1]

    nota = score_d2(alvo, setenta[:-1], padrao_diurno(), catalogo(), C2)

    assert "volume" in nota.fired
    assert nota.points == 25  # o peso inteiro, saturado pelo teto


def test_dia_mais_fraco_que_o_habitual_nao_diverge():
    """Menos evento que o normal nao e risco."""
    tres = dia_de(DIURNO, 3)

    nota = score_d2(tres[-1], tres[:-1], padrao_diurno(), catalogo(), C2)

    assert nota.points == 0


def test_rajada_de_falhas_diverge_de_quem_nunca_falha():
    base = padrao_diurno()
    falhas = tuple(
        evento(
            event_id=f"falha-{i}",
            occurred_at=AVALIACAO + timedelta(seconds=10 * i),
            session_id="dia-1",
            resource_id=None,
            event_type=__import__(
                "detection.model", fromlist=["EventType"]
            ).EventType.LOGIN,
            result=__import__(
                "detection.model", fromlist=["EventResult"]
            ).EventResult.FAILURE,
            attributes={"mfa_used": True, "failure_reason": "wrong_password"},
        )
        for i in range(11)
    )

    nota = score_d2(falhas[-1], falhas[:-1], base, catalogo(), C2)

    assert "failures" in nota.fired


def test_mistura_de_sigilo_acima_do_padrao_diverge():
    """Quem nunca abre arquivo sigiloso e passa o dia neles."""
    base = padrao_diurno()  # padrao so com recurso publico
    dia = tuple(
        evento(
            event_id=f"sig-{i}",
            occurred_at=AVALIACAO + timedelta(minutes=i),
            session_id="dia-1",
            resource_id=ERP,
        )
        for i in range(5)
    )

    nota = score_d2(dia[-1], dia[:-1], base, catalogo(), C2)

    assert "sensitive_mix" in nota.fired


# ---------------------------------------------------------------------------
# As duas janelas, e a regra do maior
# ---------------------------------------------------------------------------


def test_o_mesmo_desvio_nas_duas_janelas_conta_uma_vez():
    """A D-28 no codigo: o maior dos dois recortes, nunca a soma.

    O dia tem trinta eventos em duas sessoes de quinze. O volume diverge nas
    duas janelas, e a nota traz **um** componente de volume — o do dia, que e o
    maior — e nao dois.
    """
    primeira = dia_de(DIURNO, 15, sessao="manha")
    segunda = tuple(
        evento(
            event_id=f"tarde-{i}",
            occurred_at=AVALIACAO + timedelta(hours=2, minutes=i),
            session_id="tarde",
        )
        for i in range(15)
    )
    alvo = segunda[-1]

    nota = score_d2(alvo, primeira + segunda[:-1], padrao_diurno(), catalogo(), C2)

    volumes = [hit for hit in nota.hits if hit.rule == "volume"]

    assert len(volumes) == 1
    assert "no dia" in volumes[0].reason


def test_a_sessao_pode_ser_o_recorte_que_diverge():
    """Trinta eventos numa sessao so, num dia que tambem tem trinta.

    O dia e a sessao dao o mesmo desvio; o maior empata, e um deles entra. O
    teste existe para garantir que a nota nao dobra quando os dois recortes
    coincidem.
    """
    sessao_unica = dia_de(DIURNO, 30, sessao="unica")
    alvo = sessao_unica[-1]

    nota = score_d2(alvo, sessao_unica[:-1], padrao_diurno(), catalogo(), C2)

    assert len([hit for hit in nota.hits if hit.rule == "volume"]) == 1


# ---------------------------------------------------------------------------
# Recusas
# ---------------------------------------------------------------------------


def test_a_janela_recusa_evento_de_outra_conta():
    de_outro = (evento(event_id="outro", employee_id=PLANTONISTA, device_id=80),)

    with pytest.raises(ValueError, match="funcionario 8"):
        score_d2(evento(), de_outro, padrao_diurno(), catalogo(), C2)


def test_a_janela_recusa_evento_do_futuro():
    """A trava da D-17 no passo 2: a nota nao pode depender do que veio depois."""
    do_futuro = (evento(event_id="futuro", occurred_at=AVALIACAO + timedelta(hours=1)),)

    with pytest.raises(ValueError, match="posterior ao avaliado"):
        score_d2(
            evento(occurred_at=AVALIACAO), do_futuro, padrao_diurno(), catalogo(), C2
        )


def test_padrao_de_outra_pessoa_e_recusado():
    """Erro de carga que, calado, produziria nota sem sentido para todo mundo."""
    plantao = rotina(
        PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=30, hora_utc=6, device_id=80
    )

    with pytest.raises(ValueError, match="padrao do funcionario 8"):
        score_d2(evento(), (), padrao_de(PLANTONISTA, plantao), catalogo(), C2)


def test_configuracao_que_nao_liga_a_d2_e_recusada():
    with pytest.raises(ConfigurationError, match="nao liga a dimensao d2"):
        score_d2(evento(), (), padrao_diurno(), catalogo(), C1)


# ---------------------------------------------------------------------------
# Grupo de pares e decomposicao
# ---------------------------------------------------------------------------


def test_quem_esta_no_grupo_de_pares_e_avaliado_e_marcado():
    """Funcionario novo e avaliado desde o primeiro dia, com a limitacao a vista."""
    diurnos = rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=30)
    novato = rotina(NOVATO, primeiro_dia=JANELA_FIM, dias=1, device_id=90, prefixo="n")

    padroes = build_baselines(
        diurnos + novato, catalog=catalogo(), min_active_days=20, **TREINO
    )
    base = padroes[NOVATO]

    nota = score_d2(
        evento(event_id="novato", employee_id=NOVATO, device_id=90),
        (),
        base,
        catalogo(),
        C2,
    )

    assert base.peer_group is True
    # O dispositivo dele nao esta no padrao dos pares, e isso e esperado: o
    # resultado tem de dizer que o padrao e emprestado.
    assert "new_device" in nota.fired


def test_toda_regra_disparada_explica_o_motivo():
    """Risco decomponivel comeca no motivo de cada regra."""
    nota = score_d2(
        evento(
            event_id="varias",
            occurred_at=MADRUGADA,
            resource_id=FOLHA,
            device_id=71,
            ip_address=ip_address("192.0.2.9"),
        ),
        (),
        padrao_diurno(),
        catalogo(),
        C2,
    )

    assert len(nota.hits) == 4
    for hit in nota.hits:
        assert hit.reason.strip(), f"a regra {hit.rule} disparou sem motivo"
        assert hit.points > 0
