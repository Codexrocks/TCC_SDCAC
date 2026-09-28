# 3. Metodologia

> **3ª Versão** na numeração do professor · S5 do
> [cronograma](../docs/cronograma.md) · Davi (caneta).
>
> Estrutura, não conteúdo. Cada bloco **A escrever** é para ser substituído
> pelo seu texto.
>
> **Esta seção congela o que será medido, antes de existir código a defender.**
> É a **M2**, em 01/10. Escreva com a [arquitetura](../docs/arquitetura.md) e o
> [registro de decisões](../docs/decisoes.md) abertos ao lado: cada escolha
> abaixo já tem uma decisão registrada, e a seção precisa dizer a mesma coisa
> que elas.

***

## 3.1 Natureza e tipo de pesquisa

> **A escrever.** As [diretrizes institucionais](../docs/diretrizes.md) listam
> os tipos possíveis. O nosso é **desenvolvimento de produto ou protótipo**, de
> natureza aplicada. Declare isso com todas as letras — é critério de
> avaliação.
>
> Diga também que o desenho é **comparativo, por estudo de ablação**: não se
> avalia se um detector funciona, e sim **quanto cada dimensão acrescenta** sobre
> uma linha de base.

## 3.2 Ambiente controlado

> **A escrever.** Como os dados são gerados: 250 funcionários, um ano simulado,
> 20 a 50 eventos por dia útil por persona — os parâmetros declarados da
> simulação, conforme a decisão **D-23** e a
> [especificação do banco](../docs/banco-simulado.md).
>
> Deixe explícito que **não há dado de pessoa real** — isso responde à
> exigência de ética em pesquisa das diretrizes. Nenhum número aqui é
> estatística do mundo real: são parâmetros escolhidos, e dizê-lo é honestidade
> metodológica, não fraqueza.
>
> **A separação dos três bancos entra aqui** (`corp`, `ground_truth`, `sdcac`):
> é a trava contra vazamento de rótulo, e a banca pergunta.

## 3.3 Ferramentas e tecnologias

> **A escrever.** Python 3.12, FastAPI, PostgreSQL, Pandas, Streamlit. A
> justificativa de cada escolha importa mais que a lista. Detalhe técnico em
> [padrões de código](../docs/padroes-codigo.md).

## 3.4 As quatro configurações — o desenho de ablação

> **A escrever.** C0, C1, C2 e C3, conforme
> [arquitetura](../docs/arquitetura.md) e a decisão **D-05**. Três coisas
> precisam ficar escritas:
>
> - As quatro são **flags do mesmo código**, não quatro sistemas — é o que
>   garante que a única variável entre as linhas da tabela seja a dimensão
>   acrescentada
> - A **C0 é puramente estática**, sem nenhum histórico do funcionário. Duas das
>   quatro regras originais usavam histórico e contaminavam o grupo de controle
>   (**D-26**, pergunta **P30**)
> - Os mesmos logs, os mesmos cenários e as mesmas sementes nas quatro

## 3.5 As três dimensões e a integração

> **A escrever.** O que cada dimensão pergunta, com que janela e sobre que
> unidade — a tabela da [arquitetura](../docs/arquitetura.md).
>
> Justifique os pesos, não apenas os apresente: por que horário atípico vale 30
> e força bruta vale 40? A banca pergunta, e "foi o que pareceu razoável" não
> sustenta. Declare-os **preliminares**, com a análise de sensibilidade da S12
> (**D-09**).
>
> Duas escolhas de integração precisam aparecer no texto, porque são perguntas
> que a banca faz:
>
> - **O evento atual fica fora da janela de exposição** (**D-18**). Dentro dela,
>   o peso efetivo dele seria `α + γ`, e os pesos deixariam de ser
>   interpretáveis
> - **O baseline da D2 vem de janela anterior e disjunta da de avaliação**
>   (**D-17**). Senão o comportamento anômalo entra na definição do que é normal
>
> E a **D3 reporta duas parcelas separadas** — conduta e postura —, nunca
> somadas num número só (**D-25**).

## 3.6 Cenários de teste

> **A escrever.** As quatro famílias de cenários: pontuais, de contexto,
> longitudinais e de **escalada legítima** (**D-06** e **D-16**). Diga o que
> cada família testa.
>
> A escalada legítima é o **controle negativo**: sem ela, o falso positivo da D3
> fica sem medida — e a D3 é a contribuição original do trabalho. Vale registrar
> o **desenho cego**, se ele acontecer: quem especifica os cenários não vê a
> fórmula da D3.
>
> Eles viram teste automatizado — é o que transforma "o sistema detecta" em "o
> sistema detecta, e aqui está a prova que roda sozinha".

## 3.7 Avaliação de usabilidade

> **A escrever.** Método já definido e com fontes em
> [usabilidade](../docs/usabilidade.md), seção 6: avaliação heurística com
> escala de severidade, teste de tarefa e SUS.

## 3.8 Métricas, unidade de análise e tratamento estatístico

> **A escrever.** Taxa de falsos positivos a revocação fixa e revocação nos
> cenários longitudinais — as duas grandezas da pergunta, pela decisão **D-03**.
> Diga como cada número será obtido.
>
> Três pontos que decidem o que a seção de Resultados poderá afirmar:
>
> - **Unidade de análise declarada** (**D-12**): evento para os cenários
>   pontuais, episódio ou usuário-dia para os de contexto e longitudinais. O
>   mesmo cenário rende revocação 0,15 medido por evento e 1,00 por episódio —
>   misturar as duas grandezas invalida a tabela
> - **Tratamento estatístico** (**D-13**): 10 a 20 sementes, as mesmas nas quatro
>   configurações, com **Wilcoxon pareado** sobre as diferenças. Com menos de 6
>   sementes nenhum resultado seria declarável significativo
> - **Critério de relevância declarado antes de existir número** (**D-15**): uma
>   frase dizendo qual redução de FPR e qual revocação longitudinal contam como
>   resposta afirmativa. Declarar depois é racionalização, não rigor
>
> Se a C0 não alcançar revocação 0,90 em limiar nenhum, a métrica primária não
> existe para o grupo de controle: comparam-se **curvas precisão-revocação**, não
> pontos únicos (**D-14**).

***

## O que esta seção ainda precisa

* [ ] Natureza da pesquisa declarada conforme [diretrizes](../docs/diretrizes.md)
* [ ] Justificativa dos pesos das regras, não só a apresentação
* [ ] Declaração explícita de que não há dado de pessoa real
* [ ] Fórmulas conferidas contra [arquitetura](../docs/arquitetura.md)
* [ ] **D-12 a D-19 fechadas** antes de a seção ser dada por pronta — são as
      oito lacunas metodológicas, e todas mudam o que a S12 conseguirá afirmar
* [ ] Critério de relevância (**D-15**) escrito **antes** de existir resultado
