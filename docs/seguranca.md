# Revisão de segurança

Revisão de segurança do código do SDCAC, feita em **21/11/2026** por **Claude
Sonnet 5.5** a pedido da **Yasmin**, dona da vertente de segurança (D-19). O texto
é o registro do que foi lido, do que foi achado, do que foi corrigido e do que
ficou como recomendação — com a base pública de cada afirmação.

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

| # | Achado | Classe | Gravidade | Estado |
|---|---|---|---|---|
| S-01 | O painel monta HTML com o motivo da regra **sem escapar** | CWE-79 · OWASP A03:2021 | Média | **Corrigido** |
| S-02 | A variável `SDCAC_ORIGENS` aceitava `*`, embora o comentário do módulo dissesse que não | CWE-942 · OWASP A05:2021 | Baixa | **Corrigido** |
| S-03 | Os `002_privilegios.sql` não retiravam `CREATE` no schema `public` de `PUBLIC` | CVE-2018-1058 | Baixa | **Corrigido** |
| S-04 | Cada leitura relê, converte e ordena o arquivo de eventos inteiro | CWE-400 | Média | Recomendação |
| S-05 | Ações do GitHub referenciadas por **tag móvel**; sem Dependabot nem arquivo de travamento | Cadeia de suprimento | Média | Recomendação |
| S-06 | A API não tem autenticação | OWASP A01:2021 | Baixa, **aceito** | Decisão D-32 |
| S-07 | A linha de base da D2 pode ser **contaminada dentro da janela de treino** | Envenenamento de modelo | Média | Limitação do modelo |

### S-01 — HTML sem escape no painel · Média · corrigido

**Onde:** `frontend/components/parcelas.py`, função `motivo_html`, usada em
`frontend/dashboard/telas.py` com `unsafe_allow_html=True`.

**O quê:** o motivo de cada regra é montado pelo motor **com campo do evento** —
`recurso.name` (`detection/c0/rules.py:131`, `detection/d1/scoring.py:109`), o
destino de um download (`detection/d1/scoring.py:180`), a categoria de navegação
(`detection/d1/scoring.py:208`). Esses campos nascem de log, e log carrega texto
que alguém controla. O valor chegava ao painel e era interpolado em HTML sem
`escape`. O `!r` do Python coloca aspas, mas **não** neutraliza `<` nem `>`.

**Por que importa:** o painel existe para vigiar log. Um painel que executa o que
o log diz inverte a relação de confiança: o atacante escolhe o nome de um recurso
e fala com o navegador do analista. Hoje os dados são sintéticos, e por isso a
gravidade é **Média** e não Alta: o risco real começa quando a ingestão passar a
ler log de verdade.

**O que não foi demonstrado:** a Streamlit avisa que HTML inserido é risco do
desenvolvedor, e sanitiza parte do que renderiza. **Não testei** o que ela barra
neste caminho. A correção vale de qualquer forma, porque escapar na saída é a
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

**Correção:** a partida **falha** com `ValueError` se a lista contiver `*`.
**Teste:** `tests/test_api.py::test_o_cors_recusa_curinga_vindo_do_ambiente`, com
três formas de escrever o curinga.

### S-03 — `CREATE` herdado de `PUBLIC` · Baixa · corrigido

**Onde:** `database/{corp,ground_truth,sdcac}/002_privilegios.sql`.

**O quê:** até o PostgreSQL 14, todo papel com `CONNECT` podia criar objeto no
schema `public`. O 15 mudou o padrão, mas **banco criado antes continua como
era**, e as notas da versão recomendam o `REVOKE` para quem tem vários usuários.
Criar objeto em `public` permite sombrear objetos do catálogo e enganar quem os
usa. A separação em três bancos já fecha o `CONNECT`, mas este era o buraco que
sobrava dentro de cada um.

