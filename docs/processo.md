# Processo de trabalho

Como as peças se encaixam. **O detalhe de cada regra mora em outro lugar**, e
esta página aponta para ele em vez de repetir: regra escrita em dois lugares
começa igual e termina diferente.

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

- **GitHub é a fonte da verdade.** Documentação e código no mesmo lugar
- **GitBook só lê.** Ele espelha a pasta `docs/` e publica o site. O caminho de
  volta foi desligado porque o GitBook reformata todo o Markdown ao exportar, e
  isso não é configurável: **editar pelo site não chega ao repositório, e o
  texto se perde.** Por quê, em
  [Configuração, seção 7](configuracao.md#7-gitbook-e-a-main-protegida)
- **Documentação se escreve pelo GitHub**, por Pull Request. O
  [Guia do GitHub](guia-github.md) mostra como, sem instalar nada
- **Nada de documentação solta** em Word, Drive ou WhatsApp. Se não está em
  `docs/`, não existe

A exceção é a pasta `artigo/`, a única em que o GitBook **escreve** de volta —
para o artigo ser redigido como num editor de texto. É por isso que nenhum
marcador de bloco gerado mora lá.

---

## 2. O ciclo de uma tarefa

```
1. git pull origin main               pegue a versão mais recente
2. git checkout -b davi/docs/tema     crie sua branch, com o seu nome
3. ... trabalhe ...
4. git add . && git commit            commits pequenos e frequentes
5. git push -u origin davi/docs/tema  suba
6. abra o Pull Request                confira o checklist do template
7. espere os checks verdes
8. apague a branch
```

**Branch:** `<autor>/<tipo>/<assunto>` — começa por quem trabalha, para dar para
ver quem está com o quê sem abrir o log. Os autores aceitos são `davi`,
`yasmin`, `filipe`, `claude` e `gitbook`, e a lista é a mesma de `AUTORES` em
[`scripts/validar.py`](../scripts/validar.py) — um teste compara as duas, para
que acrescentar autor no script e esquecer a página não passe despercebido.

**Commit:** `tipo: descrição no imperativo`, mais a declaração de IA.

Os tipos, os limites de tamanho e o que vale num PR empilhado estão em
**[Padrões](padroes.md)**, que é onde essas regras moram. O `validar.py` confere
todas elas.

O que vale no merge, em uma linha cada:

- PR sempre para `main`, com **Validação** e **Governança** verdes
- **Sem aprovação de outra pessoa** — não há outra pessoa, e o GitHub não deixa
  ninguém aprovar o próprio PR. O **trabalho** continua sendo de três: ver
  [cronograma](cronograma.md#como-o-trabalho-chega-ao-repositório)
- **Só o Davi executa o merge**, e **sempre Squash and merge** — as duas são
  travas do GitHub, não combinados
- Arquivo de regra ou de checagem espera **24 h** e preenche a seção
  `Arquivo protegido`

---

## 3. Configuração do repositório

Feita uma vez, pelo Davi, e **concluída** desde 03/09/2026:

- [x] Repositório **público** — no plano gratuito, regra de branch em
      repositório privado de organização é recurso pago; em público é gratuita.
      Sem isso a proteção da `main` dependeria de disciplina, e disciplina não
      aparece no log da banca
- [x] Dois rulesets ativos — `Proteção da main` e `Merge restrito ao líder`
- [x] Secret `CLAUDE_CODE_OAUTH_TOKEN` cadastrado
- [x] Acesso: **só o Davi tem escrita.** Yasmin e Filipe tiveram papel *Write*
      entre 03/09 e 23/09/2026; hoje produzem fora e ele versiona

O passo a passo de cada item, com os campos exatos, para conferir ou refazer,
está em **[Configuração passo a passo](configuracao.md)** — inclusive a
distinção entre o `gitbook-docs.yaml` da raiz e o `docs/.gitbook.yaml`, que é o
que gera o erro `expected "site" to be defined`.

> **Toda página nova precisa entrar no `docs/SUMMARY.md`.** Fora dele, ela não
> existe para o GitBook — e o `validar.py` reprova.

---

## 4. Uso de IA

O assistente é usado o tempo todo, e isso é declarado em cada commit e em cada
Pull Request — conferido por máquina, não por disciplina. As regras que os
assistentes leem estão em [`AGENTS.md`](../AGENTS.md); a política escrita para
gente, em **[Uso de IA](uso-de-ia.md)**.

Mudança nas regras ou nas checagens espera **24 h** de PR aberto e se explica na
seção `Arquivo protegido` — para que nem a IA nem a pressa afrouxem a coleira na
mesma sentada em que a mudança foi escrita.

---

## 5. O Claude no projeto

**No GitHub** — marque `@claude` em qualquer issue ou Pull Request e descreva o
que precisa. Ele lê o repositório, responde no thread e, quando fizer sentido,
abre um PR.

```
@claude revise o referencial teórico e aponte o que falta de citação ABNT
@claude implemente a regra 3 (IP não habitual) conforme docs/arquitetura.md
```

> **Escrever `@claude` aciona o assistente — sempre.** Inclusive quando você só
> está explicando a alguém que ele existe: o workflow dispara em qualquer
> comentário que contenha a palavra, e cada disparo consome a assinatura. Para
> citar sem chamar, escreva "o assistente" ou quebre a menção (`@ claude`).

**No GitBook** — como o GitBook espelha o `docs/`, o que o Claude escreve na
documentação aparece lá sozinho. Ele não precisa de acesso separado.

### Relatórios

A cada sessão de trabalho é gravado um relatório em
[`docs/relatorios/`](relatorios/README.md): o que foi pedido, o que foi feito,
as decisões com o motivo de cada uma, **os erros da própria IA** e as pendências
com responsável e prazo.

**Toda segunda de manhã** um workflow abre sozinho um PR com o relatório da
semana, em duas etapas, e a separação é proposital:

1. [`scripts/atividade.py`](../scripts/atividade.py) **conta** — PRs abertos e
   mergeados, revisões e commits por pessoa, PRs parados. Sem IA no meio, então
   qualquer número do relatório pode ser reproduzido rodando o script
2. o assistente **lê esses números** e escreve a leitura da semana, cruzando com
   o [cronograma](cronograma.md)

Para conferir um número:

```bash
python3 scripts/atividade.py --dias 7
```

Precisa de um token do GitHub em `GITHUB_TOKEN`. O relatório também roda sob
demanda pelo botão *Run workflow*, na aba **Actions**.

Serve a dois propósitos: ninguém perde o fio da meada, e a banca tem prova
documentada do processo.
