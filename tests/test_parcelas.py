"""O teste da decomposicao do risco — a tela que o aceite da S9 cobra.

Duas regras do repositorio se cumprem aqui, e as duas sao faceis de desfazer
sem ninguem notar:

**A D-25 manda reportar as duas parcelas da D3 separadas.** Conduta e postura
respondem perguntas diferentes, e somar as duas numa barra so esconderia qual
delas causou o alerta. O teste reprova se a lista de dimensoes perder qualquer
uma das duas, ou se aparecer uma `d3` agregada.

**Nulo nao e zero.** Parcela `null` quer dizer que a configuracao nao liga
aquela dimensao; `0.0` quer dizer que ela rodou e nao achou nada. Uma tela que
mostre as duas como "0" faz a C3 parecer avaliar regras fixas sem achar nada,
quando ela nem as liga.
"""

import json
import re
from pathlib import Path

import pytest

from frontend.components.parcelas import (
    DIMENSOES,
    barra_html,
    motivo_html,
    parcelas_de,
    soma_das_parcelas,
)

RAIZ = Path(__file__).resolve().parent.parent
CONTRATO = RAIZ / "backend" / "openapi.json"


def campos_do_contrato() -> set[str]:
    """Os campos que o schema `ParcelasDoRisco` declara."""
    contrato = json.loads(CONTRATO.read_text(encoding="utf-8"))
    return set(contrato["components"]["schemas"]["ParcelasDoRisco"]["properties"])


# ---------------------------------------------------------------------------
# Contra o contrato
# ---------------------------------------------------------------------------


def test_o_painel_decompoe_exatamente_as_parcelas_do_contrato():
    do_painel = {d.campo for d in DIMENSOES}

    assert do_painel == campos_do_contrato(), (
        "a lista de dimensoes do painel divergiu do schema ParcelasDoRisco. "
        "Dimensao nova no motor que nao aparece na tela de decomposicao e "
        "pontuacao invisivel"
    )


def test_as_duas_parcelas_da_d3_sao_dimensoes_distintas():
    campos = [d.campo for d in DIMENSOES]

    assert "d3_conduct" in campos
    assert "d3_posture" in campos
    assert "d3" not in campos, (
        "apareceu uma dimensao `d3` agregada. A D-25 exige conduta e postura "
        "separadas na apresentacao, nao so no banco"
    )


def test_toda_dimensao_tem_pergunta():
    sem_pergunta = [d.campo for d in DIMENSOES if not d.pergunta.strip()]

    assert not sem_pergunta, (
        f"{sem_pergunta} ficaram sem pergunta. E a pergunta que torna o numero "
        "interpretavel em menos de um minuto, que e o que o aceite da S9 pede"
    )


def test_a_ordem_das_dimensoes_nao_depende_do_dado():
    primeira = parcelas_de({"parcels": {"d3_posture": 1.0, "c0": 2.0}})
    segunda = parcelas_de({"parcels": {"c0": 2.0, "d3_posture": 1.0}})

    assert [p.dimensao.campo for p in primeira] == [p.dimensao.campo for p in segunda]


# ---------------------------------------------------------------------------
# Nulo nao e zero
# ---------------------------------------------------------------------------


def test_parcela_desligada_nao_vira_zero():
    parcelas = parcelas_de({"parcels": {"c0": None, "d1": 0.0}})

    c0 = next(p for p in parcelas if p.dimensao.campo == "c0")
    d1 = next(p for p in parcelas if p.dimensao.campo == "d1")
    assert c0.texto == "nao ligada"
    assert d1.texto == "0"
    assert not c0.ligada
    assert d1.ligada


def test_a_soma_ignora_as_desligadas():
    parcelas = parcelas_de({"parcels": {"c0": None, "d1": 10.0, "d3_conduct": 34.0}})

    assert soma_das_parcelas(parcelas) == 44.0


def test_parcela_que_o_painel_nao_conhece_para_em_vez_de_sumir():
    with pytest.raises(ValueError, match="nao conhece"):
        parcelas_de({"parcels": {"d4_telepatia": 10.0}})


def test_parcela_ausente_na_resposta_conta_como_desligada():
    parcelas = parcelas_de({"parcels": {"d1": 5.0}})

    assert [p.ligada for p in parcelas] == [False, True, False, False, False]


# ---------------------------------------------------------------------------
# A barra
# ---------------------------------------------------------------------------


def test_a_barra_so_mostra_quem_pontuou():
    parcelas = parcelas_de({"parcels": {"c0": None, "d1": 0.0, "d3_conduct": 34.0}})

    barra = barra_html(parcelas)

    assert barra.count("<div title=") == 1, (
        "a barra ganhou fatia de parcela que nao pontuou. Fatia de largura zero "
        "vira tracinho sem rotulo"
    )
    assert "D3a" in barra


def test_a_barra_some_quando_nada_pontuou():
    parcelas = parcelas_de({"parcels": {"d1": 0.0, "d2": 0.0}})

    assert barra_html(parcelas) == ""


def test_a_barra_se_anuncia_para_leitor_de_tela():
    parcelas = parcelas_de({"parcels": {"d1": 10.0}})

    assert 'role="img"' in barra_html(parcelas)
    assert "aria-label=" in barra_html(parcelas)


def test_as_fatias_somam_a_largura_toda():
    parcelas = parcelas_de({"parcels": {"d1": 10.0, "d2": 30.0}})

    # `width:...%;background` casa so com a fatia: o contorno tem `max-width:100%`
    larguras = [
        float(x)
        for x in re.findall(r"[^-]width:([\d.]+)%;background", barra_html(parcelas))
    ]

    assert sum(larguras) == pytest.approx(100.0, abs=0.2)


# ---------------------------------------------------------------------------
# O motivo em texto
# ---------------------------------------------------------------------------


def test_o_motivo_mostra_regra_pontos_e_texto():
    html = motivo_html(
        {
            "rule": "accumulated_exposure",
            "points": 34,
            "reason": "17 eventos em 14 dias",
        }
    )

    assert "accumulated_exposure" in html
    assert "+34" in html
    assert "17 eventos em 14 dias" in html


def test_motivo_sem_texto_diz_que_nao_ha_motivo():
    html = motivo_html({"rule": "x", "points": 1, "reason": "   "})

    assert "sem motivo registrado" in html


# ---------------------------------------------------------------------------
# Contra o dado real
# ---------------------------------------------------------------------------


def test_a_resposta_real_da_api_decompoe_sem_erro():
    """O evento gravado em `exemplos.json`, decomposto pelo painel."""
    exemplos = json.loads(
        (RAIZ / "backend" / "exemplos.json").read_text(encoding="utf-8")
    )
    evento = next(
        r["corpo"]
        for r in exemplos["respostas"]
        if r["rota"].endswith("/events/ap-8-2-5")
    )

    parcelas = parcelas_de(evento)

    assert len(parcelas) == 5
    conduta = next(p for p in parcelas if p.dimensao.campo == "d3_conduct")
    assert conduta.pontos == 34.0
    assert soma_das_parcelas(parcelas) == evento["final_raw"]
