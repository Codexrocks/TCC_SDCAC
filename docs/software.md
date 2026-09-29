# O software de análise

Especificação do sistema que lê os eventos gerados, avalia o risco nas quatro
configurações e entrega o resultado para inspeção. É o par da
[especificação do banco](banco-simulado.md): lá está o que o gerador produz, aqui
está o que o software faz com aquilo.

**O código começa depois da aprovação desta página**, como já vale para o banco.

| | |
|---|---|
| Versão | 28/09/2026 — incorpora as decisões D-32 a D-36 |
| Entra em | **S6 a S8** a versão 1; **S9 em diante** a versão 2 |
| Não trata de | Telas, layout e navegação. O painel é a frente do **Filipe**, na S9, sob a [usabilidade](usabilidade.md) |

## Quem faz

| Frente | Quem |
|---|---|
| Motor de avaliação, executor do experimento, schema e API | **Davi** |
| Gerador de eventos | **Filipe** (S6) |
| Painel de inspeção em Streamlit | **Filipe** (S9) |
| Cenários e rótulos | **Yasmin** (D-06 e D-16) |

***

## 1. O que o artigo já promete

Esta página existe para cumprir o que a [Metodologia](../artigo/03-metodologia.md)
afirma. Cada linha abaixo é uma promessa já escrita no artigo, e a coluna da
direita é o que no software a sustenta:

| O artigo afirma | O que sustenta aqui |
|---|---|
| "Um único código executado sob quatro parâmetros" (3.3) | Seção 2: as configurações são composição de módulos, não quatro sistemas |
| "A C0 é puramente estática" (3.3) | Seção 4: presets canônicos imutáveis, e a C0 sem acesso a histórico |
| "A terceira dimensão reporta duas parcelas separadas" (3.3) | Seção 6: a resposta de leitura carrega D3 partida em conduta e postura |
| "Cada execução grava identificador, semente, configuração e pesos" (3.7) | Seção 4: configuração versionada, com hash preso ao resultado |
| "Comparar duas configurações é comparar dois identificadores de execução" (3.7) | Seção 5: execução é registro, não requisição |
| "A interface de inspeção é construída em Streamlit" (3.7) | Seção 6: a API entrega dados; a interface é do Filipe |
| "O painel é instrumento de análise, não objeto de avaliação" (3.9) | Seção 9: o que a v1 deliberadamente não tem |

> **O artigo não promete autenticação.** Nenhuma afirmação da Metodologia depende
> de login, sessão ou papel de usuário. Isso é engenharia do protótipo, não
> resultado — e é por isso que entra na versão 2.

## 2. As duas versões, e por que nesta ordem (D-32)

| Versão | O que é | Semanas |
|---|---|---|
| **v1** | Motor modular (C0, D1, D2, D3), leitura do `corp`, gravação no `sdcac`, **executor de linha de comando** e API **somente de leitura**, presa ao `localhost` | S6 a S8 |
| **v2** | Login, configuração editável e versionada pela interface, execução disparável por job, auditoria de consulta | S9 em diante |

O motivo da ordem é aritmético: **a tabela de resultados sai do executor, não da
API.** A S11 executa todos os cenários nas quatro configurações; se a janela de
código for gasta em login e telas de configuração, a S11 chega sem motor. A v1
continua aberta para receber o painel — o que abre não é a tela, é o contrato
OpenAPI estável desde o primeiro dia.

## 3. Módulos, e a regra que os separa

```text
detection/     c0/ · d1/ · d2/ · d3/ · integracao/     o núcleo, em Python puro
runner/        executor do experimento                 entrada sem HTTP
backend/       api/ · models/ · services/ · main.py    adaptador HTTP
database/      corp/ · ground_truth/ · sdcac/          schema e migrações
generator/     personas/ · calendario/ · cenarios/     a peça da S6
frontend/      dashboard/                              a peça da S9
```

**A regra de dependência, conferida no CI:** `detection/` não importa
`backend/`, `database/` nem `generator/`, e não consulta o relógio. As duas
entradas — `runner/` e `backend/` — importam `detection/`.

É essa regra que faz valer a frase do artigo sobre um único código sob quatro
parâmetros: **o que o painel mostra é o mesmo código que produziu a tabela.**

## 4. O que é ajustável, e o que é imutável (D-33 e D-34)

| Tipo de configuração | Quem altera | Pode ir ao artigo? |
|---|---|---|
| **Presets canônicos C0, C1, C2, C3** | Ninguém pela interface. Nascem em arquivo semeado, versionado no git | **Sim** — são o experimento |
| **Configurações exploratórias** | Qualquer usuário, quantas quiser | **Não.** Ficam marcadas como exploratórias, e todo resultado gerado por elas carrega o aviso |

O motivo do grupo de controle não ser um botão está na própria Metodologia: a C0
é a referência contra a qual tudo é medido. Controle que alguém afrouxa deixa de
medir. E configuração livre sobre a C3 abriria caminho para ajustá-la até ela
ganhar — o que a banca chamaria de ajuste posterior ao resultado, e derrubaria a
conclusão.

**Configuração é registro imutável e versionado.** Salvar não altera a versão
existente: cria a próxima, com autor, data e hash. Toda execução grava o
identificador e o hash da configuração que usou, e **execução sem esse hash é
erro, não aviso.** É o que a seção 3.7 do artigo chama de registro de execução.

