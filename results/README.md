# Resultados de execução

**Toda tabela da [Seção 4](../artigo/04-resultados.md) sai daqui.** Número que
não esteja num `metricas.json` desta pasta não entra no artigo — é a regra que o
[`artigo/README.md`](../artigo/README.md) enuncia, e esta pasta é o outro lado
dela.

Uma pasta por semente. Em cada uma:

| Arquivo | O quê |
|---|---|
| `metricas.json` | O dado. É o que a Seção 4 cita |
| `relatorio.md` | A leitura dele, com as tabelas prontas para colar |
| `procedencia.txt` | A semente do gerador e as checagens dele, como ele as imprimiu |

Os três são **gravados pela execução**, nunca editados à mão. Corrigir um número
aqui sem reexecutar seria exatamente o que a pasta existe para impedir.

Na raiz, o agregado das dez:

| Arquivo | O quê |
|---|---|
| `agregado.json` | Média, desvio-padrão e Wilcoxon pareado de cada métrica |
| `agregado.md` | As tabelas do agregado, prontas para a Seção 4 |

Como reproduzir: [execução do experimento](../docs/execucao-do-experimento.md).

## O que está aqui hoje

### Dez sementes · 12/11/2026

Dez execuções independentes, cada uma com população própria, as quatro
configurações e o mesmo limiar. É o desenho que a Seção 3.7 do artigo descreve e
o que a **D-13** cobra.

| | |
|---|---|
| Sementes do gerador | **42 a 51** — `semente-N` usa a semente `41 + N` |
| Gerador | escala cheia, 250 funcionários, 365 dias a partir de 01/01/2026 |
| Eventos pontuados por semente | **1.436.275 ± 9.681**, dos quais **2.583 ± 54** maliciosos |
| Janela de treino | 01/01 a 31/03/2026 — os três meses da **D-24** |
| Janela de avaliação | 01/04 a 31/12/2026 |
| Configurações | **as quatro**, em todas as dez |
| Limiar de operação | 20, o teto da faixa normal do preset. **Não calibrado** |

> **Onde está a semente de cada execução.** O `run_id` do `metricas.json` **não
> é** a semente: é o número da execução dentro do conjunto gerado, e cada
> semente tem o seu próprio conjunto começando em 1 — as dez trazem `run_id`
> igual a 1. Quem guarda a semente do gerador é o `procedencia.txt` de cada pasta,
> na linha `run 1 (seed M)`. O agregado identifica cada execução pelo **nome da
> pasta**, por isso, e recusa a mesma pasta contada duas vezes.

**A semente 42 foi executada duas vezes**, e as duas deram o mesmo resultado:
a execução avulsa de 11/11 e a `semente-1` desta série produzem `metricas.json`
idênticos em **todos** os números, diferindo apenas no `scoring_run_id` interno,
porque a primeira pontuou a C3 numa chamada separada. É uma verificação de
determinismo, não uma coincidência: mesma semente, mesmo resultado.

**Os dados brutos não estão aqui.** Cada semente gera cerca de 3,7 GB entre log
e banco de arquivos, e as dez somariam 37 GB — o procedimento apaga os brutos
depois de avaliar e guarda só o que esta pasta mostra. Regerar é determinístico:
a mesma semente reconstrói o mesmo dado.

### O que o agregado diz, em três linhas

**A direção da pergunta de pesquisa se confirma com significância.** A C2 tem
FPR menor que a C0 em **todos os nove** níveis de revocação, com p = 0,0020 em
cada um — o menor p-valor que dez pares podem produzir num teste bilateral
exato. A 0,20 de revocação são 0,40% contra 18,44%.

**A base de regras fixas não alcança revocação de 0,40.** Em todas as dez
sementes a C0 chega lá com FPR de 100% — ou seja, alertando o registro inteiro.
A 0,30 ela fica em 34,55 ± 34,52: o desvio quase do tamanho da média revela que
em parte das sementes aquele nível só é alcançável assim.

**A quarta dimensão não melhora o ruído.** Entre C3 e C2 o teste não rejeita a
nula em seis dos nove níveis, e nos três em que rejeita é a **C3 que tem FPR
maior**. O ganho dela aparece na cobertura por episódio, e com o custo de
alarmar em **100%** da família de controle negativo.

## Ressalvas que o artigo precisa repetir, e não esconder

1. **O limiar não foi calibrado.** No corte 20 as três primeiras configurações
   alarmam em cerca de um quinto do registro, com precisão abaixo de 1%. A
   comparação que tem sentido é a de **FPR a revocação fixa**, não a do limiar
   de operação
2. **A C3 não é operável no limiar 20.** Ela alerta sobre 99,84 ± 0,01% do
   registro: a exposição acumulada cresce ao longo da janela e empurra quase
   toda nota acima do corte. A comparação que vale para ela é a de revocação
   fixa
3. **A C3 rodou sem a parcela de postura em parte dos eventos.** O gerador
   escreve estado diário de equipamento só para notebooks, e os eventos de
   celular e de origem externa — 5,5% na semente 42 — foram pontuados sem ela,
   com a ausência registrada em cada nota. Pela decisão de 11/11/2026 a D3
   pontua a conduta e deixa a postura como não avaliada, em vez de interromper;
   o efeito é subestimar essa parcela nos eventos afetados, e portanto
   **conservador**
4. **Riscos anteriores de instante idêntico ficam fora da janela de exposição** —
   962 ocorrências na semente 42. O desenho exclui o evento corrente, e na
   resolução de segundo o irmão de mesmo instante não se distingue dele. Mesmo
   sentido conservador
5. **Dez sementes medem variação de amostragem, não validade externa.** Todas
   saem do mesmo gerador, com o mesmo catálogo de cenários. O que o Wilcoxon
   afasta é a hipótese de que a diferença veio do sorteio; o que ele **não**
   afasta é a de que o gerador seja previsível. Essa ameaça está declarada na
   Seção 3.8 e não se resolve com mais sementes
