# Uso de inteligência artificial

Os três integrantes usam IA neste projeto. Esta página diz **como** — e como
qualquer pessoa pode conferir, inclusive a banca.

As regras que os assistentes leem estão em [`AGENTS.md`](../AGENTS.md), na raiz
do repositório. Esta página é a mesma política escrita para gente.

---

## 1. A posição do grupo

Usar IA é **esperado**, não tolerado. Ela redige rascunho, revisa texto, sugere
código, explica conceito e acelera trabalho repetitivo.

O que ela **não** faz: pensar pelo grupo, decidir o escopo, escolher as fontes
ou responder pela banca. Um TCC assistido por IA continua sendo um TCC de três
pessoas — e é isso que precisa aparecer no registro.

A pergunta que a banca faz não é *se* usamos IA. É **o que foi nosso e o que foi
da máquina**. Esta página existe para que a resposta esteja documentada,
verificável e não dependa da memória de ninguém.

## 2. Quem usa o quê

| Pessoa | Assistente | Onde usa |
|---|---|---|
| Davi | Claude (Claude Code) | Repositório, automação, backend |
| Yasmin | <!-- FALTA PREENCHER --> | <!-- FALTA PREENCHER --> |
| Felipe | Claude (Claude Code) | Tratamento, Machine Learning, Análise estatística |

> **Yasmin e Felipe:** preencham a linha de vocês. Vale qualquer assistente —
> Gemini, ChatGPT, Copilot, Grok, Codex. Não existe resposta errada aqui; a
> única resposta errada é deixar em branco.

Trocar de ferramenta no meio do TCC é normal. Atualize a tabela quando trocar.

---

## 3. Como declaramos

Em três lugares, com granularidade diferente. Os dois primeiros são conferidos
por máquina — não dá para esquecer sem o check ficar vermelho.

### No commit

Toda mensagem termina declarando quem ajudou naquela mudança específica:

```
docs: adiciona seção sobre UEBA

Assistido-por: Gemini 2.5 Pro
```

Trabalhou sozinho? Declare também. O silêncio não distingue "não usei" de
"esqueci":

```
docs: corrige erro de digitação na introdução

Assistido-por: nenhuma
```

> Ferramentas que já acrescentam `Co-Authored-By:` sozinhas — Claude Code,
> Copilot — satisfazem a regra sem a linha extra.

### No Pull Request

O template tem a seção **Uso de IA**, com quatro perguntas:

| Pergunta | Por que está aí |
|---|---|
| Qual IA foi usada | Identifica a ferramenta |
| No que ela ajudou | Seja específico: "rascunhou a seção 2", não "ajudou" |
| O que é seu | A parte que você pensou, decidiu, leu ou verificou |
| Conferiu tudo que ela escreveu? | A pergunta que importa |

A última é a que carrega a responsabilidade. **Texto de IA entra no TCC sob a
responsabilidade de quem abriu o PR**, não da IA. "A IA que escreveu" não é
defesa na banca.

### No relatório de sessão

Cada sessão de trabalho com assistente vira um relatório em
[`docs/relatorios/`](relatorios/README.md), com o que foi pedido, o que foi
feito, as decisões e o motivo de cada uma. É o registro mais completo dos três,
e o que mostra o **raciocínio** por trás das escolhas.

Ele traz também a seção **Erros da IA e correções**: o que a IA errou, como foi
corrigido e — a parte que importa — **quem pegou**. Tudo isso é consolidado em
[Desempenho das IAs](desempenho-das-ias.md), que no fim do TCC vira a comparação
entre as ferramentas.

Poucos trabalhos apresentam avaliação empírica do próprio uso de IA. Com quatro
meses de registro e três ferramentas diferentes, esse vira dado primário — e
**registro honesto vale mais que registro limpo**: erro admitido e corrigido
mostra processo funcionando, não incompetência.

---

## 4. O que a IA não faz sozinha

