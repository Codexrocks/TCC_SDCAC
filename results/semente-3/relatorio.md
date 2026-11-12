# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.427.878 | 2.535 | 781 | 240.867 | 1.754 | 30.81% | 16.90% | 0.32% |
| **C1** | 1.427.878 | 2.535 | 1.082 | 230.395 | 1.453 | 42.68% | 16.16% | 0.47% |
| **C2** | 1.427.878 | 2.535 | 1.730 | 271.342 | 805 | 68.24% | 19.04% | 0.63% |
| **C3** | 1.427.878 | 2.535 | 2.535 | 1.423.061 | 0 | 100.00% | 99.84% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 0.35% (0.4%) | 16.90% (16.9%) | 16.90% (16.9%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 5.04% (5.1%) | 16.16% (16.2%) | 16.16% (16.2%) | 71.48% (71.5%) | 71.48% (71.5%) | 71.48% (71.5%) | 71.48% (71.5%) | 100.00% (100.0%) |
| **C2** | 0.04% (0.1%) | 0.27% (0.3%) | 0.58% (0.6%) | 1.68% (1.7%) | 6.84% (6.9%) | 8.54% (8.6%) | 23.53% (23.6%) | 41.48% (41.5%) | 75.99% (76.0%) |
| **C3** | 0.04% (0.1%) | 0.30% (0.3%) | 0.56% (0.6%) | 1.92% (2.0%) | 4.48% (4.6%) | 9.79% (9.9%) | 16.58% (16.7%) | 42.30% (42.4%) | 73.45% (73.5%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 5/16 (31.2%) | 3/12 (25.0%) | 46/61 (75.4%) |
| **C1** | 24/24 (100.0%) | 8/16 (50.0%) | 10/12 (83.3%) | 57/61 (93.4%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 57/61 (93.4%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 61/61 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
