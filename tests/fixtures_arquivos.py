"""Escreve um conjunto de dados no formato do adaptador de arquivo.

**Esta fixture faz o papel do gerador**, que e a frente da S6 e nao existe. Ela
escreve `corp/` — catalogo, eventos e as duas tabelas de estado — e **nunca**
escreve `sdcac/`: quem escreve ali e o executor, e separar as duas coisas aqui e
o que torna visivel quando alguem inverte.

O que ela produz continua sendo rotina regular demais para medir qualquer coisa.
Serve para verificar que as portas fecham de ponta a ponta, e **nenhum numero do
artigo sai daqui**.
"""

import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from fixtures_eventos import (
    DIURNO,
    PLANTONISTA,
    catalogo,
    evento,
    rotina,
)

from detection.model import Catalog, Event

JANELA_INICIO = date(2026, 1, 1)
JANELA_FIM = date(2026, 3, 31)
AVALIACAO_INICIO = date(2026, 4, 1)
AVALIACAO_FIM = date(2026, 4, 3)

# O MESMO numero de eventos por dia nas duas janelas, e isto nao e detalhe. A
# `rotina` espalha os eventos pelas horas do turno dividindo o turno pela
# quantidade: com 6 por dia no treino e 4 na avaliacao, a grade de horas muda, e
# aparecem horas que nao existem no padrao. A D2 marca essas como hora incomum, e
# o teste passa a medir a fixture em vez do motor — defeito que esta familia de
# fixtures ja produziu duas vezes.
POR_DIA = 6


def catalogo_para_dicionario(catalog: Catalog) -> dict[str, object]:
    """Serializa o catalogo como o gerador escreveria."""
    return {
        "employees": [
            {
                "employee_id": f.employee_id,
                "department_id": f.department_id,
                "site_id": f.site_id,
                "persona": f.persona.value,
                "privilege": f.privilege.value,
                "timezone": f.timezone,
            }
            for f in catalog.employees.values()
        ],
        "devices": [
            {
                "device_id": d.device_id,
                "employee_id": d.employee_id,
                "kind": d.kind.value,
                "ownership": d.ownership.value,
            }
            for d in catalog.devices.values()
        ],
        "resources": [
            {
                "resource_id": r.resource_id,
                "kind": r.kind.value,
                "name": r.name,
                "sensitivity": r.sensitivity.value,
                "owner_department_id": r.owner_department_id,
            }
            for r in catalog.resources.values()
        ],
        "ranges": [
            {
                "range_id": f.range_id,
                "cidr": str(f.cidr),
                "kind": f.kind.value,
                "country": f.country,
                "city": f.city,
            }
            for f in catalog.ranges
        ],
    }


def evento_para_linha(event: Event) -> str:
    return json.dumps(
        {
            "run_id": event.run_id,
            "event_id": event.event_id,
            "employee_id": event.employee_id,
            "occurred_at": event.occurred_at.isoformat(),
            "event_type": event.event_type.value,
            "result": event.result.value,
            "ip_address": str(event.ip_address),
            "device_id": event.device_id,
            "session_id": event.session_id,
            "is_vpn": event.is_vpn,
            "resource_id": event.resource_id,
            "attributes": dict(event.attributes),
        },
        ensure_ascii=False,
    )


def eventos_do_experimento() -> tuple[Event, ...]:
    """Treino de 30 dias para duas pessoas, mais tres dias de avaliacao.

    O plantonista entra as 3h durante o treino e durante a avaliacao: e o caso
    que faz a C0 alarmar e a C2 nao, e ele precisa existir nas duas janelas para
    que a comparacao signifique algo.
    """
    dias_de_avaliacao = (AVALIACAO_FIM - AVALIACAO_INICIO).days + 1
    treino = rotina(
        DIURNO, primeiro_dia=JANELA_INICIO, dias=30, por_dia=POR_DIA
    ) + rotina(
        PLANTONISTA,
        primeiro_dia=JANELA_INICIO,
        dias=30,
        por_dia=POR_DIA,
        hora_utc=6,
        device_id=80,
        prefixo="p",
    )
    avaliacao = rotina(
        DIURNO,
        primeiro_dia=AVALIACAO_INICIO,
        dias=dias_de_avaliacao,
        por_dia=POR_DIA,
        prefixo="a",
    ) + rotina(
        PLANTONISTA,
        primeiro_dia=AVALIACAO_INICIO,
        dias=dias_de_avaliacao,
        por_dia=POR_DIA,
        hora_utc=6,
        device_id=80,
        prefixo="ap",
    )
    return treino + avaliacao


def escreve_corp(raiz: Path, eventos: tuple[Event, ...] | None = None) -> Path:
    """Escreve `corp/` inteiro e devolve a raiz.

    Nao cria `sdcac/`: o executor cria, e um teste que ja encontrasse a pasta
    pronta nao perceberia se o executor parasse de criar.
    """
    if eventos is None:
        eventos = eventos_do_experimento()

    corp = raiz / "corp"
    corp.mkdir(parents=True, exist_ok=True)

    (corp / "catalogo.json").write_text(
        json.dumps(catalogo_para_dicionario(catalogo()), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (corp / "eventos.jsonl").write_text(
        "\n".join(evento_para_linha(e) for e in eventos) + "\n", encoding="utf-8"
    )

    # Estado de conta: vigente desde antes de tudo, sem fim. O `valid_to` nulo
    # e o caso comum, e e o que a porta precisa aceitar.
    (corp / "estado-de-conta.json").write_text(
        json.dumps(
            [
                {
                    "run_id": 1,
                    "employee_id": employee_id,
                    "valid_from": datetime(2025, 12, 1, tzinfo=UTC).isoformat(),
                    "valid_to": None,
                    "mfa_enabled": True,
                    "privilege": "standard",
                }
                for employee_id in (DIURNO, PLANTONISTA)
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    # Estado de equipamento: um dia por dispositivo, cobrindo a avaliacao com
    # folga de um dia nas duas pontas por causa de fuso.
    estados = []
    dia = AVALIACAO_INICIO - timedelta(days=1)
    while dia <= AVALIACAO_FIM + timedelta(days=1):
        for device_id in (70, 80):
            estados.append(
                {
                    "run_id": 1,
                    "device_id": device_id,
                    "state_date": dia.isoformat(),
                    "patch_age_days": 3,
                    "antivirus_on": True,
                }
            )
        dia += timedelta(days=1)
    (corp / "estado-de-equipamento.json").write_text(
        json.dumps(estados, indent=2), encoding="utf-8"
    )

    return raiz


def janela_de_avaliacao() -> tuple[datetime, datetime]:
    return (
        datetime.combine(AVALIACAO_INICIO, datetime.min.time(), tzinfo=UTC),
        datetime.combine(AVALIACAO_FIM, datetime.max.time(), tzinfo=UTC),
    )


def um_evento_de_avaliacao(**campos) -> Event:
    """Um evento dentro da janela de avaliacao, para testes pontuais."""
    base = {
        "event_id": "av-1",
        "occurred_at": datetime.combine(
            AVALIACAO_INICIO, datetime.min.time(), tzinfo=UTC
        )
        + timedelta(hours=17, minutes=30),
    }
    base.update(campos)
    return evento(**base)
