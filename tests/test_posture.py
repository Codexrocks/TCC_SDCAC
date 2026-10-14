"""Testes da derivacao do retrato de postura.

Nao existe tabela de postura: os cinco sinais da **D-30** saem de
`account_state`, de `device_state_daily` e dos eventos. Esta derivacao e
dominio, e nao adaptador — se fosse do adaptador, a nota mudaria com a fonte de
dados em vez de com o comportamento, e os dois adaptadores divergiriam na
primeira correcao feita em so um deles.

O teste que mais importa aqui e o do instante: o estado da conta e lido no
momento exato do evento. Ler o mais recente seria a falha da **D-17** com outra
roupa, e ela nao apareceria em nenhum numero — so num resultado bom demais.
"""

from datetime import UTC, date, datetime, timedelta

import pytest
from fixtures_eventos import DIURNO, PLANTONISTA, catalogo, evento

from detection.configuration import ConfigurationError, load_canonical
from detection.d3 import build_posture
from detection.model import AccountState, DeviceState, EventType, Privilege

C3 = load_canonical("C3")
C0 = load_canonical("C0")
JANELA = C3.dimension("d3")["window_days"]

AGORA = datetime(2026, 4, 1, 17, 30, tzinfo=UTC)  # 14h30 em Sao Paulo
DIA_LOCAL = date(2026, 4, 1)


def conta(**campos) -> AccountState:
    base = {
        "employee_id": DIURNO,
        "valid_from": datetime(2025, 1, 1, tzinfo=UTC),
        "mfa_enabled": True,
        "privilege": Privilege.STANDARD,
    }
    base.update(campos)
    return AccountState(**base)


def equipamento(**campos) -> DeviceState:
    base = {
        "device_id": 70,
        "state_date": DIA_LOCAL,
        "patch_age_days": 3,
        "antivirus_on": True,
    }
    base.update(campos)
    return DeviceState(**base)


def monta(evt=None, *, contas=None, equipamentos=None, recent=(), config=C3):
    return build_posture(
        evt or evento(occurred_at=AGORA),
        account_states=contas if contas is not None else [conta()],
        device_states=equipamentos if equipamentos is not None else [equipamento()],
        recent=recent,
        catalog=catalogo(),
        config=config,
    )


# ---------------------------------------------------------------------------
# O caso simples
# ---------------------------------------------------------------------------


def test_o_retrato_sai_com_a_data_local_do_evento():
    """E a unica data que `score_posture` aceita, e e proposital."""
    assert monta().as_of == DIA_LOCAL


def test_os_dois_sinais_da_conta_vem_do_estado_vigente():
    retrato = monta(contas=[conta(mfa_enabled=False, privilege=Privilege.ADMIN)])

    assert retrato.mfa_enabled is False
    assert retrato.privilege is Privilege.ADMIN


def test_os_dois_sinais_do_equipamento_vem_do_dia():
    retrato = monta(equipamentos=[equipamento(patch_age_days=99, antivirus_on=False)])

    assert retrato.patch_age_days == 99
    assert retrato.antivirus_on is False


def test_sem_nada_na_janela_os_tres_contadores_ficam_em_zero():
    retrato = monta()

    assert retrato.phishing_outcome is None
    assert retrato.removable_uses == 0
    assert retrato.risky_browsing == 0


# ---------------------------------------------------------------------------
# O instante, que e a trava da D-17
# ---------------------------------------------------------------------------


def test_o_estado_lido_e_o_vigente_no_instante_e_nao_o_mais_recente():
    """O caso que a tabela por intervalo existe para resolver.

    A pessoa perdeu o privilegio administrativo as 15h. Um evento das 14h30 tem
    de ser avaliado com o privilegio que ela tinha as 14h30 — ler o estado final
    faria o resultado ficar bom porque o futuro vazou para o passado.
    """
    corte = datetime(2026, 4, 1, 18, 0, tzinfo=UTC)  # 15h00 em Sao Paulo
    historico = [
        conta(
            valid_from=datetime(2025, 1, 1, tzinfo=UTC),
            valid_to=corte,
            privilege=Privilege.ADMIN,
        ),
        conta(valid_from=corte, privilege=Privilege.STANDARD),
    ]

    antes = monta(evento(occurred_at=AGORA), contas=historico)
    depois = monta(evento(occurred_at=corte + timedelta(minutes=1)), contas=historico)

    assert antes.privilege is Privilege.ADMIN
    assert depois.privilege is Privilege.STANDARD


def test_instante_sem_estado_vigente_e_erro_e_nao_o_estado_mais_proximo():
    """Escolher "o mais proximo" esconderia carga incompleta.

    O retrato sairia plausivel e errado, e nada na saida diria que ele foi
    adivinhado.
    """
    so_depois = [conta(valid_from=datetime(2026, 6, 1, tzinfo=UTC))]

    with pytest.raises(ValueError, match="nenhum estado de conta cobre"):
        monta(contas=so_depois)


def test_estado_de_outra_pessoa_e_recusado():
    with pytest.raises(ValueError, match="funcionario 8"):
        monta(contas=[conta(employee_id=PLANTONISTA)])


