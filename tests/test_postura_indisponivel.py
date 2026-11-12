"""A D-44: a D3 pontua sem a parcela de postura quando falta estado do equipamento.

**Por que este arquivo existe, e por que ele e maior que a mudanca.** Antes de
11/11/2026 o `build_posture` **se recusava** a montar o retrato sem o estado do
equipamento do dia, com a justificativa escrita na propria mensagem: *"sem ele,
atualizacao e antivirus sairiam como se estivessem em ordem"*. A recusa era a
trava.

A **D-44** tirou a trava, porque o gerador escreve estado diario so do notebook
e sem isso a C3 nao executava. O custo declarado da decisao foi este: **abre a
porta para a parcela sumir em silencio.** Estes testes sao o que fica no lugar
da trava — eles medem que a ausencia e *explicita* em quatro lugares:

1. a excecao e **propria**, e qualquer outro erro de montagem continua
   derrubando a execucao;
2. a nota traz `d3_posture` **nulo**, que na coluna significa "nao avaliada", e
   nao zero, que significa "avaliada e sem risco";
3. a decomposicao traz o achado `posture_unavailable`, visivel no painel;
4. contexto incompleto **por descuido** continua sendo recusado — a marca tem de
   ser dita, nao inferida.

O quarto e o que impede a decisao de virar o defeito que ela aceitou correr.
"""

from datetime import UTC, date, datetime

import pytest
from fixtures_eventos import DIURNO, catalogo, evento, rotina

from detection.configuration import ConfigurationError, load_canonical
from detection.d2 import build_baseline
from detection.d3 import MissingEquipmentStateError, Posture, build_posture
from detection.integracao import EvaluationContext, compose
from detection.integracao.composition import POSTURA_INDISPONIVEL
from detection.model import AccountState, DeviceState, Privilege

C3 = load_canonical("C3")
C2 = load_canonical("C2")

TREINO = {"window_start": date(2026, 1, 1), "window_end": date(2026, 3, 31)}
AGORA = datetime(2026, 4, 1, 17, 30, tzinfo=UTC)  # 14h30 em Sao Paulo
DIA_LOCAL = date(2026, 4, 1)


def conta() -> AccountState:
    return AccountState(
        employee_id=DIURNO,
        valid_from=datetime(2025, 1, 1, tzinfo=UTC),
        mfa_enabled=True,
        privilege=Privilege.STANDARD,
    )


def equipamento(**campos) -> DeviceState:
    base = {
        "device_id": 70,
        "state_date": DIA_LOCAL,
        "patch_age_days": 3,
        "antivirus_on": True,
    }
    base.update(campos)
    return DeviceState(**base)


def retrato(**campos) -> Posture:
    base = {
        "as_of": DIA_LOCAL,
        "mfa_enabled": True,
        "privilege": Privilege.STANDARD,
        "patch_age_days": 3,
        "antivirus_on": True,
    }
    base.update(campos)
    return Posture(**base)


def contexto(**campos) -> EvaluationContext:
    """Contexto completo menos o que cada teste quiser tirar.

    O padrao do funcionario entra sempre: a C2 e a C3 ligam a D2, e sem ele a
    composicao recusa **antes** de chegar na D3 — o que faria estes testes
    passarem pelo motivo errado.
    """
    base = {
        "catalog": catalogo(),
        "baseline": build_baseline(
            DIURNO,
            rotina(
                DIURNO,
                primeiro_dia=date(2026, 1, 1),
                dias=30,
                hora_utc=17,
                device_id=70,
            ),
            timezone="America/Sao_Paulo",
            catalog=catalogo(),
            **TREINO,
        ),
    }
    base.update(campos)
    return EvaluationContext(**base)


def test_sem_estado_do_equipamento_a_excecao_e_propria():
    """E `MissingEquipmentStateError`, e nao `ValueError` solto.

    O executor precisa distinguir *este* caso de qualquer outro erro de
    montagem para decidir o que a D-44 manda fazer. Capturar `ValueError`
    generico faria a parcela sumir tambem quando o motivo fosse um defeito.
    """
    with pytest.raises(
        MissingEquipmentStateError, match="nenhum estado do equipamento"
    ):
        build_posture(
            evento(occurred_at=AGORA),
            account_states=[conta()],
            device_states=[],
            catalog=catalogo(),
            config=C3,
            recent=(),
        )


