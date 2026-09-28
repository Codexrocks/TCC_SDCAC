"""Testes do gerador do quadro.

Existem pela mesma razao dos testes do validar.py: o quadro e o que vai dizer a
equipe o que esta atrasado. Se o calculo de prazo quebrar, a pagina continua
bonita, continua sendo gerada, e passa a mentir em silencio — que e exatamente o
defeito que ela nasceu para corrigir.
"""
import datetime

import pytest

import quadro

HOJE = datetime.date(2026, 9, 26)


@pytest.fixture(scope="module")
def dados():
    return quadro.carregar()


# ---------------------------------------------------------------------------
# Fronteiras do calculo de coluna
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "prazo, esperada",
    [
        (datetime.date(2026, 9, 25), "atrasado"),   # ontem
        (datetime.date(2026, 9, 26), "a-vencer"),   # hoje ainda da
        (datetime.date(2026, 10, 3), "a-vencer"),   # exatamente 7 dias
        (datetime.date(2026, 10, 4), "depois"),     # 8 dias ja e depois
        (None, "depois"),                           # sem prazo nao desaparece
    ],
)
def test_coluna_de_prazo(prazo, esperada):
    assert quadro.coluna_de_prazo(prazo, HOJE) == esperada


def test_prazo_de_hoje_nao_conta_como_atrasado():
    """Vencer hoje e diferente de ter vencido. Um cobra, o outro acusa."""
    assert quadro.frase_de_prazo(HOJE, HOJE) == "⏳ Vence hoje"


# ---------------------------------------------------------------------------
# Concordancia — a pagina e publica
# ---------------------------------------------------------------------------


def test_plural_concorda():
    assert quadro.plural(1, "dia", "dias") == "1 dia"
    assert quadro.plural(0, "dia", "dias") == "0 dias"
    assert quadro.plural(2, "item", "itens") == "2 itens"


def test_frase_no_singular_e_no_plural():
    assert quadro.frase_de_prazo(datetime.date(2026, 9, 25), HOJE) == (
        "⚠️ Atrasado há 1 dia"
    )
    assert quadro.frase_de_prazo(datetime.date(2026, 9, 24), HOJE) == (
        "⚠️ Atrasado há 2 dias"
    )
    assert quadro.frase_de_prazo(datetime.date(2026, 9, 27), HOJE) == (
        "⏳ Vence em 1 dia"
    )


# ---------------------------------------------------------------------------
# Rotulo textual junto do icone — exigencia de docs/usabilidade.md
# ---------------------------------------------------------------------------


def test_toda_situacao_tem_palavra_e_nao_so_icone(dados):
    """Cor e icone sozinhos nao informam quem nao os distingue.

    A regra esta em docs/usabilidade.md e vale para o quadro como vale para o
    dashboard. Aqui ela deixa de ser recomendacao e passa a reprovar.
    """
    for cartao in quadro.cartoes(dados, HOJE):
        situacao = cartao[6]
        letras = [c for c in situacao if c.isalpha()]
        assert letras, f"situacao sem palavra nenhuma: {situacao!r}"


def test_toda_coluna_tem_rotulo_escrito():
    for chave, icone, rotulo in quadro.COLUNAS:
        assert chave and icone and rotulo.strip()
        assert any(c.isalpha() for c in rotulo)


# ---------------------------------------------------------------------------
# Prazo que e uma semana, e prazo que nao existe
# ---------------------------------------------------------------------------


def test_resolver_prazo_por_data(dados):
    semanas = quadro.semanas_por_id(dados)
    item = {"prazo": datetime.date(2026, 10, 1)}
    assert quadro.resolver_prazo(item, semanas) == datetime.date(2026, 10, 1)


def test_resolver_prazo_por_semana(dados):
    """Prazo "fecha na S8" vira o ultimo dia da S8, nao o primeiro."""
    semanas = quadro.semanas_por_id(dados)
    assert quadro.resolver_prazo({"prazo_semana": "S8"}, semanas) == semanas["S8"]["fim"]


