# Processo de trabalho

Regra geral: **simples o suficiente para ninguém esquecer.**

---

## 1. Como as ferramentas se encaixam

```
        você escreve                 sincroniza              a equipe lê
    ┌──────────────────┐         ┌──────────────┐      ┌──────────────────┐
    │  GitHub  docs/   │ ──────> │   GitBook    │ ───> │  site publicado  │
    └──────────────────┘         └──────────────┘      └──────────────────┘
             │
             │  mesmo repositório
             ▼
    ┌──────────────────┐
    │ código protótipo │
    └──────────────────┘
```

- **GitHub é a fonte da verdade.** Documentação e código no mesmo lugar.
- **GitBook só lê.** Ele espelha a pasta `docs/`. Editar direto no GitBook
  também funciona — ele devolve a alteração como commit no GitHub.
- **Nada de documentação solta** em Word, Drive ou WhatsApp. Se não está em
  `docs/`, não existe.

---

## 2. O ciclo de uma tarefa

```
1. git pull origin main          pegue a versão mais recente
2. git checkout -b docs/tema     crie sua branch
3. ... trabalhe ...
4. git add . && git commit       commits pequenos e frequentes
5. git push -u origin docs/tema  suba
6. abra o Pull Request           peça revisão de 1 colega
7. Squash and merge              depois de aprovado
8. apague a branch
```

### Nomes de branch

| Prefixo | Para quê | Exemplo |
|---|---|---|
| `docs/` | documentação e artigo | `docs/referencial-teorico` |
| `feat/` | código novo | `feat/motor-deteccao` |
| `fix/` | correção | `fix/faixa-risco-medio` |

### Mensagens de commit

`tipo: descrição curta em português, no imperativo`

```
docs: adiciona seção sobre SIEM e SOC
feat: cria endpoint de ingestão de eventos
fix: ajusta peso da regra de força bruta
chore: adiciona dependência do Pandas
```

### Regras de merge

- PR sempre para `main`
- **1 aprovação** obrigatória de um colega
- Sempre **Squash and merge** (1 PR = 1 commit na `main`)
- Branch apagada depois do merge

---

## 3. Configuração do repositório

Configuração única, feita pelo Davi.

**a) Tornar o repositório público** — `Settings → General → Danger Zone → Change visibility`

Não é só preferência: no plano gratuito, **regra de branch em repositório
privado de organização é recurso pago**. Em repositório público é gratuita. Sem
isso, não há como impedir de fato um push direto na `main`.

O plano do TCC já prevê o repositório como ativo de portfólio profissional, e o
site do GitBook já é público — então abrir o código não muda a exposição.

**b) Proteger a `main`** — `Settings → Rules → Rulesets → New branch ruleset`

- [ ] Target: `main`
- [ ] Require a pull request before merging → **1 approval**
- [ ] Require status checks to pass → **Validação**
- [ ] Block force pushes
- [ ] Restrict deletions

**c) Adicionar o secret do assistente** — `Settings → Secrets and variables → Actions`

- [ ] `ANTHROPIC_API_KEY` — sem ele o workflow `@claude` não roda

**d) Dar acesso à equipe** — `Settings → Collaborators and teams`

- [ ] Yasmin e Felipe com papel **Write**

### Enquanto o repositório for privado

A proteção de branch não existe e o merge não é bloqueado por nada. O que sobra
é o check **Validação**, que fica vermelho no PR mas não impede o merge — ou
seja, a regra passa a depender de disciplina, não de trava.

---

## 4. GitBook — configuração inicial

Estado atual: organização `TCC_SDCAC` criada, site **TCC_SDCAC Docs** publicado,
Git Sync com status **`pending`** — a conexão foi iniciada mas não concluída.

Para concluir (só pela interface do GitBook, não dá por API):

1. Abrir o Space do site **TCC_SDCAC Docs**
2. `Configure → Git Sync → GitHub`
3. Autorizar a **organização** `Codexrocks` — não a conta pessoal
4. Repositório: `Codexrocks/TCC_SDCAC`
5. Branch: `main`
6. Project directory: `docs`
7. Config file: `gitbook-docs.yaml`
8. Na primeira sincronização, escolher **importar do Git** — e não começar
   pelo template do GitBook, senão o conteúdo do repositório é sobrescrito

> O plano Pro está em **trial até 17/09/2026**. Confira o que muda no plano
> gratuito antes dessa data.

O arquivo [`gitbook-docs.yaml`](../gitbook-docs.yaml) na raiz já diz ao GitBook
que a documentação está em `docs/` e que o índice é o `SUMMARY.md`. **O nome do
arquivo precisa ser exatamente o que o campo *Config file* do Git Sync mostrar** —
se a UI indicar outro nome, renomeie o arquivo no repositório.

> **Toda página nova precisa entrar no `docs/SUMMARY.md`.**
> Se não estiver lá, não aparece no GitBook.

---

## 5. O Claude no projeto

O assistente atua em dois lugares:

**No GitHub** — marque `@claude` em qualquer issue ou Pull Request e descreva o
que precisa. Ele lê o repositório, responde no thread e, quando fizer sentido,
abre um PR com a alteração.

```
@claude revise o referencial teórico e aponte o que falta de citação ABNT
@claude implemente a regra 3 (IP não habitual) conforme docs/arquitetura.md
```

**No GitBook** — como o GitBook espelha o `docs/`, tudo que o Claude escreve na
documentação aparece lá automaticamente. Ele não precisa de acesso separado.

### Relatórios

A cada sessão de trabalho com o Claude, é gerado um relatório em
[`docs/relatorios/`](relatorios/README.md) com: o que foi pedido, o que foi
respondido, o que mudou no repositório e o que ficou pendente.

Serve para dois propósitos: ninguém perde o fio da meada, e a banca tem prova
documentada do processo de desenvolvimento.
