# 3. Metodologia

> **3ª Versão** na numeração do professor · S5 do
> [cronograma](../docs/cronograma.md) · Todos.

---

## 3.1 Natureza e tipo de pesquisa

<!-- As diretrizes institucionais (../docs/diretrizes.md) listam os tipos possíveis.
     O nosso é DESENVOLVIMENTO DE PRODUTO OU PROTÓTIPO, de natureza aplicada.
     Declare isso com todas as letras — é critério de avaliação. -->

## 3.2 Ambiente controlado

<!-- Como os dados são gerados: usuários simulados, massa de eventos normais e
     anômalos. Deixe explícito que não há dado de pessoa real — isso responde à
     exigência de ética em pesquisa das diretrizes. -->

## 3.3 Ferramentas e tecnologias

<!-- Python 3.12, FastAPI, PostgreSQL, Pandas, Streamlit. A justificativa de
     cada escolha importa mais que a lista. Detalhe técnico em
     ../docs/padroes-codigo.md. -->

## 3.4 Modelagem das regras de detecção

<!-- As quatro regras e seus pesos, conforme ../docs/arquitetura.md.

     Aqui é preciso JUSTIFICAR os pesos, não apenas apresentá-los: por que
     horário atípico vale 30 e força bruta vale 40? A banca pergunta, e "foi o
     que pareceu razoável" não sustenta. -->

## 3.5 Cálculo do Risk Score

<!-- Soma cumulativa, teto de 100, e as quatro faixas de severidade. -->

## 3.6 Cenários de teste

<!-- Os seis cenários de ../docs/arquitetura.md, com o score esperado de cada um.
     Eles viram teste automatizado — é o que transforma "o sistema detecta" em
     "o sistema detecta, e aqui está a prova que roda sozinha". -->

## 3.7 Avaliação de usabilidade

<!-- Método já definido e com fontes em ../docs/usabilidade.md, seção 6: avaliação
     heurística com escala de severidade, teste de tarefa e SUS. -->

## 3.8 Métricas de avaliação

<!-- Taxa de detecção (recall), taxa de falsos positivos e MTTD, com as fórmulas
     de ../docs/arquitetura.md. Diga como cada número será obtido. -->

---

## O que esta seção ainda precisa

- [ ] Natureza da pesquisa declarada conforme `../docs/diretrizes.md`
- [ ] Justificativa dos pesos das regras, não só a apresentação
- [ ] Declaração explícita de que não há dado de pessoa real
- [ ] Fórmulas conferidas contra `../docs/arquitetura.md`
