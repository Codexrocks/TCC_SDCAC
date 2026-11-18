"""Os achados de severidade 3 da avaliação heurística de 12/11/2026.

Cada teste aqui nasce de uma linha da planilha em
`docs/insumos/avaliacao-heuristica-davi-v1.csv`, e existe para que o defeito
não volte sem ninguém notar. O número do achado é o da planilha.

**Dois dos cinco achados de grau 3 não estão aqui, e não por esquecimento:**

- o **achado 2** pede a data e a hora da última ingestão na barra lateral, e o
  esquema `Execucao` do contrato não traz esse campo;
- o **achado 10** pede a nota e a regra na linha do alerta, e o esquema
  `Alerta` traz apenas `band`, `employee_id`, `event_id`, `raised_at`,
  `threshold` e a janela.

Os dois exigem mudar o contrato de leitura e o backend, e o painel não inventa
campo que a API não devolve — é a mesma regra que a **D-45** aplicou à tela de
Métricas. O **achado 19** foi corrigido pelo PR #114.
"""

from __future__ import annotations

import pytest

from frontend.dashboard.cliente import FonteExemplos, FonteHTTP, Painel
from frontend.dashboard.telas import _iso_ok

# ---------------------------------------------------------------------------
# Achado 6 — o filtro não tinha efeito, e a tela não dizia
# ---------------------------------------------------------------------------


def test_fonte_de_exemplos_declara_que_nao_filtra() -> None:
    """A fonte gravada ignora a query string, e agora **diz** que ignora."""
    assert FonteExemplos.filtra is False


def test_fonte_http_declara_que_filtra() -> None:
    """A API aplica o filtro: a query vai nela."""
    assert FonteHTTP.filtra is True


def test_painel_repassa_a_capacidade_de_filtrar() -> None:
    """A tela pergunta ao painel, não à fonte: é ele que ela conhece."""

    class FonteQualquer:
        filtra = False

        def obter(self, rota: str):  # pragma: no cover - nao usado aqui
            raise AssertionError("nao deveria ser chamado")

    assert Painel(FonteQualquer()).filtra is False


def test_painel_assume_que_filtra_quando_a_fonte_nao_diz() -> None:
    """Fonte antiga, sem o atributo, não vira aviso falso na tela."""

    class FonteAntiga:
        def obter(self, rota: str):  # pragma: no cover - nao usado aqui
            raise AssertionError("nao deveria ser chamado")

    assert Painel(FonteAntiga()).filtra is True


# ---------------------------------------------------------------------------
# Achado 7 — "banana" era aceito como data, sem aviso
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "valor",
    [
        "",
        "   ",
        "2026-04-01T00:00:00Z",
        "2026-04-01T00:00:00+00:00",
        "2026-04-01",
        "2026-12-31T23:59:59Z",
    ],
)
def test_iso_aceita_o_que_e_data(valor: str) -> None:
    assert _iso_ok(valor) is True


@pytest.mark.parametrize(
    "valor",
    [
        "banana",
        "01/04/2026",
        "2026-13-01T00:00:00Z",
        "2026-04-32T00:00:00Z",
        "ontem",
        "2026-04-01T25:00:00Z",
    ],
)
def test_iso_recusa_o_que_nao_e_data(valor: str) -> None:
    assert _iso_ok(valor) is False


def test_banana_e_o_caso_da_planilha() -> None:
    """O achado 7 cita o valor exato: `banana`, aceito sem mensagem."""
    assert _iso_ok("banana") is False
