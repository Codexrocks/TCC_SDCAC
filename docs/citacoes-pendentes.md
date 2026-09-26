# Citações pendentes

Lista do que ainda precisa de fonte conferida. Uma linha por pendência, com o
lugar exato e o que falta.

Existe por uma razão prática e uma técnica.

**A prática:** modelo de linguagem inventa referência plausível — autor real,
revista real, ano real, artigo que não existe. As
[diretrizes institucionais](diretrizes.md) vedam expressamente *"qualquer forma
de plágio, cópia indevida ou fraude acadêmica"*, e referência fabricada cai
nessa cláusula. Anotar a dívida é o que a mantém visível até alguém pagá-la.

**A técnica:** dentro de `artigo/` não dá para anotar no lugar. O GitBook apaga
comentário HTML ao salvar, e em 06/09/2026 ele exportou os seis arquivos do
artigo com todos os marcadores apagados — a dívida sumiu sem ninguém perceber.
As páginas de `docs/` não têm esse problema, porque o GitBook só lê daqui.

> **Regra:** `FALTA CITAÇÃO` dentro de `artigo/` reprova na validação. A
> pendência do artigo se registra **aqui**.

***

## Pendentes — artigo

| Onde | O que falta | Quem | Desde |
|---|---|---|---|
| `02-referencial-teorico.md` § 2.1 | Fonte para os pilares da segurança da informação — confidencialidade, integridade, disponibilidade | Yasmin | 04/09/2026 |
| `01-introducao.md` § Contextualização | Entrada na lista para `(NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY, 2006)`. A chamada foi entregue ao professor em 24/09 e a `## Lista` de `referencias.md` está vazia. Conferir a fonte antes de acrescentar | Davi | 26/09/2026 |
| `01-introducao.md` § Problema | Entrada na lista para `(CHANDOLA; BANERJEE; KUMAR, 2009)`. Mesma situação da linha acima | Davi | 26/09/2026 |

## Pendentes — documentação

Estas ficam marcadas **na própria linha**, com `<!-- FALTA CITAÇÃO -->`. O
comentário é invisível no site publicado e sobrevive, porque o GitBook não
escreve em `docs/`.

| Onde | O que falta | Desde |
|---|---|---|
| [`usabilidade.md`](usabilidade.md) § 6.2 | Formulação exata e porcentagem de Nielsen e Landauer | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 6.3 | Limites exatos de cada faixa adjetiva do SUS, em Bangor, Kortum e Miller (2009) | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 7 | Literatura de carga de trabalho e fadiga de alerta em analistas de SOC | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 9 | Edição e ano de Shneiderman efetivamente consultados. **Nunca esteve indexado aqui**: o marcador já existia no arquivo e esta linha faltava | 26/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 7 | Edição e ano da obra de Shneiderman efetivamente consultada | 03/09/2026 |

***

## Como usar

**Ao escrever e precisar de uma fonte que você ainda não abriu:** acrescente uma
linha na tabela do artigo. Escreva o capítulo, a seção e o que falta — "falta
citação" sozinho não ajuda ninguém daqui a dois meses.

**Ao conferir a fonte:** apague a linha daqui e acrescente a referência em
[`artigo/referencias.md`](../artigo/referencias.md).

**Nunca:** apagar a linha sem ter aberto a fonte. É o único jeito de esta página
mentir, e ela só serve enquanto for verdadeira.

## Antes de entregar

Esta tabela precisa estar **vazia** — as duas. Página com pendência aberta é
seção que ainda não pode ser entregue.
