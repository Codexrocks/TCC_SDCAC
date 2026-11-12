# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.445.309 | 2.666 | 900 | 243.138 | 1.766 | 33.76% | 16.85% | 0.37% |
| **C1** | 1.445.309 | 2.666 | 1.116 | 239.683 | 1.550 | 41.86% | 16.61% | 0.46% |
| **C2** | 1.445.309 | 2.666 | 1.771 | 275.564 | 895 | 66.43% | 19.10% | 0.64% |
| **C3** | 1.445.309 | 2.666 | 2.666 | 1.440.379 | 0 | 100.00% | 99.84% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 0.30% (0.3%) | 16.85% (16.9%) | 16.85% (16.9%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 4.63% (4.7%) | 9.09% (9.1%) | 16.61% (16.7%) | 71.61% (71.6%) | 71.61% (71.6%) | 71.61% (71.6%) | 71.61% (71.6%) | 100.00% (100.0%) |
| **C2** | 0.05% (0.1%) | 0.63% (0.7%) | 1.75% (1.8%) | 4.36% (4.4%) | 6.40% (6.5%) | 9.49% (9.6%) | 23.37% (23.5%) | 38.65% (38.7%) | 74.63% (74.7%) |
| **C3** | 0.06% (0.1%) | 0.43% (0.5%) | 1.47% (1.5%) | 3.10% (3.2%) | 6.07% (6.2%) | 10.11% (10.2%) | 18.35% (18.4%) | 32.84% (32.9%) | 60.03% (60.1%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 4/16 (25.0%) | 6/12 (50.0%) | 45/60 (75.0%) |
| **C1** | 24/24 (100.0%) | 7/16 (43.8%) | 11/12 (91.7%) | 56/60 (93.3%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 59/60 (98.3%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 60/60 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
