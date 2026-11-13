"""As figuras da Secao 4, em SVG escrito a mao.

**Por que SVG a mao, e nao matplotlib.** Nao e por ele ser dependencia nova --
o `pyproject.toml` ja o declara. E porque **o CI instala `pytest pyyaml fastapi
httpx` e mais nada**: um teste que importasse matplotlib seria **pulado em
silencio** na nuvem, que e o modo de falhar que `tests/test_dependencias_do_ci.py`
existe para pegar. SVG e texto: sai de funcao pura, entra em teste, e o diff
mostra o que mudou.

Este modulo e para a figura que sai do **dado**. A captura de tela do painel
nao sai daqui: ela e feita a mao e versionada como imagem.

**Preto, tracejado e marcador, nao cor.** A `docs/usabilidade.md` secao 5.1 diz
que a cor nao pode ser o unico meio visual, e a razao vale igual no papel: o
artigo pode ser impresso em preto e branco. Cada serie se distingue por **traco,
marcador e rotulo ao fim da linha** -- tres meios, nenhum deles a cor.
"""

from __future__ import annotations

import math

# A area de desenho, no sistema de coordenadas do proprio SVG. A conversao para
# o documento reduz tudo na mesma proporcao, de modo que o que importa aqui e a
# razao entre as medidas, e nao o valor absoluto.
#
# A figura e **larga e baixa** de proposito. Ela entra num documento com teto
# de 12 paginas, e altura ali se paga em paragrafo cortado: achatar o desenho
# custa menos do que reduzir a largura, porque e a largura que decide se o
# texto dos eixos ainda se le no papel.
LARGURA = 720
ALTURA = 310
ESQUERDA = 74
DIREITA = 636  # sobra a direita para o rotulo de cada serie
TOPO = 16
BASE = 256

# O eixo vertical e logaritmico, em quatro decadas: 0,01% a 100%. Abaixo de
# 0,01% nao ha o que mostrar -- com 1,43 milhao de eventos pontuados, 0,01%
# equivale a cerca de 143 falsos positivos, e e o piso do que a escala resolve.
PISO_PCT = 0.01
TETO_PCT = 100.0
DECADAS = 4

FONTE = "Times New Roman, Times, serif"

# traco, marcador, e se o marcador e preenchido
ESTILOS = {
    "C0": ("", "circulo", False),
    "C1": ("8 4", "quadrado", False),
    "C2": ("", "triangulo", True),
    "C3": ("3 3", "losango", False),
}
ESPESSURA = {"C0": 1.6, "C1": 1.6, "C2": 2.6, "C3": 1.6}


def _y(pct: float) -> float:
    """Posicao vertical de um percentual na escala logaritmica."""
    valor = max(pct, PISO_PCT)
    altura = BASE - TOPO
    return TOPO + (math.log10(TETO_PCT) - math.log10(valor)) / DECADAS * altura


def _x(indice: int, total: int) -> float:
    """Posicao horizontal do i-esimo nivel de revocacao."""
    if total < 2:
        return (ESQUERDA + DIREITA) / 2
    return ESQUERDA + indice * (DIREITA - ESQUERDA) / (total - 1)


def _marcador(forma: str, x: float, y: float, preenchido: bool) -> str:
    """O marcador da serie, em 5 unidades de raio."""
    r = 5.0
    preenche = "#000" if preenchido else "#fff"
    comum = f'fill="{preenche}" stroke="#000" stroke-width="1.4"'
    if forma == "circulo":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" {comum}/>'
    if forma == "quadrado":
        return (
            f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" '
            f'height="{2 * r}" {comum}/>'
        )
    if forma == "triangulo":
        pontos = (
            f"{x:.1f},{y - r - 1:.1f} {x - r:.1f},{y + r:.1f} {x + r:.1f},{y + r:.1f}"
        )
        return f'<polygon points="{pontos}" {comum}/>'
    if forma == "losango":
        pontos = (
            f"{x:.1f},{y - r - 1:.1f} {x + r:.1f},{y:.1f} "
            f"{x:.1f},{y + r + 1:.1f} {x - r:.1f},{y:.1f}"
        )
        return f'<polygon points="{pontos}" {comum}/>'
    raise ValueError(f"marcador desconhecido: {forma}")


