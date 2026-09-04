# Processo de trabalho

Regra geral: **simples o suficiente para ninguém esquecer.**

***

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

* **GitHub é a fonte da verdade.** Documentação e código no mesmo lugar.
* **GitBook só lê.** Ele espelha a pasta `docs/` e publica o site. O caminho de volta foi desligado: o GitBook reformata todo o Markdown ao exportar, e isso não é configurável. Editar pelo site não chega ao repositório — o texto se perde. Detalhe em [Configuração, seção 7](configuracao.md#7-gitbook-e-a-main-protegida).
* **Documentação se escreve pelo GitHub**, por Pull Request. O [Guia do GitHub](guia-github.md) mostra como fazer isso sem instalar nada, editando o arquivo no navegador.
* **Nada de documentação solta** em Word, Drive ou WhatsApp. Se não está em `docs/`, não existe.

***

## 2. O ciclo de uma tarefa

```
1. git pull origin main               pegue a versão mais recente
2. git checkout -b davi/docs/tema     crie sua branch, com o seu nome
3. ... trabalhe ...
4. git add . && git commit            commits pequenos e frequentes
5. git push -u origin davi/docs/tema  suba
6. abra o Pull Request                peça revisão de 1 colega
7. avise o Davi                       o merge é ele quem faz
8. apague a branch
```

### Nomes de branch

`<autor>/<tipo>/<assunto>` — o nome começa por quem está trabalhando, para dar para ver quem está com o quê sem abrir o log.

| Tipo    | Para quê                 | Exemplo                            |
| ------- | ------------------------ | ---------------------------------- |
| `docs`  | documentação e artigo    | `yasmin/docs/referencial-teorico`  |
| `feat`  | código novo              | `davi/feat/motor-deteccao`         |
| `fix`   | correção                 | `filipe/fix/faixa-risco-medio`     |
| `chore` | configuração, manutenção | `davi/chore/atualiza-dependencias` |

Autores: `davi` · `yasmin` · `filipe` · `claude`. Detalhe em [Padrões](padroes.md#branch).

### Mensagens de commit

`tipo: descrição curta em português, no imperativo`

```
docs: adiciona seção sobre SIEM e SOC
feat: cria endpoint de ingestão de eventos
fix: ajusta peso da regra de força bruta
chore: adiciona dependência do Pandas
```

### Regras de merge

* PR sempre para `main`
* **1 aprovação** obrigatória de um colega — ninguém aprova o próprio PR
* Check **Validação** verde
* **Só o Davi executa o merge** — trava do GitHub, não combinado
* Sempre **Squash and merge**, e é a única opção que o GitHub oferece
* Branch apagada depois do merge

***

## 3. Configuração do repositório

Configuração única, feita pelo Davi.

**a) Tornar o repositório público** — `Settings → General → Danger Zone → Change visibility`

Não é só preferência: no plano gratuito, **regra de branch em repositório privado de organização é recurso pago**. Em repositório público é gratuita. Sem isso, não há como impedir de fato um push direto na `main`.

O plano do TCC já prevê o repositório como ativo de portfólio profissional, e o site do GitBook já é público — então abrir o código não muda a exposição.

**b) Proteger a `main`** — dois rulesets, ambos `Active`:

* [x] `Proteção da main` — PR obrigatório com 1 aprovação, checks **Validação** e **Governança**, sem force push, sem deleção, só _Squash and merge_. Sem bypass para ninguém
* [x] `Merge restrito ao líder` — só o dono da organização atualiza a `main`

**c) Adicionar o secret do assistente** — `Settings → Secrets and variables → Actions`

* [x] `CLAUDE_CODE_OAUTH_TOKEN` — cadastrado em 03/09/2026

**d) Dar acesso à equipe** — `Settings → Collaborators and teams`

* [x] Yasmin (`@Yas2046`) e Filipe (`@FilipeF4guiar`) com papel **Write**

Tudo isso está feito. O passo a passo de cada item, para conferir ou refazer, está em [Configuração passo a passo](configuracao.md).

### Por que o repositório precisou ser público

