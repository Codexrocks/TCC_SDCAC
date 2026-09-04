"""Testes do verificador de governanca.

Duas regras sao testadas aqui: a declaracao de IA no corpo do Pull Request e a
exigencia de duas aprovacoes para mexer nas regras do projeto.

A segunda e a que protege todas as outras. Se ela quebrar em silencio, um unico
PR passa a conseguir desligar as travas — que e exatamente o cenario que ela
existe para impedir.
"""
import pytest

import governanca


@pytest.fixture(autouse=True)
def limpa_estado():
    governanca.erros.clear()
    yield
    governanca.erros.clear()


def review(login, estado):
    return {"user": {"login": login}, "state": estado}


# ---------------------------------------------------------------------------
# Declaracao de IA no corpo do PR
# ---------------------------------------------------------------------------

PREENCHIDO = """## Uso de IA

- **IA usada:** Gemini 2.5 Pro
- **No que ajudou:** rascunhou a seção 2
- **O que é meu:** a escolha das fontes e a análise
- **Conferi tudo que a IA escreveu:** sim
"""

SEM_IA = """## Uso de IA

- **IA usada:** nenhuma
- **No que ajudou:** nada
- **O que é meu:** tudo
- **Conferi tudo que a IA escreveu:** não se aplica
"""

TEMPLATE_INTACTO = """## Uso de IA

- **IA usada:** <!-- ex.: Claude Opus 5 -->
- **No que ajudou:** <!-- seja específico -->
- **O que é meu:** <!-- o que você pensou -->
- **Conferi tudo que a IA escreveu:** <!-- sim / não -->
"""


def test_declaracao_preenchida_passa():
    governanca.checar_declaracao_ia(PREENCHIDO)
    assert governanca.erros == []


def test_nenhuma_ia_e_resposta_valida():
    """Nao usar IA e legitimo; o que nao pode e deixar em branco."""
    governanca.checar_declaracao_ia(SEM_IA)
    assert governanca.erros == []


def test_template_deixado_intacto_reprova():
    """So os comentarios do template nao sao resposta."""
    governanca.checar_declaracao_ia(TEMPLATE_INTACTO)
    assert len(governanca.erros) == 4
    assert all("em branco" in e for e in governanca.erros)


def test_campo_faltando_reprova():
    corpo = PREENCHIDO.replace("- **O que é meu:** a escolha das fontes e a análise\n", "")
    governanca.checar_declaracao_ia(corpo)
    assert len(governanca.erros) == 1
    assert "O que é meu" in governanca.erros[0]


def test_secao_ausente_reprova():
    governanca.checar_declaracao_ia("## O que muda\n\nmexi num arquivo\n")
    assert len(governanca.erros) == 1
    assert "Uso de IA" in governanca.erros[0]


def test_corpo_vazio_reprova():
    governanca.checar_declaracao_ia("")
    assert governanca.erros != []


def test_aceita_sem_negrito():
    """O template usa negrito, mas quem escrever na mao nao deve ser punido."""
    corpo = """## Uso de IA

- IA usada: Copilot
- No que ajudou: autocompletou o script
- O que é meu: a lógica e os testes
- Conferi tudo que a IA escreveu: sim
"""
    governanca.checar_declaracao_ia(corpo)
    assert governanca.erros == []


# ---------------------------------------------------------------------------
# Dupla aprovacao
# ---------------------------------------------------------------------------


def test_arquivo_comum_basta_uma_aprovacao():
    governanca.checar_dupla_aprovacao(
        ["docs/arquitetura.md", "docs/relatorios/2026-09-03-sessao-01.md"],
        [],
        "davi",
    )
    assert governanca.erros == []


@pytest.mark.parametrize(
    "arquivo",
    [
        "AGENTS.md",
        "CLAUDE.md",
        "CONTRIBUTING.md",
        "docs/padroes.md",
        "docs/padroes-codigo.md",
        "docs/processo.md",
        ".github/workflows/validacao.yml",
        ".github/pull_request_template.md",
        "scripts/validar.py",
        "scripts/governanca.py",
    ],
)
def test_arquivo_protegido_exige_duas_aprovacoes(arquivo):
    governanca.checar_dupla_aprovacao([arquivo], [], "davi")
    assert len(governanca.erros) == 1
    assert "2 aprovacoes" in governanca.erros[0]


def test_uma_aprovacao_nao_basta_em_arquivo_protegido():
    governanca.checar_dupla_aprovacao(
        ["scripts/validar.py"], [review("yasmin", "APPROVED")], "davi"
    )
    assert len(governanca.erros) == 1
    assert "faltam 1" in governanca.erros[0]


