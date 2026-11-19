# Templates

Modelos oficiais para a entrega do artigo. **Arquivo de terceiro** — não é
material da equipe, e não deve ser editado aqui.

| Arquivo | O que é | Vale? |
|---|---|---|
| **`orientacoes-tcc-reuniao-02.pdf`** | Orientações do professor, 2ª reunião. Diz o formato, a extensão, a estrutura e os prazos | **Sim — é a fonte** |
| **`COBEM-2026-modelo-do-professor.docx`** | **O arquivo que o professor distribui**, entregue pelo Davi em 18/11/2026 sob o nome *Modelo Formato COBEM* | **Sim — é o template da entrega** |
| `COBEM-2025-template.docx` | Template da ABCM, 28ª edição. Encontrado pela equipe em 07/09 | **Mesmo conteúdo** do de cima — ver abaixo |
| `CREEM-2026-template.docx` | Evento irmão da ABCM. Foi tratado por engano como sendo o do professor em 23/09 | Não |

### O que o arquivo do professor revelou, em 18/11/2026

**O modelo que o professor distribui é, no conteúdo, o mesmo COBEM 2025 que a
equipe já tinha.** Não é parecido: é igual. Conferido parágrafo a parágrafo:

| | |
|---|---|
| Parágrafos | **106** nos dois |
| Tabelas | **3** nos dois |
| Texto extraído | **14.036 caracteres**, com **zero** linhas de diferença |

O cabeçalho do próprio arquivo diz `COB-2025-XXXX` e *"28th COBEM"*. Os
tamanhos em disco diferem (455 KB contra 916 KB) porque são salvamentos
distintos do mesmo documento, com metadados e imagens embutidas diferentes.

**A consequência prática é boa:** o artigo foi escrito contra estas regras
desde setembro, e **não há nada a refazer**. O que muda é o nome do risco —
deixa de ser "falta o template" e passa a ser "o template é este, e o artigo já
o cumpre".

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
