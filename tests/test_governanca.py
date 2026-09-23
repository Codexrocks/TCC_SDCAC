"""Testes do verificador de governanca.

Duas regras sao testadas aqui: a declaracao de IA no corpo do Pull Request e a
espera de 24 h com justificativa para mexer nas regras do projeto.

A segunda e a que protege todas as outras. Se ela quebrar em silencio, um unico
PR passa a conseguir desligar as travas — que e exatamente o cenario que ela
existe para impedir.
"""
from datetime import datetime, timedelta, timezone

import pytest

import governanca


@pytest.fixture(autouse=True)
def limpa_estado():
    governanca.erros.clear()
    yield
    governanca.erros.clear()


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
# Arquivo protegido: espera e justificativa
#
# Ate 23/09/2026 esta secao testava duas aprovacoes. Com uma pessoa so, e o
# GitHub recusando que alguem aprove o proprio PR, aquela regra virou
# impossivel de cumprir. No lugar dela entraram a espera de 24 h e a secao
# "Arquivo protegido" no corpo do PR.
#
# O relogio entra por parametro justamente para o teste nao depender da hora em
# que ele roda.
# ---------------------------------------------------------------------------

AGORA = datetime(2026, 9, 23, 12, 0, tzinfo=timezone.utc)
RECEM_ABERTO = AGORA - timedelta(hours=1)
ESPERA_CUMPRIDA = AGORA - timedelta(hours=25)

PROTEGIDO_OK = """## Arquivo protegido

- **O que muda:** o governanca.py conta espera em vez de aprovacao
- **Por que agora:** o trabalho passou a ser de uma pessoa so
- **O que segura no lugar:** as 24 h de espera e esta justificativa
"""


