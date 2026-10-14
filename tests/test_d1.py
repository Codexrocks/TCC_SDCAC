"""Testes da dimensao 1.

A D1 e a primeira linha de ganho da tabela de ablacao: ela mede o que atributos
mais ricos acrescentam sobre a mesma logica pontual da C0. Dois testes aqui
valem mais que os outros:

- o de Manaus, que prova o mecanismo da **D-40** — a C0 alarma e a D1 nao;
- o da invariante, que prova que a D1 tambem nao olha o passado do funcionario.
"""

from datetime import UTC, datetime, timedelta
from ipaddress import ip_address, ip_network

import pytest

from detection.c0 import score_c0
from detection.configuration import ConfigurationError, load_canonical
from detection.d1 import score_d1
from detection.model import (
    Catalog,
    Device,
    DeviceKind,
    DeviceOwnership,
    Employee,
    Event,
    EventResult,
    EventType,
    NetworkKind,
    NetworkRange,
    Persona,
    Privilege,
    Resource,
    ResourceKind,
    Sensitivity,
)

C0 = load_canonical("C0")
C1 = load_canonical("C1")

SAO_PAULO = "America/Sao_Paulo"
MANAUS = "America/Manaus"


def catalogo(**extras) -> Catalog:
    funcionarios = {
        7: Employee(7, 1, 1, Persona.HYBRID, Privilege.STANDARD, SAO_PAULO),
        8: Employee(8, 1, 2, Persona.SHIFT, Privilege.STANDARD, MANAUS),
    }
    dispositivos = {
        70: Device(70, 7, DeviceKind.NOTEBOOK, DeviceOwnership.CORPORATE),
        71: Device(71, 7, DeviceKind.MOBILE, DeviceOwnership.PERSONAL),
        80: Device(80, 8, DeviceKind.NOTEBOOK, DeviceOwnership.CORPORATE),
    }
    recursos = {
        1: Resource(1, ResourceKind.SYSTEM, "portal", Sensitivity.PUBLIC),
        2: Resource(2, ResourceKind.SYSTEM, "erp", Sensitivity.CONFIDENTIAL),
        3: Resource(3, ResourceKind.SYSTEM, "folha", Sensitivity.RESTRICTED),
    }
    faixas = (
        NetworkRange(1, ip_network("10.0.0.0/16"), NetworkKind.OFFICE, "BR", "sede"),
        NetworkRange(2, ip_network("10.1.0.0/16"), NetworkKind.VPN, "BR", "vpn"),
        NetworkRange(3, ip_network("10.2.0.0/16"), NetworkKind.HOME, "BR", "casa"),
        NetworkRange(
            4, ip_network("192.0.2.0/24"), NetworkKind.EXTERNAL, "BR", "internet"
        ),
    )
    return Catalog(
        employees=extras.get("employees", funcionarios),
        resources=extras.get("resources", recursos),
        ranges=extras.get("ranges", faixas),
        devices=extras.get("devices", dispositivos),
    )


def evento(**campos) -> Event:
    base = {
        "run_id": 1,
        "event_id": "e-1",
        "employee_id": 7,
        "occurred_at": datetime(2026, 3, 10, 17, 30, tzinfo=UTC),  # 14:30 em SP
        "event_type": EventType.FILE_ACCESS,
        "result": EventResult.SUCCESS,
        "ip_address": ip_address("10.0.0.5"),
        "device_id": 70,
        "session_id": "s-1",
        "is_vpn": False,
        "resource_id": 1,
        "attributes": {"action": "view"},
    }
    base.update(campos)
    return Event(**base)


# ---------------------------------------------------------------------------
# O caso que separa a C0 da C1
# ---------------------------------------------------------------------------


