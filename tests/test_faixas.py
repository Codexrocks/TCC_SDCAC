"""O teste da apresentacao das faixas — a trava das exigencias de usabilidade.

A [usabilidade](../docs/usabilidade.md) escreve duas exigencias que um PR pode
desfazer sem ninguem notar: **a cor nao pode ser o unico meio visual** (criterio
1.4.1) e **o contraste nao pode cair de 4,5:1** (criterio 1.4.3). Documento nao
impede nenhuma das duas; este arquivo impede.

Tres classes de assercao, por ordem de importancia:

1. **Contra o documento.** Os rotulos e os intervalos sao lidos da tabela da
   secao 5.1 da `usabilidade.md` e comparados com o codigo. Trocar o rotulo num
   dos dois lugares reprova aqui — e foi para isso que o rotulo saiu do codigo
   para o documento, e nao o contrario.
2. **Contra o motor.** Os intervalos da legenda sao conferidos sondando
   `detection.integracao.band_of` ponto a ponto. Legenda que diz 0-20 e motor
   que classifica 0-25 e uma tela que mente sobre o sistema.
3. **Contra a norma.** Cada par texto/fundo passa pelo calculo de contraste.
"""

import re
from pathlib import Path

import pytest

from detection.configuration import load_canonical
from detection.integracao import band_of
from detection.model import RiskBand
from frontend.components.contraste import MINIMO_TEXTO, contraste
from frontend.components.faixas import FAIXAS, Faixa, faixa_de, forma_svg, selo_html

USABILIDADE = Path(__file__).resolve().parent.parent / "docs" / "usabilidade.md"


def tabela_do_documento() -> dict[str, tuple[str, str]]:
    """A tabela da secao 5.1: intervalo -> (rotulo, forma).

    Le do documento, e nao do codigo, de proposito: o documento e onde a
    exigencia esta escrita para gente.
    """
    texto = USABILIDADE.read_text(encoding="utf-8")
    secao = texto.split("### 5.1")[1].split("### 5.2")[0]
    achadas = {}
    for linha in secao.splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) != 4:
            continue
        intervalo, _cor, rotulo, forma = celulas
        if not re.fullmatch(r"\d+\s*[–-]\s*\d+", intervalo):
            continue
        achadas[intervalo.replace("–", "-").replace(" ", "")] = (
            rotulo.strip("`"),
            forma,
        )
    return achadas


def test_o_documento_descreve_as_quatro_faixas():
    do_documento = tabela_do_documento()

    assert len(do_documento) == 4, (
        "a tabela da secao 5.1 da usabilidade.md deixou de ter quatro faixas. "
        f"Foram lidas: {sorted(do_documento)}"
    )


@pytest.mark.parametrize("band", list(RiskBand))
def test_toda_faixa_do_motor_tem_apresentacao(band: RiskBand):
    faixa = faixa_de(band)

    assert isinstance(faixa, Faixa)
    assert faixa.band is band


def test_o_rotulo_e_o_intervalo_batem_com_o_documento():
    do_documento = tabela_do_documento()

    do_codigo = {f.intervalo: f.rotulo for f in FAIXAS.values()}

    assert do_codigo == {i: r for i, (r, _) in do_documento.items()}, (
        "o rotulo ou o intervalo divergiu entre o codigo e a secao 5.1 da "
        "usabilidade.md. Quem manda e o documento"
    )


def test_a_forma_bate_com_o_documento():
    do_documento = tabela_do_documento()

    for faixa in FAIXAS.values():
        _rotulo, forma = do_documento[faixa.intervalo]
        if forma == "—":
            assert faixa.lados < 0, (
                f"{faixa.rotulo} ganhou forma, e o documento nao da uma"
            )
        else:
            assert forma == faixa.forma, (
                f"{faixa.rotulo}: o documento pede {forma!r} e o codigo tem "
                f"{faixa.forma!r}"
            )


@pytest.mark.parametrize("faixa", list(FAIXAS.values()), ids=lambda f: f.band.value)
def test_o_intervalo_da_legenda_bate_com_o_que_o_motor_classifica(faixa: Faixa):
    config = load_canonical("C3")
    inicio, fim = (int(n) for n in faixa.intervalo.split("-"))

    for ponto in (inicio, fim):
        assert band_of(ponto, config) is faixa.band, (
            f"a legenda diz que {ponto} e {faixa.rotulo}, e o band_of discorda. "
            "Os limiares moram em detection/presets.toml"
        )


@pytest.mark.parametrize("faixa", list(FAIXAS.values()), ids=lambda f: f.band.value)
def test_o_contraste_cumpre_o_criterio_1_4_3(faixa: Faixa):
    razao = contraste(faixa.cor_texto, faixa.cor_fundo)

    assert razao >= MINIMO_TEXTO, (
        f"{faixa.rotulo}: {faixa.cor_texto} sobre {faixa.cor_fundo} da "
        f"{razao:.2f}:1, abaixo do minimo de {MINIMO_TEXTO}:1 da WCAG 2.2"
    )


@pytest.mark.parametrize("faixa", list(FAIXAS.values()), ids=lambda f: f.band.value)
def test_a_cor_nunca_e_o_unico_meio_visual(faixa: Faixa):
    selo = selo_html(faixa.band)

    assert faixa.rotulo in selo, (
        f"{faixa.band.value}: o selo saiu sem rotulo textual, e a cor virou o "
        "unico meio visual. E o criterio 1.4.1 reprovando"
    )


def test_as_formas_sao_distintas_entre_as_faixas_que_tem_forma():
    com_forma = [f for f in FAIXAS.values() if f.lados >= 0]

    lados = [f.lados for f in com_forma]

    assert len(set(lados)) == len(lados), (
        f"duas faixas ficaram com a mesma forma: {lados}. Forma repetida devolve "
        "a distincao para a cor"
    )


def test_o_octogono_tem_oito_vertices():
    alto = FAIXAS[RiskBand.HIGH]

    svg = forma_svg(alto)

    pontos = re.search(r'points="([^"]+)"', svg).group(1).split()
    assert len(pontos) == 8, (
        f"o octogono saiu com {len(pontos)} vertices. A usabilidade pede octogono, "
        "e desenhar um hexagono com nome de octogono e mentir na legenda"
    )


def test_a_faixa_sem_forma_nao_desenha_nada():
    normal = FAIXAS[RiskBand.NORMAL]

    assert forma_svg(normal) == ""


def test_faixa_desconhecida_para_em_vez_de_pintar_de_cinza():
    with pytest.raises(ValueError, match="nao existe no contrato"):
        faixa_de("critico")


def test_a_faixa_aceita_a_string_do_contrato_da_api():
    assert faixa_de("high") is FAIXAS[RiskBand.HIGH]


def test_o_selo_mostra_a_nota_quando_recebe_uma():
    selo = selo_html(RiskBand.HIGH, nota=88.4)

    assert "88" in selo
    assert "RISCO ALTO" in selo
