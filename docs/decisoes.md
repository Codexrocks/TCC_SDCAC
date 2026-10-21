# Registro de decisões

Toda decisão de escopo, arquitetura ou processo entra aqui, com data, dono e
status. **Uma decisão só existe quando está registrada.**

Este registro é o Anexo A do [plano](plano.md), vivo. Enquanto uma decisão
estiver aberta, o plano descreve a *proposta*, não o combinado.

## O que entra aqui, e o que não entra

| Natureza | Onde vive | Fecha com |
|---|---|---|
| **Decisão** — uma escolha a fazer | Esta página | Uma escolha registrada, que continua legível |
| **Tarefa** — algo a executar | Issue no GitHub | Um commit |
| **Prazo** — quando cada coisa acontece | [Cronograma](cronograma.md) | A semana passar |

Decisão não vira issue. O valor de uma decisão é permanecer visível; issue
fechada fica enterrada.

---

## Abertas

<!-- QUADRO:inicio decisoes-abertas -->
<!-- Bloco gerado por scripts/quadro.py a partir de quadro.toml. Editar aqui nao adianta: a proxima execucao reescreve. -->

| ID | Decisão | Proposta | Dono | Prazo | Situação |
|---|---|---|---|---|---|
| D-06 | Cenários de contexto (B) e longitudinais (L) | Adotados; desenho detalhado na S5 | Yasmin | 01/10/2026 | ⚠️ Atrasado há 20 dias |
| D-07 | Caneta rotativa por seção | Uma pessoa redige, duas revisam, a caneta gira. Registrada pelo Davi quando Yasmin e Filipe confirmarem | Davi, Yasmin, Filipe | — | 🗓️ Sem prazo |
| D-09 | Pesos preliminares e análise de sensibilidade | Valores preliminares; sensibilidade na S12 | Yasmin | S8 | ⏳ Vence em 1 dia |
| D-15 | Critério de relevância declarado a priori | Origem do número decidida em 14/10: argumento operacional — quantos alertas falsos um analista absorve por turno. Falta o valor, e ele perde o sentido no dia em que a primeira execução for registrada | Davi, Yasmin, Filipe | 01/10/2026 | ⚠️ Atrasado há 20 dias |
| D-16 | Controle negativo longitudinal | Acrescentar cenário de escalada legítima aos cenários de teste | Yasmin | 01/10/2026 | ⚠️ Atrasado há 20 dias |
| D-19 | Vertente LGPD e ISO/IEC 27001 | Entra como limitação e trabalho futuro na S13 | Yasmin | 01/10/2026 | ⚠️ Atrasado há 20 dias |
<!-- QUADRO:fim decisoes-abertas -->

## Adotadas, a confirmar

<!-- QUADRO:inicio decisoes-a-confirmar -->
<!-- Bloco gerado por scripts/quadro.py a partir de quadro.toml. Editar aqui nao adianta: a proxima execucao reescreve. -->

| ID | Decisão | Proposta | Dono | Prazo | Situação |
|---|---|---|---|---|---|
| D-05 | Ablação em quatro configurações (C0 a C3) | Confirmar no M2 | Davi | 01/10/2026 | ⚠️ Atrasado há 20 dias |
| D-10 | Isolation Forest como benchmark opcional | Cortável na S10, se as métricas estiverem em risco | Filipe | S10 | 🗓️ Em 15 dias |
| D-43 | Pesos de integração das dimensões na nota final | Um conjunto só de pesos para C1, C2 e C3 — D1 1,0; D2 1,0; conduta 1,0; postura 0,5 — e a C0 sem ponderação nenhuma. Peso próprio por configuração faria a tabela de ablação medir duas coisas ao mesmo tempo: a dimensão acrescentada e o peso trocado. A postura entra com metade porque é estado, e não ação. Valores preliminares, sujeitos à análise de sensibilidade da D-09 | Davi, Yasmin | S8 | ⏳ Vence em 1 dia |
<!-- QUADRO:fim decisoes-a-confirmar -->

