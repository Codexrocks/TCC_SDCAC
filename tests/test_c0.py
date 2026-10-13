"""Testes da linha de base.

A C0 e o grupo de controle: todo numero do artigo e medido contra ela. Um
defeito aqui nao aparece como erro, aparece como conclusao errada.

O teste que mais importa neste arquivo e o ultimo: ele prova que a C0 continua
igual quando o historico do funcionario muda. Essa e a propriedade que a
Metodologia afirma ao leitor, e e o que faz da C0 um controle em vez de uma
quarta dimensao disfarcada.
"""

from datetime import UTC, datetime, timedelta
from ipaddress import ip_address, ip_network

import pytest

from detection.c0 import external_origin, off_hours, restricted_access, score_c0
from detection.configuration import (
    ConfigurationError,
    load_canonical,
    load_implemented,
)
from detection.model import (
    Catalog,
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


# ---------------------------------------------------------------------------
# Montagem
# ---------------------------------------------------------------------------


def catalogo(**extras) -> Catalog:
    """Catalogo minimo: uma faixa de escritorio, um recurso de cada sigilo."""
    recursos = {
        1: Resource(1, ResourceKind.SYSTEM, "portal interno", Sensitivity.PUBLIC),
        2: Resource(2, ResourceKind.SYSTEM, "erp financeiro", Sensitivity.CONFIDENTIAL),
        3: Resource(
            3, ResourceKind.SYSTEM, "folha de pagamento", Sensitivity.RESTRICTED
        ),
    }
    faixas = (
        NetworkRange(1, ip_network("10.0.0.0/16"), NetworkKind.OFFICE, "BR", "sede"),
        NetworkRange(2, ip_network("10.1.0.0/16"), NetworkKind.VPN, "BR", "vpn"),
        NetworkRange(
            3, ip_network("192.0.2.0/24"), NetworkKind.EXTERNAL, "BR", "internet"
        ),
    )
    return Catalog(
        employees=extras.get("employees", {}),
        resources=extras.get("resources", recursos),
        ranges=extras.get("ranges", faixas),
    )


def evento(**campos) -> Event:
    """Um evento normal: meio da tarde, dentro do escritorio, recurso publico."""
    base = {
        "run_id": 1,
        "event_id": "e-1",
        "employee_id": 7,
        "occurred_at": datetime(2026, 3, 10, 17, 30, tzinfo=UTC),
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
# Horario, no fuso da sede
# ---------------------------------------------------------------------------


def test_evento_em_horario_comercial_nao_dispara():
    # 17:30 UTC sao 14:30 em Sao Paulo.
    assert off_hours(evento(), C0) is None


def test_evento_de_madrugada_dispara():
    # 06:17 UTC sao 03:17 em Sao Paulo.
    hit = off_hours(evento(occurred_at=datetime(2026, 3, 10, 6, 17, tzinfo=UTC)), C0)

    assert hit is not None
    assert hit.rule == "off_hours"
    assert hit.points == 30
    assert "03:17" in hit.reason


def test_a_regra_de_horario_usa_o_fuso_da_sede_e_nao_o_do_funcionario():
    """O caso da D-40: 21:30 em Manaus sao 22:30 em Sao Paulo.

    A C0 dispara, e dispara certo — e justamente o falso positivo legitimo que
    a D1 existe para corrigir. Se este teste passar a falhar, alguem trocou o
    fuso da C0 pelo do funcionario e a comparacao entre C0 e C1 perdeu o
    mecanismo central.
    """
    manaus_21h30 = datetime(2026, 3, 10, 1, 30, tzinfo=UTC)  # 22:30 em Sao Paulo

    hit = off_hours(evento(occurred_at=manaus_21h30), C0)

    assert hit is not None
    assert "22:30" in hit.reason


def test_a_borda_da_janela_e_fechada_no_inicio_e_aberta_no_fim():
    seis_em_ponto = datetime(2026, 3, 10, 9, 0, tzinfo=UTC)  # 06:00 em Sao Paulo
    vinte_e_duas = datetime(2026, 3, 11, 1, 0, tzinfo=UTC)  # 22:00 em Sao Paulo

    assert off_hours(evento(occurred_at=seis_em_ponto), C0) is None
    assert off_hours(evento(occurred_at=vinte_e_duas), C0) is not None


# ---------------------------------------------------------------------------
# Origem
# ---------------------------------------------------------------------------


def test_origem_no_escritorio_nao_dispara():
    assert external_origin(evento(), catalogo(), C0) is None


def test_origem_na_vpn_nao_dispara():
    evento_vpn = evento(ip_address=ip_address("10.1.0.9"), is_vpn=True)

    assert external_origin(evento_vpn, catalogo(), C0) is None


def test_origem_fora_das_faixas_corporativas_dispara():
    hit = external_origin(evento(ip_address=ip_address("192.0.2.10")), catalogo(), C0)

    assert hit is not None
    assert hit.points == 30
    assert "192.0.2.10" in hit.reason


def test_catalogo_sem_faixa_corporativa_falha_alto():
    """Sem faixa cadastrada, todo IP pareceria externo.

    O erro certo e reclamar do catalogo, e nao alarmar sobre a organizacao
    inteira por causa de uma carga incompleta.
    """
    vazio = catalogo(ranges=())

    with pytest.raises(ValueError, match="nenhuma faixa"):
        external_origin(evento(), vazio, C0)


# ---------------------------------------------------------------------------
# Recurso restrito
# ---------------------------------------------------------------------------


def test_acesso_a_recurso_publico_nao_dispara():
    assert restricted_access(evento(resource_id=1), catalogo(), C0) is None


def test_acesso_a_recurso_confidencial_nao_dispara_na_c0():
    """A C0 so olha `restricted`. Peso por nivel de sigilo e da D1."""
    assert restricted_access(evento(resource_id=2), catalogo(), C0) is None


def test_acesso_a_recurso_restrito_dispara():
    hit = restricted_access(evento(resource_id=3), catalogo(), C0)

    assert hit is not None
    assert hit.points == 35
    assert "folha de pagamento" in hit.reason


def test_evento_sem_recurso_nao_dispara():
    assert restricted_access(evento(resource_id=None), catalogo(), C0) is None


def test_sensibilidade_vem_do_catalogo_e_nao_do_evento():
    """Sensibilidade no `attributes` precisa ser ignorada.

    O banco proibe a coluna por restricao; aqui o motor tambem nao a le. Fosse
    diferente, um evento poderia se declarar publico e escapar da regra.
    """
    mentiroso = evento(resource_id=3, attributes={"sensitivity": "public"})

    assert restricted_access(mentiroso, catalogo(), C0) is not None


# ---------------------------------------------------------------------------
# A soma
# ---------------------------------------------------------------------------


def test_evento_normal_soma_zero():
    score = score_c0(evento(), catalogo(), C0)

    assert score.points == 0
    assert score.hits == ()


def test_pontos_se_somam_sem_teto():
    """Tres regras juntas: 30 + 30 + 35, sem teto de 100.

    O teto vive na faixa de exibicao. A avaliacao usa o bruto, porque score
    empatado no teto viraria degrau na curva da D-14.
    """
    pior_caso = evento(
        occurred_at=datetime(2026, 3, 10, 6, 17, tzinfo=UTC),
        ip_address=ip_address("192.0.2.10"),
        resource_id=3,
    )

    score = score_c0(pior_caso, catalogo(), C0)

    assert score.points == 95
    assert set(score.fired) == {"off_hours", "external_origin", "restricted_access"}


def test_configuracao_que_nao_liga_a_c0_e_recusada():
    c1 = load_canonical("C1")

    with pytest.raises(ConfigurationError, match="nao liga a dimensao c0"):
        score_c0(evento(), catalogo(), c1)


# ---------------------------------------------------------------------------
# A invariante que faz da C0 um controle
# ---------------------------------------------------------------------------


def test_a_c0_nao_consulta_o_funcionario():
    """Catalogo sem funcionario nenhum, e a pontuacao sai igual.

    E a forma mais direta de provar o que a Metodologia afirma: a C0 e
    puramente estatica. Se um dia a C0 precisar do funcionario para pontuar,
    este teste quebra — e a quebra e a noticia.
    """
    sem_pessoas = catalogo(employees={})
    com_pessoas = catalogo(
        employees={
            7: Employee(7, 1, 1, Persona.SHIFT, Privilege.ADMIN, "America/Manaus")
        }
    )

    evento_qualquer = evento(occurred_at=datetime(2026, 3, 10, 6, 17, tzinfo=UTC))

    assert (
        score_c0(evento_qualquer, sem_pessoas, C0).points
        == score_c0(evento_qualquer, com_pessoas, C0).points
    )


def test_o_passado_do_funcionario_nao_muda_a_nota_c0():
    """Mesmo evento, histórico diferente, nota igual.

    Aqui o "historico" e simulado do jeito que ele chegaria: uma sequencia de
    eventos anteriores da mesma pessoa. A C0 pontua cada evento isoladamente,
    entao a nota do ultimo nao pode depender dos anteriores.
    """
    catalogo_fixo = catalogo()
    alvo = evento(event_id="alvo", ip_address=ip_address("192.0.2.10"))

    sozinho = score_c0(alvo, catalogo_fixo, C0).points

    anteriores = [
        evento(
            event_id=f"antigo-{i}",
            occurred_at=alvo.occurred_at - timedelta(minutes=i),
            result=EventResult.FAILURE,
            event_type=EventType.LOGIN,
            resource_id=None,
        )
        for i in range(1, 30)
    ]
    for anterior in anteriores:
        score_c0(anterior, catalogo_fixo, C0)

    depois = score_c0(alvo, catalogo_fixo, C0).points

    assert sozinho == depois


def test_as_configuracoes_de_hoje_carregam():
    """C0 e C1 na S7. A D2 e a D3 entram na S8, e ai esta lista cresce."""
    nomes = [c.name for c in load_implemented()]

    assert nomes == ["C0", "C1"]
