"""Testes da composicao da nota final — as quatro linhas da tabela de ablacao.

Aqui se verifica a frase da Metodologia que diz "um unico codigo executado sob
quatro parametros". Se ela for falsa, o artigo compara coisas diferentes e
chama de ablacao; os testes deste arquivo existem para que isso nao passe em
silencio.

Tres garantias valem mais que as outras:

- **Nulo nao e zero.** Dimensao desligada sai `None`; dimensao ligada que nao
  achou nada sai `0`. Quem le a tabela precisa distinguir "nao avaliada" de
  "avaliada e limpa", e uma coluna de zeros nao distingue.
- **Entrada que falta e erro.** C2 sem padrao e C3 sem retrato param com
  mensagem. Pontuar zero produziria tabela plausivel e sem sentido.
- **As duas parcelas da D3 continuam separadas** depois da composicao, em
  campos proprios, como as colunas do banco (D-25 e D-30).
"""

from datetime import UTC, date, datetime, timedelta
from ipaddress import ip_address

import pytest
from fixtures_eventos import (
    CASA,
    DIURNO,
    FOLHA,
    PLANTONISTA,
    catalogo,
    evento,
    rotina,
)

from detection.configuration import ConfigurationError, load_all_canonical
from detection.d2 import build_baseline
from detection.d3 import Posture, PriorScore
from detection.integracao import EvaluationContext, RiskScore, band_of, compose
from detection.model import Privilege, RiskBand

C0, C1, C2, C3 = load_all_canonical()
PESOS = C3.parameters["integration"]

JANELA_INICIO = date(2026, 1, 1)
JANELA_FIM = date(2026, 3, 31)
TREINO = {"window_start": JANELA_INICIO, "window_end": JANELA_FIM}

AVALIACAO = datetime(2026, 4, 1, 17, 30, tzinfo=UTC)  # 14h30 em Sao Paulo
MADRUGADA = datetime(2026, 4, 1, 6, 0, tzinfo=UTC)  # 03h00 em Sao Paulo
DIA_LOCAL = date(2026, 4, 1)


def padrao_de(employee_id, eventos):
    return build_baseline(
        employee_id,
        eventos,
        timezone="America/Sao_Paulo",
        catalog=catalogo(),
        **TREINO,
    )


def postura(**campos) -> Posture:
    """Postura limpa, no dia do evento avaliado."""
    base = {
        "as_of": DIA_LOCAL,
        "mfa_enabled": True,
        "privilege": Privilege.STANDARD,
        "patch_age_days": 3,
        "antivirus_on": True,
    }
    base.update(campos)
    return Posture(**base)


def contexto(employee_id=DIURNO, *, eventos=None, **campos) -> EvaluationContext:
    """Contexto completo: serve as quatro configuracoes sem remonte."""
    if eventos is None:
        device_id = 80 if employee_id == PLANTONISTA else 70
        hora_utc = 6 if employee_id == PLANTONISTA else 17
        eventos = rotina(
            employee_id,
            primeiro_dia=JANELA_INICIO,
            dias=30,
            hora_utc=hora_utc,
            device_id=device_id,
        )
    base = {
        "catalog": catalogo(),
        "recent": (),
        "baseline": padrao_de(employee_id, eventos),
        "priors": (),
        "posture": postura(),
    }
    base.update(campos)
    return EvaluationContext(**base)


# ---------------------------------------------------------------------------
# As quatro linhas da tabela
# ---------------------------------------------------------------------------


