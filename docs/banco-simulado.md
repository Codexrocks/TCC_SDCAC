# Banco da corporação simulada

Especificação do que o gerador de logs precisa produzir: quais eventos existem,
com quais atributos, em que tabelas, e o que cada atributo serve para medir.

É o insumo da **S6** e a base da seção de Metodologia que descreve o ambiente
experimental. **O código começa depois da aprovação desta página.**

| | |
|---|---|
| Versão | 28/09/2026 — incorpora as decisões D-23 a D-31 |
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

> **O que está fechado e o que não está.** As decisões de fundo — volume,
> dimensões, linha de base, sementes, calendário, janelas da D2, forma do desvio
> e escopo da higiene — estão em [decisões](decisoes.md), de **D-23 a D-31**.
> Restam **dez definições abertas**, listadas no fim desta página, com o
> responsável de cada grupo. Nenhuma delas impede escrever a especificação; várias impedem rodar o
> gerador.

***

## 1. As decisões que moldam esta página

| Decisão | O que ficou | Consequência aqui |
|---|---|---|
| **D-23** | 20 a 50 eventos **por dia útil**, faixa média, diferente por persona | Vira restrição das personas: a média ponderada precisa cair entre 20 e 50 |
| **D-24** | A **dimensão 2** compara o funcionário com o próprio padrão de 3 meses | Exige a tabela `baselines` (seção 5) |
| **D-25** | A **dimensão 3** combina exposição acumulada **e** higiene de segurança, com as duas parcelas reportadas separadas | Entra o evento `PHISHING_SIM` e entram as duas tabelas de estado (seção 4) |
| **D-26** | A **linha de base continua separada**: quatro configurações, C0 a C3 | A matriz da seção 7 ganha a coluna C0, e nada nela pode usar histórico |
| **D-13** (alterada) | De 20 a 30 sementes para **10 a 20**, com a regra de corte pelo tempo do ciclo | `run_id` passa a ser obrigatório no envelope |
| **D-27** | Calendário **por persona**; feriado e férias com atividade residual declarada | Seção 10: é regra, e só vira parâmetro quando as personas existirem (P07) |
| **D-28** | A D2 tem duas janelas: **sessão** e **usuário-dia**. Semana não | Seção 5. Se a D2 olhasse a semana, ela e a D3 mediriam a mesma coisa |
| **D-29** | Padrão com **mediana e MAD**; desvio robusto com piso, teto e grupo de pares | Seção 5, que deixa de ser lista de características e passa a ser contrato |
| **D-30** | Higiene em **cinco sinais**, antivírus fora; D3 em duas parcelas, conduta e postura | Seção 4 |
| **D-31** | A **C0 é puramente estática**, e a D1 é pontuação ponderada sobre o evento | Seção 7, e é o critério de aceite da S7 |

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
| **SYSTEM_CONFIG** | `action_subtype` | `password_change` · `privilege_escalation` · `mfa_disabled` · `mfa_enabled` · `permission_grant` | O que foi feito na conta. É o evento que muda o `account_state` da seção 4 |
| | `initiated_by` | `self` · `admin` | Quem mandou fazer |
| | `target_employee_id` | Inteiro, opcional | Administrador mexendo em conta alheia |
| **PHISHING_SIM** | `campaign_id` | Identificador da campanha simulada | Agrupar a simulação. Uma campanha por mês basta |
| | `outcome` | `reported` · `ignored` · `clicked` · `submitted_credentials` | Conduta do funcionário, **do melhor ao pior caso, nesta ordem**. Entra pela D-25 |

> **`sensitivity` não entra no `jsonb`.** Ela é atributo do **recurso**, e precisa
> valer igual em todo tipo de evento. Na versão original ela só existia no
> `FILE_ACCESS` — e sumia justamente no `FILE_DOWNLOAD`, que é o evento de
> vazamento.

> **O MFA precisa de caminho de volta.** O `account_state` da seção 4 guarda
> `mfa_enabled`, que muda nos dois sentidos. Se o `SYSTEM_CONFIG` só soubesse
> desligar, o estado seria de mão única: uma vez desligado, nunca mais religa, e
> a parcela de postura da D3 nunca voltaria a melhorar. Por isso os dois
> subtipos existem.

> **Os atributos do `PHISHING_SIM` não dependem da P28.** A P28 pergunta *quais
> itens de higiene entram no básico* — se o phishing entra como evento, se MFA e
> privilégio ficam como estado, se o alerta de antivírus fica de fora. Os
> atributos do evento são outra coisa, e estão fechados acima.
>
> Se a D3 vier a transformar o desfecho em número, **a ordem da lista é a fonte
> da verdade**: do melhor ao pior caso. Reportar é melhor que ignorar — quem
> reporta identificou o ataque e agiu. A escala entra com a **P29**.

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

