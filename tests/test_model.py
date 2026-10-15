"""Testes dos tipos do dominio.

O arquivo existe por um motivo so: **o motor e o banco nao podem discordar sobre
que valores existem.** Um valor que o banco aceita e o motor nao conhece vira
evento sem pontuacao, e nada avisa. O caminho inverso vira carga reprovada no
meio da geracao.

Entao aqui os enums do Python sao comparados com os `CREATE TYPE` do SQL, que
por sua vez ja sao comparados com a especificacao em `tests/test_schema.py`. A
corrente fica fechada: especificacao, banco e codigo dizem a mesma coisa, ou a
suite reprova.
"""

import re
from datetime import UTC, datetime
from ipaddress import ip_address, ip_network
from pathlib import Path

import pytest

from detection.model import (
    Catalog,
    DimensionScore,
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
    RiskBand,
    RuleHit,
    Sensitivity,
)

RAIZ = Path(__file__).resolve().parent.parent
CORP = (RAIZ / "database" / "corp" / "001_schema.sql").read_text(encoding="utf-8")
SDCAC = (RAIZ / "database" / "sdcac" / "001_schema.sql").read_text(encoding="utf-8")


def enum_do_sql(sql: str, nome: str) -> list[str]:
    achado = re.search(rf"CREATE TYPE {nome} AS ENUM \((.*?)\);", sql, re.DOTALL)
    assert achado, f"o tipo {nome} nao existe no SQL"
    return re.findall(r"'([^']+)'", achado.group(1))


# ---------------------------------------------------------------------------
# Os enums do motor sao os do banco
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("classe", "tipo_no_sql", "sql"),
    [
        (EventType, "event_type", CORP),
        (EventResult, "event_result", CORP),
        (Sensitivity, "sensitivity_level", CORP),
        (NetworkKind, "network_kind", CORP),
        (Persona, "persona", CORP),
        (Privilege, "privilege_level", CORP),
        (ResourceKind, "resource_kind", CORP),
        (RiskBand, "risk_band", SDCAC),
    ],
)
def test_enum_do_motor_bate_com_o_do_banco(classe, tipo_no_sql, sql):
    no_motor = [membro.value for membro in classe]
    no_banco = enum_do_sql(sql, tipo_no_sql)

    assert no_motor == no_banco, (
        f"{classe.__name__} tem {no_motor} e o tipo {tipo_no_sql} do banco tem "
        f"{no_banco}"
    )


# ---------------------------------------------------------------------------
# Evento
# ---------------------------------------------------------------------------


def evento_valido(**campos) -> Event:
    base = {
        "run_id": 1,
        "event_id": "e-1",
        "employee_id": 7,
        "occurred_at": datetime(2026, 3, 10, 17, 30, tzinfo=UTC),
        "event_type": EventType.LOGIN,
        "result": EventResult.SUCCESS,
        "ip_address": ip_address("10.0.0.5"),
        "device_id": 70,
        "session_id": "s-1",
        "is_vpn": False,
    }
    base.update(campos)
    return Event(**base)


def test_evento_sem_fuso_horario_e_recusado():
    """Horario sem fuso nao da para avaliar.

    A C0 usa o fuso da sede e a D1 o do funcionario. Um datetime ingenuo faria
    as duas medirem a mesma coisa errada, e o erro passaria calado — por isso a
    recusa e na construcao, e nao na regra.
    """
    with pytest.raises(ValueError, match="sem fuso"):
        evento_valido(occurred_at=datetime(2026, 3, 10, 17, 30))


def test_evento_e_imutavel():
    evento = evento_valido()

    with pytest.raises(AttributeError):
        evento.result = EventResult.FAILURE


# ---------------------------------------------------------------------------
# Catalogo
# ---------------------------------------------------------------------------


def catalogo_simples() -> Catalog:
    return Catalog(
        employees={
            7: Employee(
                7, 1, 1, Persona.HYBRID, Privilege.STANDARD, "America/Sao_Paulo"
            )
        },
        resources={
            3: Resource(3, ResourceKind.SYSTEM, "folha", Sensitivity.RESTRICTED)
        },
        ranges=(
            NetworkRange(
                1, ip_network("10.0.0.0/16"), NetworkKind.OFFICE, "BR", "sede"
            ),
            NetworkRange(2, ip_network("10.1.0.0/16"), NetworkKind.VPN, "BR", "vpn"),
            NetworkRange(
                3, ip_network("192.0.2.0/24"), NetworkKind.EXTERNAL, "BR", "net"
            ),
        ),
    )


def test_catalogo_nao_aceita_alteracao():
    """Regra que altera o catalogo contaminaria os eventos seguintes."""
    catalogo = catalogo_simples()

    with pytest.raises(TypeError):
        catalogo.resources[9] = Resource(
            9, ResourceKind.SYSTEM, "intruso", Sensitivity.PUBLIC
        )


def test_catalogo_explica_o_que_faltou():
    """Erro de carga precisa dizer o que faltou, e nao estourar com KeyError seco."""
    catalogo = catalogo_simples()

    with pytest.raises(KeyError, match="funcionario 99"):
        catalogo.employee(99)

    with pytest.raises(KeyError, match="recurso 99"):
        catalogo.resource(99)


def test_catalogo_filtra_faixas_por_tipo():
    catalogo = catalogo_simples()

    corporativas = catalogo.ranges_of(NetworkKind.OFFICE, NetworkKind.VPN)

    assert [faixa.range_id for faixa in corporativas] == [1, 2]


# ---------------------------------------------------------------------------
# Nota de dimensao
# ---------------------------------------------------------------------------


def test_nota_lista_as_regras_que_dispararam():
    nota = DimensionScore(
        points=60,
        hits=(
            RuleHit("off_hours", 30, "03:17 no fuso da sede"),
            RuleHit("external_origin", 30, "origem fora das faixas"),
        ),
    )

    assert nota.fired == ("off_hours", "external_origin")


def test_nota_vazia_nao_tem_regra():
    assert DimensionScore(points=0).fired == ()
