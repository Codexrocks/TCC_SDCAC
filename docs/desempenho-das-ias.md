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

### Sessão 06 — Claude Opus 5

| Erro | Tipo | Como apareceu | Correção | Quem pegou |
|---|---|---|---|---|
| Empurrou um commit no PR #1 sem avisar que isso descartaria a aprovação já existente | processo | A revisão do Felipe virou `DISMISSED` e o PR voltou a `REVIEW_REQUIRED` | Nada a corrigir — o efeito é o desejado da regra. Faltou avisar **antes** e deixar a pessoa escolher o momento | a própria IA, depois do fato consumado |

| Recomendou a branch dedicada para o GitBook sem antes verificar o que o GitBook faz com o conteúdo | processo | Nenhum na hora. Só apareceu na primeira sincronização real, quando ele reformatou 11 arquivos e −982 linhas | Caminho de volta desligado; a branch virou espelho de mão única. Uma rodada inteira de trabalho — branch, workflow, documentação — teve de ser refeita | a própria IA, depois de o Davi mandar investigar |
| Afirmou no corpo do PR #3 que uma aprovação bastava, sem conferir a lista de arquivos protegidos | conteúdo | O check `governanca` reprovou o PR: `docs/processo.md` está na lista e exige duas | Corpo do PR corrigido | **o check** |
| Detectou o Python nos ganchos com `command -v python3`, que no Windows encontra um atalho falso do Microsoft Store | defeito latente | Os sete casos de teste do gancho reprovaram, inclusive os corretos: o "python3" achado não era Python, só um convite para instalar da loja | Cada candidato passou a ser **executado** antes de ser aceito, e `py` entrou na lista | a própria IA, ao testar o gancho antes de entregá-lo |

| Quebrou o heredoc do shell com aspas no conteúdo — **pela terceira vez na mesma sessão** | sintaxe | `unexpected EOF while looking for matching '` ao criar as seções do artigo | Passou a escrever pela ferramenta de escrita | a própria IA |

| A checagem de declaração de IA aprovava template em branco quando o corpo vinha com CRLF | processo | O PR #5, o primeiro aberto por outra pessoa, passou no check com os quatro campos vazios | `sem_comentarios` passou a normalizar o fim de linha; cinco testes com o formato real do GitHub | a pessoa — o Davi mandou investigar por que o PR passou |
| Tornou obrigatório um check que dispara duas vezes e acumula resultados | processo | O PR #3 ficou travado com tudo aprovado: o GitHub soma os check runs e o rollup dava FAILURE por causa de execuções antigas | Runs antigos re-executados na hora. **Correção estrutural em 04/09:** o resultado virou *commit status*, que vale pelo mais recente por contexto | a pessoa — travou no merge dela |
| Gancho `commit-msg` barrava commit de merge | conteúdo | `git merge origin/main` de rotina foi interrompido pelo gancho pedindo `Assistido-por:` | Sai antes quando existe `MERGE_HEAD`, espelhando o `--no-merges` do validador | a própria IA, ao tropeçar nele |
| Comentou o PR #5 com uma correção longa, e o pedido concreto ficou enterrado nela | processo | O Felipe fechou o PR 45 segundos depois e abriu o #7 sem as quatro respostas que o comentário pedia. O texto foi lido; o pedido dentro dele, não | Nada a desfazer. O erro é de proporção: três seções e uma tabela para pedir quatro linhas | a pessoa — pelo que fez em seguida, não por um aviso |
| **Concluiu, a partir do fechamento do PR, que o Felipe tinha desistido** | conteúdo | Registrou nesta mesma tabela que o comentário "levou o autor a fechar o próprio PR". Onze minutos depois ele abriu o #7, refazendo o trabalho por conta própria | Linha reescrita. A causa era outra: ele fechou para **recomeçar**, não para abandonar | a própria IA, ao ver o PR #7 aparecer |
| Escreveu um assunto de commit com 73 caracteres, um a mais que o limite da própria regra | sintaxe | `aviso  commit e32a05d4: assunto com 73 caracteres (limite 72)` na execução seguinte do validador | Nenhuma — o commit ficou. Reescrever o histórico para esconder um aviso do próprio verificador seria pior que o aviso | **o check** |

> **O gancho era mais rigoroso que o próprio check que ele imita.** O
> `validar.py` ignora commits de merge desde sempre; o gancho, escrito para
> "reaproveitar as mesmas regras", não reproduziu essa parte. Copiar a intenção
> não é o mesmo que copiar o comportamento.

