# Guia do GitHub — para quem nunca usou

Escrito para quem abriu o GitHub pela primeira vez esta semana. Não pressupõe
nada: nem git instalado, nem terminal, nem saber o que é um commit.

Você **não precisa instalar nada** para trabalhar neste projeto. Dá para
escrever documentação inteira pelo navegador. A parte de instalar o git está no
fim, para quando fizer falta.

---

## 1. Cinco palavras que resolvem tudo

| Palavra | O que é, sem enfeite |
|---|---|
| **Repositório** | A pasta do projeto, que mora no GitHub. É o `Codexrocks/TCC_SDCAC` |
| **Branch** | Uma cópia paralela do projeto, onde você mexe à vontade sem quebrar nada de ninguém. Some depois que o trabalho entra |
| **Commit** | Um "salvar" com bilhete explicando o que mudou. O histórico do projeto é a fila de commits |
| **Pull Request** (PR) | O pedido: "terminei, dá uma olhada e deixa entrar". É onde a conversa acontece |
| **Merge** | O momento em que o trabalho aprovado entra de verdade no projeto |

O caminho é sempre o mesmo: **branch → commit → Pull Request → alguém aprova →
merge**.

A `main` é a versão oficial. Ninguém escreve nela direto — nem o Davi. Tudo
entra por Pull Request. Não é burocracia: é o que faz existir o registro de
quem fez o quê, que a banca vai querer ver.

---

## 2. Aprovar um Pull Request

A tarefa mais comum, e a que destrava o trabalho dos outros. Leva dois minutos.

**1.** Abra o link do PR. Você chega numa página com abas: *Conversation*,
*Commits*, *Files changed*.

**2.** Clique em **`Files changed`**. É aqui que se revisa.

**3.** Leia o que mudou. As cores dizem tudo:

- Linha **verde** com `+` na frente — foi acrescentada
- Linha **vermelha** com `-` na frente — foi removida
- Linha alterada aparece como as duas: a vermelha velha, a verde nova

**4.** O que olhar (não precisa entender cada linha):

- O PR faz o que o título promete?
- Tem alguma senha, token ou chave no meio? Isso nunca pode entrar
- O texto em português está legível e correto?
- Se criaram página nova em `docs/`, ela foi adicionada ao `docs/SUMMARY.md`?
  Sem isso ela não aparece no site

**5.** Achou algo estranho? Passe o mouse na linha, clique no **`+`** azul que
aparece à esquerda e escreva o comentário ali. Fica ancorado naquela linha
exata, e quem escreveu sabe do que você está falando.

**6.** Botão **`Review changes`**, no canto superior direito da lista de
arquivos. Abre uma caixinha com três opções:

| Opção | Quando usar |
|---|---|
| **Comment** | Você comentou, mas não está dizendo sim nem não |
| **Approve** | Está bom, pode entrar |
| **Request changes** | Tem algo que precisa mudar antes |

**7.** Escreva uma linha na caixa de texto e clique em **`Submit review`**.

Pronto. Se você aprovou, o botão de merge destrava — **para o Davi**. Só ele
executa o merge, e é uma trava do GitHub, não combinado.

> **Você não consegue aprovar o próprio PR.** O GitHub não permite, de
> propósito. Por isso todo mundo depende de outra pessoa para avançar.

---

## 3. Escrever documentação pelo navegador

Sem instalar nada. Serve para o referencial teórico, o artigo, qualquer texto.

### Pelo GitBook — o caminho mais confortável

