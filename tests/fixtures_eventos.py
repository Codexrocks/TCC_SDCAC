"""Fixtures de evento para os testes do motor.

O gerador de eventos e a frente do Filipe, e nao existe ainda. Estas fixtures
**nao sao um substituto dele**: elas produzem rotina regular demais para medir
qualquer coisa, e servem para verificar que o motor faz o que diz. Nenhum numero
do artigo sai daqui.

O que elas garantem e o que os testes precisam: evento com fuso, sessao
coerente, catalogo com recurso e faixa de rede, e um padrao construivel.
"""

from datetime import UTC, date, datetime, timedelta
from ipaddress import ip_address, ip_network

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

SAO_PAULO = "America/Sao_Paulo"
MANAUS = "America/Manaus"

# Identificadores usados pelos testes.
DIURNO = 7
PLANTONISTA = 8
NOVATO = 9

PORTAL = 1
ERP = 2
FOLHA = 3

ESCRITORIO = 1
VPN = 2
CASA = 3
INTERNET = 4


def catalogo(**extras) -> Catalog:
    """Catalogo pequeno, com um funcionario de cada caso dos testes."""
    funcionarios = {
        DIURNO: Employee(
            DIURNO, 1, 1, Persona.OFFICE_DAYTIME, Privilege.STANDARD, SAO_PAULO
        ),
        PLANTONISTA: Employee(
            PLANTONISTA, 1, 1, Persona.SHIFT, Privilege.STANDARD, SAO_PAULO
        ),
        NOVATO: Employee(
            NOVATO, 1, 1, Persona.OFFICE_DAYTIME, Privilege.STANDARD, SAO_PAULO
        ),
    }
    dispositivos = {
        70: Device(70, DIURNO, DeviceKind.NOTEBOOK, DeviceOwnership.CORPORATE),
        71: Device(71, DIURNO, DeviceKind.MOBILE, DeviceOwnership.PERSONAL),
        80: Device(80, PLANTONISTA, DeviceKind.NOTEBOOK, DeviceOwnership.CORPORATE),
        90: Device(90, NOVATO, DeviceKind.NOTEBOOK, DeviceOwnership.CORPORATE),
    }
    recursos = {
        PORTAL: Resource(PORTAL, ResourceKind.SYSTEM, "portal", Sensitivity.PUBLIC),
        ERP: Resource(ERP, ResourceKind.SYSTEM, "erp", Sensitivity.CONFIDENTIAL),
        FOLHA: Resource(FOLHA, ResourceKind.SYSTEM, "folha", Sensitivity.RESTRICTED),
    }
    faixas = (
        NetworkRange(
            ESCRITORIO, ip_network("10.0.0.0/16"), NetworkKind.OFFICE, "BR", "sede"
        ),
        NetworkRange(VPN, ip_network("10.1.0.0/16"), NetworkKind.VPN, "BR", "vpn"),
        NetworkRange(CASA, ip_network("10.2.0.0/16"), NetworkKind.HOME, "BR", "casa"),
        NetworkRange(
            INTERNET, ip_network("192.0.2.0/24"), NetworkKind.EXTERNAL, "BR", "net"
        ),
    )
    return Catalog(
        employees=extras.get("employees", funcionarios),
        resources=extras.get("resources", recursos),
        ranges=extras.get("ranges", faixas),
        devices=extras.get("devices", dispositivos),
    )


def evento(**campos) -> Event:
    """Um evento de acesso comum, no meio da tarde, dentro do escritorio."""
    base = {
        "run_id": 1,
        "event_id": "e-1",
        "employee_id": DIURNO,
        "occurred_at": datetime(2026, 4, 1, 17, 30, tzinfo=UTC),  # 14:30 em SP
        "event_type": EventType.FILE_ACCESS,
        "result": EventResult.SUCCESS,
        "ip_address": ip_address("10.0.0.5"),
        "device_id": 70,
        "session_id": "s-1",
        "is_vpn": False,
        "resource_id": PORTAL,
        "attributes": {"action": "view"},
    }
    base.update(campos)
    return Event(**base)


def rotina(
    employee_id: int,
    *,
    primeiro_dia: date,
    dias: int,
    por_dia: int = 10,
    hora_utc: int = 17,
    device_id: int = 70,
    resource_id: int = PORTAL,
    ip: str = "10.0.0.5",
    falhas_por_dia: int = 0,
    horas_de_turno: int = 9,
    prefixo: str = "r",
) -> tuple[Event, ...]:
    """Rotina regular de um funcionario, espalhada pelo turno dele.

    Serve de janela de treino. Os dias sao consecutivos de proposito: dia sem
    evento nao entra na mediana, e a regularidade aqui e o que torna o piso de
    dispersao da D-29 observavel em teste.

    Os eventos se espalham pelas horas do turno em vez de ficarem todos na mesma
    hora. Com rotina de uma hora so, qualquer evento em outra hora viraria
    divergencia, e os testes mediriam a fixture em vez do motor — foi o que
    aconteceu na primeira versao deste arquivo.
    """
    eventos: list[Event] = []
    for dia in range(dias):
        momento = datetime(
            primeiro_dia.year,
            primeiro_dia.month,
            primeiro_dia.day,
            hora_utc,
            0,
            tzinfo=UTC,
        ) + timedelta(days=dia)
        intervalo = (horas_de_turno * 60) // max(por_dia, 1)
        for i in range(por_dia):
            eventos.append(
                evento(
                    event_id=f"{prefixo}-{employee_id}-{dia}-{i}",
                    employee_id=employee_id,
                    occurred_at=momento + timedelta(minutes=intervalo * i),
                    session_id=f"{prefixo}-sessao-{employee_id}-{dia}",
                    device_id=device_id,
                    resource_id=resource_id,
                    ip_address=ip_address(ip),
                )
            )
        for i in range(falhas_por_dia):
            eventos.append(
                evento(
                    event_id=f"{prefixo}-{employee_id}-{dia}-f{i}",
                    employee_id=employee_id,
                    occurred_at=momento + timedelta(minutes=30 + i),
                    session_id=f"{prefixo}-sessao-{employee_id}-{dia}",
                    device_id=device_id,
                    resource_id=None,
                    ip_address=ip_address(ip),
                    event_type=EventType.LOGIN,
                    result=EventResult.FAILURE,
                    attributes={"mfa_used": True, "failure_reason": "wrong_password"},
                )
            )
    return tuple(eventos)
