# Metricas da semente 1

Gerado por `python -m evaluator`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado.

Limiar de operacao: **20**.

## Por evento, no limiar de operacao

| Config | Pontuados | Maliciosos | TP | FP | FN | Revocacao | FPR | Precisao |
|---|---|---|---|---|---|---|---|---|
| **C0** | 1.424.321 | 2.516 | 740 | 267.085 | 1.776 | 29.41% | 18.78% | 0.28% |
| **C1** | 1.424.321 | 2.516 | 1.013 | 260.296 | 1.503 | 40.26% | 18.31% | 0.39% |
| **C2** | 1.424.321 | 2.516 | 1.601 | 297.914 | 915 | 63.63% | 20.95% | 0.53% |
| **C3** | 1.424.321 | 2.516 | 2.516 | 1.419.484 | 0 | 100.00% | 99.84% | 0.18% |

## Ruido: FPR com a revocacao fixada (por evento)

A grandeza da **D-03**. Toda revocacao e alcancavel baixando o limiar ate alertar o log inteiro — por isso nao existe celula vazia aqui, e **FPR de 100% se le como "so alcanca alertando tudo"**. A fracao do log alertada esta entre parenteses.

| Config | rev. 0.10 | rev. 0.20 | rev. 0.30 | rev. 0.40 | rev. 0.50 | rev. 0.60 | rev. 0.70 | rev. 0.80 | rev. 0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **C0** | 1.80% (1.8%) | 18.78% (18.8%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) | 100.00% (100.0%) |
| **C1** | 0.07% (0.1%) | 10.15% (10.2%) | 18.31% (18.3%) | 18.31% (18.3%) | 72.18% (72.2%) | 72.18% (72.2%) | 72.18% (72.2%) | 72.18% (72.2%) | 100.00% (100.0%) |
| **C2** | 0.07% (0.1%) | 0.69% (0.7%) | 1.96% (2.0%) | 4.18% (4.2%) | 7.08% (7.2%) | 13.52% (13.6%) | 28.22% (28.3%) | 75.24% (75.3%) | 76.64% (76.7%) |
| **C3** | 0.13% (0.1%) | 1.23% (1.3%) | 2.86% (2.9%) | 4.53% (4.6%) | 6.44% (6.5%) | 13.60% (13.7%) | 29.73% (29.8%) | 60.97% (61.0%) | 75.13% (75.2%) |

## Cobertura: por episodio, no limiar de operacao

Um episodio conta como detectado quando **pelo menos um** evento dele passa do limiar. A unidade de analise e a **D-12**, que esta aberta — por isso as duas tabelas, e nao uma.

A familia **N** e benigna por construcao: ali a coluna nao e revocacao, e **alarme sobre atividade legitima**. Quanto menor, melhor.

| Config | P | B | L | N |
|---|---|---|---|---|
| **C0** | 20/24 (83.3%) | 4/16 (25.0%) | 3/12 (25.0%) | 45/59 (76.3%) |
| **C1** | 24/24 (100.0%) | 8/16 (50.0%) | 10/12 (83.3%) | 55/59 (93.2%) |
| **C2** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 56/59 (94.9%) |
| **C3** | 24/24 (100.0%) | 16/16 (100.0%) | 12/12 (100.0%) | 59/59 (100.0%) |

Legenda das familias: **P** pontual · **B** comportamental · **L** longitudinal · **N** normal (benigno por construcao)
