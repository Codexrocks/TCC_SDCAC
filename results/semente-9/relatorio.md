# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.454.213 | 2.583 | 830 | 273.602 | 1.753 | 32.13% | 18.85% | 0.30% |
| **C1** | 1.454.213 | 2.583 | 1.188 | 264.668 | 1.395 | 45.99% | 18.23% | 0.45% |
| **C2** | 1.454.213 | 2.583 | 1.736 | 305.673 | 847 | 67.21% | 21.06% | 0.56% |
| **C3** | 1.454.213 | 2.583 | 2.583 | 1.449.326 | 0 | 100.00% | 99.84% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 1.60% (1.6%) | 18.85% (18.9%) | 18.85% (18.9%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.00% (0.0%) | 4.70% (4.7%) | 10.30% (10.3%) | 18.23% (18.3%) | 72.27% (72.3%) | 72.27% (72.3%) | 72.27% (72.3%) | 72.27% (72.3%) | 100.00% (100.0%) |
| **C2** | 0.04% (0.1%) | 0.23% (0.3%) | 0.65% (0.7%) | 1.69% (1.8%) | 4.49% (4.6%) | 8.70% (8.8%) | 25.43% (25.5%) | 40.58% (40.6%) | 75.36% (75.4%) |
| **C3** | 0.05% (0.1%) | 0.42% (0.5%) | 0.99% (1.0%) | 2.83% (2.9%) | 9.66% (9.7%) | 15.92% (16.0%) | 30.28% (30.3%) | 47.50% (47.6%) | 75.32% (75.4%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 4/16 (25.0%) | 4/12 (33.3%) | 45/59 (76.3%) |
| **C1** | 24/24 (100.0%) | 7/16 (43.8%) | 12/12 (100.0%) | 55/59 (93.2%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 56/59 (94.9%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 59/59 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
