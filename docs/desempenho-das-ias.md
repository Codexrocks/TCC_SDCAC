# Desempenho das IAs

Registro acumulado dos erros que os assistentes cometeram ao longo do TCC, e de
quem os pegou. No fim do projeto, esta página vira o parecer comparativo entre
as ferramentas.

Existe por um motivo prático: **erro de IA é esquecido em minutos.** Ele é
corrigido, o trabalho segue, e no fim do TCC sobra impressão — "o Claude foi
bom", "o Gemini alucinou umas referências" — que não sustenta nada diante da
banca. Registrado na hora, vira dado.

> **Aviso de método.** Boa parte deste registro é escrita pela própria IA que
> errou, o que é um viés óbvio. Por isso quem revisa o Pull Request confere a
> seção de erros do relatório, e erro que a IA não registrou e uma pessoa notou
> vale mais no balanço. Ver [Uso de IA](uso-de-ia.md).

---

## 1. Como esta página se alimenta

Cada [relatório de sessão](relatorios/README.md) tem a seção **Erros da IA e
correções**. As linhas de lá são consolidadas aqui.

| Campo | O que registra |
|---|---|
| **Erro** | O que a IA fez de errado, em uma frase |
| **Tipo** | `sintaxe` · `conteúdo` · `defeito latente` · `processo` · `desperdício` |
| **Como apareceu** | O sintoma — o que se viu antes de saber a causa |
| **Correção** | O que foi feito |
| **Quem pegou** | `a própria IA` · `a pessoa` · `o check` · `a revisão do PR` |

**Quem pegou** é a coluna que carrega a conclusão do estudo: ela mede quanto a
supervisão humana pesou de fato, em vez de quanto se supõe que pesou.

## 2. Critérios da comparação final

Definidos **agora**, no começo, e não no fim — critério escolhido depois dos
dados é critério escolhido para caber neles.

| Critério | Como se mede |
|---|---|
| Densidade de erro | Erros por sessão, e por tipo |
| Autocorreção | Proporção pega pela própria IA, contra a pega por humano ou check |
| Gravidade | Quantos eram `processo` ou `defeito latente` — os que sobrevivem à sessão |
| Fabricação | Quantas vezes inventou referência, dado ou resultado |
| Aderência | Quantas vezes ignorou uma regra escrita no [`AGENTS.md`](../AGENTS.md) |
| Retrabalho | Iterações até a entrega ficar de pé |

Comparar ferramentas exige cuidado: elas foram usadas em tarefas diferentes, por
pessoas diferentes. **O número bruto não compara** — a leitura precisa dizer em
que contexto cada uma trabalhou.

---

## 3. Registro

### Sessões 01 a 03 — Claude

| Erro | Tipo | Como apareceu | Correção | Quem pegou |
|---|---|---|---|---|
| `.github/CODEOWNERS` apontava para o time `@Codexrocks/lideranca`, que nunca foi criado | processo | Nenhum sintoma visível: o GitHub silenciosamente ignorava o arquivo inteiro, então nenhuma regra de revisão valia | Passou a apontar para `@DaviSoaresDilly`; conferido com `gh api .../codeowners/errors` | a própria IA, na sessão 04 |

> Este passou por três sessões antes de alguém notar. Foi criado com aparência
> de funcionar — e arquivo quebrado que parece certo é o pior caso.

### Sessão 05 — Claude Opus 5