> **Três vezes o mesmo erro, no mesmo dia.** Já havia acontecido ao criar
> `usabilidade.md` e ao editar o `validar.py`. A IA corrige o caso e volta a
> cometê-lo minutos depois: ela não retém a correção dentro da própria sessão.
> Se o padrão se repetir com Gemini e Copilot, é achado para a discussão do
> artigo; se for só aqui, é característica desta ferramenta.

> O tipo mais incômodo de erro: a IA **sabia**. Ela mesma configurou
> `dismiss_stale_reviews_on_push` na sessão 04 e escreveu em `configuracao.md`
> que *"a aprovação cai a cada novo commit"*. Conhecer a regra e não aplicar a
> consequência ao próprio ato é diferente de não conhecer — e é o que a coluna
> **quem pegou** existe para tornar visível.

---

## 4. Balanço parcial

Fechado em 04/09/2026, ainda na fase de configuração.

| Tipo | Ocorrências |
|---|---|
| processo | 10 |
| conteúdo | 7 |
| defeito latente | 2 |
| sintaxe | 3 |
| desperdício | 2 |
| **Total** | **24** |

| Quem pegou | Ocorrências |
|---|---|
| a própria IA | 18 |
| **a pessoa** | **4** |
| o check | 2 |
| a revisão do PR | 0 |

> **O primeiro erro pego por uma máquina.** O check `governanca` reprovou uma
> afirmação que a IA fez sem verificar — que uma aprovação bastaria no PR #3.
> É a rede de segurança saindo do zero, e vale mais que qualquer autocorreção:
> não dependeu de a IA decidir olhar de novo.

### O que estes números ainda **não** dizem

Dezoito de vinte e quatro pegos pela própria IA parece um resultado excelente,
e seria leitura errada. As ressalvas abaixo importam mais que a proporção:

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
4. **"Pego pela própria IA" às vezes quer dizer "pego tarde demais".** O erro da
   sessão 06 foi percebido depois de já ter descartado a aprovação de alguém.
   Detectar não é o mesmo que evitar, e a tabela ainda não distingue os dois —
   vale considerar uma coluna a mais se o caso se repetir.
5. **A conta de "quem pegou" virou.** Os três erros mais graves do dia — o
   verificador adulterável, o falso negativo do CRLF e o check que se
   auto-bloqueia — **foram todos pegos por uma pessoa**, não pela IA. Dois
   deles só apareceram porque o Davi perguntou "por que isso passou?" em vez de
   aceitar o verde. A autocorreção da IA continua alta em número e baixa em
   gravidade.
6. **Testar antes de entregar pega o que a leitura não pega.** O gancho de
   commit parecia certo e teria falhado na máquina de todo mundo: no Windows,
   `command -v python3` encontra um atalho da Microsoft Store que não é Python.
   Nenhuma revisão de código pegaria isso — só rodar. Vale como contraponto ao
   item anterior: a IA erra menos quando executa do que quando raciocina sobre
   o que aconteceria.
7. **O erro mais caro não foi técnico, foi de investigação.** A IA ofereceu três
   opções para o GitBook sem ter verificado o que o produto faz com o conteúdo.
   A escolha foi tomada com informação incompleta, e uma rodada inteira de
   trabalho precisou ser refeita. Bastava uma consulta à documentação — que ela
   só fez quando mandaram. **Ela sabe pesquisar; o que faltou foi julgar que
   precisava.**
8. **Nenhuma métrica aqui mede se a mensagem chegou.** O comentário no PR #5
   estava correto em cada parágrafo: explicava a causa, assumia a culpa do
   guia, admitia o defeito do check. Tinha três seções, uma tabela e um pedido
   de quatro linhas no meio. O Felipe leu, fechou o PR e abriu outro — **sem as
   quatro respostas.** O texto foi entregue; o pedido, não. A IA otimiza para
   completude, e completude enterra a única frase que exigia ação.
9. **E a IA leu errado a reação.** Do fechamento em 45 segundos ela concluiu
   desistência, e escreveu isso nesta tabela como fato. Onze minutos depois o
   PR #7 apareceu, refazendo o trabalho. **A IA inferiu estado emocional de um
   dado de log e registrou a inferência como observação** — num documento cuja
   função é justamente separar as duas coisas.

Três hipóteses a testar no resto do TCC:

1. **A IA se corrige bem no detalhe e mal no estrutural.**
2. **A IA calibra o conteúdo e não calibra o efeito.** Acerta o que dizer e
   erra quanto dizer, para quem e em que momento.
3. **A IA confunde o que observou com o que deduziu**, e a diferença só
   aparece quando a realidade contradiz a dedução.

Se as três se sustentarem até dezembro, valem discussão no artigo.

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
