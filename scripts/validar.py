#!/usr/bin/env python3
"""Valida as regras do TCC_SDCAC.

Uso:
    python3 scripts/validar.py            # valida a branch atual contra a main
    python3 scripts/validar.py --base X   # compara com outra base

Confere: nome de branch, formato dos commits, cobertura do SUMMARY.md,
links internos e segredos vazados. Sai com codigo 1 se algo falhar.
"""
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPOS = ("docs", "feat", "fix", "chore")
# Quem pode abrir branch. O prefixo diz de quem e o trabalho sem precisar abrir
# o log. Entrou alguem novo no projeto? Acrescente aqui, senao a branch dele
# nao passa na validacao.
#
# "gitbook" nao e pessoa: e a branch permanente do Git Sync, onde o GitBook
# escreve as edicoes feitas pelo site. Ela nao pode ser apagada depois do merge,
# ao contrario das outras. Ver docs/configuracao.md.
#
# "felipe" e a grafia errada do nome do Filipe, e esta aqui SO enquanto esta
# correcao nao chega na main. O motivo e mecanico: os workflows validam cada PR
# com o validar.py da BASE, nao com o do proprio PR. Enquanto a main tiver a
# lista antiga, uma branch "filipe/..." seria reprovada com "nao esta na lista
# de autores" — e quem abriu ela nao teria como adivinhar por que.
# REMOVER assim que este arquivo estiver na main. Ver docs/equipe.md.
AUTORES = ("davi", "yasmin", "filipe", "claude", "gitbook", "felipe")
RE_BRANCH = re.compile(
    r"^(%s)/(%s)/[a-z0-9][a-z0-9-]*$" % ("|".join(AUTORES), "|".join(TIPOS))
)
RE_COMMIT = re.compile(r"^(%s): .{3,}$" % "|".join(TIPOS))
# Toda mensagem de commit declara quem ajudou. "Co-Authored-By" conta porque
# algumas ferramentas (Claude Code, Copilot) ja acrescentam essa linha sozinhas.
# Sem IA nenhuma? Escreva "Assistido-por: nenhuma" — silencio nao distingue
# "nao usei" de "esqueci". Regra em AGENTS.md, secao 3.
RE_IA = re.compile(r"^[ \t]*(assistido-por|co-authored-by)[ \t]*:[ \t]*\S+",
                   re.IGNORECASE | re.MULTILINE)

# O GitBook escreve na pasta artigo/ e gera as mensagens de commit sozinho:
# "GitBook: Export content from X" e "GITBOOK-SITE: Changes to Y". Elas nunca
# vao seguir "tipo: descricao" nem trazer Assistido-por, e nao ha como
# configurar isso — e comportamento do produto.
#
# EXCECAO DECLARADA, e o unico buraco conhecido nesta validacao: quem quisesse
# escapar da regra poderia forjar uma mensagem com esse prefixo. O que segura o
# caso e a revisao do Pull Request, onde o diff aparece, e nao esta regra.
#
# Motivo em docs/configuracao.md, secao 7.
RE_COMMIT_GITBOOK = re.compile(r"^(GitBook|GITBOOK-[A-Z]+):", re.IGNORECASE)

# Cada espaco do GitBook tem seu proprio SUMMARY. Pasta que nao esta aqui nao e
# publicada, e seus .md nao precisam estar em indice nenhum.
ESPACOS = ("docs", "artigo")
RE_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")

SEGREDOS = [
    (re.compile(r"(?i)\b(senha|password|passwd)\s*[=:]\s*['\"]?[^\s'\"<>{}]{6,}"), "senha literal"),
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "chave de API"),
    (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "token do GitHub"),
    (re.compile(r"(?i)\bAKIA[0-9A-Z]{16}\b"), "chave AWS"),
    (re.compile(r"(?i)postgres(?:ql)?://[^\s:]+:[^\s@]+@"), "string de conexao com senha"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "chave privada"),
]

erros, avisos = [], []


def git(*args):
    try:
        r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def arquivos_md():
    saida = []
    for base, dirs, files in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv")]
        for f in files:
            if f.endswith(".md"):
                saida.append(os.path.join(base, f))
    return sorted(saida)


def checar_branch():
    b = os.environ.get("BRANCH_PR") or git("rev-parse", "--abbrev-ref", "HEAD")
    if not b or b in ("main", "HEAD"):
        return
    if RE_BRANCH.match(b):
        return
    autor = b.split("/")[0]
    if autor in TIPOS:
        # Padrao antigo, de antes de 03/09/2026: comecava pelo tipo.
        erros.append(
            f"branch '{b}': o padrao mudou, agora comeca pelo autor. "
            f"Use <autor>/{b}"
        )
    elif autor not in AUTORES:
        erros.append(
            f"branch '{b}': '{autor}' nao esta na lista de autores "
            f"({', '.join(AUTORES)}). Se entrou alguem novo, acrescente em "
            f"scripts/validar.py"
        )
    else:
        erros.append(
            f"branch '{b}' fora do padrao. Use <autor>/<tipo>/<assunto-com-hifen>, "
            f"com tipo em {'/'.join(TIPOS)}"
        )


