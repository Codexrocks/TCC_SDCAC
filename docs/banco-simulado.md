# Banco da corporação simulada

Especificação do que o gerador de logs precisa produzir: quais eventos existem,
com quais atributos, em que tabelas, e o que cada atributo serve para medir.

É o insumo da **S6** e a base da seção de Metodologia que descreve o ambiente
experimental. **O código começa depois da aprovação desta página.**

| | |
|---|---|
| Versão | 23/09/2026 — incorpora as decisões D-23 a D-26 |
| Escala | 250 funcionários · 1 ano simulado · 1,15 a 2,9 milhões de eventos por semente |
| Substitui | `atributos.docx` e as versões anteriores em `.docx`, que não estavam versionadas |

## Quem faz

| Frente | Quem |
|---|---|
| **Gerador de eventos** — personas, calendário, rotina, ruído legítimo | **Filipe** |
| Schema, migrações, carga e ingestão | Davi |
| Cenários e rótulos — a injeção sobre o tráfego normal | Yasmin, pelas [D-06 e D-16](decisoes.md) |

O gerador é a peça de maior superfície desta página: as seções 3, 5 e 10 são o
contrato do que ele precisa produzir, e as checagens da seção 9 são os testes que
ele precisa passar.

> **O que está fechado e o que não está.** As cinco decisões de fundo — volume,
> dimensões, linha de base e sementes — estão em [decisões](decisoes.md), de
> **D-23 a D-26**. Restam **26 definições abertas**, listadas no fim desta
> página. Nenhuma delas impede escrever a especificação; várias impedem rodar o
> gerador.

***

## 1. As cinco decisões que moldam esta página

| Decisão | O que ficou | Consequência aqui |
|---|---|---|
| **D-23** | 20 a 50 eventos **por dia útil**, faixa média, diferente por persona | Vira restrição das personas: a média ponderada precisa cair entre 20 e 50 |
| **D-24** | A **dimensão 2** compara o funcionário com o próprio padrão de 3 meses | Exige a tabela `baselines` (seção 5) |
| **D-25** | A **dimensão 3** combina exposição acumulada **e** higiene de segurança, com as duas parcelas reportadas separadas | Entra o evento `PHISHING_SIM` e entram as duas tabelas de estado (seção 4) |
| **D-26** | A **linha de base continua separada**: quatro configurações, C0 a C3 | A matriz da seção 7 ganha a coluna C0, e nada nela pode usar histórico |
| **D-13** (alterada) | De 20 a 30 sementes para **10 a 20** | `run_id` passa a ser obrigatório no envelope |

> **Por que a D-26 importa mais do que parece.** Se a linha de base virasse a
> dimensão 1, nenhuma dimensão compararia o funcionário com ele mesmo — e a
> pergunta de pesquisa publicada, que fala em *"desvio comportamental do
> usuário"*, ficaria sem como ser respondida. A decisão preserva a pergunta.

## 2. O envelope: a tabela principal de eventos

| Campo | Tipo | O que é | Obrigatório |
|---|---|---|---|
| `run_id` | `int` | Execução e semente que geraram o evento | Sim |
| `event_id` | `uuid` | Chave primária, determinística a partir da semente | Sim |
| `employee_id` | `int` | Quem fez | Sim |
| `occurred_at` | `timestamptz` | Quando aconteceu, gravado em UTC | Sim |
| `ingested_at` | `timestamptz` | Quando o sistema recebeu. Latência de engenharia, **nunca métrica do TCC** | Sim |
| `event_type` | `enum` | Um dos oito tipos da seção 3 | Sim |
| `result` | `enum` | `success` · `failure` · `blocked` | Sim |
| `ip_address` | `inet` | Origem, sempre dentro de uma faixa de `network_ranges` | Sim |
| `device_id` | `int` | Máquina usada | Sim |
| `session_id` | `uuid` | Sessão de trabalho. É o recorte natural da dimensão 2 | Sim |
| `resource_id` | `int` | Arquivo ou sistema acessado. Traz a classificação de sigilo | Quando houver recurso |
| `is_vpn` | `bool` | A sessão veio por VPN | Sim |
| `attributes` | `jsonb` | Os atributos do tipo, conforme a seção 3 | Sim |

**Quatro regras da tabela:**