def _grade(niveis: list[float]) -> list[str]:
    """As linhas de referencia e os rotulos dos dois eixos."""
    partes = []
    for decada in range(DECADAS + 1):
        pct = TETO_PCT / (10**decada)
        y = _y(pct)
        partes.append(
            f'<line x1="{ESQUERDA}" y1="{y:.1f}" x2="{DIREITA}" y2="{y:.1f}" '
            'stroke="#bbb" stroke-width="1" stroke-dasharray="2 3"/>'
        )
        rotulo = f"{pct:g}".replace(".", ",")
        partes.append(
            f'<text x="{ESQUERDA - 10}" y="{y + 6:.1f}" text-anchor="end" '
            f'font-family="{FONTE}" font-size="17">{rotulo}</text>'
        )
    for i, nivel in enumerate(niveis):
        x = _x(i, len(niveis))
        partes.append(
            f'<line x1="{x:.1f}" y1="{BASE}" x2="{x:.1f}" y2="{BASE + 5}" '
            'stroke="#000" stroke-width="1"/>'
        )
        # o rotulo e montado antes: concatenar literais e so depois trocar o
        # ponto pela virgula trocaria tambem o ponto das coordenadas, e o SVG
        # passa a desenhar tudo em x=0 -- foi o que aconteceu na primeira versao
        rotulo = f"{nivel:.2f}".replace(".", ",")
        partes.append(
            f'<text x="{x:.1f}" y="{BASE + 24}" text-anchor="middle" '
            f'font-family="{FONTE}" font-size="17">{rotulo}</text>'
        )
    partes.append(
        f'<line x1="{ESQUERDA}" y1="{BASE}" x2="{DIREITA}" y2="{BASE}" '
        'stroke="#000" stroke-width="1.2"/>'
    )
    partes.append(
        f'<line x1="{ESQUERDA}" y1="{TOPO}" x2="{ESQUERDA}" y2="{BASE}" '
        'stroke="#000" stroke-width="1.2"/>'
    )
    partes.append(
        f'<text x="{(ESQUERDA + DIREITA) / 2:.0f}" y="{ALTURA - 8}" '
        f'text-anchor="middle" font-family="{FONTE}" font-size="18">'
        "Revocação fixada</text>"
    )
    meio = (TOPO + BASE) / 2
    partes.append(
        f'<text x="20" y="{meio:.0f}" text-anchor="middle" '
        f'font-family="{FONTE}" font-size="18" '
        f'transform="rotate(-90 20 {meio:.0f})">'
        "Falsos positivos (%)</text>"
    )
    return partes


def _serie(nome: str, pontos: list[tuple[float, float, float]]) -> list[str]:
    """A linha de uma configuracao, com as barras de desvio e o rotulo no fim."""
    traco, forma, preenchido = ESTILOS[nome]
    espessura = ESPESSURA[nome]
    dash = f' stroke-dasharray="{traco}"' if traco else ""
    caminho = " ".join(f"{x:.1f},{_y(media):.1f}" for x, media, _ in pontos)
    partes = [
        f'<polyline points="{caminho}" fill="none" stroke="#000" '
        f'stroke-width="{espessura}"{dash}/>'
    ]
    for x, media, desvio in pontos:
        alto, baixo = media + desvio, media - desvio
        if desvio > 0 and alto > PISO_PCT:
            partes.append(
                f'<line x1="{x:.1f}" y1="{_y(alto):.1f}" x2="{x:.1f}" '
                f'y2="{_y(baixo):.1f}" stroke="#000" stroke-width="1"/>'
            )
    for x, media, _ in pontos:
        partes.append(_marcador(forma, x, _y(media), preenchido))
    return partes


def _legenda(nomes: list[str], x0: float, y0: float) -> list[str]:
    """A legenda, em duas colunas, no canto que as curvas deixam vazio.

    Rotular o fim de cada linha seria mais direto, e nao serve aqui: a 0,90 de
    revocacao as quatro curvas se encontram acima de 70%, e os quatro rotulos
    cairiam um sobre o outro.
    """
    partes = []
    for i, nome in enumerate(nomes):
        traco, forma, preenchido = ESTILOS[nome]
        dash = f' stroke-dasharray="{traco}"' if traco else ""
        x = x0 + (i % 2) * 118
        y = y0 + (i // 2) * 34
        partes.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + 40:.1f}" y2="{y:.1f}" '
            f'stroke="#000" stroke-width="{ESPESSURA[nome]}"{dash}/>'
        )
        partes.append(_marcador(forma, x + 20, y, preenchido))
        partes.append(
            f'<text x="{x + 50:.1f}" y="{y + 6:.1f}" font-family="{FONTE}" '
            f'font-size="18">{nome}</text>'
        )
    return partes


def figura_fpr(agregado: dict) -> str:
    """A FPR de cada configuracao em cada nivel de revocacao fixada.

    E a figura da grandeza central da pergunta de pesquisa. Em escala
    logaritmica porque os valores vao de centesimos de ponto percentual a 100%,
    e numa escala linear as tres configuracoes boas virariam uma linha colada no
    eixo.

    Cada ponto e a media das sementes, e a barra vertical e o desvio-padrao
    amostral -- os mesmos numeros que a tabela da Secao 4.3.1 reportava.
    """
    niveis = list(agregado["niveis_de_revocacao"])
    fixa = agregado["fpr_a_revocacao_fixa"]
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA}" '
        f'height="{ALTURA}" viewBox="0 0 {LARGURA} {ALTURA}">',
        f'<rect width="{LARGURA}" height="{ALTURA}" fill="#fff"/>',
    ]
    partes += _grade(niveis)
    for nome in agregado["configuracoes"]:
        pontos = []
        for i, nivel in enumerate(niveis):
            resumo = fixa[f"{nivel:.2f}"]["por_configuracao"][nome]
            pontos.append(
                (_x(i, len(niveis)), resumo["media"] * 100, resumo["desvio"] * 100)
            )
        partes += _serie(nome, pontos)
    # abaixo de 1% e a partir de 0,50 de revocacao nao passa nenhuma curva
    partes += _legenda(list(agregado["configuracoes"]), 408, BASE - 106)
    partes.append("</svg>")
    return "\n".join(partes) + "\n"
