"""A ingestao traduz o CSV do gerador, e o que ela traduz nao pode ser chute.

**Por que este arquivo existe.** A ingestao e uma camada de traducao entre dois
vocabularios que nao coincidem — e traducao errada nao estoura: ela entrega
dado plausivel ao motor. Uma persona mapeada para a chave errada produziria
nota errada em 1,9 milhao de eventos sem uma linha de erro.

Os tres desencontros que a traducao resolve estao testados um por um: a
persona, o fuso e o privilegio. Os dois primeiros apareceram **em execucao** —
o fuso derrubou a pontuacao no primeiro evento, com `ZoneInfoNotFoundError`.

Nada aqui importa numpy nem pandas: o CI instala so `pytest pyyaml fastapi
httpx`, e teste que dependa do gerador seria pulado em silencio.
"""

import csv
import json
from pathlib import Path

import pytest

from ingest.corp import FUSOS, PERSONAS, IngestError, converte_run

FUNCIONARIOS = [
    # Fora de ordem alfabetica de proposito: o `department_id` tem de sair da
    # ordem alfabetica, nao da ordem de leitura.
    {
        "employee_id": "2",
        "department": "sales",
        "role": "sales_traveler",
        "manager_id": "",
        "persona": "sales_traveler",
        "privileged": "False",
        "site": "porto_verde",
        "timezone": "UTC-4",
        "hired_at": "2024-03-01",
    },
    {
        "employee_id": "1",
        "department": "it_infra",
        "role": "it_privileged",
        "manager_id": "",
        "persona": "it_privileged",
        "privileged": "True",
        "site": "vila_sede",
        "timezone": "UTC-3",
        "hired_at": "2023-01-01",
    },
]

CONTA = [
    # O funcionario 1 e `admin` (nivel 2); o booleano `privileged` de
    # employees.csv diria apenas "True" para ele e para um `elevated`.
    {
        "run_id": "1",
        "employee_id": "1",
        "valid_from": "2026-01-01T00:00:00Z",
        "valid_to": "",
        "mfa_enabled": "True",
        "privilege_level": "2",
    },
    {
        "run_id": "1",
        "employee_id": "2",
        "valid_from": "2026-01-01T00:00:00Z",
        "valid_to": "",
        "mfa_enabled": "False",
        "privilege_level": "0",
    },
]

EQUIPAMENTOS = [
    # O sentinela do gerador: sem dono, e presente nos eventos de origem externa.
    {
        "device_id": "0",
        "owner_employee_id": "",
        "device_type": "unknown_external",
        "corporate": "False",
    },
    # O `pandas` escreve `1.0` numa coluna de inteiros que tenha um vazio.
    {
        "device_id": "1",
        "owner_employee_id": "1.0",
        "device_type": "notebook",
        "corporate": "True",
    },
    {
        "device_id": "2",
        "owner_employee_id": "2.0",
        "device_type": "personal_phone",
        "corporate": "False",
    },
]

RECURSOS = [
    {
        "resource_id": "1",
        "system": "portal",
        "name": "portal_interno_001",
        "sensitivity": "public",
        "owner_department": "",
    },
    {
        "resource_id": "2",
        "system": "fs_own_sales",
        "name": "arquivos_sales_001",
        "sensitivity": "internal",
        "owner_department": "sales",
    },
]

FAIXAS = [
    {"cidr": "10.10.0.0/16", "type": "office", "country": "XA", "city": "vila_sede"},
    {"cidr": "198.18.0.0/16", "type": "external", "country": "XA", "city": "externo"},
]

EVENTOS = [
    {
        "run_id": "1",
        "event_id": "ev-1",
        "employee_id": "1",
        "occurred_at": "2026-04-01T12:00:00Z",
        "ingested_at": "2026-04-01T12:00:02Z",
        "event_type": "LOGIN",
        "result": "success",
        "ip_address": "10.10.0.5",
        "device_id": "1",
        "session_id": "ses-1",
        "resource_id": "",
        "is_vpn": "False",
        "attributes": '{"mfa_used":true,"failure_reason":null}',
    },
    {
        "run_id": "1",
        "event_id": "ev-2",
        "employee_id": "2",
        "occurred_at": "2026-04-01T13:00:00Z",
        "ingested_at": "2026-04-01T13:00:01Z",
        "event_type": "FILE_DOWNLOAD",
        "result": "success",
        "ip_address": "198.18.0.9",
        "device_id": "0",
        "session_id": "ses-2",
        "resource_id": "2",
        "is_vpn": "False",
        "attributes": '{"size_bytes":1024,"destination":"removable"}',
    },
]

