"""Agrega varias sementes numa tabela so, com teste pareado.

**Por que isto existe.** Uma semente e uma amostra de uma populacao sorteada.
A secao 3.7 do artigo pede de dez a vinte, e nao por capricho: com uma, a
diferenca entre duas configuracoes e descritiva, e a banca pergunta se ela nao
e sorte do sorteio. Com dez, a pergunta tem resposta — e a resposta e um
p-valor, nao uma impressao.

**O teste e o de Wilcoxon de postos sinalizados, pareado e bilateral.** Pareado
porque a mesma semente gera a mesma populacao para as quatro configuracoes: a
comparacao e dentro da semente, nao entre sementes, e isso tira a variacao do
sorteio de dentro do erro. De postos porque a FPR nao e normal — ela se acumula
perto de zero e tem teto em 1 —, e um teste t suporia o que os dados nao tem.

**O p-valor e exato, nao aproximado.** Com dez pares a distribuicao nula e
contavel, e a aproximacao normal do Wilcoxon e justamente pior em amostra
pequena. O custo e uma contagem de subconjuntos por programacao dinamica, que
roda em milissegundos e nao depende de biblioteca de fora.

**A familia N se le ao contrario das outras.** `P`, `B` e `L` sao episodios
maliciosos: detectar mais e melhor. A familia `N` e **benigna por construcao** —
atividade legitima que parece estranha —, e alertar sobre ela e falso positivo.
O agregado marca a familia invertida, porque numero que se le ao contrario sem
aviso e numero que vai ser lido errado.
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Callable, Iterable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

CONFIGURACOES = ("C0", "C1", "C2", "C3")
FAMILIAS = ("P", "B", "L", "N")
FAMILIA_INVERTIDA = "N"
PARES = (("C2", "C0"), ("C2", "C1"), ("C3", "C2"), ("C1", "C0"))


class AgregadoError(ValueError):
    """Recusa de agregacao: as sementes nao sao comparaveis entre si."""


@dataclass(frozen=True)
class Wilcoxon:
    """O resultado do teste, com o n que sobrou depois de descartar empates."""

    estatistica: float
    p: float
    n_efetivo: int

    @property
    def conclusivo(self) -> bool:
        """Verdadeiro quando sobrou par com diferenca para testar."""
        return self.n_efetivo > 0


@dataclass(frozen=True)
class Resumo:
    """Media e desvio-padrao amostral de uma serie de sementes."""

    media: float
    desvio: float
    n: int


def resume(valores: Sequence[float]) -> Resumo:
    """Media e desvio-padrao amostral — o de n-1, nao o populacional."""
    if not valores:
        raise AgregadoError("serie vazia nao tem media")
    desvio = statistics.stdev(valores) if len(valores) > 1 else 0.0
    return Resumo(statistics.fmean(valores), desvio, len(valores))


def postos(valores: Sequence[float]) -> list[float]:
    """Postos de 1 a n, com empate recebendo a media das posicoes empatadas."""
    ordem = sorted(range(len(valores)), key=lambda i: valores[i])
    saida = [0.0] * len(valores)
    i = 0
    while i < len(ordem):
        j = i
        while j + 1 < len(ordem) and valores[ordem[j + 1]] == valores[ordem[i]]:
            j += 1
        medio = (i + j) / 2 + 1
        for k in range(i, j + 1):
            saida[ordem[k]] = medio
        i = j + 1
    return saida


def _subconjuntos_por_soma(dobrados: Sequence[int]) -> list[int]:
    """Quantos subconjuntos somam cada valor — a distribuicao nula contada.

    Sob a hipotese nula cada posto entra com sinal mais ou menos com a mesma
    probabilidade, o que equivale a sortear um subconjunto dos postos. Contar
    por programacao dinamica da o resultado exato sem enumerar os 2**n casos,
    e por isso o teste continua exato com vinte sementes, nao so com dez.
    """
    contagem = [0] * (sum(dobrados) + 1)
    contagem[0] = 1
    for peso in dobrados:
        for soma in range(len(contagem) - 1, peso - 1, -1):
            contagem[soma] += contagem[soma - peso]
    return contagem


def wilcoxon(a: Sequence[float], b: Sequence[float]) -> Wilcoxon:
    """Postos sinalizados pareado bilateral, com p-valor exato.

    Par com diferenca zero e descartado, como manda o procedimento classico —
    e o `n_efetivo` diz quantos sobraram, para nao se ler como dez um teste que
    correu com dois.
    """
    if len(a) != len(b):
        raise AgregadoError(f"series de tamanhos diferentes: {len(a)} e {len(b)}")
    diferencas = [x - y for x, y in zip(a, b, strict=True) if x != y]
    if not diferencas:
        return Wilcoxon(float("nan"), 1.0, 0)
    ranks = postos([abs(d) for d in diferencas])
    mais = sum(r for d, r in zip(diferencas, ranks, strict=True) if d > 0)
    menos = sum(r for d, r in zip(diferencas, ranks, strict=True) if d < 0)
    w = min(mais, menos)

    dobrados = [round(r * 2) for r in ranks]
    total = sum(dobrados)
    contagem = _subconjuntos_por_soma(dobrados)
    limite = round(w * 2)
    extremos = sum(
        quantos
        for soma, quantos in enumerate(contagem)
        if min(soma, total - soma) <= limite
    )
    return Wilcoxon(w, extremos / 2 ** len(diferencas), len(diferencas))


# ------------------------------------------------------------------- leitura
def carrega(diretorios: Iterable[Path]) -> list[tuple[str, dict]]:
    """Le um `metricas.json` por diretorio, recusando o que nao e comparavel.

    A recusa e o ponto: medir a FPR de uma semente avaliada no limiar 20 junto
    com outra avaliada no limiar 30 daria uma media sem significado, e nada no
    numero final acusaria a mistura.

    **A identidade de uma semente e o nome do diretorio, nao o `run_id`.** O
    `run_id` do `metricas.json` e o numero da execucao *dentro* de um conjunto
    gerado, e um conjunto por semente comeca em 1 — dez sementes independentes
    tem dez `run_id` iguais a 1. Quem guarda a semente do gerador e o
    `gerador.log` de cada diretorio, na linha `run N (seed M)`.
    """
    lidos: list[tuple[str, Path, dict]] = []
    vistos: set[str] = set()
    for diretorio in sorted(diretorios, key=lambda p: (len(p.name), p.name)):
        caminho = diretorio / "metricas.json"
        if not caminho.exists():
            raise AgregadoError(f"{caminho} nao existe")
        nome = diretorio.name
        if nome in vistos:
            raise AgregadoError(
                f"{nome} entrou duas vezes: a mesma semente contada em dobro "
                "estreita o desvio-padrao, e nada no numero final acusaria"
            )
        vistos.add(nome)
        lidos.append((nome, caminho, json.loads(caminho.read_text(encoding="utf-8"))))
    if len(lidos) < 2:
        raise AgregadoError("agregar exige pelo menos duas sementes")

    _, primeiro_caminho, primeiro = lidos[0]
    limiar = primeiro["limiar_de_operacao"]
    niveis = list(primeiro["niveis_de_revocacao"])
    configs = sorted(primeiro["configuracoes"])
    for _, caminho, atual in lidos[1:]:
        if atual["limiar_de_operacao"] != limiar:
            raise AgregadoError(
                f"{caminho} usou limiar {atual['limiar_de_operacao']} e "
                f"{primeiro_caminho} usou {limiar}: nao se media FPR de "
                "limiares diferentes"
            )
        if list(atual["niveis_de_revocacao"]) != niveis:
            raise AgregadoError(f"{caminho} tem outros niveis de revocacao")
        if sorted(atual["configuracoes"]) != configs:
            raise AgregadoError(
                f"{caminho} avaliou {sorted(atual['configuracoes'])} e "
                f"{primeiro_caminho} avaliou {configs}"
            )
    return [(nome, dado) for nome, _, dado in lidos]


def _chave_do_nivel(nivel: float, chaves: Iterable[str]) -> str:
    """A chave textual de um nivel de revocacao, como o `metricas.json` grava."""
    for chave in chaves:
        if abs(float(chave) - nivel) < 1e-9:
            return chave
    raise AgregadoError(f"nivel de revocacao {nivel} ausente")


def _pareado(dados: dict[str, list[float]]) -> dict[str, dict]:
    """O Wilcoxon de cada par de configuracoes que exista nos dados."""
    return {
        f"{a} vs {b}": asdict(wilcoxon(dados[a], dados[b]))
        for a, b in PARES
        if a in dados and b in dados
    }


def agrega(sementes: Sequence[dict], nomes: Sequence[str] | None = None) -> dict:
    """Media, desvio e Wilcoxon de cada metrica, sobre as sementes dadas.

    `nomes` identifica cada semente no relatorio. Sem ele as sementes saem
    numeradas pela posicao, que serve para teste e nao para procedencia.
    """
    if len(sementes) < 2:
        raise AgregadoError("agregar exige pelo menos duas sementes")
    if nomes is not None and len(nomes) != len(sementes):
        raise AgregadoError(f"{len(nomes)} nomes para {len(sementes)} sementes")
    etiquetas = list(nomes) if nomes else [str(i + 1) for i in range(len(sementes))]
    configs = tuple(c for c in CONFIGURACOES if c in sementes[0]["configuracoes"])
    niveis = list(sementes[0]["niveis_de_revocacao"])
    chaves = list(sementes[0]["configuracoes"][configs[0]]["fpr_a_revocacao_fixa"])

    def serie(extrai: Callable[[dict], float]) -> dict[str, list[float]]:
        return {c: [extrai(s["configuracoes"][c]) for s in sementes] for c in configs}

    def bloco(dados: dict[str, list[float]]) -> dict:
        return {
            "por_configuracao": {c: asdict(resume(v)) for c, v in dados.items()},
            "wilcoxon": _pareado(dados),
        }

    saida: dict = {
        "sementes": len(sementes),
        "nomes": etiquetas,
        "limiar_de_operacao": sementes[0]["limiar_de_operacao"],
        "niveis_de_revocacao": niveis,
        "configuracoes": list(configs),
        "familia_invertida": FAMILIA_INVERTIDA,
        "escala": {
            nome: asdict(
                resume([s["configuracoes"][configs[0]][nome] for s in sementes])
            )
            for nome in ("eventos_pontuados", "eventos_maliciosos")
        },
        "fpr_a_revocacao_fixa": {},
        "revocacao_obtida": {},
        "por_evento": {},
        "por_episodio": {},
    }

    for nivel in niveis:
        chave = _chave_do_nivel(nivel, chaves)
        saida["fpr_a_revocacao_fixa"][chave] = bloco(
            serie(lambda c, k=chave: c["fpr_a_revocacao_fixa"][k]["fpr"])
        )
        saida["revocacao_obtida"][chave] = bloco(
            serie(lambda c, k=chave: c["fpr_a_revocacao_fixa"][k]["revocacao_obtida"])
        )

    for campo in ("revocacao", "fpr", "precisao"):
        saida["por_evento"][campo] = bloco(serie(lambda c, f=campo: c["por_evento"][f]))

    por_episodio = sementes[0]["configuracoes"][configs[0]]["por_episodio"]
    for familia in FAMILIAS:
        if familia not in por_episodio:
            continue
        saida["por_episodio"][familia] = bloco(
            serie(lambda c, f=familia: c["por_episodio"][f]["taxa"])
        ) | {
            "alerta_e_falso_positivo": familia == FAMILIA_INVERTIDA,
            "episodios_na_janela": asdict(
                resume(
                    [
                        s["configuracoes"][configs[0]]["por_episodio"][familia][
                            "episodios_na_janela"
                        ]
                        for s in sementes
                    ]
                )
            ),
        }
    return saida


def agrega_diretorios(diretorios: Iterable[Path]) -> dict:
    """Le e agrega — o caminho que a linha de comando usa."""
    lidos = carrega(diretorios)
    return agrega([dado for _, dado in lidos], [nome for nome, _ in lidos])
