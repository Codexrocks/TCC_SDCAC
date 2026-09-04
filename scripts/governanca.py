#!/usr/bin/env python3
"""Confere as regras de governanca de um Pull Request.

Duas checagens, ambas descritas em AGENTS.md:

1. **Declaracao de IA** (secao 3) — o corpo do PR precisa dizer qual assistente
   foi usado, no que ajudou, o que e da pessoa, e se ela conferiu o resultado.
2. **Dupla aprovacao** (secao 4) — PR que mexe nas regras do projeto ou nas
   checagens automaticas exige duas aprovacoes, nao uma.

A segunda existe por um motivo especifico: sem ela, bastaria um PR editando o
validar.py para desligar todas as travas — e a IA que escreveu o PR seria a
mesma que sugeriu a mudanca. Duas pessoas precisam concordar em afrouxar a
coleira.

Uso, dentro do GitHub Actions:
    PR_NUMERO=12 REPO=dono/nome GITHUB_TOKEN=... python3 scripts/governanca.py
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"

# Mexer nestes arquivos exige duas aprovacoes. Sao as regras do projeto e as
# checagens que as fazem valer. Mudou esta lista? Voce esta mexendo nas regras,
# entao o proprio PR ja cai na regra.
ARQUIVOS_PROTEGIDOS = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
    "CONTRIBUTING.md",
    "docs/padroes.md",
    "docs/padroes-codigo.md",
    "docs/processo.md",
}
PREFIXOS_PROTEGIDOS = (".github/", "scripts/")

APROVACOES_EXIGIDAS = 2

CAMPOS_IA = (
    "IA usada",
    "No que ajudou",
    "O que é meu",
    "Conferi tudo que a IA escreveu",
)

erros = []


def api(caminho, tok):
    """GET na API do GitHub, seguindo a paginacao."""
    itens = []
    url = f"{API}{caminho}"
    url += ("&" if "?" in url else "?") + "per_page=100"
    while url:
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {tok}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "tcc-sdcac-governanca",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                dados = json.loads(resp.read().decode("utf-8"))
                link = resp.headers.get("Link", "")
        except urllib.error.HTTPError as erro:
            sys.exit(f"GitHub respondeu {erro.code} em {url}: {erro.reason}")
        except urllib.error.URLError as erro:
            sys.exit(f"Nao consegui falar com o GitHub: {erro.reason}")
        itens.extend(dados if isinstance(dados, list) else [dados])
        prox = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = prox.group(1) if prox else None
    return itens


def sem_comentarios(texto):
    """Remove comentarios HTML e normaliza o fim de linha.

    A normalizacao nao e detalhe de estilo. O GitHub devolve o corpo do Pull
    Request com CRLF; sem trocar por LF, o retorno de carro sobra no campo
    depois que o comentario e removido, o campo parece preenchido, e um
    template intacto passa como se tivesse sido respondido.

    Foi exatamente o que aconteceu no PR #5: os quatro campos em branco e o
    check verde.
    """
    texto = (texto or "").replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)


def checar_declaracao_ia(corpo):
    """O corpo do PR precisa ter a secao Uso de IA preenchida de verdade."""
    limpo = sem_comentarios(corpo)

    if not re.search(r"^#+\s*Uso de IA\s*$", limpo, re.IGNORECASE | re.MULTILINE):
        erros.append(
            "o corpo do PR nao tem a secao 'Uso de IA'. Copie o bloco de "
            ".github/pull_request_template.md e preencha. Ver AGENTS.md secao 3"
        )
        return

    for campo in CAMPOS_IA:
        # Aceita com ou sem negrito, e com o texto na mesma linha do rotulo.
        padrao = re.compile(
            r"^[ \t]*[-*][ \t]*\**[ \t]*" + re.escape(campo) + r"[ \t]*:?\**[ \t]*:?(.*)$",
            re.IGNORECASE | re.MULTILINE,
        )
        achado = padrao.search(limpo)
        if not achado:
            erros.append(f"falta o campo '{campo}' na secao Uso de IA do PR")
        # Cobre espaco, tabulacao e os enfeites de Markdown. O retorno de carro
        # ja saiu em sem_comentarios; fica aqui como segunda barreira.
        elif not achado.group(1).strip(" \t\r*_`-"):
            erros.append(
                f"o campo '{campo}' esta em branco. Uma resposta honesta e curta "
                f"basta — inclusive 'nenhuma', se for o caso"
            )


def checar_dupla_aprovacao(arquivos, reviews, autor):
    """PR que toca as regras ou as checagens precisa de duas aprovacoes."""
    tocados = sorted(
        a
        for a in arquivos
        if a in ARQUIVOS_PROTEGIDOS or a.startswith(PREFIXOS_PROTEGIDOS)
    )
    if not tocados:
        print("Nenhum arquivo de governanca tocado: 1 aprovacao basta.")
        return

    print("Arquivos de governanca neste PR:")
    for a in tocados:
        print(f"  - {a}")

    # Cada pessoa conta uma vez, pelo seu review mais recente: quem aprovou e
    # depois pediu mudancas nao esta mais aprovando.
    ultimo = {}
    for r in reviews:
        estado = r.get("state")
        if estado == "COMMENTED":
            continue  # comentario nao é posicao
        login = (r.get("user") or {}).get("login")
        if login and login != autor:
            ultimo[login] = estado

    aprovadores = sorted(k for k, v in ultimo.items() if v == "APPROVED")
    print(f"Aprovacoes validas: {len(aprovadores)} de {APROVACOES_EXIGIDAS}")
    for a in aprovadores:
        print(f"  + {a}")

    if len(aprovadores) < APROVACOES_EXIGIDAS:
        faltam = APROVACOES_EXIGIDAS - len(aprovadores)
        erros.append(
            f"este PR mexe nas regras do projeto ou nas checagens automaticas, "
            f"entao precisa de {APROVACOES_EXIGIDAS} aprovacoes — faltam "
            f"{faltam}. Motivo em AGENTS.md secao 4"
        )


def main():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    repo = os.environ.get("REPO")
    numero = os.environ.get("PR_NUMERO")
    if not (tok and repo and numero):
        sys.exit("Faltam GITHUB_TOKEN, REPO ou PR_NUMERO no ambiente.")

    pr = api(f"/repos/{repo}/pulls/{numero}", tok)[0]
    autor = (pr.get("user") or {}).get("login", "")
    arquivos = [a["filename"] for a in api(f"/repos/{repo}/pulls/{numero}/files", tok)]
    reviews = api(f"/repos/{repo}/pulls/{numero}/reviews", tok)

    print(f"PR #{numero} de @{autor} — {len(arquivos)} arquivo(s)\n")

    checar_declaracao_ia(pr.get("body") or "")
    checar_dupla_aprovacao(arquivos, reviews, autor)

    print()
    if erros:
        for e in erros:
            print(f"  ERRO   {e}")
        print(f"\nGovernanca falhou: {len(erros)} erro(s).")
        print("Regras em AGENTS.md e docs/uso-de-ia.md")
        return 1
    print("Governanca OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
