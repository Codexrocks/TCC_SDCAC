# Arquitetura

## Fluxo de dados

Unidirecional, com isolamento de responsabilidades:

```
[ Usuários simulados ] ──> [ Eventos / Logs ] ──> [ API ] ──> [ Motor de detecção ]
                                                                       │
                                    ┌──────────────────────────────────┴───────┐
                                    ▼                                          ▼
                            [ Evento normal ]                        [ Evento anômalo ]
                          (armazenado, sem alerta)                            │
                                                                              ▼
                                                                  [ Cálculo de Risk Score ]
                                                                              │
                                                                              ▼
                                                                     [ Disparo de alerta ]
                                                                              │
                                                                              ▼
                                                                 [ Dashboard de monitoramento ]
```

## Regras de detecção

Pontos cumulativos por evento:

| # | Regra | Condição | Pontos |
|---|---|---|---|
| 1 | Horário atípico | `horario < 06:00` ou `horario > 22:00` | +30 |
| 2 | Força bruta / volumetria | `tentativas_falhas > 10` em 2 min | +40 |
| 3 | Anomalia de origem | `ip_origem != ip_habitual_usuario` | +30 |
| 4 | Recurso incomum | `acesso_sensivel == TRUE` | +25 a +40 |

## Faixas de Risk Score

| Pontuação | Classificação | Comportamento do sistema |
|---|---|---|
| 0–20 | **NORMAL** | Evento armazenado. Sem alerta. |
| 21–50 | **RISCO BAIXO** | Registro preventivo, indicação azul no painel. |
| 51–75 | **RISCO MÉDIO** | Alerta amarelo no dashboard. |
| 76–100 | **RISCO ALTO** | Alerta crítico vermelho, notificação imediata. |

## Cenários de teste

| # | Comportamento | Gatilhos | Score esperado | Resultado esperado |
|---|---|---|---|---|
| 1 | Maria loga às 08:10 via IP habitual | nenhum | 0–20 | Verdadeiro negativo |
| 2 | Maria acessa às 03:17 via IP habitual | horário (+30) | 30 | Verdadeiro positivo (baixo/médio) |
| 3 | João erra 15 logins em 2 min | falhas (+40) + IP (+30) | 70–85 | Verdadeiro positivo (alto) |
| 4 | Carlos acessa de IP externo | IP não habitual (+30) | 30–60 | Verdadeiro positivo (suspeito) |
| 5 | Leitura massiva de diretório restrito | acesso atípico (+35) | 55–70 | Verdadeiro positivo (suspeito) |
| 6 | Conta comum tenta alterar permissões | privilégio (+40) + horário (+30) | 80–95 | Verdadeiro positivo (alto) |

## Métricas de avaliação

```
Taxa de detecção (Recall)  =  VP / (VP + FN)
Taxa de falsos positivos   =  FP / (FP + VN)
MTTD                       =  tempo_disparo_alerta − tempo_registro_log
```

## Estrutura planejada do código

Ainda não criada — entra a partir da **S6 (02/10)**, quando o desenvolvimento começa.
Registrada aqui para não haver divergência depois:

```
TCC_SDCAC/
├── backend/          api/ · models/ · services/ · main.py
├── detection/        rules/ · anomaly_detection/ · risk_score/
├── frontend/         dashboard/ · components/
├── database/         schema.sql · seed.sql
├── data/             normal/ · anomalous/
├── tests/            scenario_01/ ... scenario_06/
├── results/          graphs/ · tables/
└── docs/             ← documentação (GitBook)
```

Tabelas do banco: `users` · `events` · `alerts` · `risk_scores`
