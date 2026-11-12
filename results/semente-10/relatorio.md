# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.427.301 | 2.648 | 797 | 268.153 | 1.851 | 30.10% | 18.82% | 0.30% |
| **C1** | 1.427.301 | 2.648 | 1.190 | 263.923 | 1.458 | 44.94% | 18.53% | 0.45% |
| **C2** | 1.427.301 | 2.648 | 1.730 | 299.125 | 918 | 65.33% | 21.00% | 0.58% |
| **C3** | 1.427.301 | 2.648 | 2.648 | 1.422.273 | 0 | 100.00% | 99.83% | 0.19% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 0.32% (0.3%) | 18.82% (18.8%) | 18.82% (18.8%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 6.51% (6.5%) | 18.53% (18.6%) | 18.53% (18.6%) | 72.20% (72.2%) | 72.20% (72.2%) | 72.20% (72.2%) | 72.20% (72.2%) | 100.00% (100.0%) |
| **C2** | 0.01% (0.0%) | 0.35% (0.4%) | 1.55% (1.6%) | 3.52% (3.6%) | 6.93% (7.0%) | 9.64% (9.7%) | 27.15% (27.2%) | 43.09% (43.2%) | 75.92% (75.9%) |
| **C3** | 0.03% (0.0%) | 0.43% (0.5%) | 1.32% (1.4%) | 1.96% (2.0%) | 4.85% (4.9%) | 10.00% (10.1%) | 30.42% (30.5%) | 62.31% (62.3%) | 75.38% (75.4%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 5/16 (31.2%) | 3/12 (25.0%) | 46/61 (75.4%) |
| **C1** | 24/24 (100.0%) | 8/16 (50.0%) | 11/12 (91.7%) | 57/61 (93.4%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 61/61 (100.0%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 61/61 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
