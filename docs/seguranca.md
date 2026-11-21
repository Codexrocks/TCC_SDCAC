# Revisão de segurança

Revisão de segurança do código do SDCAC, feita em **21/11/2026** por **Claude
Sonnet 5.5** a pedido da **Yasmin**, responsável pelo conteúdo de segurança do projeto ([equipe](equipe.md)) e dona da **D-19**, a vertente de LGPD e ISO/IEC 27001. O texto
é o registro do que foi lido, do que foi achado, do que foi corrigido e do que
ficou como recomendação — com a **base pública indicada**. **As fontes foram
abertas e conferidas pelo assistente em 21/11/2026, a pedido do Davi**, e não por
uma pessoa: a seção 5 diz o que cada conclusão sustenta, e a seção 8 diz o que
falta para a Yasmin assinar.

> **O que esta página é, e o que não é.** É uma **revisão por leitura de código**,
> com testes que fixam cada correção. **Não é teste de intrusão**, não rodou
> ferramenta de análise estática e **não demonstrou exploração** de nenhum achado.
> A gravidade de cada item é **julgamento da revisão**, e não pontuação CVSS. O
> assistente leu, a pessoa que assina precisa **ler e confirmar** — a mesma
> divisão que [citações pendentes](citacoes-pendentes.md) já registra para as
> referências.

---

## 1. O que foi revisado

| Área | O que foi lido |
|---|---|
| **API** | **Leitura integral** de `backend/main.py` e `backend/dependencies.py`. De `backend/api.py`, as rotas, a validação de parâmetros e os limites de paginação |
| **Leitura de dados** | De `storage/leitura.py` e `storage/arquivos.py`, o acesso a arquivo e `ArquivoStorage.events` |
| **Painel** | Os construtores de HTML (`frontend/components/`) e todos os usos de `unsafe_allow_html` em `frontend/dashboard/` |
| **Banco** | `database/00_bancos_e_papeis.sql` e os três `002_privilegios.sql`, por inteiro |
| **Automação** | Os sete workflows de `.github/workflows/`: **busca** por gatilhos, permissões, referências a ações e interpolações; leitura do `claude.yml` até a metade do *prompt* |
| **Dependências** | `pyproject.toml` e a presença de arquivo de travamento |
| **O modelo** | O cabeçalho e as funções de `detection/d2/baseline.py`, e a regra de calendário do gerador |

**Não foi coberto:** `generator/`, `evaluator/` e `runner/` por inteiro, o código
de `scripts/` além do uso de rede e de processos, e qualquer coisa fora do
repositório (configuração do GitHub, do GitBook, da máquina de quem roda).

## 2. Modelo de ameaça, em pouco espaço

| | |
|---|---|
| **O que se protege** | A integridade do experimento (o gabarito não pode vazar para o motor), a integridade do log, e quem usa o painel |
| **Quem ataca** | (a) um **log com conteúdo hostil**, porque o sistema existe para ler log de uma empresa e log carrega texto que alguém controla; (b) um **insider** que conhece o motor; (c) **quem contribui** com o repositório público; (d) **a cadeia de dependências** |
| **Onde passa a fronteira** | Evento → motor → API → painel. Cada seta é um lugar onde o dado muda de natureza e precisa ser tratado como não confiável |

## 3. O que já estava bem

O desenho original aplica, sem citá-los, princípios clássicos de projeto seguro
(Saltzer e Schroeder, 1975):

| Controle existente | Princípio |
|---|---|
| Três bancos separados, com `REVOKE CONNECT … FROM PUBLIC` e `sdcac_app` **sem** acesso ao `ground_truth` | **Padrão negado** (*fail-safe defaults*): o acesso nasce fechado e é concedido |
| Papéis `generator`, `sdcac_app` e `evaluator` com só o privilégio de que precisam; **ninguém recebe `UPDATE` ou `DELETE`** do log | **Privilégio mínimo** |
| `tests/test_schema.py` reprova se um `GRANT` perigoso aparecer | A trava está num teste, e não num comentário |
| A API **só lê**, escuta em `127.0.0.1`, pagina com teto de 200, devolve envelope de erro sem SQL, caminho ou pilha | Superfície pequena e erro que não conta como o sistema é feito |
| O caminho dos dados vem do **ambiente**, e não da requisição | Evita leitura de arquivo arbitrário |
| Sem `pickle`, `eval`, `exec`, `shell=True` nem SQL montado por concatenação | Ausência conferida **por busca** em `backend`, `ingest`, `generator`, `evaluator`, `detection` e `frontend`, e não por leitura de cada arquivo |

