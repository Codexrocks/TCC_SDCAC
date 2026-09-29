# Insumos das encomendas

Material **produzido fora do GitHub** e versionado aqui como recebido. Cada
arquivo desta pasta é a entrega de uma pessoa, com data e autoria declaradas.

A pasta existe pela decisão **[D-22](../decisoes.md)**, de 07/09/2026: insumo
vai em `docs/insumos/`, **nunca** em `artigo/insumos/`. O motivo é mecânico — o
GitBook **escreve** em `artigo/` e normaliza o Markdown ao salvar; em `docs/`
ele só lê. Foi assim que os comentários dos seis capítulos sumiram em 06/09.

## Por que guardar o insumo, se o texto já entrou no artigo

Porque são coisas diferentes, e a banca pode perguntar pelas duas.

| | O insumo, aqui | O capítulo, em `artigo/` |
|---|---|---|
| O que é | O que a pessoa entregou, como entregou | O texto que vai para o artigo |
| Muda? | **Não.** É registro | Sim, a cada revisão |
| Serve para | Provar o que foi de quem, e conferir o que a edição mudou | Ser lido pela banca |

Desde 23/09/2026 só o Davi opera o GitHub: Yasmin e Filipe produzem fora e ele
versiona por Pull Request — ver
[cronograma](../cronograma.md#como-o-trabalho-chega-ao-repositório). **A autoria
não muda por causa do caminho.** Esta pasta é o que torna isso verificável em vez
de afirmado.

## O que está aqui

| Insumo | Quem produziu | Entregue | Onde foi usado |
|---|---|---|---|
| [Referencial teórico — versão enxuta](referencial-teorico-yasmin-v2.md) | **Yasmin** | 28/09/2026 | [`artigo/02-referencial-teorico.md`](../../artigo/02-referencial-teorico.md) |
| [Metodologia — 1º rascunho](metodologia-davi-v1.md) | **Davi**, com rascunho assistido por IA | 28/09/2026 | [`artigo/03-metodologia.md`](../../artigo/03-metodologia.md) |

## Ao acrescentar um insumo

1. Grave o arquivo **como recebido**, com um cabeçalho de procedência por cima:
   quem produziu, quando entregou, o que foi feito com ele e o que foi mudado
   ao levá-lo para o artigo
2. Acrescente a linha na tabela acima
3. Acrescente a página ao [`docs/SUMMARY.md`](../SUMMARY.md) — exigência da D-22
   e da regra 3 do [`AGENTS.md`](../../AGENTS.md)
4. **Não edite o insumo depois.** Correção de conteúdo entra no capítulo do
   artigo; o insumo fica como prova do que chegou
5. No Pull Request, a seção **Uso de IA** responde pela IA de **quem produziu**,
   não pela de quem versionou. Não declarado? Escreva exatamente isso
