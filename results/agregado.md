# Agregado de 10 sementes

Gerado por `python -m evaluator.agregado_cli`. **Todo numero aqui saiu de execucao registrada** — nenhum foi estimado, e nenhum foi redigitado.

Sementes: **semente-1, semente-2, semente-3, semente-4, semente-5, semente-6, semente-7, semente-8, semente-9, semente-10** · limiar de operacao **20** · configuracoes **C0, C1, C2, C3**.

Escala por semente: **1.436.275 ± 9.681** eventos pontuados, dos quais **2.583 ± 54** maliciosos.

Toda celula e **media ± desvio-padrao amostral** sobre as sementes, em pontos percentuais.

## Ruido: FPR com a revocacao fixada

A primeira grandeza da **D-03**. FPR de 100,00 ± 0,00 se le como **so alcanca aquela revocacao alertando o registro inteiro** — e e resultado, nao celula vazia.

| Revocacao | **C0** | **C1** | **C2** | **C3** |
|---|---|---|---|---|
| **0,10** | 1,15 ± 0,71 | 0,01 ± 0,02 | 0,04 ± 0,02 | 0,05 ± 0,03 |
| **0,20** | 18,44 ± 1,49 | 6,03 ± 2,75 | 0,40 ± 0,19 | 0,54 ± 0,29 |
| **0,30** | 34,55 ± 34,52 | 14,05 ± 4,21 | 1,33 ± 0,55 | 1,70 ± 0,94 |
| **0,40** | 100,00 ± 0,00 | 23,27 ± 17,36 | 3,18 ± 1,60 | 3,47 ± 1,36 |
| **0,50** | 100,00 ± 0,00 | 58,75 ± 21,51 | 6,85 ± 1,01 | 7,18 ± 2,12 |
| **0,60** | 100,00 ± 0,00 | 72,09 ± 0,47 | 11,93 ± 4,13 | 14,04 ± 4,48 |
| **0,70** | 100,00 ± 0,00 | 72,09 ± 0,47 | 26,75 ± 4,24 | 28,33 ± 8,84 |
| **0,80** | 100,00 ± 0,00 | 72,09 ± 0,47 | 47,42 ± 14,82 | 52,87 ± 11,11 |
| **0,90** | 100,00 ± 0,00 | 100,00 ± 0,00 | 76,00 ± 1,41 | 73,69 ± 6,75 |

### Wilcoxon pareado, bilateral, p-valor exato

Hipotese nula: as duas configuracoes tem a mesma FPR na mesma semente. A palavra depois do p-valor diz o lado da **primeira** configuracao do par, e em FPR **menor e melhor**. Par com diferenca zero e descartado; quando sobra menos de uma semente por par, o n efetivo vem anotado.

| Revocacao | **C2 vs C0** | **C2 vs C1** | **C3 vs C2** | **C1 vs C0** |
|---|---|---|---|---|
| **0,10** | p = 0,0020 · menor | p = 0,0039 · maior | p = 0,0020 · maior | p = 0,0020 · menor |
| **0,20** | p = 0,0020 · menor | p = 0,0020 · menor | p = 0,0488 · maior | p = 0,0020 · menor |
| **0,30** | p = 0,0020 · menor | p = 0,0020 · menor | p = 0,2324 · maior | p = 0,0020 · menor |
| **0,40** | p = 0,0020 · menor | p = 0,0020 · menor | p = 0,7695 · maior | p = 0,0020 · menor |
| **0,50** | p = 0,0020 · menor | p = 0,0020 · menor | p = 1,0000 · maior | p = 0,0020 · menor |
| **0,60** | p = 0,0020 · menor | p = 0,0020 · menor | p = 0,0488 · maior | p = 0,0020 · menor |
| **0,70** | p = 0,0020 · menor | p = 0,0020 · menor | p = 0,9219 · maior | p = 0,0020 · menor |
| **0,80** | p = 0,0020 · menor | p = 0,0098 · menor | p = 0,2324 · maior | p = 0,0020 · menor |
| **0,90** | p = 0,0020 · menor | p = 0,0020 · menor | p = 0,1602 · menor | idênticas |

