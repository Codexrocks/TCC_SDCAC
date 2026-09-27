# Arquitetura

> **Versão 2 — o modelo de três dimensões.** A versão anterior desta página
> descrevia o detector de uma dimensão do plano v1: quatro regras fixas, um Risk
> Score só e seis cenários pontuais. O [plano v2](plano.md) substituiu esse
> modelo por um **estudo comparativo**, e esta página foi refeita na **S5** para
> acompanhá-lo. O que sobrou da v1 está marcado como herança, no fim.

Esta página descreve **como o sistema é construído**. O que ele é e o que ele
responde está no [plano](plano.md); os dados sobre os quais ele roda, na
[especificação do banco](banco-simulado.md).

## O que muda em relação à v1

| | v1 | v2 |
|---|---|---|
| O que o sistema é | Um detector | **Quatro configurações do mesmo código** |
| O que se mede | Se o detector funciona | **Quanto cada dimensão acrescenta** |
| Linha de base | Não existia | **C0**, grupo de controle, puramente estática |
| Score | Um número | **Decomponível por dimensão**, e a D3 reporta duas parcelas separadas |

---

## Fluxo de dados

Unidirecional, com isolamento de responsabilidades. O rótulo do que é ataque
**não passa** pelo caminho da aplicação:

```text
[ Gerador de eventos ] ──> [ corp ] ──> [ API ] ──> [ Motor, em C0..C3 ]
   (semente, run_id)       (sem rótulo)                      │
          │                                                  ▼
          │                                       [ Score decomponível ]
          │                                         D1 · D2 · D3a · D3b
          │                                                  │
          │                                   ┌──────────────┴──────────────┐
          │                                   ▼                             ▼
          │                          [ sdcac: notas,              [ Dashboard, com o
          │                            alertas, métricas ]         risco por dimensão ]
          ▼
[ ground_truth: episódios e rótulos ] ──> [ Cálculo das métricas ]
```

**A separação dos três bancos é trava, não organização.** O usuário da aplicação
não recebe permissão de conectar em `ground_truth`; é o equivalente estrutural da
**D-17**, e está detalhado na [especificação do banco](banco-simulado.md),
seção 8.

---

## As quatro configurações

```text
C0 ──────► C1 ──────► C2 ──────► C3
regras     + risco    + desvio    + exposição
fixas      do evento  do usuário  acumulada
(controle) (D1)       (D1+D2)     (D1+D2+D3)
```

Cada configuração é uma **flag de execução no mesmo código**, não quatro
sistemas. É o que garante que a única variável entre as linhas da tabela de
ablação seja a dimensão acrescentada. Decisões **D-05** e **D-26**.

| Configuração | O que liga | Papel |
|---|---|---|
| **C0** | Regras fixas sobre o evento isolado, **sem nenhum histórico do funcionário** | Grupo de controle |
| **C1** | D1 | Ganho de atributos mais ricos sobre a mesma lógica pontual |
| **C2** | D1 + D2 | Ganho de contexto individual |
| **C3** | D1 + D2 + D3 | A contribuição original do trabalho |

### C0 — a linha de base precisa ser estática

As quatro regras da v1 não servem como grupo de controle sem correção. **Duas
delas usavam histórico do funcionário** — o "IP habitual" e a janela de falhas —
e histórico é justamente o que as dimensões 2 e 3 acrescentam. Usá-lo na C0
contamina o controle. É a pergunta **P30**, aberta pela **D-26**.

| # | Regra da C0 | Condição, só com configuração estática |
|---|---|---|
| 1 | Horário fora do expediente | `occurred_at` fora de 06:00–22:00 |
| 2 | Volume de falhas | `result` de falha acima de **limite fixo**, em janela fixa |
| 3 | Origem fora da rede corporativa | `ip_address` fora das faixas de `network_ranges` |
| 4 | Recurso sensível | `sensitivity` em nível restrito |

