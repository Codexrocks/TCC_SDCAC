# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.435.546 | 2.638 | 769 | 287.310 | 1.869 | 29.15% | 20.05% | 0.27% |
| **C1** | 1.435.546 | 2.638 | 955 | 279.100 | 1.683 | 36.20% | 19.48% | 0.34% |
| **C2** | 1.435.546 | 2.638 | 1.593 | 315.140 | 1.045 | 60.39% | 21.99% | 0.50% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 1.60% (1.6%) | 20.05% (20.1%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 11.13% (11.2%) | 19.48% (19.5%) | 72.52% (72.5%) | 72.52% (72.5%) | 72.52% (72.5%) | 72.52% (72.5%) | 72.52% (72.5%) | 100.00% (100.0%) |
| **C2** | 0.02% (0.0%) | 0.68% (0.7%) | 1.83% (1.9%) | 6.54% (6.6%) | 8.59% (8.7%) | 21.99% (22.1%) | 37.98% (38.0%) | 75.52% (75.5%) | 79.67% (79.7%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 5/16 (31.2%) | 3/12 (25.0%) | 42/57 (73.7%) |
| **C1** | 24/24 (100.0%) | 7/16 (43.8%) | 9/12 (75.0%) | 53/57 (93.0%) |
| **C2** | 24/24 (100.0%) | 15/16 (93.8%) | 12/12 (100.0%) | 53/57 (93.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