## Fechadas

| ID | Decisão | O que ficou | Data |
|---|---|---|---|
| D-01 | Mudança de título | **Adotado "Sistema de Avaliação Multidimensional de Risco Comportamental"**, comunicado ao orientador. O título anterior fica na [Tarefa 01](entregas/tarefa-01.md) como registro do que foi entregue em 03/09 | 23/09/2026 |
| D-02 | Dashboard: objetivo, instrumento ou fora do escopo | **Opção A — painel como instrumento de análise**, não objeto de um segundo experimento. É a proposta do [plano](plano.md), seção 1.5, e a que a Metodologia já pressupunha na § 3.9. Não há avaliação com participantes, o que mantém coerente a declaração de ausência de dado de pessoa real da § 3.2. Aberta desde 08/09, fechada a pedido do Davi | 14/10/2026 |
| D-03 | Operacionalização de "resultados diferentes" | FPR a revocação fixa **e** revocação longitudinal, com a **direção declarada** na pergunta. Precisão@k é secundária. Ver [plano, seção 1.3](plano.md) | 07/09/2026 |
| D-04 | Dono da Justificativa | Evidência de Yasmin e Filipe; tese e redação de Davi | 06/09/2026 |
| D-08 | SLA de resposta a Pull Request | 24 horas. PR sem resposta em 24 h é item obrigatório de pauta | 06/09/2026 |
| D-11 | Formato do artigo | **COBEM 2026 para tudo, ABNT só para a lista de referências.** Consta duas vezes nas orientações do professor, versionadas em [`templates/`](../templates/README.md). A volta anterior, que dizia CREEM 2026, foi engano de arquivo: o `.docx` tratado como sendo do professor era de evento irmão. ⚠️ **O template do COBEM 2026 ainda não está no repositório.** Quarta volta nesta decisão — o histórico das quatro está em [formato do artigo](formato-do-artigo.md) | 23/09/2026 |
| D-12 | Unidade de análise das métricas | **Duas unidades, declaradas separadamente**: evento para os cenários pontuais, episódio para os de contexto e longitudinais. Implementado em `detection/integracao/composition.py`; `tests/test_schema.py` confere no schema que a D3 alarma sobre um período, e não sobre um evento | 14/10/2026 |
| D-13 | Tratamento estatístico dos resultados | **Faixa e regra de fechamento, não número final** — como o alerta da própria decisão exigia. 10 a 20 sementes, as mesmas nas quatro configurações, Wilcoxon pareado. A regra de corte foi declarada em 28/09, respondendo à P31: ciclo completo de uma semente até 30 min → 20 sementes; acima disso → 10, com o motivo registrado. **O número final sai da S11**, e isso não impede o fechamento. `tests/test_portas.py` trata semente descartada como caso previsto, não como erro | 14/10/2026 |
| D-14 | O que fazer se a C0 não alcançar revocação 0,90 | **Curvas precisão-revocação completas, não pontos únicos.** O teto de pontuação da C0 foi desenhado para não virar degrau na curva — `detection/c0/rules.py` e `detection/integracao/composition.py` —, e `tests/test_c0.py` cobre o empate no teto | 14/10/2026 |
| D-17 | Janela de constituição do baseline da D2 | **Janela de treino anterior e disjunta da janela de avaliação.** `detection/d2/scoring.py` recusa evento posterior na fronteira e `runner/experiment.py` falha se as janelas se cruzarem; a trava está coberta em `tests/test_baseline.py` | 14/10/2026 |
| D-18 | Dupla contagem e escala na integração | **O evento atual não entra na janela de exposição.** `detection/d3/posture.py` e `detection/d3/scoring.py` recusam o risco do próprio evento avaliado; `tests/test_d3.py` registra a D-18 como trava, e não como aviso na documentação | 14/10/2026 |
| D-20 | Sexto capítulo do artigo (`04-desenvolvimento`), proposto pelo plano | **Não entra.** As orientações escritas do professor definem **cinco seções**, com a quinta juntando Conclusão e Referências. É a palavra de quem tem autoridade sobre a estrutura, e ela já estava no repositório — não precisava esperar reunião. O argumento de espaço, que já tinha caído quando a extensão virou 8 a 12 páginas, deixa de importar | 23/09/2026 |
| D-21 | Idioma do artigo | Texto inteiro em **português**; só o *abstract* e as *keywords* em inglês. O template pede inglês, mas quem define para o TCC é a coordenação | 07/09/2026 |
| D-22 | Onde ficam os insumos das encomendas | **`docs/insumos/`**, não `artigo/insumos/`. O GitBook **escreve** em `artigo/` e normaliza o Markdown ao salvar — foi assim que os comentários dos seis capítulos sumiram em 06/09. Em `docs/` ele só lê. As duas pastas publicam; o que muda é a escrita de volta. Cada insumo entregue entra no `docs/SUMMARY.md` | 07/09/2026 |
| D-23 | Volume de eventos da simulação | **20 a 50 eventos por dia útil**, faixa média por persona, 250 funcionários, 1 ano. Dá 1,15 a 2,9 milhões de eventos por semente. A média ponderada das personas precisa cair dentro da faixa. Ver [banco simulado](banco-simulado.md) | 23/09/2026 |
| D-24 | Qual dimensão compara o funcionário com o próprio padrão | **A dimensão 2.** Um conjunto de eventos de uma janela comparado ao padrão individual dos 3 primeiros meses. É o que mantém a pergunta de pesquisa respondível — sem isso, nenhuma dimensão compara o funcionário com ele mesmo | 23/09/2026 |
| D-25 | O que é a dimensão 3 | **Exposição acumulada e higiene de segurança**, com as **duas parcelas reportadas separadas** — nunca somadas num número só, cujo peso seria impossível de justificar. Atende também a regra de risco decomponível da [usabilidade](usabilidade.md). A Introdução entregue descreve a dimensão 3 só como exposição acumulada, e o ajuste está no [cronograma](cronograma.md), na S5 | 23/09/2026 |
| D-26 | A linha de base vira dimensão 1 ou continua separada | **Continua separada**: quatro configurações, C0 a C3, como no plano v2. Confirma a **D-05**. Abre a **P30**: duas das quatro regras da C0 usavam histórico do funcionário e contaminavam o grupo de controle — a C0 precisa ser puramente estática. **Precisado pela D-42**: o que a C0 não tem é **parâmetro aprendido**, e a janela de falhas de dois minutos continua nela | 23/09/2026 |
| D-27 | Calendário do gerador: dia útil, feriado e férias | **Calendário por persona**, não global: quem faz plantão trabalha fim de semana, e a manutenção de TI acontece de madrugada por motivo legítimo. Feriado tem **atividade residual** e férias têm **atividade legítima mínima** — nenhum dos dois é zero absoluto, senão "evento em férias" vira detector perfeito e a C0 acerta esses cenários sem olhar mais nada. A faixa de eventos da **D-23** passa a ser medida sobre os dias úteis de cada persona. É regra, não lista: só vira parâmetro quando as personas fecharem (**P07**). Ver [banco simulado](banco-simulado.md) | 28/09/2026 |
| D-28 | As janelas da dimensão 2 | **Sessão e usuário-dia**, com a nota sendo o **maior** dos dois desvios, nunca a soma. **Semana fica de fora**: acumulação ao longo de dias é o que a D3 mede, e se a D2 também olhasse sete dias a ablação não separaria a contribuição das duas. O usuário-dia é o denominador de falso positivo da **D-12** | 28/09/2026 |
| D-29 | Como o padrão é medido e como o desvio é calculado | Padrão com **mediana e MAD**, não média e desvio padrão: um dia de pico na janela de treino inflaria o desvio e mascararia divergência real pelos nove meses seguintes. Desvio robusto `(x − mediana) / (1,4826 × MAD)`, com **piso de dispersão** `máximo(1 evento; 10% da mediana)` — sem ele o funcionário perfeitamente regular tem MAD zero e a D2 alarma sobre as pessoas mais previsíveis. **Teto de 6** por componente, para um atributo não dominar a nota e esvaziar os pesos da **D-09**. Conjuntos usam novidade, proporções usam distância. Quem não tem histórico suficiente cai no **grupo de pares** | 28/09/2026 |
| D-30 | Escopo da higiene e as duas parcelas da dimensão 3 | Higiene em **cinco sinais**: desfecho de phishing, segundo fator e privilégio, atualização e antivírus do equipamento, dispositivo removível e navegação de risco. **Alerta de antivírus fica de fora** — exigiria modelar a detecção do próprio antivírus, e a informação útil já está no estado diário. A D3 reporta **conduta** e **postura** separadas, cada uma de 0 a 100: somá-las antes de exibir esconderia qual das duas causou o alerta, contra a regra de risco decomponível da [usabilidade](usabilidade.md). Detalha a **D-25** | 28/09/2026 |
| D-31 | O que separa a C0 da dimensão 1 | A **C0 é puramente estática** — leia-se **sem parâmetro aprendido**, pela **D-42**: horário fixo no fuso da sede, limite fixo de falhas por conta, faixas corporativas cadastradas e acesso a recurso restrito. Nada de "IP habitual", que era histórico do funcionário dentro do grupo de controle. A **D1 acrescenta** dispositivo, tipo de faixa com peso graduado, VPN, MFA, subtipo de configuração, tamanho e destino do download e categoria de navegação, trocando ponto fixo por peso por atributo, com o horário no fuso do funcionário. Fecha a **P30** e é o critério de aceite da **S7** | 28/09/2026 |
| D-32 | As duas versões do software, e a ordem | **v1 = motor, executor de linha de comando e API somente de leitura** (S6 a S8); **v2 = login, configuração editável e execução por job** (S9 em diante). A ordem é aritmética: a tabela de resultados sai do executor, não da API, e a S11 executa tudo nas quatro configurações. Entra a pasta `runner/` na [arquitetura](arquitetura.md). Ver [o software](software.md) | 28/09/2026 |
| D-33 | Presets canônicos contra configuração exploratória | **C0 a C3 são somente-leitura**, nascem em arquivo semeado e versionado. Configuração criada por usuário é marcada como **exploratória** e não pode ir ao artigo. Controle que alguém afrouxa deixa de ser controle, e configuração livre sobre a C3 abriria caminho para ajustá-la até ganhar — ajuste posterior ao resultado, que derruba a conclusão | 28/09/2026 |
| D-34 | Configuração é versão imutável, presa ao resultado | Salvar **cria a próxima versão**, com autor, data e hash; não altera a existente. Toda execução grava o identificador e o hash da configuração usada, e **execução sem hash é erro, não aviso**. É o registro de execução que a [Metodologia](../artigo/03-metodologia.md), seção 3.7, já promete ao leitor | 28/09/2026 |
| D-35 | Execução é job, não requisição | A requisição enfileira e devolve identificador; um processo separado consome a fila; o estado é consultado por outra chamada. **Fila em tabela do `sdcac`, sem Celery e sem Redis** — nesta escala, dependência nova não se paga. Na v1 o executor é de linha de comando e não precisa de fila | 28/09/2026 |
| D-36 | O contrato de leitura da API | Prefixo `/api/v1` desde o início; paginação em toda lista; data em UTC com fuso; nenhuma rota devolve HTML. **Score sempre decomposto** em C0, D1, D2 e a D3 partida em conduta e postura — número único impediria a decomponibilidade da seção 3.9 do artigo. A API **não lê o `ground_truth`** e **não calcula métrica**: precisão e revocação vêm de `sdcac.metrics`, gravada pelo avaliador | 28/09/2026 |
| D-37 | Departamentos e efetivo da corporação simulada | **Oito departamentos, 250 pessoas**: Operações e Atendimento 70, Comercial 45, Engenharia e Produto 40, Administrativo e Financeiro 35, TI 25, RH 15, Jurídico 10, Diretoria 10. Oito é o mínimo que sustenta uma matriz de acesso com sentido: precisa haver área com dado restrito, área com dado confidencial, área com privilégio técnico e áreas grandes sem acesso sensível nenhum. Tabelas em [banco simulado](banco-simulado.md) | 28/09/2026 |
| D-38 | Personas, calendários e faixa de eventos | **Seis personas**, cada uma com o seu calendário pela D-27: administrativo diurno (95), operação em turno (45), TI privilegiado (25), comercial viajante (45), híbrido (30), gestão e diretoria (10). A **média ponderada dá 32,7 eventos por dia útil** e o volume anual ≈ 1,93 milhão por semente — as duas dentro das faixas da **D-23**. O TI é a única persona acima do teto de 50, o que a D-23 permite porque restringe a média, não cada persona | 28/09/2026 |
| D-39 | Sistemas e matriz de acesso | **Dez sistemas em onze níveis** — o servidor de arquivos tem pasta `internal` e pastas `confidential`, que é o caso que separa "acessou o servidor" de "acessou o que não devia". Folha de pagamento, dossiê de pessoal e console de infraestrutura são `restricted`, com **15 pessoas de 250** alcançando algum deles. É a matriz que dá definição a "acesso incomum" e é sobre ela que os cenários da **D-06** são desenhados. Fecha também o que faltava da **P11** | 28/09/2026 |
| D-40 | Sede, filial e fusos horários | **São Paulo (UTC−3) com 210 pessoas e Manaus (UTC−4) com 40.** Corrige a recomendação anterior, de um fuso só: a **D-31** faz a C0 usar o fuso da sede e a D1 o fuso do funcionário, e com um fuso único essa diferença é decorativa. Com dois, quem encerra às 21:30 em Manaus são 22:30 em São Paulo — a C0 dispara e a D1 não. É falso positivo legítimo, fabricado por desenho, que é o mecanismo que a pergunta de pesquisa alega resolver | 28/09/2026 |
| D-41 | Dispositivos e estado inicial de higiene | **425 dispositivos**: 250 notebooks corporativos, 150 celulares corporativos e **25 celulares pessoais autorizados**. MFA ligado em ~87% no início. O dispositivo pessoal precisa existir no tráfego legítimo: se aparecesse só em cenário, viraria detector perfeito e a C0 acertaria sem olhar mais nada — a mesma armadilha que a D-27 evitou em férias e feriado | 28/09/2026 |
| D-42 | A quarta regra da C0: janela de falhas ou evento isolado | Decidida pelo Davi em 13/10, no pedido *"mantenha a janela e corrija a Metodologia, registra a D-42"*. **A janela fica**, com limiar fixo igual para todos e memória de dois minutos. E "puramente estática" passa a ser dito com precisão: a C0 não tem **parâmetro aprendido** — nada estimado do comportamento de ninguém. A distinção é entre correlação de curto prazo e perfil individual: a primeira é regra de SIEM, a segunda é a D2. Tirar a janela produziria um grupo de controle incapaz de pegar tentativa sucessiva de autenticação, e o ganho apareceria nas dimensões por falta de adversário — a banca chamaria isso de comparação com adversário de palha. O custo foi reescrever a seção 3.3 da [Metodologia](../artigo/03-metodologia.md) e reformular a invariante da **D-31**: a nota da C0 depende do evento, do cadastro e dos dois minutos anteriores da mesma conta — nada mais antigo, nada de outra pessoa. Verificado em teste. As duas afirmações sem fonte que a reescrita trouxe estão em [citações pendentes](citacoes-pendentes.md) | 13/10/2026 |

