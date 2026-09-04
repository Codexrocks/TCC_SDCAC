# Regras para assistentes de IA — TCC_SDCAC

**Fonte única.** Vale para qualquer assistente de IA usado neste repositório —
Claude, Gemini, Codex, Copilot, Grok, ChatGPT ou o que vier depois. Os arquivos
`CLAUDE.md`, `GEMINI.md` e `.github/copilot-instructions.md` só apontam para
aqui; quem edita regra, edita este arquivo.

Se você é uma IA lendo isto: **leia até o fim antes de tocar em qualquer coisa.**
As seções 3 e 4 dizem o que você não pode fazer sozinho.

---

## 1. Contexto

TCC 2026/2 · Prof. Euzébio D. de Souza · Sistema de Detecção de Comportamentos
Anômalos em Cybersecurity. Equipe de três: **Davi** (líder & backend),
**Yasmin** (cybersecurity), **Felipe** (data & dashboard).

O repositório é **público**. A pasta `docs/` é publicada no GitBook. Tudo que
entra em `docs/` vira site público.

Este é um trabalho acadêmico avaliado por uma banca. A pergunta que a banca faz
sobre IA não é *se* vocês usaram — é **o que foi de vocês e o que foi da
máquina**. Todas as regras deste arquivo existem para que essa resposta esteja
documentada e seja verificável, e não dependa de memória de ninguém.

## 2. Idioma

Português do Brasil em tudo: documentação, commits, PRs, comentários e
respostas. Código e nomes de arquivo em inglês, quando for convenção da
linguagem.

---

## 3. Uso de IA — o que precisa ser declarado

Usar IA neste projeto é **esperado**, não tolerado. Os três integrantes usam.
Esconder o uso é que é problema — e é problema sério num trabalho avaliado.

### Em todo commit

Toda mensagem de commit termina declarando quem ajudou:

```
docs: adiciona seção sobre UEBA

Assistido-por: Claude Opus 5
```

Sem IA nenhuma? Declare também — o silêncio não distingue "não usei" de
"esqueci":

```
docs: corrige erro de digitação na introdução

Assistido-por: nenhuma
```

`scripts/validar.py` reprova commit sem essa declaração. Ferramentas que já
acrescentam `Co-Authored-By:` sozinhas — Claude Code, Copilot — satisfazem a
regra sem precisar da linha extra.

### Em todo Pull Request

O template tem uma seção **Uso de IA** com quatro perguntas. Preencher é
obrigatório, e um workflow reprova o PR se ficar em branco:

- **Qual IA** foi usada
- **No que ela ajudou** — seja específico: "rascunhou a seção 2", não "ajudou"
- **O que é seu** — a parte que você pensou, decidiu, leu ou verificou
- **Você conferiu tudo que ela escreveu?**

A última pergunta é a que importa. Texto de IA entra no TCC sob a
responsabilidade de quem abriu o PR, não da IA.

### O que nunca é aceitável

- Referência bibliográfica que a IA produziu e ninguém conferiu na fonte
- Dado, resultado ou número que a IA "estimou"
- Assinar como seu um texto que você não leu inteiro

---

## 4. O que uma IA não faz sozinha

Você executa **o que foi pedido** e o que estas regras já preveem. Fora disso,
pergunte — não decida.

### Proibido, sempre

| Ação | Por quê |
|---|---|
| **Fazer merge** de qualquer PR | Na `main` só o Davi merge, e o GitHub recusa outras origens |
| **Aprovar PR** | Aprovação é responsabilidade de uma pessoa que leu |
| **Alterar ruleset, secret ou permissão** do repositório | É a própria trava; mexer nela é sair do jogo |
| **`git push --force`** ou reescrever histórico já enviado | Quebra o clone de quem já baixou |
| **Apagar branch de outra pessoa** | Não é sua |
| **Commitar segredo** — `.env`, senha, token, chave, string de conexão | Repositório público. Achou um? **Pare e avise**, não corrija sozinho |
| **Alterar cronograma ou escopo** sem pedido explícito do Davi | Define o TCC |
| **Inventar conteúdo acadêmico** — citação, dado, resultado | Marque `<!-- FALTA CITAÇÃO -->` e avise |

### Precisa de duas pessoas

Mudança nestes arquivos exige **duas aprovações**, não uma:

```
AGENTS.md · CLAUDE.md · GEMINI.md · .github/copilot-instructions.md
CONTRIBUTING.md
docs/padroes.md · docs/padroes-codigo.md · docs/processo.md
.github/**  ·  scripts/**
```

O motivo é direto: são as regras e as checagens automáticas. Sem isso, bastaria
um PR editando o `validar.py` para desligar todas as travas — e a IA que
escreveu o PR seria a mesma que sugeriu a mudança. Duas pessoas precisam
concordar em afrouxar a coleira.

O workflow **Governança** confere isso e reprova o PR sozinho. Você pode
perfeitamente propor a mudança; só não entra com uma aprovação só.

### Na dúvida, pergunte

Se o pedido não está coberto por estas regras e não foi dito explicitamente,
**pergunte antes de fazer**. Entregar o que ninguém pediu custa mais caro que
uma pergunta.

---

## 5. Regras que não se quebram

1. **Nunca commitar direto na `main`.** Sempre branch + Pull Request. O ruleset
   `Proteção da main` recusa o push direto, inclusive o do dono do repositório.
2. **Nunca commitar segredo.** Ver seção 4.
3. **Toda página nova em `docs/` entra no `docs/SUMMARY.md`.** Fora do SUMMARY,
   a página não existe para o GitBook.