## 4. Achados

Legenda de gravidade, **estimada pela revisão**: **Alta** · **Média** · **Baixa**.
*Corrigido* quer dizer corrigido **neste PR**, com teste que falha no código
antigo; *Recomendação* quer dizer que o arquivo é protegido pelo
[`AGENTS.md`](../AGENTS.md) seção 4 e a mudança exige 24 h de espera.

| # | Achado | Classe | Gravidade (estimada) | Estado |
|---|---|---|---|---|
| S-01 | O painel monta HTML com o motivo da regra **sem escapar** | CWE-79 · OWASP A03:2021 | Média | **Corrigido** |
| S-02 | A variável `SDCAC_ORIGENS` aceitava `*`, embora o comentário do módulo dissesse que não | CWE-942 · OWASP A05:2021 | Baixa | **Corrigido** |
| S-03 | Os `002_privilegios.sql` não retiravam `CREATE` no schema `public` de `PUBLIC` | CVE-2018-1058 | Baixa | **Corrigido** |
| S-04 | Cada leitura relê, converte e ordena o arquivo de eventos inteiro | CWE-400 | Média | Recomendação |
| S-05 | Ações do GitHub referenciadas por **tag móvel**; sem Dependabot nem arquivo de travamento | Cadeia de suprimento | Média | Recomendação |
| S-06 | A API não tem autenticação | OWASP A01:2021 | Baixa | Escopo da v1 (D-32) |
| S-07 | A linha de base da D2 pode ser **contaminada dentro da janela de treino** | Envenenamento de modelo | Média | Limitação do modelo |

### S-01 — HTML sem escape no painel · Média · corrigido

**Onde:** `frontend/components/parcelas.py`, função `motivo_html`, usada em
`frontend/dashboard/telas.py` com `unsafe_allow_html=True`.

**O quê:** o motivo de cada regra é montado pelo motor **com campo do evento** —
`recurso.name` (`restricted_access`, em `detection/c0/rules.py`, e `_sensitivity`,
em `detection/d1/scoring.py`), o destino de um download (`_download`) e a
categoria de navegação (`_risky_browsing`), as duas em `detection/d1/scoring.py`. Esses campos nascem de log, e log carrega texto
que alguém controla. O valor chegava ao painel e era interpolado em HTML sem
`escape`. O `!r` do Python coloca aspas, mas **não** neutraliza `<` nem `>`.

**Por que importa:** o painel existe para vigiar log. Um painel que executa o que
o log diz inverte a relação de confiança: o atacante escolhe o nome de um recurso
e fala com o navegador do analista. Hoje os dados são sintéticos, e por isso a
gravidade é **Média** e não Alta: o risco real começa quando a ingestão passar a
ler log de verdade.

**O que não foi demonstrado:** a documentação do `st.markdown` avisa que HTML
customizado *"impacts safety, styling, and maintainability"* do app, e que, com
`unsafe_allow_html` desligado, as marcas são escapadas. **Não testei** o que o
navegador executa neste caminho. A correção vale de qualquer forma, porque escapar na saída é a
defesa correta e não depende do que o renderizador faz depois.

**Correção:** `html.escape` em tudo que vem da API em `motivo_html` e no rótulo de
`barra_html`. O HTML que o próprio painel monta continua valendo.
**Teste:** `tests/test_parcelas.py::test_o_motivo_escapa_o_que_vem_da_api`.

### S-02 — Curinga no CORS · Baixa · corrigido

**Onde:** `backend/main.py`, `origens_permitidas`.

**O quê:** o comentário do módulo afirmava que `*` não entra. Era **convenção**: o
código aceitava `SDCAC_ORIGENS="*"` sem reclamar. A API só lê e não usa
credencial, o que limita o estrago, mas qualquer página aberta no navegador de
quem analisa passaria a poder consultá-la.