def test_cada_configuracao_preenche_so_as_parcelas_que_liga():
    """Nulo e "nao avaliada"; zero e "avaliada e limpa".

    Se a C1 gravasse zero nas colunas da D2 e da D3, a tabela de resultados
    ficaria indistinguivel de uma execucao da C3 em que nada disparou — e a
    ablacao perderia justamente o que ela mede.
    """
    alvo = evento(occurred_at=AVALIACAO)
    ctx = contexto()

    notas = {c.name: compose(alvo, ctx, c) for c in (C0, C1, C2, C3)}

    assert notas["C0"].c0 is not None
    assert (notas["C0"].d1, notas["C0"].d2, notas["C0"].d3_conduct) == (None,) * 3

    assert notas["C1"].c0 is None
    assert notas["C1"].d1 is not None
    assert notas["C1"].d2 is None

    assert (notas["C2"].d1, notas["C2"].d2) != (None, None)
    assert notas["C2"].d3_conduct is None

    assert notas["C3"].d3_conduct is not None
    assert notas["C3"].d3_posture is not None
    assert notas["C3"].c0 is None


def test_a_linha_de_base_nao_passa_por_peso():
    """A C0 e a soma dos pontos das regras fixas, e nada mais.

    Peso na linha de base seria um botao capaz de mexer no grupo de controle, e
    grupo de controle que alguem ajusta deixa de medir.
    """
    fora_de_hora = evento(occurred_at=MADRUGADA)

    nota = compose(fora_de_hora, contexto(), C0)

    assert nota.c0 > 0
    assert nota.final_raw == nota.c0


def test_a_nota_final_da_c3_usa_os_pesos_do_arquivo():
    """A composicao le o peso, e nao o traz embutido.

    E o que torna a analise de sensibilidade da D-09 possivel sem mexer em
    codigo — e o que faz o hash da configuracao significar algo.
    """
    alvo = evento(occurred_at=MADRUGADA, resource_id=FOLHA)
    ctx = contexto(
        priors=(PriorScore(occurred_at=AVALIACAO - timedelta(days=5), points=120),),
        posture=postura(mfa_enabled=False, antivirus_on=False),
    )

    nota = compose(alvo, ctx, C3)
    esperado = (
        nota.d1 * PESOS["d1"]
        + nota.d2 * PESOS["d2"]
        + nota.d3_conduct * PESOS["d3_conduct"]
        + nota.d3_posture * PESOS["d3_posture"]
    )

    assert nota.d3_posture > 0  # senao o peso de 0,5 nao estaria sendo exercido
    assert nota.final_raw == pytest.approx(round(esperado, 2))


def test_a_postura_entra_com_peso_menor_que_a_conduta():
    """O peso declarado da postura e metade, e a composicao respeita isso.

    Postura e estado, nao acao: tratar "antivirus desligado" com o mesmo peso
    de "a pessoa fez isso" inverteria a leitura do alerta.
    """
    alvo = evento(occurred_at=AVALIACAO)

    so_postura = compose(
        alvo, contexto(posture=postura(mfa_enabled=False)), C3
    ).final_raw

    assert PESOS["d3_posture"] < PESOS["d3_conduct"]
    assert so_postura == pytest.approx(
        compose(alvo, contexto(posture=postura(mfa_enabled=False)), C3).d3_posture
        * PESOS["d3_posture"]
    )


def test_as_duas_parcelas_da_d3_nao_viram_um_campo_so():
    """D-25 e D-30 sobrevivem a composicao.

    Somar as duas num campo e o atalho obvio, e e o que a decisao proibe: o
    alerta de quem acumulou risco e o alerta de quem esta mal configurado pedem
    acoes diferentes, e o total nao diz qual dos dois e.
    """
    alvo = evento(occurred_at=AVALIACAO)
    ctx = contexto(
        priors=(PriorScore(occurred_at=AVALIACAO - timedelta(days=1), points=200),),
        posture=postura(privilege=Privilege.ADMIN),
    )

    nota = compose(alvo, ctx, C3)

    assert nota.d3_conduct > 0
    assert nota.d3_posture > 0
    assert nota.d3_conduct != nota.d3_posture
    assert not hasattr(nota, "d3")


# ---------------------------------------------------------------------------
# Entrada que falta
# ---------------------------------------------------------------------------


def test_c2_sem_padrao_para_com_mensagem():
    """Pontuar zero aqui sairia como "comportamento normal" na tabela."""
    with pytest.raises(ConfigurationError, match="nao trouxe o padrao"):
        compose(
            evento(occurred_at=AVALIACAO),
            EvaluationContext(catalog=catalogo()),
            C2,
        )