**Correção:** `REVOKE CREATE ON SCHEMA public FROM PUBLIC;` nos três arquivos. O
`GRANT CREATE … TO generator` do `corp` continua, depois dele.
**Teste:** `tests/test_schema.py::test_ninguem_cria_objeto_no_schema_public_por_ser_public`.

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
| Ações referenciadas por **tag móvel** (`@v4`, `@v5`, `@v1`), não por *commit* | `claude.yml:60,65` e demais |
| O workflow `claude.yml` roda com `contents: write`, `id-token: write` e os *secrets* do Claude | `claude.yml:52-57,67-68` |
| **Não há** `dependabot.yml`, análise de código nem arquivo de travamento das dependências Python | `ls .github`, `ls` na raiz |
| `pyproject.toml` declara só limite inferior (`fastapi>=0.115`) | `pyproject.toml` |

**Por que importa, com um caso público.** A ação que o repositório usa para o
assistente, `claude-code-action`, teve em 2026 uma falha divulgada: a verificação
de que o ator tem permissão de escrita podia ser contornada por conta de bot. A
correção saiu na versão 1.0.94, e a orientação foi atualizar e revisar quem pode
disparar a ação. Nenhum workflow usa `allowed_non_write_users`
(conferido por busca). O `claude.yml` **não** define `allowed_bots`, e registra
isso como trava; o `revisor.yml` define `allowed_bots: "github-actions,gitbook-com"`,
uma lista **explícita**, sem curinga. Vale o Davi reler essa lista à luz da falha. Como a referência é a
tag móvel `@v1`, a correção chega sozinha — e uma versão adulterada também
chegaria. É o dilema das duas pontas, e a revisão **não** recomenda trocar uma
pela outra sem decisão.

**Recomendações, todas em arquivo protegido (24 h e seção `Arquivo protegido`):**

1. Referenciar as ações por **SHA de commit completo**, com o comentário da
   versão, e deixar o Dependabot atualizar. <!-- FALTA CITAÇÃO --> a recomendação
   de pinagem é da documentação do GitHub, e eu não abri a página.
2. Acrescentar `.github/dependabot.yml` para `pip` e `github-actions`.
3. Ligar, nas configurações do GitHub, a **varredura de segredos** e a
   **proteção contra push de segredo**. É configuração fora do repositório, e o
   `AGENTS.md` proíbe a IA de mexer nela.
4. Manter `allowed_non_write_users` **ausente** e a lista de `allowed_bots` do
   `revisor.yml` **sem curinga**, como estão.

### S-06 — API sem autenticação · Baixa · aceito

É a **D-32**, e o próprio `backend/main.py` a explica: a trava é de rede
(`127.0.0.1`) e a que protege o experimento é o **papel de banco**, não a
aplicação. A revisão **concorda com o desenho para a v1** e registra só o limite:
nada na aplicação impede `--host 0.0.0.0`, e a segurança dessa escolha é de quem
inicia o servidor. Se a API sair de `localhost`, autenticação, limite de taxa e
auditoria de consulta deixam de ser opcionais — é o que a **D-19** já registra.

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
não sobre o teste. A literatura também mostra que detectores de anomalia podem
ser envenenados de forma gradual (Rubinstein et al., 2009) e que um atacante que
conhece o detector pode imitar o comportamento normal (Wagner e Soto, 2002).

**O que o experimento mede e o que não mede.** Por construção, os cenários
**só começam depois** da janela de treino: `generator/config.py:150` registra
*"primeiros 3 meses = baseline; cenários só depois"*, e o gerador tem uma
checagem de que eles começam após o baseline
([banco simulado](banco-simulado.md), seção *O baseline de 100 dias e a D-24*).
**Por isso nenhum número deste trabalho mede o caso de um insider que já age
dentro dos três primeiros meses.** Esta página não afirma que a D2 falharia
nele: afirma que **não foi medido**.

**Mitigações possíveis, como trabalho futuro e não como resultado:** tratar a
janela de treino como período de vigilância reforçada, comparar a pessoa também
com o grupo de pares, e reaprender o padrão com validação do que entra nele.