### O básico da higiene são cinco sinais (D-30)

| Sinal | De onde vem |
|---|---|
| Desfecho de campanha de phishing | Evento `PHISHING_SIM`, uma campanha por mês |
| Segundo fator e nível de privilégio | `account_state` |
| Atualização do equipamento e antivírus ativo | `device_state_daily` |
| Uso de dispositivo removível | Evento `EXTERNAL_DEVICE`, que já existe |
| Navegação de categoria de risco | Evento `WEB_BROWSING`, que já existe |

**O alerta de antivírus fica de fora.** Ele exigiria modelar a detecção do
próprio antivírus — uma segunda ferramenta dentro da simulação — e a informação
que importa para a postura, se o equipamento está protegido, já está no estado
diário. Custo alto, informação repetida. Assim, o "básico das duas" da **D-25**
não acrescenta nenhum tipo de evento além do `PHISHING_SIM`.

### As duas parcelas da dimensão 3 (D-30)

| Parcela | O que mede | Dinâmica |
|---|---|---|
| **Conduta** | Exposição acumulada pelo que a pessoa fez | Janela deslizante com decaimento, **excluindo o evento atual** (D-18) |
| **Postura** | Estado de conta e equipamento na data do evento | Persiste até alguém mudar; lida como estava naquele dia |

As duas normalizadas de 0 a 100 e mostradas lado a lado, com pesos declarados.
Somá-las antes de exibir esconderia qual das duas causou o alerta — e risco
decomponível é exigência da [usabilidade](usabilidade.md), não preferência.

## 5. O padrão do funcionário

A dimensão 2 compara um conjunto de eventos com o padrão individual dos três
primeiros meses. Isso exige uma tabela `baselines`, com estas características por
funcionário:

| Característica | O que o baseline guarda | Divergência que revela |
|---|---|---|
| Volume diário | **Mediana e MAD** de eventos por dia útil | Dia muito acima do próprio hábito |
| Faixa horária | Histograma de 24 posições, com hora mediana de início e fim | Atividade fora do horário **daquela pessoa** |
| Recursos habituais | Conjunto de `resource_id`, com frequência | Acesso a área que a pessoa nunca tocou |
| Mistura de sigilo | Proporção de eventos por nível de sensibilidade | Subida repentina de acesso a restrito |
| Origem e dispositivo | Faixas de rede e `device_id` habituais, com frequência | Origem nova, sem ser viagem declarada |
| Taxa de falha | Mediana e MAD de falhas de autenticação por dia | Erro humano contra tentativa de invasão |
| Conduta de higiene | Desfechos de campanha e uso de dispositivo removível | Insumo da D3, junto do estado da seção 4 |

> **Mediana e MAD, não média e desvio padrão (D-29).** Um único dia de pico
> dentro da janela de treino infla o desvio padrão e mascara divergência real
> pelos nove meses seguintes. Mediana e MAD não se mexem com um ponto extremo.

### As duas janelas da dimensão 2 (D-28)

| Janela | O que captura |
|---|---|
| **Sessão** | "Esta sessão está estranha": volume, horário, origem e sequência dentro do mesmo login |
| **Usuário-dia** | O que atravessa sessões no mesmo dia. É o denominador de falso positivo da **D-12** |

A nota da D2 de um evento é o **maior** dos dois desvios, não a soma — soma
contaria o mesmo desvio duas vezes. Os dois são calculados com corte em
`as_of`: nada depois do evento.

**Semana fica de fora**, e é isso que faz a ablação funcionar: acumulação ao
longo de dias é o que a D3 existe para medir. Se a D2 olhasse sete dias, as duas
mediriam quase a mesma coisa, e a tabela de ablação não separaria a contribuição
de cada uma.

### Como o desvio é medido (D-29)

| Tipo de característica | Como compara |
|---|---|
| Contagem — volume, falhas | Desvio robusto: `(x − mediana) / (1,4826 × MAD)`. A constante põe o MAD na escala de um desvio padrão |
| Conjunto — recursos, origens, dispositivos | **Novidade**: apareceu na janela de treino ou não, com peso maior quando o recurso é de sigilo alto |
| Proporção — mistura de sigilo | Distância entre a distribuição do dia e a do baseline, não desvio por categoria |

> **O piso de dispersão, que decide se a D2 funciona.** O divisor é
> `máximo(1,4826 × MAD; piso)`, com **piso = máximo(1 evento; 10% da mediana)**.
> Funcionário perfeitamente regular tem MAD zero: sem piso, a divisão explode e
> a D2 alarma justamente sobre as pessoas mais previsíveis da empresa.

Mais duas travas da mesma decisão:

- **Teto por componente.** Cada desvio entra limitado a 6 antes de compor a
  nota. Sem teto, um atributo sozinho domina e os pesos da **D-09** viram
  enfeite.
- **Quem não tem histórico suficiente não recebe baseline próprio.** Admitido no
  meio da janela de treino, ou de férias durante boa parte dela, cai no padrão
  do **grupo de pares** — mesmo cargo e departamento —, e isso é declarado. Sem
  essa regra, todo funcionário novo vira alarme.

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

### A organização simulada (D-37 a D-41)

Os números abaixo são **parâmetros declarados da simulação**. Nenhum deles é
estatística do mundo real, e nenhum vai ao artigo como dado empírico.

**Departamentos** (D-37):

| Departamento | Pessoas | | Departamento | Pessoas |
|---|---|---|---|---|
| Operações e Atendimento | 70 | | TI e Infraestrutura | 25 |
| Comercial | 45 | | Recursos Humanos | 15 |
| Engenharia e Produto | 40 | | Jurídico | 10 |
| Administrativo e Financeiro | 35 | | Diretoria | 10 |
| | | | **Total** | **250** |

**Personas** (D-38) — cada uma com seu calendário, pela D-27:

| Persona | Pessoas | Faixa/dia útil | Calendário | Ruído legítimo que produz |
|---|---|---|---|---|
| Administrativo diurno | 95 | 20–35 | Seg–sex, 08–18 | O caso base |
| Operação em turno | 45 | 25–40 | Escala 24×7, **inclui fim de semana e feriado** | Madrugada legítima |
| TI privilegiado | 25 | 45–70 | Seg–sex + **12 janelas de manutenção** noturnas | Acesso privilegiado noturno legítimo |
| Comercial viajante | 45 | 20–35 | Seg–sex, ~30% dos dias fora | Origem de outra cidade; pico de fim de mês |
| Híbrido (engenharia) | 30 | 30–50 | Seg–sex, 2 dias de casa | Origem `home` recorrente |
| Gestão e diretoria | 10 | 15–30 | Seg–sex com cauda até 22h | Aprovação noturna |

O TI é a única persona acima do teto de 50, e isso é permitido porque a **D-23**
restringe a *média ponderada*, não cada persona: quem administra dez sistemas
gera mais evento que quem usa dois.

| Verificação da D-23 | Resultado |
|---|---|
| Média ponderada de eventos por dia útil | **32,7** — dentro da faixa de 20 a 50 |
| Volume anual por semente | **≈ 1,93 milhão** — dentro de 1,15 a 2,9 milhões |

**Sistemas e matriz de acesso** (D-39) — é esta tabela que dá definição a "acesso
incomum", e é sobre ela que os cenários são desenhados:

| Sistema | Sigilo | Quem acessa |
|---|---|---|
| Portal interno | `public` | Todos |
| E-mail e agenda | `internal` | Todos |
| Atendimento (CRM operacional) | `internal` | Operações, Comercial |
| Repositório de código | `internal` | Engenharia, TI |
| Servidor de arquivos — pasta do próprio departamento | `internal` | Todos, na própria pasta |
| Servidor de arquivos — pastas de Financeiro e Jurídico | `confidential` | Financeiro, Jurídico, Diretoria |
| ERP financeiro | `confidential` | Financeiro, Diretoria |
| Contratos jurídicos | `confidential` | Jurídico, Diretoria |
| Folha de pagamento | `restricted` | RH (5 de 15), Diretoria |
| Dossiê de pessoal | `restricted` | RH |
| Console de infraestrutura | `restricted` | TI privilegiado |

São onze linhas para dez sistemas de propósito: o servidor de arquivos tem dois
níveis de sigilo, e é o caso que separa "acessou o servidor" de "acessou o que não
devia".

**Sede, filial e fusos** (D-40): **São Paulo (UTC−3) com 210 pessoas** e
**Manaus (UTC−4) com 40**, todas de Operações e Atendimento.

> **Por que dois fusos, e não um.** A **D-31** faz a C0 usar horário fixo no fuso
> da sede e a D1 usar o fuso do funcionário. Com um fuso só, essa diferença é
> decorativa. Com dois, ela produz o caso que a pergunta de pesquisa alega
> resolver: quem encerra o expediente às 21:30 em Manaus são 22:30 em São Paulo
> — **a C0 dispara por horário atípico e a D1 não**. É falso positivo legítimo,
> fabricado por desenho e mensurável.

**Dispositivos e estado inicial de higiene** (D-41):

| Item | Quantidade | Observação |
|---|---|---|
| Notebook corporativo | 250 | Um por pessoa |
| Celular corporativo | 150 | 60%, nas funções com acesso móvel |
| Celular pessoal **autorizado** | 25 | 10%, só e-mail e portal |
| **Total** | **425** | |

