"""Testes da API de leitura — o contrato que o painel vai consumir.

**Estes testes sao pulados quando o FastAPI nao esta instalado, e isso e um
problema conhecido, nao um detalhe.** O workflow `Validacao` instala apenas
`pytest` e `pyyaml`, entao **no CI este arquivo e pulado inteiro**. O mesmo
formato de defeito ja mordeu este projeto uma vez — o `tzdata` ausente fazia o
CI passar verde enquanto a maquina da equipe quebrava. A correcao e acrescentar a
instalacao ao workflow, que e arquivo protegido e espera 24 h; a pendencia esta
no relatorio da sessao.

Enquanto isso, `test_a_dependencia_esta_declarada` roda **sempre**, mesmo sem o
FastAPI: ele confere que a dependencia continua no `pyproject.toml`. Nao
substitui os outros, mas impede o caso pior — alguem remover a dependencia e nada
reclamar.

As garantias que importam aqui:

- **nenhuma rota escreve.** Um teste varre o contrato e reprova qualquer verbo
  que nao seja GET;
- **a nota sai decomposta, e nulo e diferente de zero.** E a decomponibilidade
  que a secao 3.9 do artigo promete;
- **paginacao com teto duro.** Sem ele, uma requisicao puxa dois milhoes de
  eventos;
- **o erro nao vaza nada.** Nem SQL, nem caminho de arquivo, nem rastreio.
"""

import json
import tomllib
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


def test_a_dependencia_esta_declarada():
    """Roda sempre, inclusive sem o FastAPI instalado.

    Se alguem remover a dependencia, os outros testes deste arquivo passariam a
    ser pulados em silencio e a API continuaria "passando".
    """
    dados = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))
    declaradas = " ".join(dados["project"]["dependencies"])

    assert "fastapi" in declaradas
    assert "uvicorn" in declaradas


fastapi = pytest.importorskip(
    "fastapi",
    reason=(
        "FastAPI nao instalado. O workflow Validacao instala so pytest e pyyaml, "
        "entao no CI este arquivo e pulado — pendencia registrada no relatorio da "
        "sessao 26"
    ),
)

from fastapi.testclient import TestClient  # noqa: E402

from backend.dependencies import VARIAVEL, limpa_cache  # noqa: E402
from backend.main import ORIGENS_PADRAO, cria_app, origens_permitidas  # noqa: E402
from backend.openapi import CONTRATO, texto_do_contrato  # noqa: E402
from detection.configuration import load_canonical  # noqa: E402
from fixtures_arquivos import (  # noqa: E402
    JANELA_FIM,
    JANELA_INICIO,
    escreve_corp,
    janela_de_avaliacao,
)
from runner import run_experiment  # noqa: E402
from storage.leitura import LIMITE_MAXIMO, ArquivoRepository  # noqa: E402


@pytest.fixture
def execucoes(tmp_path, monkeypatch):
    """Um diretorio com as quatro execucoes gravadas, servido pela API."""
    escreve_corp(tmp_path)
    resumos = run_experiment(
        ArquivoRepository(tmp_path),
        run_id=1,
        configs=[load_canonical(n) for n in ("C0", "C1", "C2", "C3")],
        training=(JANELA_INICIO, JANELA_FIM),
        evaluation=janela_de_avaliacao(),
        threshold=20.0,
        commit="teste",
    )
    monkeypatch.setenv(VARIAVEL, str(tmp_path))
    limpa_cache()
    yield {r.configuration: r for r in resumos}
    limpa_cache()


@pytest.fixture
def cliente(execucoes):
    with TestClient(cria_app()) as cliente:
        cliente.execucoes = execucoes
        yield cliente


# ---------------------------------------------------------------------------
# Saude e configuracoes
# ---------------------------------------------------------------------------


def test_saude_diz_quantas_execucoes_existem(cliente):
    corpo = cliente.get("/api/v1/health").json()

    assert corpo["status"] == "ok"
    assert corpo["runs"] == 4
    assert corpo["adapter"] == "ArquivoRepository"


def test_as_configuracoes_vem_dos_presets_com_hash(cliente):
    """O painel sabe o que cada execucao ligou sem deduzir do nome."""
    corpo = cliente.get("/api/v1/configurations").json()

    assert [c["name"] for c in corpo] == ["C0", "C1", "C2", "C3"]
    assert corpo[0]["dimensions"] == ["c0"]
    assert corpo[3]["dimensions"] == ["d1", "d2", "d3"]
    assert all(len(c["config_hash"]) == 64 for c in corpo)
    assert not any(c["exploratory"] for c in corpo)


