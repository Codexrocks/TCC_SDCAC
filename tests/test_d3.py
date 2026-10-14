"""Testes da D3 — exposicao acumulada e postura de seguranca.

A dimensao que e contribuicao original do trabalho, e tambem a que tem mais
maneira de dar errado em silencio. Tres testes aqui valem mais que os outros:

- o que recusa risco anterior do proprio evento avaliado, que e a **D-18** com
  trava em vez de boa vontade;
- o que recusa retrato de postura de outro dia, que e a **D-17** por outro
  caminho — ler o estado final faria o resultado ficar bom pelo motivo errado;
- o que mantem conduta e postura em parcelas separadas, que e a **D-25** e a
  **D-30**. Somar as duas aqui exigiria um peso relativo sem justificativa.
"""

from datetime import UTC, date, datetime, timedelta

import pytest
from fixtures_eventos import DIURNO, PLANTONISTA, catalogo, evento

from detection.configuration import ConfigurationError, load_canonical
from detection.d3 import (
    DESFECHOS_DE_PHISHING,
    Posture,
    PriorScore,
    score_conduct,
    score_d3,
    score_posture,
)
from detection.model import Privilege

C3 = load_canonical("C3")
C0 = load_canonical("C0")
D3 = C3.dimension("d3")
POSTURA = D3["posture"]

# O evento avaliado em quase todos os testes: 01/04/2026, 14h30 em Sao Paulo.
AGORA = datetime(2026, 4, 1, 17, 30, tzinfo=UTC)
DIA_LOCAL = date(2026, 4, 1)


def postura(**campos) -> Posture:
    """Postura limpa: segundo fator ligado, sem privilegio, tudo em dia."""
    base = {
        "as_of": DIA_LOCAL,
        "mfa_enabled": True,
        "privilege": Privilege.STANDARD,
        "patch_age_days": 3,
        "antivirus_on": True,
    }
    base.update(campos)
    return Posture(**base)


def anteriores(*pares: tuple[int, int]) -> tuple[PriorScore, ...]:
    """Risco anterior, em pares (dias atras, pontos)."""
    return tuple(
        PriorScore(occurred_at=AGORA - timedelta(days=dias), points=pontos)
        for dias, pontos in pares
    )


# ---------------------------------------------------------------------------
# Conduta: o risco anterior da pessoa, com decaimento
# ---------------------------------------------------------------------------


def test_quem_nao_tem_passado_nao_tem_exposicao():
    nota = score_conduct(evento(occurred_at=AGORA), (), catalogo(), C3)

    assert nota.points == 0
    assert nota.hits == ()


def test_o_risco_de_ontem_pesa_mais_que_o_da_semana_passada():
    """O decaimento, que e o que distingue exposicao de soma historica.

    Sem ele, quem teve um incidente no inicio da janela carregaria o mesmo peso
    duas semanas depois — e a dimensao mediria passado, nao exposicao atual.
    """
    alvo = evento(occurred_at=AGORA)

    ontem = score_conduct(alvo, anteriores((1, 100)), catalogo(), C3).points
    semana = score_conduct(alvo, anteriores((7, 100)), catalogo(), C3).points

    assert ontem > semana > 0


def test_evento_fora_da_janela_nao_conta():
    """A janela e deslizante, e o que saiu dela saiu de fato."""
    alvo = evento(occurred_at=AGORA)
    janela = D3["window_days"]

    dentro = score_conduct(alvo, anteriores((janela, 300)), catalogo(), C3)
    fora = score_conduct(alvo, anteriores((janela + 1, 300)), catalogo(), C3)

    assert dentro.points > 0
    assert fora.points == 0


def test_a_exposicao_e_normalizada_pela_referencia():
    """Cem pontos na escala significam a referencia declarada, nao "muito"."""
    alvo = evento(occurred_at=AGORA)
    referencia = D3["exposure_reference"]

    # Eventos do mesmo dia, que nao decaem: soma crua igual a referencia.
    hoje = tuple(
        PriorScore(
            occurred_at=AGORA - timedelta(minutes=10 + i), points=referencia // 6
        )
        for i in range(6)
    )

    assert score_conduct(alvo, hoje, catalogo(), C3).points == 100


def test_a_exposicao_tem_teto_de_cem():
    alvo = evento(occurred_at=AGORA)
    muito = tuple(
        PriorScore(occurred_at=AGORA - timedelta(minutes=i + 1), points=500)
        for i in range(50)
    )

    assert score_conduct(alvo, muito, catalogo(), C3).points == 100


def test_o_motivo_da_exposicao_diz_quantos_eventos_e_contra_o_que():
    """Score sem motivo obriga quem analisa a adivinhar o que o numero quis."""
    nota = score_conduct(
        evento(occurred_at=AGORA), anteriores((1, 150)), catalogo(), C3
    )

    (achado,) = nota.hits

    assert achado.rule == "accumulated_exposure"
    assert "1 eventos" in achado.reason
    assert str(D3["exposure_reference"]) in achado.reason