def test_duas_aprovacoes_passam():
    governanca.checar_dupla_aprovacao(
        ["scripts/validar.py"],
        [review("yasmin", "APPROVED"), review("felipe", "APPROVED")],
        "davi",
    )
    assert governanca.erros == []


def test_autor_nao_conta_como_aprovador():
    """Ninguem se auto-aprova, nem quando o GitHub deixa registrar o review."""
    governanca.checar_dupla_aprovacao(
        ["AGENTS.md"],
        [review("davi", "APPROVED"), review("yasmin", "APPROVED")],
        "davi",
    )
    assert len(governanca.erros) == 1
    assert "faltam 1" in governanca.erros[0]


def test_mesma_pessoa_aprovando_duas_vezes_conta_uma():
    governanca.checar_dupla_aprovacao(
        ["AGENTS.md"],
        [review("yasmin", "APPROVED"), review("yasmin", "APPROVED")],
        "davi",
    )
    assert len(governanca.erros) == 1


def test_quem_aprovou_e_depois_pediu_mudancas_nao_conta():
    """Vale a posicao mais recente de cada pessoa, nao a primeira."""
    governanca.checar_dupla_aprovacao(
        ["AGENTS.md"],
        [
            review("yasmin", "APPROVED"),
            review("felipe", "APPROVED"),
            review("felipe", "CHANGES_REQUESTED"),
        ],
        "davi",
    )
    assert len(governanca.erros) == 1
    assert "faltam 1" in governanca.erros[0]


def test_comentario_nao_derruba_aprovacao_anterior():
    """Comentar depois de aprovar nao e mudar de posicao."""
    governanca.checar_dupla_aprovacao(
        ["AGENTS.md"],
        [
            review("yasmin", "APPROVED"),
            review("felipe", "APPROVED"),
            review("felipe", "COMMENTED"),
        ],
        "davi",
    )
    assert governanca.erros == []


def test_qualquer_arquivo_dentro_de_github_ou_scripts_conta():
    governanca.checar_dupla_aprovacao(["scripts/atividade.py"], [], "davi")
    assert governanca.erros != []
    governanca.erros.clear()
    governanca.checar_dupla_aprovacao([".github/CODEOWNERS"], [], "davi")
    assert governanca.erros != []


def test_arquivo_parecido_nao_e_protegido():
    """A regra vale para os caminhos exatos, nao para nomes parecidos."""
    governanca.checar_dupla_aprovacao(
        ["docs/padroes-de-escrita.md", "documentacao/scripts/algo.py"], [], "davi"
    )
    assert governanca.erros == []


# ---------------------------------------------------------------------------
# Fim de linha CRLF
#
# O GitHub devolve o corpo do Pull Request com CRLF. Os testes acima usam "\n"
# porque as strings foram escritas aqui — e foi essa diferenca que deixou passar
# o PR #5 com os quatro campos em branco e o check verde.
#
# A licao: teste com dado que voce mesmo inventou nao prova que funciona com o
# dado de verdade.
# ---------------------------------------------------------------------------


def crlf(texto):
    return texto.replace("\n", "\r\n")


def test_template_intacto_reprova_tambem_com_crlf():
    """O caso que escapou: o \r sobrava no campo e parecia resposta."""
    governanca.checar_declaracao_ia(crlf(TEMPLATE_INTACTO))
    assert len(governanca.erros) == 4
    assert all("em branco" in e for e in governanca.erros)


def test_declaracao_preenchida_passa_com_crlf():
    governanca.checar_declaracao_ia(crlf(PREENCHIDO))
    assert governanca.erros == []


def test_secao_ausente_reprova_com_crlf():
    governanca.checar_declaracao_ia(crlf("## O que muda\n\nmexi num arquivo\n"))
    assert len(governanca.erros) == 1
    assert "Uso de IA" in governanca.erros[0]


def test_campo_so_com_espaco_ou_tabulacao_reprova():
    corpo = (
        "## Uso de IA\n\n"
        "- **IA usada:**   \n"
        "- **No que ajudou:** \t \n"
        "- **O que é meu:** ***\n"
        "- **Conferi tudo que a IA escreveu:** -\n"
    )
    governanca.checar_declaracao_ia(corpo)
    assert len(governanca.erros) == 4, (
        "espaco, tabulacao e enfeite de Markdown nao sao resposta"
    )


def test_sem_comentarios_normaliza_fim_de_linha():
    assert "\r" not in governanca.sem_comentarios("linha\r\noutra\rterceira")
