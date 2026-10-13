"""Nucleo de avaliacao de risco — C0, D1, D2 e D3.

Este pacote e Python puro: ele nao importa `fastapi`, nao importa `psycopg`,
nao le arquivo de configuracao do ambiente e **nao consulta o relogio**. Tudo
que ele precisa saber chega por parametro.

A razao nao e purismo. A Metodologia afirma ao leitor que as quatro
configuracoes sao "um unico codigo executado sob quatro parametros", e que o
painel mostra o mesmo risco que a tabela de resultados mediu. As duas frases so
continuam verdadeiras se existir um nucleo unico, chamado tanto pelo executor do
experimento quanto pela API — e isso exige que ele nao dependa de nenhum dos
dois.

Quem le daqui: `runner/` (o experimento) e `backend/` (a API). Nunca o
contrario. Ver docs/software.md, secao 3.
"""