def test_arquivo_comum_nao_exige_nada():
    governanca.checar_arquivo_protegido(
        ["docs/arquitetura.md"], "", RECEM_ABERTO, AGORA
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
def test_arquivo_protegido_recem_aberto_espera(arquivo):
    governanca.checar_arquivo_protegido([arquivo], PROTEGIDO_OK, RECEM_ABERTO, AGORA)
    assert len(governanca.erros) == 1
    assert "faltam 23.0 h" in governanca.erros[0]


def test_espera_cumprida_com_a_secao_preenchida_passa():
    governanca.checar_arquivo_protegido(
        ["scripts/validar.py"], PROTEGIDO_OK, ESPERA_CUMPRIDA, AGORA
    )
    assert governanca.erros == []


def test_o_limite_exato_das_24_h_ja_passa():
    """24 h cravadas contam como cumpridas; abaixo disso, nao."""
    governanca.checar_arquivo_protegido(
        ["AGENTS.md"], PROTEGIDO_OK, AGORA - timedelta(hours=24), AGORA
    )
    assert governanca.erros == []


def test_sem_a_secao_reprova_mesmo_depois_da_espera():
    governanca.checar_arquivo_protegido(
        ["scripts/validar.py"], "## O que muda\n\nmexi num script\n", ESPERA_CUMPRIDA, AGORA
    )
    assert len(governanca.erros) == 1
    assert "Arquivo protegido" in governanca.erros[0]


def test_campos_em_branco_reprovam():
    corpo = (
        "## Arquivo protegido\n\n"
        "- **O que muda:**\n"
        "- **Por que agora:**\n"
        "- **O que segura no lugar:**\n"
    )
    governanca.checar_arquivo_protegido(["AGENTS.md"], corpo, ESPERA_CUMPRIDA, AGORA)
    assert len(governanca.erros) == 3
    assert all("em branco" in e for e in governanca.erros)


def test_falta_o_campo_do_que_segura_no_lugar():
    """O campo que importa: afrouxar sem repor e o que a regra existe para pegar."""
    corpo = PROTEGIDO_OK.replace(
        "- **O que segura no lugar:** as 24 h de espera e esta justificativa\n", ""
    )
    governanca.checar_arquivo_protegido(["AGENTS.md"], corpo, ESPERA_CUMPRIDA, AGORA)
    assert len(governanca.erros) == 1
    assert "O que segura no lugar" in governanca.erros[0]


def test_qualquer_arquivo_dentro_de_github_ou_scripts_conta():
    governanca.checar_arquivo_protegido(
        ["scripts/atividade.py"], PROTEGIDO_OK, RECEM_ABERTO, AGORA
    )
    assert governanca.erros != []
    governanca.erros.clear()
    governanca.checar_arquivo_protegido(
        [".github/CODEOWNERS"], PROTEGIDO_OK, RECEM_ABERTO, AGORA
    )
    assert governanca.erros != []


def test_arquivo_parecido_nao_e_protegido():
    """A regra vale para os caminhos exatos, nao para nomes parecidos."""
    governanca.checar_arquivo_protegido(
        ["docs/padroes-de-escrita.md", "documentacao/scripts/algo.py"],
        "",
        RECEM_ABERTO,
        AGORA,
    )
    assert governanca.erros == []


def test_a_secao_protegido_tambem_vale_com_crlf():
    governanca.checar_arquivo_protegido(
        ["AGENTS.md"], crlf(PROTEGIDO_OK), ESPERA_CUMPRIDA, AGORA
    )
    assert governanca.erros == []


# ---------------------------------------------------------------------------
# Renomeacao
#
# A API de arquivos do PR poe o caminho novo em `filename` e o antigo em
# `previous_filename`. O verificador lia so o novo, entao mover um arquivo
# protegido para fora da lista escapava da dupla aprovacao.
#
# Status, filename e previous_filename abaixo sao os de uma entrada real, nao
# inventada: a renomeacao de .gitbook.yaml para gitbook-docs.yaml (commit
# 04c68fb), como a API de compare do GitHub a devolve. Nenhum PR deste
# repositorio renomeou arquivo ate hoje, entao nao havia exemplo vindo de PR.
#
# Que /pulls/{n}/files traz os mesmos tres campos foi conferido numa resposta
# real, e nao presumido: no PR cli/cli#14116, a entrada de
# .github/skills/code-review/SKILL.md vem com status "renamed", filename e
# previous_filename.
# ---------------------------------------------------------------------------

RENOMEACAO_REAL = {
    "status": "renamed",
    "filename": "gitbook-docs.yaml",
    "previous_filename": ".gitbook.yaml",
}


def renomeacao(de, para):
    """A entrada real acima, com outros caminhos."""
    return {**RENOMEACAO_REAL, "previous_filename": de, "filename": para}


def test_caminhos_tocados_inclui_a_origem_da_renomeacao():
    assert governanca.caminhos_tocados([RENOMEACAO_REAL]) == [
        "gitbook-docs.yaml",
        ".gitbook.yaml",
    ]


def test_caminhos_tocados_sem_renomeacao_devolve_so_o_filename():
    """Entrada que nao e renomeacao nao traz a chave — e nada de None na lista."""
    itens = [
        {"status": "added", "filename": "docs/novo.md"},
        {"status": "removed", "filename": "docs/velho.md"},
        {"status": "modified", "filename": "README.md"},
    ]
    assert governanca.caminhos_tocados(itens) == [
        "docs/novo.md",
        "docs/velho.md",
        "README.md",
    ]


@pytest.mark.parametrize(
    ("de", "para"),
    [
        ("AGENTS.md", "docs/regras.md"),
        (".github/workflows/validacao.yml", "docs/validacao.yml"),
        ("scripts/validar.py", "ferramentas/validar.py"),
    ],
)
def test_mover_arquivo_protegido_para_fora_cai_na_regra(de, para):
    """O caso que escapava: so o destino era lido, e o destino nao e protegido."""
    arquivos = governanca.caminhos_tocados([renomeacao(de, para)])
    governanca.checar_arquivo_protegido(arquivos, PROTEGIDO_OK, RECEM_ABERTO, AGORA)
    assert len(governanca.erros) == 1
    assert "faltam" in governanca.erros[0]


def test_renomear_entre_caminhos_comuns_nao_cai_na_regra():
    arquivos = governanca.caminhos_tocados([renomeacao("docs/a.md", "docs/b.md")])
    governanca.checar_arquivo_protegido(arquivos, "", RECEM_ABERTO, AGORA)
    assert governanca.erros == []


def test_caminhos_tocados_nao_repete_caminho():
    """Renomear A para B e criar outro A no mesmo PR deixa A duas vezes na API.

    Apontado pelo revisor automatico no PR #34: sem tirar a repeticao, o log
    listava o mesmo arquivo protegido duas vezes.
    """
    itens = [
        renomeacao("AGENTS.md", "docs/regras.md"),
        {"status": "added", "filename": "AGENTS.md"},
    ]
    assert governanca.caminhos_tocados(itens) == ["docs/regras.md", "AGENTS.md"]


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
        "- **Conferi tudo que a IA escreveu:** `\n"
    )
    governanca.checar_declaracao_ia(corpo)
    assert len(governanca.erros) == 4, (
        "espaco, tabulacao e enfeite de Markdown nao sao resposta"
    )