- **Índice** `(run_id, employee_id, occurred_at)` — é o formato de toda janela das dimensões 2 e 3
- **Partição por `run_id`** — descartar uma semente vira operação instantânea
- **Só inserção.** A tabela não aceita `UPDATE` nem `DELETE`, por privilégio de banco. Log é evidência
- **Nenhum rótulo aqui.** O gabarito mora em outro banco (seção 8)

## 3. Os oito tipos de evento

Atributo que já está no envelope não se repete no `jsonb`.

| Tipo | Atributo | Valores | Serve para |
|---|---|---|---|
| **LOGIN** | `mfa_used` | `true` · `false` | Login sem segundo fator (D1) e fração sem MFA (D3) |
| | `failure_reason` | `wrong_password` · `user_locked` · `mfa_failed` · `unknown_user` | Separar erro humano de ataque |
| **LOGOUT** | `reason` | `user` · `timeout` · `forced` | A duração da sessão é insumo da D2 |
| **FILE_ACCESS** | `action` | `view` · `edit` | Distinguir leitura de alteração |
| **FILE_DOWNLOAD** | `size_bytes` | Inteiro > 0 | Volume (D1) e soma por janela (D2 e D3) |
| | `destination` | `local_disk` · `external_storage` · `removable` | Para onde o arquivo foi |
| **EXTERNAL_DEVICE** | `device_type` | `usb_pendrive` · `external_hd` · `phone` | O que foi conectado |
| | `files_copied_count` | Inteiro ≥ 0 | Zero significa que só plugou |
| | `bytes_copied` | Inteiro, opcional | Mesma unidade do download |
| **WEB_BROWSING** | `domain` | Domínios `.example` de catálogo fictício | Destino, sem citar organização real |
| | `category` | `corporate` · `cloud_storage` · `social_media` · `webmail` · `uncategorized` | Categoria de risco |
| **SYSTEM_CONFIG** | `action_subtype` | `password_change` · `privilege_escalation` · `mfa_disabled` · `permission_grant` | O que foi feito na conta |
| | `initiated_by` | `self` · `admin` | Quem mandou fazer |
| | `target_employee_id` | Inteiro, opcional | Administrador mexendo em conta alheia |
| **PHISHING_SIM** | *(a definir na P28)* | — | Entra pela D-25. Campanha simulada: clicou, reportou ou ignorou |

> **`sensitivity` não entra no `jsonb`.** Ela é atributo do **recurso**, e precisa
> valer igual em todo tipo de evento. Na versão original ela só existia no
> `FILE_ACCESS` — e sumia justamente no `FILE_DOWNLOAD`, que é o evento de
> vazamento.

> **A navegação é justificada por segurança, não por produtividade.** Interessam
> armazenamento em nuvem, webmail e categorias de risco, porque são canais de
> saída de dado. A [delimitação do plano](plano.md) proíbe monitorar navegação
> para fim de produtividade.

## 4. Estado, não evento

Parte da higiene de segurança **não é evento: é condição que dura**. Virar evento
diário inflaria o volume sem acrescentar informação.

| Tabela | Colunas essenciais | Tamanho |
|---|---|---|
| `device_state_daily` | `run_id`, `device_id`, data, `patch_age_days`, antivírus ativo | ~250 dispositivos × 365 dias por semente |
| `account_state` | `run_id`, `employee_id`, início, fim, `mfa_enabled`, nível de privilégio | Muda só quando acontece um `SYSTEM_CONFIG` |

> **Estado tem data de validade.** As duas precisam ser lidas *"como estavam
> naquele dia"*, nunca no estado final. Ler o estado final é a mesma falha da
> **D-17** por outro caminho: o resultado fica bom porque o futuro vazou para o
> passado.

## 5. O padrão do funcionário

A dimensão 2 compara um conjunto de eventos com o padrão individual dos três
primeiros meses. Isso exige uma tabela `baselines`, com estas características por
funcionário:

| Característica | Como se mede | Divergência que revela |
|---|---|---|
| Volume diário | Média e dispersão de eventos por dia útil | Dia muito acima do próprio hábito |
| Faixa horária | Distribuição das horas de trabalho | Atividade fora do horário **daquela pessoa** |
| Recursos habituais | Conjunto de sistemas e pastas acessados | Acesso a área que a pessoa nunca tocou |
| Mistura de sigilo | Proporção de acesso por nível de sensibilidade | Subida repentina de acesso a restrito |
| Origem e dispositivo | Faixas de rede e máquinas habituais | Origem nova, sem ser viagem declarada |
| Taxa de falha | Falhas de autenticação por dia | Erro humano contra tentativa de invasão |
| Conduta de higiene | Campanhas e uso de dispositivo removível | Insumo da D3, junto do estado da seção 4 |