**Correção:** a partida **falha** com `ValueError` se a lista contiver `*`. É
um comportamento mais restritivo, e foi conferido que **nenhuma página de
documentação ou arquivo de exemplo manda definir `*`**: a única menção ao
assunto é o relatório da sessão 29, que diz *"nunca `*`"*.
**Teste:** `tests/test_api.py::test_o_cors_recusa_curinga_vindo_do_ambiente`, com
quatro formas de escrever o curinga, **inclusive `https://*.exemplo`**. A recusa
cobre qualquer `*` porque o `CORSMiddleware` compara a origem **literalmente**:
um padrão parcial nunca casaria, e falhar na partida avisa quem achou que casaria.

### S-03 — `CREATE` herdado de `PUBLIC` · Baixa · corrigido

**Onde:** `database/{corp,ground_truth,sdcac}/002_privilegios.sql`.

**O quê:** até o PostgreSQL 14, todo papel com `CONNECT` podia criar objeto no
schema `public`. As notas da versão 15 (seção E.21) listam, entre as
incompatibilidades, *"Remove PUBLIC creation permission on the public schema"* e
dizem que, *"for existing databases, especially those having multiple users"*,
convém revogar o `CREATE` para adotar o novo padrão. **Banco criado antes
continua como era.** Esta é a única fonte da página que o assistente **abriu**,
em 21/11/2026; uma pessoa ainda precisa conferir.
Criar objeto em `public` permite sombrear objetos do catálogo e enganar quem os
usa. A separação em três bancos já fecha o `CONNECT`, mas este era o buraco que
sobrava dentro de cada um.

**Correção:** `REVOKE CREATE ON SCHEMA public FROM PUBLIC;` nos três arquivos. O
`GRANT CREATE … TO generator` do `corp` continua, depois dele.
**Testes:** `tests/test_schema.py::test_ninguem_cria_objeto_no_schema_public_por_ser_public`,
e dois que fixam o que **não** pode mudar: o `GRANT CREATE` do gerador no `corp`
continua **depois** do `REVOKE`, e nenhum outro papel recebe `CREATE` em `public`. No
`ground_truth` e no `sdcac` nunca houve `GRANT CREATE`, e o `ground_truth` não tem
tabela particionada, então nada ali dependia do `CREATE` que vinha de `PUBLIC`.
**O que o teste não prova:** ele confere que o texto do `REVOKE` está nos três
arquivos, e não o **efeito** num banco real. Nenhum teste do projeto aplica o
esquema num PostgreSQL, e esta máquina não tem um. Aplicar os três arquivos num
servidor e tentar `CREATE TABLE` como `sdcac_app` é a conferência que falta.

### S-04 — Custo por requisição · Média · recomendação

**Onde:** `storage/arquivos.py`, `ArquivoStorage.events`, chamado por
`ArquivoRepository._eventos_por_id` em `/alerts`, `/employees` e `/events/{id}`.

**O quê:** a cada chamada o arquivo `eventos.jsonl` é lido inteiro, convertido
linha a linha e ordenado, **sem cache**. Cada semente tem na ordem de 1,4 milhão
de eventos (`results/agregado.md`). O teto de 200 itens protege o **tamanho da
resposta**, mas não o **custo no servidor**: a "negação de serviço mais barata"
que o comentário de `backend/main.py` cita continua aberta por outro caminho.

**Por que fica como recomendação:** a API escuta em `127.0.0.1` e é usada por uma
pessoa, o que reduz o risco, e a troca do adaptador de arquivo pelo de
PostgreSQL já está prevista na arquitetura. **Não medi** o tempo de uma chamada,
e o corte entre "incômodo" e "indisponibilidade" depende dessa medida.
**Sugestão:** cachear o resultado pela data de modificação do arquivo, ou
indexar por `event_id` uma única vez.

### S-05 — Cadeia de suprimento · Média · recomendação

**Onde:** `.github/workflows/*.yml` e a raiz do repositório.

