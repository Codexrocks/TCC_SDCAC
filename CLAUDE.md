# Regras do assistente — TCC_SDCAC

Instruções permanentes para o Claude neste repositório. Valem em toda sessão,
no Claude Code e no workflow `@claude` do GitHub Actions.

## Contexto

TCC 2026/2 · Prof. Euzébio D. de Souza · Sistema de Detecção de Comportamentos
Anômalos em Cybersecurity. Equipe de três: **Davi** (líder & backend),
**Yasmin** (cybersecurity), **Felipe** (data & dashboard).

O repositório é **público**. A pasta `docs/` é publicada no GitBook em
`TCC_SDCAC Docs`. Tudo que entra em `docs/` vira site público.

## Idioma

Escreva sempre em **português do Brasil** — documentação, commits, PRs,
comentários e respostas. Código e nomes de arquivo em inglês, quando for
convenção da linguagem.

## Regras que não se quebram

1. **Nunca commitar direto na `main`.** Sempre branch + Pull Request.
   Sem exceção. O ruleset `Proteção da main` está ativo desde 03/09/2026 e o
   próprio GitHub recusa o push direto, inclusive o do dono do repositório.
2. **Nunca commitar segredo** — `.env`, senha, token, chave, string de conexão.
   Se encontrar um no repositório, pare e avise em vez de corrigir sozinho.
3. **Toda página nova em `docs/` entra no `docs/SUMMARY.md`.** Fora do SUMMARY,
   a página não existe para o GitBook.
4. **Não criar pasta vazia.** Pasta de código só quando houver código nela.
5. **Não inventar conteúdo acadêmico.** Referência bibliográfica, citação, dado
   ou resultado experimental só entram se vierem de fonte verificada. Na dúvida,
   marque `<!-- FALTA CITAÇÃO -->` e avise.
6. **Não alterar o cronograma nem o escopo** sem pedido explícito do Davi.
7. **Código segue `docs/padroes-codigo.md`** — Python 3.12, Ruff, type hints,
   docstring em português, nome de identificador em inglês, SQL parametrizado.
8. **Mexeu no dashboard? Vale `docs/usabilidade.md`** — rótulo textual junto da
   cor, contraste mínimo de 4,5:1, decomposição do Risk Score visível.

## Padrão de branch

```
<autor>/<tipo>/<assunto>
```

Autor: `davi` · `yasmin` · `felipe` · `claude`.
Tipo: `docs` (documentação e artigo) · `feat` (código novo) · `fix` (correção) ·
`chore` (configuração, dependências, manutenção).

Só minúsculas, números e hífen. Ex.: `yasmin/docs/referencial-teorico`.
As suas branches começam com `claude/`.

Autor novo precisa entrar na lista `AUTORES` de `scripts/validar.py`, senão a
branch reprova.

## Padrão de commit

```
tipo: descrição no imperativo, minúscula, sem ponto final
```

Tipos: `docs` · `feat` · `fix` · `chore`. Máximo 72 caracteres na primeira linha.
Corpo opcional explicando **por quê**, não o quê.

## Pull Request

- Base sempre `main`
- Título no mesmo padrão do commit
- Preencher o template
- 1 aprovação antes do merge
- **Squash and merge**, sempre

**Nunca faça merge.** Na `main` só o Davi merge, e o GitHub recusa qualquer
outra origem. Deixe o PR pronto e aprovado, e avise.

## Relatório de sessão — obrigatório

Ao fim de **toda** sessão de trabalho, gravar um relatório em
`docs/relatorios/AAAA-MM-DD-sessao-NN.md` usando `docs/relatorios/_modelo.md`,
adicionar ao `docs/SUMMARY.md` e ao índice em `docs/relatorios/README.md`.

O relatório contém, nesta ordem:

1. **O que foi pedido** — citação resumida do pedido, nas palavras de quem pediu
2. **O que foi feito** — lista objetiva
3. **Decisões tomadas** — tabela `decisão | motivo`
4. **Alterações no repositório** — tabela `arquivo | o que é`
5. **Pendências** — checklist com responsável e prazo

Não omitir decisão nem pendência para encurtar o relatório. Ele é a prova
documentada do processo para a banca.

## Antes de abrir PR

Rodar a validação e só subir se passar:

```bash
python3 scripts/validar.py
```

Ela confere nome de branch, formato dos commits, cobertura do `SUMMARY.md`,
links internos quebrados e segredo vazado.

## Ao responder no GitHub (`@claude`)

- Responder em português, direto ao ponto
- Se a mudança for pequena e clara, abrir PR com ela
- Se for ambígua ou mudar escopo/cronograma, perguntar antes
- Nunca fazer merge nem aprovar PR