| Erro | Tipo | Como apareceu | Correção | Quem pegou |
|---|---|---|---|---|
| Heredoc do shell quebrado por aspas no conteúdo | sintaxe | `unexpected EOF while looking for matching '` ao escrever `usabilidade.md` | Passou a escrever o arquivo pela ferramenta de escrita, sem shell no meio | a própria IA |
| String Python sem `r"..."`, com escape `\S` inválido | sintaxe | `SyntaxWarning` e a edição abortou na asserção | Reescrito com raw string | a própria IA |
| Comentário HTML aninhado no template de PR | conteúdo | Nenhum na hora: o primeiro `-->` fecharia o comentário externo e vazaria texto solto no formulário de todo PR | Removido o aninhamento | a própria IA |
| Seção "Por que declarar a IA" caiu depois do separador, órfã entre duas seções | conteúdo | Estrutura de cabeçalhos fora de ordem no guia | Movida para dentro da seção 3 | a própria IA |
| O guia ensinava `git commit` **sem** a linha `Assistido-por:` | conteúdo | Nenhum: quem copiasse o exemplo levaria check vermelho — justamente quem nunca usou GitHub | Exemplo corrigido, com nota explicando o segundo `-m` | a própria IA |
| `atividade.py` checava `len(campos) < 5` e acessava `campos[5]` | defeito latente | Nenhum: funcionava por sorte com a tabela atual do cronograma | Limite corrigido para `< 6` | a própria IA |
| Escreveu `@claude` literal nos comentários dos PRs, só para explicar que ele existe | desperdício | Duas execuções do workflow na aba Actions, sem ninguém ter pedido nada | Documentada a armadilha no `processo.md`; comentários seguintes evitam a menção | a própria IA |
| PR #2 aberto sem check nenhum | processo | O PR nasceu `CLEAN` e mergeável na hora, sem revisão | `validacao.yml` passou a rodar em todo PR, não só nos que miram a `main` | a própria IA |
| **Workflows rodavam os verificadores a partir do código do próprio PR** | processo | Nenhum sintoma: tudo verde. Um PR que editasse `scripts/governanca.py` faria o próprio check que deveria barrá-lo passar | Workflows passaram a usar `scripts/*.py` da base; limite residual documentado | **a pessoa** — só apareceu porque o Davi pediu a auditoria |
| Primeiros testes davam falsa segurança | processo | 66 testes verdes, mas a mutação `if False:` desligava a checagem de IA sem quebrar nenhum | Testes de `checar_commits` sobre um repositório git de verdade | a própria IA, via teste de mutação |
| Data em UTC no `configuracao.md` | conteúdo | "04/09/2026" para um cadastro feito às 21h33 de 03/09 em Brasília, inconsistente com a numeração das sessões | Padronizado no fuso local | a própria IA |
| `git add -A` repetido colapsou dois commits temáticos em um | processo | Segundo commit saiu vazio: "nothing to commit" | Nenhuma: o conteúdo estava correto e reescrever histórico enviado é proibido. Registrado | a própria IA |
| Reescrita desnecessária de `docs/README.md` por uma condicional supérflua | desperdício | Aviso de conversão de fim de linha num arquivo que ninguém pediu para tocar | Sem efeito — o git normalizou e nada entrou no commit | a própria IA |


> **O mesmo erro, duas vezes na mesma sessão.** O escape sem raw string
> reapareceu horas depois, justamente ao escrever a linha da tabela que descreve
> esse erro. Vale como dado, não como piada: a IA **não aprendeu dentro da
> própria sessão** — corrigiu o caso, não o hábito. Se o padrão se repetir com
> as outras ferramentas, é achado para a discussão do artigo.

---

## 4. Balanço parcial

Fechado em 03/09/2026, ainda na fase de configuração.

| Tipo | Ocorrências |
|---|---|
| processo | 5 |
| conteúdo | 4 |
| sintaxe | 2 |
| desperdício | 2 |
| defeito latente | 1 |
| **Total** | **14** |

| Quem pegou | Ocorrências |
|---|---|
| a própria IA | 13 |
| a pessoa | 1 |
| o check | 0 |
| a revisão do PR | 0 |

### O que estes números ainda **não** dizem

Treze de quatorze pegos pela própria IA parece um resultado excelente, e seria
leitura errada. Três ressalvas, todas importantes:

1. **A rede de segurança humana ainda não foi exercitada.** Nenhum Pull Request
   foi revisado até aqui, e o check `Governança` nem era obrigatório. Zero em
   "o check" e zero em "a revisão do PR" não é elogio à IA — é ausência de
   oportunidade.
2. **O erro mais grave foi o único que a IA não pegou sozinha.** Os workflows
   rodando o verificador do próprio PR anulavam toda a governança construída na
   mesma sessão. Ele só apareceu porque o Davi perguntou *"em que podemos
   melhorar?"*. Sem a pergunta, teria entrado na `main`.
3. **O que a IA pega sozinha é o barato.** Sintaxe, formatação, inconsistência
   de data — coisas que aparecem na próxima linha de saída. O que escapa é o
   estrutural: o `CODEOWNERS` quebrado sobreviveu a três sessões, e o buraco dos
   workflows sobreviveu até uma provocação direta.

A hipótese a testar no resto do TCC é essa: **a IA se corrige bem no detalhe e
mal no estrutural.** Se ela se sustentar até dezembro, é um achado que vale
discussão no artigo.

---

## 5. Parecer final

<!-- A preencher na S15 (04–10/12), com o TCC fechado. -->

Escrever ao fim do projeto, com os dados acumulados acima:

- Comparação entre as ferramentas usadas, sob os critérios da seção 2
- Em que tipo de tarefa cada uma se saiu melhor e pior
- Se a hipótese da seção 4 se sustentou
- O que a equipe faria diferente

> Não escreva este parecer antes da S15, e não peça a uma IA que escreva o
> parecer sobre si mesma sem que uma pessoa confira linha a linha.

---

## 6. Onde está o resto

- [Uso de IA](uso-de-ia.md) — a política e o que se declara
- [`AGENTS.md`](../AGENTS.md) — as regras como os assistentes leem
- [Relatórios](relatorios/README.md) — o registro sessão a sessão
