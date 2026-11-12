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
| [Auditoria das citações pendentes](auditoria-citacoes-ia-v1.md) | **Uma IA**, integralmente | 12/11/2026 | **Material de conferência** — não fecha pendência nenhuma |

## A entrega de 10/11/2026, e o que a conferência achou

Os quatro insumos acima chegaram num `.zip` em 11/11. **Entraram como recebidos e
não foram editados**, conforme a regra desta pasta — inclusive onde a conferência
discorda deles. A correção mora aqui; o insumo fica como prova do que chegou.

**Três deles declaravam, no próprio cabeçalho, "Conferi tudo que a IA escreveu?
**Ainda não**".** Pelo [`AGENTS.md`](../../AGENTS.md) seção 3, isso os tornava
**proposta**, não entrega.

> ✅ **A Yasmin leu e confirmou os quatro, em 12/11/2026** — relatado pelo Davi.
> Os arquivos **não foram editados**, porque a regra desta pasta é que insumo não
> se altera depois de entregue; a confirmação mora aqui, com data e com quem a
> trouxe.
>
> **O que isso fecha:** a **D-06** e a **D-16**, que são o desenho dos cenários, e
> a **D-19**, que é o recorte de LGPD e ISO. A metade dela da **D-43** também está
> ratificada; falta a do Davi.
>
> **O que isso não fecha, e por dois motivos diferentes:**
>
> 1. **A D-09 continua aberta**, e não por falta de leitura: o que ela confirmou
>    **contradiz o código** em dois atributos da D1, como a seção abaixo mostra.
>    Fechar a decisão agora registraria no quadro uma escolha que o sistema não
>    implementa. Ela fecha quando a contradição for resolvida — por qualquer um
>    dos dois lados
> 2. **As quatro fontes dos exemplos reais continuam em
>    [citações pendentes](../citacoes-pendentes.md).** Confirmar um insumo e
>    conferir uma fonte são atos diferentes: o primeiro diz "este texto é meu", o
>    segundo diz "abri a obra e ela sustenta o que o texto afirma". O
>    `AGENTS.md` seção 3 cobra o segundo por nome
>
> **E uma afirmação do insumo dos cenários continua errada depois de confirmada:**
> a de que o código "nunca teve um N06". A confirmação a torna *dela*, não a torna
> *verdadeira* — o N06 está medido, em duas escalas, na seção abaixo. O que a
> confirmação fecha é o desenho dos cenários; o que ela não pode fechar é um fato
> sobre o código.

O `exemplos-reais-yasmin-v1.md` declara **"Sim"**. O `README.md` que vinha no
`.zip` dizia o contrário — *"nenhum destes arquivos foi lido e confirmado pela
Yasmin ainda"* —, e as duas afirmações não podem valer juntas. É o campo cuja
honestidade o `AGENTS.md` cobra por nome, e vale a Yasmin dizer qual é a certa.

### O cenário N06 **já existe no código**

O `cenarios-yasmin-v2.md` corrige a v1 com base nesta afirmação:

> *"É um cenário (N06) e uma prevalência que o código ainda não tem… o arquivo
> **nunca** teve um `N06`."*

**Isso não se sustenta.** O `N06_manutencao_noturna_ti` está implementado em
[`generator/normal.py`](../../generator/normal.py), **linha 281**, desde o #89 —
não em `generator/scenarios.py`, que foi o único arquivo consultado. Ele está lá
porque é atividade **legítima**, e pertence à rotina normal em vez da injeção de
cenários.

> **Correção de 12/11/2026:** esta página dizia linha **185**, e estava errada.
> A 185 é um ramo de persona da atividade normal; o `sink.episode("N",
> "N06_manutencao_noturna_ti", …)` está na 283, sob o comentário da 281. Quem
> fosse conferir a correção cairia no lugar errado — e a credibilidade dela
> depende de a pessoa achar o código.

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

**Medido de novo em 12/11, em outra escala, para mostrar de onde vem a
prevalência.** Com 15 funcionários em vez de 250, o gabarito traz 88 episódios:
P 24, B 16, L 12 e N 36 — sendo **N06 = 17**. Os três primeiros não mudam porque
o CATALOG injeta um número fixo por semente; o N06 **escala com a população**,
porque nasce das janelas de manutenção que o mundo sorteia. É isso que explica
por que ele é 53 na escala cheia e por que não aparece no `CATALOG`.

### O insumo dos pesos: a D-43 confere, a ordenação da D1 não

O [`pesos-yasmin-v1.md`](pesos-yasmin-v1.md) faz duas coisas, e elas tiveram
sortes diferentes na conferência.

**A ratificação da D-43 confere com o código, item por item.** O insumo ratifica
D1 = 1,0, D2 = 1,0, conduta = 1,0, postura = 0,5 e a C0 sem ponderação. O
`detection/presets.toml` traz exatamente isso, num bloco `[integration]` único
compartilhado por C1, C2 e C3, e a C0 fora dele. Confirmar a D-43 **não muda uma
linha de código** — a leitura dela é um sim.

**A ordenação de severidade proposta para a D1 diverge em dois atributos.** O
insumo organiza os sinais da D1 em Alto, Médio e Baixo; o `presets.toml` atribui
pontos, e a nota da D1 é a **soma** de todas as regras que disparam
(`detection/d1/scoring.py`). A comparação correta é entre o nível do insumo e a
pontuação da situação que ele descreve:

| A situação que o insumo descreve | Nível | Pontos no código | Bate? |
|---|---|---|---|
| Download grande para externo | **Alto** | 45 — `large_download` 20 + `download_to_external` 25 | ✅ o maior |
| Escalada de privilégio | **Alto** | 40 — `privilege_change` | ✅ |
| Acesso a recurso `restricted` | **Alto** | 35 — `sensitivity.restricted` | ✅ |
| Faixa `external` sem VPN | **Médio** | 30 — `network_kind.external` | ✅ topo do Médio |
| **Dispositivo pessoal** | **Baixo** | **25** — `personal_device` | ❌ acima de tudo que é Médio |
| Horário fora do padrão | **Médio** | 20 — `off_hours_employee` | ✅ |
| **`mfa_used = false` em login** | **Alto** | **15** — `login_without_mfa` | ❌ 8º de 10 |
| Navegação de risco | **Médio** | 10 — `risky_browsing` | ✅ |
| Faixa `home` | **Baixo** | 10 — `network_kind.home` | ✅ |

**Sete de nove batem. As duas que não batem estão quase invertidas entre si:** o
MFA ausente num login, que o insumo põe no **topo**, vale 15; o dispositivo
pessoal, que o insumo põe na **base**, vale 25.

> **Correção de 12/11/2026.** Esta página dizia **três** divergências, incluindo
> a faixa `external`. Eram **duas**: eu comparei pesos de regra isolados, quando o
> D1 soma os pontos de todas as regras que disparam. Com a soma, a `external`
> fica em 30 — abaixo dos três Altos e acima de todos os Médios, que é exatamente
> onde "topo do Médio" deve ficar.

⚠️ **Nada foi mudado.** Mexer nesses pontos **invalida as dez sementes da § 4** —
todo número do artigo teria de ser reexecutado, cerca de duas horas. A pergunta é
da Yasmin e do Davi juntos, e tem três saídas possíveis:

1. **A ordenação do insumo está certa** e os pontos se ajustam — e então as dez
   sementes rodam de novo, antes da banca
2. **Os pontos estão certos** e a ordenação do insumo se corrige — e aí ela não
   pode ir para o artigo como está
3. **As duas descrevem coisas diferentes** — o insumo fala de gravidade
   conceitual e os pontos, de poder discriminativo observado — e o artigo diz
   isso explicitamente, em vez de deixar a contradição implícita

A terceira é a mais provável e a mais honesta, mas é **decisão**, não conferência.

### O que a conferência **não** alcança

Duas coisas ficaram fora, e por limite de método, não de tempo:

| O quê | Por quê |
|---|---|
| O [insumo de LGPD e ISO](lgpd-iso-yasmin-v1.md) — a **D-19** | Afirmação sobre texto legal e sobre controles da ISO/IEC 27001:2022 só se confere **na fonte**. Nada nele é checável contra o código |
| Os **quatro casos reais** do [insumo de exemplos](exemplos-reais-yasmin-v1.md) | Mesmo motivo. Estão em [citações pendentes](../citacoes-pendentes.md), e um deles — Capital One — **declara-se incompleto no próprio insumo** |

Conferir afirmação contra código é o que uma IA pode fazer. Conferir afirmação
contra fonte é o que o [`AGENTS.md`](../../AGENTS.md) seção 3 reserva a uma
pessoa, por nome.

### Duas outras afirmações do `.zip` que não se confirmam

O `README.md` do pacote dizia que os arquivos *"também ficam versionados em
`TCC_SDCAC/docs/insumos/`"* e que o relatório
`docs/relatorios/2026-11-10-sessao-40.md` estava *"já feito"*. Nenhuma das duas
era verdade em 11/11: os insumos entraram **neste** Pull Request, e aquele
relatório não existe em nenhuma branch do repositório.

### A auditoria de citações de 12/11, e o que ela pode fazer

Uma IA auditou as onze citações pendentes e identificou as obras, os dados
bibliográficos e, em vários casos, o trecho que sustenta cada afirmação. O
documento está em
[auditoria das citações](auditoria-citacoes-ia-v1.md), versionado como recebido.

**Ela não fecha pendência nenhuma**, e o `AGENTS.md` seção 3 diz por quê:
*"referência bibliográfica que a IA produziu e ninguém conferiu na fonte"* está
entre o que nunca é aceitável. **A própria auditoria recusou assinar por vocês** —
é a parte mais importante dela, e está citada no cabeçalho do insumo.

**O que ela muda é o custo.** Antes, conferir era procurar a obra, decidir se era
a certa e ler o trecho. Agora é abrir um documento nomeado e checar se o trecho
sustenta a afirmação.

**E traz cinco correções que mudam o artigo**, nenhuma aplicada:

| | |
|---|---|
| `KAUFMAN et al., 2012` | O ano seria **2011** — KDD '11 |
| Target | O evento é de 2013, a publicação de **2014** |
| Bangor et al. | A média da amostra deles é **69,5**, não 68, e eles dão médias e desvios — **não limites de faixa** |
| Nielsen e Landauer | **Não** estabeleceram cinco participantes como regra; o estudo é um modelo |
| Sommer e Paxson | Tratam de generalização, **não** especificamente de dado sintético |

As três últimas são do tipo mais perigoso: a obra existe, está citada, e o que o
texto afirma **não é o que ela diz**. É exatamente o que a validação automática
não pega e a banca pega.

**E uma referência nova que ela propõe — Tariq et al. (2025), sobre fadiga de
alertas — não entra.** Citação nova sugerida por IA é o caso que a regra nomeia
primeiro.

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