> **O cuidado técnico que decide se a D2 funciona.** Funcionário muito regular
> tem dispersão quase zero no padrão, e qualquer desvio vira um número enorme. A
> comparação precisa de um **piso de dispersão declarado** — senão a dimensão 2
> alarma justamente sobre as pessoas mais previsíveis. É a **P27**.

## 6. Tabelas de apoio

O catálogo de eventos só funciona se estas existirem junto:

| Tabela | Colunas essenciais | Por que existe |
|---|---|---|
| `employees` | Departamento, cargo, gestor, persona, privilégio, sede, **fuso horário**, admissão | O fuso é o que torna possível a regra de horário atípico |
| `resources` | Tipo, nome fictício, `sensitivity`, departamento dono | Dá sigilo a todo evento e viabiliza a matriz cargo × sistema |
| `devices` | Dono, tipo, corporativo ou pessoal | Identifica a máquina do evento |
| `network_ranges` | Faixa `cidr`, tipo, país e cidade fictícios | Origem e localização sem serviço externo de GeoIP |
| `sessions` | Funcionário, início, fim, `is_vpn`, dispositivo | Duração e recorte da dimensão 2 |
| `hr_calendar` | Férias, afastamento, mudança de cargo | Ruído legítimo |

### Listas fechadas

Tudo em inglês e minúsculo, conforme [padrões de código](padroes-codigo.md). Cada
lista vira restrição no banco, e cada tipo ganha validação do `jsonb`, conferida
em teste.

| Campo | Valores |
|---|---|
| `event_type` | `LOGIN` · `LOGOUT` · `FILE_ACCESS` · `FILE_DOWNLOAD` · `EXTERNAL_DEVICE` · `WEB_BROWSING` · `SYSTEM_CONFIG` · `PHISHING_SIM` |
| `result` | `success` · `failure` · `blocked` |
| `sensitivity` | `public` · `internal` · `confidential` · `restricted` |
| Tipo de faixa de rede | `office` · `vpn` · `home` · `external` |

## 7. Matriz atributo → configuração e dimensão

**É esta tabela que prova que o catálogo está completo.** Linha vazia é atributo
sem uso; regra que se queira e não esteja aqui precisa de atributo novo.

O que está na **C0 não pode depender do histórico do funcionário** — é o que
define o grupo de controle.

| Atributo | C0 linha de base | D1 evento | D2 conjunto | D3 exposição |
|---|---|---|---|---|
| `occurred_at` com fuso | Horário fixo, fora de 6h–22h | Horário com peso por faixa | Horário vs. o padrão da pessoa | — |
| `result` + `failure_reason` | Falhas acima de limite fixo | Motivo da falha com peso | Falhas acima do hábito | Recorrência de falhas |
| `ip_address` | Fora das faixas corporativas | Origem com peso por tipo | Origem nova para a pessoa | Tempo fora da rede |
| `is_vpn` | — | Acesso externo sem VPN | — | Fração de acesso sem VPN |
| `mfa_used` | — | Login sem segundo fator | — | Fração de logins sem MFA |
| `sensitivity` | Acesso a restrito | Peso por nível | Mistura de sigilo fora do padrão | Contato acumulado com dado sensível |
| `size_bytes` + `destination` | — | Download grande | Volume acima do hábito | Volume acumulado para fora |
| `device_type`, `files_copied_count` | — | Uso de dispositivo removível | USB logo após download | Recorrência de cópia física |
| `domain` + `category` | — | Categoria de risco | Navegação e download juntos | Exposição acumulada a categorias |
| `action_subtype` | — | Escalada de privilégio | Escalada seguida de acesso novo | Privilégio acumulado |
| `session_id` | — | — | Recorte do conjunto | Duração e frequência das sessões |

> **A P30, que a D-26 abriu.** Duas das quatro regras da linha de base original
> usavam histórico — *"IP habitual"* e a janela de falhas. Isso **contamina o
> grupo de controle**. A C0 precisa ser puramente estática: horário fixo, faixas
> corporativas cadastradas, limite fixo de falhas.

