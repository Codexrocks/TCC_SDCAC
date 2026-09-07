# Templates

Modelos oficiais para a entrega do artigo. **Arquivo de terceiro** — não é
material da equipe, e não deve ser editado aqui.

| Arquivo | O que é |
|---|---|
| `COBEM-2025-template.docx` | Template oficial da ABCM, 28ª edição do COBEM. O arquivo de exemplo dentro dele se chama `COB-2025-XXXX` |

O que ele exige está lido e traduzido em
[`docs/cobem.md`](../docs/cobem.md) — margens, fontes, número de páginas,
estilo de citação. **Consulte a página; use o arquivo para diagramar.**

## Por que esta pasta fica na raiz

Não é organização, é segurança.

O GitBook **escreve** em `artigo/`, e escreve reformatando: em 06/09/2026 ele
exportou os seis capítulos com todos os comentários HTML apagados. Um `.docx`
ali dentro ficaria exposto ao mesmo tratamento, e ninguém sabe o que a
normalização faz com um binário que ela não entende.

`docs/` seria seguro — o GitBook só lê de lá. A raiz é mais seguro ainda: está
**fora dos dois espaços**, então nenhuma sincronização passa por aqui.

## Ao trocar o template

Quando o template do COBEM 2027 for publicado:

1. Acrescente o novo arquivo **ao lado** do antigo, não por cima
2. Atualize a tabela acima e a
   [página do COBEM](../docs/cobem.md), lendo o arquivo novo
3. Só apague o antigo quando o artigo estiver diagramado no novo

O `.gitattributes` da raiz marca `.docx` como binário. Sem isso, o git no
Windows pode tentar converter fim de linha dentro do arquivo e corrompê-lo —
estrago que só aparece na véspera da entrega.