def test_a_c0_alarma_quem_esta_em_manaus_e_a_d1_nao():
    """O mecanismo da D-40, em teste.

    21:30 em Manaus sao 22:30 em Sao Paulo. A C0 usa o fuso da sede e dispara;
    a D1 usa o fuso do funcionario e nao dispara. Esse e o falso positivo
    legitimo que a C1 corrige, e e a reducao de FPR que a pergunta de pesquisa
    alega medir. Se este teste cair, a comparacao entre C0 e C1 perdeu o
    mecanismo central.
    """
    manaus_21h30 = datetime(2026, 3, 11, 1, 30, tzinfo=UTC)
    evento_manaus = evento(employee_id=8, device_id=80, occurred_at=manaus_21h30)

    nota_c0 = score_c0(evento_manaus, catalogo(), C0)
    nota_d1 = score_d1(evento_manaus, catalogo(), C1)

    assert "off_hours" in nota_c0.fired
    assert "off_hours_employee" not in nota_d1.fired


def test_a_d1_alarma_quem_esta_de_madrugada_no_proprio_fuso():
    """A D1 nao e mais permissiva: ela e mais precisa."""
    madrugada_em_sp = datetime(2026, 3, 10, 6, 17, tzinfo=UTC)  # 03:17 em SP

    nota = score_d1(evento(occurred_at=madrugada_em_sp), catalogo(), C1)

    assert "off_hours_employee" in nota.fired
    assert "03:17" in nota.hits[0].reason


# ---------------------------------------------------------------------------
# Peso graduado, que a C0 nao tem
# ---------------------------------------------------------------------------


def test_origem_corporativa_nao_pontua():
    nota = score_d1(evento(), catalogo(), C1)

    assert "network_kind" not in nota.fired


def test_casa_e_internet_pesam_diferente():
    """`home` nao e o mesmo que `external` — e e isso que a C0 nao distingue."""
    de_casa = score_d1(evento(ip_address=ip_address("10.2.0.9")), catalogo(), C1)
    de_fora = score_d1(evento(ip_address=ip_address("192.0.2.9")), catalogo(), C1)

    assert de_casa.points == 10
    assert de_fora.points == 30


def test_endereco_fora_de_toda_faixa_falha_alto():
    """Sem o tipo da faixa, ponderar a origem seria pontuar por suposicao."""
    with pytest.raises(ValueError, match="fora de todas as faixas"):
        score_d1(evento(ip_address=ip_address("203.0.113.7")), catalogo(), C1)


def test_sigilo_pesa_por_nivel():
    publico = score_d1(evento(resource_id=1), catalogo(), C1)
    confidencial = score_d1(evento(resource_id=2), catalogo(), C1)
    restrito = score_d1(evento(resource_id=3), catalogo(), C1)

    assert publico.points == 0
    assert confidencial.points == 20
    assert restrito.points == 35


def test_a_c0_so_ve_o_restrito_e_a_d1_ve_os_quatro_niveis():
    """A diferenca de granularidade entre a linha de base e a D1."""
    confidencial = evento(resource_id=2)

    assert score_c0(confidencial, catalogo(), C0).points == 0
    assert score_d1(confidencial, catalogo(), C1).points == 20


# ---------------------------------------------------------------------------
# Atributos que so a D1 enxerga
# ---------------------------------------------------------------------------


def test_dispositivo_pessoal_pontua():
    nota = score_d1(evento(device_id=71), catalogo(), C1)

    assert "personal_device" in nota.fired
    assert nota.points == 25


def test_login_sem_segundo_fator_pontua():
    login = evento(
        event_type=EventType.LOGIN,
        resource_id=None,
        attributes={"mfa_used": False},
    )

    nota = score_d1(login, catalogo(), C1)

    assert "login_without_mfa" in nota.fired


def test_login_com_segundo_fator_nao_pontua():
    login = evento(
        event_type=EventType.LOGIN, resource_id=None, attributes={"mfa_used": True}
    )

    assert score_d1(login, catalogo(), C1).points == 0