def test_c3_sem_retrato_de_postura_para_com_mensagem():
    with pytest.raises(ConfigurationError, match="nao trouxe o retrato"):
        compose(
            evento(occurred_at=AVALIACAO),
            EvaluationContext(
                catalog=catalogo(),
                baseline=padrao_de(
                    DIURNO, rotina(DIURNO, primeiro_dia=JANELA_INICIO, dias=30)
                ),
            ),
            C3,
        )


def test_a_c0_e_a_c1_rodam_sem_padrao_e_sem_retrato():
    """As duas primeiras linhas nao dependem de passado, e e isso que as define.

    Se a C1 passasse a exigir padrao, a comparacao C1 contra C2 deixaria de ser
    "o que o contexto individual acrescenta".
    """
    alvo = evento(occurred_at=MADRUGADA)
    magro = EvaluationContext(catalog=catalogo())

    assert compose(alvo, magro, C0).c0 > 0
    assert compose(alvo, magro, C1).d1 > 0


def test_a_mensagem_diz_qual_configuracao_e_qual_dimensao():
    """Erro que nao diz onde doi vira tentativa e erro de quem executa."""
    with pytest.raises(ConfigurationError, match=r"C2 liga a D2"):
        compose(
            evento(occurred_at=AVALIACAO), EvaluationContext(catalog=catalogo()), C2
        )


# ---------------------------------------------------------------------------
# O que a nota carrega consigo
# ---------------------------------------------------------------------------


def test_a_nota_carrega_a_configuracao_e_o_hash():
    """D-34: quem grava uma execucao sem o hash nao consegue, por falta do valor."""
    nota = compose(evento(occurred_at=AVALIACAO), contexto(), C3)

    assert nota.configuration == "C3"
    assert nota.config_hash == C3.config_hash
    assert nota.event_id == "e-1"


def test_a_nota_junta_os_motivos_de_todas_as_dimensoes():
    """A decomposicao que a usabilidade exige comeca aqui.

    Score sem motivo obriga quem analisa a adivinhar o que o numero quis dizer,
    e a nota final de tres dimensoes e onde isso seria mais caro.
    """
    de_casa = evento(
        occurred_at=MADRUGADA,
        ip_address=ip_address("10.2.0.9"),
        resource_id=FOLHA,
    )
    ctx = contexto(posture=postura(mfa_enabled=False))

    nota = compose(de_casa, ctx, C3)

    assert len(nota.hits) > 3
    assert "mfa_disabled" in nota.fired
    assert all(hit.reason for hit in nota.hits)
    assert CASA  # a faixa de casa existe no catalogo, e o evento veio dela


def test_a_nota_e_imutavel():
    nota = compose(evento(occurred_at=AVALIACAO), contexto(), C1)

    with pytest.raises(AttributeError):
        nota.final_raw = 999


# ---------------------------------------------------------------------------
# Faixas de exibicao
# ---------------------------------------------------------------------------


def test_as_faixas_saem_do_arquivo_e_cobrem_a_escala():
    faixas = C3.parameters["bands"]

    assert band_of(0, C3) is RiskBand.NORMAL
    assert band_of(faixas["normal_max"], C3) is RiskBand.NORMAL
    assert band_of(faixas["normal_max"] + 1, C3) is RiskBand.LOW
    assert band_of(faixas["low_max"] + 1, C3) is RiskBand.MEDIUM
    assert band_of(faixas["medium_max"] + 1, C3) is RiskBand.HIGH
    assert band_of(10_000, C3) is RiskBand.HIGH


