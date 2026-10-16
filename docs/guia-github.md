# Guia do GitHub — para quem nunca usou

Escrito para quem abriu o GitHub pela primeira vez esta semana. Não pressupõe
git instalado, nem terminal, nem saber o que é um commit.

**Você não precisa instalar nada.** Dá para escrever documentação inteira pelo
navegador; a parte do git fica no fim, para quando fizer falta.

---

## 1. Cinco palavras que resolvem tudo

| Palavra | O que é, sem enfeite |
|---|---|
| **Repositório** | A pasta do projeto, que mora no GitHub: `Codexrocks/TCC_SDCAC` |
| **Branch** | Uma cópia paralela onde você mexe à vontade sem quebrar nada de ninguém |
| **Commit** | Um "salvar" com bilhete explicando o que mudou |
| **Pull Request** (PR) | O pedido "terminei, deixa entrar". É onde a conversa acontece |
| **Merge** | O momento em que o trabalho entra de verdade no projeto |

O caminho é sempre o mesmo: **branch → commit → Pull Request → checks verdes →
merge**.

A `main` é a versão oficial, e ninguém escreve nela direto — nem o Davi. Isso
não é burocracia: é o que faz existir o registro de quem fez o quê, que a banca
vai querer ver.

---

## 2. Escrever pelo navegador

Serve para o referencial teórico, o artigo, qualquer texto. Sem instalar nada.