### Revocacao obtida em cada nivel

A conferencia de que o nivel foi alcancado. O limiar e discreto, e por isso o ponto escolhido costuma passar do nivel pedido.

| Nivel | **C0** | **C1** | **C2** | **C3** |
|---|---|---|---|---|
| **0,10** | 12,5 ± 1,9 | 10,7 ± 0,5 | 10,3 ± 0,3 | 10,1 ± 0,0 |
| **0,20** | 32,3 ± 2,7 | 23,4 ± 2,8 | 20,3 ± 0,2 | 20,5 ± 0,7 |
| **0,30** | 46,4 ± 28,3 | 37,0 ± 5,8 | 31,3 ± 1,2 | 31,2 ± 1,4 |
| **0,40** | 100,0 ± 0,0 | 48,5 ± 11,9 | 41,2 ± 2,2 | 40,9 ± 0,8 |
| **0,50** | 100,0 ± 0,0 | 72,9 ± 15,1 | 51,6 ± 2,2 | 50,9 ± 1,0 |
| **0,60** | 100,0 ± 0,0 | 82,5 ± 0,7 | 60,4 ± 0,6 | 60,7 ± 0,7 |
| **0,70** | 100,0 ± 0,0 | 82,5 ± 0,7 | 70,9 ± 0,6 | 70,7 ± 0,7 |
| **0,80** | 100,0 ± 0,0 | 82,5 ± 0,7 | 82,3 ± 3,3 | 82,1 ± 1,7 |
| **0,90** | 100,0 ± 0,0 | 100,0 ± 0,0 | 90,7 ± 0,6 | 90,9 ± 0,9 |

## Cobertura: deteccao por episodio no limiar de operacao

A familia **N** e benigna por construcao: ali a coluna nao e cobertura, e **alarme sobre atividade legitima**. Quanto menor, melhor — ao contrario de todas as outras linhas.

| Familia | Episodios | **C0** | **C1** | **C2** | **C3** |
|---|---|---|---|---|---|
| **P** | 24,0 | 83,3 ± 0,0 | 100,0 ± 0,0 | 100,0 ± 0,0 | 100,0 ± 0,0 |
| **B** | 16,0 | 28,7 ± 3,2 | 45,6 ± 3,0 | 98,8 ± 2,6 | 100,0 ± 0,0 |
| **L** | 12,0 | 35,0 ± 10,2 | 89,2 ± 7,9 | 100,0 ± 0,0 | 100,0 ± 0,0 |
| **N** ⚠️ alarme | 59,9 | 75,8 ± 1,1 | 93,3 ± 0,2 | 96,0 ± 2,6 | 100,0 ± 0,0 |

### Wilcoxon pareado por familia

| Familia | **C2 vs C0** | **C2 vs C1** | **C3 vs C2** | **C1 vs C0** |
|---|---|---|---|---|
| **P** | p = 0,0020 · maior | idênticas | idênticas | p = 0,0020 · maior |
| **B** | p = 0,0020 · maior | p = 0,0020 · maior | p = 0,5000 (n=2) · maior | p = 0,0020 · maior |
| **L** | p = 0,0020 · maior | p = 0,0078 (n=8) · maior | idênticas | p = 0,0020 · maior |
| **N** | p = 0,0020 · maior | p = 0,0156 (n=7) · maior | p = 0,0039 (n=9) · maior | p = 0,0020 · maior |

## Por evento, no limiar de operacao

| Metrica | **C0** | **C1** | **C2** | **C3** |
|---|---|---|---|---|
| **revocacao** | 32,27 ± 2,66 | 44,00 ± 3,97 | 65,40 ± 2,47 | 99,99 ± 0,03 |
| **fpr** | 18,44 ± 1,49 | 17,97 ± 1,52 | 20,75 ± 1,36 | 99,84 ± 0,01 |
| **precisao** | 0,32 ± 0,04 | 0,44 ± 0,05 | 0,57 ± 0,04 | 0,18 ± 0,00 |
