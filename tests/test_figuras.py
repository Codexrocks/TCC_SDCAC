"""O desenho da figura da Secao 4.

**O que este arquivo mede.** O SVG e texto gerado por funcao pura, e e a unica
figura do artigo que nasce do dado -- a outra e captura de tela. Um defeito aqui
nao quebra nada: produz um desenho errado, que entra no documento e vai para a
banca parecendo um resultado.

O caso que motivou o arquivo esta em `test_nenhuma_coordenada_usa_virgula`: a
primeira versao trocava o ponto pela virgula no numero do eixo **e nas
coordenadas junto**, porque a troca caiu sobre literais ja concatenados. O SVG
passou a desenhar os nove rotulos em `x=0`, empilhados. Nenhuma excecao, nenhum
teste vermelho -- so a figura errada.
"""

import re

import pytest

from evaluator.figuras import (
    BASE,
    DIREITA,
    ESQUERDA,
    ESTILOS,
    PISO_PCT,
    TOPO,
    _x,
    _y,
    figura_fpr,
)

CONFIGS = ["C0", "C1", "C2", "C3"]
NIVEIS = [0.1, 0.2, 0.3]


def agregado(valores: dict[str, list[float]]) -> dict:
    """Um agregado minimo, com os desvios em zero salvo indicacao."""
    return {
        "niveis_de_revocacao": NIVEIS,
        "configuracoes": CONFIGS,
        "fpr_a_revocacao_fixa": {
            f"{nivel:.2f}": {
                "por_configuracao": {
                    nome: {"media": valores[nome][i], "desvio": 0.0, "n": 10}
                    for nome in CONFIGS
                }
            }
            for i, nivel in enumerate(NIVEIS)
        },
    }


SIMPLES = agregado({nome: [0.01, 0.1, 0.5] for nome in CONFIGS})


# ------------------------------------------------------------------- escala
def test_cem_por_cento_fica_no_topo():
    assert _y(100.0) == pytest.approx(TOPO)


def test_o_piso_da_escala_fica_na_base():
    assert _y(PISO_PCT) == pytest.approx(BASE)


def test_valor_abaixo_do_piso_e_preso_na_base_em_vez_de_sair_do_desenho():
    """Sem o corte, uma FPR de zero iria para o infinito negativo do log."""
    assert _y(0.0) == pytest.approx(BASE)
    assert _y(PISO_PCT / 1000) == pytest.approx(BASE)


def test_cada_decada_ocupa_a_mesma_altura():
    alturas = [_y(10 ** (2 - k)) - _y(10 ** (3 - k)) for k in range(1, 4)]
    assert alturas[0] == pytest.approx(alturas[1]) == pytest.approx(alturas[2])


def test_o_primeiro_e_o_ultimo_nivel_tocam_as_bordas_do_desenho():
    assert _x(0, 9) == pytest.approx(ESQUERDA)
    assert _x(8, 9) == pytest.approx(DIREITA)


def test_os_niveis_avancam_sempre_para_a_direita():
    posicoes = [_x(i, 9) for i in range(9)]
    assert posicoes == sorted(posicoes)
    assert len(set(posicoes)) == 9


# -------------------------------------------------------------------- o SVG
def test_o_svg_abre_e_fecha():
    svg = figura_fpr(SIMPLES)
    assert svg.startswith("<svg ")
    assert svg.rstrip().endswith("</svg>")


ATRIBUTOS = re.compile(
    r'\b(?:x|y|x1|y1|x2|y2|cx|cy|r|width|height|font-size)="([^"]*)"'
)


def test_nenhuma_coordenada_usa_virgula():
    """O defeito de 12/11/2026: a troca decimal caiu sobre a coordenada.

    Virgula em atributo de coordenada nao e erro de SVG -- o valor e lido como
    invalido e vira zero, e o desenho sai torto **sem reclamar**.
    """
    for valor in ATRIBUTOS.findall(figura_fpr(SIMPLES)):
        assert "," not in valor, f"coordenada com virgula: {valor!r}"


def test_o_rotulo_do_eixo_usa_a_virgula_decimal():
    """No texto, ao contrario, o numero e brasileiro."""
    assert ">0,10<" in figura_fpr(SIMPLES)


def test_ha_uma_linha_por_configuracao():
    assert figura_fpr(SIMPLES).count("<polyline") == len(CONFIGS)


def test_cada_serie_se_distingue_sem_depender_de_cor():
    """Traco e marcador, nunca so a cor: o artigo pode sair impresso em p&b."""
    assinaturas = {(traco, forma, cheio) for traco, forma, cheio in ESTILOS.values()}
    assert len(assinaturas) == len(ESTILOS)


def test_o_desenho_e_preto_no_branco():
    svg = figura_fpr(SIMPLES)
    cores = set(re.findall(r'stroke="(#[0-9a-f]{3,6})"', svg))
    assert cores <= {"#000", "#bbb"}


def test_a_legenda_nomeia_as_quatro_configuracoes():
    svg = figura_fpr(SIMPLES)
    for nome in CONFIGS:
        assert f">{nome}<" in svg


def test_a_barra_de_desvio_so_aparece_quando_ha_desvio():
    sem = figura_fpr(SIMPLES)
    com = agregado({nome: [0.05, 0.1, 0.5] for nome in CONFIGS})
    for bloco in com["fpr_a_revocacao_fixa"].values():
        bloco["por_configuracao"]["C0"]["desvio"] = 0.01
    assert figura_fpr(com).count("<line") > sem.count("<line")


def test_o_agregado_de_verdade_desenha():
    """Prende o formato do `agregado.json` contra o que a figura espera."""
    import json
    from pathlib import Path

    caminho = Path(__file__).resolve().parent.parent / "results" / "agregado.json"
    if not caminho.exists():  # pragma: no cover - so quando results/ nao veio
        pytest.skip("results/agregado.json nao esta neste clone")
    svg = figura_fpr(json.loads(caminho.read_text(encoding="utf-8")))
    assert svg.count("<polyline") == 4
    for valor in ATRIBUTOS.findall(svg):
        assert "," not in valor
