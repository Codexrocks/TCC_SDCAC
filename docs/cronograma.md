# Cronograma

**Entrega do TCC: 10/12/2026.** Onze semanas a partir de 24/09.

Cada semana tem um entregável, um responsável e um **critério de aceite** — a
condição que permite dizer "pronto" sem discussão. Sem critério escrito não há
como recusar uma entrega, e a recusa vira atrito.

## Prazos do professor

| Data | Entrega | Estado |
|---|---|---|
| **05/09/26** | Tema do trabalho e composição do grupo — *Tarefa 01* | ✅ **Entregue em 03/09** |
| **24/09/26** | Introdução do artigo no template **COBEM 2026** — *Tarefa 02* | ⏳ **amanhã** |
| Quinzenal | Reunião de acompanhamento com o orientador | — |
| **10/12/26** | **Entrega do TCC** | — |
| Dezembro | Apresentação e defesa | — |

## Onde estamos, em 23/09

Honestidade sobre o ponto de partida, porque é o que torna o resto realizável ou
não:

| Capítulo | Estado | Semana prevista |
|---|---|---|
| 1. Introdução | Escrita, com **seis blocos de complementação vazios** | S2 — venceu 10/09 |
| 2. Referencial teórico | Rascunho pronto, **fora do repositório** | S3 e S4 — vence 24/09 |
| 3. Metodologia | Esqueleto | S5 |
| 4. Resultados | Esqueleto | S13 |
| 5. Conclusão | Esqueleto | S14 |

**Nenhuma linha de código existe ainda.** O que existe é a especificação do
gerador — que chega ao repositório pelo Pull Request #43, e ainda não está na
`main`.

A S5 carrega, além da Metodologia, o que ficou de S2 a S4. É a única semana com
acúmulo declarado — depois dela o cronograma volta a ter uma entrega por semana.

## As onze semanas

| # | Período | Entregável | Critério de aceite | Quem |
|---|---|---|---|---|
| **S5** | 25/09–01/10 | `artigo/03-metodologia.md` + arquitetura v2 · **o atrasado de S2 a S4** · ajustar a Introdução à **D-25**, que amplia a dimensão 3 | Teste de coerência pergunta ↔ objetivos ↔ métricas aprovado · **D-12 a D-19 fechadas** · cenários definidos | Davi (caneta) · Yasmin (cenários) · Filipe (métricas) |
| **S6** | 02–08/10 | Schema, migrações, **gerador de eventos** e ingestão | Uma semente completa gerada · as **sete checagens** do catálogo passando · carga por `COPY` | **Filipe** (gerador) · Davi (schema e ingestão) |
| **S7** | 09–15/10 | C0 (regras fixas) e motor D1 | Cenários pontuais produzem o score esperado · C0 e C1 selecionáveis por flag · **C0 sem nenhum histórico do funcionário** | Davi + Yasmin |
| **S8** | 16–22/10 | D2 (desvio do padrão) e D3 (exposição + higiene) | C2 e C3 executam ponta a ponta · cenário longitudinal gera exposição crescente **sem** alerta pontual · D3 reporta as duas parcelas separadas | Davi + Yasmin |
| **S9** | 23–29/10 | Dashboard Streamlit | Leitor externo identifica em **menos de 1 min** por que um usuário está em risco alto · risco decomponível por dimensão | Filipe |
| **S10** | 30/10–05/11 | Isolation Forest — **opcional** | Documentado como benchmark · o TCC não depende dele | Filipe |
| **S11** | 06–12/11 | Execução de todos os cenários nas quatro configurações | Reprodutível por script único · o número de sementes definido pela **D-13**, as mesmas nas quatro configurações | Todos (Yasmin) |
| **S12** | 13–19/11 | Tabela de ablação, sensibilidade dos pesos, gráficos | Cada número sai de notebook versionado · Wilcoxon pareado sobre as diferenças | Filipe + Davi |
| **S13** | 20–26/11 | `artigo/04-resultados.md` | Cada limitação nomeada tem proposta de trabalho futuro · LGPD e ISO 27001 entram aqui | Filipe (caneta) |
| **S14** | 27/11–03/12 | `artigo/05-conclusao.md` | A pergunta é respondida com **sim, não ou parcialmente — e um número** | Davi (caneta) |
| **S15** | 04–10/12 | Versão final diagramada · **ENTREGA 10/12** | 8 a 12 páginas no template COBEM 2026 · zero referência não conferida · bloco em inglês depois das referências · responsabilidade autoral | Todos |
| **S16** | 11/12 em diante | Slides, ensaio cronometrado, defesa | Cada integrante apresenta qualquer seção sob sorteio | Todos |

## Como o trabalho chega ao repositório

A equipe e os papéis continuam os mesmos. **O que mudou é só o caminho:** a
Yasmin e o Filipe produzem fora do GitHub — documento, planilha, rascunho — e o
Davi versiona.

> **Dois arquivos ainda dizem o contrário.** O [`AGENTS.md`](../AGENTS.md) e a
> [política de uso de IA](uso-de-ia.md) afirmam que, desde 23/09, o Davi conduz
> o trabalho sozinho. A frase descreve mal o que houve: quem ficou com uma
> pessoa foi a **aprovação de Pull Request**, não o trabalho. Os dois são
> arquivos protegidos e entram em Pull Request próprio, com as 24 h de espera.
> Até lá, **vale o que está escrito aqui**.

| | |
|---|---|
| **Quem produz** | Yasmin e Filipe, na ferramenta que preferirem |
| **Quem versiona** | Davi, por Pull Request |
| **Quem responde pelo conteúdo** | Quem produziu — a autoria não muda por causa do caminho |