Escreva no [GitBook](https://app.gitbook.com) como escreveria no Word. Ao
salvar, o texto vai parar numa branch chamada `gitbook/docs/documentacao` e um
Pull Request abre sozinho. Você não faz mais nada — só avisa que terminou.

### Pelo GitHub, editando o arquivo

Quando quiser mexer num arquivo específico:

**1.** Abra o arquivo no GitHub, por exemplo `docs/arquitetura.md`.

**2.** Clique no **lápis** (`✏️`), no canto superior direito do arquivo.

**3.** Edite o texto. É Markdown — o mínimo que você precisa:

```markdown
# Título grande
## Subtítulo

Texto normal. **Negrito** com dois asteriscos, *itálico* com um.

- item de lista
- outro item

[link para outra página](equipe.md)
```

**4.** Terminou, clique em **`Commit changes...`**, no alto à direita.

**5.** Aparece uma janela. Preencha assim:

| Campo | O que escrever |
|---|---|
| Mensagem (primeira linha) | `docs: adiciona seção sobre UEBA` — sempre começando com `docs:`, em minúscula, sem ponto final |
| Descrição | Opcional. Se usar, explique **por quê**, não o quê |
| Onde salvar | Escolha **`Create a new branch for this commit`** — nunca a primeira opção |
| Nome da branch | `yasmin/docs/assunto-do-texto` |

> **O nome da branch começa com o seu nome.** É assim que a equipe vê quem está
> trabalhando em quê sem perguntar. Se errar o formato, uma verificação
> automática reprova e o PR não fecha.

**6.** **`Propose changes`** e depois **`Create pull request`**.

**7.** Preencha o formulário que aparece — ele já vem com as perguntas — e
clique em **`Create pull request`** de novo.

**8.** Na direita da página, em *Reviewers*, escolha um colega. Espere a
aprovação e o check verde. Depois avise o Davi para fazer o merge.

---

## 4. O check "Validação"

Alguns minutos depois de abrir o PR, aparece uma caixa no fim da página:

- **Bolinha amarela** — está rodando, espere
- **✅ verde** — passou, pode seguir
- **❌ vermelho** — algo está fora do padrão

Se der vermelho, clique em **`Details`** e leia a última linha. Ela diz o
problema em português, por exemplo:

```
ERRO   docs/meu-texto.md nao esta no docs/SUMMARY.md
```

Nesse caso: edite o `docs/SUMMARY.md` na mesma branch e acrescente a linha da
página nova. O check roda de novo sozinho.

Os erros mais comuns:

| Mensagem | O que fazer |
|---|---|
| `nao esta no docs/SUMMARY.md` | Acrescente a página ao `docs/SUMMARY.md` |
| `branch ... fora do padrao` | Renomeie para `seunome/docs/assunto` |
| `commit ... fora do padrao` | A mensagem precisa começar com `docs:`, `feat:`, `fix:` ou `chore:` |
| `link quebrado` | Um link aponta para arquivo que não existe. Confira o nome |
| `possivel senha literal` | Tem algo parecido com senha no texto. **Avise antes de corrigir sozinha** |

---

## 5. Pelo computador, com o git instalado

Só quando o navegador ficar apertado — por exemplo para mexer em vários
arquivos de uma vez. Não é obrigatório para escrever documentação.

```bash
git clone https://github.com/Codexrocks/TCC_SDCAC.git
cd TCC_SDCAC
```

Depois, o ciclo de sempre:

```bash
git checkout main && git pull origin main
git checkout -b yasmin/docs/meu-assunto
```

Trabalhe nos arquivos. Quando terminar:

```bash
git add .
git commit -m "docs: adiciona seção sobre UEBA"
python3 scripts/validar.py
git push -u origin yasmin/docs/meu-assunto
```

O `validar.py` confere tudo antes de subir. Se ele reclamar, corrija e commite
de novo — é melhor descobrir aqui do que no PR.

Depois é só abrir o PR pelo link que o `git push` imprime.

---

## 6. As regras que valem sempre

1. **Nunca escreva na `main` direto.** O GitHub recusa, então nem dá para errar
2. **Nunca commite senha, token, chave ou arquivo `.env`.** Achou um no
   repositório? **Pare e avise** — não corrija sozinha
3. **Página nova em `docs/` entra no `docs/SUMMARY.md`.** Fora dele, não existe
   para o site
4. **Referência bibliográfica só entra se você leu a fonte.** Enquanto faltar,
   escreva `<!-- FALTA CITAÇÃO -->` na linha. A validação deixa passar; a banca
   não
5. **Uma branch por assunto.** Não junte o referencial teórico com uma correção
   de digitação

---

## 7. Quando der errado

Nada aqui é irreversível. O git guarda tudo, e a `main` está protegida contra
os erros que doem de verdade.

| Situação | O que fazer |
|---|---|
| Errei o texto e já commitei | Edite de novo e commite outra vez, na mesma branch. O PR se atualiza sozinho |
| Abri o PR sem terminar | Deixe aberto e continue commitando na mesma branch |
| Fiz besteira na branch inteira | Feche o PR, apague a branch, comece de novo. Não afeta ninguém |
| Não entendi o que o check quer | Comente no próprio PR marcando `@claude` e descreva o problema. Ele responde ali |
| Escrevi na `main` sem querer | Não conseguiu. O GitHub recusou o envio antes de acontecer |

---

## 8. Onde está o resto

- [Padrões](padroes.md) — branch, commit e PR em detalhe
- [Processo de trabalho](processo.md) — como as ferramentas se encaixam
- [Equipe e papéis](equipe.md) — quem cuida do quê
- [Configuração passo a passo](configuracao.md) — quando algo não funciona
