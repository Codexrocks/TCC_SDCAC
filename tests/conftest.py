"""Deixa os scripts de `scripts/` importaveis pelos testes.

Eles nao sao um pacote instalavel — sao ferramentas de linha de comando — entao
o caminho entra no sys.path na mao, uma vez so.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
