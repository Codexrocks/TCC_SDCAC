"""Validacao de instante ISO 8601 para os campos de periodo do painel.

Mora aqui, e nao em `frontend/dashboard/telas.py`, por uma razao de CI: o
modulo de telas importa `streamlit`, que o CI **nao instala** -- ele instala so
`pytest pyyaml fastapi httpx`. Um teste que importasse as telas quebraria a
coleta inteira, como quebrou em 18/11/2026. Logica pura fica em
`frontend/components/`, que nao depende de streamlit, e por isso e testavel.
"""

from __future__ import annotations

from datetime import datetime

__all__ = ["iso_ok"]


def iso_ok(valor: str) -> bool:
    """O campo esta vazio ou traz um instante ISO 8601 que o Python aceita?

    Campo de texto livre que engole data invalida sem dizer nada foi o achado 7
    da avaliacao heuristica de 12/11/2026, de severidade 3: digitar `banana` e
    dar Enter nao produzia erro nem mudanca na fila.
    """
    if not valor.strip():
        return True
    try:
        datetime.fromisoformat(valor.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    return True