| O quê | Evidência |
|---|---|
| Ações referenciadas por **tag móvel** (`@v4`, `@v5`, `@v1`), não por *commit* | Os passos `Checkout` e `Claude Code` de `claude.yml`, e os demais workflows |
| O workflow `claude.yml` roda com `contents: write`, `id-token: write` e os *secrets* do Claude | O bloco `permissions` e o passo `Claude Code` de `claude.yml` |
| **Não há** `dependabot.yml`, análise de código nem arquivo de travamento das dependências Python | `ls .github`, `ls` na raiz |
| `pyproject.toml` declara só limite inferior (`fastapi>=0.115`) | `pyproject.toml` |

**Por que importa, com um caso público.** A ação que o repositório usa para o
assistente, `claude-code-action`, publicou em 2026 o aviso de segurança
**GHSA-8q5r-mmjf-575q**: um PR com um `.mcp.json` malicioso podia executar código
no *runner* e vazar os segredos do workflow quando alguém com permissão disparava
a ação sobre ele; a correção saiu na versão **1.0.74** (Anthropic, 2026a). Em
12/11/2026 a versão **1.0.273** passou a exigir, para execução disparada pela
atividade de um bot num PR, que o autor do PR tenha permissão de escrita ou seja
bot permitido (Anthropic, 2026b).

> **Corrigido em 21/11/2026.** A versão anterior desta página dizia, a partir de
> notícia, que uma falha de contorno da permissão de escrita por bot fora
> corrigida na 1.0.94. **As notas da 1.0.94 não dizem isso** — tratam do `PATH`
> quando `allowed_non_write_users` está definido —, e o único aviso de segurança
> publicado no repositório da ação é o acima. Nenhum workflow usa `allowed_non_write_users`
(conferido por busca). O `claude.yml` **não** define `allowed_bots`, e registra
isso como trava; o `revisor.yml` define `allowed_bots: "github-actions,gitbook-com"`,
uma lista **explícita**, sem curinga. Vale o Davi reler essa lista à luz da falha. Como a referência é a
tag móvel `@v1`, a correção chega sozinha — e uma versão adulterada também
chegaria. É o dilema das duas pontas, e a revisão **não** recomenda trocar uma
pela outra sem decisão.

**Recomendações, todas em arquivo protegido (24 h e seção `Arquivo protegido`):**

1. Referenciar as ações por **SHA de commit completo**, com o comentário da
   versão, e deixar o Dependabot atualizar. É a recomendação da documentação do
   GitHub, que acrescenta que o *lockfile* de dependências do workflow a
   substitui para quem o adotar (GitHub, 2026).
2. Acrescentar `.github/dependabot.yml` para `pip` e `github-actions`.
3. Ligar, nas configurações do GitHub, a **varredura de segredos** e a
   **proteção contra push de segredo**. É configuração fora do repositório, e o
   `AGENTS.md` proíbe a IA de mexer nela.
4. Manter `allowed_non_write_users` **ausente** e a lista de `allowed_bots` do
   `revisor.yml` **sem curinga**, como estão.

### S-06 — API sem autenticação · Baixa · escopo da v1

**O que a D-32 diz, e o que não diz.** A D-32
([decisões](decisoes.md)) separa a v1 (motor, executor e API somente de leitura) da
v2 (login, configuração editável e execução por job) e põe o login na **v2**. Ela
**não** registra o risco como aceito: é uma decisão de **ordem de entrega**. Quem
descreve a ausência de login como escolha explícita é o comentário de
`backend/main.py`, que diz que a trava é de rede (`127.0.0.1`) e que a que protege o
experimento é o **papel de banco**, não a aplicação.

**Avaliação da revisão:** a revisão **concorda com o desenho para a v1**, mas a
aceitação do risco consta no comentário do código, e **não** em uma decisão. Se a
equipe quiser que ela seja formal, é uma decisão a registrar.

**O limite:** nada na aplicação impede `--host 0.0.0.0`, e a segurança dessa
escolha é de quem inicia o servidor. Se a API sair de `localhost`, autenticação,
limite de taxa e auditoria de consulta deixam de ser opcionais — é o que a **D-19**
já registra como o que uma implantação real exigiria.

### S-07 — Contaminação da linha de base · Média · limitação do modelo

Este achado é sobre o **modelo**, e não sobre o código.

**O quê.** A D2 compara cada pessoa com o **próprio** padrão dos três primeiros
meses (D-24), calculado por mediana e MAD (D-29). O desenho tem duas virtudes
contra manipulação:

- a **janela é fixa**: depois dela o padrão não aprende mais, o que fecha o
  ataque de deriva lenta, em que o atacante aumenta o comportamento um pouco a
  cada dia para o detector acompanhar;
- a **mediana e o MAD** são robustos a um pico isolado (D-29).

**A brecha:** quem já age de forma indevida **durante a janela de treino** tem
esse comportamento aprendido como normal, e a D2 passa a medir desvio em relação
a um padrão já contaminado. É o que a literatura de aprendizado de máquina
adversarial chama de ataque **causativo**: o adversário atua sobre o treino, e
não sobre o teste (Barreno et al., 2010). A literatura também mostra que detectores de anomalia podem
ser envenenados de forma gradual (Rubinstein et al., 2009) e que um atacante que
conhece o detector pode imitar o comportamento normal (Wagner e Soto, 2002).

**O que o experimento mede e o que não mede.** Por construção, os cenários
**só começam depois** da janela de treino: o comentário da D-24 em
`generator/config.py` registra *"primeiros 3 meses = baseline; cenários só
depois"*, e o gerador tem uma
checagem de que eles começam após o baseline
([banco simulado](banco-simulado.md), seção *O baseline de 100 dias e a D-24*).
**Por isso nenhum número deste trabalho mede o caso de um insider que já age
dentro dos três primeiros meses.** Esta página não afirma que a D2 falharia
nele: afirma que **não foi medido**.

**Mitigações possíveis, como trabalho futuro e não como resultado:** tratar a
janela de treino como período de vigilância reforçada, comparar a pessoa também
com o grupo de pares, e reaprender o padrão com validação do que entra nele.

## 5. Como cada achado foi confirmado

Esta seção responde à pergunta que a banca fará: **o que foi confirmado por
execução, o que por fonte aberta e o que repousa só na leitura do assistente.**
**As fontes foram abertas pelo assistente em 21/11/2026, a pedido do Davi**, e
nenhuma por uma pessoa.

| # | Base da afirmação | Por execução? | Fonte aberta? |
|---|---|---|---|
| S-01 | Leitura do código e dos usos de `unsafe_allow_html` | **Sim, do escape:** o teste falha sem a correção. **Não** de exploração no navegador | **Sim, pelo assistente:** `st.markdown`, OWASP A03:2021 e CWE-79, em 21/11 |
| S-02 | Leitura do código | **Sim:** o teste falha sem a correção e cobre quatro formas do curinga | **Sim, pelo assistente:** CWE-942 e OWASP A05:2021, em 21/11 |
| S-03 | Leitura do SQL e das notas do PostgreSQL 15 | **Não.** O teste confere o texto, e não o efeito num banco | **Sim, pelo assistente:** a página das notas da versão 15, em 21/11/2026 |
| S-04 | Leitura de `ArquivoStorage.events` | **Não:** o tempo de uma chamada não foi medido | Não |
| S-05 | **Busca** por referências e permissões nos workflows | Sim, da busca | **Sim, pelo assistente:** o aviso GHSA e as notas de versão da ação, e a documentação do GitHub, em 21/11 |
| S-06 | Leitura de `backend/main.py` e da D-32 | Não | Não |
| S-07 | Leitura de `detection/d2/baseline.py` e do calendário do gerador | Não: **justamente o caso não foi medido** | **Sim, pelo assistente:** os três artigos, em 21/11 |

**Em resumo:** duas correções (S-01 e S-02) têm **execução** que as sustenta; uma
(S-03) tem fonte aberta, mas sem execução; as outras quatro repousam na leitura,
com a literatura que as cerca conferida. É esse o peso de cada conclusão, e a página não pede
mais que isso dela.

## 6. O que mudou no repositório

| Arquivo | Mudança |
|---|---|
| `backend/main.py` | `origens_permitidas` recusa `*` (S-02) |
| `frontend/components/parcelas.py` | `escape` no motivo e no rótulo da barra (S-01) |
| `database/{corp,ground_truth,sdcac}/002_privilegios.sql` | `REVOKE CREATE ON SCHEMA public FROM PUBLIC` (S-03) |
| `tests/test_api.py`, `tests/test_parcelas.py`, `tests/test_schema.py` | Um teste por correção, mais dois que fixam o que não pode mudar no banco. **Os testes das três correções falham no código antigo** |