Uma IA executa o que foi pedido e o que as regras já preveem. Fora disso, ela
pergunta — não decide.

**Proibido sempre:** fazer merge, aprovar PR, mexer em ruleset, secret ou
permissão, `push --force`, apagar branch alheia, commitar segredo, alterar
cronograma ou escopo, inventar citação ou dado.

**Precisa de duas pessoas:** mudança nas regras (`AGENTS.md`, `CONTRIBUTING.md`,
`docs/padroes*.md`, `docs/processo.md`) ou nas checagens automáticas
(`.github/`, `scripts/`).

O motivo dessa segunda lista é o que mais importa aqui. Sem ela, bastaria um
Pull Request editando o `validar.py` para desligar todas as travas — e a IA que
escreveu esse PR seria a mesma que sugeriu a mudança. **Duas pessoas precisam
concordar em afrouxar a coleira.** Uma IA pode perfeitamente propor a mudança;
só não consegue aprová-la.

---

## 5. O que nunca é aceitável

- **Referência bibliográfica que a IA produziu e ninguém conferiu na fonte.**
  Modelo de linguagem inventa referência plausível: autor real, revista real,
  ano real, artigo inexistente. Enquanto não conferir, marque
  `<!-- FALTA CITAÇÃO -->` na linha
- **Dado, resultado ou métrica "estimado" pela IA.** Número do TCC sai de
  execução real, registrada em `results/`
- **Assinar como seu um texto que você não leu inteiro.** Se não consegue
  explicar um parágrafo na defesa, ele não pode estar no artigo

---

## 6. Como isso é garantido

Instrução em arquivo de texto é pedido, não trava: qualquer IA pode ignorar. Por
isso cada regra que importa tem uma verificação de verdade atrás.

| Regra | O que realmente impede | Onde |
|---|---|---|
| Declarar a IA no commit | Reprova o check | `scripts/validar.py` |
| Declarar a IA no PR | Reprova o check | workflow **Governança** |
| Duas aprovações para mudar as regras | Reprova o check | workflow **Governança** |
| Não commitar na `main` | GitHub recusa o push | ruleset |
| Só o líder faz merge | GitHub recusa o push | ruleset |
| Sem segredo, branch no padrão | Reprova o check | `scripts/validar.py` |
| Um PR não adultera o próprio verificador | Workflow usa o script da base | `.github/workflows/` |
| Os verificadores não quebram calados | Testes a cada PR | `tests/` |

Nenhuma delas depende de a IA "se comportar bem".

> **Um limite que fica em aberto.** O arquivo do workflow em si vem do Pull
> Request, então um PR pode alterar o próprio workflow. Não há como impedir isso
> tecnicamente no GitHub Actions. O que existe contra esse caso é a dupla
> aprovação em `.github/**` e a visibilidade no diff — defesa em camadas, não
> trava. Vale registrar em vez de fingir que o cerco é perfeito.

---

## 7. O que dizer na defesa

Se a banca perguntar sobre o uso de IA, a resposta não precisa ser ensaiada —
está registrada:

- **"Usaram IA?"** Sim, os três, declarado em cada commit e cada Pull Request
- **"Em quê?"** O histórico do repositório responde por mudança
- **"Como sabemos que vocês entenderam o que foi entregue?"** Todo PR foi lido e
  aprovado por outra pessoa, e o merge passou pelo líder. Nada entrou sozinho
- **"E as referências?"** Só entram conferidas na fonte; o que falta conferir
  está marcado no próprio texto

O repositório é público. Qualquer afirmação desta página pode ser verificada
por quem quiser abrir o histórico.

---

## 8. Onde está o resto

- [`AGENTS.md`](../AGENTS.md) — as regras como os assistentes leem
- [Padrões](padroes.md) — branch, commit e Pull Request
- [Guia do GitHub](guia-github.md) — para quem está começando
- [Relatórios](relatorios/README.md) — o registro sessão a sessão
