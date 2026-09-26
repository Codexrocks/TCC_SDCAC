# Formato do artigo

> **O artigo do TCC sai no template COBEM 2026, com as referências em ABNT.**
> Consta duas vezes nas
> [orientações do professor](../templates/orientacoes-tcc-reuniao-02.pdf),
> apresentadas na 2ª reunião. Decisão [D-11](decisoes.md).

## ⚠️ O template do COBEM 2026 ainda não está no repositório

O que está versionado em [`templates/`](../templates/README.md) é o **COBEM
2025** e o **CREEM 2026** — nenhum dos dois é o arquivo que o professor pede.

As orientações dizem: *"O Artigo deve ser produzido e entregue no template
fornecido."* Enquanto o arquivo do COBEM 2026 não for obtido e versionado, esta
página descreve **o que o professor exige**, que é verificável, e sinaliza o que
depende do template.

| Fonte | O que dá |
|---|---|
| Orientações do professor | Extensão, estrutura, limites da Introdução, prazos — **tudo abaixo** |
| Template COBEM 2026 | Margens, fontes, estilos, blocos de abertura e fechamento — **falta** |
| `COBEM-2025-template.docx` | Aproximação da família, útil para diagramar enquanto o de 2026 não chega |

***

## O que o professor exige

### Extensão

| Item | Valor |
|---|---|
| **Artigo completo** | **Mínimo 8, máximo 12 páginas** |
| **Introdução** | **Mínimo 1, máximo 2 páginas** |

> **A Introdução não leva figura, gráfico nem tabela.** É exigência explícita das
> orientações.

### Estrutura

Cinco seções, nesta ordem:

1. Introdução
2. Referencial Teórico
3. Metodologia
4. Resultados e Discussão
5. **Conclusão e Referências**

> A quinta junta Conclusão e Referências. O esqueleto em `artigo/` tem
> `05-conclusao.md` e `referencias.md` separados — isso é organização de escrita,
> e os dois viram uma seção só na diagramação.

### Como a Introdução deve ser montada

As orientações descrevem três elementos, nesta ordem:

| Elemento | O que é |
|---|---|
| **1. Cenário (contexto)** | Apresenta o tema, o que já foi pesquisado e **quais são as lacunas**. Objetivo, sempre citando referências |
| **2. Justificativa** | Por que o artigo é relevante, qual a contribuição para o avanço do conhecimento, quais as implicações práticas |
| **3. Objetivo** | **É onde o problema de pesquisa é declarado.** A lacuna que se busca resolver, a hipótese, e como ela será testada — destacando o método |

Duas exigências que decidem se a seção é aceita:

- **As referências do contexto têm de ser atuais: publicação de até 5 anos.**
  Fontes mais antigas continuam válidas em outras partes do artigo, mas o
  contexto precisa mostrar o estado atual
- **O objetivo é específico e mensurável por resultados práticos.** Não basta
  "desenvolver um modelo": precisa dizer o que será medido

> Isto conversa diretamente com a [pergunta de pesquisa](plano.md), que declara
> a direção — reduzir a taxa de falsos positivos a uma mesma revocação e
> aumentar a revocação longitudinal. São duas grandezas mensuráveis, que é o que
> as orientações pedem.

### Referências: ABNT

**A lista bibliográfica segue a ABNT NBR 6023.** Confirmado pelo professor.
Vale só para a lista; o restante do documento segue o template COBEM.

```
CHANG, M.; PAKZAD, S. N. Modified natural excitation technique for stochastic
modal identification. Journal of Structural Engineering, v. 139, n. 10, 2013.
```

#### E a chamada dentro do texto? **Não converta nada até o template chegar**

A Introdução já escrita usa a forma da **NBR 10520** — `(CHANDOLA; BANERJEE;
KUMAR, 2009)`, caixa alta e ponto e vírgula. Enquanto se supunha que o formato
era CREEM, a orientação aqui era converter para `(Chandola et al., 2009)`.
**Essa orientação caiu, e converter agora seria andar para trás.**

| | |
|---|---|
| O professor disse | "As referências seguem a **ABNT**" |
| A NBR 10520 é | **a norma ABNT da chamada no texto** |
| O template COBEM 2026 | **não está no repositório** |