## 5. Execução é job, não requisição (D-35)

Pontuar dois milhões de eventos dentro de uma requisição HTTP não existe. O
desenho:

1. A requisição **enfileira** e devolve um identificador de job
2. Um processo separado — o mesmo monólito, outra entrada — consome a fila
3. O estado do job é consultado por outra chamada
4. Ao terminar, o job aponta para a execução gravada no `sdcac`

A fila é uma tabela do `sdcac`. **Sem Celery e sem Redis:** fila em banco, nesta
escala, não tem desvantagem que justifique uma dependência nova.

Na v1 o executor é de linha de comando e não precisa de fila — o job entra na v2,
quando a interface passa a disparar execução.

## 6. O contrato de leitura (D-36)

Quatro grupos, prefixo `/api/v1` desde o primeiro dia:

| Grupo | O que entrega |
|---|---|
| **Execuções** | Semente, commit, configuração, hash e estado de cada execução |
| **Funcionários** | Lista paginada com a nota mais recente por dimensão; detalhe com histórico |
| **Eventos e alertas** | Alertas filtráveis por período, faixa e dimensão; evento com o score decomposto |
| **Métricas** | O que o avaliador gravou: FPR, revocação, unidade de análise, configuração |

Quatro exigências, e é isso que "pronto para o frontend" significa:

- **Score sempre decomposto:** C0, D1, D2, e a D3 partida em **conduta** e
  **postura**. Devolver um número só impediria o painel de cumprir a
  decomponibilidade que a seção 3.9 do artigo promete
- **Paginação em toda lista**, com envelope de erro único
- **Data em UTC com fuso explícito**, sempre
- **Nenhuma rota devolve HTML.** A API entrega dados; a interface é outra peça

Duas proibições que vêm de decisões anteriores:

- **A API não lê o `ground_truth`.** O usuário da aplicação não tem permissão de
  conectar naquele banco
- **A API não calcula métrica.** Precisão e revocação vêm da tabela
  `sdcac.metrics`, gravada pelo avaliador, que é o único que enxerga o gabarito

## 7. O que entra no `sdcac` na v2

As tabelas de eventos, estado, padrão e gabarito estão na
[especificação do banco](banco-simulado.md) e não se repetem aqui — duas listas
em dois arquivos viram dois schemas na primeira alteração. O que a v2
**acrescenta**:

| Tabela | Para quê |
|---|---|
| `users`, `roles` | Login e dois papéis: `analyst` e `researcher` |
| `configurations`, `configuration_items` | Configuração como versão imutável, com hash e autor |
| `jobs` | Fila de execução: estado, início, fim, erro e execução gerada |
| `audit_log` | Quem consultou o risco de quem — insumo direto da **D-19** |

## 8. Autenticação, quando chegar a hora (v2)

O que o backend faz, e só isso: senha guardada com **Argon2**; usuário inicial
vindo de arquivo semeado do projeto, **nunca do código**; sessão curta com
renovação; bloqueio progressivo por tentativa; dois papéis, sem tela de
administração.

Fora de escopo por decisão: recuperação de senha por e-mail, cadastro aberto,
integração com provedor de identidade. São serviços externos, e um protótipo de
ambiente simulado não tem por que tê-los.

> **A proteção que importa aqui não é o login.** É o privilégio de banco: o
> usuário da aplicação não conecta no `ground_truth`. O login protege a tela; o
> papel de banco protege o experimento.

## 9. Testes que a v1 precisa passar

Além dos invariantes da especificação do banco — nada do futuro, exposição sem o
evento atual, determinismo:

- **A C0 não olha histórico:** apagar o passado do funcionário não muda a nota C0
  nem a D1. É a **D-31** virando teste
- **Preset canônico é imutável:** alterar C0 a C3 pela API falha
- **Configuração presa ao resultado:** execução gravada sem hash de configuração
  falha
- **A aplicação não alcança o gabarito:** o teste tenta conectar com o usuário da
  aplicação no `ground_truth` e **espera** erro de permissão
- **Score decomposto:** toda resposta de leitura traz as cinco parcelas

## 10. O que a v1 deliberadamente não tem

Login, cadastro de usuário, edição de configuração pela interface, fila de job,
auditoria de consulta, execução em nuvem, cache, notificação e qualquer rota de
escrita. Nada disso aparece na Metodologia, e nenhuma conclusão do artigo depende
deles.

## 11. Onde termina esta página

No contrato da API. **Tela, layout, navegação e texto de onboarding são do
painel**, que é frente do Filipe na S9, governado pela
[usabilidade](usabilidade.md) — rótulo textual junto da cor, contraste mínimo e
risco decomponível à vista.

> **A D-02 continua aberta.** Se o painel virar objeto de avaliação, e não
> instrumento, a seção 3.9 do artigo é reescrita e a exigência sobre a API muda
> com ela. Até lá vale a opção A: instrumento de análise.

***

## Procedência

Página preparada com assistência do **Claude Opus 5** em 28/09/2026, a partir do
pedido de planejar o software em duas versões. A recomendação de inverter a ordem
das versões, de tornar os presets imutáveis e de separar configuração canônica de
exploratória é dela; as decisões D-32 a D-36 são do Davi.

Nada aqui é número de desempenho: não há medição de tempo, memória ou volume
neste documento, porque nenhuma execução aconteceu.
