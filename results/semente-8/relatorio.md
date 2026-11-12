# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.433.841 | 2.519 | 805 | 244.672 | 1.714 | 31.96% | 17.09% | 0.33% |
| **C1** | 1.433.841 | 2.519 | 1.126 | 241.424 | 1.393 | 44.70% | 16.87% | 0.46% |
| **C2** | 1.433.841 | 2.519 | 1.625 | 288.466 | 894 | 64.51% | 20.15% | 0.56% |
| **C3** | 1.433.841 | 2.519 | 2.519 | 1.428.952 | 0 | 100.00% | 99.83% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 1.62% (1.6%) | 17.09% (17.1%) | 17.09% (17.1%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 4.74% (4.8%) | 16.87% (16.9%) | 16.87% (16.9%) | 71.70% (71.7%) | 71.70% (71.7%) | 71.70% (71.7%) | 71.70% (71.7%) | 100.00% (100.0%) |
| **C2** | 0.05% (0.1%) | 0.37% (0.4%) | 1.62% (1.7%) | 3.81% (3.9%) | 6.92% (7.0%) | 14.19% (14.3%) | 26.23% (26.3%) | 41.96% (42.0%) | 75.50% (75.5%) |
| **C3** | 0.05% (0.1%) | 0.58% (0.6%) | 2.96% (3.0%) | 4.84% (4.9%) | 10.18% (10.2%) | 21.70% (21.8%) | 36.62% (36.7%) | 61.94% (62.0%) | 75.16% (75.2%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 5/16 (31.2%) | 4/12 (33.3%) | 45/59 (76.3%) |
| **C1** | 24/24 (100.0%) | 7/16 (43.8%) | 10/12 (83.3%) | 55/59 (93.2%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 58/59 (98.3%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 59/59 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