ESTADO_DE_EQUIPAMENTO = [
    {
        "run_id": "1",
        "device_id": "1",
        "date": "2026-04-01",
        "patch_age_days": "3",
        "antivirus_active": "True",
    }
]


def _grava(caminho: Path, linhas: list[dict]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


@pytest.fixture
def gerado(tmp_path: Path) -> Path:
    """Um `run_001/` minimo, no formato que o gerador escreve."""
    corp = tmp_path / "run_001" / "corp"
    _grava(corp / "employees.csv", FUNCIONARIOS)
    _grava(corp / "account_state.csv", CONTA)
    _grava(corp / "devices.csv", EQUIPAMENTOS)
    _grava(corp / "resources.csv", RECURSOS)
    _grava(corp / "network_ranges.csv", FAIXAS)
    _grava(corp / "events.csv", EVENTOS)
    _grava(corp / "device_state_daily.csv", ESTADO_DE_EQUIPAMENTO)
    return tmp_path / "run_001"


def _catalogo(destino: Path) -> dict:
    return json.loads((destino / "corp" / "catalogo.json").read_text(encoding="utf-8"))


def test_as_seis_personas_tem_correspondencia_nos_dois_vocabularios():
    """O gerador e os motores nomeiam as mesmas personas de formas diferentes.

    Nao basta o mapa existir: ele tem de cobrir as seis, e os destinos tem de
    ser valores do `Persona` do modelo. Persona nova em so um dos lados e
    defeito de integracao, nao de formato.
    """
    from detection.model import Persona

    assert len(PERSONAS) == 6
    assert set(PERSONAS.values()) == {p.value for p in Persona}


def test_o_fuso_sai_como_chave_iana_e_nao_como_deslocamento(gerado, tmp_path):
    """`UTC-3` nao e fuso para o `ZoneInfo` — e foi assim que a execucao caiu."""
    from zoneinfo import ZoneInfo

    converte_run(gerado, tmp_path / "dados")
    por_id = {f["employee_id"]: f for f in _catalogo(tmp_path / "dados")["employees"]}

    assert por_id[1]["timezone"] == "America/Sao_Paulo"
    assert por_id[2]["timezone"] == "America/Manaus"
    # O que o motor faz com o valor, feito aqui: se a chave nao existir, isto
    # estoura — que e o erro que a ingestao existe para impedir.
    for funcionario in por_id.values():
        ZoneInfo(funcionario["timezone"])


def test_fuso_sem_correspondencia_e_recusado(gerado, tmp_path):
    """Deslocamento novo precisa de decisao, nao de adivinhacao."""
    linhas = [dict(f) for f in FUNCIONARIOS]
    linhas[0]["timezone"] = "UTC-5"
    _grava(gerado / "corp" / "employees.csv", linhas)

    with pytest.raises(IngestError, match="UTC-5"):
        converte_run(gerado, tmp_path / "dados")


def test_persona_sem_correspondencia_e_recusada(gerado, tmp_path):
    linhas = [dict(f) for f in FUNCIONARIOS]
    linhas[0]["persona"] = "night_owl"
    _grava(gerado / "corp" / "employees.csv", linhas)

    with pytest.raises(IngestError, match="night_owl"):
        converte_run(gerado, tmp_path / "dados")


def test_o_privilegio_sai_do_estado_de_conta_e_nao_do_booleano(gerado, tmp_path):
    """`privileged = True` nao distingue `elevated` de `admin`, e a C0 distingue."""
    converte_run(gerado, tmp_path / "dados")
    por_id = {f["employee_id"]: f for f in _catalogo(tmp_path / "dados")["employees"]}

    assert por_id[1]["privilege"] == "admin"
    assert por_id[2]["privilege"] == "standard"


def test_os_identificadores_saem_da_ordem_alfabetica(gerado, tmp_path):
    """Ordem de leitura mudaria o id quando o gerador trocasse as coortes.

    Dois experimentos deixariam de ser comparaveis sem que nada acusasse — e o
    `department_id` nao aparece em nenhum relatorio para alguem notar.
    """
    converte_run(gerado, tmp_path / "dados")
    mapa = json.loads(
        (tmp_path / "dados" / "corp" / "mapeamento.json").read_text(encoding="utf-8")
    )

    # `it_infra` vem antes de `sales` no alfabeto, e por isso leva o 1 — ainda
    # que `sales` seja a primeira linha do CSV.
    assert mapa["departamentos"] == {"it_infra": 1, "sales": 2}
    assert mapa["sitios"] == {"porto_verde": 1, "vila_sede": 2}


def test_o_equipamento_sem_dono_entra_com_sentinela(gerado, tmp_path):
    """O `device_id = 0` aparece nos eventos e nao pode faltar no catalogo.

    E nao pode ganhar um dono do cadastro: atribuir o equipamento de origem
    externa a alguem seria inventar dado onde o gerador nao tem nenhum.
    """
    converte_run(gerado, tmp_path / "dados")
    por_id = {d["device_id"]: d for d in _catalogo(tmp_path / "dados")["devices"]}

    assert por_id[0]["employee_id"] == 0
    assert por_id[1] == {
        "device_id": 1,
        "employee_id": 1,
        "kind": "notebook",
        "ownership": "corporate",
    }
    # Os dois telefones viram o mesmo `mobile`; a posse e que os separa.
    assert por_id[2]["kind"] == "mobile"
    assert por_id[2]["ownership"] == "personal"


def test_o_recurso_de_compartilhamento_se_distingue_do_sistema(gerado, tmp_path):
    converte_run(gerado, tmp_path / "dados")
    por_id = {r["resource_id"]: r for r in _catalogo(tmp_path / "dados")["resources"]}

    assert por_id[1]["kind"] == "system"
    assert por_id[2]["kind"] == "file_share"
    assert por_id[2]["owner_department_id"] == 2
    assert por_id[1]["owner_department_id"] is None


def test_os_atributos_saem_como_objeto_e_nao_como_texto(gerado, tmp_path):
    """O adaptador faz `dict(linha["attributes"])`.

    Texto passaria: `dict` de uma string de JSON nao estoura — ele estoura ou
    produz lixo, e a regra que le `attributes["size_bytes"]` sairia sem ponto
    nenhum sem nada acusar.
    """
    converte_run(gerado, tmp_path / "dados")
    linhas = (
        (tmp_path / "dados" / "corp" / "eventos.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    eventos = [json.loads(linha) for linha in linhas]

    assert eventos[0]["attributes"] == {"mfa_used": True, "failure_reason": None}
    assert eventos[1]["attributes"]["size_bytes"] == 1024
    # Coluna vazia e `None`, e nao zero: recurso 0 nao existe.
    assert eventos[0]["resource_id"] is None
    assert eventos[1]["resource_id"] == 2


def test_o_que_a_ingestao_escreve_o_adaptador_le(gerado, tmp_path):
    """O teste que importa: o contrato, e nao o formato de cada campo.

    Ele carrega a saida da ingestao pelo `ArquivoStorage` de verdade — o mesmo
    que o executor usa. Campo com nome errado passa nos testes de cima e cai
    aqui.
    """
    from storage.arquivos import ArquivoStorage

    destino = tmp_path / "dados"
    contagem = converte_run(gerado, destino)
    assert contagem == {
        "funcionarios": 2,
        "equipamentos": 3,
        "recursos": 2,
        "faixas": 2,
        "eventos": 2,
    }

    storage = ArquivoStorage(destino)
    catalogo = storage.catalog(run_id=1)
    assert catalogo.employee(1).privilege.value == "admin"
    assert catalogo.employee(2).persona.value == "sales_travel"
    assert len(catalogo.ranges) == 2

    eventos = list(storage.events(run_id=1))
    assert [e.event_id for e in eventos] == ["ev-1", "ev-2"]
    assert eventos[0].occurred_at.tzinfo is not None

    estados = storage.account_states(run_id=1, employee_id=1)
    assert estados[0].mfa_enabled is True
    assert estados[0].privilege.value == "admin"


def test_arquivo_que_falta_e_recusado_com_o_nome_dele(gerado, tmp_path):
    (gerado / "corp" / "resources.csv").unlink()

    with pytest.raises(IngestError, match="resources.csv"):
        converte_run(gerado, tmp_path / "dados")


def test_todo_fuso_declarado_existe_no_banco_iana():
    """O mapa nao serve de nada se a chave de destino nao existir na maquina."""
    from zoneinfo import ZoneInfo

    for chave in FUSOS.values():
        ZoneInfo(chave)
