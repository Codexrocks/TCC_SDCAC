"""O avaliador: as duas grandezas da pergunta de pesquisa, contra o gabarito.

**E o unico componente que le `ground_truth/`.** A separacao esta nas portas de
`detection.ports` e no privilegio do banco: o usuario da aplicacao nao conecta
no gabarito, e o adaptador de arquivo nem sabe que ele existe. Quem compara
nota com rotulo e este modulo, e nada em `detection/` o importa.

**As duas grandezas sao as da D-03**, operacionalizadas na secao 1.3 do
[plano](../docs/plano.md):

| Grandeza | Metrica |
|---|---|
| Ruido | Taxa de falsos positivos **com a revocacao fixada no mesmo nivel** nas quatro configuracoes |
| Cobertura | Revocacao nos cenarios longitudinais — a familia `L` do catalogo |

**Duas unidades de analise, as duas reportadas — porque a D-12 esta aberta.** O
proprio plano avisa que um cenario longitudinal "pode render revocacao de 0,15
medido por evento e 1,00 medido por episodio". Escolher uma aqui seria fechar a
D-12 por omissao, dentro de um arquivo de codigo. As duas saem no relatorio, com
o nome da unidade em cada numero.

**O que conta como positivo.** Evento com rotulo `malicious` em
`event_labels.csv.gz`. Evento sem rotulo nenhum e negativo: o gabarito so
rotula o que pertence a um episodio. A familia `N` e episodio **benigno por
construcao** — atividade legitima que parece estranha —, e por isso alerta sobre
um `N` e falso positivo, nao acerto. E a razao de a familia existir.

**Revocacao fixa, e como ler uma FPR de 100%.** A FPR so se compara entre
configuracoes no mesmo ponto de revocacao. Qualquer revocacao e sempre
alcancavel — basta baixar o limiar ate alertar o log inteiro —, e por isso nao
existe "nao alcanca": existe **alcanca alertando tudo**, que e o que uma FPR de
100% diz. E a leitura da linha da C0 na execucao piloto, e e um resultado, nao
uma lacuna: a base de regras fixas so chega a 40% de revocacao abrindo alerta
em cada evento do log.

O denominador da revocacao sao os **maliciosos pontuados**, nao os do gabarito
inteiro: evento malicioso fora da janela de avaliacao nao foi oferecido ao
motor, e cobrar dele seria descontar da revocacao o que a janela escondeu.
"""

import csv
import gzip
import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# Os niveis de revocacao em que a FPR e reportada. O nivel que vale para o
# artigo e **declarado pela equipe**, nao escolhido aqui: reportar varios e o
# que permite declarar um depois sem reexecutar, e o que impede escolher o
# nivel que favorece a conclusao — que seria o mesmo defeito da D-15.
#
# A faixa comeca em 0,10 porque a base de regras fixas nao chega longe: na
# execucao piloto a C0 so alcanca 0,50 de revocacao alertando o log inteiro, e
# uma tabela que comecasse em 0,50 reportaria `100%` na linha dela e esconderia
# onde a comparacao ainda tem sentido.
NIVEIS_DE_REVOCACAO = (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90)

FAMILIAS = {
    "P": "pontual",
    "B": "comportamental",
    "L": "longitudinal",
    "N": "normal (benigno por construcao)",
}


class EvaluatorError(Exception):
    """Erro de avaliacao, com o arquivo ou a execucao que faltou."""


@dataclass
class Gabarito:
    """O gabarito de uma semente: rotulo por evento e episodio por evento."""

    maliciosos: set[str] = field(default_factory=set)
    episodio_de: dict[str, int] = field(default_factory=dict)
    familia_de: dict[int, str] = field(default_factory=dict)
    maliciosos_por_episodio: dict[int, bool] = field(default_factory=dict)

    def episodios_da_familia(self, familia: str, *, maliciosos: bool) -> set[int]:
        return {
            ep
            for ep, fam in self.familia_de.items()
            if fam == familia
            and self.maliciosos_por_episodio.get(ep, False) is maliciosos
        }


def _verdadeiro(texto: str | None) -> bool:
    """Um booleano a partir do que o `pandas` escreve numa coluna de bool.

    `episodes.csv` traz `is_malicious` como **`1` e `0`**, nao como `True` e
    `False` — o `pandas` escreveu a coluna como inteiro. Ler so `true` fez as
    familias P, B e L virarem benignas em silencio, e a tabela por episodio
    saiu vazia nelas sem erro nenhum. As duas formas entram aqui.
    """
    return str(texto).strip().lower() in {"1", "true", "yes", "t"}


