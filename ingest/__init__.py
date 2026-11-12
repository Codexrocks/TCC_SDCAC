"""Ingestao: traduz o CSV do gerador para o formato que a aplicacao le.

O gerador escreve CSV em `corp/` e `ground_truth/`; o adaptador de arquivo de
`storage/arquivos.py` le `catalogo.json`, `eventos.jsonl` e os dois arquivos de
estado. Este pacote e o elo entre os dois — o que faltava para o experimento
rodar sobre dado gerado em vez de *fixture* de teste.
"""

from ingest.corp import Mapeamento, converte_run

__all__ = ["Mapeamento", "converte_run"]