## 8. Três bancos, não um

| Banco | O que guarda | Quem lê |
|---|---|---|
| `corp` | Eventos, **sem rótulo** | A aplicação |
| `ground_truth` | Episódios e rótulos | Só as métricas |
| `sdcac` | Padrões, notas, alertas e métricas | A aplicação |

**O usuário da aplicação não recebe permissão de conectar em `ground_truth`.** É
a trava contra vazamento de rótulo — o equivalente estrutural da **D-17**.

## 9. Checagens automáticas

Viram teste do gerador e falham **antes** de qualquer dado entrar no banco:

- Todo evento aponta para uma sessão existente, do mesmo funcionário
- Nenhuma ação depois do `LOGOUT` da própria sessão
- `sensitivity` nunca aparece dentro do `jsonb`
- Todo campo de lista fechada tem valor da lista
- Todo domínio termina em `.example`
- Todo IP cai dentro de uma faixa declarada em `network_ranges`
- `size_bytes` maior que zero em todo `FILE_DOWNLOAD`

> **Por que `.example` e faixas reservadas.** A versão original usava domínios de
> organizações reais e só faixas privadas. O repositório é **público**: citar
> organização real num log sintético de segurança é problema. E sem faixa externa
> não existe acesso de casa, viagem, atacante nem regra de origem.

***

## 10. O que ainda falta decidir

**Sete abertas pelas decisões D-23 a D-26**, e são as que o gerador encontra
primeiro:

| # | Pergunta | Recomendação |
|---|---|---|
| P24 | O que é "dia útil" por persona, e o que acontece em feriado e férias? | Calendário por persona; férias sem atividade, salvo cenário |
| P25 | Qual é a janela da dimensão 2: sessão, dia ou semana? | Começar por duas — sessão e usuário-dia — e declarar qual vale por cenário |
| P26 | Quais características entram no padrão? | As sete da seção 5 |
| P27 | Como a divergência é medida, e qual o piso de dispersão? | Desvio vs. a própria distribuição, com piso declarado |
| P28 | O que entra no "básico" da higiene? | Phishing como evento; MFA e privilégio como estado de conta; atualização como estado de dispositivo. Alerta de antivírus fica fora |
| P29 | A D3 reporta conduta e postura separadas? | Sim, duas parcelas visíveis, não um número só |
| P30 | O que a C0 tem que a D1 não tem? | C0 só com configuração estática. Nada de histórico |
| P31 | 10 ou 20 sementes? | Medir a primeira execução completa e decidir pelo tempo |

**Dezenove que já estavam abertas:**

| Grupo | Perguntas | O que trava |
|---|---|---|
| A empresa | P06 a P10 | Departamentos, personas e a **matriz cargo × sistema** — sem ela, "acesso incomum" não tem definição |
| O ambiente | P11 a P13 | Lista de sistemas com sigilo, faixas de rede, calendário do ano simulado |
| Os eventos | P14, P15, P17 | Proporção por persona e a **taxa normal de senha errada** — sem ela a força bruta só enxerga ataque, nunca erro de digitação |
| Os cenários | P18 a P23 | Vencem em **01/10** pelas decisões [D-06](decisoes.md) e [D-16](decisoes.md) |

## 11. O que pode esperar

| Assunto | Por quê |
|---|---|
| Unidade de análise (**D-12**) | O gabarito guarda evento **e** episódio: dá para decidir depois |
| Padrão congelado ou que se atualiza | Decisão da aplicação. O gerador só precisa produzir mudanças legítimas |
| Se a aplicação pode ler férias e mudança de cargo | Fica em tabela separada; o acesso vira opção do experimento |
| Pesos, limites e faixas de nota | Decisões da aplicação, não do gerador |

***

## Procedência

Esta página consolida dois documentos preparados com assistência do **Claude
Opus 5**, em 23/09/2026: *Banco da corporação simulada — versão 3* e *Catálogo de
eventos e atributos — versão 2*. Eles substituíram um `atributos.docx` que não
estava versionado.

Nenhum número aqui é estatística do mundo real: **250 funcionários, 20 a 50
eventos por dia útil e um ano simulado são parâmetros declarados da simulação**.
Nenhum deles vai ao artigo como dado empírico — a distinção precisa aparecer na
Metodologia.
