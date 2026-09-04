# Configuração passo a passo

Página de consulta para quando algo não estiver funcionando. Cada seção é
independente — vá direto na que precisa.

Estado em 03/09/2026: repositório **público**, branch padrão **`main`**,
ruleset **`Proteção da main`** ativo, Yasmin com acesso de escrita.
Pendente: o secret da seção 2 e o acesso do Felipe (seção 5).

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
| Davi | `@DaviSoaresDilly` | Admin | ativo |
| Yasmin | `@Yas2046` | Write | ativo |
| Felipe | — | Write | **falta convidar** |

Com o ruleset da seção 3 ativo, o acesso do Felipe deixa de ser só organização:
enquanto a equipe for de duas pessoas, cada PR depende da outra estar
disponível para aprovar.
