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

from detection.c0 import (
    brute_force,
    external_origin,
    off_hours,
    restricted_access,
    score_c0,
)
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

# Instante de referencia das rajadas: 14:30 em Sao Paulo, dentro do horario
# comercial, para a janela de falhas ser a unica regra a disparar.
INSTANTE = datetime(2026, 3, 10, 17, 30, tzinfo=UTC)


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
    score = score_c0(evento(), catalogo(), C0, ())

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

    score = score_c0(pior_caso, catalogo(), C0, ())

    assert score.points == 95
    assert set(score.fired) == {"off_hours", "external_origin", "restricted_access"}


def test_configuracao_que_nao_liga_a_c0_e_recusada():
    c1 = load_canonical("C1")

    with pytest.raises(ConfigurationError, match="nao liga a dimensao c0"):
        score_c0(evento(), catalogo(), c1, ())


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
        score_c0(evento_qualquer, sem_pessoas, C0, ()).points
        == score_c0(evento_qualquer, com_pessoas, C0, ()).points
    )


def falha(segundos_antes: int, *, employee_id: int = 7, sufixo: str = "") -> Event:
    """Uma falha de autenticacao, `segundos_antes` do instante de referencia."""
    return evento(
        event_id=f"falha-{segundos_antes}{sufixo}",
        employee_id=employee_id,
        occurred_at=INSTANTE - timedelta(seconds=segundos_antes),
        event_type=EventType.LOGIN,
        result=EventResult.FAILURE,
        resource_id=None,
        attributes={"mfa_used": False, "failure_reason": "wrong_password"},
    )


def test_falhas_abaixo_do_limite_nao_disparam():
    """Dez falhas e o limite; o limite nao e ultrapassado por igualdade."""
    anteriores = tuple(falha(s) for s in range(10, 100, 10))  # nove anteriores
    alvo = falha(0)

    assert len(anteriores) == 9
    assert brute_force(alvo, anteriores, C0) is None


def test_falhas_acima_do_limite_disparam():
    anteriores = tuple(falha(s) for s in range(5, 55, 5))  # dez anteriores
    alvo = falha(0)

    hit = brute_force(alvo, anteriores, C0)

    assert hit is not None
    assert hit.rule == "brute_force"
    assert hit.points == 40
    assert "11 falhas" in hit.reason


def test_falha_fora_da_janela_nao_conta():
    """A memoria da C0 e de dois minutos, e nao do dia inteiro.

    Vinte falhas espalhadas por uma hora nao disparam; e o que separa uma
    rajada de alguem que erra a senha de vez em quando. Quem enxerga a
    recorrencia ao longo do dia e a D3.
    """
    espalhadas = tuple(falha(s) for s in range(180, 180 * 21, 180))
    alvo = falha(0)

    assert len(espalhadas) == 20
    assert brute_force(alvo, espalhadas, C0) is None


def test_sucesso_depois_da_rajada_nao_dispara():
    """A regra e sobre falha de autenticacao, na forma literal da D-31.

    Login bem-sucedido logo depois de uma rajada e sequencia, e sequencia e o
    que a D2 avalia. Esticar a C0 para cobrir isso seria dar contexto ao grupo
    de controle.
    """
    rajada = tuple(falha(s) for s in range(5, 55, 5))
    sucesso = evento(
        event_id="entrou",
        event_type=EventType.LOGIN,
        result=EventResult.SUCCESS,
        resource_id=None,
    )

    assert brute_force(sucesso, rajada, C0) is None


def test_a_janela_recusa_evento_de_outra_conta():
    """Mistura de contas inflaria a contagem e alarmaria o inocente."""
    de_outro = (falha(10, employee_id=8, sufixo="-b"),)

    with pytest.raises(ValueError, match="funcionario 8"):
        brute_force(falha(0), de_outro, C0)


def test_a_janela_recusa_evento_do_futuro():
    """Nao olhar para o futuro, verificado na fronteira.

    Com evento posterior na janela, a nota de um evento passado passaria a
    depender do que veio depois — a falha da D-17, por outro caminho.
    """
    do_futuro = (falha(-30),)

    with pytest.raises(ValueError, match="posterior ao avaliado"):
        brute_force(falha(0), do_futuro, C0)


def test_a_janela_vale_igual_para_qualquer_conta():
    """O que a D-42 chama de "sem parametro aprendido", em teste.

    Duas pessoas diferentes, com a mesma sequencia de falhas, recebem a mesma
    nota. A C0 nao estima nada de ninguem: o limiar e o mesmo para as 250.
    """
    rajada_de_sete = tuple(falha(s, employee_id=7) for s in range(5, 55, 5))
    rajada_de_oito = tuple(
        falha(s, employee_id=8, sufixo="-b") for s in range(5, 55, 5)
    )

    nota_sete = brute_force(falha(0, employee_id=7), rajada_de_sete, C0)
    nota_oito = brute_force(falha(0, employee_id=8, sufixo="-b"), rajada_de_oito, C0)

    assert nota_sete is not None and nota_oito is not None
    assert nota_sete.points == nota_oito.points


def test_so_a_janela_de_dois_minutos_muda_a_nota_c0():
    """A invariante da C0, na forma que a D-42 deixou.

    "Embaralhar o historico nao muda nota nenhuma" deixou de ser verdade com a
    janela ligada, e a formulacao honesta e esta: a nota da C0 depende apenas do
    evento, do cadastro e dos dois minutos anteriores da propria conta. Nada
    mais antigo que isso entra, e nada de outra pessoa entra.
    """
    catalogo_fixo = catalogo()
    alvo = falha(0)

    sem_passado = score_c0(alvo, catalogo_fixo, C0, ()).points

    passado_antigo = tuple(falha(s) for s in range(300, 300 * 31, 300))
    com_passado_antigo = score_c0(alvo, catalogo_fixo, C0, passado_antigo).points

    dentro_da_janela = tuple(falha(s) for s in range(5, 55, 5))
    com_rajada = score_c0(alvo, catalogo_fixo, C0, dentro_da_janela).points

    assert com_passado_antigo == sem_passado
    assert com_rajada == sem_passado + 40


def test_as_configuracoes_de_hoje_carregam():
    """C0 e C1 na S7. A D2 e a D3 entram na S8, e ai esta lista cresce."""
    nomes = [c.name for c in load_implemented()]

    assert nomes == ["C0", "C1"]