No plano gratuito, regra de branch em repositório **privado** de organização é recurso pago. Em repositório público é gratuita. Sem isso, não haveria como impedir de fato um push direto na `main` — a regra dependeria de disciplina, e disciplina não aparece no log da banca.

***

## 4. GitBook — configuração inicial

O passo a passo com os campos exatos está em [Configuração passo a passo](configuracao.md#1-gitbook-git-sync).

Dois arquivos, com papéis diferentes — confundir os dois é o que gera o erro `expected "site" to be defined`:

| Arquivo                                                                                                         | Onde              | Configura                                    |
| --------------------------------------------------------------------------------------------------------------- | ----------------- | -------------------------------------------- |
| [`gitbook-docs.yaml`](https://github.com/Codexrocks/TCC_SDCAC/tree/gitbook/docs/documentacao/gitbook-docs.yaml) | raiz              | o **site** e qual pasta alimenta cada espaço |
| `docs/.gitbook.yaml`                                                                                            | dentro de `docs/` | **o espaço**: página inicial e índice        |

No Git Sync, deixe **Project directory vazio** — o `gitbook-docs.yaml` está na raiz do repositório. A **branch é `gitbook/docs/documentacao`**, não a `main`: ela é um espelho descartável, forçado a cada merge, e nada volta dela.

> O plano Pro está em **trial até 17/09/2026**. Confira o que muda no plano gratuito antes dessa data.

> **Toda página nova precisa entrar no `docs/SUMMARY.md`.** Se não estiver lá, não aparece no GitBook.

***

## 4.1 Uso de IA

Os três integrantes usam assistente de IA, e isso é declarado em cada commit e em cada Pull Request — conferido por máquina, não por disciplina. As regras que os assistentes leem estão em [`AGENTS.md`](https://github.com/Codexrocks/TCC_SDCAC/tree/gitbook/docs/documentacao/AGENTS.md); a política escrita para gente está em [Uso de IA](uso-de-ia.md).

Mudança nas regras ou nas checagens automáticas exige **duas** aprovações, para que nenhuma IA consiga afrouxar a própria coleira com uma aprovação só.

## 5. O Claude no projeto

O assistente atua em dois lugares:

**No GitHub** — marque `@claude` em qualquer issue ou Pull Request e descreva o que precisa. Ele lê o repositório, responde no thread e, quando fizer sentido, abre um PR com a alteração.

```
@claude revise o referencial teórico e aponte o que falta de citação ABNT
@claude implemente a regra 3 (IP não habitual) conforme docs/arquitetura.md
```

> **Escrever `@claude` aciona o assistente — sempre.** Inclusive quando você só está explicando a alguém que ele existe: o workflow dispara em qualquer comentário que contenha essa palavra, e cada disparo consome a assinatura. Para citar sem chamar, escreva "o assistente" ou quebre a menção (`@ claude`).

**No GitBook** — como o GitBook espelha o `docs/`, tudo que o Claude escreve na documentação aparece lá automaticamente. Ele não precisa de acesso separado.

### Relatórios

A cada sessão de trabalho com o Claude, é gerado um relatório em [`docs/relatorios/`](relatorios/relatorios.md) com: o que foi pedido, o que foi respondido, o que mudou no repositório e o que ficou pendente.

**Toda segunda de manhã**, além disso, um workflow abre sozinho um PR com o relatório da semana. Ele funciona em duas etapas, e a separação é proposital:

1. [`scripts/atividade.py`](https://github.com/Codexrocks/TCC_SDCAC/tree/gitbook/docs/documentacao/scripts/atividade.py) **conta** — PRs abertos e mergeados, revisões e commits por pessoa, PRs parados. Sem IA no meio, então qualquer número do relatório pode ser reproduzido rodando o script
2. o assistente **lê esses números** e escreve a leitura da semana, cruzando com o [cronograma](cronograma.md)

Quem quiser conferir um número roda:

```bash
python3 scripts/atividade.py --dias 7
```

Precisa de um token do GitHub em `GITHUB_TOKEN`. O relatório também roda sob demanda pelo botão _Run workflow_, na aba **Actions**.

Serve para dois propósitos: ninguém perde o fio da meada, e a banca tem prova documentada do processo de desenvolvimento.
