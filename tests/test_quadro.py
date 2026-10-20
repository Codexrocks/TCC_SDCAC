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
        (datetime.date(2026, 9, 25), "atrasado"),  # ontem
        (datetime.date(2026, 9, 26), "a-vencer"),  # hoje ainda da
        (datetime.date(2026, 10, 3), "a-vencer"),  # exatamente 7 dias
        (datetime.date(2026, 10, 4), "depois"),  # 8 dias ja e depois
        (None, "depois"),  # sem prazo nao desaparece
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
    assert (
        quadro.resolver_prazo({"prazo_semana": "S8"}, semanas) == semanas["S8"]["fim"]
    )


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
            assert nome in quadro.DESENHISTAS, (
                f"bloco {nome!r} sem funcao que o desenhe"
            )


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


# ---------------------------------------------------------------------------
# Coerencia entre o quadro.toml e as paginas escritas a mao
#
# Cada uma destas checagens nasceu de uma divergencia real que passou por todos
# os checks que ja existiam. Os testes vem em par: o repositorio esta limpo E o
# verificador sabe acusar. So o primeiro seria um check que nunca dispara.
# ---------------------------------------------------------------------------


def test_citacoes_batem_com_o_indice(dados):
    assert quadro.checar_citacoes_no_indice(dados) == []


def test_citacao_a_menos_e_apontada(dados):
    """Foi o caso de 28/09: 20 linhas entraram no indice e nao no TOML."""
    magro = dict(dados)
    magro["citacao"] = dados["citacao"][:-1]
    problemas = quadro.checar_citacoes_no_indice(magro)
    assert problemas, "tirar uma citacao do TOML tem de acusar"
    assert any("pendencia" in p for p in problemas)


def test_citacao_com_dono_trocado_e_apontada(dados):
    """Contagem igual e dono diferente tambem e divergencia."""
    trocado = dict(dados)
    copia = [dict(c) for c in dados["citacao"]]
    copia[0]["dono"] = "Ninguem"
    trocado["citacao"] = copia
    assert quadro.checar_citacoes_no_indice(trocado), "dono trocado tem de acusar"


def test_marcadores_batem_com_o_indice(dados):
    assert quadro.checar_marcadores_no_indice(dados) == []


def test_marcador_sem_linha_e_apontado(dados):
    """Foi o caso de 26/09: marcador indexado na secao errada, contagem cega."""
    magro = dict(dados)
    magro["citacao"] = [
        c for c in dados["citacao"] if not c["onde"].startswith("docs/usabilidade.md")
    ]
    assert quadro.checar_marcadores_no_indice(magro), "marcador orfao tem de acusar"


def test_nenhum_titulo_datado_a_mao():
    assert quadro.checar_titulo_datado() == []


@pytest.mark.parametrize(
    "titulo",
    [
        "## Onde estamos, em 28/09",
        "### Situacao em 01/10/2026",
        "# Retrato, em 05/12",
    ],
)
def test_titulo_datado_e_reconhecido(titulo):
    assert quadro.RE_TITULO_DATADO.findall(titulo), f"deveria pegar {titulo!r}"


@pytest.mark.parametrize(
    "titulo",
    ["## Onde estamos", "## Prazos do professor", "### D-13 · Tratamento"],
)
def test_titulo_sem_data_passa(titulo):
    assert not quadro.RE_TITULO_DATADO.findall(titulo)


def test_tabelas_de_pendencia_le_os_quatro_formatos():
    """O indice tem quatro formatos de tabela; o parser nao conhece nenhum."""
    texto = (
        "| Onde | O que falta | Quem | Desde |\n|---|---|---|---|\n"
        "| a.md | falta x | Yasmin | 01/01/2026 |\n\n"
        "| Chamada | Onde | Quem | Desde |\n|---|---|---|---|\n"
        "| (X, 2020) | 2.1 | Davi | 02/01/2026 |\n\n"
        "| Coluna | Sem | Data |\n|---|---|---|\n"
        "| nao | conta | aqui |\n"
    )
    linhas = quadro.tabelas_de_pendencia(texto)
    assert len(linhas) == 2, "so as tabelas com coluna Desde contam"
    cab, corpo = linhas[0]
    assert corpo[cab.index("Quem")] == "Yasmin"


def test_sem_codigo_ignora_mencao_ao_marcador():
    """Explicar o marcador nao e usa-lo — a pagina de regra nao vira pendencia."""
    assert "FALTA" not in quadro.sem_codigo("use `FALTA CITAÇÃO` na linha")
    assert "FALTA" in quadro.sem_codigo("<!-- FALTA CITAÇÃO --> conferir")