> **Nenhuma das quatro consulta o passado da pessoa.** Os pesos preliminares são
> da **D-09**, e a análise de sensibilidade sobre eles é da S12.

---

## As três dimensões

O que cada dimensão lê de cada atributo está na matriz da
[especificação do banco](banco-simulado.md), seção 7. O resumo:

| | O que pergunta | Janela | Unidade |
|---|---|---|---|
| **D1** Risco do evento | Este evento, isolado, é arriscado? | O próprio evento | Evento |
| **D2** Desvio do padrão | Este conjunto destoa do que **esta pessoa** costuma fazer? | Padrão dos **três primeiros meses** (**D-24**) | Sessão ou usuário-dia (**P25**) |
| **D3** Exposição acumulada | O risco vem **crescendo** ao longo de dias, sem que nenhum evento isolado dispare? | Janela deslizante, com decaimento | Episódio (**D-12**) |

### A D3 reporta duas parcelas, nunca somadas

A **D-25** fechou o que a dimensão 3 é: **exposição acumulada e higiene de
segurança**, com **as duas parcelas reportadas separadas**.

| Parcela | O que mede |
|---|---|
| **D3a — conduta** | Recorrência, combinação e evolução temporal dos comportamentos |
| **D3b — postura** | Higiene de segurança: MFA, privilégio, atualização de dispositivo e resultado da campanha de phishing (**P28**) |

Somar as duas num número só exigiria um peso entre "o que a pessoa fez" e "como
a conta dela está configurada" — peso que ninguém consegue justificar perante a
banca. Separadas, atendem também à regra de **risco decomponível** da
[usabilidade](usabilidade.md).

---

## Integração — e as duas armadilhas conhecidas

```text
final = α·D1 + β·D2 + γ·D3
```

A exposição é uma soma com decaimento sobre a janela:

```text
exposure(u,t) = Σ (event_risk_e + behavioral_risk_e) · λ^(t−t_e)
                e ∈ [t−W, t)
```

Repare no intervalo **aberto à direita**: o evento atual fica **fora** da janela
de exposição. É a decisão **D-18**, e ela trata duas coisas de uma vez:

| Armadilha | O que acontecia | O que a D-18 fez |
|---|---|---|
| **Dupla contagem** | Com o evento atual dentro da janela (`λ⁰ = 1`), o peso efetivo dele virava `α + γ`, não `α` — e os pesos deixavam de ser interpretáveis | Excluir o evento atual: a exposição passa a ser "o que veio antes" |
| **Escala** | `event_risk` vai de 0 a 100; a exposição soma até 14 dias e chega à ordem de centenas. O termo dominava o score em todos os casos | A exclusão resolve a dupla contagem; **normalizar a exposição para 0–100** resolve a escala |

> **O baseline da D2 vem de janela anterior e disjunta da janela de avaliação**
> (**D-17**). Sem isso, o comportamento anômalo entra na definição do que é
> normal, e o resultado fica bom pelo motivo errado.

---

## Faixas do score final

| Pontuação | Classificação | Comportamento do sistema |
|---|---|---|
| 0–20 | **NORMAL** | Evento armazenado. Sem alerta |
| 21–50 | **RISCO BAIXO** | Registro preventivo, indicação azul no painel |
| 51–75 | **RISCO MÉDIO** | Alerta amarelo no dashboard |
| 76–100 | **RISCO ALTO** | Alerta crítico vermelho, notificação imediata |

> **A faixa nunca aparece sozinha.** A [usabilidade](usabilidade.md) exige
> rótulo textual junto da cor e a **decomposição do risco visível** — quanto veio
> da D1, da D2, da D3a e da D3b. Um número só, sem decomposição, não passa no
> critério de aceite da S9.

---

## Métricas de avaliação

As grandezas são as da [pergunta de pesquisa](plano.md), pela decisão **D-03**:

| Grandeza | Métrica | Unidade de análise (**D-12**) |
|---|---|---|
| **Ruído** | Taxa de falsos positivos, **com a revocação fixada no mesmo nível** nas quatro configurações | FP por **usuário-dia** |
| **Cobertura** | Revocação nos **cenários longitudinais** | **Episódio** — par usuário × cenário |
| Secundária | Precisão@k sobre a fila de alertas | Evento |

Duas ressalvas que mudam o que a tabela final pode afirmar:

- **A métrica primária pode não existir para a C0** (**D-14**). Se ela não
  alcançar revocação 0,90 em limiar nenhum, comparam-se **curvas
  precisão-revocação**, não pontos únicos
- **Uma execução por configuração não distingue "a C3 é melhor" de "a C3 deu
  sorte nesta semente"** (**D-13**). São **10 a 20 sementes**, as mesmas nas
  quatro configurações, com **Wilcoxon pareado** sobre as diferenças

---

## Cenários de teste

O desenho dos cenários é da **Yasmin**, na S5, e cobre quatro famílias:
pontuais, de contexto, longitudinais e de **escalada legítima** — decisões
**D-06** e **D-16**. A última é o controle negativo: sem ela, o falso positivo da
D3 fica sem medida, e a D3 é a contribuição original.

> **Desenho cego, se der para organizar.** A Yasmin especifica os cenários **sem
> ver a fórmula da D3**. Senão a D3 é projetada para capturar escalada gradual, o
> cenário é projetado como escalada gradual, e mede-se se uma pega a outra — o
> que prova que a implementação funciona, não que a abordagem serve.

### Herança da v1 — a refazer na S5

Os seis cenários pontuais abaixo vêm da versão anterior desta página. **Os
scores esperados foram calculados com as quatro regras da v1**, duas das quais
usavam histórico e saíram da C0. Ficam como ponto de partida do desenho da S5,
não como expectativa a conferir:

| # | Comportamento | Gatilhos da v1 | Score esperado na v1 |
|---|---|---|---|
| 1 | Maria loga às 08:10 via IP habitual | nenhum | 0–20 |
| 2 | Maria acessa às 03:17 via IP habitual | horário (+30) | 30 |
| 3 | João erra 15 logins em 2 min | falhas (+40) + IP (+30) | 70–85 |
| 4 | Carlos acessa de IP externo | IP não habitual (+30) | 30–60 |
| 5 | Leitura massiva de diretório restrito | acesso atípico (+35) | 55–70 |
| 6 | Conta comum tenta alterar permissões | privilégio (+40) + horário (+30) | 80–95 |

---

## Estrutura planejada do código

Ainda não criada — entra a partir da **S6 (02/10)**, quando o desenvolvimento
começa. Registrada aqui para não haver divergência depois:

```text
TCC_SDCAC/
├── backend/          api/ · models/ · services/ · main.py
├── detection/        c0/ · d1/ · d2/ · d3/ · integracao/   ← a flag C0..C3 mora aqui
├── generator/        personas/ · calendario/ · cenarios/   ← a peça da S6
├── frontend/         dashboard/ · components/
├── database/         corp/ · ground_truth/ · sdcac/ — schema e migrações
├── data/             sementes geradas, por run_id
├── results/          graphs/ · tables/ — de onde sai todo número do artigo
│
├── artigo/           ← o artigo (o GitBook escreve aqui)
├── docs/             ← documentação (o GitBook só lê)
├── scripts/          ← os verificadores do repositório
├── templates/        ← modelos de entrega do artigo
└── tests/            ← hoje, os testes dos verificadores; na S6, também os do sistema
```

> **`tests/` já existe** e guarda os testes de `scripts/`. Os testes dos cenários
> entram ao lado deles, não no lugar.

**Os três bancos** — `corp`, `ground_truth` e `sdcac` — e todas as tabelas estão
na [especificação do banco](banco-simulado.md), que é a fonte para o schema da
S6. Esta página não repete a lista: **duas listas de tabelas em dois arquivos
viram dois schemas diferentes na primeira alteração.**
