"""A API de leitura — a segunda entrada do monolito.

Fala HTTP e nao sabe pontuar: ela le o que o executor gravou e serializa. As
duas entradas, `runner/` e `backend/`, importam o mesmo nucleo em `detection/`,
e e isso que garante que o painel mostre o mesmo codigo que produziu a tabela do
artigo.
"""
