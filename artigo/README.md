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

**Referência só entra se você leu a fonte.** Enquanto não conferir, escreva na
linha:

```markdown
<!-- FALTA CITAÇÃO -->
```

A validação deixa passar; a banca não. Modelo de linguagem inventa referência
plausível — autor real, revista real, ano real, artigo que não existe.

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
