"""Testes do validador de regras do repositorio.

Estes testes existem porque `scripts/validar.py` e o que faz as regras valerem.
Se uma expressao regular dele quebrar, o check continua verde e ninguem percebe
— e a partir dai qualquer coisa entra na main.
"""
import pytest

import validar


@pytest.fixture(autouse=True)
def limpa_estado():
    """O validador acumula erros em variaveis de modulo; zere entre os testes."""
    validar.erros.clear()
    validar.avisos.clear()
    yield
    validar.erros.clear()
    validar.avisos.clear()


# ---------------------------------------------------------------------------
# Nome de branch
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "branch",
    [
        "davi/feat/motor-deteccao",
        "yasmin/docs/referencial-teorico",
        "filipe/fix/faixa-risco-medio",
        "claude/chore/governanca-e-padroes",
        "gitbook/docs/documentacao",
        "davi/docs/a1",
    ],
)
def test_branch_valida(branch):
    assert validar.RE_BRANCH.match(branch), f"deveria aceitar {branch}"


@pytest.mark.parametrize(
    "branch",
    [
        "docs/referencial-teorico",       # padrao antigo, sem autor
        "joao/docs/teste",                # autor fora da lista
        "davi/docs",                      # falta o assunto
        "davi/feature/algo",              # tipo invalido
        "Davi/docs/algo",                 # maiuscula
        "davi/docs/Assunto",              # maiuscula no assunto
        "davi/docs/-comeca-com-hifen",
        "davi/docs/com espaco",
        "davi/docs/assunto/extra",        # nivel a mais
    ],
)
def test_branch_invalida(branch):
    assert not validar.RE_BRANCH.match(branch), f"nao deveria aceitar {branch}"


def test_branch_padrao_antigo_da_mensagem_util(monkeypatch):
    """Quem vem do padrao antigo precisa saber que ele mudou, nao que errou."""
    monkeypatch.setenv("BRANCH_PR", "docs/referencial-teorico")
    validar.checar_branch()
    assert len(validar.erros) == 1
    assert "o padrao mudou" in validar.erros[0]


def test_branch_autor_desconhecido_lista_os_validos(monkeypatch):
    monkeypatch.setenv("BRANCH_PR", "joao/docs/teste")
    validar.checar_branch()
    assert len(validar.erros) == 1
    assert "nao esta na lista de autores" in validar.erros[0]
    assert "davi" in validar.erros[0]


def test_branch_main_nao_e_avaliada(monkeypatch):
    monkeypatch.setenv("BRANCH_PR", "main")
    validar.checar_branch()
    assert validar.erros == []


# ---------------------------------------------------------------------------
# Mensagem de commit
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "assunto",
    [
        "docs: adiciona seção sobre UEBA",
        "feat: implementa regra de horário atípico",
        "fix: corrige faixa de severidade",
        "chore: atualiza dependências",
    ],
)
def test_commit_valido(assunto):
    assert validar.RE_COMMIT.match(assunto)


@pytest.mark.parametrize(
    "assunto",
    [
        "Atualizações",                      # sem tipo
        "docs: ab",                          # curto demais
        "Docs: adiciona seção",              # tipo com maiuscula
        "wip",
        "refactor: reorganiza pastas",       # tipo fora da lista
        "docs adiciona seção",               # falta o dois-pontos
    ],
)
def test_commit_invalido(assunto):
    assert not validar.RE_COMMIT.match(assunto)


# ---------------------------------------------------------------------------
# Declaracao de IA — AGENTS.md, secao 3
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mensagem",
    [
        "docs: algo\n\nAssistido-por: Claude Opus 5",
        "docs: algo\n\nAssistido-por: nenhuma",
        "docs: algo\n\nassistido-por: Gemini 2.5 Pro",          # minuscula
        "docs: algo\n\nAssistido-por:   Copilot",               # espaco extra
        "docs: algo\n\nCo-Authored-By: Claude <a@b.c>",         # ferramenta poe sozinha
        "docs: algo\n\ncorpo explicando\n\nAssistido-por: Grok",
    ],
)
def test_declaracao_de_ia_aceita(mensagem):
    assert validar.RE_IA.search(mensagem), f"deveria aceitar: {mensagem!r}"


@pytest.mark.parametrize(
    "mensagem",
    [
        "docs: algo",                                # nada declarado
        "docs: algo\n\nCorpo sem declaracao nenhuma",
        "docs: algo\n\nAssistido-por:",              # rotulo sem valor
        "docs: algo\n\nAssistido por: Claude",       # sem o hifen
        "docs: algo\n\nAssistido-por-alguem: x",
    ],
)
def test_declaracao_de_ia_recusada(mensagem):
    assert not validar.RE_IA.search(mensagem), f"nao deveria aceitar: {mensagem!r}"


def test_lista_de_autores_bate_com_a_documentacao():
    """Autor novo entra aqui e em docs/padroes.md — os dois nao podem divergir.

    "felipe" e transitorio: a grafia errada do nome do Filipe, aceita so ate
    esta correcao chegar na main. Ao remove-la de validar.py, remova daqui.
    """
    assert set(validar.AUTORES) == {
        "davi",
        "yasmin",
        "filipe",
        "claude",
        "gitbook",
        "felipe",
    }


