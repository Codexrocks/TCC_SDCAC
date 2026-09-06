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

## Norma: ABNT

Confirmado com o orientador em 04/09/2026: o artigo segue as **normas da ABNT**,
e não o template COBEM que o [cronograma](../docs/cronograma.md) menciona. O
**abstract em inglês é obrigatório**, além do Resumo em português.

O Markdown daqui é a **fonte da verdade do texto**; a formatação ABNT é aplicada
na hora de montar o documento de entrega.

Escreva o conteúdo aqui primeiro. Formatar é o último passo, não o primeiro —
texto preso dentro de um `.docx` não é revisável por ninguém e não aparece no
histórico.