Para reproduzir: `python -m pytest tests/test_api.py tests/test_parcelas.py
tests/test_schema.py`. Para ver o teste cair, desfaça a correção correspondente.

### Exceção ao marco M4, que o Davi precisa autorizar

O [cronograma](cronograma.md) diz, no marco **M4**, que *"a partir daqui o trabalho
é escrita. Nenhuma alteração de código é aceita"*, e o M4 fechou em 12/11/2026. **Este
PR altera código em 21/11/2026**: `backend/main.py`, `frontend/components/parcelas.py`
e três arquivos SQL. **O assistente não verificou o M4 antes de alterar**, e isso está
registrado como erro no relatório da sessão 56.

**Quem pediu, e quem precisa autorizar.** O pedido foi da **Yasmin**, e o
[`AGENTS.md`](../AGENTS.md) seção 4 exige pedido explícito do **Davi** para mexer em
escopo ou cronograma. **A autorização dele não está registrada.** Sem ela, as três
correções são uma proposta, e não uma mudança aceita.

**O que a evidência mostra sobre os números da seção 4 do artigo** (conferida em
21/11/2026 por busca e leitura, sem reexecutar o experimento):

| Verificação | Resultado |
|---|---|
| Algum módulo do experimento (`detection`, `runner`, `evaluator`, `generator`, `ingest`, `storage`) importa `backend/` ou `frontend/`? | **Não.** A busca por `import backend` e `import frontend` fora de `backend/`, `frontend/` e `tests/` volta vazia |
| O `detection/` pode importar `backend/`? | **Não**, e há teste que reprova (`tests/test_arquitetura.py`) |
| Algum código lê os `002_privilegios.sql`? | **Só testes.** O experimento usa o adaptador de arquivos, e não PostgreSQL |
| Este PR altera `results/` ou `artigo/`? | **Não**: nenhum arquivo |
| A suíte inteira, inclusive os testes do experimento? | **765 passam** |

**O que isto não prova.** É evidência **estática**: o experimento não foi rodado de
novo, e `results/agregado.md` não foi regenerado nem comparado. A conclusão correta é
que **nada no caminho que gera os números importa o código alterado**, e não que um
reexecução daria byte a byte o mesmo resultado.

**Opção que não depende da autorização.** A documentação (`docs/seguranca.md`, o
relatório, o quadro) **não é código**. Se o Davi não autorizar a exceção, o PR pode
entrar só com ela, e as três correções ficam como recomendação.

> **`frontend/components/parcelas.py` é da área do Filipe** (S9), e o painel é
> dele. A mudança é pequena e está coberta por teste, mas **ele precisa ler**.

## 7. Limites desta revisão

- **Leitura, não execução.** Nenhum achado foi explorado, nenhuma ferramenta de
  análise estática foi rodada e o efeito do `REVOKE` não foi testado num
  PostgreSQL real.
- **Cobertura parcial**, como a seção 1 declara.
- **Gravidade é julgamento.** Uma pessoa pode discordar de qualquer classificação.
- **O modelo de ameaça é curto.** Não cobre ameaça física, engenharia social nem a
  máquina de quem roda o sistema.
- **A quem cabe conferir:** o assistente leu e escreveu; **a Yasmin lê, confirma e
  assina**. As referências abaixo foram abertas e conferidas pelo assistente em
  21/11/2026, a pedido do Davi.

## 8. Para a Yasmin assinar

**Enquanto as caixas abaixo não estiverem marcadas, esta página é do assistente, e a
revisão não está assinada.** O assistente leu, escreveu, testou e registrou os
próprios erros, e conferiu as fontes em 21/11 a pedido do Davi; quem assume uma revisão diante
da banca é quem a leu. É a mesma divisão que o repositório já usa para as
referências do artigo.