MFA ligado em ~87% no início: 100% em TI e Diretoria, 85% nos demais. Mediana de
atraso de atualização: 3 dias no TI, 12 na sede, 25 em quem viaja.

> **O dispositivo pessoal precisa existir no tráfego legítimo.** Se aparecesse só
> em cenário, "evento de dispositivo pessoal" viraria detector perfeito e a C0
> acertaria sem olhar mais nada — a mesma armadilha que a D-27 evitou em férias e
> feriado. Vale igual para desligar o MFA, que acontece legitimamente na troca de
> aparelho.

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
| `outcome` (phishing) | — | — | — | Conduta de higiene: reportou, ignorou, clicou ou entregou credencial |
| Estado de conta e de dispositivo (seção 4) | — | — | — | Postura na data do evento: MFA, privilégio e atualização |

> **A P30, que a D-26 abriu, está fechada pela D-31.** Duas das quatro regras da
> linha de base original usavam histórico — *"IP habitual"* e a janela de falhas
> — e isso **contaminava o grupo de controle**.

### O que a C0 tem, e o que a D1 acrescenta (D-31)

**C0 — quatro regras binárias, limiar fixo, configuração estática:**

1. Horário fora de 06:00–22:00, **no fuso da sede** — genérico de propósito
2. Mais de N falhas de autenticação em 2 minutos na mesma conta, com N fixo
3. Origem fora das faixas corporativas **cadastradas** (`office` e `vpn`) — lista
   estática, e **não** "o IP habitual daquela pessoa"
4. Acesso a recurso com `sensitivity = restricted`

**D1 acrescenta, sobre o mesmo evento isolado:** dispositivo corporativo ou
pessoal, tipo de faixa com peso graduado — `home` não é o mesmo que `external` —,
VPN, MFA, subtipo do `SYSTEM_CONFIG`, tamanho e destino do download e categoria
de navegação. E troca ponto fixo por **peso por atributo**, com o horário
ponderado e **no fuso do funcionário**.

Em uma frase: **a C0 é uma lista de quatro regras com limiar fixo; a D1 é
pontuação ponderada sobre todos os atributos do evento.** Nenhuma das duas olha
o passado do funcionário, e o teste que prova isso é o mesmo para as duas:
embaralhar o histórico não pode mudar nota nenhuma.

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

**As oito que as decisões D-23 a D-26 tinham aberto estão fechadas** em 28/09,
pelas decisões **D-27 a D-31**:

| # | Onde a resposta vive agora | Decisão |
|---|---|---|
| P24 | Calendário por persona; feriado e férias com atividade residual, nunca zero absoluto | **D-27** |
| P25 | Seção 5 — janelas de sessão e usuário-dia; semana é terreno da D3 | **D-28** |
| P26 | Seção 5 — as sete características, com mediana e MAD | **D-29** |
| P27 | Seção 5 — desvio robusto, piso de dispersão, teto e grupo de pares | **D-29** |
| P28 | Seção 4 — os cinco sinais da higiene; antivírus fica fora | **D-30** |
| P29 | Seção 4 — conduta e postura, separadas | **D-30** |
| P30 | Seção 7 — a C0 estática e o que a D1 acrescenta | **D-31** |
| P31 | Regra de corte declarada agora: ciclo completo de uma semente **≤ 30 min → 20 sementes**; acima → 10, com o motivo registrado. **O número sai da S11**, que é a primeira execução completa; na S6 mede-se só o que existe — geração e carga | **D-13** |

> **A D-27 é regra, não lista.** O calendário por persona só vira parâmetro
> quando as personas existirem, e elas são a **P07**, ainda aberta.

**Fechadas em 28/09 pelas decisões D-37 a D-41:** P06 a P10 — departamentos,
personas, matriz de acesso, sede e filial, dispositivos. A **P11** fecha junto,
porque a lista de sistemas com sigilo saiu na mesma decisão, e a **P14** também:
com os atributos do `PHISHING_SIM` definidos e a P28 decidida, os oito tipos
estão completos.

**Dez que continuam abertas, e quem responde por elas:**

| Grupo | Perguntas | O que trava | Quem |
|---|---|---|---|
| O ambiente | P12, P13 | Faixas de rede com país e cidade fictícios; ano simulado, feriados e férias | **Davi** |
| Os eventos | P15, P17 | Proporção de cada tipo por persona e a **taxa normal de senha errada** — sem ela a força bruta só enxerga ataque, nunca erro de digitação | Sem dono registrado. **Proposta: Filipe**, que faz o gerador, com ratificação do Davi |
| Os cenários | P18 a P23 | Catálogo, prevalência, modo de injeção, rótulos e desenho cego. Vencem em **01/10** pelas decisões [D-06](decisoes.md) e [D-16](decisoes.md) | **Yasmin** |

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