Três consequências que valem saber:

- **A declaração de IA continua obrigatória**, e não vira frase genérica. Quem
  produz diz se usou assistente e no quê; o Davi transcreve. Os quatro campos do
  Pull Request passam a ser respondidos assim:

  | Campo | O que responder |
  |---|---|
  | Qual IA | A que **quem produziu** usou — não a que o Davi usou para versionar |
  | No que ajudou | O que ela fez no material recebido. Se quem produziu não informou, **escreva isso**: "não declarado por quem produziu" |
  | O que é seu | Nomear a pessoa e o que ela decidiu. "Versionado por Davi" não responde |
  | Conferiu tudo? | Responde quem versiona, sobre o que leu. Se não leu inteiro, diz que não leu |
- **A aprovação de PR ficou com uma pessoa só.** Foi por isso que as duas
  aprovações viraram 24 h de espera e justificativa, em 23/09
- **O que não está no repositório não existe para a banca.** Rascunho em pasta
  local não entra no histórico, e o histórico é a prova do processo

## O que cada um faz

### Davi — líder, backend e redação constitutiva

| Semana | Entregável |
|---|---|
| S5 | Metodologia (caneta) · arquitetura v2 · fechar D-12 a D-19 |
| S6 | Schema, migrações, carga e ingestão |
| S7 | C0 (regras fixas, sem histórico) e motor D1 |
| S8 | D2, D3 e a integração |
| S11 | Execução dos cenários |
| S12 | Tabela de ablação, junto do Filipe |
| S14 | Conclusão (caneta) |
| Contínuo | Versionar o trabalho dos outros dois · prazos · orientador |

### Yasmin — cybersecurity

| Semana | Entregável |
|---|---|
| S5 | **Cenários**: pontuais, de contexto, longitudinais e de escalada legítima (D-06 e D-16) · desenho **sem ver as fórmulas** |
| S5 | Referencial teórico — converter o rascunho para ABNT e fechar as citações pendentes |
| S7 | Regras e pesos preliminares da C0 e da D1 |
| S8 | Validação do comportamento da D2 e da D3 contra os cenários |
| S11 | Execução dos cenários — é a dona do desenho |
| S13 | Interpretação dos resultados · LGPD e ISO 27001 nas limitações |

### Filipe — dados e dashboard

| Semana | Entregável |
|---|---|
| S6 | **Gerador de eventos** — personas, calendário, rotina, ruído legítimo. É a peça de maior superfície da especificação |
| S9 | Dashboard Streamlit, com risco decomponível por dimensão |
| S10 | Isolation Forest — opcional, e é a folga do cronograma |
| S12 | Métricas, tabelas e gráficos · Wilcoxon pareado |
| S13 | Resultados e discussão (caneta) |

## Marcos e caminho crítico

| Marco | Data | O que fecha | Por que é marco |
|---|---|---|---|
| **M1** Introdução | 10/09 | Problema, pergunta, objetivos, delimitação | ⚠️ Entregue com seis blocos vazios. Fecha de verdade na S5 |
| **M2** Metodologia congelada | **01/10** | Cenários, métricas, quatro configurações, atributos | Congela o que será medido **antes** de existir código a defender |
| **M3** Modelo executável | **22/10** | C0 a C3 rodando sobre o mesmo gerador | Última data em que uma dimensão pode ser cortada sem comprometer a comparação |
| **M4** Tabela de ablação | **19/11** | Números finais das quatro configurações | A partir daqui o trabalho é escrita. Nenhuma alteração de código é aceita |
| **M5** Entrega | **10/12** | Artigo diagramado e submetido | — |

**Caminho crítico:** M2 → S6 (gerador com histórico de um ano) → S8 (D3) → S11 (execução) → S12 (tabela) → M4.

Um atraso em qualquer desses pontos atrasa a resposta à pergunta de pesquisa.
Dashboard, Isolation Forest e referencial teórico correm em paralelo e têm folga.

## O que está em risco, e o que fazer

| Risco | Onde aperta | Mitigação |
|---|---|---|
| **M2 em 8 dias** com 14 decisões abertas | D-12 a D-19 vencem em 01/10, e os cenários também | Fechar as sete lacunas metodológicas antes de escrever a Metodologia |
| **Gerador sem parâmetros** | 26 definições abertas na especificação do gerador — personas, matriz cargo × sistema, faixas de rede | As perguntas P06 a P10 e P24 a P31, numeradas na especificação que chega pelo PR #43, precisam de resposta antes da S6 |
| **Nenhum código em 23/09** | S6 a S8 são três semanas para banco, gerador e quatro motores | A S10 é o único corte disponível: o Isolation Forest é opcional por definição |
| **Referencial fora do repositório** | O rascunho existe e não está versionado | Entra na S5, convertido para ABNT |

> **A S10 é a folga do cronograma.** Se a S6, a S7 ou a S8 estourarem, o
> Isolation Forest sai e a semana é reaproveitada. Foi declarado opcional desde o
> começo, na decisão **D-10**, justamente para isso.

## Estrutura do artigo

Cinco seções, conforme o escopo definido pelo professor:

1. Introdução
2. Referencial Teórico
3. Metodologia
4. Resultados e Discussões
5. Conclusão

O [formato do artigo](formato-do-artigo.md) — COBEM 2026, com as referências em
ABNT — define o resto: de 8 a 12 páginas, títulos de seção em maiúsculas, e o
bloco em inglês depois das referências.