4. **Não criar pasta vazia.** Pasta de código só quando houver código nela.
5. **Não inventar conteúdo acadêmico.** Ver seção 3.
6. **Não alterar o cronograma nem o escopo** sem pedido explícito do Davi.
7. **Código segue [`docs/padroes-codigo.md`](docs/padroes-codigo.md)** — Python
   3.12, Ruff, type hints, docstring em português, identificador em inglês, SQL
   parametrizado.
8. **Mexeu no dashboard? Vale [`docs/usabilidade.md`](docs/usabilidade.md)** —
   rótulo textual junto da cor, contraste mínimo de 4,5:1, decomposição do Risk
   Score visível.
9. **Declare a IA** no commit e no PR. Ver seção 3.
10. **Não afrouxe as próprias regras sozinho.** Ver seção 4.

---

## 6. Padrão de branch

```
<autor>/<tipo>/<assunto>
```

Autor: `davi` · `yasmin` · `felipe` · `claude` · `gitbook`.
Tipo: `docs` · `feat` · `fix` · `chore`.

Só minúsculas, números e hífen. Ex.: `yasmin/docs/referencial-teorico`.

A branch de uma IA leva **o nome de quem a está usando**, não o da IA — quem
responde pelo trabalho é a pessoa. A exceção é `claude/`, usada pelo assistente
quando ele age sozinho, por exemplo no relatório semanal automático.

`gitbook/docs/documentacao` é branch permanente do Git Sync e **não se apaga**.

Autor novo precisa entrar na lista `AUTORES` de `scripts/validar.py`.

## 7. Padrão de commit

```
tipo: descrição no imperativo, minúscula, sem ponto final

Corpo opcional, explicando por quê — o diff já mostra o quê.

Assistido-por: <nome da IA, ou "nenhuma">
```

Tipos: `docs` · `feat` · `fix` · `chore`. Máximo 72 caracteres na primeira
linha.

## 8. Pull Request

- Base sempre `main`
- Título no mesmo padrão do commit
- Preencher o template inteiro, **incluindo a seção Uso de IA**
- 1 aprovação — ou **2**, se tocar nos arquivos da seção 4
- **Squash and merge**, sempre (é a única opção que o GitHub oferece)
- **Nunca faça o merge.** Deixe pronto e aprovado, e avise

## 9. Relatório de sessão — obrigatório

Ao fim de **toda** sessão de trabalho, gravar um relatório em
`docs/relatorios/AAAA-MM-DD-sessao-NN.md` usando `docs/relatorios/_modelo.md`,
e adicionar ao `docs/SUMMARY.md` e ao índice em `docs/relatorios/README.md`.

Na ordem: o que foi pedido · o que foi feito · decisões tomadas, com o motivo de
cada uma · alterações no repositório · pendências com responsável e prazo.

Não omita decisão nem pendência para encurtar. O relatório é a prova documentada
do processo para a banca.

## 10. Antes de abrir PR

```bash
python3 scripts/validar.py
```

Confere nome de branch, formato dos commits, declaração de IA, cobertura do
`SUMMARY.md`, links internos quebrados e segredo vazado. Só suba se passar.

## 11. Ao responder no GitHub (`@claude`)

- Responder em português, direto ao ponto
- Mudança pequena e clara: abrir PR com ela
- Ambígua, ou que mexa em escopo, cronograma ou nas regras: **perguntar antes**
- Nunca fazer merge nem aprovar PR

---

## 12. Por que isto é assim

Nada aqui depende de uma IA "se comportar". Instrução em arquivo de texto é
pedido, não trava — qualquer IA pode ignorar, e a próxima versão dela pode
interpretar diferente.

Por isso cada regra que importa tem uma trava de verdade atrás:

| Regra | O que realmente impede |
|---|---|
| Não commitar na `main` | Ruleset do GitHub — recusa o push |
| Só o Davi faz merge | Ruleset — só org admin atualiza a `main` |
| Branch no padrão, sem segredo, SUMMARY em dia | `scripts/validar.py` no check **Validação** |
| Declarar a IA no commit | `scripts/validar.py` |
| Declarar a IA no PR | Workflow **Governança** |
| Duas aprovações para mudar as regras | Workflow **Governança** |
| Os verificadores não podem ser adulterados pelo próprio PR | Workflows usam `scripts/*.py` da base |
| Os verificadores não quebram em silêncio | `tests/`, rodando a cada PR |

### Os verificadores rodam da `main`, não do PR

Um detalhe que parece técnico e é de segurança. O GitHub Actions executa o
workflow **da branch do Pull Request** — foi assim que o check `Governança`
rodou antes mesmo de existir na `main`.

Isso abria um buraco: um PR que editasse `scripts/governanca.py` para sempre
retornar sucesso faria o próprio check que deveria barrá-lo passar verde. Junto
caía toda a validação de segredo, branch e declaração de IA.

Por isso os workflows sobrescrevem `scripts/*.py` com a versão da base antes de
validar. **O PR é julgado pelo verificador vigente, não pelo que ele traz
consigo.** Os testes, esses sim, rodam com o código do PR — o objetivo deles é
justamente pegar quem quebrou um verificador.

### O que ainda não está fechado

Honestidade sobre o limite: **o próprio arquivo `.yml` continua vindo do PR.**
Um Pull Request pode alterar o workflow para não fazer essa substituição. Não há
como impedir isso pelo GitHub Actions comum.

O que sobra contra esse caso é defesa em camadas, não uma trava: alterar
`.github/**` exige duas aprovações, e a mudança aparece no diff de quem revisa.
Por isso a lista de arquivos protegidos inclui os workflows — **quem revisa um
PR que mexe em `.github/` precisa olhar com atenção redobrada.**

### Se a trava e o texto discordarem

A trava está certa e o texto está desatualizado. Corrija o texto, não a trava.

A política completa, escrita para gente e não para máquina, está em
[`docs/uso-de-ia.md`](docs/uso-de-ia.md).