# ---------------------------------------------------------------------------
# O bloco de pendencias por pessoa, na pagina inicial
# ---------------------------------------------------------------------------

# Data propria destes casos: nao reutiliza o HOJE do topo, que é de 26/09 e
# sustenta os testes de fronteira de prazo.
HOJE_PENDENCIAS = datetime.date(2026, 10, 16)


def _dados_falsos(decisoes):
    """O minimo que o desenhista le, para o caso nao depender do quadro.toml real."""
    return {"decisao": decisoes, "semana": []}


def test_a_pendencia_aparece_sob_cada_dono():
    """Decisao de tres donos e pendencia dos tres, e nao de um escolhido.

    Era o comportamento da lista escrita a mao, e quem a lia procurava o proprio
    nome. Agrupar por dono unico esconderia a D-15 de duas das tres pessoas.
    """
    bloco = quadro.bloco_pendencias_por_pessoa(
        _dados_falsos(
            [
                {
                    "id": "D-15",
                    "titulo": "Critério a priori",
                    "estado": "aberta",
                    "donos": ["Davi", "Yasmin", "Filipe"],
                }
            ]
        ),
        HOJE_PENDENCIAS,
    )
    for pessoa in ("Davi", "Yasmin", "Filipe"):
        assert f"**{pessoa}**" in bloco
    assert bloco.count("D-15") == 3


def test_decisao_fechada_nao_entra():
    """O par do teste acima: o bloco precisa de fato filtrar.

    Foi o defeito que motivou gerar esta secao — a pagina anunciava a D-02, a
    D-12 e a D-14 como abertas depois de as tres fecharem.
    """
    bloco = quadro.bloco_pendencias_por_pessoa(
        _dados_falsos(
            [
                {
                    "id": "D-02",
                    "titulo": "Painel",
                    "estado": "fechada",
                    "donos": ["Filipe"],
                }
            ]
        ),
        HOJE_PENDENCIAS,
    )
    assert "D-02" not in bloco
    assert "Nenhuma decisao aberta" in bloco


def test_dono_fora_da_equipe_nao_desaparece():
    """Pessoa nova no projeto nao pode sumir da pagina inicial.

    A ordem de exibicao vem de uma constante. Se a constante fosse tambem o
    filtro, alguem que entrasse na equipe ficaria invisivel ate alguem lembrar
    de editar o script — defeito silencioso, que e o pior tipo.
    """
    bloco = quadro.bloco_pendencias_por_pessoa(
        _dados_falsos(
            [
                {
                    "id": "D-99",
                    "titulo": "Alguma coisa",
                    "estado": "aberta",
                    "donos": ["Convidado"],
                }
            ]
        ),
        HOJE_PENDENCIAS,
    )
    assert "**Convidado**" in bloco
    assert "D-99" in bloco


def test_cada_nome_tem_linha_em_branco_antes_da_tabela():
    """Sem a linha em branco, o Markdown engole o nome dentro da tabela anterior.

    Foi exatamente o que a primeira versao deste bloco fez, e nenhum check
    pegaria: o arquivo continuaria valido, so renderizaria errado no GitBook.
    """
    bloco = quadro.bloco_pendencias_por_pessoa(
        _dados_falsos(
            [
                {"id": "D-1", "titulo": "Um", "estado": "aberta", "donos": ["Davi"]},
                {
                    "id": "D-2",
                    "titulo": "Dois",
                    "estado": "aberta",
                    "donos": ["Yasmin"],
                },
            ]
        ),
        HOJE_PENDENCIAS,
    )
    linhas = bloco.splitlines()
    for i, linha in enumerate(linhas):
        if linha.startswith("**") and i > 0:
            assert linhas[i - 1].strip() == "", (
                f"falta linha em branco antes de {linha}"
            )
        if linha.startswith("**"):
            assert linhas[i + 1].strip() == "", (
                f"falta linha em branco depois de {linha}"
            )


def test_a_pagina_inicial_tem_os_marcadores(dados):
    """O bloco so chega ao GitBook se os marcadores existirem na pagina.

    Marcador apagado por engano — numa resolucao de conflito, por exemplo, que
    foi o que aconteceu com o `capitulos` em 28/09 — faria o bloco deixar de ser
    escrito sem erro nenhum.
    """
    texto = (quadro.RAIZ / "docs" / "README.md").read_text(encoding="utf-8")
    assert "<!-- QUADRO:inicio pendencias-por-pessoa -->" in texto
    assert "<!-- QUADRO:fim pendencias-por-pessoa -->" in texto
    assert "docs/README.md" in quadro.BLOCOS