def test_traco_sozinho_e_resposta_valida():
    """Um traco quer dizer 'nao se aplica', e reprova-lo insultava quem respondeu.

    Veio do PR #10: o campo 'No que ajudou' foi preenchido com '-' e o check
    disse que estava em branco, porque o hifen entrava no strip de enfeites.
    """
    for traco in ("-", "–", "—"):
        governanca.erros.clear()
        corpo = (
            "## Uso de IA\n\n"
            "- **IA usada:** nenhuma\n"
            f"- **No que ajudou:** {traco}\n"
            "- **O que é meu:** a linha inteira\n"
            "- **Conferi tudo que a IA escreveu:** não se aplica\n"
        )
        governanca.checar_declaracao_ia(corpo)
        assert governanca.erros == [], f"{traco!r} sozinho e resposta: 'nao se aplica'"


def test_exemplo_citado_em_bloco_de_codigo_nao_conta_como_resposta():
    """O PR #11 se auto-reprovou citando o campo do PR #10 para explicar o bug.

    O `search` pega a primeira ocorrencia do campo em todo o corpo, entao a
    citacao dentro do bloco de codigo era lida como se fosse a resposta.
    Qualquer PR que documente o proprio formulario caia nisso.
    """
    corpo = (
        "## Uso de IA\n\n"
        "Explicando o que aconteceu no outro PR:\n\n"
        "```\n"
        "- **No que ajudou:** \n"
        "```\n\n"
        "- **IA usada:** Claude Opus 5\n"
        "- **No que ajudou:** escreveu os testes\n"
        "- **O que é meu:** o diagnóstico\n"
        "- **Conferi tudo que a IA escreveu:** sim\n"
    )
    governanca.checar_declaracao_ia(corpo)
    assert governanca.erros == [], "exemplo citado nao e resposta dada"


def test_campo_fora_da_secao_nao_vale():
    """O formulario e a secao. Campo solto em outra parte do PR nao responde."""
    corpo = (
        "## O que muda\n\n"
        "- **IA usada:** Claude Opus 5\n"
        "- **No que ajudou:** tudo\n"
        "- **O que é meu:** nada\n"
        "- **Conferi tudo que a IA escreveu:** sim\n\n"
        "## Uso de IA\n\n"
        "- **IA usada:** \n"
        "- **No que ajudou:** \n"
        "- **O que é meu:** \n"
        "- **Conferi tudo que a IA escreveu:** \n"
    )
    governanca.checar_declaracao_ia(corpo)
    assert len(governanca.erros) == 4, "vale o que esta na secao, nao fora dela"


def test_varios_tracos_seguidos_continuam_reprovando():
    """'---' e linha horizontal do Markdown, nao resposta."""
    corpo = (
        "## Uso de IA\n\n"
        "- **IA usada:** ---\n"
        "- **No que ajudou:** --\n"
        "- **O que é meu:** ————\n"
        "- **Conferi tudo que a IA escreveu:** sim\n"
    )
    governanca.checar_declaracao_ia(corpo)
    assert len(governanca.erros) == 3, "traco repetido e enfeite, nao resposta"


def test_sem_comentarios_normaliza_fim_de_linha():
    assert "\r" not in governanca.sem_comentarios("linha\r\noutra\rterceira")
