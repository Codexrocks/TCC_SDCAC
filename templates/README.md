# Templates

Modelos oficiais para a entrega do artigo. **Arquivo de terceiro** — não é
material da equipe, e não deve ser editado aqui.

| Arquivo | O que é | Vale? |
|---|---|---|
| **`orientacoes-tcc-reuniao-02.pdf`** | Orientações do professor, 2ª reunião. Diz o formato, a extensão, a estrutura e os prazos | **Sim — é a fonte** |
| `COBEM-2026-template.docx` | **Ainda não obtido.** É o que o professor pede | **Falta** |
| `CREEM-2026-template.docx` | Evento irmão da ABCM. Foi tratado por engano como sendo o do professor em 23/09 | Não |
| `COBEM-2025-template.docx` | Template da ABCM, 28ª edição. Encontrado pela equipe em 07/09 | Aproximação da família, até o de 2026 chegar |

O que o template em vigor exige está lido e traduzido em
[`docs/formato-do-artigo.md`](../docs/formato-do-artigo.md) — margens, fontes,
número de páginas, estilo de citação. **Consulte a página; use o arquivo para
diagramar.**

> **Parecidos não é igual, e isso já custou uma volta inteira.** COBEM, CREEM e
> CONEM são eventos irmãos da ABCM, com templates de mesma família e números
> diferentes. Em 23/09 o arquivo do CREEM 2026 foi tratado como sendo o do
> professor, e não era. **Confira o nome do evento contra o que o professor
> escreveu, não contra o que o template parece ser.**

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
