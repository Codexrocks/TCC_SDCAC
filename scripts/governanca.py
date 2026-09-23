#!/usr/bin/env python3
"""Confere as regras de governanca de um Pull Request.

Duas checagens, ambas descritas em AGENTS.md:

1. **Declaracao de IA** (secao 3) — o corpo do PR precisa dizer qual assistente
   foi usado, no que ajudou, o que e da pessoa, e se ela conferiu o resultado.
2. **Arquivo protegido** (secao 4) — PR que mexe nas regras do projeto ou nas
   checagens automaticas espera 24 h e se explica na secao "Arquivo
   protegido" do corpo do PR.

A segunda existe por um motivo especifico: sem ela, bastaria um PR editando o
validar.py para desligar todas as travas — e a IA que escreveu o PR seria a
mesma que sugeriu a mudanca.

Ate 23/09/2026 essa trava eram duas aprovacoes. O trabalho passou a ser de uma
pessoa so, e o GitHub nao deixa ninguem aprovar o proprio PR: a regra virou
impossivel de cumprir, nao rigorosa. A espera e a justificativa sao o que uma
pessoa sozinha cumpre sem deixar de ser trava — quem confere e este script.

Uso, dentro do GitHub Actions:
    PR_NUMERO=12 REPO=dono/nome GITHUB_TOKEN=... python3 scripts/governanca.py
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"

# Mexer nestes arquivos pede espera e justificativa. Sao as regras do projeto e
# as checagens que as fazem valer. Mudou esta lista? Voce esta mexendo nas
# regras, entao o proprio PR ja cai na regra.
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

# Quanto tempo um PR que toca arquivo protegido fica aberto antes de poder
# entrar. Um dia: a mudanca e lida em dois momentos diferentes, e nao duas
# vezes na mesma pressa. Mudar este numero e mudar a regra — e este arquivo e
# protegido, entao o proprio PR que mexer aqui espera as 24 h.
HORAS_DE_ESPERA = 24

SECAO_IA = "Uso de IA"
CAMPOS_IA = (
    "IA usada",
    "No que ajudou",
    "O que é meu",
    "Conferi tudo que a IA escreveu",
)

SECAO_PROTEGIDO = "Arquivo protegido"
CAMPOS_PROTEGIDO = (
    "O que muda",
    "Por que agora",
    "O que segura no lugar",
)

# Dois ou mais tracos seguidos sao enfeite de Markdown, nao resposta. Um traco
# sozinho e resposta: quer dizer "nao se aplica". Cobre hifen, traco de dialogo
# e travessao, porque quem escreve nao distingue os tres no teclado.
RE_SO_TRACOS = re.compile(r"^[-–—]{2,}$")

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


def sem_blocos_de_codigo(texto):
    """Remove blocos ``` ou ~~~ do texto.

    Existe porque o PR #11 se auto-reprovou. Ele corrigia um defeito e, para
    explica-lo, citava o campo do PR #10 dentro de um bloco de codigo:

        - **No que ajudou:** -

    O `search` pega a PRIMEIRA ocorrencia do campo em todo o corpo, entao leu a
    citacao como se fosse a resposta. Qualquer PR que documente o proprio
    formulario caia no mesmo buraco — e sao justamente os PRs sobre o guia e
    sobre as regras.

    Exemplo citado nao e resposta dada.
    """
    return re.sub(
        r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$",
        "",
        texto or "",
        flags=re.DOTALL | re.MULTILINE,
    )


def secao(texto, titulo):
    """Devolve so o trecho da secao com este titulo, ate o proximo cabecalho.

    O formulario e a secao. Procurar os campos no corpo inteiro faz o check
    aceitar — ou recusar — texto que esta em outra parte do PR.
    """
    achado = re.search(
        r"^#+[ \t]*" + re.escape(titulo) + r"[ \t]*$(.*?)(?=^#+[ \t]|\Z)",
        texto,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    return achado.group(1) if achado else ""


def checar_campos(trecho, campos, onde):
    """Confere que cada campo do formulario tem resposta de verdade."""
    for campo in campos:
        # Aceita com ou sem negrito, e com o texto na mesma linha do rotulo.
        padrao = re.compile(
            r"^[ \t]*[-*][ \t]*\**[ \t]*" + re.escape(campo) + r"[ \t]*:?\**[ \t]*:?(.*)$",
            re.IGNORECASE | re.MULTILINE,
        )
        achado = padrao.search(trecho)
        if not achado:
            erros.append(f"falta o campo '{campo}' na secao {onde} do PR")
        # Cobre espaco, tabulacao e os enfeites de Markdown. O retorno de carro
        # ja saiu em sem_comentarios; fica aqui como segunda barreira.
        #
        # O hifen NAO entra nesta lista, e isso e proposital: um traco sozinho e
        # resposta legitima para "nao se aplica", e foi o que o PR #10 escreveu.
        # Reprova-lo dizia a quem respondeu que ele nao tinha respondido.
        # Traco de enfeite continua barrado logo abaixo.
        elif not achado.group(1).strip(" \t\r*_`"):
            erros.append(
                f"o campo '{campo}' esta em branco. Uma resposta honesta e curta "
                f"basta — inclusive 'nenhuma', se for o caso"
            )
        elif RE_SO_TRACOS.match(achado.group(1).strip(" \t\r*_`")):
            # "---" e linha horizontal do Markdown, nao resposta. Um traco so e.
            erros.append(
                f"o campo '{campo}' tem so tracos de enfeite. Escreva a resposta "
                f"— um traco sozinho vale como 'nao se aplica'"
            )


