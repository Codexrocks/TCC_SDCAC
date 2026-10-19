"""O teste do cliente do painel — e do caminho que ele monta.

O que importa aqui nao e o `httpx`: e que **o caminho que o painel pede exista
no contrato**. Metodo que monte `/api/v1/run/4` em vez de `/api/v1/runs/4` passa
em qualquer teste de unidade e quebra na tela, tarde. Entao cada caminho que o
`Painel` monta e conferido contra `backend/openapi.json`, do mesmo jeito que
`tests/test_exemplos.py` confere os corpos.

O resto cobre a fonte de exemplos, que e o que permite escrever o painel sem
subir servidor: ela responde as rotas gravadas, e **para com mensagem** nas que
nao estao — em vez de devolver vazio, que a tela mostraria como "nao ha dados".
"""

import json
import re
from pathlib import Path

import pytest

from frontend.dashboard.cliente import (
    EXEMPLOS,
    FonteExemplos,
    Painel,
    Resposta,
    SourceUnavailableError,
    _query,
)

RAIZ = Path(__file__).resolve().parent.parent
CONTRATO = RAIZ / "backend" / "openapi.json"


@pytest.fixture
def painel() -> Painel:
    return Painel(FonteExemplos())


def caminhos_do_contrato() -> list[str]:
    """As rotas declaradas no contrato, com os parametros de caminho como regex."""
    contrato = json.loads(CONTRATO.read_text(encoding="utf-8"))
    return list(contrato["paths"])


def vira_regex(rota: str) -> re.Pattern[str]:
    """`/runs/{id}/events/{event_id}` vira um padrao que casa com valores reais."""
    return re.compile(
        "^"
        + re.sub(
            r"\{[^}]+\}",
            r"[^/]+",
            re.escape(rota).replace(r"\{", "{").replace(r"\}", "}"),
        )
        + "$"
    )


# ---------------------------------------------------------------------------
# O caminho que o painel monta existe no contrato
# ---------------------------------------------------------------------------

CHAMADAS = (
    ("saude", (), {}),
    ("configuracoes", (), {}),
    ("execucoes", (), {"limit": 10, "offset": 0}),
    ("execucao", (4,), {}),
    ("alertas", (4,), {"band": "high", "since": "2026-04-01T00:00:00Z", "limit": 5}),
    ("funcionarios", (4,), {"limit": 50}),
    ("funcionario", (4, 8), {}),
    ("evento", (4, "ap-8-2-5"), {}),
    ("metricas", (4,), {}),
)


class FonteEspia:
    """Guarda a rota pedida, sem responder nada util."""

    def __init__(self) -> None:
        self.pedidas: list[str] = []

    def obter(self, rota: str) -> Resposta:
        self.pedidas.append(rota)
        return Resposta(200, {})


@pytest.mark.parametrize("metodo,args,kwargs", CHAMADAS, ids=[c[0] for c in CHAMADAS])
def test_o_caminho_montado_existe_no_contrato(metodo, args, kwargs):
    espia = FonteEspia()
    painel = Painel(espia)

    getattr(painel, metodo)(*args, **kwargs)

    pedida = espia.pedidas[0].split("?", 1)[0]
    padroes = [vira_regex(r) for r in caminhos_do_contrato()]
    assert any(p.match(pedida) for p in padroes), (
        f"{metodo} montou {pedida!r}, que nao casa com nenhuma rota de "
        "backend/openapi.json"
    )


def test_o_painel_cobre_todas_as_rotas_do_contrato():
    espia = FonteEspia()
    painel = Painel(espia)
    for metodo, args, kwargs in CHAMADAS:
        getattr(painel, metodo)(*args, **kwargs)

    pedidas = [r.split("?", 1)[0] for r in espia.pedidas]

    for rota in caminhos_do_contrato():
        padrao = vira_regex(rota)
        assert any(padrao.match(p) for p in pedidas), (
            f"a rota {rota} existe no contrato e o Painel nao tem metodo que a "
            "chame. Tela que precisar dela vai montar caminho a mao"
        )


# ---------------------------------------------------------------------------
# A query string
# ---------------------------------------------------------------------------


def test_a_query_omite_o_que_nao_foi_pedido():
    assert _query(band=None, limit=None) == ""


def test_a_query_monta_so_o_que_veio():
    montada = _query(band="high", limit=None, offset=0)

    assert montada == "?band=high&offset=0"


def test_o_filtro_de_faixa_usa_o_vocabulario_do_contrato():
    contrato = json.loads(CONTRATO.read_text(encoding="utf-8"))
    rota = contrato["paths"]["/api/v1/runs/{scoring_run_id}/alerts"]["get"]
    faixa = next(p for p in rota["parameters"] if p["name"] == "band")

    padrao = next(v["pattern"] for v in faixa["schema"]["anyOf"] if "pattern" in v)

    espia = FonteEspia()
    Painel(espia).alertas(4, band="high")
    valor = espia.pedidas[0].split("band=")[1].split("&")[0]
    assert re.fullmatch(padrao, valor), f"{valor!r} nao casa com {padrao!r}"


# ---------------------------------------------------------------------------
# A fonte de exemplos
# ---------------------------------------------------------------------------


def test_a_fonte_de_exemplos_responde_a_saude(painel: Painel):
    corpo = painel.saude().exigir()

    assert corpo["status"] == "ok"


def test_a_fonte_de_exemplos_traz_a_decomposicao_em_cinco_parcelas(painel: Painel):
    corpo = painel.evento(4, "ap-8-2-5").exigir()

    assert set(corpo["parcels"]) == {"c0", "d1", "d2", "d3_conduct", "d3_posture"}


def test_as_duas_parcelas_da_d3_vem_separadas(painel: Painel):
    """A D-25 manda reportar conduta e postura em campos proprios."""
    parcelas = painel.evento(4, "ap-8-2-5").exigir()["parcels"]

    assert "d3_conduct" in parcelas
    assert "d3_posture" in parcelas
    assert "d3" not in parcelas, (
        "apareceu uma parcela `d3` agregada. A D-25 exige as duas separadas, e "
        "guardar so o total esconde qual delas causou o alerta"
    )


def test_o_evento_traz_o_motivo_em_texto(painel: Painel):
    corpo = painel.evento(4, "ap-8-2-5").exigir()

    assert corpo["hits"], "sem `hits` nao ha o que mostrar na decomposicao"
    assert corpo["hits"][0]["reason"].strip()


def test_rota_nao_gravada_para_com_mensagem(painel: Painel):
    with pytest.raises(SourceUnavailableError, match="nao esta gravada"):
        painel.funcionario(4, 99)


def test_a_fonte_de_exemplos_declara_os_proprios_limites():
    fonte = FonteExemplos()

    assert "high" in fonte.limites, (
        "o campo `_limites` deixou de avisar que nao existe ninguem na faixa "
        "`high`. E o aviso que impede o painel de prometer o aceite da S9"
    )


def test_a_resposta_de_erro_nao_passa_por_dado():
    resposta = Resposta(404, {"detail": "nao existe"})

    assert not resposta.ok
    with pytest.raises(SourceUnavailableError, match="404"):
        resposta.exigir()


def test_a_execucao_inexistente_esta_gravada_como_erro():
    """O arquivo de exemplos guarda o 404 de `/runs/999`, e isso e proposito."""
    fonte = FonteExemplos()

    resposta = fonte.obter("/api/v1/runs/999")

    assert resposta.status == 404


def test_o_caminho_padrao_dos_exemplos_existe():
    assert EXEMPLOS.is_file(), f"{EXEMPLOS} nao existe"
