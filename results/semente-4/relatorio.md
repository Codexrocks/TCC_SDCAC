# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.447.027 | 2.604 | 987 | 267.737 | 1.617 | 37.90% | 18.54% | 0.37% |
| **C1** | 1.447.027 | 2.604 | 1.223 | 256.263 | 1.381 | 46.97% | 17.74% | 0.47% |
| **C2** | 1.447.027 | 2.604 | 1.709 | 297.620 | 895 | 65.63% | 20.60% | 0.57% |
| **C3** | 1.447.027 | 2.604 | 2.604 | 1.442.285 | 0 | 100.00% | 99.85% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 0.35% (0.4%) | 18.54% (18.6%) | 18.54% (18.6%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 5.14% (5.2%) | 10.18% (10.2%) | 17.74% (17.8%) | 31.85% (31.9%) | 72.14% (72.2%) | 72.14% (72.2%) | 72.14% (72.2%) | 100.00% (100.0%) |
| **C2** | 0.04% (0.1%) | 0.28% (0.3%) | 1.60% (1.7%) | 2.36% (2.4%) | 7.29% (7.4%) | 10.44% (10.5%) | 25.28% (25.4%) | 37.86% (37.9%) | 75.22% (75.3%) |
| **C3** | 0.05% (0.1%) | 0.43% (0.5%) | 1.30% (1.4%) | 3.21% (3.3%) | 7.22% (7.3%) | 12.02% (12.1%) | 21.47% (21.6%) | 44.66% (44.7%) | 65.04% (65.1%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 5/16 (31.2%) | 6/12 (50.0%) | 46/60 (76.7%) |
| **C1** | 24/24 (100.0%) | 7/16 (43.8%) | 11/12 (91.7%) | 56/60 (93.3%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 56/60 (93.3%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 60/60 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