def checar_declaracao_ia(corpo):
    """O corpo do PR precisa ter a secao Uso de IA preenchida de verdade."""
    limpo = sem_comentarios(corpo)

    if not re.search(
        rf"^#+\s*{re.escape(SECAO_IA)}\s*$", limpo, re.IGNORECASE | re.MULTILINE
    ):
        erros.append(
            "o corpo do PR nao tem a secao 'Uso de IA'. Copie o bloco de "
            ".github/pull_request_template.md e preencha. Ver AGENTS.md secao 3"
        )
        return

    # So a secao, e sem os blocos de codigo dela: o que vale e o que foi
    # respondido no formulario, nao o que foi citado como exemplo.
    checar_campos(sem_blocos_de_codigo(secao(limpo, SECAO_IA)), CAMPOS_IA, SECAO_IA)


def caminhos_tocados(itens):
    """Caminhos que o PR toca, incluindo a origem de cada renomeacao.

    Recebe a lista devolvida por /pulls/{numero}/files.

    Renomear tira o arquivo do caminho antigo tanto quanto apaga-lo: um PR que
    mova AGENTS.md para docs/regras.md mexe no AGENTS.md. So que a API poe o
    caminho novo em `filename` e guarda o antigo em `previous_filename`. Lendo so
    o primeiro, a checagem de arquivo protegido nao via o arquivo saindo do
    lugar, e o PR escapava da regra.
    """
    caminhos = []
    for item in itens:
        caminhos.append(item["filename"])
        if item.get("previous_filename"):
            caminhos.append(item["previous_filename"])
    # O mesmo caminho pode vir duas vezes: renomear A para B e criar outro A no
    # mesmo PR. Sem tirar a repeticao, o log listava o arquivo protegido em
    # dobro. A ordem continua a da API.
    return list(dict.fromkeys(caminhos))


def checar_arquivo_protegido(arquivos, corpo, criado_em, agora):
    """PR que toca as regras ou as checagens espera 24 h e se explica.

    Ate 23/09/2026 a trava eram duas aprovacoes. Com uma pessoa so, e o GitHub
    recusando que alguem aprove o proprio PR, a regra virou impossivel de
    cumprir. No lugar dela: o PR fica aberto HORAS_DE_ESPERA antes de entrar, e
    o corpo responde o que muda, por que agora e o que segura no lugar.
    """
    tocados = sorted(
        a
        for a in arquivos
        if a in ARQUIVOS_PROTEGIDOS or a.startswith(PREFIXOS_PROTEGIDOS)
    )
    if not tocados:
        print("Nenhum arquivo de governanca tocado: basta o check verde.")
        return

    print("Arquivos de governanca neste PR:")
    for a in tocados:
        print(f"  - {a}")

    horas = (agora - criado_em).total_seconds() / 3600
    print(f"Aberto ha {horas:.1f} h; a regra pede {HORAS_DE_ESPERA} h.")
    if horas < HORAS_DE_ESPERA:
        erros.append(
            f"este PR mexe nas regras do projeto ou nas checagens automaticas, "
            f"entao fica {HORAS_DE_ESPERA} h aberto antes de entrar — faltam "
            f"{HORAS_DE_ESPERA - horas:.1f} h. Passado o prazo, edite o corpo do "
            f"PR ou reexecute este check para ele contar de novo. Motivo em "
            f"AGENTS.md secao 4"
        )

    limpo = sem_comentarios(corpo)
    if not re.search(
        rf"^#+\s*{re.escape(SECAO_PROTEGIDO)}\s*$",
        limpo,
        re.IGNORECASE | re.MULTILINE,
    ):
        erros.append(
            f"o corpo do PR nao tem a secao '{SECAO_PROTEGIDO}', obrigatoria em "
            f"PR que toca arquivo de regra ou de checagem. Copie o bloco de "
            f".github/pull_request_template.md e responda. Ver AGENTS.md secao 4"
        )
        return

    checar_campos(
        sem_blocos_de_codigo(secao(limpo, SECAO_PROTEGIDO)),
        CAMPOS_PROTEGIDO,
        SECAO_PROTEGIDO,
    )


def main():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    repo = os.environ.get("REPO")
    numero = os.environ.get("PR_NUMERO")
    if not (tok and repo and numero):
        sys.exit("Faltam GITHUB_TOKEN, REPO ou PR_NUMERO no ambiente.")

    pr = api(f"/repos/{repo}/pulls/{numero}", tok)[0]
    autor = (pr.get("user") or {}).get("login", "")
    itens = api(f"/repos/{repo}/pulls/{numero}/files", tok)
    arquivos = caminhos_tocados(itens)
    corpo = pr.get("body") or ""
    criado = pr.get("created_at")
    if not criado:
        sys.exit(
            "A API nao devolveu created_at do PR; sem isso nao da para contar a espera."
        )
    criado_em = datetime.fromisoformat(criado.replace("Z", "+00:00"))

    print(f"PR #{numero} de @{autor} — {len(itens)} arquivo(s)\n")

    checar_declaracao_ia(corpo)
    checar_arquivo_protegido(arquivos, corpo, criado_em, datetime.now(timezone.utc))

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
