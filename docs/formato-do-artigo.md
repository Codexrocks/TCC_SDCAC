# Formato do artigo

> **O artigo do TCC sai no formato CREEM 2026, com as referências em ABNT.**
> Confirmado pelo professor em 23/09/2026, que disponibilizou o template. Ver
> decisão [D-11](decisoes.md).

Tudo nesta página foi **lido do template oficial em Word**, entregue pelo
professor e versionado em
[`templates/`](../templates/README.md). É o **XXXII CREEM 2026** — Congresso
Nacional de Estudantes de Engenharia Mecânica.

> **Use o arquivo para diagramar; use esta página para saber o que ele exige.**
> Ele está na raiz, e não em `artigo/`, porque o GitBook escreve naquela pasta —
> o motivo está em [`templates/README.md`](../templates/README.md).

## A regra de convivência entre os dois padrões

| O quê | Segue |
|---|---|
| **A lista de referências**, no fim do artigo | **ABNT** |
| **Todo o resto** — layout, margens, fonte, seções, figuras, tabelas, equações e as **chamadas de citação dentro do texto** | **Template CREEM 2026** |

Confirmado pelo professor em 23/09/2026. A distinção importa porque a ABNT tem
duas normas aqui, e só uma vale: a **NBR 6023** rege a lista; a **NBR 10520**
rege a chamada no texto, e **essa não se aplica**.

```
Chamada no texto — CREEM:   (Chang e Pakzad, 2013)
                            Chang e Pakzad (2013) demonstram que ...
NÃO use a forma ABNT:       (CHANG; PAKZAD, 2013)

Lista no fim — ABNT NBR 6023:
CHANG, M.; PAKZAD, S. N. Modified natural excitation technique for stochastic
modal identification. **Journal of Structural Engineering**, v. 139, n. 10, 2013.
```

***

## O que o template exige

### Página e texto

| Item | Valor |
|---|---|
| Papel | A4 |
| Margem superior | **3 cm** |
| Margens esquerda, direita e inferior | **2 cm** |
| Fonte do corpo | **Times New Roman 10** — exceto o título |
| Entrelinha | Simples, em todo o texto |
| Alinhamento | Justificado |
| Recuo da primeira linha | **0,5 cm** |
| Número de página | **Não numerar.** O template é enfático: *"NÃO NUMERAR AS PÁGINAS."* |
| Notas de rodapé | Evitar |
| Extensão | **Mínimo 8, máximo 12 páginas**, incluindo tabelas e figuras |
| Arquivo final | PDF de **no máximo 4 MB** |

> O texto do template **não diz** o tamanho de fonte do título nem dos nomes dos
> autores — apenas que o corpo é TNR 10 "exceto para o título". Diagrame pelo
> arquivo `.docx`, que já traz os estilos prontos.

O bloco de **nomes dos autores, instituição, endereço, resumo e palavras-chave**
leva recuo de **0,1 cm** da margem esquerda e é marcado por uma **linha preta de
2¼ pt** na borda esquerda.

### Resumo e palavras-chave

**De 200 a 300 palavras, em um único parágrafo.** Sem fórmulas e sem
referências bibliográficas. Deve descrever: objetivos, contexto, importância,
métodos, resultados e principais conclusões.

Palavras-chave: **até 5**, separadas por vírgula.

### Seções

| Nível | Forma | Exemplo |
|---|---|---|
| Título de seção | **TODAS MAIÚSCULAS** | `MODELO MATEMÁTICO` |
| Subtítulo | **Primeiras Letras Maiúsculas** | `Modelo Matemático` |

Numerados com algarismos arábicos separados por pontos, **até 3 subníveis**. Uma
linha em branco de espaçamento simples acima e abaixo de cada título.

> O esqueleto do [Referencial Teórico](../artigo/02-referencial-teorico.md) usa
> `2.1` a `2.7`, que cabe. Não desça para `2.1.1.1`.

