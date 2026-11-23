# De onde vem cada número da apresentação

Os números dos slides vêm do artigo e de [`results/agregado.md`](../results/agregado.md), exceto os que são **cálculo
dos autores**, derivados abaixo, e os que são contagem de outras páginas do repositório. O roteiro avisa, na fala, quando
um número é cálculo e não medida.

## A precisão implícita do slide 4 (cálculo, não medida)

O slide 4 aplica a falácia da taxa-base (Axelsson, 2000) para mostrar **por que a FPR sozinha engana**:

`P = TPR·p / (TPR·p + FPR·(1 − p))`

| Entrada | Valor | Origem |
|---|---|---|
| p, a proporção de eventos maliciosos | **0,18%** | 2.583 maliciosos ÷ 1.436.275 eventos por semente = 0,1798% (`results/agregado.md`, contagens por semente; a coluna da C3 mostra 0,18 ± 0,00) |
| TPR (revocação) | **0,20** | A revocação em que a FPR da tabela de resultados é lida (`results/agregado.md`) |
| FPR a revocação 0,20 | C0 18,44%, C1 6,03%, C2 0,40%, C3 0,54% | `results/agregado.md` |

Resultado: C0 0,20% (1 em 513), C1 0,59%, C2 8,26% (1 em 12), C3 6,26%. É conta dos autores para ilustrar o efeito.
**Não é a precisão medida do experimento.** A precisão medida, no limiar de operação, é C0 0,32% e C2 0,57%
(`results/agregado.md`, linha `precisao`; `artigo/04-resultados.md`). O slide 4 usa o número calculado porque o ponto dele
é a comparação **à mesma revocação**, que é o desenho do experimento (FPR a revocação fixa). Por isso o slide traz o calculado, e o medido está no artigo.

## Contagens que não vêm de `results/`

| Número no slide | Origem |
|---|---|
| 20 achados na avaliação heurística, nenhum de severidade 4 (slide 22) | [`docs/insumos/avaliacao-heuristica-davi-v1.md`](../docs/insumos/avaliacao-heuristica-davi-v1.md) e `artigo/04-resultados.md`, seção 4.4 |
| Revisão de segurança: 7 achados, 3 corrigidos (slide 23) | [Relatório da sessão 56](../docs/relatorios/2026-11-21-sessao-56.md) |
| Duas afirmações de IA que não se sustentaram na fonte (só na resposta da banca sobre IA, no `roteiro.md`; não está mais em slide) | [Relatório da sessão 58](../docs/relatorios/2026-11-21-sessao-58.md) |
| 21 referências conferidas (slide 27) | [Relatório da sessão 55](../docs/relatorios/2026-11-21-sessao-55.md); lista em `artigo/referencias.md` |
| Linhas de código e de testes, 765 testes | Contagem do repositório na sessão de 22/11 (`wc` e `pytest`); muda a cada commit |

## Os números da conclusão (slides 25 e 26)

Todos vêm de `results/agregado.md` e do artigo: FPR de 18,44%, 6,03%, 0,40% e 0,54% (C0, C1, C2, C3) a revocação 0,20; cobertura
longitudinal de 35,0% a 100,0%; alarme sobre atividade legítima de 75,8% (C0) e 96,0% (C2); critério de 45 alertas falsos por turno
cumprido na C2 em 7 de 10 sementes; p = 0,0020 (piso do Wilcoxon exato com dez sementes). A leitura da D3 como segundo estágio de
triagem é a da seção 4.5 do artigo.

## As paráfrases de autores

As afirmações atribuídas a cada autor nos slides 5 a 7 são as do **artigo** (seções 2 e 3.7 e 3.8), que citam as obras de
`artigo/referencias.md`. Os slides **não acrescentam** afirmação nova sobre Demšar, Sommer e Paxson ou qualquer outro:
repetem o que o artigo diz. Nenhuma página ou trecho da obra foi conferido a mais para a apresentação. Quem quiser citar
página, na defesa, precisa abrir a obra.

## Como gerar de novo

O `.pptx` e o PDF são gerados pelos scripts de [`gerador/`](gerador/README.md), a partir de `gerador/roteiro.json` (a fala, as
palavras-chave e os tempos) e de `artigo/referencias.md`. Corrigir um texto no `roteiro.json` ou no `gerar.py` e gerar de novo
mantém o `.pptx`, as notas do apresentador, o `roteiro.md` e o PDF iguais entre si.
