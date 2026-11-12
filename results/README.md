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

Os dois são **gravados pelo avaliador**, nunca editados à mão. Corrigir um
número aqui sem reexecutar seria exatamente o que a pasta existe para impedir.

Como reproduzir: [execução do experimento](../docs/execucao-do-experimento.md).

## O que está aqui hoje

### `semente-1` — primeira execução sobre dado gerado · 11/11/2026

| | |
|---|---|
| Gerador | escala cheia, 250 funcionários, 365 dias a partir de 01/01/2026, semente 42 |
| Eventos gerados | 1.905.111, em 124 episódios |
| Janela de treino | 01/01 a 31/03/2026 — os três meses da **D-24** |
| Janela de avaliação | 01/04 a 31/12/2026 — 1.435.546 eventos, 2.638 maliciosos |
| Configurações | **as quatro** |
| Limiar de operação | 20, o teto da faixa normal do preset. **Não calibrado** |
| `code_sha` | `5729695`, registrado em cada execução pelo próprio executor |

**Três ressalvas que o artigo precisa repetir, e não esconder:**

1. **Uma semente só.** A **D-13** pede tratamento estatístico sobre múltiplas
   sementes, e uma execução por configuração não distingue ganho sistemático de
   variação de amostragem. É o que a Seção 3.7 descreve e o que falta rodar
2. **O limiar não foi calibrado.** No corte 20 as três configurações alarmam em
   um quinto do log, com precisão abaixo de 1%. A comparação que tem sentido
   hoje é a de **FPR a revocação fixa**, não a do limiar de operação
3. **A C3 rodou sem a parcela de postura em 5,5% dos eventos.** O gerador
   escreve estado diário de equipamento só para notebooks, e **79.456 eventos**
   de celular e de origem externa foram pontuados sem ela, com a ausência
   registrada em cada nota. Pela decisão de 11/11/2026 a D3 pontua a conduta e
   deixa a postura como não avaliada, em vez de interromper — o efeito é
   subestimar essa parcela nos eventos afetados, e portanto **conservador**
4. **A C3 não é operável no limiar 20.** Ela alerta sobre 99,8% do registro: a
   exposição acumulada cresce ao longo da janela e empurra quase toda nota acima
   do corte. A comparação que vale para ela é a de revocação fixa
5. **962 riscos anteriores ficaram fora da janela de exposição** por terem o
   mesmo instante do evento avaliado. O desenho exclui o evento corrente, e na
   resolução de segundo o irmão de mesmo instante não se distingue dele. Mesmo
   sentido conservador
