"""O baseline do gerador tem de ser os 3 meses da D-24, e nao o que a constante disser.

**Por que este arquivo existe.** Ate 04/11/2026 o `EVAL_START_DAY` valia 100, e a
checagem da secao 9 que anunciava a D-24 comparava os cenarios com
`W.eval_start` — ou seja, com a propria constante. Ela passava por construcao,
qualquer que fosse o valor: verificava coerencia interna, nao aderencia a
decisao. O desvio de dez dias ficou invisivel porque nada media a decisao.

O primeiro teste roda **sempre**, inclusive sem numpy instalado, porque o
`generator/config.py` nao importa nada. E deliberado: o CI instala apenas
`pytest pyyaml fastapi httpx`, e um teste que dependa de numpy seria pulado em
silencio — que e exatamente o modo de falhar que este arquivo existe para
impedir.
"""

import calendar
from datetime import date, timedelta

import pytest

INICIO_PADRAO = date(2026, 1, 1)


def tres_meses(inicio):
    """Dias dos tres primeiros meses a partir de `inicio`, pelo calendario.

    Reimplementado aqui de proposito, com a biblioteca padrao: comparar o
    gerador com uma funcao do proprio gerador nao provaria nada.
    """
    mes = inicio.month + 3
    ano, mes = inicio.year + (mes - 1) // 12, (mes - 1) % 12 + 1
    dia = min(inicio.day, calendar.monthrange(ano, mes)[1])
    return (date(ano, mes, dia) - inicio).days


def test_o_baseline_declarado_sao_tres_meses():
    """A constante do gerador tem de bater com o calendario, nao com um palpite.

    Roda sem numpy: `generator/config.py` nao tem import nenhum.
    """
    from generator import config

    assert config.EVAL_START_DAY == tres_meses(INICIO_PADRAO), (
        f"EVAL_START_DAY={config.EVAL_START_DAY}, e os 3 meses da D-24 a partir "
        f"de {INICIO_PADRAO} sao {tres_meses(INICIO_PADRAO)} dias"
    )


def test_o_valor_antigo_seria_reprovado():
    """O par do teste acima: provar que ele discrimina.

    Sem isto, "a constante passa" nao distingue "esta certa" de "o teste nao
    olha". 100 era o valor anterior, e punha o inicio da avaliacao em 11 de
    abril — dez dias dentro do baseline que a D-24 reserva.
    """
    assert tres_meses(INICIO_PADRAO) == 90
    assert 100 != tres_meses(INICIO_PADRAO)
    # O que 100 significava na pratica: dez dias dentro da janela.
    assert INICIO_PADRAO + timedelta(days=100) == date(2026, 4, 11)
    assert INICIO_PADRAO + timedelta(days=90) == date(2026, 4, 1)


@pytest.mark.parametrize(
    ("inicio", "esperado"),
    [
        (date(2026, 1, 1), 90),  # 31 + 28 + 31; 2026 nao e bissexto
        (date(2024, 1, 1), 91),  # 31 + 29 + 31; 2024 e bissexto
        (date(2026, 1, 31), 89),  # 31/01 mais tres meses cai em 30/04
        (date(2026, 11, 1), 92),  # atravessa o ano: 01/11 -> 01/02 = 30+31+31
    ],
)
def test_tres_meses_pelo_calendario(inicio, esperado):
    """As bordas que uma subtracao de 90 dias fixos erraria."""
    assert tres_meses(inicio) == esperado


def test_o_gerador_deriva_os_tres_meses_do_calendario():
    """O helper do gerador tem de concordar com a reimplementacao daqui.

    Pulado sem numpy, porque `generator/checks.py` o importa. O teste que
    importa de verdade — o alinhamento da constante — roda sempre.
    """
    pytest.importorskip("numpy")
    from generator.checks import _dias_de_tres_meses

    for inicio in (
        date(2026, 1, 1),
        date(2024, 1, 1),
        date(2026, 1, 31),
        date(2026, 11, 1),
    ):
        assert _dias_de_tres_meses(inicio) == tres_meses(inicio)
