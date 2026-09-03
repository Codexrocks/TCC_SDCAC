# Configuração passo a passo

Página de consulta para quando algo não estiver funcionando. Cada seção é
independente — vá direto na que precisa.

Estado em 03/09/2026: repositório **público**, branch padrão **`main`**.

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

---

## 3. Proteger a `main` com um ruleset

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
> menos uma vez. Se a lista vier vazia, abra um PR qualquer, espere o check
> rodar, e volte aqui.

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

O arquivo está em `.github/CODEOWNERS`, com as linhas **comentadas** — porque
comentário só vira regra quando os usuários existem de verdade no repositório.

Quando Yasmin e Felipe tiverem acesso, descubra o usuário GitHub de cada uma,
apague o `#` do começo das linhas e troque os nomes:

```
/docs/                @usuario-da-yasmin @usuario-do-felipe
/detection/           @usuario-da-yasmin
/frontend/            @usuario-do-felipe
```

É opcional. Sem ele nada quebra — só significa que quem abre o PR escolhe o
revisor na mão.

---

## 5. Dar acesso à equipe

`Settings → Collaborators and teams → Add people`

Yasmin e Felipe com papel **Write**. Write permite criar branch, abrir PR e
aprovar — e não permite mexer em configuração do repositório.
