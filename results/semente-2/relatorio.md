# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.435.938 | 2.559 | 873 | 306.300 | 1.686 | 34.11% | 21.37% | 0.28% |
| **C1** | 1.435.938 | 2.559 | 1.295 | 302.761 | 1.264 | 50.61% | 21.12% | 0.43% |
| **C2** | 1.435.938 | 2.559 | 1.758 | 338.505 | 801 | 68.70% | 23.62% | 0.52% |
| **C3** | 1.435.938 | 2.559 | 2.557 | 1.431.164 | 2 | 99.92% | 99.85% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 1.80% (1.8%) | 21.37% (21.4%) | 21.37% (21.4%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 1.82% (1.9%) | 12.34% (12.4%) | 21.12% (21.2%) | 21.12% (21.2%) | 73.04% (73.1%) | 73.04% (73.1%) | 73.04% (73.1%) | 100.00% (100.0%) |
| **C2** | 0.02% (0.0%) | 0.23% (0.3%) | 0.52% (0.6%) | 1.77% (1.8%) | 6.88% (7.0%) | 9.31% (9.4%) | 24.19% (24.3%) | 40.29% (40.4%) | 76.01% (76.0%) |
| **C3** | 0.02% (0.0%) | 0.23% (0.3%) | 0.51% (0.6%) | 2.01% (2.1%) | 5.49% (5.6%) | 11.10% (11.2%) | 23.34% (23.4%) | 48.69% (48.7%) | 77.53% (77.5%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 5/16 (31.2%) | 5/12 (41.7%) | 45/60 (75.0%) |
| **C1** | 24/24 (100.0%) | 7/16 (43.8%) | 11/12 (91.7%) | 56/60 (93.3%) |
| **C2** | 24/24 (100.0%) | 15/16 (93.8%) | 12/12 (100.0%) | 57/60 (95.0%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 60/60 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
