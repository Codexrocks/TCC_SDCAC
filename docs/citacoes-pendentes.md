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
| `02-referencial-teorico.md` § 2.1 | **Fonte proposta na entrega de 28/09:** `(INTERNATIONAL ORGANIZATION FOR STANDARDIZATION, 2022)`. A pendência deixa de ser "qual fonte" e passa a ser a confirmação de que ela foi aberta — ver a tabela do referencial, abaixo | Yasmin | 04/09/2026 |
| `01-introducao.md` § Contextualização | Entrada na lista para `(NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY, 2006)`. A chamada foi entregue ao professor em 24/09 e a `## Lista` de `referencias.md` está vazia. Conferir a fonte antes de acrescentar. ⚠️ **Pode ser a mesma obra** que `KENT; SOUPPAYA, 2006` do referencial — a NIST SP 800-92 é de 2006. Se for, a chamada da Introdução precisa mudar para os autores, que é o que a ABNT pede. **Conferir antes de acrescentar qualquer uma das duas** | Davi | 26/09/2026 |
| `01-introducao.md` § Problema | Entrada na lista para `(CHANDOLA; BANERJEE; KUMAR, 2009)`. Mesma situação da linha acima. A mesma obra é citada no referencial, § 2.4 — uma confirmação resolve as duas | Davi | 26/09/2026 |

### As 13 do referencial teórico

O [insumo entregue pela Yasmin](insumos/referencial-teorico-yasmin-v2.md) em
28/09 traz as 13 referências já formatadas, e declara que **nenhuma foi
descartada por dúvida quanto à existência da fonte**. Não declara que cada uma
foi aberta — e é isso que
[`artigo/referencias.md`](../artigo/referencias.md) exige para aceitar a entrada.

**A pendência é de confirmação, não de busca.** Ao confirmar, apague a linha e
acrescente a referência em ABNT NBR 6023 na `## Lista`.

| Chamada, como está no texto | Onde | Quem | Desde |
|---|---|---|---|
| `(AXELSSON, 2000)` | § 2.4 | Yasmin | 28/09/2026 |
| `Cappelli, Moore e Trzeciak (2012)` | § 2.3 | Yasmin | 28/09/2026 |
| `Chandola, Banerjee e Kumar (2009)` | § 2.4 | Yasmin | 28/09/2026 |
| `Denning (1987)` | § 2.4 | Yasmin | 28/09/2026 |
| `(GONZALEZ-GRANADILLO; GONZALEZ-ZARZOSA; DIAZ, 2021)` | § 2.2 | Yasmin | 28/09/2026 |
| `(GRASSI et al., 2017)` | § 2.1 | Yasmin | 28/09/2026 |
| `Homoliak et al. (2019)` | § 2.3 | Yasmin | 28/09/2026 |
| `(INTERNATIONAL ORGANIZATION FOR STANDARDIZATION, 2022)` | § 2.1 | Yasmin | 28/09/2026 |
| `(KENT; SOUPPAYA, 2006)` | § 2.1 | Yasmin | 28/09/2026 |
| `(SANDHU et al., 1996)` | § 2.1 | Yasmin | 28/09/2026 |
| `(SHASHANKA; SHEN; WAN, 2016)` | § 2.3 | Yasmin | 28/09/2026 |
| `(SUNDARAMURTHY et al., 2015)` | § 2.4 | Yasmin | 28/09/2026 |
| `Vielberth et al. (2020)` | § 2.2 | Yasmin | 28/09/2026 |

### As 7 da metodologia

Situação diferente, e mais exigente. O
[insumo entregue pelo Davi](insumos/metodologia-davi-v1.md) em 28/09 declara, no
próprio cabeçalho, que a redação foi **rascunhada por IA** e que **nenhuma das
sete citações foi conferida na fonte**.

> O [`AGENTS.md`](../AGENTS.md), seção 3, é categórico: *"referência
> bibliográfica que a IA produziu e ninguém conferiu na fonte"* está entre o que
> **nunca é aceitável**. Por isso as sete estão aqui, e não em
> [`referencias.md`](../artigo/referencias.md) — e o capítulo avisa disso no
> cabeçalho, à vista de quem for escrever.

Ao conferir, apague a linha e acrescente a referência em ABNT NBR 6023 na
`## Lista`.

| Chamada, como está no texto | Onde | O que sustenta | Quem | Desde |
|---|---|---|---|---|
| `(WOHLIN et al., 2012)` ⚠️ | § 3.8 | A taxonomia das quatro categorias de validade. **O ano está marcado como duvidoso pelo próprio insumo** — pode ser outra edição | Davi | 28/09/2026 |
| `(DEMŠAR, 2006)` | § 3.7 | A escolha do Wilcoxon pareado para comparar configurações | Davi | 28/09/2026 |
| `(WILCOXON, 1945)` | § 3.7 | O teste em si | Davi | 28/09/2026 |
| `(DAVIS; GOADRICH, 2006)` | § 3.6 | Curva PR sobre ROC em classe desbalanceada | Davi | 28/09/2026 |
| `(SAITO; REHMSMEIER, 2015)` | § 3.6 | O mesmo ponto da linha acima | Davi | 28/09/2026 |
| `(KAUFMAN et al., 2012)` | § 3.8 | Vazamento na constituição do padrão individual | Davi | 28/09/2026 |
| `(SOMMER; PAXSON, 2010)` | § 3.8 | Limite das avaliações sobre dado sintético | Davi | 28/09/2026 |

> **A `SOMMER; PAXSON, 2010` já era conhecida do repositório:** ela aparece no
> [plano](plano.md), seção 4, como apoio ao risco de dados sintéticos fáceis
> demais, e o insumo da Yasmin a descartou do referencial por já estar citada
> ali. **Uma conferência resolve os dois usos.**

## Pendentes — documentação

Estas ficam marcadas **na própria linha**, com `<!-- FALTA CITAÇÃO -->`. O
comentário é invisível no site publicado e sobrevive, porque o GitBook não
escreve em `docs/`.

| Onde | O que falta | Quem | Desde |
|---|---|---|---|
| [`usabilidade.md`](usabilidade.md) § 6.2 | Formulação exata e porcentagem de Nielsen e Landauer | Filipe | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 6.3 | Limites exatos de cada faixa adjetiva do SUS, em Bangor, Kortum e Miller (2009) | Filipe | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 7 | Literatura de carga de trabalho e fadiga de alerta em analistas de SOC | Yasmin | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 9 | Edição e ano da obra de Shneiderman efetivamente consultada | Filipe | 03/09/2026 |

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