**O template não prescreve quais seções de conteúdo o artigo tem** — é um guia
de formatação. A estrutura de cinco seções definida pela instituição cabe sem
ajuste.

### Equações

Alinhadas à esquerda com recuo de **0,5 cm**. Número em algarismo arábico entre
parênteses, alinhado à direita. Símbolos matemáticos em itálico; unidades em
romano (`kg`, `m`, `kW/m²`). Todas as grandezas no Sistema Internacional.

No texto: **`Eq. (1)`** no meio da frase, **`Equação (1)`** no começo. Os
símbolos são definidos imediatamente antes ou depois da primeira ocorrência.

### Figuras e tabelas

* Colocadas o mais perto possível da primeira menção no texto
* Numeradas consecutivamente em algarismos arábicos
* **Tabelas centralizadas**, com a legenda **acima**; explicações ao pé da
  tabela, nunca dentro dela. Unidades só na primeira linha ou primeira coluna
* **Figuras centralizadas**, com a legenda **abaixo**, também centralizada
* Uma linha em branco, espaçamento simples, entre a figura ou tabela e o texto
  seguinte
* Salvar em **GIF** (até 16 cores) ou **JPEG** (alta densidade de cores) antes
  de inserir
* No texto: **`Tab. 1`** / **`Figura 1`** no meio da frase; **`Tabela 1`** /
  **`Figura 1`** no começo

### As três seções de fechamento

Na ordem, no fim do artigo:

| Seção | Obrigatória? | Conteúdo |
|---|---|---|
| **AGRADECIMENTOS** | Opcional | Se houver, vem antes das referências |
| **REFERÊNCIAS** | **Sim** | Ordem alfabética pelo sobrenome do primeiro autor. Primeira linha alinhada à esquerda, as demais com recuo. **Toda referência da lista aparece no texto, e vice-versa** |
| **RESPONSABILIDADE AUTORAL** | **Sim** | Texto fixo, adaptado ao número de autores |

O texto da última, em português:

> *O(s) autor(es) é(são) o(s) único(s) responsável(is) pelo conteúdo deste
> trabalho.*

### O bloco em inglês vai no fim

Como o artigo é em português, o template exige repetir **depois da lista de
referências**, no fim do documento:

* Título
* Nomes dos autores e afiliações
* *Abstract* — as mesmas 200 a 300 palavras, um parágrafo
* *Keywords*

> **Isto mudou.** A versão anterior desta página dizia que o abstract ficava ao
> lado do Resumo, no alto. No CREEM ele vai **no fim**, depois das referências.

***

## O que isto muda no artigo

### 1. Oito a doze páginas — e oito é o piso

A versão anterior desta página trabalhava com 6 a 10 páginas. O CREEM pede
**mínimo 8**. O artigo precisa ser **maior** do que estava planejado, não menor.

Orçamento sugerido para um artigo de 10 páginas — números de orientação, não
regra, mas a soma é o que existe:

| Seção | Páginas |
|---|---|
| Cabeçalho, resumo e palavras-chave | 0,5 |
| Introdução | 1 a 1,5 |
| Referencial teórico | 2 a 2,5 |
| Metodologia | 2 a 2,5 |
| Resultados e discussão | 2,5 a 3 |
| Conclusão | 0,5 |
| Referências, responsabilidade autoral e bloco em inglês | 1 |

### 2. A lista de referências é ABNT — e já está certa

O [`referencias.md`](../artigo/referencias.md) **não precisa ser refeito.** Os
modelos que ele traz já são ABNT, que é o que o professor confirmou. O que falta
ali é preencher a lista, não reformatá-la.

> A versão anterior desta página mandava refazer o arquivo em autor-ano. Essa
> tarefa **caiu**.

### 3. Chamadas no texto seguem o CREEM, não a ABNT

É a armadilha mais fácil de cair, porque as duas formas são parecidas. Ver a
tabela de convivência no alto desta página.

### 4. O idioma: português, com o bloco em inglês no fim

