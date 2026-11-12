# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.431.378 | 2.564 | 856 | 244.480 | 1.708 | 33.39% | 17.11% | 0.35% |
| **C1** | 1.431.378 | 2.564 | 1.173 | 237.697 | 1.391 | 45.75% | 16.64% | 0.49% |
| **C2** | 1.431.378 | 2.564 | 1.638 | 285.576 | 926 | 63.88% | 19.99% | 0.57% |
| **C3** | 1.431.378 | 2.564 | 2.564 | 1.426.751 | 0 | 100.00% | 99.86% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 1.79% (1.8%) | 17.11% (17.1%) | 17.11% (17.1%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 6.39% (6.4%) | 9.26% (9.3%) | 16.64% (16.7%) | 30.56% (30.6%) | 71.80% (71.8%) | 71.80% (71.8%) | 71.80% (71.8%) | 100.00% (100.0%) |
| **C2** | 0.05% (0.1%) | 0.30% (0.3%) | 1.26% (1.3%) | 1.92% (2.0%) | 7.13% (7.2%) | 13.52% (13.6%) | 26.08% (26.2%) | 39.52% (39.6%) | 75.05% (75.1%) |
| **C3** | 0.05% (0.1%) | 0.50% (0.5%) | 2.73% (2.8%) | 5.72% (5.8%) | 10.02% (10.1%) | 21.46% (21.5%) | 45.91% (46.0%) | 66.00% (66.0%) | 84.71% (84.7%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 4/16 (25.0%) | 5/12 (41.7%) | 49/63 (77.8%) |
| **C1** | 24/24 (100.0%) | 7/16 (43.8%) | 12/12 (100.0%) | 59/63 (93.7%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 62/63 (98.4%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 63/63 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
