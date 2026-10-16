"""Mantem `backend/exemplos.json` honesto — exemplo velho mente pior que exemplo ausente.

O arquivo existe para o painel ser escrito antes de haver dado de verdade: sao as
respostas reais da execucao 4, capturadas da propria API. O risco e conhecido e e
o mesmo que o `docs/cronograma.md` ja produziu uma vez, quando dizia "amanha" dois
dias depois do prazo — **conteudo gravado que ninguem compara com a fonte apodrece
em silencio**. Aqui a fonte e o contrato, e quem compara e este arquivo.

Dois testes rodam sempre, mesmo sem o pydantic instalado: a cobertura das rotas e
a procedencia. Os de validacao pedem o pydantic, e por isso sao pulados quando ele
falta — do mesmo jeito, e pelo mesmo motivo, que os de `test_api.py`.
"""

import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
EXEMPLOS = RAIZ / "backend" / "exemplos.json"
CONTRATO = RAIZ / "backend" / "openapi.json"

# A rota concreta que foi capturada, o molde que ela cumpre no contrato e o
# modelo que valida o corpo. Declarado, e nao deduzido: deduzir o molde a partir
# da rota exigiria adivinhar quais segmentos sao identificadores.
MAPA = (
    ("/api/v1/health", "/api/v1/health", "Saude"),
    ("/api/v1/configurations", "/api/v1/configurations", "list[Configuracao]"),
    ("/api/v1/runs", "/api/v1/runs", "Pagina[Execucao]"),
    ("/api/v1/runs/4", "/api/v1/runs/{scoring_run_id}", "Execucao"),
    (
        "/api/v1/runs/4/metrics",
        "/api/v1/runs/{scoring_run_id}/metrics",
        "Pagina[Metrica]",
    ),
    (
        "/api/v1/runs/4/alerts",
        "/api/v1/runs/{scoring_run_id}/alerts",
        "Pagina[Alerta]",
    ),
    (
        "/api/v1/runs/4/employees",
        "/api/v1/runs/{scoring_run_id}/employees",
        "Pagina[NotaDoFuncionario]",
    ),
    (
        "/api/v1/runs/4/employees/8",
        "/api/v1/runs/{scoring_run_id}/employees/{employee_id}",
        "Pagina[NotaDoEvento]",
    ),
    (
        "/api/v1/runs/4/events/ap-8-2-5",
        "/api/v1/runs/{scoring_run_id}/events/{event_id}",
        "NotaDoEvento",
    ),
    ("/api/v1/runs/999", None, "Erro"),
)


@pytest.fixture(scope="module")
def amostras() -> dict:
    return json.loads(EXEMPLOS.read_text(encoding="utf-8"))


def _modelo(nome: str):
    """Resolve o nome declarado no MAPA no modelo de verdade."""
    from backend import schemas

    if nome.startswith("list["):
        return list[getattr(schemas, nome[5:-1])]
    if nome.startswith("Pagina["):
        return schemas.Pagina[getattr(schemas, nome[7:-1])]
    return getattr(schemas, nome)


def test_toda_rota_do_contrato_tem_exemplo(amostras):
    """Rota nova obriga exemplo novo.

    Sem isto, acrescentar rota ao contrato deixaria o painel sem amostra dela, e
    nada acusaria: o arquivo continuaria valido, so incompleto.
    """
    contrato = json.loads(CONTRATO.read_text(encoding="utf-8"))
    moldes = {molde for _, molde, _ in MAPA if molde}
    assert moldes == set(contrato["paths"]), (
        "exemplos.json e openapi.json discordam sobre quais rotas existem: "
        f"so no contrato {set(contrato['paths']) - moldes}, "
        f"so nos exemplos {moldes - set(contrato['paths'])}"
    )
    capturadas = {r["rota"] for r in amostras["respostas"]}
    assert capturadas == {rota for rota, _, _ in MAPA}


def test_a_procedencia_esta_escrita(amostras):
    """O arquivo diz de onde veio e o que nao cobre.

    A banca vai perguntar se o exemplo e dado real ou invencao. A resposta mora
    no arquivo, nao na memoria de quem o gerou.
    """
    for chave in ("_sobre", "_como_refazer", "_limites"):
        assert amostras[chave].strip(), f"{chave} vazio"
    assert "high" in amostras["_limites"], "o limite da faixa alta precisa estar dito"


@pytest.mark.parametrize(("rota", "nome"), [(r, n) for r, _, n in MAPA])
def test_o_corpo_do_exemplo_cumpre_o_contrato(amostras, rota, nome):
    """Cada corpo capturado ainda valida contra o modelo que o produziu.

    E o teste que pega o exemplo defasado: mudar um campo em `schemas.py` sem
    recapturar as respostas reprova aqui.
    """
    pytest.importorskip("pydantic")
    from pydantic import TypeAdapter

    corpo = next(r["corpo"] for r in amostras["respostas"] if r["rota"] == rota)
    TypeAdapter(_modelo(nome)).validate_python(corpo)


def test_um_corpo_adulterado_e_recusado(amostras):
    """O par do teste acima: provar que a validacao de fato valida.

    Um teste que so afirma "o arquivo passa" nao distingue "esta correto" de "a
    validacao nao olha". Aqui o campo obrigatorio e removido de proposito.
    """
    pytest.importorskip("pydantic")
    from pydantic import TypeAdapter, ValidationError

    corpo = next(
        r["corpo"] for r in amostras["respostas"] if r["rota"] == "/api/v1/runs/4"
    )
    sem_hash = {k: v for k, v in corpo.items() if k != "config_hash"}
    with pytest.raises(ValidationError):
        TypeAdapter(_modelo("Execucao")).validate_python(sem_hash)


def test_o_nulo_da_parcela_sobreviveu_a_captura(amostras):
    """`c0` e nulo na C3, e nao zero — e o exemplo precisa mostrar isso.

    Se a captura ou uma serializacao trocasse nulo por zero, o painel aprenderia
    pelo exemplo a desenhar barra zerada onde a dimensao nao foi avaliada, e a
    tabela de ablacao ficaria descrita errado. Ver `docs/usabilidade.md`.
    """
    corpo = next(
        r["corpo"]
        for r in amostras["respostas"]
        if r["rota"] == "/api/v1/runs/4/events/ap-8-2-5"
    )
    assert corpo["configuration"] == "C3"
    assert corpo["parcels"]["c0"] is None, "a C3 nao avalia a C0: tem de vir nulo"
    assert corpo["parcels"]["d1"] == 0.0, "avaliada e sem risco e zero, nao nulo"
