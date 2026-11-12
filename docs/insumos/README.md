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
| [Cenários, rótulos e desenho cego — v2](cenarios-yasmin-v2.md) | **Yasmin**, rascunho integral por Claude Sonnet 5 | 10/11/2026 | **Nada ainda** — ver a conferência abaixo |
| [Pesos preliminares e sensibilidade](pesos-yasmin-v1.md) | **Yasmin**, rascunho integral por Claude Sonnet 5 | 10/11/2026 | **Nada ainda** — proposta até ela confirmar |
| [LGPD e ISO/IEC 27001](lgpd-iso-yasmin-v1.md) | **Yasmin**, rascunho integral por Claude Sonnet 5 | 10/11/2026 | **Nada ainda** — proposta até ela confirmar |
| [Exemplos reais do problema](exemplos-reais-yasmin-v1.md) | **Yasmin**, rascunho integral por Claude Sonnet 5 | 10/11/2026 | **Nada ainda** — as 4 fontes vão para [citações pendentes](../citacoes-pendentes.md) |

## A entrega de 10/11/2026, e o que a conferência achou

Os quatro insumos acima chegaram num `.zip` em 11/11. **Entraram como recebidos e
não foram editados**, conforme a regra desta pasta — inclusive onde a conferência
discorda deles. A correção mora aqui; o insumo fica como prova do que chegou.

**Três deles declaram, no próprio cabeçalho, "Conferi tudo que a IA escreveu?
**Ainda não**".** Pelo [`AGENTS.md`](../../AGENTS.md) seção 3, isso os torna
**proposta**, não entrega: nenhum fecha a decisão que diz fechar — D-06, D-09,
D-16, D-19 e P18 a P23 continuam abertas até a Yasmin ler e confirmar.

O `exemplos-reais-yasmin-v1.md` declara **"Sim"**. O `README.md` que vinha no
`.zip` dizia o contrário — *"nenhum destes arquivos foi lido e confirmado pela
Yasmin ainda"* —, e as duas afirmações não podem valer juntas. É o campo cuja
honestidade o `AGENTS.md` cobra por nome, e vale a Yasmin dizer qual é a certa.

### O cenário N06 **já existe no código**

O `cenarios-yasmin-v2.md` corrige a v1 com base nesta afirmação:

> *"É um cenário (N06) e uma prevalência que o código ainda não tem… o arquivo
> **nunca** teve um `N06`."*

**Isso não se sustenta.** O `N06_manutencao_noturna_ti` está implementado em
[`generator/normal.py`](../../generator/normal.py), linha 185, desde o #89 — não
em `generator/scenarios.py`, que foi o único arquivo consultado. Ele está lá
porque é atividade **legítima**, e pertence à rotina normal em vez da injeção de
cenários.

Medido no gabarito que o gerador produz:

| Família | Episódios |
|---|---|
| P01 a P06 | 24 |
| B01 a B04 | 16 |
| L01 a L04 | 12 |
| N01 a N05 | 19 |
| **N06** | **53** |
| **N total** | **72** |
| **Total** | **124** |

São exatamente os números que o insumo atribui ao artigo do Drive e nega ao
código. **O código e o artigo já concordam**, e a pendência que o insumo abre
para o Filipe — implementar o N06 — **não existe**.

### Duas outras afirmações do `.zip` que não se confirmam

O `README.md` do pacote dizia que os arquivos *"também ficam versionados em
`TCC_SDCAC/docs/insumos/`"* e que o relatório
`docs/relatorios/2026-11-10-sessao-40.md` estava *"já feito"*. Nenhuma das duas
era verdade em 11/11: os insumos entraram **neste** Pull Request, e aquele
relatório não existe em nenhuma branch do repositório.

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