def test_a_excecao_continua_sendo_um_valueerror():
    """Quem ja tratava `ValueError` nao muda de comportamento.

    A excecao nova e **mais especifica**, nao diferente: herdar de `ValueError`
    e o que mantem valendo o contrato anterior de `build_posture`.
    """
    assert issubclass(MissingEquipmentStateError, ValueError)


def test_estado_de_outro_dia_nao_vira_parcela_ausente():
    """O caso vizinho, e o que mais importa separar.

    Equipamento com estado de **outro dia** nao e dado faltando: e insumo
    errado, e continua derrubando. Se esta linha passasse a devolver a excecao
    da D-44, a parcela desapareceria sempre que alguem buscasse o dia errado —
    que e exatamente o defeito que o `build_posture` recusava.
    """
    with pytest.raises(MissingEquipmentStateError):
        build_posture(
            evento(occurred_at=AGORA),
            account_states=[conta()],
            device_states=[equipamento(state_date=date(2026, 3, 31))],
            catalog=catalogo(),
            config=C3,
            recent=(),
        )


def test_a_nota_sai_com_postura_nula_e_conduta_pontuada():
    """`d3_posture` nulo significa "nao avaliada"; zero significaria "sem risco".

    A diferenca nao e estetica: a tabela de ablacao soma colunas, e zero entra
    na media como se tivesse sido medido.
    """
    nota = compose(evento(occurred_at=AGORA), contexto(posture_unavailable=True), C3)

    assert nota.d3_posture is None
    assert nota.d3_conduct is not None
    assert nota.d1 is not None
    assert nota.d2 is not None


def test_a_decomposicao_registra_a_parcela_ausente():
    """O achado vale zero ponto e aparece na decomposicao de toda nota afetada.

    E o que o painel mostra, e o que impede "nota mais baixa" de virar "evento
    menos arriscado" sem explicacao.
    """
    nota = compose(evento(occurred_at=AGORA), contexto(posture_unavailable=True), C3)

    assert "posture_unavailable" in nota.fired
    achado = next(h for h in nota.hits if h.rule == "posture_unavailable")
    assert achado.points == 0
    assert "D-44" in achado.reason
    assert achado == POSTURA_INDISPONIVEL


def test_contexto_incompleto_por_descuido_continua_recusado():
    """Sem a marca, a composicao recusa — e e isso que fica no lugar da trava.

    Se a ausencia do retrato bastasse para pular a parcela, todo chamador que
    esquecesse de montar o retrato produziria nota plausivel e sem a terceira
    dimensao. A marca tem de ser **dita**.
    """
    with pytest.raises(ConfigurationError, match="o retrato de postura"):
        compose(evento(occurred_at=AGORA), contexto(), C3)


def test_retrato_e_marca_juntos_sao_recusados():
    """Os dois ao mesmo tempo nao definem o que pontuar.

    Escolher um deles dentro do `compose` seria adivinhar qual o chamador
    quis — e a nota sairia diferente conforme o lado escolhido, sem nada
    acusar.
    """
    with pytest.raises(ConfigurationError, match="indisponivel"):
        compose(
            evento(occurred_at=AGORA),
            contexto(posture=retrato(), posture_unavailable=True),
            C3,
        )


def test_a_marca_nao_tem_efeito_em_configuracao_sem_d3():
    """Na C2 a D3 esta desligada, e a marca nao inventa achado nenhum.

    Importa porque o executor passa o contexto para todas as configuracoes, e
    um achado de D-44 numa nota de C2 sujaria a comparacao da ablacao.
    """
    nota = compose(
        evento(occurred_at=AGORA),
        contexto(posture_unavailable=True),
        C2,
    )

    assert nota.d3_posture is None
    assert nota.d3_conduct is None
    assert "posture_unavailable" not in nota.fired