Ou seja: a forma que está escrita é **consistente com a ABNT**, que é a única
instrução escrita que existe sobre referências. A forma autor-ano em caixa
normal é o costume da família ABCM — costume, não instrução que alguém tenha
dado a este trabalho.

**Para a entrega de 24/09:** deixe como está. Texto internamente consistente com
a ABNT é defensável; texto convertido para uma forma que ninguém pediu, e que não
casa com a lista, não é.

**Quando o template chegar:** se ele exigir autor-ano em caixa normal, a conversão
é mecânica e vale para o artigo inteiro de uma vez — não para três citações
isoladas na véspera de uma entrega.

### Entrega final

| Item | |
|---|---|
| Apresentação | Obrigatória |
| Texto | 8 a 12 páginas |
| **Simulação funcionando** | **Diferencial e opcional** |

> A simulação como diferencial opcional muda a leitura do protótipo: ele não é
> requisito de aprovação, e sim o que distingue o trabalho. O que **é** requisito
> são as 8 a 12 páginas com resultados concretos.

### Outras exigências

- Trabalho **em grupo**, conforme as diretrizes da instituição — de 3 a 8 componentes
- **Caráter prático, com resultados concretos**
- **Trabalho plagiado é considerado nulo**

***

## Prazos

Ficam no [cronograma](cronograma.md), e só lá — inclusive os do professor, que
esta página leu do PDF e passou para lá. Duas tabelas de prazo em dois arquivos
viram duas datas diferentes na primeira vez que uma for atualizada sozinha.

O que vale saber aqui: a **Tarefa 02 é a Introdução no template COBEM 2026**.

***

## Histórico deste arquivo

Quatro voltas na mesma questão. Ficam à vista porque a banca pode perguntar por
que o formato mudou, e a resposta honesta — *a fonte de autoridade foi lida
errada, e depois lida certo* — só se sustenta com o registro.

| Data | O que ficou | Fonte |
|---|---|---|
| 04/09 | ABNT | Registro da equipe |
| 07/09 | COBEM 2025 | Template encontrado pela equipe |
| 23/09 | CREEM 2026, com referências em ABNT | Template entregue como sendo o do professor |
| **23/09** | **COBEM 2026, com referências em ABNT** | **Orientações do professor, 2ª reunião** |

**A terceira volta foi engano de arquivo.** O `.docx` tratado como "o formato do
professor" era do CREEM 2026 — evento irmão da ABCM, template de mesma família,
números parecidos e nome diferente. As orientações escritas dizem COBEM 2026,
duas vezes.

O que sobreviveu daquela volta, porque coincide com o que o professor exige: a
extensão de **8 a 12 páginas**. O que caiu: o nome do evento e tudo que dependia
do arquivo errado.

> **A lição que fica, e já tinha aparecido antes:** a primeira versão desta
> página foi montada a partir de CREEM 2022 e CONEM 2020 e estava errada; a
> terceira foi montada a partir do CREEM 2026 e estava errada de novo. **Fonte
> parecida não é a mesma fonte** — e desta vez a checagem que faltou foi
> confrontar o arquivo com o que o professor escreveu.

> **Se houver uma quinta volta:** acrescente a linha na tabela e reescreva o
> corpo lendo a fonte nova. A tabela guarda o histórico; o corpo descreve só o
> que vale hoje.

***

## O que ainda precisa ser feito

- [ ] **Obter o template COBEM 2026 com o professor** e versionar em
      `templates/` · **Davi** · antes da diagramação
- [ ] **Decidir a forma da chamada no texto** quando o template chegar, e
      converter o artigo inteiro de uma vez se for o caso · **Davi**
      · ⚠️ **não converter as três citações da Introdução antes disso** — ver a
      seção de referências acima
- [ ] Combinar a divisão de páginas por seção dentro de 8 a 12, no
      [`artigo/README.md`](../artigo/README.md) · **os três**
- [ ] Conferir se as referências do contexto da Introdução têm **até 5 anos** ·
      **Yasmin** · antes de 24/09
- [ ] Acrescentar ao artigo as seções de fechamento que o template exigir ·
      **Davi** · quando o arquivo chegar
