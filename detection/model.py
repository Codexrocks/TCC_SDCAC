"""Os tipos do dominio.

Os nomes e os valores aqui sao os mesmos do schema em `database/`. Nao e
coincidencia nem gosto: `tests/test_model.py` compara os enums deste arquivo com
os `CREATE TYPE` do SQL e reprova se os dois divergirem. Valor que existe no
banco e nao existe aqui e evento que o motor nao sabe pontuar.

Tudo e imutavel. O motor pontua eventos; ele nao corrige log.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from types import MappingProxyType
from typing import Any

IpAddress = IPv4Address | IPv6Address
IpNetwork = IPv4Network | IPv6Network


# ---------------------------------------------------------------------------
# Listas fechadas — espelho dos CREATE TYPE do banco `corp`
# ---------------------------------------------------------------------------


class EventType(StrEnum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    FILE_ACCESS = "FILE_ACCESS"
    FILE_DOWNLOAD = "FILE_DOWNLOAD"
    EXTERNAL_DEVICE = "EXTERNAL_DEVICE"
    WEB_BROWSING = "WEB_BROWSING"
    SYSTEM_CONFIG = "SYSTEM_CONFIG"
    PHISHING_SIM = "PHISHING_SIM"


class EventResult(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    BLOCKED = "blocked"


class Sensitivity(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class NetworkKind(StrEnum):
    OFFICE = "office"
    VPN = "vpn"
    HOME = "home"
    EXTERNAL = "external"


class Persona(StrEnum):
    OFFICE_DAYTIME = "office_daytime"
    SHIFT = "shift"
    IT_PRIVILEGED = "it_privileged"
    SALES_TRAVEL = "sales_travel"
    HYBRID = "hybrid"
    MANAGEMENT = "management"


class Privilege(StrEnum):
    STANDARD = "standard"
    ELEVATED = "elevated"
    ADMIN = "admin"


class ResourceKind(StrEnum):
    SYSTEM = "system"
    FILE_SHARE = "file_share"


class RiskBand(StrEnum):
    NORMAL = "normal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ---------------------------------------------------------------------------
# O evento e o catalogo que as regras precisam consultar
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Event:
    """Um evento, no formato do envelope da especificacao.

    `occurred_at` chega sempre com fuso. Horario sem fuso nao da para avaliar:
    a C0 usa o fuso da sede e a D1 usa o fuso do funcionario, e sem fuso as
    duas medem a mesma coisa errada.
    """

    run_id: int
    event_id: str
    employee_id: int
    occurred_at: datetime
    event_type: EventType
    result: EventResult
    ip_address: IpAddress
    device_id: int
    session_id: str
    is_vpn: bool
    resource_id: int | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.occurred_at.tzinfo is None:
            raise ValueError(f"evento {self.event_id}: occurred_at sem fuso horario")


@dataclass(frozen=True, slots=True)
class Employee:
    employee_id: int
    department_id: int
    site_id: int
    persona: Persona
    privilege: Privilege
    timezone: str


class DeviceKind(StrEnum):
    NOTEBOOK = "notebook"
    MOBILE = "mobile"


class DeviceOwnership(StrEnum):
    CORPORATE = "corporate"
    PERSONAL = "personal"


@dataclass(frozen=True, slots=True)
class Device:
    device_id: int
    employee_id: int
    kind: DeviceKind
    ownership: DeviceOwnership


@dataclass(frozen=True, slots=True)
class Resource:
    resource_id: int
    kind: ResourceKind
    name: str
    sensitivity: Sensitivity
    owner_department_id: int | None = None


@dataclass(frozen=True, slots=True)
class NetworkRange:
    range_id: int
    cidr: IpNetwork
    kind: NetworkKind
    country: str
    city: str


class Catalog:
    """O que o motor sabe sobre a organizacao, somente leitura.

    Vem do banco `corp` e nao muda durante a pontuacao. Guardar em dicionario
    comum deixaria uma regra alterar o catalogo por engano e contaminar a
    pontuacao dos eventos seguintes — por isso o `MappingProxyType`.
    """

    __slots__ = ("employees", "resources", "ranges", "devices")

    def __init__(
        self,
        employees: Mapping[int, Employee],
        resources: Mapping[int, Resource],
        ranges: tuple[NetworkRange, ...] = (),
        devices: Mapping[int, Device] | None = None,
    ) -> None:
        self.employees = MappingProxyType(dict(employees))
        self.resources = MappingProxyType(dict(resources))
        self.ranges = tuple(ranges)
        self.devices = MappingProxyType(dict(devices or {}))

    def employee(self, employee_id: int) -> Employee:
        try:
            return self.employees[employee_id]
        except KeyError:
            raise KeyError(f"funcionario {employee_id} nao esta no catalogo") from None

    def resource(self, resource_id: int) -> Resource:
        try:
            return self.resources[resource_id]
        except KeyError:
            raise KeyError(f"recurso {resource_id} nao esta no catalogo") from None

    def device(self, device_id: int) -> Device:
        try:
            return self.devices[device_id]
        except KeyError:
            raise KeyError(f"dispositivo {device_id} nao esta no catalogo") from None

    def ranges_of(self, *kinds: NetworkKind) -> tuple[NetworkRange, ...]:
        return tuple(r for r in self.ranges if r.kind in kinds)

    def range_of(self, address: IpAddress) -> NetworkRange | None:
        """A faixa que contem o endereco, ou None se nenhuma contiver."""
        for faixa in self.ranges:
            if address in faixa.cidr:
                return faixa
        return None


# ---------------------------------------------------------------------------
# O que a pontuacao devolve
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RuleHit:
    """Uma regra que disparou, com o motivo em texto.

    O motivo nao e enfeite: a regra de usabilidade exige que o risco seja
    decomponivel, e a decomposicao comeca aqui. Score sem motivo obriga quem
    analisa a adivinhar o que o numero quis dizer.
    """

    rule: str
    points: int
    reason: str


@dataclass(frozen=True, slots=True)
class DimensionScore:
    """A nota de uma dimensao, com as regras que a formaram."""

    points: int
    hits: tuple[RuleHit, ...] = ()

    @property
    def fired(self) -> tuple[str, ...]:
        return tuple(hit.rule for hit in self.hits)
