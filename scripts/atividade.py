#!/usr/bin/env python3
"""Coleta a atividade da equipe no repositorio e gera uma tabela em Markdown.

Uso:
    python3 scripts/atividade.py --dias 7
    python3 scripts/atividade.py --dias 7 --saida atividade.md

Precisa de um token do GitHub em GITHUB_TOKEN ou GH_TOKEN. No GitHub Actions,
o token padrao do workflow ja serve.

Este script so conta. Ele nao interpreta, nao elogia e nao cobra ninguem — a
leitura do que os numeros significam vem depois, escrita pelo assistente ou por
uma pessoa. Separar as duas coisas e proposital: numero de relatorio de banca
precisa ser reproduzivel, e texto gerado por IA nao e.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_PADRAO = "Codexrocks/TCC_SDCAC"
API = "https://api.github.com"
ANO_CRONOGRAMA = 2026


# ---------------------------------------------------------------------------
# Acesso a API
# ---------------------------------------------------------------------------


def token():
    for chave in ("GITHUB_TOKEN", "GH_TOKEN"):
        valor = os.environ.get(chave)
        if valor:
            return valor
    sys.exit("Falta o token: defina GITHUB_TOKEN ou GH_TOKEN no ambiente.")


def api(caminho, tok):
    """Faz um GET na API e devolve o JSON, seguindo a paginacao ate o fim."""
    itens = []
    url = f"{API}{caminho}"
    if "?" not in url:
        url += "?per_page=100"
    elif "per_page" not in url:
        url += "&per_page=100"

    while url:
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {tok}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "tcc-sdcac-atividade",
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


def quando(texto):
    """Converte a data ISO que o GitHub devolve em datetime com fuso."""
    if not texto:
        return None
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Coleta
# ---------------------------------------------------------------------------


def coletar(repo, desde, tok):
    """Junta PRs, revisoes e commits do periodo, agrupados por pessoa."""
    pessoas = defaultdict(
        lambda: {"abertos": 0, "mergeados": 0, "revisoes": 0, "commits": 0}
    )
    mergeados, abertos, parados = [], [], []

    for pr in api(f"/repos/{repo}/pulls?state=all&sort=updated&direction=desc", tok):
        criado = quando(pr["created_at"])
        fechado = quando(pr.get("merged_at"))
        autor = (pr.get("user") or {}).get("login", "desconhecido")

        # A lista vem ordenada por atualizacao: quando passamos do periodo e
        # o PR ja esta fechado, o resto so tem coisa mais velha ainda.
        if quando(pr["updated_at"]) < desde and pr["state"] != "open":
            break

        if criado >= desde:
            pessoas[autor]["abertos"] += 1
            if pr["state"] == "open":
                abertos.append((pr["number"], pr["title"], autor))

        if fechado and fechado >= desde:
            pessoas[autor]["mergeados"] += 1
            mergeados.append((pr["number"], pr["title"], autor))

        if pr["state"] == "open":
            idade = (datetime.now(timezone.utc) - quando(pr["updated_at"])).days
            if idade >= 3:
                parados.append((pr["number"], pr["title"], autor, idade))

        for rev in api(f"/repos/{repo}/pulls/{pr['number']}/reviews", tok):
            enviado = quando(rev.get("submitted_at"))
            revisor = (rev.get("user") or {}).get("login", "desconhecido")
            # Comentario no proprio PR nao conta como revisao.
            if enviado and enviado >= desde and revisor != autor:
                pessoas[revisor]["revisoes"] += 1

    desde_iso = desde.isoformat()
    for commit in api(f"/repos/{repo}/commits?since={desde_iso}", tok):
        autor = (commit.get("author") or {}).get("login")
        if not autor:
            # Commit sem conta do GitHub associada — conta no total, mas nao
            # da para atribuir a ninguem.
            autor = "sem atribuicao"
        pessoas[autor]["commits"] += 1

    return pessoas, mergeados, abertos, parados


# ---------------------------------------------------------------------------
# Semana do cronograma
# ---------------------------------------------------------------------------


def semana_do_cronograma(hoje):
    """Descobre em que semana do cronograma estamos, lendo docs/cronograma.md.

    A fonte da verdade e o cronograma, nunca uma copia dentro deste script. Se
    a tabela mudar de formato, devolve None e o relatorio simplesmente sai sem
    essa linha — melhor faltar do que mentir.
    """
    caminho = os.path.join(RAIZ, "docs", "cronograma.md")
    if not os.path.exists(caminho):
        return None

    with open(caminho, encoding="utf-8") as fh:
        texto = fh.read()

    for linha in texto.splitlines():
        campos = [c.strip() for c in linha.split("|")]
        if len(campos) < 6 or not re.fullmatch(r"S\d+", campos[1]):
            continue
        faixa = campos[2].replace("–", "-").replace("—", "-")
        partes = faixa.split("-")
        if len(partes) != 2:
            continue
        try:
            fim = partes[1].strip()
            dia_f, mes_f = (int(x) for x in fim.split("/"))
            inicio = partes[0].strip()
            if "/" in inicio:
                dia_i, mes_i = (int(x) for x in inicio.split("/"))
            else:
                dia_i, mes_i = int(inicio), mes_f
        except ValueError:
            continue

        d_ini = datetime(ANO_CRONOGRAMA, mes_i, dia_i, tzinfo=timezone.utc)
        d_fim = datetime(ANO_CRONOGRAMA, mes_f, dia_f, 23, 59, tzinfo=timezone.utc)
        if d_ini <= hoje <= d_fim:
            return {"semana": campos[1], "foco": campos[3], "quem": campos[5]}

    return None


# ---------------------------------------------------------------------------
# Saida
# ---------------------------------------------------------------------------


def render(repo, desde, ate, pessoas, mergeados, abertos, parados, semana):
    linhas = []
    add = linhas.append

    add(f"# Atividade de {desde:%d/%m/%Y} a {ate:%d/%m/%Y}")
    add("")
    add(f"Repositório: `{repo}`")
    if semana:
        add("")
        add(
            f"Semana **{semana['semana']}** do cronograma — {semana['foco']} "
            f"(responsável: {semana['quem']})"
        )
    add("")

    add("## Por pessoa")
    add("")
    add("| Pessoa | PRs abertos | PRs mergeados | Revisões feitas | Commits |")
    add("|---|---|---|---|---|")
    if pessoas:
        ordem = sorted(pessoas.items(), key=lambda kv: -sum(kv[1].values()))
        for nome, d in ordem:
            add(
                f"| `{nome}` | {d['abertos']} | {d['mergeados']} "
                f"| {d['revisoes']} | {d['commits']} |"
            )
    else:
        add("| — | 0 | 0 | 0 | 0 |")
    add("")

    add("## Pull Requests mergeados no período")
    add("")
    if mergeados:
        for num, titulo, autor in mergeados:
            add(f"- #{num} — {titulo} · `{autor}`")
    else:
        add("Nenhum.")
    add("")

    add("## Pull Requests abertos no período e ainda em aberto")
    add("")
    if abertos:
        for num, titulo, autor in abertos:
            add(f"- #{num} — {titulo} · `{autor}`")
    else:
        add("Nenhum.")
    add("")

    add("## Pull Requests parados há 3 dias ou mais")
    add("")
    if parados:
        for num, titulo, autor, idade in parados:
            add(f"- #{num} — {titulo} · `{autor}` · parado há {idade} dia(s)")
    else:
        add("Nenhum.")
    add("")

    return "\n".join(linhas) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dias", type=int, default=7, help="janela em dias (padrao 7)")
    p.add_argument("--repo", default=REPO_PADRAO, help="owner/nome do repositorio")
    p.add_argument("--saida", help="arquivo de saida (padrao: imprime na tela)")
    args = p.parse_args()

    ate = datetime.now(timezone.utc)
    desde = ate - timedelta(days=args.dias)
    tok = token()

    pessoas, mergeados, abertos, parados = coletar(args.repo, desde, tok)
    texto = render(
        args.repo,
        desde,
        ate,
        pessoas,
        mergeados,
        abertos,
        parados,
        semana_do_cronograma(ate),
    )

    if args.saida:
        with open(args.saida, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
        print(f"Gravado em {args.saida}")
    else:
        print(texto)

    return 0


if __name__ == "__main__":
    sys.exit(main())