# ---------------------------------------------------------------------------
# Execucoes
# ---------------------------------------------------------------------------


def test_as_execucoes_vem_da_mais_recente_para_a_mais_antiga(cliente):
    corpo = cliente.get("/api/v1/runs").json()

    assert corpo["total"] == 4
    ids = [r["scoring_run_id"] for r in corpo["items"]]
    assert ids == sorted(ids, reverse=True)


def test_a_execucao_carrega_hash_commit_e_semente(cliente):
    """D-34: o registro sem hash nao serve para dizer que duas execucoes batem."""
    numero = cliente.execucoes["C3"].scoring_run_id

    corpo = cliente.get(f"/api/v1/runs/{numero}").json()

    assert corpo["config_name"] == "C3"
    assert corpo["config_hash"] == load_canonical("C3").config_hash
    assert corpo["code_sha"] == "teste"
    assert corpo["run_id"] == 1
    assert corpo["exploratory"] is False
    assert corpo["status"] == "done"


def test_execucao_que_nao_existe_devolve_404_com_envelope(cliente):
    resposta = cliente.get("/api/v1/runs/999")

    assert resposta.status_code == 404
    assert resposta.json()["code"] == "nao_encontrado"
    assert "999" in resposta.json()["message"]


# ---------------------------------------------------------------------------
# A nota decomposta, que e o que a usabilidade exige
# ---------------------------------------------------------------------------


