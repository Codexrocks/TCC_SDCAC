# Plano do TCC

| | |
|---|---|
| Versão | 2.0 — 06/09/2026 |
| Período | 02/09 a dezembro de 2026 (16 semanas) |
| Equipe | Davi · Yasmin · Filipe |
| Substitui | Plano Executivo e Manual Técnico v1 — modelo de uma dimensão |

Esta página define **o que o trabalho é**: tema, problema, pergunta, objetivos,
delimitação e desenho experimental. Como ele será executado está no
[cronograma](cronograma.md) e no [processo de trabalho](processo.md); como o
sistema será construído, na [arquitetura](arquitetura.md).

**Mudança central em relação à versão 1:** o projeto deixa de ser um detector de
anomalias baseado em regras e passa a ser um **estudo comparativo**. O modelo de
três dimensões só tem valor se for medido contra uma linha de base de regras
fixas — e é isso que a pergunta de pesquisa exige.

## Precedência

Quando a documentação, o artigo e este plano divergirem, **o plano prevalece**
até que uma decisão registrada em [decisões](decisoes.md) o altere.

Isso vale para texto, não para trava. As travas do repositório — rulesets do
GitHub, `scripts/validar.py`, `scripts/governanca.py` — continuam acima de
qualquer documento, inclusive deste. Regra do [`AGENTS.md`](../AGENTS.md), seção
12: se a trava e o texto discordarem, quem está desatualizado é o texto.

---

## 1. Ficha técnica

### 1.1 Tema

Sistema de Avaliação Multidimensional de Risco Comportamental em ambientes
corporativos simulados.

> **O título ainda não mudou no repositório.** O anterior — "Detecção de
> Comportamentos Anômalos" — consta na [Tarefa 01](entregas/tarefa-01.md),
> entregue em 03/09, e no README. A mudança precisa ser comunicada ao orientador
> antes de valer. Decisão **D-01**, ainda aberta.

### 1.2 Problema

A análise de segurança baseada exclusivamente em eventos individuais e regras
fixas gera interpretações imprecisas: uma divergência em relação ao
comportamento habitual não representa, necessariamente, uma ameaça, e eventos
legítimos são sinalizados como suspeitos. Ao mesmo tempo, a análise isolada de
cada evento impede a identificação de padrões comportamentais e da exposição
gradual do usuário ao risco — situações em que nenhum evento ultrapassa o limiar
de alerta, mas a sequência sim.

### 1.3 Pergunta de pesquisa

> A avaliação combinada do risco do evento individual, do desvio comportamental
> do usuário e da exposição acumulada ao risco **reduz a taxa de falsos
> positivos, a uma mesma revocação, e aumenta a revocação em cenários
> longitudinais** na identificação de comportamentos potencialmente anômalos,
> quando comparada à análise baseada exclusivamente em regras fixas aplicadas a
> eventos individuais, em ambiente corporativo simulado?

**Operacionalização.** A pergunta é respondida por duas grandezas, ambas
calculadas sobre os mesmos logs e os mesmos cenários:

| Grandeza | O que mede | Métrica |
|---|---|---|
| **Ruído** | Quanto o modelo alarma à toa | Taxa de falsos positivos (FPR), com a revocação fixada no mesmo nível em todas as configurações |
| **Cobertura** | O que só o modelo enxerga | Revocação nos cenários longitudinais — aqueles em que o risco cresce ao longo de dias sem que um evento isolado dispare alerta |

Precisão@k sobre a fila de alertas é métrica secundária, reportada se o tempo
permitir.

#### Por que a direção está declarada

A redação anterior perguntava se o modelo produz "resultados diferentes". Isso é
trivialmente verdadeiro: qualquer alteração no algoritmo produz resultados
diferentes, e uma FPR de 12,3% contra 12,2% também é "diferente". A pergunta era
mensurável e, ao mesmo tempo, não exigia que a resposta fosse interessante — e a
Conclusão acabaria afirmando algo que a pergunta nunca perguntou.

Declarar a direção resolve isso sem cair no defeito oposto. A expressão "mais
contextualizada" continua **fora** da pergunta: ela é a conclusão que os dois
números autorizam ou não, não a hipótese.

#### A pergunta admite "não"

De três maneiras, todas resultados publicáveis:

- A FPR não cai, ou cai dentro do ruído experimental
- A revocação longitudinal não sobe
- Uma sobe e a outra não — o modelo troca ruído por cobertura, em vez de ganhar
  nas duas

Nenhuma dessas hipóteses invalida o trabalho. O que invalidaria é não conseguir
distinguir qualquer uma delas do acaso — daí o tratamento estatístico da
decisão **D-13**.

