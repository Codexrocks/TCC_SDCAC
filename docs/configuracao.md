# Configuração passo a passo

Página de consulta para quando algo não estiver funcionando. Cada seção é
independente — vá direto na que precisa.

Estado em 03/09/2026: repositório **público**, branch padrão **`main`**, dois
rulesets ativos, secret do assistente cadastrado, equipe completa com acesso.
A configuração inicial está **concluída** — esta página vira consulta.

---

## 1. GitBook — Git Sync

### O erro `expected "site" to be defined`

São **dois arquivos diferentes**, não um só. Confundir os dois causa exatamente
esse erro:

| Arquivo | Onde fica | Configura |
|---|---|---|
| `gitbook-docs.yaml` | raiz do repositório | o **site**: quais espaços existem e qual pasta alimenta cada um |
| `.gitbook.yaml` | dentro de `docs/` | **um espaço**: onde está o índice e a página inicial |

O `gitbook-docs.yaml` precisa da chave `site`. Se ele tiver `root:` e
`structure: readme/summary` — que é o formato do outro arquivo — o GitBook
reclama que falta `site`.

Os dois já estão corretos no repositório:

```
TCC_SDCAC/
├── gitbook-docs.yaml     ← site
└── docs/
    ├── .gitbook.yaml     ← espaço
    ├── README.md         ← página inicial
    └── SUMMARY.md        ← índice
```

### Ligando o Git Sync

`GitBook → Space do site TCC_SDCAC Docs → Configure → Git Sync`

| Campo | Valor |
|---|---|
| Provider | GitHub |
| Organização a autorizar | **`Codexrocks`** — não a conta pessoal |
| Repositório | `Codexrocks/TCC_SDCAC` |
| Branch | **`gitbook/docs/documentacao`** — não a `main`, ver seção 7 |
| **Project directory** | **deixe vazio** |

> Project directory vazio significa "raiz do repositório", que é onde o
> `gitbook-docs.yaml` está. Se você apontar para `docs`, o GitBook procura o
> arquivo em `docs/gitbook-docs.yaml` e não acha.

Na primeira sincronização, escolha **importar do Git** — não começar pelo
template do GitBook, senão ele sobrescreve o repositório.

### O espaço "Untitled"

O site foi criado com um espaço vazio chamado *Untitled*. O
`gitbook-docs.yaml` declara um espaço com a chave `documentacao`, então o
GitBook criou um espaço novo e deixou o *Untitled* solto na organização.

Conferido em 03/09/2026: o *Untitled* está **vazio** (nenhuma página, nenhum
comentário, nenhuma change request) e **não é fonte de conteúdo do site** — o
site tem só o espaço `Documentação`. Apagar não afeta a publicação.

`GitBook → espaço Untitled → menu ⋯ → Delete`. Se apagar por engano, o GitBook
guarda na lixeira e dá para restaurar.

> **Não mude a chave `documentacao` depois que o espaço existir.** O GitBook
> identifica o espaço pela chave, não pelo título. Trocar a chave faz ele criar
> outro espaço do zero e abandonar o antigo, com outro ID — links e referências
> param de funcionar.

---

## 2. Secret do assistente

> **Já está feito.** `CLAUDE_CODE_OAUTH_TOKEN` foi cadastrado em 03/09/2026 e o
> `@claude` responde em issue e em PR. O resto da seção fica como referência
> para quando o token expirar ou precisar ser trocado.

O workflow `@claude` aceita **uma** destas duas credenciais. Basta escolher uma.

### Opção A — token da assinatura (mais simples)

Serve se você já paga o Claude Pro ou Max. Não tem custo por uso.

No terminal, com o Claude Code instalado:

```bash
claude setup-token
```

Copie o token que ele imprimir.

### Opção B — chave da API (cobrada por uso)

`console.anthropic.com → API Keys → Create Key`. Exige créditos na conta —
é uma conta separada da assinatura do Claude.

### Cadastrando no GitHub

`Settings → Secrets and variables → Actions`

Você já esteve nessa tela. O botão é o verde escrito **`New repository secret`**,
na caixa **Repository secrets** — a do meio. Não confunda com:

- **Environment secrets** (a de cima) — para ambientes de deploy, não serve
- **Organization secrets** (a de baixo) — precisa de plano pago, não serve

Preencha:

| Campo | Opção A | Opção B |
|---|---|---|
| Name | `CLAUDE_CODE_OAUTH_TOKEN` | `ANTHROPIC_API_KEY` |
| Secret | o token do `claude setup-token` | a chave do console |