---

## Detalhamento — as lacunas metodológicas

D-12 a D-19 vêm de uma revisão crítica do plano feita em 06/09. Nenhuma delas
muda o texto da Introdução; **todas** mudam o que a S12 conseguirá afirmar. Por
isso vencem em M2, quando a metodologia congela.

### D-12 · Unidade de análise

A mesma detecção rende números opostos conforme a unidade escolhida. Tome o
cenário longitudinal L1 — dez dias, dezenas de eventos, nenhum acima de 50
pontos, a D3 dispara no dia 8:

```text
POR EVENTO
  Quais dos ~40 eventos são "anomalous"? Todos? Só os dos dias 8 a 10?
  C0: 0 de 40        C3: talvez 6 de 40   →   revocação ≈ 0,15
  O número parece péssimo, e o sistema fez exatamente o que devia.

POR EPISÓDIO (par usuário × cenário)
  L1 é UM episódio, detectado ou não.
  C0: 0 de 1         C3: 1 de 1           →   0,00 contra 1,00
  O número descreve o que aconteceu.
```

O falso positivo precisa do mesmo denominador: **FP por usuário-dia**, não por
evento — senão compara-se uma taxa medida em eventos com uma detecção que só
existe em janelas.

**Proposta:** duas unidades, declaradas separadamente. Evento para os cenários
pontuais; episódio ou usuário-dia para os de contexto e longitudinais. A tabela
final ganha uma coluna e para de misturar grandezas.

