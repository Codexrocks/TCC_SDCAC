# Como contribuir

Versão curta. A completa está em [`docs/padroes.md`](docs/padroes.md).

## O ciclo

```bash
git checkout main && git pull origin main
git checkout -b docs/meu-assunto      # docs/ feat/ fix/ chore/
# ... trabalhe ...
git commit -m "docs: adiciona seção sobre SIEM"
python3 scripts/validar.py            # tem que passar
git push -u origin docs/meu-assunto
# abra o PR, peça revisão de 1 colega, Squash and merge
```

## Branch

| Prefixo | Para quê |
|---|---|
| `docs/` | documentação e artigo |
| `feat/` | código novo |
| `fix/` | correção |
| `chore/` | configuração, manutenção |

Só minúsculas, números e hífen.

## Commit

`tipo: descrição no imperativo, minúscula, sem ponto final` — máx. 72 caracteres.

```
docs: adiciona referencial teórico sobre UEBA
feat: implementa regra de horário atípico
fix: corrige faixa de severidade do Risk Score
chore: atualiza dependências
```

## Merge

PR para `main` → check **Validação** verde → **1 aprovação** → **Squash and merge** → apaga a branch.

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

As regras que o assistente segue estão em [`CLAUDE.md`](CLAUDE.md).