def test_dia_sem_estado_de_equipamento_e_erro():
    """Sem ele, atualizacao e antivirus sairiam como se estivessem em ordem."""
    with pytest.raises(ValueError, match="nenhum estado do equipamento"):
        monta(equipamentos=[equipamento(state_date=date(2026, 3, 31))])


def test_o_equipamento_procurado_e_o_do_evento():
    """Dois dispositivos no mesmo dia: vale o que gerou o evento."""
    estados = [
        equipamento(device_id=70, patch_age_days=1),
        equipamento(device_id=71, patch_age_days=500),
    ]

    assert monta(equipamentos=estados).patch_age_days == 1
    assert (
        monta(evento(occurred_at=AGORA, device_id=71), equipamentos=estados) is not None
    )
    assert (
        monta(
            evento(occurred_at=AGORA, device_id=71), equipamentos=estados
        ).patch_age_days
        == 500
    )


def test_o_dia_do_equipamento_e_o_dia_local_e_nao_o_em_utc():
    """02h30 UTC de 02/04 ainda sao 23h30 de 01/04 em Sao Paulo.

    Procurar pelo dia em UTC traria o estado errado para todo evento perto da
    meia-noite — e sempre para o mesmo lado.
    """
    virada = evento(occurred_at=datetime(2026, 4, 2, 2, 30, tzinfo=UTC))

    retrato = monta(virada, equipamentos=[equipamento(state_date=DIA_LOCAL)])

    assert retrato.as_of == DIA_LOCAL


# ---------------------------------------------------------------------------
# Os tres sinais que vem dos eventos
# ---------------------------------------------------------------------------


def passado(**campos):
    base = {
        "event_id": "ant-1",
        "occurred_at": AGORA - timedelta(days=1),
        "employee_id": DIURNO,
    }
    base.update(campos)
    return evento(**base)


def test_o_desfecho_e_o_da_ultima_campanha_e_nao_o_pior():
    """Quem clicou e depois reportou corrigiu a conduta.

    Guardar o pior desfecho da janela congelaria a pessoa no erro mais antigo, e
    a parcela de postura deixaria de medir estado.
    """
    campanhas = [
        passado(
            event_id="c-1",
            occurred_at=AGORA - timedelta(days=5),
            event_type=EventType.PHISHING_SIM,
            attributes={"campaign_id": 1, "outcome": "submitted_credentials"},
        ),
        passado(
            event_id="c-2",
            occurred_at=AGORA - timedelta(days=1),
            event_type=EventType.PHISHING_SIM,
            attributes={"campaign_id": 2, "outcome": "reported"},
        ),
    ]

    assert monta(recent=campanhas).phishing_outcome == "reported"


def test_desfecho_fora_da_lista_fechada_e_recusado():
    """Lista fechada que aceita valor de fora deixa de ser lista fechada."""
    invalida = [
        passado(
            event_type=EventType.PHISHING_SIM,
            attributes={"campaign_id": 1, "outcome": "talvez"},
        )
    ]

    with pytest.raises(ValueError, match="fora da lista fechada"):
        monta(recent=invalida)


def test_removivel_e_navegacao_de_risco_contam_na_janela():
    historico = [
        passado(event_id="r-1", event_type=EventType.EXTERNAL_DEVICE),
        passado(event_id="r-2", event_type=EventType.EXTERNAL_DEVICE),
        passado(
            event_id="w-1",
            event_type=EventType.WEB_BROWSING,
            attributes={"category": "cloud_storage"},
        ),
        passado(
            event_id="w-2",
            event_type=EventType.WEB_BROWSING,
            attributes={"category": "noticias"},
        ),
    ]

    retrato = monta(recent=historico)

    assert retrato.removable_uses == 2
    assert retrato.risky_browsing == 1  # "noticias" nao e categoria de risco


def test_evento_fora_da_janela_da_d3_nao_conta():
    velho = [
        passado(
            event_id="r-velho",
            occurred_at=AGORA - timedelta(days=JANELA + 1),
            event_type=EventType.EXTERNAL_DEVICE,
        )
    ]

    assert monta(recent=velho).removable_uses == 0


def test_o_evento_atual_nao_entra_na_propria_postura():
    """Mesma razao da D-18, no outro sinal.

    O uso de removivel do evento sendo avaliado ja pontua na D1. Conta-lo
    tambem na postura seria dupla contagem com outro nome.
    """
    atual = evento(occurred_at=AGORA, event_type=EventType.EXTERNAL_DEVICE)

    retrato = monta(atual, recent=[atual])

    assert retrato.removable_uses == 0


def test_evento_de_outra_pessoa_na_janela_e_ignorado():
    """A postura e da pessoa. Janela por sessao ou por dispositivo mediria equipe."""
    de_outro = [
        passado(
            event_id="o-1",
            employee_id=PLANTONISTA,
            device_id=80,
            event_type=EventType.EXTERNAL_DEVICE,
        )
    ]

    assert monta(recent=de_outro).removable_uses == 0


# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------


def test_nao_se_monta_postura_para_configuracao_que_nao_liga_a_d3():
    """Derivar postura na C0 faria a linha de base deixar de ser linha de base."""
    with pytest.raises(ConfigurationError, match="C0 nao liga a dimensao d3"):
        monta(config=C0)
