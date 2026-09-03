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
   *Exceção única, temporária:* enquanto o ruleset da `main` não existir e a
   equipe não tiver acesso ao repositório, commits de configuração podem ir
   direto para a `main` — não há quem aprove um PR. A exceção morre no instante
   em que o ruleset for criado.
2. **Nunca commitar segredo** — `.env`, senha, token, chave, string de conexão.
   Se encontrar um no repositório, pare e avise em vez de corrigir sozinho.
3. **Toda página nova em `docs/` entra no `docs/SUMMARY.md`.** Fora do SUMMARY,
   a página não existe para o GitBook.
4. **Não criar pasta vazia.** Pasta de código só quando houver código nela.
5. **Não inventar conteúdo acadêmico.** Referência bibliográfica, citação, dado
   ou resultado experimental só entram se vierem de fonte verificada. Na dúvida,
   marque `<!-- FALTA CITAÇÃO -->` e avise.
6. **Não alterar o cronograma nem o escopo** sem pedido explícito do Davi.

## Padrão de branch

```
docs/<assunto>     documentação e artigo
feat/<assunto>     código novo
fix/<assunto>      correção
chore/<assunto>    configuração, dependências, manutenção
```

Só minúsculas, números e hífen. Ex.: `docs/referencial-teorico`.

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
