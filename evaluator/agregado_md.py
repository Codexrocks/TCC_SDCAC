"""O relatorio do agregado, em Markdown e em numero brasileiro.

Separado de `relatorio.py` por um motivo de formato, nao de organizacao: as
tabelas daqui vao **direto para a Secao 4 do artigo**, que escreve numero com
virgula decimal e ponto de milhar. O relatorio de uma semente serve para
conferir no terminal e usa o ponto decimal do JSON de origem.

Redigitar numero e como erro de resultado entra num artigo — a Secao 4 do
proprio artigo diz isso. Entao a tabela sai daqui pronta para colar.
"""

from __future__ import annotations

MINIMO_IMPRIMIVEL = 1e-4


def num(valor: float, casas: int = 2) -> str:
    """Numero em formato brasileiro: virgula decimal, ponto de milhar."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def pct(valor: float, casas: int = 2) -> str:
    """Percentual em formato brasileiro, sem o sinal de porcentagem."""
    return num(valor * 100, casas)


def media_e_desvio(resumo: dict, casas: int = 2) -> str:
    """`media ± desvio` em pontos percentuais."""
    return f"{pct(resumo['media'], casas)} ± {pct(resumo['desvio'], casas)}"


def nivel(chave: str) -> str:
    """A chave do nivel de revocacao, com virgula decimal."""
    return chave.replace(".", ",")


def valor_p(teste: dict, sementes: int) -> str:
    """O p-valor, ou a razao de nao haver um.

    O `n` so vem anotado quando empates derrubaram pares, porque e ai que ele
    muda a leitura: um p de 0,5 com dois pares nao e o mesmo que com dez.
    """
    if not teste["n_efetivo"]:
        return "idênticas"
    p = teste["p"]
    texto = "p < 0,0001" if p < MINIMO_IMPRIMIVEL else f"p = {num(p, 4)}"
    if teste["n_efetivo"] < sementes:
        texto += f" (n={teste['n_efetivo']})"
    return texto


def _direcao(bloco: dict, par: str) -> str:
    """Para que lado a diferenca aponta — o fato, nao o juizo.

    Se "menor" e bom ou ruim depende da metrica, e quem diz isso e o texto
    acima de cada tabela: em FPR menor e melhor, na familia benigna tambem, e
    nas familias maliciosas e o contrario. A palavra aqui e so a direcao.
    """
    a, b = par.split(" vs ")
    media_a = bloco["por_configuracao"][a]["media"]
    media_b = bloco["por_configuracao"][b]["media"]
    if media_a == media_b:
        return "igual"
    return "menor" if media_a < media_b else "maior"


def _tabela(cabecalho: list[str], linhas: list[list[str]]) -> list[str]:
    return [
        "| " + " | ".join(cabecalho) + " |",
        "|" + "---|" * len(cabecalho),
        *["| " + " | ".join(linha) + " |" for linha in linhas],
    ]


def escreve_markdown(agregado: dict) -> str:
    """Monta o relatorio agregado de varias sementes."""
    configs = agregado["configuracoes"]
    n = agregado["sementes"]
    pares = list(next(iter(agregado["fpr_a_revocacao_fixa"].values()))["wilcoxon"])
    escala = agregado["escala"]

    linhas = [
        f"# Agregado de {agregado['sementes']} sementes",
        "",
        "Gerado por `python -m evaluator.agregado_cli`. **Todo numero aqui saiu de "
        "execucao registrada** — nenhum foi estimado, e nenhum foi redigitado.",
        "",
        f"Sementes: **{', '.join(agregado['nomes'])}** · "
        f"limiar de operacao **{agregado['limiar_de_operacao']:g}** · "
        f"configuracoes **{', '.join(configs)}**.",
        "",
        f"Escala por semente: **{num(escala['eventos_pontuados']['media'], 0)} "
        f"± {num(escala['eventos_pontuados']['desvio'], 0)}** eventos pontuados, "
        f"dos quais **{num(escala['eventos_maliciosos']['media'], 0)} "
        f"± {num(escala['eventos_maliciosos']['desvio'], 0)}** maliciosos.",
        "",
        "Toda celula e **media ± desvio-padrao amostral** sobre as sementes, em "
        "pontos percentuais.",
        "",
        "## Ruido: FPR com a revocacao fixada",
        "",
        "A primeira grandeza da **D-03**. FPR de 100,00 ± 0,00 se le como "
        "**so alcanca aquela revocacao alertando o registro inteiro** — e e "
        "resultado, nao celula vazia.",
        "",
        *_tabela(
            ["Revocacao", *[f"**{c}**" for c in configs]],
            [
                [
                    f"**{nivel(chave)}**",
                    *[media_e_desvio(bloco["por_configuracao"][c]) for c in configs],
                ]
                for chave, bloco in agregado["fpr_a_revocacao_fixa"].items()
            ],
        ),
        "",
        "### Wilcoxon pareado, bilateral, p-valor exato",
        "",
        "Hipotese nula: as duas configuracoes tem a mesma FPR na mesma semente. "
        "A palavra depois do p-valor diz o lado da **primeira** configuracao do "
        "par, e em FPR **menor e melhor**. Par com diferenca zero e descartado; "
        "quando sobra menos de uma semente por par, o n efetivo vem anotado.",
        "",
        *_tabela(
            ["Revocacao", *[f"**{p}**" for p in pares]],
            [
                [
                    f"**{nivel(chave)}**",
                    *[
                        f"{valor_p(bloco['wilcoxon'][p], n)} · {_direcao(bloco, p)}"
                        if bloco["wilcoxon"][p]["n_efetivo"]
                        else valor_p(bloco["wilcoxon"][p], n)
                        for p in pares
                    ],
                ]
                for chave, bloco in agregado["fpr_a_revocacao_fixa"].items()
            ],
        ),
        "",
        "### Revocacao obtida em cada nivel",
        "",
        "A conferencia de que o nivel foi alcancado. O limiar e discreto, e por "
        "isso o ponto escolhido costuma passar do nivel pedido.",
        "",
        *_tabela(
            ["Nivel", *[f"**{c}**" for c in configs]],
            [
                [
                    f"**{nivel(chave)}**",
                    *[media_e_desvio(bloco["por_configuracao"][c], 1) for c in configs],
                ]
                for chave, bloco in agregado["revocacao_obtida"].items()
            ],
        ),
    ]

    if agregado["por_episodio"]:
        invertida = agregado["familia_invertida"]
        linhas += [
            "",
            "## Cobertura: deteccao por episodio no limiar de operacao",
            "",
            f"A familia **{invertida}** e benigna por construcao: ali a coluna "
            "nao e cobertura, e **alarme sobre atividade legitima**. "
            "Quanto menor, melhor — ao contrario de todas as outras linhas.",
            "",
            *_tabela(
                ["Familia", "Episodios", *[f"**{c}**" for c in configs]],
                [
                    [
                        f"**{familia}**"
                        + (" ⚠️ alarme" if bloco["alerta_e_falso_positivo"] else ""),
                        num(bloco["episodios_na_janela"]["media"], 1),
                        *[
                            media_e_desvio(bloco["por_configuracao"][c], 1)
                            for c in configs
                        ],
                    ]
                    for familia, bloco in agregado["por_episodio"].items()
                ],
            ),
            "",
            "### Wilcoxon pareado por familia",
            "",
            *_tabela(
                ["Familia", *[f"**{p}**" for p in pares]],
                [
                    [
                        f"**{familia}**",
                        *[
                            f"{valor_p(bloco['wilcoxon'][p], n)} · {_direcao(bloco, p)}"
                            if bloco["wilcoxon"][p]["n_efetivo"]
                            else valor_p(bloco["wilcoxon"][p], n)
                            for p in pares
                        ],
                    ]
                    for familia, bloco in agregado["por_episodio"].items()
                ],
            ),
        ]

    linhas += [
        "",
        "## Por evento, no limiar de operacao",
        "",
        *_tabela(
            ["Metrica", *[f"**{c}**" for c in configs]],
            [
                [
                    f"**{campo}**",
                    *[media_e_desvio(bloco["por_configuracao"][c]) for c in configs],
                ]
                for campo, bloco in agregado["por_evento"].items()
            ],
        ),
        "",
    ]
    return "\n".join(linhas)
