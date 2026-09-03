# Regras de trabalho

Versão curta. A versão explicada está em [`docs/processo.md`](docs/processo.md).

## 1. Branches

`main` é protegida. **Ninguém commita direto nela.**

Crie uma branch por tarefa:

```
docs/<assunto>     documentação e artigo      ex.: docs/introducao
feat/<assunto>     código novo                ex.: feat/risk-score
fix/<assunto>      correção                   ex.: fix/regra-horario
```

## 2. Commits

`tipo: descrição curta em português, no imperativo`

```
docs: adiciona referencial teórico sobre UEBA
feat: implementa regra de horário atípico
fix: corrige faixa de severidade do Risk Score
chore: atualiza dependências
```

Tipos: `docs` · `feat` · `fix` · `chore`

## 3. Pull Request

1. Suba a branch: `git push -u origin <branch>`
2. Abra o PR para `main`
3. Peça revisão de **1 colega**
4. Após aprovação: **Squash and merge**
5. Apague a branch

## 4. Nunca

- Commitar direto na `main`
- Commitar `.env`, senhas, tokens ou chaves
- Fazer `git push --force` em branch de outra pessoa

## 5. Ritmo

| Quando | O quê |
|---|---|
| Semanal | Reunião de 30 min, ata em `docs/relatorios/` |
| Quinzenal | Reunião com o orientador |
| A cada sessão com o Claude | Relatório em `docs/relatorios/` |