def checar_commits(base):
    intervalo = f"{base}..HEAD"
    bruto = git("log", "--no-merges", "--format=%H%x1f%B%x1e", intervalo)
    if not bruto:
        return
    for registro in bruto.split("\x1e"):
        registro = registro.strip("\n")
        if not registro:
            continue
        sha, _, mensagem = registro.partition("\x1f")
        linhas = mensagem.strip().splitlines()
        assunto = linhas[0] if linhas else ""

        if RE_COMMIT_GITBOOK.match(assunto):
            # Commit do GitBook: formato e declaracao de IA nao se aplicam.
            avisos.append(f"commit {sha[:8]}: gerado pelo GitBook, formato nao verificado")
            continue

        if not RE_COMMIT.match(assunto):
            erros.append(f"commit {sha[:8]}: '{assunto}' fora do padrao 'tipo: descricao'")
        elif len(assunto) > 72:
            avisos.append(f"commit {sha[:8]}: assunto com {len(assunto)} caracteres (limite 72)")

        if not RE_IA.search(mensagem):
            erros.append(
                f"commit {sha[:8]}: falta declarar a IA. Acrescente ao corpo do "
                f"commit a linha 'Assistido-por: <nome da IA>' — ou "
                f"'Assistido-por: nenhuma' se trabalhou sem. Ver AGENTS.md secao 3"
            )


def checar_summary():
    for espaco in ESPACOS:
        base = os.path.join(RAIZ, espaco)
        sm = os.path.join(base, "SUMMARY.md")
        if not os.path.exists(sm):
            erros.append(f"{espaco}/SUMMARY.md nao existe")
            continue
        with open(sm, encoding="utf-8") as fh:
            conteudo = fh.read()
        listados = {os.path.normpath(m) for m in RE_LINK.findall(conteudo)}
        for caminho in arquivos_md():
            rel = os.path.relpath(caminho, base)
            if rel.startswith("..") or rel == "SUMMARY.md":
                continue
            if os.path.normpath(rel) not in listados:
                erros.append(f"{espaco}/{rel} nao esta no {espaco}/SUMMARY.md")


def checar_links():
    for caminho in arquivos_md():
        base = os.path.dirname(caminho)
        with open(caminho, encoding="utf-8") as fh:
            for n, linha in enumerate(fh, 1):
                for alvo in RE_LINK.findall(linha):
                    alvo = alvo.split("#")[0].strip()
                    if not alvo or alvo.startswith(("http", "mailto:", "<", "/")):
                        continue
                    if not os.path.exists(os.path.normpath(os.path.join(base, alvo))):
                        rel = os.path.relpath(caminho, RAIZ)
                        erros.append(f"{rel}:{n}: link quebrado -> {alvo}")


def checar_segredos():
    rastreados = git("ls-files").splitlines()
    for rel in rastreados:
        if rel.startswith("scripts/validar.py"):
            continue
        caminho = os.path.join(RAIZ, rel)
        if not os.path.isfile(caminho) or os.path.getsize(caminho) > 2_000_000:
            continue
        try:
            with open(caminho, encoding="utf-8") as fh:
                texto = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        for regex, rotulo in SEGREDOS:
            if regex.search(texto):
                erros.append(f"{rel}: possivel {rotulo} no arquivo")
        if os.path.basename(rel) == ".env":
            erros.append(f"{rel}: arquivo .env nao deve ser versionado")


def main():
    pedida = None
    if "--base" in sys.argv:
        pedida = sys.argv[sys.argv.index("--base") + 1]

    base = ""
    for candidata in ([pedida] if pedida else []) + ["origin/main", "main"]:
        if candidata and git("rev-parse", "--verify", candidata):
            base = candidata
            break

    checar_branch()
    if base:
        checar_commits(base)
    else:
        # Sem base nao da para saber quais commits sao novos. Nao passe calado:
        # em CI isso significaria aprovar commits sem conferir o formato.
        alvo = pedida or "origin/main"
        (erros if os.environ.get("CI") else avisos).append(
            f"nao foi possivel resolver a base '{alvo}'; commits nao verificados"
        )
    checar_summary()
    checar_links()
    checar_segredos()

    for a in avisos:
        print(f"  aviso  {a}")
    for e in erros:
        print(f"  ERRO   {e}")

    if erros:
        print(f"\nValidacao falhou: {len(erros)} erro(s), {len(avisos)} aviso(s).")
        print("Regras em docs/padroes.md")
        return 1
    print(f"Validacao OK ({len(avisos)} aviso(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