### D-13 · Tratamento estatístico

Hoje o desenho prevê uma semente e uma execução por configuração: quatro
números. Com isso não há como distinguir "a C3 é melhor" de "a C3 deu sorte
nesta semente".

```text
DECIDIDO: N sementes (10 a 20) × 4 configurações
          cada célula vira média ± desvio
          as MESMAS sementes nas quatro configurações → comparação pareada
          teste de Wilcoxon pareado sobre as N diferenças

CUSTO:    um laço no script da S11. Horas de CPU, não de pessoa.
GANHO:    a diferença entre "a tabela mostra" e "a diferença é
          estatisticamente significativa (p < 0,05, n = 10)".
```

A semente já é configurável no gerador e já é gravada em cada execução. Falta
usar.

#### Por que o piso é 10, e não um número escolhido a esmo

No teste de Wilcoxon pareado **exato**, o menor valor de *p* bilateral que se
consegue com *n* pares é `2 / 2ⁿ` — o caso em que todas as diferenças têm o
mesmo sinal. Daí:

| *n* pares | Menor *p* bilateral possível | Alcança p < 0,05? |
|---|---|---|
| 5 | 2/32 = 0,0625 | **Não** — nem no melhor caso |
| 6 | 2/64 ≈ 0,031 | Sim, no limite |
| 10 | 2/1024 ≈ **0,002** | Sim, com folga |
| 20 | 2/1.048.576 ≈ 0,000002 | Sim |

