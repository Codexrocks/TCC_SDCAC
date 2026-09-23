# Templates

Modelos oficiais para a entrega do artigo. **Arquivo de terceiro** — não é
material da equipe, e não deve ser editado aqui.

| Arquivo | O que é | Vale? |
|---|---|---|
| **`CREEM-2026-template.docx`** | Template do **XXXII CREEM 2026**, disponibilizado pelo professor em 23/09/2026 | **Sim — é este** |
| `COBEM-2025-template.docx` | Template da ABCM, 28ª edição do COBEM. Encontrado pela equipe em 07/09/2026, antes de o professor se pronunciar | Não. Guardado para rastreabilidade |

O que o template em vigor exige está lido e traduzido em
[`docs/formato-do-artigo.md`](../docs/formato-do-artigo.md) — margens, fontes,
número de páginas, estilo de citação. **Consulte a página; use o arquivo para
diagramar.**

> **Os dois são parecidos e não são iguais.** São eventos irmãos da ABCM, com
> templates de mesma família. A diferença que mais pega é a extensão: o COBEM
> pede 6 a 10 páginas, o CREEM **8 a 12**. Confira sempre pelo arquivo do CREEM.

## Por que esta pasta fica na raiz

Não é organização, é segurança.

O GitBook **escreve** em `artigo/`, e escreve reformatando: em 06/09/2026 ele
exportou os seis capítulos com todos os comentários HTML apagados. Um `.docx`
ali dentro ficaria exposto ao mesmo tratamento, e ninguém sabe o que a
normalização faz com um binário que ela não entende.

`docs/` seria seguro — o GitBook só lê de lá. A raiz é mais seguro ainda: está
**fora dos dois espaços**, então nenhuma sincronização passa por aqui.

## Ao trocar o template

Já aconteceu uma vez, em 23/09/2026. O procedimento que funcionou:

1. Acrescente o novo arquivo **ao lado** do antigo, não por cima
2. Atualize a tabela acima e a
   [página de formato](../docs/formato-do-artigo.md), **lendo o arquivo novo** —
   não presuma que a família de templates é idêntica
3. Só apague o antigo quando o artigo estiver diagramado no novo

O `.gitattributes` da raiz marca `.docx` como binário. Sem isso, o git no
Windows pode tentar converter fim de linha dentro do arquivo e corrompê-lo —
estrago que só aparece na véspera da entrega.
