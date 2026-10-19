"""A razao de contraste da WCAG 2.2, calculada — nao afirmada.

A [usabilidade](../../docs/usabilidade.md), secao 5.2, exige **4,5:1** entre
texto e fundo, e **3:1** para texto grande. Exigencia escrita em documento e
pedido; o que a cumpre e um numero que alguem calcula.

Este modulo existe para que a escolha de cor do painel seja **provada**. O
`tests/test_faixas.py` passa cada par cor-de-texto/cor-de-fundo das quatro
faixas por aqui e reprova se algum cair abaixo de 4,5. Trocar o amarelo por um
tom mais claro deixa de ser questao de gosto: ou passa no teste, ou nao entra.

**O amarelo sobre branco e a armadilha que a usabilidade nomeia.** Com este
calculo ela para de depender de alguem lembrar: `contraste("#FFD400",
"#FFFFFF")` devolve 1,33, e 1,33 reprova.

A formula e a da WCAG 2.x: luminancia relativa de cada cor e a razao entre a
mais clara e a mais escura, ambas deslocadas em 0,05. O limite de 0,03928 na
linearizacao do canal e o que a norma escreve, e nao o 0,04045 que sairia da
algebra — a diferenca nao muda nenhuma decisao nesta faixa de cores, e seguir o
texto da norma e o que torna o numero conferivel contra ela.

Referencia: W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, criterio
1.4.3, outubro de 2023.
"""

MINIMO_TEXTO = 4.5
"""Criterio 1.4.3 para texto normal."""

MINIMO_TEXTO_GRANDE = 3.0
"""Criterio 1.4.3 para texto grande — 18pt, ou 14pt em negrito."""


def canais(cor: str) -> tuple[int, int, int]:
    """Os tres canais de uma cor `#RRGGBB` ou `#RGB`, de 0 a 255."""
    bruto = cor.strip().lstrip("#")
    if len(bruto) == 3:
        bruto = "".join(c * 2 for c in bruto)
    if len(bruto) != 6:
        raise ValueError(
            f"cor {cor!r} nao esta em #RRGGBB nem em #RGB. O painel nao adivinha "
            "cor: nome de cor do CSS passaria por aqui sem contraste conferido"
        )
    try:
        return tuple(int(bruto[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    except ValueError as erro:
        raise ValueError(f"cor {cor!r} tem digito que nao e hexadecimal") from erro


def luminancia(cor: str) -> float:
    """A luminancia relativa de uma cor, de 0 (preto) a 1 (branco)."""
    partes = []
    for canal in canais(cor):
        c = canal / 255
        partes.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    vermelho, verde, azul = partes
    return 0.2126 * vermelho + 0.7152 * verde + 0.0722 * azul


def contraste(frente: str, fundo: str) -> float:
    """A razao de contraste entre duas cores, de 1,0 a 21,0.

    A ordem dos argumentos nao altera o resultado: a razao e sempre da mais
    clara para a mais escura.
    """
    a, b = luminancia(frente), luminancia(fundo)
    clara, escura = max(a, b), min(a, b)
    return (clara + 0.05) / (escura + 0.05)


def passa(frente: str, fundo: str, *, grande: bool = False) -> bool:
    """O par cumpre o criterio 1.4.3?"""
    minimo = MINIMO_TEXTO_GRANDE if grande else MINIMO_TEXTO
    return contraste(frente, fundo) >= minimo