Com menos de 6 sementes, **nenhum resultado seria declarável significativo,
mesmo que a C3 vencesse em todas as execuções.** Dez dá folga confortável; vinte
não acrescenta poder na prática, e custa o dobro de CPU.

> A aritmética está aqui em vez de uma citação porque é derivável em duas
> linhas, e derivação verificável vale mais que fonte que ninguém abre. Se algum
> revisor discordar, o que se confere é a conta.

### D-14 · A métrica primária pode não existir para a C0

A C0 soma no máximo quatro regras discretas e não dispara em cenários
longitudinais. Se ela não alcançar revocação de 0,90 em limiar nenhum, "FPR a
revocação 0,90" não existe para o grupo de controle — e a métrica primária fica
sem par de comparação.

**Proposta:** comparar curvas precisão-revocação em vez de pontos únicos. Em
classe muito desbalanceada, que é o caso aqui, a curva PR informa mais que a
ROC.

### D-15 · Critério de relevância declarado antes

Sem dizer de antemão quanto de redução conta como sucesso, a discussão dos
resultados vira racionalização do que deu. Declarar o critério *antes* de
existir número é rigor; declará-lo depois é justificativa.

**Proposta:** uma frase na Metodologia (S5) fixando qual redução de FPR e qual
revocação longitudinal contam como resposta afirmativa.