def _le_csv(caminho: Path):
    if not caminho.exists():
        raise EvaluatorError(f"{caminho} nao existe")
    abrir = gzip.open if caminho.suffix == ".gz" else open
    with abrir(caminho, "rt", newline="", encoding="utf-8") as arquivo:
        yield from csv.DictReader(arquivo)


def carrega_gabarito(raiz: Path, run_id: int) -> Gabarito:
    """Le `episodes.csv` e `event_labels.csv.gz` de um `run_NNN/`."""
    gt = Gabarito()
    for linha in _le_csv(raiz / "ground_truth" / "episodes.csv"):
        if int(linha["run_id"]) != run_id:
            continue
        ep = int(linha["episode_id"])
        gt.familia_de[ep] = linha["family"]
        gt.maliciosos_por_episodio[ep] = _verdadeiro(linha["is_malicious"])

    for linha in _le_csv(raiz / "ground_truth" / "event_labels.csv.gz"):
        if int(linha["run_id"]) != run_id:
            continue
        gt.episodio_de[linha["event_id"]] = int(linha["episode_id"])
        if linha["label"] == "malicious":
            gt.maliciosos.add(linha["event_id"])

    if not gt.familia_de:
        raise EvaluatorError(f"o gabarito nao tem episodio da semente {run_id}")
    return gt


def carrega_notas(dados: Path, scoring_run_id: int) -> list[tuple[str, float]]:
    """Le `sdcac/notas/<id>.jsonl` e devolve (event_id, nota) por evento."""
    caminho = dados / "sdcac" / "notas" / f"{scoring_run_id}.jsonl"
    if not caminho.exists():
        raise EvaluatorError(f"{caminho} nao existe: a execucao nao gravou nota")
    with caminho.open(encoding="utf-8") as arquivo:
        notas = [
            (dados_da_nota["event_id"], float(dados_da_nota["final_raw"]))
            for linha in arquivo
            if (dados_da_nota := json.loads(linha))
        ]
    if not notas:
        raise EvaluatorError(f"{caminho} esta vazio")
    return notas


def _curva(notas: list[tuple[str, float]], maliciosos: set[str]) -> list[dict]:
    """A curva revocacao/FPR, um ponto por valor distinto de nota.

    Ordena por nota decrescente e caminha. Cada ponto e "alertar tudo com nota
    >= este valor" — e so vale como ponto de corte quando o valor termina, nao
    no meio de um empate: eventos de nota igual nao se separam por limiar.
    """
    ordenadas = sorted(notas, key=lambda par: -par[1])
    positivos = sum(1 for eid, _ in notas if eid in maliciosos)
    negativos = len(notas) - positivos
    if positivos == 0 or negativos == 0:
        raise EvaluatorError(
            f"a janela tem {positivos} evento malicioso e {negativos} benigno: "
            "sem as duas classes nao existe revocacao nem FPR"
        )

    pontos, tp, fp = [], 0, 0
    for i, (eid, nota) in enumerate(ordenadas):
        if eid in maliciosos:
            tp += 1
        else:
            fp += 1
        ultimo_do_empate = i + 1 == len(ordenadas) or ordenadas[i + 1][1] != nota
        if ultimo_do_empate:
            pontos.append(
                {
                    "limiar": nota,
                    "alertados": i + 1,
                    "tp": tp,
                    "fp": fp,
                    "revocacao": tp / positivos,
                    "fpr": fp / negativos,
                }
            )
    return pontos


def fpr_a_revocacao_fixa(
    notas: list[tuple[str, float]], maliciosos: set[str], niveis=NIVEIS_DE_REVOCACAO
) -> dict[str, dict]:
    """A FPR no limiar mais alto que ainda alcanca cada revocacao pedida.

    Todo nivel tem resposta: o ultimo ponto da curva alerta o log inteiro e
    chega a revocacao 1,0. O que distingue uma configuracao ruim nao e a
    ausencia do ponto — e a FPR dele, que tende a 100% quando a unica forma de
    alcancar a revocacao e alertar tudo. Ver o cabecalho do modulo.
    """
    curva = _curva(notas, maliciosos)
    saida: dict[str, dict] = {}
    for nivel in niveis:
        ponto = next(p for p in curva if p["revocacao"] >= nivel)
        saida[f"{nivel:.2f}"] = {
            "limiar": ponto["limiar"],
            "fpr": ponto["fpr"],
            "revocacao_obtida": ponto["revocacao"],
            "alertados": ponto["alertados"],
            # A fracao do log que precisou ser alertada para chegar ali. E o
            # numero que diz se o ponto e operavel: 100% de FPR e 100% de log
            # alertado sao a mesma frase dita de duas formas.
            "fracao_do_log": ponto["alertados"] / len(notas),
        }
    return saida