O nome tem que ser exatamente esse, em maiúsculas.

### Alternativa pelo terminal

Se preferir não passar o token pelo navegador, o `gh` cadastra direto e lê o
valor de forma oculta:

```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN -R Codexrocks/TCC_SDCAC
```

Ele pergunta o valor, você cola, e o token não fica no histórico do shell.
Confira depois com `gh secret list -R Codexrocks/TCC_SDCAC` — o comando mostra
só o nome e a data, nunca o valor.

---

## 3. Proteger a `main` com um ruleset

> **Já está feito.** O ruleset `Proteção da main` foi criado em 03/09/2026 e
> está `Active`. O passo a passo abaixo fica como referência — para conferir o
> que está valendo, para recriar se alguém apagar, ou para repetir em outro
> repositório.

O que ficou valendo:

| Regra | Efeito |
|---|---|
| Restrict deletions | ninguém apaga a `main` |
| Block force pushes | ninguém reescreve o histórico |
| Require a pull request | 1 aprovação, e aprovação cai a cada novo commit |
| Require status checks | `validar` e `governanca` precisam passar, com a branch atualizada |
| Allowed merge methods | só **Squash and merge** — as outras opções somem do botão |
| Bypass list | **vazia** — a regra vale para todo mundo, inclusive o dono |

Como a lista de bypass está vazia e o GitHub não pede revisão ao autor do
próprio PR, **quem abre o PR sempre depende de outra pessoa para mergear**.
Hoje isso significa: Davi depende da Yasmin, e vice-versa.

### Os dois checks obrigatórios não são da mesma espécie

Detalhe que parece burocrático e não é — ele já travou um merge:

| Nome | Espécie | Quem publica |
|---|---|---|
| `validar` | **check run** — o próprio job do workflow `Validação` | GitHub Actions |
| `governanca` | **commit status** — publicado pelo job `verificar` via API | GitHub Actions |

O motivo está em como o GitHub soma cada uma. **Check runs de mesmo nome se
acumulam** no mesmo commit: uma reprovação antiga continua contando depois de
uma aprovação nova. Já o **commit status vale pelo mais recente por contexto**.