def test_a_faixa_nao_limita_o_score_bruto():
    """A avaliacao usa o bruto; a faixa e para a tela (D-14).

    Nota empatada no teto viraria degrau na curva precisao-revocacao, e o degrau
    nao e do detector — e do teto.
    """
    alvo = evento(occurred_at=MADRUGADA, resource_id=FOLHA)
    ctx = contexto(
        priors=tuple(
            PriorScore(occurred_at=MADRUGADA - timedelta(hours=h + 1), points=300)
            for h in range(10)
        ),
        posture=postura(
            mfa_enabled=False, antivirus_on=False, privilege=Privilege.ADMIN
        ),
    )

    nota = compose(alvo, ctx, C3)

    assert nota.band is RiskBand.HIGH
    assert nota.final_raw > 100


def test_evento_limpo_de_quem_tem_rotina_fica_em_normal():
    """O caso comum tem de ser silencioso, ou a fila de alerta e inutil."""
    rotineiro = evento(occurred_at=AVALIACAO, session_id="r-sessao-7-91")

    nota = compose(rotineiro, contexto(), C3)

    assert nota.band is RiskBand.NORMAL
    assert nota.final_raw <= C3.parameters["bands"]["normal_max"]


# ---------------------------------------------------------------------------
# O exemplo do projeto, agora nas quatro linhas
# ---------------------------------------------------------------------------


def test_o_plantonista_das_tres_da_manha_nas_quatro_configuracoes():
    """O falso positivo que a pergunta de pesquisa alega reduzir, fim a fim.

    O plantonista entra as 3h todos os dias. A C0 e a C1 alarmam por horario
    atipico; da C2 em diante o padrao dele entra na conta e a nota cai. E o
    mesmo exemplo do teste da D2, aqui pela nota final — que e o numero que
    chega ao resultado do artigo.
    """
    plantao = rotina(
        PLANTONISTA, primeiro_dia=JANELA_INICIO, dias=30, hora_utc=6, device_id=80
    )
    entrada = evento(
        event_id="plantao-1",
        employee_id=PLANTONISTA,
        occurred_at=MADRUGADA,
        device_id=80,
        session_id="plantao-sessao",
    )
    ctx = contexto(PLANTONISTA, eventos=plantao)

    notas = {c.name: compose(entrada, ctx, c).final_raw for c in (C0, C1, C2, C3)}

    assert notas["C0"] > 0
    assert notas["C1"] > 0
    assert notas["C2"] == notas["C1"]  # a D2 nao acrescentou nada: e a rotina dele
    assert notas["C3"] == notas["C2"]  # postura limpa e sem exposicao anterior


def test_a_mesma_madrugada_pesa_mais_para_quem_trabalha_de_dia():
    """Mesmo evento, pessoa diferente, nota final diferente.

    E a contrapartida do teste anterior: a D2 nao e um desconto geral para
    madrugada, e sim a comparacao com o padrao de cada um. Sem este par, o
    anterior passaria tambem se a D2 so soubesse perdoar.
    """
    entrada_diurno = evento(occurred_at=MADRUGADA, session_id="fora-de-hora")
    entrada_plantao = evento(
        event_id="plantao-2",
        employee_id=PLANTONISTA,
        occurred_at=MADRUGADA,
        device_id=80,
        session_id="plantao-sessao",
    )

    do_diurno = compose(entrada_diurno, contexto(DIURNO), C2).final_raw
    do_plantonista = compose(
        entrada_plantao,
        contexto(
            PLANTONISTA,
            eventos=rotina(
                PLANTONISTA,
                primeiro_dia=JANELA_INICIO,
                dias=30,
                hora_utc=6,
                device_id=80,
            ),
        ),
        C2,
    ).final_raw

    assert do_diurno > do_plantonista


def test_a_nota_espelha_as_colunas_do_banco():
    """Os campos sao os de `sdcac.risk_scores`, e nao uma estrutura paralela.

    Quando o executor gravar, o mapeamento tem de ser direto: campo que existe
    so em memoria e campo que ninguem consegue auditar depois.
    """
    campos = set(RiskScore.__dataclass_fields__)

    assert {
        "event_id",
        "configuration",
        "config_hash",
        "c0",
        "d1",
        "d2",
        "d3_conduct",
        "d3_posture",
        "final_raw",
        "band",
    } <= campos
