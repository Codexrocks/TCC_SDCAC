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
| Branch | `main` |
| **Project directory** | **deixe vazio** |

> Project directory vazio significa "raiz do repositório", que é onde o
> `gitbook-docs.yaml` está. Se você apontar para `docs`, o GitBook procura o
> arquivo em `docs/gitbook-docs.yaml` e não acha.

Na primeira sincronização, escolha **importar do Git** — não começar pelo
template do GitBook, senão ele sobrescreve o repositório.

### O espaço "Untitled"

O site foi criado com um espaço vazio chamado *Untitled*. O
`gitbook-docs.yaml` declara um espaço com a chave `documentacao`, então o
GitBook vai criar um espaço novo e deixar o *Untitled* solto na organização.
Pode apagar o *Untitled* depois que a sincronização funcionar.

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
| Require status checks | o check `validar` precisa passar, com a branch atualizada |
| Allowed merge methods | só **Squash and merge** — as outras opções somem do botão |
| Bypass list | **vazia** — a regra vale para todo mundo, inclusive o dono |

Como a lista de bypass está vazia e o GitHub não pede revisão ao autor do
próprio PR, **quem abre o PR sempre depende de outra pessoa para mergear**.
Hoje isso significa: Davi depende da Yasmin, e vice-versa.

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
  - [ ] Require branches to be up to date before merging

**Create** no fim da página.

> O check só aparece na busca depois que o workflow **Validação** rodar pelo
> menos uma vez. Isso já aconteceu — `validar` aparece normalmente na lista.

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
| Felipe | `@filipef4guiar-afk` | Write | ativo |

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