Isso importa porque o workflow da governança roda de novo **a cada revisão
enviada**, sempre no mesmo commit. O caminho normal é reprovar primeiro (ainda
sem aprovação) e passar depois (com as aprovações) — exatamente o padrão que
quebra com check run. Foi o que travou o [PR #3](https://github.com/Codexrocks/TCC_SDCAC/pull/3)
com tudo aprovado na tela, e exigiu re-executar runs antigos na mão.

O `validar` não tem esse problema: ele só roda quando o código muda, e código
que muda gera commit novo.

> **Se um dia precisar mexer:** o job chama-se `verificar` e o status chama-se
> `governanca` de propósito. A documentação do GitHub avisa que, quando um
> check e um status têm o mesmo nome, **os dois** precisam passar — e o check
> run voltaria a travar tudo. Não unifique os nomes.

### Refazendo pela interface

`Settings → Rules → Rulesets → New ruleset → New branch ruleset`

Preencha nesta ordem:

**Ruleset Name** — `Proteção da main`

**Enforcement status** — mude de `Disabled` para **`Active`**. Se esquecer
disso, o ruleset existe mas não faz nada.

**Target branches** — `Add target → Include default branch`

**Rules** — marque estas caixas:

- [ ] **Restrict deletions** — ninguém apaga a `main`
- [ ] **Block force pushes** — ninguém reescreve o histórico
- [ ] **Require a pull request before merging**
  - Required approvals: **1**
  - [ ] Dismiss stale pull request approvals when new commits are pushed
- [ ] **Require status checks to pass**
  - `Add checks` → procure **`validar`** → selecione
  - `Add checks` → procure **`governanca`** → selecione
  - [ ] Require branches to be up to date before merging

**Create** no fim da página.

> Nenhum dos dois aparece na busca antes de ter sido publicado **pelo menos uma
> vez**. Se a caixa vier vazia, abra um PR qualquer, espere os workflows
> rodarem e volte aqui. Não digite o nome no escuro: o GitHub aceita um nome
> que nunca vai existir, e o resultado é um PR travado para sempre esperando um
> check que ninguém publica.
>
> Procure por **`governanca`**, e não por `verificar`. O primeiro é o commit
> status que decide; o segundo é o job que o produz e não deve ser obrigatório
> — a explicação está logo acima, em *"Os dois checks obrigatórios não são da
> mesma espécie"*.

### "Merge without waiting for requirements to be met (bypass rules)"

Ao mergear, o Davi vê essa caixa marcável e ela assusta. **Marcar é necessário,
e é seguro** — mas vale entender por quê, porque o rótulo do GitHub não explica.

O bypass é **por ruleset**, não geral:

| Ruleset | Regras | O Davi pode contornar? |
|---|---|---|
| `Proteção da main` | PR obrigatório, 1 aprovação, checks verdes | **Nunca** — `bypass_actors` vazio |
| `Merge restrito ao líder` | só `update` | Sempre — é o papel dele |

Marcar a caixa contorna apenas o que ele **tem permissão** de contornar, ou seja
a regra `update`, que é justamente a que impede Yasmin e Felipe de mergear. As
exigências de revisão e de check continuam valendo para ele, marcando ou não.

Foi por isso que os dois ficaram separados em rulesets distintos. Num ruleset só
com bypass, aquela caixa passaria por cima de tudo.

Para conferir a qualquer momento quem pode contornar o quê:

```bash
for id in $(gh api repos/Codexrocks/TCC_SDCAC/rulesets --jq '.[].id'); do
  gh api repos/Codexrocks/TCC_SDCAC/rulesets/$id --jq '"\(.name): \(.current_user_can_bypass)"'
done
```

A resposta esperada é `Proteção da main: never` e
`Merge restrito ao líder: always`. Se o primeiro deixar de ser `never`, alguém
abriu uma brecha na regra de revisão.

> Precisa consultar um ruleset por vez: a listagem devolve
> `current_user_can_bypass: null` para todos, e só o `GET` por id traz o valor
> de verdade.

> **O risco não é o clique, é o hábito.** Ele vai marcar essa caixa em todo
> merge e ela vai virar rotina. Duas defesas: **nunca** adicionar bypass ao
> `Proteção da main`, e olhar a lista de checks antes de clicar — check vermelho
> importa mais que o botão.

### Testando

Depois de criar, tente:

```bash
git checkout main
echo teste >> README.md
git commit -am "teste: isso tem que falhar"
git push origin main
```

O GitHub tem que recusar. Se recusar, está funcionando — desfaça com
`git reset --hard origin/main`.

> Como você é dono da organização, pode existir uma opção de contornar o
> ruleset (*bypass*). Não adicione ninguém à lista de bypass: a regra vale para
> todos, inclusive para você e para o assistente.

### Quem pode executar o merge

Um **segundo ruleset**, `Merge restrito ao líder` (id `22236517`), resolve o
"quem aperta o botão". Ele tem uma regra só — *Restrict updates* — e uma lista
de bypass com **Organization admin**.

O efeito combinado dos dois rulesets:

| Pessoa | Abre PR | Aprova PR | Executa o merge |
|---|---|---|---|
| Davi (org owner) | sim | sim, no PR dos outros | **sim** |
| Yasmin | sim | sim | não |
| Felipe | sim | sim | não |
| Assistente (`@claude`) | sim | não | não |

Yasmin e Felipe veem o botão de merge, mas o GitHub recusa o push resultante.
Não é falta de educação com a ferramenta: é a regra funcionando.

> **O Davi não fica acima das regras.** O bypass vale só neste segundo ruleset,
> o do merge. O primeiro — `Proteção da main` — continua sem bypass nenhum, então
> ele também precisa de PR, de 1 aprovação de outra pessoa e do check verde. Ele
> decide **quando** entra, não **se** passou pelas regras.

Para recriar pela API, se alguém apagar:

```bash
gh api --method POST repos/Codexrocks/TCC_SDCAC/rulesets --input - <<'JSON'
{
  "name": "Merge restrito ao líder",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "bypass_actors": [
    { "actor_id": 1, "actor_type": "OrganizationAdmin", "bypass_mode": "always" }
  ],
  "rules": [ { "type": "update" } ]
}
JSON
```

Para conferir os dois de uma vez:

```bash
gh api repos/Codexrocks/TCC_SDCAC/rulesets --jq '.[] | "\(.name): \(.enforcement)"'
```

### Por que o padrão de branch não é travado no servidor

Seria possível exigir o formato `<autor>/<tipo>/<assunto>` por ruleset, com uma
regra de *branch name pattern*. **Não fizemos, de propósito:** essa regra vale
para toda branch criada no repositório, e o GitBook cria branches próprias
quando alguém edita a documentação pelo site. Travar o padrão no servidor
quebraria o Git Sync.

A verificação fica no [`scripts/validar.py`](../scripts/validar.py), que roda no
check **Validação** de todo PR. O efeito prático é o mesmo — branch fora do
padrão não fecha PR — sem o efeito colateral.

---

## 4. CODEOWNERS — o item 6

`CODEOWNERS` é um arquivo que diz **quem é chamado automaticamente para revisar
cada parte do repositório**. Quando alguém abre um PR que mexe em `docs/`, o
GitHub pede revisão de quem estiver marcado ali, sem ninguém precisar lembrar.

O arquivo está em `.github/CODEOWNERS`. A linha geral aponta para
`@DaviSoaresDilly`; as linhas por pasta seguem **comentadas**, porque um
usuário só vira regra válida depois de ter acesso de escrita ao repositório.

> Antes de 03/09/2026 a linha geral apontava para o time
> `@Codexrocks/lideranca`, que nunca foi criado. O GitHub tratava o arquivo
> inteiro como inválido, com o erro *Unknown owner*. Foi por isso que trocou.

Quando o Felipe entrar, descubra o usuário GitHub dele, apague o `#` do começo
das linhas e troque o placeholder:

```
/docs/                @Yas2046 @usuario-do-felipe
/detection/           @Yas2046
/frontend/            @usuario-do-felipe
```

Para conferir se o arquivo está válido sem precisar abrir um PR:

```bash
gh api repos/Codexrocks/TCC_SDCAC/codeowners/errors
```

Resposta com `"errors":[]` significa arquivo limpo.

É opcional. Sem ele nada quebra — só significa que quem abre o PR escolhe o
revisor na mão.

---

## 5. Dar acesso à equipe

`Settings → Collaborators and teams → Add people`

Yasmin e Felipe com papel **Write**. Write permite criar branch, abrir PR e
aprovar — e não permite mexer em configuração do repositório.

| Pessoa | Usuário | Papel | Estado |
|---|---|---|---|
| Davi | `@DaviSoaresDilly` | Admin · owner da org | ativo |
| Yasmin | `@Yas2046` | Write | ativo |
| Felipe | `@FilipeF4guiar` | Write | ativo |

Equipe completa desde 03/09/2026. Com três pessoas, sempre há alguém que possa
aprovar o PR de outro — o que era o ponto frágil enquanto o time era de dois.

> Yasmin é membro da organização; Felipe entrou como **colaborador externo** do
> repositório. Para o dia a dia dá no mesmo. A diferença aparece se um dia o
> `CODEOWNERS` usar time (`@Codexrocks/algum-time`): time só alcança quem é
> membro da organização.

---

## 6. Relatório semanal automático

Todo segunda de manhã o workflow **Relatório semanal** abre um PR com o balanço
da semana. Configuração em
[`.github/workflows/relatorio-semanal.yml`](https://github.com/Codexrocks/TCC_SDCAC/blob/main/.github/workflows/relatorio-semanal.yml).

Duas etapas, e a separação é o ponto:

| Etapa | Quem faz | Saída |
|---|---|---|
| Contar | [`scripts/atividade.py`](../scripts/atividade.py) | PRs, revisões e commits por pessoa, PRs parados |
| Interpretar | o assistente, lendo só esses números | a leitura da semana, os riscos e as pendências |

Número de relatório de banca precisa ser reproduzível. Como a contagem é um
script sem IA, qualquer número pode ser conferido:

```bash
GITHUB_TOKEN=$(gh auth token) python3 scripts/atividade.py --dias 7
```

Para rodar fora da segunda-feira: aba **Actions** → *Relatório semanal* →
*Run workflow*.

### Se o relatório não aparecer

| Sintoma | Causa provável |
|---|---|
| Nenhuma execução na aba Actions | Repositório sem atividade há 60 dias — o GitHub suspende `schedule`. Rode uma vez na mão para religar |
| Executou e falhou na etapa do assistente | Token do secret expirado. Refaça a seção 2 |
| PR aberto com relatório vazio | Semana sem atividade mesmo. É resultado válido |

---

## 7. GitBook e a `main` protegida

### O erro `cannot update this protected ref`

Se o Git Sync falhar com:

```
Git repository rule violation: "cannot update this protected ref."
```

não é defeito do GitBook. É a proteção da `main` funcionando.

O Git Sync é de mão dupla. Na direção **import** (GitHub → GitBook) ele só lê, e
nada o impede. Na direção **export** (GitBook → GitHub) ele **empurra um commit
direto na branch configurada** — e é aí que bate nos dois rulesets da seção 3: o
primeiro exige Pull Request, o segundo exige que quem atualiza a `main` seja o
dono da organização. O app `gitbook-com` não é nem uma coisa nem outra.

Vale registrar o que esse erro revelou: enquanto o Git Sync apontava para a
`main`, **o GitBook era uma porta dos fundos**. Qualquer pessoa com acesso de
edição ao site escrevia na `main` sem PR, sem revisão e sem passar pelo líder.
A trava não quebrou o fluxo — ela expôs um furo que já existia.

### A solução: espelho de mão única

O GitBook lê de uma branch própria, **`gitbook/docs/documentacao`**, que é um
**espelho descartável da `main`**. Nada volta dela.

```
  main ──────> gitbook/docs/documentacao ──────> GitBook lê e publica
                (espelho, forçado a cada push)
```

O workflow
[`gitbook-sync.yml`](https://github.com/Codexrocks/TCC_SDCAC/blob/main/.github/workflows/gitbook-sync.yml)
força a branch a espelhar a `main` a cada merge. Se o GitBook tiver escrito
alguma coisa nela, é sobrescrito.

### Por que o caminho de volta foi desligado

A primeira sincronização respondeu isso sozinha. O GitBook não editou conteúdo:
ele **reformatou 11 arquivos, −982 linhas**. Desfez todas as quebras de linha,
trocou `---` por `***` e `# Summary` por `# Table of contents`, realinhou as
tabelas, **apagou os comentários do `gitbook-docs.yaml`** — justamente os que
explicam a diferença entre os dois arquivos de configuração — e **criou
`docs/relatorios/relatorios.md`**, deixando o `README.md` órfão.

Não é defeito nem configuração errada. É comportamento documentado:

> GitBook is opinionated. If there are different ways to express the same
> concept or style in markdown, GitBook will only use one.

E, sobre corrigir à mão:

> If you add new content or change existing content to use markup that's not
> GitBook's flavor, GitBook will change it back at the next opportunity.

Eles mantêm um repositório público,
[`GitbookIO/git-sync-normalization`](https://github.com/GitbookIO/git-sync-normalization),
documentando a tradução de cada bloco. **Não existe opção para desligar.**

Some-se a isso que os commits dele nunca passariam no `validar.py`: não seguem
`tipo: descrição` nem trazem `Assistido-por:`. O caminho de volta estava
quebrado nas duas pontas.

> **Não apague a branch `gitbook/docs/documentacao`.** Ela é permanente e é o
> que o GitBook lê. Mas também **não trabalhe nela**: qualquer commit ali é
> descartado no próximo espelhamento.

### As duas zonas

Boa parte do TCC é redação, não código: oito das quinze semanas do
[cronograma](cronograma.md) são escrever texto. Fechar o GitBook por completo
resolveria o problema técnico e criaria um pior — obrigar quem escreve artigo a
trabalhar num editor de código.

Por isso o repositório tem **duas zonas**, com regimes diferentes:

| Pasta | Espaço | Quem escreve | Por quê |
|---|---|---|---|
| `artigo/` | **Artigo** | GitBook | É o texto do TCC. A reformatação não incomoda, porque o que importa ali é o conteúdo |
| `docs/` | **Documentação** | só GitHub | Regras, processo, relatórios. Formato instável aqui quebra revisão e links |

```
                    ┌── espelho forçado ──> gitbook/docs/documentacao ──> lê
main ───────────────┤
                    └── merge ────────────> gitbook/docs/artigo ────────> lê e escreve
                                                      │
                                                      └── Pull Request ──> main
```

**As pastas precisam ser irmãs.** O GitBook não aceita o diretório de um espaço
aninhado dentro do de outro — foi isso que tirou o artigo de dentro de `docs/`:

> Keep all mapped directories as distinct, non-overlapping sibling folders.

### A regra que evita conflito

**`artigo/` se escreve pelo GitBook. `docs/` se escreve pelo GitHub.**

Ninguém edita `artigo/` pelo GitHub — nem para corrigir digitação. Se as duas
pontas mexerem no mesmo arquivo, o workflow falha com conflito e alguém precisa
resolver na mão. Revisão de texto se faz por comentário no Pull Request, sem
editar o arquivo.

### A exceção no validador

Os commits que o GitBook gera — `GitBook: Export content from...` — nunca vão
seguir `tipo: descrição` nem trazer `Assistido-por:`. O `validar.py` os isenta,
e essa é a **única exceção da governança**.

Ela é estreita de propósito: só alcança mensagens que começam exatamente com
`GitBook:` ou `GITBOOK-ALGO:`. Uma mensagem como `GitBooking: ...` continua
reprovando, e há teste garantindo isso.

Mas é um buraco declarado: quem quisesse escapar da declaração de IA poderia
forjar uma mensagem com esse prefixo. **O que segura esse caso é a revisão do
Pull Request, onde o diff aparece — não o validador.**

### Trocando a branch no GitBook

`GitBook → espaço Documentação → Configure → Git Sync`

| Campo | Valor |
|---|---|
| Repositório | `Codexrocks/TCC_SDCAC` |
| **Branch** | **`gitbook/docs/documentacao`** |
| Project directory | vazio |

Se ele perguntar a direção da primeira sincronização, escolha **importar do
Git** (GitHub → GitBook). O GitHub é a fonte da verdade.

**Trave a edição no espaço.** Como o caminho de volta é descartado, deixar
alguém editar no site cria trabalho que se perde sem aviso. No GitBook, deixe o
espaço em modo de leitura para a equipe — quem precisa escrever, escreve pelo
GitHub.

Para conferir o estado do Git Sync sem abrir o site, incluindo o erro da última
operação:

```bash
curl -s -H "Authorization: Bearer $GITBOOK_TOKEN"   https://api.gitbook.com/v1/spaces/aKvalQTXmABRN7IP3nVq/git/info
```

### Se o workflow avisar que descartou commits

Mensagem esperada, não erro:

```
::warning:: Descartando N commit(s) que o GitBook escreveu na branch.
```

Significa que alguém editou pelo site. O texto se perdeu — e é por isso que a
edição no GitBook deve ficar travada. Se acontecer, o conteúdo ainda existe no
histórico da branch antes do espelhamento, e dá para recuperar:

```bash
git fetch origin
git log origin/gitbook/docs/documentacao@{1}    # antes do ultimo espelhamento
```

---

## 6. Windows — dois comandos que não funcionam como estão escritos

O restante desta página assume Linux ou macOS. No Windows, dois comandos que
aparecem na documentação falham por motivos que não têm nada a ver com o
projeto. Ambos têm solução de uma linha.

### `python3` abre a Microsoft Store em vez de rodar

O Windows traz um atalho falso chamado `python3` em `WindowsApps`. Ele não é o
Python — só abre a loja. O sintoma é este, com código de saída `9009`:

```
Python não foi encontrado; executar sem argumentos para instalar do
Microsoft Store ou desabilitar este atalho em Configurações > Aplicativos...
```

O Python de verdade atende por **`python`**. Então, no Windows:

```powershell
python scripts/validar.py
```

O workflow **Validação** roda em Ubuntu e continua usando `python3` — lá o nome
certo é esse. Não mude o `.github/workflows/validacao.yml`.

> Para conferir qual é o seu: `python --version` tem que responder `Python 3.x`.
> Se responder a mensagem da loja, o Python não está instalado.

### `claude` não é reconhecido como comando

Quem usa o **aplicativo desktop** do Claude não recebe o `claude` no PATH. O
executável existe, mas mora dentro do aplicativo — e o aplicativo é empacotado
(MSIX), o que traz uma armadilha a mais.

Um aplicativo empacotado roda num contêiner com **redirecionamento de sistema
de arquivos**. Dentro do contêiner o executável aparece em:

```
%APPDATA%\Claude\claude-code\<versão>\claude.exe
```

Esse caminho é uma visão virtual. **Num PowerShell comum ele não existe** — o
erro é `CommandNotFoundException` apontando justamente para o caminho que você
acabou de ver funcionando em outro lugar. O arquivo de verdade está em:

```
%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\<versão>\claude.exe
```

Então, no seu terminal, use o caminho real. Esta versão descobre sozinha qual é
a versão mais nova, e não quebra quando o aplicativo atualizar:

```powershell
& (Get-ChildItem "$env:LOCALAPPDATA\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\*\claude.exe" | Sort-Object { [version]$_.Directory.Name } -Descending | Select-Object -First 1).FullName setup-token
```

> O sufixo `pzs8sxrjxfjjc` identifica o pacote e pode mudar em outra instalação.
> Se o caminho não existir, ache o seu com:
> `Get-ChildItem "$env:LOCALAPPDATA\Packages" -Filter "Claude*"`.

Quem instala o Claude Code pelo `npm`, no terminal, não passa por nada disso —
o `claude` entra no PATH como qualquer outro programa.
