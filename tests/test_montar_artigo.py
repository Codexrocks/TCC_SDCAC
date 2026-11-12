"""A leitura do Markdown pelo montador do artigo.

**O que este arquivo mede, e o que nao mede.** Mede `blocos` e `trechos`, que
sao as funcoes que decidem **o que entra no documento de entrega** e com que
formatacao. Nao mede a escrita do `.docx`, que depende do `python-docx` -- e o
CI instala so `pytest pyyaml fastapi httpx`, de modo que um teste que exigisse a
biblioteca seria **pulado em silencio** na nuvem.

Por isso o `scripts/montar_artigo.py` importa o `docx` com tolerancia a falta:
as funcoes puras rodam sem ele, e e aqui que elas sao prendidas.

**Por que isto importa mais do que parece.** O que o montador descarta nao
aparece no documento, e ninguem percebe a falta lendo o Markdown. Se `blocos`
deixasse de reconhecer um bloco de citacao, instrucoes internas do repositorio
iriam para a banca; se passasse a descartar demais, texto do artigo sumiria do
`.docx` sem erro nenhum.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from montar_artigo import SECOES_DE_CONTROLE, blocos, trechos  # noqa: E402


# ------------------------------------------------------------------- blocos
def test_paragrafo_de_varias_linhas_vira_um_bloco_so():
    """O Markdown quebra linha por largura; o paragrafo do artigo e um so."""
    saida = blocos("Primeira linha\ne a continuacao dela.")
    assert saida == [("paragrafo", 0, "Primeira linha e a continuacao dela.")]


def test_bloco_de_citacao_nao_entra_no_documento():
    """`>` e instrucao do repositorio, e e o descarte mais importante.

    Se este teste cair, instrucoes internas -- "a escrever", "confirmar com o
    professor" -- vao para o documento que a banca le.
    """
    texto = "Texto do artigo.\n\n> Instrucao interna que nao sai no documento.\n\nMais texto."
    tipos = [(tipo, conteudo) for tipo, _, conteudo in blocos(texto)]
    assert tipos == [("paragrafo", "Texto do artigo."), ("paragrafo", "Mais texto.")]
    assert all("Instrucao interna" not in c for _, c in tipos)


def test_citacao_de_varias_linhas_sai_inteira():
    texto = "Antes.\n\n> linha um\n> linha dois\n> linha tres\n\nDepois."
    conteudos = [c for _, _, c in blocos(texto)]
    assert conteudos == ["Antes.", "Depois."]


def test_titulos_saem_com_o_nivel():
    saida = blocos("# Um\n\n## Dois\n\n### Tres")
    assert saida == [("titulo", 1, "Um"), ("titulo", 2, "Dois"), ("titulo", 3, "Tres")]


def test_tabela_sai_inteira_em_um_bloco():
    texto = "| a | b |\n|---|---|\n| 1 | 2 |"
    saida = blocos(texto)
    assert len(saida) == 1
    tipo, _, linhas = saida[0]
    assert tipo == "tabela"
    assert len(linhas) == 3


def test_formula_e_reconhecida():
    tipo, _, conteudo = blocos("$$x = y$$")[0]
    assert tipo == "formula"
    assert conteudo == "x = y"


def test_item_de_lista_junta_as_linhas_de_continuacao():
    saida = blocos("* um item que continua\n  na linha seguinte")
    assert saida == [("item", 0, "* um item que continua na linha seguinte")]


def test_a_lista_alfabetica_dos_objetivos_e_item():
    """A Introducao lista os objetivos como `a)`, `b)` -- tem de virar item."""
    tipo, _, conteudo = blocos("a) o primeiro objetivo")[0]
    assert tipo == "item"


def test_linha_horizontal_nao_vira_paragrafo():
    assert blocos("Antes.\n\n***\n\nDepois.") == [
        ("paragrafo", 0, "Antes."),
        ("paragrafo", 0, "Depois."),
    ]


def test_texto_vazio_nao_quebra():
    assert blocos("") == []


def test_a_secao_de_controle_tem_o_nome_exato_que_o_artigo_usa():
    """O descarte e por igualdade exata: um titulo renomeado deixa de ser cortado.

    Prende a lista contra edicao distraida -- se alguem trocar "seção" por
    "secao" numa pagina do artigo, a secao de controle inteira vaza para o
    documento de entrega.
    """
    assert "O que esta seção ainda precisa" in SECOES_DE_CONTROLE
    assert "O que esta página ainda precisa" in SECOES_DE_CONTROLE


# ------------------------------------------------------------------ trechos
@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("simples", [("simples", False, False, False)]),
        ("**forte**", [("forte", True, False, False)]),
        ("*enfase*", [("enfase", False, True, False)]),
        ("`codigo`", [("codigo", False, False, True)]),
    ],
)
def test_cada_marcacao_vira_seu_formato(entrada, esperado):
    assert trechos(entrada) == esperado


def test_negrito_no_meio_da_frase_nao_engole_o_resto():
    assert trechos("antes **meio** depois") == [
        ("antes ", False, False, False),
        ("meio", True, False, False),
        (" depois", False, False, False),
    ]


def test_dois_asteriscos_nao_viram_italico():
    """`**` e negrito e `*` e italico; confundir os dois estraga a pagina toda."""
    ((texto, negrito, italico, _),) = trechos("**x**")
    assert (negrito, italico) == (True, False)
    ((texto, negrito, italico, _),) = trechos("*x*")
    assert (negrito, italico) == (False, True)