O critério de relevância — quanto de redução conta como resposta afirmativa —
precisa ser declarado **antes** de existir número, e é a decisão **D-15**.

### 1.4 Objetivo geral

Desenvolver um modelo de classificação de risco baseado na análise integrada de
eventos individuais, padrões comportamentais e exposição acumulada, e avaliá-lo
comparativamente a uma linha de base de regras fixas aplicadas a eventos
individuais, em um ambiente corporativo simulado.

### 1.5 Objetivos específicos

No artigo, os objetivos não carregam número de semana. A rastreabilidade
objetivo → semana vive aqui.

| # | Objetivo específico | Dimensão | Semana | Frente |
|---|---|---|---|---|
| OE1 | Definir e modelar os tipos de eventos e os atributos necessários para representar atividades de usuários em um ambiente corporativo simulado, e gerar logs sintéticos normais, divergentes e suspeitos. | — | S6 | Davi |
| OE2 | Implementar uma linha de base de regras fixas aplicadas a eventos individuais, que servirá como grupo de controle da comparação. | Base | S7 | Davi + Yasmin |
| OE3 | Desenvolver um mecanismo de classificação de risco do evento individual a partir de características previamente definidas (horário, IP, dispositivo, localização, origem, VPN). | D1 | S7 | Davi + Yasmin |
| OE4 | Implementar mecanismos para identificar divergências entre eventos observados e o padrão comportamental previamente estabelecido para cada usuário. | D2 | S8 | Davi + Yasmin |
| OE5 | Desenvolver uma abordagem para avaliar a exposição acumulada ao risco a partir da recorrência, combinação e evolução temporal dos comportamentos. | D3 | S8, S11 | Davi + Yasmin |
| OE6 | Integrar as três dimensões em uma avaliação final e comparar, por estudo de ablação, as configurações resultantes com a linha de base, usando cenários simulados e as métricas definidas. | Todas | S11, S12 | Todos — métricas: Filipe |

> **Dashboard — decisão pendente (D-02).** A proposta registrada aqui é que o
> dashboard seja *instrumento de análise*, descrito na Metodologia e na
> [arquitetura](arquitetura.md), e não objetivo específico. Ele viabiliza o OE6
> ao tornar o risco decomponível por dimensão. Alternativas: elevar a objetivo
> específico (OE7), ou excluir e declarar na delimitação. Qualquer uma serve; a
> omissão não.

### 1.6 Delimitação

O trabalho está delimitado ao desenvolvimento e à avaliação de um protótipo em
ambiente corporativo simulado, com eventos previamente definidos e logs gerados
para fins experimentais. O sistema analisa divergências comportamentais e
indicadores de exposição ao risco; ele **não** tem por objetivo:

- confirmar invasões ou identificar autores de ataques;
- substituir ferramentas profissionais de segurança (SIEM, EDR, UEBA
  comerciais);
- aplicar bloqueio automático ou resposta autônoma a incidentes;
- monitorar integralmente a navegação de usuários ou coletar dados pessoais
  além dos necessários à simulação;
- demonstrar superioridade em dados reais de produção — os resultados valem
  para o ambiente simulado descrito.

### 1.7 Justificativa

A justificativa é bloco obrigatório da Introdução. Regra adotada: **evidência
dos dois, tese de um.**

| Quem | O que entrega |
|---|---|
| Yasmin | Casos reais e a lacuna na literatura — ameaças internas, fadiga de alertas, *base-rate fallacy* |
| Filipe | Números setoriais e a aritmética dos falsos positivos |
| Davi | O parágrafo que responde "por que este trabalho, agora, para quem" |

Decisão **D-04**, fechada em 06/09.

### 1.8 Metodologia

Pesquisa aplicada, experimental, de natureza quantitativa, executada por meio da
construção de um protótipo, execução de cenários controlados e avaliação de
desempenho por estudo de ablação (seção 2). A definição final dos pesos e
fórmulas ocorre durante o desenvolvimento e é validada por análise de
sensibilidade, descrita na [arquitetura](arquitetura.md).

---

## 2. Desenho experimental

As três dimensões formam naturalmente um estudo de ablação: liga-se uma
componente por vez e mede-se o que cada uma acrescenta. Mesmos logs, mesmos
cenários, mesmas métricas nas quatro configurações.

```text
C0 ──────► C1 ──────► C2 ──────► C3
regras     + risco    + desvio    + exposição
fixas      do evento  do usuário  acumulada
(controle) (D1)       (D1+D2)     (D1+D2+D3)
```