- [ ] Li a página inteira, e discordo ou concordo de cada gravidade da seção 4
- [x] ~~Abri cada fonte da lista de [Referências](#referências)~~ — **conferidas
      pelo assistente em 21/11/2026, a pedido do Davi**, que delegou a conferência:
      autor, título, veículo, paginação e o trecho que sustenta cada afirmação. Duas
      correções saíram dela, e estão nas seções 4 e 5
- [x] ~~Abri o relato da falha do `claude-code-action` em fonte primária~~ — feito
      pelo assistente no mesmo dia: o relato da notícia **não se confirmou**, e o
      texto passou a citar o aviso GHSA e as notas de versão
- [ ] Rodei `python -m pytest tests/test_api.py tests/test_parcelas.py tests/test_schema.py`
      e desfiz uma correção para **ver o teste falhar**
- [ ] Abri `frontend/components/parcelas.py` e `backend/main.py` e li as duas
      mudanças
- [ ] Declarei no PR **"Conferi tudo que a IA escreveu: sim"**

> **O Filipe leu a mudança em `frontend/components/parcelas.py`**, que é da área
> dele (S9), relatado pelo Davi em 21/11/2026.

**Como a banca verifica.** Pelo que fica no repositório, e não pela palavra de
ninguém: o histórico do PR mostra quem escreveu cada commit e a declaração de IA;
as linhas de `docs/citacoes-pendentes.md` só saem quando alguém abriu a fonte; os
testes das três correções **falham sem a correção** e qualquer pessoa pode repetir isso; e
o relatório da sessão 56 lista os erros do assistente e **quem os pegou**.

## Referências

**Conferidas pelo assistente em 21/11/2026, a pedido do Davi.** As obras
acadêmicas foram conferidas no Crossref e no texto dos autores; as páginas da web,
abertas. O NIST SP 800-218 saiu da lista: não era citado no texto.

ANTHROPIC. **GHSA-8q5r-mmjf-575q**: malicious MCP server configuration in PRs
enables remote code execution and secret exfiltration. [S. l.]: GitHub, 2026a.
Disponível em: https://github.com/anthropics/claude-code-action/security/advisories/GHSA-8q5r-mmjf-575q.
Acesso em: 21 nov. 2026.

ANTHROPIC. **claude-code-action v1.0.273**: notas de versão. [S. l.]: GitHub,
2026b. Disponível em: https://github.com/anthropics/claude-code-action/releases/tag/v1.0.273.
Acesso em: 21 nov. 2026.

BARRENO, M. et al. The security of machine learning. **Machine Learning**, v. 81,
n. 2, p. 121-148, 2010.

MITRE. **CWE-79**: improper neutralization of input during web page generation
('cross-site scripting'). Disponível em: https://cwe.mitre.org/data/definitions/79.html.

MITRE. **CWE-942**: permissive cross-domain security policy with untrusted
domains. Disponível em: https://cwe.mitre.org/data/definitions/942.html.

GITHUB. **Secure use reference**: GitHub Actions. [S. l.]: GitHub, 2026. Disponível em:
https://docs.github.com/en/actions/reference/security/secure-use. Acesso em: 21 nov. 2026.

OWASP FOUNDATION. **OWASP Top 10:2021**. Disponível em: https://owasp.org/Top10/2021/.

OWASP FOUNDATION. **Cross site scripting prevention cheat sheet**. Disponível em:
https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html.

POSTGRESQL GLOBAL DEVELOPMENT GROUP. **PostgreSQL 15 release notes**. Disponível
em: https://www.postgresql.org/docs/15/release-15.html.

RUBINSTEIN, B. I. P. et al. ANTIDOTE: understanding and defending against poisoning
of anomaly detectors. In: **Proceedings of the 9th ACM SIGCOMM Internet Measurement
Conference (IMC 2009)**. Chicago: ACM, 2009. p. 1-14.

SALTZER, J. H.; SCHROEDER, M. D. The protection of information in computer systems.
**Proceedings of the IEEE**, v. 63, n. 9, p. 1278-1308, 1975.

STREAMLIT. **st.markdown**. Disponível em:
https://docs.streamlit.io/develop/api-reference/text/st.markdown.

WAGNER, D.; SOTO, P. Mimicry attacks on host-based intrusion detection systems. In:
**Proceedings of the 9th ACM Conference on Computer and Communications Security
(CCS 2002)**. Washington, D.C.: ACM, 2002. p. 255-264.