def test_a_nota_sai_com_as_cinco_parcelas(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id

    corpo = cliente.get(f"/api/v1/runs/{numero}/employees").json()
    parcelas = corpo["items"][0]["parcels"]

    assert set(parcelas) == {"c0", "d1", "d2", "d3_conduct", "d3_posture"}


def test_parcela_nao_avaliada_sai_nula_e_nao_zero(cliente):
    """Nulo e "nao avaliada"; zero e "avaliada e sem risco".

    Se a API trocasse nulo por zero, uma execucao da C1 ficaria indistinguivel de
    uma da C3 em que nada disparou — e e justamente a diferenca entre as linhas
    da tabela de ablacao.
    """
    c0 = cliente.execucoes["C0"].scoring_run_id
    c1 = cliente.execucoes["C1"].scoring_run_id

    da_c0 = cliente.get(f"/api/v1/runs/{c0}/employees").json()["items"][0]["parcels"]
    da_c1 = cliente.get(f"/api/v1/runs/{c1}/employees").json()["items"][0]["parcels"]

    assert da_c0["c0"] is not None
    assert da_c0["d1"] is None
    assert da_c1["c0"] is None
    assert da_c1["d1"] is not None


def test_as_duas_parcelas_da_d3_saem_separadas(cliente):
    """D-25 e D-30 chegando ao painel.

    Guardar so o total esconderia qual das duas causou o alerta, e a acao e
    diferente: conduta pede investigacao, postura pede correcao de configuracao.
    """
    numero = cliente.execucoes["C3"].scoring_run_id

    parcelas = cliente.get(f"/api/v1/runs/{numero}/employees").json()["items"][0][
        "parcels"
    ]

    assert "d3_conduct" in parcelas
    assert "d3_posture" in parcelas
    assert "d3" not in parcelas


def test_o_historico_traz_os_motivos_de_cada_nota(cliente):
    """Score sem motivo obriga quem analisa a adivinhar o que o numero quis."""
    numero = cliente.execucoes["C3"].scoring_run_id

    corpo = cliente.get(f"/api/v1/runs/{numero}/employees/8").json()
    com_motivo = [i for i in corpo["items"] if i["hits"]]

    assert com_motivo
    for item in com_motivo:
        for motivo in item["hits"]:
            assert motivo["rule"]
            assert motivo["reason"]


def test_o_historico_vem_do_mais_recente_para_o_mais_antigo(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id

    corpo = cliente.get(f"/api/v1/runs/{numero}/employees/8").json()
    instantes = [i["occurred_at"] for i in corpo["items"]]

    assert instantes == sorted(instantes, reverse=True)


def test_a_nota_de_um_evento_vem_pelo_identificador(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id
    algum = cliente.get(f"/api/v1/runs/{numero}/employees").json()["items"][0]

    corpo = cliente.get(
        f"/api/v1/runs/{numero}/events/{algum['event_id']}"
    ).json()

    assert corpo["event_id"] == algum["event_id"]
    assert corpo["config_hash"] == load_canonical("C3").config_hash
    assert corpo["parcels"] == algum["parcels"]


def test_evento_sem_nota_devolve_404(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id

    resposta = cliente.get(f"/api/v1/runs/{numero}/events/nao-existe")

    assert resposta.status_code == 404
    assert resposta.json()["code"] == "nao_encontrado"


def test_toda_data_sai_com_fuso(cliente):
    """Data sem fuso no contrato viraria hora local no painel, em silencio."""
    numero = cliente.execucoes["C3"].scoring_run_id

    corpo = cliente.get(f"/api/v1/runs/{numero}/employees").json()

    for item in corpo["items"]:
        assert item["occurred_at"].endswith("Z") or "+" in item["occurred_at"]


# ---------------------------------------------------------------------------
# Alertas
# ---------------------------------------------------------------------------


def test_o_alerta_carrega_o_limiar_que_o_levantou(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id

    corpo = cliente.get(f"/api/v1/runs/{numero}/alerts").json()

    assert corpo["total"] > 0
    for alerta in corpo["items"]:
        assert alerta["threshold"] == 20.0


def test_o_filtro_de_faixa_so_aceita_as_quatro(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id

    valido = cliente.get(f"/api/v1/runs/{numero}/alerts?band=low")
    invalido = cliente.get(f"/api/v1/runs/{numero}/alerts?band=roxo")

    assert valido.status_code == 200
    assert all(a["band"] == "low" for a in valido.json()["items"])
    assert invalido.status_code == 422
    assert invalido.json()["code"] == "parametro_invalido"
    assert invalido.json()["detail"] == "band"


def test_o_filtro_de_periodo_recorta(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id
    todos = cliente.get(f"/api/v1/runs/{numero}/alerts?limit=200").json()
    meio = sorted(a["raised_at"] for a in todos["items"])[len(todos["items"]) // 2]

    recorte = cliente.get(f"/api/v1/runs/{numero}/alerts?since={meio}").json()

    assert 0 < recorte["total"] < todos["total"]


# ---------------------------------------------------------------------------
# Metricas — a API nao calcula
# ---------------------------------------------------------------------------


def test_metricas_sai_vazia_enquanto_o_avaliador_nao_existir(cliente):
    """Pagina vazia e resposta, nao falha.

    Calcular aqui exigiria o rotulo, e o usuario da aplicacao nao tem permissao
    de conectar no `ground_truth`.
    """
    numero = cliente.execucoes["C3"].scoring_run_id

    corpo = cliente.get(f"/api/v1/runs/{numero}/metrics").json()

    assert corpo["items"] == []
    assert corpo["total"] == 0


# ---------------------------------------------------------------------------
# Paginacao, que tambem e limite de dano
# ---------------------------------------------------------------------------


def test_toda_lista_vem_com_envelope_de_pagina(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id
    listas = (
        "/api/v1/runs",
        f"/api/v1/runs/{numero}/employees",
        f"/api/v1/runs/{numero}/employees/8",
        f"/api/v1/runs/{numero}/alerts",
        f"/api/v1/runs/{numero}/metrics",
    )

    for rota in listas:
        corpo = cliente.get(rota).json()
        assert set(corpo) == {"items", "total", "limit", "offset"}, rota


def test_o_teto_de_pagina_e_duro(cliente):
    """Sem teto, uma requisicao puxa dois milhoes de eventos."""
    numero = cliente.execucoes["C3"].scoring_run_id

    resposta = cliente.get(f"/api/v1/runs/{numero}/employees?limit={LIMITE_MAXIMO + 1}")

    assert resposta.status_code == 422
    assert resposta.json()["detail"] == "limit"


def test_o_deslocamento_nao_repete_nem_perde_item(cliente):
    numero = cliente.execucoes["C3"].scoring_run_id

    primeira = cliente.get(f"/api/v1/runs/{numero}/employees/8?limit=2&offset=0").json()
    segunda = cliente.get(f"/api/v1/runs/{numero}/employees/8?limit=2&offset=2").json()

    ids_primeira = {i["event_id"] for i in primeira["items"]}
    ids_segunda = {i["event_id"] for i in segunda["items"]}

    assert not (ids_primeira & ids_segunda)
    assert primeira["total"] == segunda["total"]


def test_deslocamento_negativo_e_recusado(cliente):
    resposta = cliente.get("/api/v1/runs?offset=-1")

    assert resposta.status_code == 422


# ---------------------------------------------------------------------------
# O que a API nao faz
# ---------------------------------------------------------------------------


def test_nenhuma_rota_escreve(cliente):
    """Somente leitura, e isso e verificavel no proprio contrato.

    Execucao e disparada pela linha de comando, pela D-35. Rota de escrita
    entraria na v2 — e enquanto nao entrar, nao pode aparecer por descuido.
    """
    contrato = cliente.get("/api/v1/openapi.json").json()

    for caminho, metodos in contrato["paths"].items():
        assert set(metodos) <= {"get"}, f"{caminho} aceita {sorted(metodos)}"


def test_nenhuma_rota_entrega_gabarito(cliente):
    """Rota que entregasse rotulo seria o vazamento com nome de API.

    A busca e na **superficie que a maquina usa** — caminho, nome de parametro,
    campo de esquema, identificador de operacao —, e nao no texto das
    descricoes: a primeira versao deste teste reprovava justamente a frase que
    diz que a API nao le o gabarito.
    """
    contrato = cliente.get("/api/v1/openapi.json").json()
    suspeitas = ("label", "ground_truth", "scenario", "rotulo", "gabarito", "injected")

    nomes: list[str] = []
    for caminho, metodos in contrato["paths"].items():
        nomes.append(caminho)
        for operacao in metodos.values():
            nomes.append(operacao.get("operationId", ""))
            for parametro in operacao.get("parameters", []):
                nomes.append(parametro.get("name", ""))
    for nome, esquema in contrato["components"]["schemas"].items():
        nomes.append(nome)
        nomes.extend(esquema.get("properties", {}))

    for nome in nomes:
        for suspeita in suspeitas:
            assert suspeita not in nome.lower(), (
                f"{nome!r} parece entregar o gabarito"
            )


def test_o_erro_inesperado_nao_vaza_caminho_nem_pilha(cliente, monkeypatch):
    """O repositorio e publico; isso nao e motivo para a API se narrar.

    Quando algo falha de forma nao prevista, o cliente recebe que falhou — e nada
    sobre como o servidor e feito por dentro.
    """
    import backend.api as rotas

    def explode(*_, **__):
        raise RuntimeError(
            "select * from risk_scores where caminho='/home/davi/segredo'"
        )

    monkeypatch.setattr(rotas, "_execucao_ou_404", explode)

    # `raise_server_exceptions=False` faz o cliente se comportar como um
    # navegador: ele recebe a resposta do manipulador em vez de a excecao subir
    # pelo teste. E a resposta que o painel veria.
    with TestClient(cria_app(), raise_server_exceptions=False) as navegador:
        resposta = navegador.get("/api/v1/runs/1/employees")

    assert resposta.status_code == 500
    corpo = resposta.json()
    assert corpo == {
        "code": "erro_interno",
        "message": "a requisicao nao pode ser atendida",
        "detail": None,
    }
    assert "select" not in resposta.text.lower()
    assert "/home" not in resposta.text


# ---------------------------------------------------------------------------
# CORS e o contrato versionado
# ---------------------------------------------------------------------------


def test_o_cors_tem_lista_explicita_e_nao_curinga(monkeypatch):
    """`*` deixaria qualquer pagina aberta no navegador consultar esta API."""
    assert origens_permitidas() == list(ORIGENS_PADRAO)
    assert "*" not in origens_permitidas()

    monkeypatch.setenv("SDCAC_ORIGENS", "https://painel.exemplo, https://outro.exemplo")

    assert origens_permitidas() == ["https://painel.exemplo", "https://outro.exemplo"]


def test_o_contrato_versionado_esta_em_dia():
    """O arquivo no git tem de bater com o que a aplicacao gera.

    E o mesmo truque do `docs/quadro.md` contra o `quadro.toml`: contrato que
    muda sem aparecer no diff e tela que quebra sem aviso. Rode
    `python -m backend.openapi` para regerar.
    """
    assert CONTRATO.exists(), "falta backend/openapi.json — rode python -m backend.openapi"

    assert CONTRATO.read_text(encoding="utf-8") == texto_do_contrato(), (
        "backend/openapi.json esta defasado. Rode: python -m backend.openapi"
    )


def test_o_contrato_publicado_cobre_os_quatro_grupos_da_d36():
    """Execucoes, funcionarios, eventos e alertas, metricas."""
    contrato = json.loads(CONTRATO.read_text(encoding="utf-8"))
    caminhos = set(contrato["paths"])

    assert "/api/v1/runs" in caminhos
    assert "/api/v1/runs/{scoring_run_id}/employees" in caminhos
    assert "/api/v1/runs/{scoring_run_id}/alerts" in caminhos
    assert "/api/v1/runs/{scoring_run_id}/events/{event_id}" in caminhos
    assert "/api/v1/runs/{scoring_run_id}/metrics" in caminhos