def test_escalada_de_privilegio_pontua_e_troca_de_senha_nao():
    escalada = evento(
        event_type=EventType.SYSTEM_CONFIG,
        resource_id=None,
        attributes={"action_subtype": "privilege_escalation", "initiated_by": "self"},
    )
    troca_de_senha = evento(
        event_type=EventType.SYSTEM_CONFIG,
        resource_id=None,
        attributes={"action_subtype": "password_change", "initiated_by": "self"},
    )

    assert score_d1(escalada, catalogo(), C1).points == 40
    assert score_d1(troca_de_senha, catalogo(), C1).points == 0


def test_download_grande_para_fora_pontua_as_duas_coisas():
    """Volume e destino sao dois riscos, e somam."""
    vazamento = evento(
        event_type=EventType.FILE_DOWNLOAD,
        resource_id=2,
        attributes={"size_bytes": 80_000_000, "destination": "external_storage"},
    )

    nota = score_d1(vazamento, catalogo(), C1)

    assert set(nota.fired) == {"sensitivity", "large_download", "download_to_external"}
    assert nota.points == 20 + 20 + 25


def test_download_pequeno_para_o_disco_local_nao_pontua_volume_nem_destino():
    rotina = evento(
        event_type=EventType.FILE_DOWNLOAD,
        resource_id=1,
        attributes={"size_bytes": 1_024, "destination": "local_disk"},
    )

    assert score_d1(rotina, catalogo(), C1).points == 0


def test_dispositivo_removivel_pontua():
    usb = evento(
        event_type=EventType.EXTERNAL_DEVICE,
        resource_id=None,
        attributes={"device_type": "usb_pendrive", "files_copied_count": 3},
    )

    assert "removable_device" in score_d1(usb, catalogo(), C1).fired


def test_navegacao_corporativa_nao_pontua_e_nuvem_pontua():
    corporativa = evento(
        event_type=EventType.WEB_BROWSING,
        resource_id=None,
        attributes={"domain": "intranet.empresa.example", "category": "corporate"},
    )
    nuvem = evento(
        event_type=EventType.WEB_BROWSING,
        resource_id=None,
        attributes={"domain": "arquivos.nuvem.example", "category": "cloud_storage"},
    )

    assert score_d1(corporativa, catalogo(), C1).points == 0
    assert score_d1(nuvem, catalogo(), C1).points == 10


# ---------------------------------------------------------------------------
# Invariantes
# ---------------------------------------------------------------------------


def test_o_passado_do_funcionario_nao_muda_a_nota_d1():
    """A D1 pontua o evento isolado, como a C0 — com mais atributos.

    Quem olha o passado e a D2, e a diferenca entre as duas e o que a C2 mede.
    """
    catalogo_fixo = catalogo()
    alvo = evento(event_id="alvo", ip_address=ip_address("192.0.2.9"))

    sozinho = score_d1(alvo, catalogo_fixo, C1).points

    for i in range(1, 30):
        score_d1(
            evento(
                event_id=f"antigo-{i}",
                occurred_at=alvo.occurred_at - timedelta(minutes=i),
                event_type=EventType.LOGIN,
                result=EventResult.FAILURE,
                resource_id=None,
                attributes={"mfa_used": False, "failure_reason": "wrong_password"},
            ),
            catalogo_fixo,
            C1,
        )

    assert score_d1(alvo, catalogo_fixo, C1).points == sozinho


def test_configuracao_que_nao_liga_a_d1_e_recusada():
    with pytest.raises(ConfigurationError, match="nao liga a dimensao d1"):
        score_d1(evento(), catalogo(), C0)


def test_toda_regra_disparada_explica_o_motivo():
    """Risco decomponivel comeca no motivo de cada regra, nao no total."""
    pior = evento(
        occurred_at=datetime(2026, 3, 10, 6, 17, tzinfo=UTC),
        ip_address=ip_address("192.0.2.9"),
        device_id=71,
        resource_id=3,
    )

    nota = score_d1(pior, catalogo(), C1)

    assert len(nota.hits) == 4
    for hit in nota.hits:
        assert hit.reason.strip(), f"a regra {hit.rule} disparou sem motivo"
        assert hit.points > 0