## 5. O que mudou no repositório

| Arquivo | Mudança |
|---|---|
| `backend/main.py` | `origens_permitidas` recusa `*` (S-02) |
| `frontend/components/parcelas.py` | `escape` no motivo e no rótulo da barra (S-01) |
| `database/{corp,ground_truth,sdcac}/002_privilegios.sql` | `REVOKE CREATE ON SCHEMA public FROM PUBLIC` (S-03) |
| `tests/test_api.py`, `tests/test_parcelas.py`, `tests/test_schema.py` | Um teste por correção; **os cinco testes novos falham no código antigo** |

Para reproduzir: `python -m pytest tests/test_api.py tests/test_parcelas.py
tests/test_schema.py`. Para ver o teste cair, desfaça a correção correspondente.

> **`frontend/components/parcelas.py` é da área do Filipe** (S9), e o painel é
> dele. A mudança é pequena e está coberta por teste, mas **ele precisa ler**.

## 6. Limites desta revisão

- **Leitura, não execução.** Nenhum achado foi explorado, e nenhuma ferramenta de
  análise estática foi rodada.
- **Cobertura parcial**, como a seção 1 declara.
- **Gravidade é julgamento.** Uma pessoa pode discordar de qualquer classificação.
- **O modelo de ameaça é curto.** Não cobre ameaça física, engenharia social nem a
  máquina de quem roda o sistema.
- **A quem cabe conferir:** o assistente leu e escreveu; **a Yasmin lê, confirma e
  assina**. As referências abaixo foram achadas por busca e **não** foram abertas
  na fonte pelo assistente.

## Referências

<!-- FALTA CITAÇÃO --> **Todas as entradas abaixo foram localizadas por busca e
precisam ser abertas na fonte por uma pessoa**, em
[citações pendentes](citacoes-pendentes.md). Os dados de publicação vêm de
registros bibliográficos, e a paginação de Saltzer e Schroeder **não** foi
conferida.

BARRENO, M. et al. The security of machine learning. **Machine Learning**, v. 81,
n. 2, p. 121-148, 2010.

MITRE. **CWE-79**: improper neutralization of input during web page generation
('cross-site scripting'). Disponível em: https://cwe.mitre.org/data/definitions/79.html.

MITRE. **CWE-942**: permissive cross-domain security policy with untrusted
domains. Disponível em: https://cwe.mitre.org/data/definitions/942.html.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. **Secure software development
framework (SSDF) version 1.1**: recommendations for mitigating the risk of software
vulnerabilities. Gaithersburg: NIST, 2022. (NIST Special Publication 800-218).

OWASP FOUNDATION. **OWASP Top 10:2021**. Disponível em: https://owasp.org/Top10/2021/.

OWASP FOUNDATION. **Cross site scripting prevention cheat sheet**. Disponível em:
https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html.

POSTGRESQL GLOBAL DEVELOPMENT GROUP. **PostgreSQL 15 release notes**. Disponível
em: https://www.postgresql.org/docs/15/release-15.html.

RUBINSTEIN, B. I. P. et al. ANTIDOTE: understanding and defending against poisoning
of anomaly detectors. In: **Proceedings of the 9th ACM SIGCOMM Internet Measurement
Conference (IMC 2009)**. Chicago: ACM, 2009. p. 1-14.

SALTZER, J. H.; SCHROEDER, M. D. The protection of information in computer systems.
**Proceedings of the IEEE**, v. 63, n. 9, 1975.

STREAMLIT. **st.markdown**. Disponível em:
https://docs.streamlit.io/develop/api-reference/text/st.markdown.

WAGNER, D.; SOTO, P. Mimicry attacks on host-based intrusion detection systems. In:
**Proceedings of the 9th ACM Conference on Computer and Communications Security
(CCS 2002)**. Washington, D.C.: ACM, 2002. p. 255-264.