# ---------------------------------------------------------------------------
# checar_commits sobre um repositorio de verdade
#
# Os testes acima cobrem as expressoes regulares isoladas. Faltava cobrir a
# funcao que as usa: um teste de mutacao mostrou que trocar a condicao de
# checar_commits por `if False:` desligava a regra sem quebrar teste nenhum.
# ---------------------------------------------------------------------------


def _repo(tmp_path, mensagens):
    """Cria um repositorio com um commit base e a lista de mensagens dada."""
    import subprocess

    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)

    def git(*args):
        subprocess.run(
            ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args],
            cwd=repo,
            check=True,
            capture_output=True,
        )

    git("init", "-q")
    (repo / "base.txt").write_text("base\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "-m", "chore: base", "-m", "Assistido-por: nenhuma")
    git("branch", "-M", "main")
    git("checkout", "-q", "-b", "davi/docs/teste")

    for i, mensagem in enumerate(mensagens):
        (repo / f"a{i}.txt").write_text("x\n", encoding="utf-8")
        git("add", "-A")
        git("commit", "-q", "-m", mensagem)

    return repo


def test_checar_commits_reprova_commit_sem_declaracao(tmp_path, monkeypatch):
    repo = _repo(tmp_path, ["docs: mudanca sem declarar a ia"])
    monkeypatch.setattr(validar, "RAIZ", str(repo))
    validar.checar_commits("main")
    assert len(validar.erros) == 1
    assert "falta declarar a IA" in validar.erros[0]


def test_checar_commits_aceita_commit_com_declaracao(tmp_path, monkeypatch):
    repo = _repo(tmp_path, ["docs: mudanca declarada\n\nAssistido-por: Grok 4"])
    monkeypatch.setattr(validar, "RAIZ", str(repo))
    validar.checar_commits("main")
    assert validar.erros == []


def test_checar_commits_reprova_assunto_fora_do_padrao(tmp_path, monkeypatch):
    repo = _repo(tmp_path, ["Atualizações\n\nAssistido-por: nenhuma"])
    monkeypatch.setattr(validar, "RAIZ", str(repo))
    validar.checar_commits("main")
    assert len(validar.erros) == 1
    assert "fora do padrao" in validar.erros[0]


def test_checar_commits_avalia_cada_commit_do_intervalo(tmp_path, monkeypatch):
    """Um commit bom no topo nao pode encobrir um ruim atras dele."""
    repo = _repo(
        tmp_path,
        [
            "docs: primeiro, sem declarar",
            "docs: segundo, declarado\n\nAssistido-por: nenhuma",
            "docs: terceiro, sem declarar",
        ],
    )
    monkeypatch.setattr(validar, "RAIZ", str(repo))
    validar.checar_commits("main")
    assert len(validar.erros) == 2
    assert all("falta declarar a IA" in e for e in validar.erros)


# ---------------------------------------------------------------------------
# Isencao dos commits do GitBook
#
# O GitBook escreve na pasta artigo/ e gera as mensagens sozinho, sem seguir
# "tipo: descricao" nem declarar IA. A isencao existe por isso — e e o unico
# buraco conhecido desta validacao, entao precisa ser ESTREITA.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "assunto",
    [
        "GitBook: Export content from Documentação",
        "GITBOOK-SITE: Changes to TCC_SDCAC Docs",
        "gitbook: export minusculo",
    ],
)
def test_reconhece_commit_do_gitbook(assunto):
    assert validar.RE_COMMIT_GITBOOK.match(assunto)


@pytest.mark.parametrize(
    "assunto",
    [
        "GitBooking: tentativa de imitar",       # prefixo parecido, sem os dois-pontos no lugar
        "docs: fala sobre o GitBook",            # menciona, mas nao comeca com ele
        "chore: ajusta GitBook: config",         # o prefixo nao esta no inicio
        "Sobre GitBook: alguma coisa",
    ],
)
def test_nao_confunde_com_commit_do_gitbook(assunto):
    assert not validar.RE_COMMIT_GITBOOK.match(assunto), (
        f"a isencao nao pode alcancar {assunto!r} — ela precisa ser estreita"
    )


def test_commit_do_gitbook_passa_com_aviso(tmp_path, monkeypatch):
    repo = _repo(tmp_path, ["GitBook: Export content from Documentação"])
    monkeypatch.setattr(validar, "RAIZ", str(repo))
    validar.checar_commits("main")
    assert validar.erros == []
    assert any("gerado pelo GitBook" in a for a in validar.avisos)


def test_commit_humano_nao_escapa_pela_isencao(tmp_path, monkeypatch):
    """A isencao vale para o GitBook, nao para quem quiser fugir da regra."""
    repo = _repo(tmp_path, ["docs: mudanca sem declarar ia"])
    monkeypatch.setattr(validar, "RAIZ", str(repo))
    validar.checar_commits("main")
    assert any("falta declarar a IA" in e for e in validar.erros)


def test_espacos_declarados():
    """Cada espaco do GitBook precisa do proprio SUMMARY conferido."""
    assert validar.ESPACOS == ("docs", "artigo")
