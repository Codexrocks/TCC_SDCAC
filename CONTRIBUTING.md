# Como contribuir

Versão curta. A completa está em [`docs/padroes.md`](docs/padroes.md).

**Primeira vez no GitHub?** Comece pelo
[Guia do GitHub](docs/guia-github.md), que parte do zero e não pressupõe git
instalado.

## O ciclo

```bash
git checkout main && git pull origin main
git checkout -b davi/docs/meu-assunto   # <seu-nome>/<tipo>/<assunto>
# ... trabalhe ...
git commit -m "docs: adiciona seção sobre SIEM"
python3 scripts/validar.py              # tem que passar
git push -u origin davi/docs/meu-assunto
# abra o PR; com os checks verdes, o merge é seu
```


## Ligue as verificações locais

Uma vez por clone, logo depois de baixar o repositório:

```bash
git config core.hooksPath .githooks
```

A partir daí, dois ganchos rodam na sua máquina antes de cada commit:

| Gancho | Confere |
|---|---|
| `pre-commit` | Nome de branch, cobertura do `SUMMARY.md`, links quebrados, segredo vazado |
| `commit-msg` | Formato da mensagem e a linha `Assistido-por:` |

Sem isso nada quebra — o check do Pull Request roda igual. A diferença é
**quando** você descobre o erro: agora, na sua máquina, ou dez minutos depois,
no PR.

Precisam de Python instalado. Se não houver, os ganchos avisam e saem sem
atrapalhar. Para pular num commit específico: `git commit --no-verify`.

## Branch

`<autor>/<tipo>/<assunto>` — começa pelo seu nome, para dar para ver quem está
com o quê.

| Tipo | Para quê | Exemplo |
|---|---|---|
| `docs` | documentação e artigo | `yasmin/docs/referencial-teorico` |
| `feat` | código novo | `davi/feat/motor-deteccao` |
| `fix` | correção | `filipe/fix/faixa-risco-medio` |
| `chore` | configuração, manutenção | `davi/chore/atualiza-dependencias` |

Autores: `davi` · `yasmin` · `filipe` · `claude`. Só minúsculas, números e
hífen.

## Commit

`tipo: descrição no imperativo, minúscula, sem ponto final` — máx. 72 caracteres.

```
docs: adiciona referencial teórico sobre UEBA
feat: implementa regra de horário atípico
fix: corrige faixa de severidade do Risk Score
chore: atualiza dependências
```

E toda mensagem termina declarando quem ajudou:

```
docs: adiciona referencial teórico sobre UEBA

Assistido-por: Gemini 2.5 Pro
```

Sem IA? `Assistido-por: nenhuma`. O `validar.py` reprova quem esquecer. Ver
[Uso de IA](docs/uso-de-ia.md).

## Merge

PR para `main` → checks **Validação** e **Governança** verdes → **o Davi faz o
merge** → apaga a branch.

Não há aprovação de outra pessoa: o trabalho é de uma pessoa só, e o GitHub não
deixa ninguém aprovar o próprio PR. O que segura no lugar é o check verde, o
checklist do template lido de verdade e, nos arquivos de regra, as 24 h de
espera da seção 4 do [`AGENTS.md`](AGENTS.md).

## Código

O código começa na S6 (02/10). O que vale para ele — Python 3.12, Ruff, type
hints, docstring em português, teste com pytest — está em
[`docs/padroes-codigo.md`](docs/padroes-codigo.md). Antes de abrir PR com `.py`:

```bash
ruff format . && ruff check --fix . && pytest
```

Mexeu no dashboard? Vale também [`docs/usabilidade.md`](docs/usabilidade.md).

## Uso de IA

Usar IA é esperado. O que não pode é não declarar:

- No **commit**, a linha `Assistido-por:`
- No **Pull Request**, a seção *Uso de IA* do template

As duas são conferidas por máquina. Detalhe em
[`docs/uso-de-ia.md`](docs/uso-de-ia.md); as regras que os assistentes leem
estão em [`AGENTS.md`](AGENTS.md).

Mexer nas regras (`AGENTS.md`, `docs/padroes*.md`) ou nas checagens
(`.github/`, `scripts/`) pede 24 h de PR aberto e a seção `Arquivo protegido`
respondida — ver [`AGENTS.md`](AGENTS.md), seção 4.

## Nunca

- Commitar direto na `main`
- Commitar `.env`, senha, token ou chave
- `git push --force` em branch de outra pessoa
- `git rebase` em branch já enviada

## Ritmo

| Quando | O quê |
|---|---|
| Semanal | Reunião de 30 min, ata em `docs/relatorios/` |
| Quinzenal | Reunião com o orientador |
| A cada sessão com o Claude | Relatório em `docs/relatorios/` |

No Windows, `python3` e `claude` não funcionam como escrito acima — a
correção está em [`docs/configuracao.md`](docs/configuracao.md), seção 6.

As regras que o assistente segue estão em [`CLAUDE.md`](CLAUDE.md).