| Configuração | O que avalia | Papel no experimento |
|---|---|---|
| **C0** Linha de base | Regras fixas sobre o evento isolado, sem histórico do usuário — as quatro regras da v1. | Grupo de controle. Sem ela, a Conclusão só pode dizer "o modelo funcionou". |
| **C1** D1 | Características do evento: horário, IP, dispositivo, localização, origem, VPN. | Mede o ganho de atributos mais ricos sobre a mesma lógica pontual. |
| **C2** D1 + D2 | Desvio em relação ao baseline histórico do próprio usuário. | Mede o ganho de contexto individual — redução de falsos positivos esperada. |
| **C3** D1 + D2 + D3 | Recorrência, combinação e evolução temporal ao longo de dias. | Mede a contribuição original do trabalho — cobertura de cenários longitudinais. |

Cada configuração é uma *flag* de execução no mesmo código, não quatro sistemas.
Isso garante que a única variável entre as linhas da tabela seja a dimensão
acrescentada.

Se a D3 não melhorar nada, **isso também é resultado**. Uma boa pergunta admite
a resposta "não".

---

## 3. Produtos finais

1. **Artigo científico** completo, no [formato COBEM](cobem.md) — 6 a 10
   páginas no total, referências em autor-ano, texto em português com *abstract*
   em inglês —, com a tabela de ablação de quatro linhas. Decisão **D-11**,
   fechada em 07/09.

   > **O limite de páginas é restrição de projeto, não detalhe de formatação.**
   > O artigo inteiro cabe em 6 a 10 páginas, tabelas e figuras incluídas. Isso
   > condiciona quanto cada seção pode ocupar e desaconselha acrescentar
   > capítulos à estrutura — ver decisão **D-20**.
2. **Protótipo funcional:** API, gerador de logs, quatro configurações de risco
   selecionáveis, dashboard.
3. **Repositório documentado:** código, [decisões](decisoes.md), relatórios de
   sessão, atribuição de IA por commit e de humano por papel CRediT.
4. **Apresentação e defesa** ensaiada e cronometrada.

---

## 4. Riscos

| Risco | Prob. | Impacto | Mitigação | Dono |
|---|---|---|---|---|
| Cenários longitudinais não são criados, e a D3 fica sem teste | Média | Alto — a contribuição original não é avaliada | Definir L1–L3 na S5 (M2); o gerador da S6 já produz 30 dias de histórico | Yasmin |
| Pesos arbitrários, e a banca pergunta de onde saíram | Alta | Médio | Declarar como preliminares; análise de sensibilidade na S12; AHP se houver tempo | Yasmin |
| Dados sintéticos fáceis demais inflam os resultados | Média | Alto | Ruído legítimo — viagem, plantão, home office; discutir na S13 citando Sommer & Paxson | Davi |
| Vazão de PRs baixa trava contribuições dos colegas | Alta — já ocorreu | Alto | SLA de 24 h; congelar infraestrutura em semana de capítulo | Davi |
| Líder redige tudo e os demais deixam de ser coautores | Média | Alto na defesa | Caneta rotativa combinada agora, não em outubro | Davi |
| Isolation Forest consome tempo da frente de dados | Média | Baixo | Opcional por definição; cortar na S10 se as métricas estiverem em risco | Filipe |
| Repositório e artigo divergem — título, dimensões | Alta — já ocorre | Médio | Atualizar README e arquitetura na S5; este plano é a fonte de verdade | Davi |
| Escopo cresce — bloqueio, resposta automática, dados reais | Baixa | Alto | Delimitação explícita (1.6); toda ampliação passa pelas [decisões](decisoes.md) | Davi |

Não há risco listado para "a Introdução não sai em 10/09". É o marco mais
próximo e o único sem plano B.

---

## 5. O que este plano ainda não decide

O plano define o trabalho; ele não fecha sozinho tudo que o trabalho exige. Sete
lacunas metodológicas continuam abertas e vencem em **M2 (01/10)** — nenhuma
delas muda o texto da Introdução, e todas mudam o que a S12 conseguirá afirmar.

Estão registradas como **D-12 a D-19** em [decisões](decisoes.md), com dono e
prazo. As duas de maior consequência:

- **Unidade de análise** (D-12) — evento, usuário-dia ou episódio. A escolha
  muda o valor das métricas, não só a apresentação: o mesmo cenário
  longitudinal pode render revocação de 0,15 medido por evento e 1,00 medido
  por episódio.
- **Tratamento estatístico** (D-13) — uma semente e uma execução por
  configuração não permitem distinguir "a C3 é melhor" de "a C3 deu sorte nesta
  semente".
