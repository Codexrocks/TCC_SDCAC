"""Integracao das dimensoes na nota final.

A flag C0..C3 mora aqui: `compose` avalia o evento com as dimensoes que a
configuracao liga, e devolve a nota decomposta em campo por dimensao — com as
duas parcelas da D3 separadas, como a D-30 exige e como o banco guarda.
"""

from detection.integracao.composition import (
    Alert,
    EvaluationContext,
    RiskScore,
    alert_for,
    band_of,
    compose,
)

__all__ = [
    "Alert",
    "EvaluationContext",
    "RiskScore",
    "alert_for",
    "band_of",
    "compose",
]
