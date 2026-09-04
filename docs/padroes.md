# Padrões

A regra única: **nada entra na `main` sem passar por um Pull Request.**
O resto desta página é o detalhe disso.

---

## Branch

```
<autor>/<tipo>/<assunto>
```

O nome **começa por quem está trabalhando**. Assim a lista de branches do
GitHub agrupa por pessoa, e dá para ver quem está com o quê sem abrir o log.

| Tipo | Para quê | Exemplo |
|---|---|---|
| `docs` | documentação e artigo | `yasmin/docs/referencial-teorico` |
| `feat` | código novo | `davi/feat/motor-deteccao` |
| `fix` | correção | `felipe/fix/faixa-risco-medio` |
| `chore` | configuração, manutenção | `davi/chore/atualiza-dependencias` |

Autores válidos: `davi` · `yasmin` · `felipe` · `claude`. Só minúsculas,
números e hífen. Uma branch por tarefa — não acumule assuntos.

> **Entrou alguém novo no projeto?** O nome precisa ser acrescentado à lista
> `AUTORES` em [`scripts/validar.py`](../scripts/validar.py), senão a branch
> dele reprova na validação e o PR não fecha.

## Commit

```
tipo: descrição no imperativo, minúscula, sem ponto final
```

| | |
|---|---|
| ✅ | `docs: adiciona seção sobre SIEM e SOC` |
| ✅ | `feat: implementa regra de horário atípico` |
| ✅ | `fix: corrige faixa de severidade do Risk Score` |
| ❌ | `Atualizações` |
| ❌ | `docs: Adiciona Seção Sobre SIEM.` |
| ❌ | `wip` |

Máximo 72 caracteres na primeira linha. Se precisar explicar, use o corpo do
commit — e explique **por quê**, não o quê (o diff já mostra o quê).

Commits pequenos e frequentes. Um commit deve fazer uma coisa só.

## Pull

Antes de começar qualquer coisa:

```bash
git checkout main
git pull origin main
git checkout -b davi/docs/meu-assunto     # troque pelo seu nome
```

Se a sua branch ficou velha enquanto você trabalhava:

```bash
git fetch origin
git merge origin/main
```

**Não use `rebase` em branch que já foi enviada.** Reescrever histórico
publicado quebra o clone de quem já baixou.

## Push

```bash
git push -u origin davi/docs/meu-assunto
```

Nunca `--force` em branch de outra pessoa. Push direto na `main` não é questão
de disciplina: o GitHub recusa.

## Merge

1. Abra o PR para `main`
2. Preencha o template
3. Peça revisão de **1 colega**
4. Espere o check **Validação** ficar verde
5. **Avise o Davi** — o merge é ele quem faz
6. Apague a branch

### Quem faz o merge

Só o **Davi**, e isso é trava do GitHub, não combinado de boca: o ruleset
`Merge restrito ao líder` recusa qualquer atualização da `main` que não venha
dele. Yasmin e Felipe abrem PR e aprovam normalmente — o botão de merge é que
falha para os dois.

O Davi não escapa do resto: PR, 1 aprovação de outra pessoa e check verde valem
para ele igual. Ele decide **quando** entra, não **se** passou pelas regras.

O GitHub também só oferece **Squash and merge** — as outras opções foram
desligadas no ruleset. Um PR = um commit na `main`.

Um PR = um commit na `main`. O histórico da `main` deve ser legível de cima a
baixo, sem `wip` nem `corrige typo`.

### O que olhar numa revisão

- O PR faz o que o título diz?
- Página nova em `docs/` foi para o `SUMMARY.md`?
- Tem segredo, senha ou `.env` no diff?
- O texto está em português e legível?

## Docs

- Toda documentação vive em `docs/`. Se não está lá, não existe.
- **Toda página nova entra no `docs/SUMMARY.md`.** Sem isso, não aparece no GitBook.
- Um assunto por arquivo. Nome em minúsculas com hífen: `referencial-teorico.md`.
- Link entre páginas sempre relativo: `[equipe](equipe.md)`.
- Conteúdo do artigo vai em `docs/` também — o template COBEM é formatação, não fonte da verdade.

### Citações

Referência bibliográfica só entra se você leu a fonte. Enquanto faltar, marque:

```markdown
<!-- FALTA CITAÇÃO -->
```

A validação não bloqueia isso, mas a banca bloqueia.

## Relatórios

Todo trabalho com o Claude gera um relatório em `docs/relatorios/`.
Toda reunião da equipe também.

```
docs/relatorios/AAAA-MM-DD-sessao-NN.md     sessão com o Claude
docs/relatorios/AAAA-MM-DD-reuniao.md       reunião da equipe
```

Use o [modelo](relatorios/_modelo.md). Estrutura fixa:

1. O que foi pedido
2. O que foi feito
3. Decisões tomadas — e o **motivo** de cada uma
4. Alterações no repositório
5. Pendências, com responsável e prazo

Serve para duas coisas: ninguém perde o fio entre uma semana e outra, e a banca
tem prova documentada de como o projeto foi construído.

## Validação automática

Antes de abrir PR:

```bash
python3 scripts/validar.py
```

Confere nome de branch, formato dos commits, cobertura do `SUMMARY.md`, links
internos quebrados e segredo vazado. O mesmo script roda no GitHub Actions a
cada PR — o check aparece como **Validação**.