def test_resolver_prazo_inexistente(dados):
    semanas = quadro.semanas_por_id(dados)
    assert quadro.resolver_prazo({}, semanas) is None
    assert quadro.resolver_prazo({"prazo_semana": "S99"}, semanas) is None


# ---------------------------------------------------------------------------
# Injecao nos blocos
# ---------------------------------------------------------------------------


MOLDE = """prosa antes, que ninguem deve tocar

<!-- QUADRO:inicio teste -->
conteudo velho
<!-- QUADRO:fim teste -->

prosa depois, que tambem nao
"""


def test_injetar_troca_so_o_miolo():
    saida = quadro.injetar(MOLDE, "teste", "conteudo novo")
    assert "conteudo novo" in saida
    assert "conteudo velho" not in saida
    assert "prosa antes, que ninguem deve tocar" in saida
    assert "prosa depois, que tambem nao" in saida


def test_injetar_e_idempotente():
    """Gerar duas vezes tem de dar o mesmo arquivo, ou o check vira ruido."""
    uma = quadro.injetar(MOLDE, "teste", "conteudo novo")
    duas = quadro.injetar(uma, "teste", "conteudo novo")
    assert uma == duas


def test_injetar_sem_marcador_falha():
    """Marcador apagado por engano precisa parar a execucao, nao ser ignorado."""
    with pytest.raises(SystemExit):
        quadro.injetar("texto sem marcador nenhum", "teste", "x")


def test_todo_bloco_declarado_tem_desenhista():
    for nomes in quadro.BLOCOS.values():
        for nome in nomes:
            assert nome in quadro.DESENHISTAS, f"bloco {nome!r} sem funcao que o desenhe"


# ---------------------------------------------------------------------------
# A duplicacao que sobrou, e a conferencia dela
# ---------------------------------------------------------------------------


def test_semanas_do_toml_aparecem_no_cronograma(dados):
    """A tabela das onze semanas continua a mao: aqui se confere que nao divergiu."""
    assert quadro.checar_semanas_no_cronograma(dados) == []


def test_semana_divergente_e_apontada():
    """E o teste do proprio verificador: ele precisa saber acusar."""
    inventada = {
        "semana": [
            {
                "id": "S99",
                "inicio": datetime.date(2030, 1, 1),
                "fim": datetime.date(2030, 1, 7),
            }
        ]
    }
    assert quadro.checar_semanas_no_cronograma(inventada) != []


# ---------------------------------------------------------------------------
# A pagina inteira
# ---------------------------------------------------------------------------


def test_render_e_estavel(dados):
    """Mesma data, mesmo arquivo. Sem isso o --conferir acusaria mudanca falsa."""
    assert quadro.render_quadro(dados, HOJE) == quadro.render_quadro(dados, HOJE)


def test_render_grava_a_data_do_retrato(dados):
    pagina = quadro.render_quadro(dados, HOJE)
    achado = quadro.RE_MARCA_DATA.search(pagina)
    assert achado, "a pagina precisa gravar a data, senao --conferir nao funciona"
    assert achado.group(1) == "2026-09-26"


def test_todo_cartao_cai_em_alguma_coluna(dados):
    validas = {chave for chave, _, _ in quadro.COLUNAS}
    for cartao in quadro.cartoes(dados, HOJE):
        assert cartao[0] in validas, f"coluna desconhecida: {cartao[0]!r}"


def test_nenhum_item_do_toml_desaparece(dados):
    """Cartao que nao cai em coluna nenhuma sai do quadro sem avisar."""
    esperado = (
        len(dados.get("tarefa_professor", []))
        + len(dados.get("marco", []))
        + len(dados.get("semana", []))
        + len(dados.get("capitulo", []))
        + len(dados.get("decisao", []))
    )
    assert len(quadro.cartoes(dados, HOJE)) == esperado


def test_celula_nao_quebra_a_tabela():
    assert quadro.celula("a | b") == "a \\| b"
    assert quadro.celula("linha\nquebrada") == "linha quebrada"