### D-16 · Falta o controle negativo longitudinal

Os cenários preveem verdadeiros positivos longitudinais e ruído pontual, mas
**não existe cenário de escalada legítima** — alguém que muda de projeto e passa
a acessar mais coisas, mais tarde, com mais volume. Sem ele, o falso positivo da
D3 fica sem medida, e a D3 é justamente a contribuição original.

Há um problema de circularidade junto: a D3 é projetada para capturar escalada
gradual, o cenário L1 é projetado como escalada gradual, e mede-se se a D3 pega
a L1. Isso prova que a implementação funciona, não que a abordagem serve.

**Proposta:** acrescentar o cenário de escalada legítima e, se der para
organizar, desenho cego — a Yasmin especifica os cenários sem ver a fórmula da
D3. Ela já é a dona dos cenários; a separação sai de graça.

### D-17 · Vazamento no baseline da D2

Se o baseline de cada usuário for calculado sobre a mesma janela que já contém
os cenários injetados, o comportamento anômalo entra na definição do que é
normal. O resultado fica bom pelo motivo errado. A **D-24** fixou o baseline nos
**três primeiros meses** do ano simulado; o que falta é garantir que a janela de
avaliação venha depois dela.

**Proposta:** separação temporal explícita — janela de constituição do baseline
anterior e disjunta da janela de avaliação. Precisa aparecer no artigo: é
pergunta que a banca faz.

