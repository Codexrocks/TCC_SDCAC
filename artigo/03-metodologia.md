# 3. Metodologia

> **3ª Versão** na numeração do professor · S5 do
> [cronograma](../docs/cronograma.md) · Todos.
>
> Estrutura, não conteúdo. Cada bloco **A escrever** é para ser substituído
> pelo seu texto.

***

## 3.1 Natureza e tipo de pesquisa

> **A escrever.** As [diretrizes institucionais](../docs/diretrizes.md) listam
> os tipos possíveis. O nosso é **desenvolvimento de produto ou protótipo**, de
> natureza aplicada. Declare isso com todas as letras — é critério de
> avaliação.

## 3.2 Ambiente controlado

> **A escrever.** Como os dados são gerados: usuários simulados, massa de
> eventos normais e anômalos.
>
> Deixe explícito que **não há dado de pessoa real** — isso responde à
> exigência de ética em pesquisa das diretrizes.

## 3.3 Ferramentas e tecnologias

> **A escrever.** Python 3.12, FastAPI, PostgreSQL, Pandas, Streamlit. A
> justificativa de cada escolha importa mais que a lista. Detalhe técnico em
> [padrões de código](../docs/padroes-codigo.md).

## 3.4 Modelagem das regras de detecção

> **A escrever.** As quatro regras e seus pesos, conforme
> [arquitetura](../docs/arquitetura.md).
>
> Aqui é preciso **justificar** os pesos, não apenas apresentá-los: por que
> horário atípico vale 30 e força bruta vale 40? A banca pergunta, e "foi o que
> pareceu razoável" não sustenta.

## 3.5 Cálculo do Risk Score

> **A escrever.** Soma cumulativa, teto de 100, e as quatro faixas de
> severidade.

## 3.6 Cenários de teste

> **A escrever.** Os seis cenários de [arquitetura](../docs/arquitetura.md),
> com o score esperado de cada um.
>
> Eles viram teste automatizado — é o que transforma "o sistema detecta" em "o
> sistema detecta, e aqui está a prova que roda sozinha".

## 3.7 Avaliação de usabilidade

> **A escrever.** Método já definido e com fontes em
> [usabilidade](../docs/usabilidade.md), seção 6: avaliação heurística com
> escala de severidade, teste de tarefa e SUS.

## 3.8 Métricas de avaliação

> **A escrever.** Taxa de detecção (recall), taxa de falsos positivos e MTTD,
> com as fórmulas de [arquitetura](../docs/arquitetura.md). Diga como cada
> número será obtido.

***

## O que esta seção ainda precisa

* [ ] Natureza da pesquisa declarada conforme [diretrizes](../docs/diretrizes.md)
* [ ] Justificativa dos pesos das regras, não só a apresentação
* [ ] Declaração explícita de que não há dado de pessoa real
* [ ] Fórmulas conferidas contra [arquitetura](../docs/arquitetura.md)
