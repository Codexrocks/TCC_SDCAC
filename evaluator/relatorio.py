"""O relatorio em Markdown, a partir do `metricas.json`.

Existe para conferir numero sem abrir JSON, e para colar a tabela na Secao 4 do
artigo sem redigitar — redigitar numero e como erro de resultado entra.
"""


def _pct(valor: float | None, casas: int = 2) -> str:
    return "—" if valor is None else f"{valor * 100:.{casas}f}%"


def escreve_markdown(relatorio: dict) -> str:
    """Monta o relatorio legivel de uma semente avaliada."""
    configuracoes = relatorio["configuracoes"]
    linhas = [
        f"# Metricas da semente {relatorio['run_id']}",
        "",
        "Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao "
        "registrada** — nenhum foi estimado.",
        "",
        f"Limiar de operacao: **{relatorio['limiar_de_operacao']:g}**.",
        "",
        "## Por evento, no limiar de operacao",
        "",
        "| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for nome, dados in configuracoes.items():
        ev = dados["por_evento"]
        linhas.append(
            f"| **{nome}** | {dados['eventos_pontuados']:,} | "
            f"{dados['eventos_maliciosos']:,} | {ev['tp']:,} | {ev['fp']:,} | "
            f"{ev['fn']:,} | {_pct(ev['revocacao'])} | {_pct(ev['fpr'])} | "
            f"{_pct(ev['precisao'])} |".replace(",", ".")
        )

    niveis = [f"{n:.2f}" for n in relatorio["niveis_de_revocacao"]]
    linhas += [
        "",
        "## Ruido: FPR com a revocacao fixada (por evento)",
        "",
        "A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar "
        "ate alertar o log inteiro — por isso nao existe celula vazia aqui, e "
        '**FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do '
        "log alertada esta entre parenteses.",
        "",
        "| Config | " + " | ".join(f"rev. {n}" for n in niveis) + " |",
        "|---" * (len(niveis) + 1) + "|",
    ]
    for nome, dados in configuracoes.items():
        celulas = []
        for nivel in niveis:
            ponto = dados["fpr_a_revocacao_fixa"][nivel]
            celulas.append(f"{_pct(ponto['fpr'])} ({_pct(ponto['fracao_do_log'], 1)})")
        linhas.append(f"| **{nome}** | " + " | ".join(celulas) + " |")

    linhas += [
        "",
        "## Cobertura: por episodio, no limiar de operacao",
        "",
        "Um episodio conta como detectado quando **pelo menos um** evento dele "
        "passa do limiar. A unidade de analise e a **D-12**, que esta aberta — "
        "por isso as duas tabelas, e nao uma.",
        "",
        "A familia **N** e benigna por construcao: ali a coluna nao e "
        "revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.",
        "",
    ]
    familias = list(next(iter(configuracoes.values()))["por_episodio"].keys())
    linhas += [
        "| Config | " + " | ".join(familias) + " |",
        "|---" * (len(familias) + 1) + "|",
    ]
    for nome, dados in configuracoes.items():
        celulas = []
        for familia in familias:
            fam = dados["por_episodio"][familia]
            celulas.append(
                f"{fam['detectados']}/{fam['episodios_na_janela']} "
                f"({_pct(fam['taxa'], 1)})"
                if fam["episodios_na_janela"]
                else "—"
            )
        linhas.append(f"| **{nome}** | " + " | ".join(celulas) + " |")

    linhas += [
        "",
        "Legenda das familias: "
        + " · ".join(
            f"**{f}** {next(iter(configuracoes.values()))['por_episodio'][f]['descricao']}"
            for f in familias
        ),
        "",
    ]
    return "\n".join(linhas)