### D-18 · Dupla contagem e escala na integração

```text
exposure(u,t) = Σ (event_risk_e + behavioral_risk_e) · λ^(t−t_e)
                e ∈ [t−W, t]

O evento atual está nessa janela, com t_e = t  →  λ⁰ = 1
Logo exposure JÁ CONTÉM o risco do evento atual.

final = α·event_risk + β·behavioral_risk + γ·exposure
        └───────────┬───────────┘         └──┬──┘
           contados aqui...           ...e de novo aqui
```

Duas consequências:

1. **Pesos deixam de ser interpretáveis** — o peso efetivo do evento atual é
   α + γ, não α.
2. **Escala** — `event_risk` vai de 0 a 100; `exposure` soma até 14 dias de
   eventos, na ordem de centenas ou milhares. O termo de exposição domina o
   score final em todos os casos, inclusive nos pontuais.

**Proposta:** excluir o evento atual da janela de exposição — ela passa a ser "o
que veio antes". Normalizar `exposure` para 0–100 resolve a escala, mas não a
dupla contagem; excluir o evento resolve as duas.

### D-19 · A vertente LGPD e ISO/IEC 27001

Monitorar comportamento de colaborador é tratamento de dado pessoal. Com dados
sintéticos a LGPD não vincula o trabalho operacionalmente — mas discutir o que a
implantação real implicaria é matéria de limitações e trabalhos futuros, e é
diferencial de baixo custo perante a banca.

**Proposta:** entra na S13, apoiada na Lei 13.709/2018, no material da ANPD
sobre monitoramento no ambiente de trabalho e no controle 8.16 da ISO/IEC
27001:2022.

---

## Como registrar uma decisão nova

1. Próximo ID livre da sequência
2. Uma linha em **Abertas**, com proposta, dono e prazo
3. Quando fechar: mover para **Fechadas**, com a data e o que ficou combinado
4. Se a decisão mudar o [plano](plano.md), alterar o plano no mesmo Pull Request

Decisão que muda regra de processo, padrão ou workflow entra por Pull Request que
espera **24 h** e traz a seção `Arquivo protegido` — ver
[`AGENTS.md`](../AGENTS.md), seção 4.