O artigo inteiro sai em português. O template admite isso explicitamente: a
língua oficial do congresso é o português, e quem escreve em português repete
título, autores, resumo e palavras-chave em inglês no fim.

| Elemento | Idioma | Onde |
|---|---|---|
| Título, autores e afiliação | Português | Alto |
| **Resumo** e **Palavras-chave** | Português | Alto |
| Corpo, da Introdução às Conclusões | Português | — |
| Referências | Como cada obra foi publicada | Fim |
| Título, autores, ***Abstract*** e ***Keywords*** | **Inglês** | **Depois das referências** |

> **O que não muda:** o Markdown de `artigo/` continua sendo a fonte da verdade
> do texto. O template é formatação, e formatação é o último passo. Texto preso
> dentro de um `.docx` não é revisável por ninguém e não aparece no histórico.

***

## Histórico deste arquivo

Três voltas na mesma questão. Vale conhecer, porque a banca pode perguntar por
que o formato mudou, e a resposta — *a fonte de autoridade se pronunciou depois*
— só se sustenta com o registro.

| Data | O que ficou | Fonte |
|---|---|---|
| 04/09/2026 | ABNT | Registro da equipe |
| 07/09/2026 | COBEM 2025 — *"não é ABNT"* | Template encontrado pela equipe |
| **23/09/2026** | **CREEM 2026, com referências em ABNT** | **Template do professor** |

Uma correção anterior continua valendo como lição: a primeiríssima versão desta
página foi montada a partir de páginas de eventos e de templates de CREEM 2022 e
CONEM 2020, com números que se provaram errados. **Fonte parecida não é a mesma
fonte** — e é por isso que esta versão só afirma o que está no arquivo entregue.

## Sobre o COBEM 2027 — outro evento

Informação levantada quando se supunha que o formato era COBEM. Fica registrada
porque continua verdadeira sobre aquele congresso, **mas não é o formato deste
trabalho**.

O 51º COBEM acontece em Campinas/SP, de 06 a 10 de dezembro de 2027. A janela de
resumos abre em **06/12/2026** — dentro da S15 do [cronograma](cronograma.md) —
e a primeira etapa não exige arquivo, só título, resumo e palavras-chave no
formulário. Submeter é possibilidade, não obrigação; e o template daquela edição
será outro.

***

## O que ainda precisa ser decidido

- [x] **Idioma**, definido em 07/09/2026: artigo em português, *abstract* e
      *keywords* em inglês
- [x] **Formato**, definido em 23/09/2026: CREEM 2026, referências em ABNT
- [ ] **Combinar a divisão de páginas por seção** com a equipe, agora dentro da
      faixa de 8 a 12 · **equipe**
- [ ] **Acrescentar as seções de fechamento** ao esqueleto do artigo —
      AGRADECIMENTOS, REFERÊNCIAS, RESPONSABILIDADE AUTORAL e o bloco em inglês ·
      **Davi**
- [ ] **Converter os títulos de seção para MAIÚSCULAS** na hora de diagramar ·
      **quem montar o documento**
- [ ] **Converter as chamadas de citação já escritas** na
      [Introdução](../artigo/01-introducao.md) · **Davi** · antes da revisão

> **As citações da Introdução estão no formato errado.** O texto já escrito usa
> a forma da NBR 10520, que é a que **não** se aplica:
>
> | Está assim | Deveria ser |
> |---|---|
> | `(NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY, 2006)` | `(NIST, 2006)` |
> | `(CHANDOLA; BANERJEE; KUMAR, 2009)` | `(Chandola et al., 2009)` |
> | `Chandola, Banerjee e Kumar (2009)` | `Chandola et al. (2009)` |
>
> Não corrigi no texto: a Introdução está sendo escrita pela equipe no GitBook, e
> mexer na prosa de quem está redigindo gera conflito. A **lista** em
> [`referencias.md`](../artigo/referencias.md), essa sim, fica em ABNT.
