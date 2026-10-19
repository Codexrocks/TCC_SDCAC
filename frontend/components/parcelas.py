"""A decomposicao do risco — de onde vieram os pontos.

E a peca que o aceite da S9 cobra por nome: *"leitor externo identifica em menos
de 1 min por que um usuario esta em risco alto"*. A
[usabilidade](../../docs/usabilidade.md) diz o mesmo com outras palavras — um
numero sozinho e algo que o analista precisa aceitar sem poder verificar.

**As duas parcelas da D3 ficam separadas.** E a **D-25**, e o motor ja as guarda
em campos proprios. Somar conduta com postura numa barra so esconderia qual
delas causou o alerta, que e exatamente a pergunta de quem abre a tela.

**Nulo nao e zero, e a diferenca importa.** Uma parcela `null` quer dizer que a
configuracao **nao liga** aquela dimensao — a `c0` numa execucao C3, por
exemplo. Uma parcela `0.0` quer dizer que a dimensao rodou e **nao achou nada**.
Mostrar as duas como "0" faria a tabela de ablacao parecer que a C3 avalia
regras fixas e nao encontra nada, quando ela nem as liga. As duas aparecem
diferentes: a desligada sai como `nao ligada`, em cinza.

As perguntas de cada dimensao vem da [arquitetura](../../docs/arquitetura.md),
e nao foram reescritas aqui: e o que elas respondem que torna o numero
interpretavel em menos de um minuto.
"""

from dataclasses import dataclass

CINZA_FUNDO = "#EDEFF2"
CINZA_TEXTO = "#1F2430"
BARRA = "#4A5568"


@dataclass(frozen=True)
class Dimensao:
    """Uma parcela do score, como a arquitetura a descreve."""

    campo: str
    rotulo: str
    pergunta: str


DIMENSOES: tuple[Dimensao, ...] = (
    Dimensao(
        "c0",
        "C0 · regras fixas",
        "Este evento viola uma regra fixa, sem nenhum historico da pessoa?",
    ),
    Dimensao(
        "d1",
        "D1 · risco do evento",
        "Este evento, isolado, e arriscado?",
    ),
    Dimensao(
        "d2",
        "D2 · desvio do padrao",
        "Este conjunto destoa do que esta pessoa costuma fazer?",
    ),
    Dimensao(
        "d3_conduct",
        "D3a · conduta",
        "Recorrencia, combinacao e evolucao temporal dos comportamentos.",
    ),
    Dimensao(
        "d3_posture",
        "D3b · postura",
        "Higiene de seguranca: MFA, privilegio, dispositivo e phishing.",
    ),
)


@dataclass(frozen=True)
class Parcela:
    """Uma dimensao com o valor que a execucao produziu."""

    dimensao: Dimensao
    pontos: float | None

    @property
    def ligada(self) -> bool:
        """A configuracao liga esta dimensao?"""
        return self.pontos is not None

    @property
    def texto(self) -> str:
        """O valor como vai na tela — `nao ligada` nunca vira zero."""
        return "nao ligada" if self.pontos is None else f"{self.pontos:g}"


def parcelas_de(corpo: dict) -> list[Parcela]:
    """As cinco parcelas de uma nota, na ordem da arquitetura.

    A ordem e fixa e nao depende do que a API devolveu: tela cuja ordem de
    coluna muda com o dado e tela que o leitor precisa reler toda vez.
    """
    valores = corpo.get("parcels") or {}
    desconhecidas = set(valores) - {d.campo for d in DIMENSOES}
    if desconhecidas:
        raise ValueError(
            f"a resposta trouxe parcela que o painel nao conhece: "
            f"{sorted(desconhecidas)}. Mostrar so as conhecidas esconderia uma "
            "dimensao nova do motor justamente na tela que existe para decompor"
        )
    return [Parcela(d, valores.get(d.campo)) for d in DIMENSOES]


def soma_das_parcelas(parcelas: list[Parcela]) -> float:
    """O que as parcelas somam, ignorando as desligadas."""
    return sum(p.pontos for p in parcelas if p.pontos is not None)


def barra_html(parcelas: list[Parcela], largura: int = 420) -> str:
    """A barra empilhada das parcelas que pontuaram.

    E ilustracao: a tabela ao lado carrega os numeros, porque barra sozinha nao
    se le com leitor de tela nem com deficiencia de visao de cores. Parcela que
    nao pontuou nao entra, para nao virar um tracinho sem rotulo.
    """
    com_ponto = [(p.dimensao.rotulo, p.pontos) for p in parcelas if p.pontos]
    total = sum(pontos for _, pontos in com_ponto)
    if not total:
        return ""
    pedacos = []
    for i, (rotulo, pontos) in enumerate(com_ponto):
        fatia = pontos / total
        tom = 0.45 + 0.4 * (i / max(len(com_ponto) - 1, 1))
        pedacos.append(
            f'<div title="{rotulo}: {pontos:g}" '
            f'style="width:{fatia * 100:.1f}%;background:{BARRA};'
            f'opacity:{tom:.2f};height:14px"></div>'
        )
    return (
        f'<div role="img" aria-label="composicao do score por dimensao" '
        f'style="display:flex;width:{largura}px;max-width:100%;border-radius:4px;'
        f'overflow:hidden;gap:1px">{"".join(pedacos)}</div>'
    )


def motivo_html(hit: dict) -> str:
    """Uma regra que disparou, com o motivo em texto e os pontos."""
    regra = hit.get("rule", "?")
    pontos = hit.get("points", 0)
    motivo = hit.get("reason", "").strip() or "sem motivo registrado"
    return (
        f'<div style="background:{CINZA_FUNDO};color:{CINZA_TEXTO};'
        'padding:8px 10px;border-radius:6px;margin-bottom:6px">'
        f'<code style="font-size:0.78rem">{regra}</code> '
        f'<strong>+{pontos}</strong><br><span style="font-size:0.86rem">{motivo}</span>'
        "</div>"
    )
