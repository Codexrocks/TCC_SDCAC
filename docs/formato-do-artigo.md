# Formato do artigo

> **O artigo do TCC sai no template COBEM 2026, com as referências em ABNT.**
> Consta duas vezes nas
> [orientações do professor](../templates/orientacoes-tcc-reuniao-02.pdf),
> apresentadas na 2ª reunião. Decisão [D-11](decisoes.md).

## ✅ O template do professor chegou em 18/11/2026 — e é o COBEM 2025

O Davi entregou o arquivo que o professor distribui, sob o nome *Modelo Formato
COBEM*, versionado em
[`templates/COBEM-2026-modelo-do-professor.docx`](../templates/README.md).

**No conteúdo, ele é o mesmo COBEM 2025 que a equipe já tinha** — 106
parágrafos, 3 tabelas e 14.036 caracteres, com **zero linhas de diferença** na
comparação. O cabeçalho do próprio arquivo diz `COB-2025-XXXX` e *"28th
COBEM"*.

**Nada no artigo precisa mudar:** ele foi escrito contra estas regras desde
setembro, e o documento montado cumpre A4, margens 3/2/2/2, Times New Roman 10
e entrelinha simples — conferido no `.docx` em 18/11/2026.

> O texto abaixo foi escrito quando o arquivo ainda não existia no
> repositório. Fica como estava, porque descreve de onde as regras vieram:
> esta
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
| **Artigo completo** | **Mínimo 8, máximo 12 páginas** — confirmado pelo Davi em 12/11/2026 |
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
| O template do professor | **versionado desde 18/11/2026**, e silencioso sobre a forma da chamada |

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

> **O template do COBEM 2025 diz 6 a 10 páginas**, e o do CREEM 2026 também traz
> número próprio. **Vale o do professor**: 8 a 12. Se o template de 2026 chegar
> com outro número, é ele que muda o documento — e o artigo fecha hoje em 12.

### Tabelas e figuras

Exigência que o professor apontou **por escrito, em 12/11/2026**, ao comentar a
entrega da Seção de Resultados:

> *"as tabelas e figuras devem possuir legenda com a respectiva fonte
> indicada."*

O que o artigo passou a fazer, e o montador passou a conferir:

| | |
|---|---|
| **Legenda** | **Acima** da tabela, centralizada, no formato `Tabela N. Texto.` — é a forma do template da família ABCM |
| **Fonte** | **Abaixo**, centralizada, em corpo 9: `Fonte: dados da pesquisa (2026).` para o que o experimento mediu, `Fonte: elaborada pelos autores (2026).` para o que a equipe definiu |
| **Numeração** | **Contínua no documento inteiro**, e não por seção. A Tabela 1 está na Metodologia; as cinco seguintes, nos Resultados |
| **Chamada no texto** | Pelo número — `Tab. 4` no meio da frase, `Tabela 4` no começo. O template exige, e nenhuma tabela era chamada assim antes de 12/11 |
| **Título de seção** | À esquerda, **em negrito**, Times 10, numerado com arábicos separados por ponto, **no máximo três níveis**. **Sem caixa alta** — o template não a pede, e ela saiu em 12/11/2026 |
| **E-mail dos autores** | Em corpo 9, abaixo do nome. Mora fora do versionamento, em `artigo/emails.local.json` — o repositório é público |

> **Isto é verificação, não lembrete.** `scripts/montar_artigo.py` **não monta o
> documento** se uma tabela estiver sem legenda, sem fonte ou com a numeração
> fora de sequência. Lembrete escrito não reprova nada — e esta exigência já
> custou uma volta de entrega.

**Figura o artigo não tem** — nenhuma das cinco seções usa imagem. A regra fica
escrita porque a primeira que entrar vai precisar dela, e o montador já aceita
`Figura N.` na mesma forma.

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

- [x] ~~**Obter o template COBEM 2026 com o professor**~~ — entregue pelo Davi
      em **18/11/2026** e versionado em `templates/`. É o COBEM 2025 no
      conteúdo, e o artigo já o cumpre
- [x] ~~**Decidir a forma da chamada no texto** quando o template chegar~~ —
      resolvida em 18/11/2026, **a favor do que já estava escrito**. O template
      prescreve a chamada por sobrenome e ano: *"Recent work (Choma and Ugaya,
      2017)..."*, *"Recently, Choma and Ugaya (2017)..."*, e
      *"(Porto-Hernandez et al., 2023)"* para três ou mais autores. **É a forma
      que o artigo usa** — `(Wohlin et al., 2012)`, `Axelsson (2000)`,
      `(Sommer e Paxson, 2010)` —, com "e" no lugar de "and" porque o texto é
      em português. Nada a converter
      · ⚠️ **não converter as três citações da Introdução antes disso** — ver a
      seção de referências acima
- [ ] Combinar a divisão de páginas por seção dentro de 8 a 12, no
      [`artigo/README.md`](../artigo/README.md) · **os três**
- [ ] Conferir se as referências do contexto da Introdução têm **até 5 anos** ·
      **Yasmin** · antes de 24/09
- [ ] Acrescentar ao artigo as seções de fechamento que o template exigir ·
      **Davi** · quando o arquivo chegar