def matriz_por_evento(
    notas: list[tuple[str, float]], maliciosos: set[str], limiar: float
) -> dict[str, float]:
    """A matriz de confusao por evento no limiar de operacao da configuracao."""
    tp = fp = tn = fn = 0
    for eid, nota in notas:
        alertou = nota >= limiar
        malicioso = eid in maliciosos
        if alertou and malicioso:
            tp += 1
        elif alertou:
            fp += 1
        elif malicioso:
            fn += 1
        else:
            tn += 1
    return {
        "limiar": limiar,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "revocacao": tp / (tp + fn) if tp + fn else 0.0,
        "precisao": tp / (tp + fp) if tp + fp else 0.0,
        "fpr": fp / (fp + tn) if fp + tn else 0.0,
    }


def revocacao_por_episodio(
    notas: list[tuple[str, float]], gt: Gabarito, limiar: float
) -> dict[str, dict]:
    """Revocacao por familia, contando episodio e nao evento.

    Um episodio esta detectado quando **pelo menos um** evento dele passa do
    limiar. E a unidade que a D-12 ainda nao escolheu, e a que faz diferenca
    justamente nos cenarios longitudinais, onde nenhum evento isolado e grave.
    """
    melhor: dict[int, float] = defaultdict(lambda: float("-inf"))
    eventos_por_episodio: dict[int, int] = defaultdict(int)
    for eid, nota in notas:
        ep = gt.episodio_de.get(eid)
        if ep is None:
            continue
        eventos_por_episodio[ep] += 1
        melhor[ep] = max(melhor[ep], nota)

    saida: dict[str, dict] = {}
    for familia, descricao in FAMILIAS.items():
        maliciosa = familia != "N"
        episodios = {
            ep
            for ep in gt.episodios_da_familia(familia, maliciosos=maliciosa)
            if ep in melhor
        }
        detectados = {ep for ep in episodios if melhor[ep] >= limiar}
        saida[familia] = {
            "descricao": descricao,
            "episodios_na_janela": len(episodios),
            "detectados": len(detectados),
            # Numa familia maliciosa isto e revocacao; na `N` e taxa de alarme
            # sobre episodio benigno, que e o contrario de um acerto.
            "taxa": len(detectados) / len(episodios) if episodios else None,
            "eventos": sum(eventos_por_episodio[ep] for ep in episodios),
        }
    return saida


def avalia(
    dados: Path, gerado: Path, run_id: int, execucoes: dict[str, int], limiar: float
) -> dict:
    """Avalia todas as configuracoes de uma semente e devolve o relatorio.

    Args:
        dados: o diretorio do adaptador, com `sdcac/` dentro.
        gerado: o `run_NNN/` do gerador, com `ground_truth/` dentro.
        run_id: a semente.
        execucoes: nome da configuracao -> `scoring_run_id` a avaliar.
        limiar: o corte de alerta usado na execucao.
    """
    gt = carrega_gabarito(gerado, run_id)
    relatorio = {
        "run_id": run_id,
        "limiar_de_operacao": limiar,
        "niveis_de_revocacao": list(NIVEIS_DE_REVOCACAO),
        "configuracoes": {},
    }
    for nome, scoring_run_id in execucoes.items():
        notas = carrega_notas(dados, scoring_run_id)
        relatorio["configuracoes"][nome] = {
            "scoring_run_id": scoring_run_id,
            "eventos_pontuados": len(notas),
            "eventos_maliciosos": sum(1 for eid, _ in notas if eid in gt.maliciosos),
            "por_evento": matriz_por_evento(notas, gt.maliciosos, limiar),
            "fpr_a_revocacao_fixa": fpr_a_revocacao_fixa(notas, gt.maliciosos),
            "por_episodio": revocacao_por_episodio(notas, gt, limiar),
        }
    return relatorio
