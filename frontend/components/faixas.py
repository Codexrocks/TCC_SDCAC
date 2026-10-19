"""Como cada faixa de risco se apresenta na tela — cor, rotulo e forma.

**A cor nunca vem sozinha.** O criterio 1.4.1 da WCAG proibe que a cor seja o
unico meio visual de transmitir informacao, e a
[usabilidade](../../docs/usabilidade.md), secao 5.1, registra que o desenho
original do painel — "indicacao azul, alerta amarelo, alerta critico vermelho" —
**reprovaria nesse criterio**: vermelho e amarelo sao o par mais afetado pela
deficiencia de visao de cores mais comum.

A correcao nao foi trocar de cor. Cada faixa carrega tres coisas ao mesmo tempo:

| Faixa | Cor | Rotulo | Forma |
|---|---|---|---|
| 0-20 | neutra | `NORMAL` | — |
| 21-50 | azul | `RISCO BAIXO` | circulo |
| 51-75 | amarelo | `RISCO MEDIO` | triangulo |
| 76-100 | vermelho | `RISCO ALTO` | octogono preenchido |

**As faixas em si nao se decidem aqui.** Os limiares moram em
`detection/presets.toml` e a classificacao, em `detection.integracao.band_of`.
Este modulo so sabe pintar o que o motor decidiu — e `tests/test_faixas.py`
reprova se o intervalo escrito na legenda deixar de corresponder ao que o
`band_of` faz. Quem decide sobre as faixas e a Yasmin.

**O octogono e desenhado, nao escrito.** Nenhuma fonte de texto comum tem
glifo de octogono preenchido: o que existe e emoji, que muda de forma entre
sistemas. Entao a forma sai em SVG, com os oito vertices calculados — assim o
octogono e octogono, e nao um hexagono com nome errado.
"""

import math
from dataclasses import dataclass

from detection.model import RiskBand


@dataclass(frozen=True)
class Faixa:
    """A apresentacao de uma faixa de risco."""

    band: RiskBand
    rotulo: str
    intervalo: str
    cor_fundo: str
    cor_texto: str
    forma: str
    lados: int
    """Vertices do poligono. 0 e circulo; -1 e sem forma."""

    @property
    def descricao(self) -> str:
        """O texto que vai na legenda, com rotulo, intervalo e forma."""
        if self.lados < 0:
            return f"{self.rotulo} ({self.intervalo})"
        return f"{self.rotulo} ({self.intervalo}) · {self.forma}"


FAIXAS: dict[RiskBand, Faixa] = {
    RiskBand.NORMAL: Faixa(
        band=RiskBand.NORMAL,
        rotulo="NORMAL",
        intervalo="0-20",
        cor_fundo="#EDEFF2",
        cor_texto="#1F2430",
        forma="sem forma",
        lados=-1,
    ),
    RiskBand.LOW: Faixa(
        band=RiskBand.LOW,
        rotulo="RISCO BAIXO",
        intervalo="21-50",
        cor_fundo="#D8E6FF",
        cor_texto="#0B3B8C",
        forma="círculo",
        lados=0,
    ),
    RiskBand.MEDIUM: Faixa(
        band=RiskBand.MEDIUM,
        rotulo="RISCO MÉDIO",
        intervalo="51-75",
        cor_fundo="#FFF0BF",
        cor_texto="#5A4100",
        forma="triângulo",
        lados=3,
    ),
    RiskBand.HIGH: Faixa(
        band=RiskBand.HIGH,
        rotulo="RISCO ALTO",
        intervalo="76-100",
        cor_fundo="#FFDAD6",
        cor_texto="#8C1007",
        forma="octógono preenchido",
        lados=8,
    ),
}


def faixa_de(band: RiskBand | str) -> Faixa:
    """A apresentacao da faixa que o motor devolveu.

    Aceita o enum ou a string do contrato da API (`normal`, `low`, `medium`,
    `high`), que e o que chega numa resposta HTTP.
    """
    try:
        chave = band if isinstance(band, RiskBand) else RiskBand(band)
    except ValueError as erro:
        conhecidas = ", ".join(b.value for b in RiskBand)
        raise ValueError(
            f"faixa {band!r} nao existe no contrato. As do motor sao: {conhecidas}. "
            "Pintar faixa desconhecida de cinza esconderia divergencia entre o "
            "painel e o motor"
        ) from erro
    return FAIXAS[chave]


def _poligono(lados: int, tamanho: int) -> str:
    """Os vertices de um poligono regular, em coordenadas SVG.

    O primeiro vertice fica no topo para o triangulo apontar para cima; o
    octogono recebe meia volta de rotacao para assentar numa aresta, que e como
    uma placa de parada se desenha.
    """
    raio = tamanho / 2
    giro = -math.pi / 2 + (math.pi / lados if lados % 2 == 0 else 0)
    pontos = []
    for i in range(lados):
        angulo = giro + i * 2 * math.pi / lados
        pontos.append(
            f"{raio + raio * math.cos(angulo):.2f},{raio + raio * math.sin(angulo):.2f}"
        )
    return " ".join(pontos)


def forma_svg(faixa: Faixa, tamanho: int = 13) -> str:
    """A forma da faixa como SVG embutido, ou vazio se a faixa nao tem forma."""
    if faixa.lados < 0:
        return ""
    comum = (
        f'<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 {tamanho} {tamanho}" '
        f'role="img" aria-label="{faixa.forma}" style="vertical-align:-1px">'
    )
    if faixa.lados == 0:
        meio = tamanho / 2
        miolo = f'<circle cx="{meio}" cy="{meio}" r="{meio - 0.5}" fill="{faixa.cor_texto}"/>'
    else:
        pontos = _poligono(faixa.lados, tamanho)
        miolo = f'<polygon points="{pontos}" fill="{faixa.cor_texto}"/>'
    return f"{comum}{miolo}</svg>"


def selo_html(band: RiskBand | str, *, nota: float | None = None) -> str:
    """O selo da faixa, com forma, rotulo e — quando houver — a nota.

    Sai como HTML porque a tabela do Streamlit nao renderiza marcacao: o selo e
    para `st.markdown(..., unsafe_allow_html=True)`.
    """
    faixa = faixa_de(band)
    texto = faixa.rotulo if nota is None else f"{faixa.rotulo} · {nota:.0f}"
    espaco = " " if faixa.lados >= 0 else ""
    return (
        f'<span style="background:{faixa.cor_fundo};color:{faixa.cor_texto};'
        "padding:2px 8px;border-radius:10px;font-size:0.8rem;font-weight:600;"
        'white-space:nowrap">'
        f"{forma_svg(faixa)}{espaco}{texto}</span>"
    )


def legenda_html() -> str:
    """As quatro faixas lado a lado, para o rodape de qualquer tela."""
    selos = " ".join(selo_html(f.band) for f in FAIXAS.values())
    return (
        '<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">'
        f"{selos}</div>"
    )
