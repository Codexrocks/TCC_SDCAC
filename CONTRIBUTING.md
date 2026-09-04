# Como contribuir

Versão curta. A completa está em [`docs/padroes.md`](docs/padroes.md).

## O ciclo

```bash
git checkout main && git pull origin main
git checkout -b davi/docs/meu-assunto   # <seu-nome>/<tipo>/<assunto>
# ... trabalhe ...
git commit -m "docs: adiciona seção sobre SIEM"
python3 scripts/validar.py              # tem que passar
git push -u origin davi/docs/meu-assunto
# abra o PR, peça revisão de 1 colega, avise o Davi para fazer o merge
```

## Branch

`<autor>/<tipo>/<assunto>` — começa pelo seu nome, para dar para ver quem está
com o quê.

| Tipo | Para quê | Exemplo |
|---|---|---|
| `docs` | documentação e artigo | `yasmin/docs/referencial-teorico` |
| `feat` | código novo | `davi/feat/motor-deteccao` |
| `fix` | correção | `felipe/fix/faixa-risco-medio` |
| `chore` | configuração, manutenção | `davi/chore/atualiza-dependencias` |

Autores: `davi` · `yasmin` · `felipe` · `claude`. Só minúsculas, números e
hífen.

## Commit

`tipo: descrição no imperativo, minúscula, sem ponto final` — máx. 72 caracteres.

```
docs: adiciona referencial teórico sobre UEBA
feat: implementa regra de horário atípico
fix: corrige faixa de severidade do Risk Score
chore: atualiza dependências
```

## Merge

PR para `main` → check **Validação** verde → **1 aprovação** → **o Davi faz o
merge** → apaga a branch.

Só o Davi consegue mergear: o GitHub recusa a atualização da `main` vinda de
qualquer outra pessoa. Você abre o PR e aprova normalmente — quando estiver
verde e aprovado, avise.

## Código

O código começa na S6 (02/10). O que vale para ele — Python 3.12, Ruff, type
hints, docstring em português, teste com pytest — está em
[`docs/padroes-codigo.md`](docs/padroes-codigo.md). Antes de abrir PR com `.py`:

```bash
ruff format . && ruff check --fix . && pytest
```

Mexeu no dashboard? Vale também [`docs/usabilidade.md`](docs/usabilidade.md).

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