def test_o_evento_atual_nao_entra_na_propria_exposicao():
    """A D-18 como trava, e nao como aviso na documentacao.

    Se o proprio evento entrasse na janela, o peso efetivo dele seria a soma do
    peso dele com o da exposicao, e nenhum dos dois seria interpretavel. A
    funcao recusa em vez de confiar em quem chama.
    """
    alvo = evento(occurred_at=AGORA)
    ele_mesmo = (PriorScore(occurred_at=AGORA, points=40),)

    with pytest.raises(ValueError, match="dupla contagem"):
        score_conduct(alvo, ele_mesmo, catalogo(), C3)


def test_risco_do_futuro_tambem_e_recusado():
    """Mesma trava, do outro lado: a janela nunca ve o que ainda nao houve."""
    alvo = evento(occurred_at=AGORA)
    depois = (PriorScore(occurred_at=AGORA + timedelta(hours=1), points=40),)

    with pytest.raises(ValueError, match="maior ou igual"):
        score_conduct(alvo, depois, catalogo(), C3)


def test_o_dia_do_decaimento_e_o_dia_local_da_pessoa():
    """Decaimento por dia precisa saber onde a pessoa esta.

    Fuso errado desloca o limite do dia e muda em quantos dias um evento
    decaiu — pouco, mas sistematicamente, e para todo mundo fora da sede.
    """
    # 02h30 UTC de 02/04 ainda sao 23h30 de 01/04 em Sao Paulo.
    virada = evento(occurred_at=datetime(2026, 4, 2, 2, 30, tzinfo=UTC))
    mesmo_dia_local = (
        PriorScore(occurred_at=datetime(2026, 4, 1, 18, 0, tzinfo=UTC), points=100),
    )

    nota = score_conduct(virada, mesmo_dia_local, catalogo(), C3)
    sem_decaimento = score_conduct(
        evento(occurred_at=AGORA),
        (PriorScore(occurred_at=AGORA - timedelta(hours=1), points=100),),
        catalogo(),
        C3,
    )

    assert nota.points == sem_decaimento.points


# ---------------------------------------------------------------------------
# Postura: o estado da conta e do equipamento naquele dia
# ---------------------------------------------------------------------------


def test_postura_limpa_nao_pontua():
    nota = score_posture(evento(occurred_at=AGORA), postura(), catalogo(), C3)

    assert nota.points == 0
    assert nota.hits == ()


def test_conta_sem_segundo_fator_pontua():
    nota = score_posture(
        evento(occurred_at=AGORA), postura(mfa_enabled=False), catalogo(), C3
    )

    assert nota.points == POSTURA["mfa_disabled"]
    assert nota.fired == ("mfa_disabled",)


def test_privilegio_administrativo_pontua_e_privilegio_elevado_nao():
    """O peso e do privilegio que da acesso total, nao de qualquer elevacao.

    Elevado sem ser administrador e o cargo de quem aprova — alarmar sobre isso
    encheria a fila com a chefia inteira, todos os dias.
    """
    alvo = evento(occurred_at=AGORA)

    admin = score_posture(alvo, postura(privilege=Privilege.ADMIN), catalogo(), C3)
    elevado = score_posture(alvo, postura(privilege=Privilege.ELEVATED), catalogo(), C3)

    assert admin.points == POSTURA["privilege_admin"]
    assert elevado.points == 0


def test_atualizacao_atrasada_pontua_acima_do_limite_declarado():
    alvo = evento(occurred_at=AGORA)
    limite = POSTURA["patch_age_days_limit"]

    no_limite = score_posture(alvo, postura(patch_age_days=limite), catalogo(), C3)
    atrasado = score_posture(alvo, postura(patch_age_days=limite + 1), catalogo(), C3)

    assert no_limite.points == 0
    assert atrasado.points == POSTURA["patch_overdue"]
    assert str(limite) in atrasado.hits[0].reason


def test_antivirus_desligado_pontua():
    nota = score_posture(
        evento(occurred_at=AGORA), postura(antivirus_on=False), catalogo(), C3
    )

    assert nota.fired == ("antivirus_off",)


def test_entregar_credencial_pesa_mais_que_clicar():
    """A ordem dos desfechos e a fonte da verdade, e nao a lista por acaso.

    Quem reportou a campanha fez o certo e nao pode pontuar; quem ignorou nao
    deu informacao nova; clicar e pior; entregar credencial e o pior caso.
    """
    alvo = evento(occurred_at=AGORA)
    notas = {
        desfecho: score_posture(
            alvo, postura(phishing_outcome=desfecho), catalogo(), C3
        ).points
        for desfecho in DESFECHOS_DE_PHISHING
    }

    assert notas["reported"] == 0
    assert notas["ignored"] == 0
    assert notas["clicked"] == POSTURA["phishing_clicked"]
    assert notas["submitted_credentials"] == POSTURA["phishing_submitted"]
    assert notas["submitted_credentials"] > notas["clicked"]


def test_sem_campanha_na_janela_nao_pontua_nem_a_favor_nem_contra():
    nota = score_posture(
        evento(occurred_at=AGORA), postura(phishing_outcome=None), catalogo(), C3
    )

    assert nota.points == 0