> **Não escreva pelo site do GitBook.** Ele publica a documentação, mas o
> caminho de volta está desligado e o texto escrito lá **se perde**. O motivo
> está em [Configuração, seção 7](configuracao.md#7-gitbook-e-a-main-protegida).

**1.** Abra o arquivo no GitHub — por exemplo `docs/arquitetura.md` — e clique
no **lápis** (`✏️`), no canto superior direito.

**2.** Edite. É Markdown, e o mínimo é isto:

```markdown
# Título grande
## Subtítulo

Texto normal. **Negrito** com dois asteriscos, *itálico* com um.

- item de lista

[link para outra página](equipe.md)
```

**3.** Clique em **`Commit changes...`**. Aqui vem a parte que já derrubou gente:

> ⚠️ **Os campos vêm preenchidos, e o que vem dentro está errado.** O GitHub
> sugere `SeuNome-patch-1` e `Update arquivo.md`, e os dois reprovam na
> validação. **Apague e escreva por cima.**

| Campo | O que vem | O que você escreve |
|---|---|---|
| Mensagem (1ª linha) | `Update arquivo.md` | `docs: adiciona seção sobre UEBA` — minúscula, sem ponto final, **até 72 caracteres** |
| Descrição | vazio | `Assistido-por: nome da IA` — ou `Assistido-por: nenhuma` |
| Onde salvar | *Commit directly* | **`Create a new branch for this commit`** |
| Nome da branch | `SeuNome-patch-1` | `yasmin/docs/assunto-do-texto` |

> 🔒 **O nome da branch é o único campo sem conserto.** Mensagem de commit e
> corpo do PR você edita à vontade; nome de branch fica preso ao PR desde que
> ele nasce. Errar aqui significa abrir tudo de novo — pare cinco segundos
> neste campo.
>
> Válidos: `yasmin/docs/referencial-teorico` · `filipe/docs/uso-de-ia` ·
> `davi/feat/coletor-de-logs`

**4.** **`Propose changes`**, depois **`Create pull request`**.

**5.** Preencha o modelo que aparece. A seção **Uso de IA** tem quatro campos, e
**nenhum pode ficar vazio**:

```markdown
- **IA usada:** Gemini 2.5 Pro
- **No que ajudou:** revisou a redação da seção
- **O que é meu:** a pesquisa e a escolha das fontes
- **Conferi tudo que a IA escreveu:** sim
```

> As linhas entre `<!--` e `-->` são instruções, não respostas: escreva depois
> dos dois-pontos, apagando o comentário. Não usou IA? `nenhuma` e `não se
> aplica` são respostas válidas — **o silêncio é o único errado.**

**6.** Espere os checks ficarem verdes. Não há aprovação de outra pessoa a
esperar; o merge é do Davi.

**Por que declarar a IA:** usar é esperado, esconder é que é problema. A banca
vai perguntar o que foi seu e o que foi da máquina, e a resposta precisa estar
no registro, não na memória. A última das quatro perguntas é a que carrega a
responsabilidade — o texto entra no TCC no seu nome, não no da IA. Política
inteira em [Uso de IA](uso-de-ia.md).

---

## 3. Ler o que mudou num Pull Request

> Desde 23/09/2026 o trabalho é de uma pessoa só, e **não há aprovação de outra
> pessoa a esperar** — o `Approve` do GitHub saiu do processo. Ler o diff
> continua valendo, e é o que esta seção ensina.

Abra o PR e clique na aba **`Files changed`**. As cores dizem tudo: linha
**verde** com `+` foi acrescentada, **vermelha** com `-` foi removida, e linha
alterada aparece como as duas.

O que olhar, sem precisar entender cada linha:

- O PR faz o que o título promete?
- Tem senha, token ou chave no meio? Isso nunca pode entrar
- Se criaram página nova em `docs/`, ela entrou no `docs/SUMMARY.md`?

Achou algo estranho? Passe o mouse na linha, clique no **`+`** azul à esquerda e
escreva ali. O comentário fica ancorado naquela linha exata.

---

## 4. O check "Validação"

Minutos depois de abrir o PR aparece uma caixa no fim da página: bolinha
amarela está rodando, ✅ passou, ❌ está fora do padrão. No vermelho, clique em
**`Details`** e leia a última linha — ela diz o problema em português.

| Mensagem | O que fazer |
|---|---|
| `nao esta no docs/SUMMARY.md` | Acrescente a página ao `docs/SUMMARY.md`, na mesma branch |
| `branch ... fora do padrao` | Renomeie para `seunome/docs/assunto` — e isso pede PR novo |
| `commit ... fora do padrao` | A mensagem precisa começar com `docs:`, `feat:`, `fix:` ou `chore:` |
| `link quebrado` | Um link aponta para arquivo que não existe |
| `possivel senha literal` | **Avise antes de corrigir sozinha** |
| `falta declarar a IA` | Acrescente `Assistido-por: ...` no corpo do commit |
| `fica 24 h aberto antes de entrar` | O PR mexe nas regras. Espere o prazo e preencha a seção `Arquivo protegido` |

> ⚠️ **A diferença que mais custa caro.** Conteúdo se corrige na mesma branch,
> quantas vezes for preciso. **Mensagem de commit e nome de branch, não** — a
> validação confere *todos* os commits do PR, e um commit novo não apaga o
> anterior. Errou num dos dois: PR novo.

---

## 5. Pelo computador, com o git instalado

Só quando o navegador ficar apertado — vários arquivos de uma vez, por exemplo.

```bash
git clone https://github.com/Codexrocks/TCC_SDCAC.git
cd TCC_SDCAC
git config core.hooksPath .githooks
```

O `core.hooksPath` é uma vez só: com ele o computador confere o commit antes de
gravá-lo, e você descobre o erro na hora em vez de no Pull Request. Precisa de
Python; sem ele o gancho avisa e não atrapalha.

Depois, o ciclo de sempre:

```bash
git checkout main && git pull origin main
git checkout -b yasmin/docs/meu-assunto
git add .
git commit -m "docs: adiciona seção sobre UEBA" -m "Assistido-por: nenhuma"
python3 scripts/validar.py
git push -u origin yasmin/docs/meu-assunto
```

> O segundo `-m` é a declaração de IA, e sem ela o `validar.py` reprova.

O PR se abre pelo link que o `git push` imprime.

---

## 6. As regras que valem sempre

1. **Nunca escreva na `main` direto** — o GitHub recusa, então nem dá para errar
2. **Nunca commite senha, token, chave ou `.env`.** Achou um? **Pare e avise**
3. **Página nova em `docs/` entra no `docs/SUMMARY.md`** — fora dele, não existe
   para o site
4. **Referência só entra se você leu a fonte.** Enquanto faltar, anote em
   [citações pendentes](citacoes-pendentes.md). A validação não confere se a
   fonte existe; a banca confere
5. **Uma branch por assunto** — não junte o referencial com uma correção de
   digitação

---

## 7. Quando der errado

Nada aqui é irreversível. O git guarda tudo, e a `main` está protegida contra os
erros que doem de verdade.

| Situação | O que fazer |
|---|---|
| Errei o **texto** | Edite e commite de novo, na mesma branch. O PR se atualiza sozinho |
| Errei a **mensagem do commit** ou o **nome da branch** | Não tem conserto: feche o PR e abra outro |
| Abri o PR sem terminar | Deixe aberto e continue commitando na mesma branch |
| Fiz besteira na branch inteira | Feche o PR, apague a branch, comece de novo. Não afeta ninguém |
| Não entendi o que o check quer | Comente no próprio PR marcando `@claude` e descreva o problema |
| Escrevi na `main` sem querer | Não conseguiu — o GitHub recusou antes de acontecer |

---

## 8. Onde está o resto

- [Uso de IA](uso-de-ia.md) — o que declarar, e por quê
- [Padrões](padroes.md) — branch, commit e PR em detalhe
- [Processo de trabalho](processo.md) — como as ferramentas se encaixam
- [Equipe e papéis](equipe.md) — quem cuida do quê
- [Configuração passo a passo](configuracao.md) — quando algo não funciona
