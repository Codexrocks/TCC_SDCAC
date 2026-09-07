# O artigo

Esta pasta é **a zona de escrita da equipe**. É o único lugar do repositório
onde o GitBook pode escrever de volta — então dá para redigir o artigo no
GitBook, como se escreve num editor de texto, sem passar por branch e Pull
Request.

Fora daqui, o GitBook só lê. O motivo está em
[Configuração, seção 7](../docs/configuracao.md#7-gitbook-e-a-main-protegida).

> **Aviso que vale a pena entender.** O GitBook normaliza o Markdown ao salvar:
> junta as quebras de linha, realinha tabelas, troca `---` por `***`. Aqui isso
> é aceitável, porque o que importa é o texto. Por isso a divisão existe — para
> a reformatação não alcançar as regras, os workflows e os relatórios.
>
> **O que ele não perdoa é comentário HTML.** Tudo entre `<!--` e `-->`
> desaparece ao salvar. Por isso as instruções destes capítulos são blocos
> `> **A escrever:**` visíveis, e não comentários escondidos: elas precisam
> sobreviver, e quem vai escrever precisa vê-las.

---

## As cinco seções

Estrutura definida pelo professor, conforme o [cronograma](../docs/cronograma.md).

| # | Seção | Quando | Quem |
|---|---|---|---|
| 1 | [Introdução](01-introducao.md) | S2 — **entrega 10/09** | Todos |
| 2 | [Referencial teórico](02-referencial-teorico.md) | S3 e S4 | Yasmin, com Filipe na S4 |
| 3 | [Metodologia](03-metodologia.md) | S5 | Todos |
| 4 | [Resultados e discussão](04-resultados.md) | S12 e S13 | Filipe e Davi, discussão com todos |
| 5 | [Conclusão](05-conclusao.md) | S14 | Todos |
| — | [Referências](referencias.md) | contínuo | Quem citar |

## Divisão de páginas

O artigo inteiro tem **de 6 a 10 páginas**, tabelas e figuras incluídas. É o
limite do [template](../docs/cobem.md), e ele é rígido: trabalho fora do padrão
é desclassificado antes da revisão.

Orçamento combinado para um artigo de **8 páginas**:

| Seção | Páginas |
|---|---|
| Cabeçalho, resumo, palavras-chave, abstract, keywords | 0,5 |
| **1. Introdução** | **1 a 1,5** |
| **2. Referencial teórico** (entra em Fundamentação) | **1,5 a 2** |
| **3. Metodologia** | **2** |
| **4. Resultados e discussão** | **2 a 2,5** |
| **5. Conclusões** | **0,5** |
| Referências e *responsibility notice* | 0,5 |

Três coisas sobre estes números:

**São orçamento, não cota.** Quem terminar em menos devolve o espaço para quem
precisa de mais. O que não existe é passar de 10 no total.

**A Metodologia e os Resultados são o coração do artigo**, e juntos levam
metade dele. É onde está o trabalho que a banca vai avaliar — o resto
contextualiza.

**Quem escrever primeiro tem a régua mais fácil.** Se a Introdução ocupar três
páginas em setembro, alguém vai ter de cortá-la em dezembro, com o texto já
revisado e as referências já casadas. Cortar cedo é barato.

> **Meça no template, não no editor.** Uma página do
> [`COBEM-2025-template.docx`](../templates/COBEM-2025-template.docx) tem
> Times New Roman 10, entrelinha simples, margens de 3 cm no topo e 2 cm nas
> outras. Cabe muito mais texto do que numa página do Word em branco — e muito
> menos do que a contagem de palavras sugere, quando entram figuras.

## Como escrever aqui

**Pelo GitBook** — abra o espaço do artigo e escreva. O texto chega ao
repositório sozinho.

**Pelo GitHub** — como qualquer outra página, pelo
[guia](../docs/guia-github.md). Vale quando você quiser revisar o texto de outra
pessoa com comentário linha a linha, que o GitBook não faz tão bem.

## Duas regras que não mudam aqui

**Referência só entra se você leu a fonte.** Enquanto não conferir, registre a
pendência em [citações pendentes](../docs/citacoes-pendentes.md) — uma linha
dizendo o capítulo, a seção e o que falta.

O marcador **não** vai dentro do artigo, e isso é aprendido na prática: em
06/09/2026 o GitBook exportou os seis arquivos daqui com todos os comentários
HTML apagados, marcadores de citação incluídos. Aviso invisível que some sem
ninguém perceber é pior que aviso nenhum.

Modelo de linguagem inventa referência plausível — autor real, revista real, ano
real, artigo que não existe. A validação não pega isso; a banca pega.

**Número sai de execução real.** Taxa de detecção, falso positivo e MTTD vêm dos
testes registrados em `results/`, nunca de estimativa.

## Formato: COBEM

Confirmado em 07/09/2026 — o registro de 04/09 dizia ABNT e estava errado. O
artigo do TCC sai no **template da ABCM**, e o **abstract em inglês é
obrigatório**, além do Resumo em português.

Três coisas mudam por causa disso, e estão em
[COBEM 2027](../docs/cobem.md#o-que-isto-muda-no-artigo):

1. **O artigo inteiro tem de 6 a 10 páginas**, incluindo tabelas e figuras
2. **O Referencial Teórico não tem seção própria** no COBEM — entra em
   Fundamentação. Continua sendo entrega da 2ª Versão para a instituição
3. **As referências são autor-ano**, não ABNT NBR 6023
4. **O texto é em português**, e só o *abstract* e as *keywords* saem em
   inglês — decidido em 07/09/2026, apesar de o template pedir inglês

O Markdown daqui é a **fonte da verdade do texto**; o template é aplicado na
hora de montar o documento de entrega. Ele está versionado em
[`templates/`](../templates/README.md), para todo mundo diagramar no mesmo
arquivo.

Escreva o conteúdo aqui primeiro. Formatar é o último passo, não o primeiro —
texto preso dentro de um `.docx` não é revisável por ninguém e não aparece no
histórico.