def test_uso_de_removivel_e_navegacao_de_risco_crescem_ate_um_teto():
    """Repeticao pesa, mas nao indefinidamente.

    Sem teto por regra, um unico atributo repetido dominaria a parcela e os
    outros pesos viriam enfeite — a mesma razao da D-29, aqui.
    """
    alvo = evento(occurred_at=AGORA)

    um = score_posture(alvo, postura(removable_uses=1), catalogo(), C3).points
    tres = score_posture(alvo, postura(removable_uses=3), catalogo(), C3).points
    trinta = score_posture(alvo, postura(removable_uses=30), catalogo(), C3).points

    assert um < tres
    assert tres == trinta == POSTURA["removable_use"] * 3

    navegacao = score_posture(alvo, postura(risky_browsing=99), catalogo(), C3).points

    assert navegacao == POSTURA["risky_browsing"] * 4


def test_a_postura_tem_teto_de_cem():
    tudo_errado = postura(
        mfa_enabled=False,
        privilege=Privilege.ADMIN,
        patch_age_days=400,
        antivirus_on=False,
        phishing_outcome="submitted_credentials",
        removable_uses=10,
        risky_browsing=10,
    )

    nota = score_posture(evento(occurred_at=AGORA), tudo_errado, catalogo(), C3)

    assert nota.points == 100
    assert sum(hit.points for hit in nota.hits) > 100  # o teto cortou de fato


def test_retrato_de_outro_dia_e_recusado():
    """A falha da D-17 por outro caminho.

    Ler a postura de hoje para avaliar um evento de marco faria o resultado
    ficar bom porque o futuro vazou para o passado — e sem nenhum sinal na
    saida.
    """
    alvo = evento(occurred_at=AGORA)

    with pytest.raises(ValueError, match="precisa ser o do dia do evento"):
        score_posture(alvo, postura(as_of=date(2026, 3, 31)), catalogo(), C3)


def test_o_dia_do_retrato_e_o_dia_local_da_pessoa():
    """Quem esta em Manaus vira o dia uma hora depois da sede.

    Conferir contra o dia em UTC recusaria retrato correto perto da meia-noite,
    ou aceitaria o errado — nos dois casos por causa do fuso.
    """
    # 02h30 UTC de 02/04 sao 23h30 de 01/04 em Sao Paulo.
    alvo = evento(occurred_at=datetime(2026, 4, 2, 2, 30, tzinfo=UTC))

    assert score_posture(alvo, postura(as_of=DIA_LOCAL), catalogo(), C3).points == 0

    with pytest.raises(ValueError, match="precisa ser o do dia do evento"):
        score_posture(alvo, postura(as_of=date(2026, 4, 2)), catalogo(), C3)


# ---------------------------------------------------------------------------
# As duas parcelas juntas, e separadas
# ---------------------------------------------------------------------------


def test_as_duas_parcelas_saem_separadas():
    """A D-25 e a D-30 em codigo: conduta e postura nunca viram um numero so.

    Guardar so o total esconderia qual das duas causou o alerta, e a pergunta
    "o que fazer a respeito" tem resposta diferente para cada uma: conduta pede
    investigacao, postura pede correcao de configuracao.
    """
    nota = score_d3(
        evento(occurred_at=AGORA),
        anteriores((1, 150)),
        postura(mfa_enabled=False),
        catalogo(),
        C3,
    )

    assert nota.conduct.points > 0
    assert nota.posture.points == POSTURA["mfa_disabled"]
    assert nota.conduct.fired == ("accumulated_exposure",)
    assert nota.posture.fired == ("mfa_disabled",)


def test_a_d3_nao_roda_em_configuracao_que_nao_a_liga():
    """Pontuar a D3 na C0 faria a linha de base deixar de ser linha de base."""
    with pytest.raises(ConfigurationError, match="C0 nao liga a dimensao d3"):
        score_d3(evento(occurred_at=AGORA), (), postura(), catalogo(), C0)


def test_exposicao_alta_nao_contamina_a_postura_e_vice_versa():
    """Independencia das parcelas, que e o que justifica reportar as duas."""
    alvo = evento(occurred_at=AGORA)

    so_conduta = score_d3(alvo, anteriores((1, 300)), postura(), catalogo(), C3)
    so_postura = score_d3(alvo, (), postura(antivirus_on=False), catalogo(), C3)

    assert so_conduta.conduct.points > 0
    assert so_conduta.posture.points == 0
    assert so_postura.posture.points > 0
    assert so_postura.conduct.points == 0


def test_a_exposicao_e_da_pessoa_e_nao_da_equipe():
    """Quem chama passa a janela de uma pessoa, e a D3 nao busca nada sozinha.

    O teste e barato e guarda um engano caro: janela montada por sessao, ou por
    dispositivo, somaria risco de colega e a D3 passaria a medir equipe.
    """
    alvo = evento(employee_id=PLANTONISTA, device_id=80, occurred_at=AGORA)

    nota = score_d3(alvo, (), postura(), catalogo(), C3)

    assert nota.conduct.points == 0
    assert alvo.employee_id != DIURNO
