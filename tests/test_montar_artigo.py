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

from montar_artigo import (  # noqa: E402
    SECOES_DE_CONTROLE,
    blocos,
    confere_legendas,
    trechos,
)


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


# ---------------------------------------------------- legenda e fonte da tabela
# O orientador apontou em 12/11/2026, na entrega da Secao de Resultados: "as
# tabelas e figuras devem possuir legenda com a respectiva fonte indicada".
# Nenhuma das seis tabelas do artigo tinha. Estes casos prendem a exigencia no
# lugar onde ela se perde: o Markdown continua legivel sem a legenda, e e o
# `.docx` entregue que sai errado.

TABELA = "| a | b |\n|---|---|\n| 1 | 2 |"
LEGENDA = "**Tabela 1.** Uma tabela."
FONTE = "Fonte: dados da pesquisa (2026)."


def test_legenda_de_tabela_nao_e_paragrafo_comum():
    """Se virar paragrafo, sai justificada e com recuo, e nao centralizada."""
    assert blocos(LEGENDA) == [("legenda", 0, LEGENDA)]


def test_legenda_de_figura_usa_a_mesma_forma():
    """O artigo nao tem figura ainda; a primeira que entrar nao pode precisar
    de codigo novo."""
    ((tipo, _, conteudo),) = blocos("**Figura 3.** Um grafico.")
    assert (tipo, conteudo) == ("legenda", "**Figura 3.** Um grafico.")


def test_fonte_de_tabela_nao_e_paragrafo_comum():
    assert blocos(FONTE) == [("fonte", 0, FONTE)]


def test_paragrafo_que_fala_de_fonte_no_meio_continua_paragrafo():
    """So a linha que **comeca** com `Fonte:` e fonte de tabela."""
    ((tipo, _, _conteudo),) = blocos("A fonte: o que ela diz importa.")
    assert tipo == "paragrafo"


def test_a_ordem_e_legenda_tabela_fonte():
    """Legenda acima e fonte abaixo: e a forma do template somada a NBR 6023."""
    tipos = [t for t, _, _ in blocos(f"{LEGENDA}\n\n{TABELA}\n\n{FONTE}")]
    assert tipos == ["legenda", "tabela", "fonte"]


# ------------------------------------------------------- confere_legendas
def escreve(tmp_path, texto, nome="04-resultados.md"):
    caminho = tmp_path / nome
    caminho.write_text(texto, encoding="utf-8")
    return caminho


def test_tabela_com_legenda_e_fonte_passa(tmp_path):
    caminho = escreve(tmp_path, f"{LEGENDA}\n\n{TABELA}\n\n{FONTE}\n")
    assert confere_legendas([caminho]) == []


def test_tabela_sem_legenda_reprova(tmp_path):
    caminho = escreve(tmp_path, f"{TABELA}\n\n{FONTE}\n")
    ((erro,)) = confere_legendas([caminho])
    assert "sem legenda acima" in erro


def test_tabela_sem_fonte_reprova(tmp_path):
    """E o caso exato do apontamento: a legenda existe e a fonte nao."""
    caminho = escreve(tmp_path, f"{LEGENDA}\n\n{TABELA}\n\nUm paragrafo.\n")
    ((erro,)) = confere_legendas([caminho])
    assert "sem fonte abaixo" in erro


def test_numeracao_fora_de_sequencia_reprova(tmp_path):
    """Numero repetido ou salto e o defeito que aparece ao mover uma tabela."""
    caminho = escreve(
        tmp_path,
        f"{LEGENDA}\n\n{TABELA}\n\n{FONTE}\n\n"
        f"**Tabela 4.** Outra.\n\n{TABELA}\n\n{FONTE}\n",
    )
    ((erro,)) = confere_legendas([caminho])
    assert "numerada 4, esperada 2" in erro


def test_a_numeracao_e_continua_entre_os_arquivos(tmp_path):
    """A Tabela 1 esta na Metodologia e as seguintes nos Resultados: a contagem
    nao reinicia por arquivo."""
    um = escreve(tmp_path, f"{LEGENDA}\n\n{TABELA}\n\n{FONTE}\n", "03.md")
    dois = escreve(tmp_path, f"**Tabela 2.** Outra.\n\n{TABELA}\n\n{FONTE}\n", "04.md")
    assert confere_legendas([um, dois]) == []
    assert confere_legendas([dois]) == [
        f"04.md, 1a tabela ({TABELA.splitlines()[0]}): legenda numerada 2, esperada 1"
    ]


def test_tabela_em_secao_de_controle_nao_precisa_de_legenda(tmp_path):
    """Andaime do repositorio nao vai para o documento, logo nao leva legenda."""
    caminho = escreve(
        tmp_path,
        f"{LEGENDA}\n\n{TABELA}\n\n{FONTE}\n\n## {SECOES_DE_CONTROLE[0]}\n\n{TABELA}\n",
    )
    assert confere_legendas([caminho]) == []


def test_o_erro_diz_qual_tabela_e(tmp_path):
    """Contar blocos de Markdown a mao e o que ninguem faz: o erro traz a
    primeira linha da tabela."""
    caminho = escreve(tmp_path, f"{TABELA}\n")
    ((erro,)) = confere_legendas([caminho])
    assert "1a tabela (| a | b |)" in erro
