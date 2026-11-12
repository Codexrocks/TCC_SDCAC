# Execução do experimento, ponta a ponta

Quatro comandos, na ordem. Até 11/11/2026 os dois do meio não existiam, e era
por isso que o experimento rodava sobre *fixture* de dois funcionários enquanto
o gerador produzia 1,9 milhão de eventos que ninguém lia.

```bash
python -m generator --out out                       # 1. gera
python -m ingest --origem out/run_001 --destino dados/semente-1   # 2. traduz
python -m runner --dados dados/semente-1 --run-id 1 \            # 3. pontua
    --treino 2026-01-01:2026-03-31 --avaliacao 2026-04-01:2026-12-31
python -m evaluator --dados dados/semente-1 --gerado out/run_001 \ # 4. mede
    --run-id 1 --limiar 20 --saida results/semente-1
```

> **Nenhum número do artigo se digita à mão.** O passo 4 grava
> `results/<semente>/metricas.json` e um `relatorio.md` com as tabelas prontas.
> O `.json` é o dado; o `.md` existe para conferir sem abrir JSON e para colar
> a tabela na [Seção 4](../artigo/04-resultados.md) sem redigitar. Redigitar é
> como erro de resultado entra.

---

## 1. O gerador — o dado

Escreve CSV em `out/run_NNN/corp/` e o gabarito em `ground_truth/`. Detalhe em
[banco simulado](banco-simulado.md). Em escala cheia: 250 funcionários, 365
dias, **1.905.111 eventos** e **124 episódios**, em pouco mais de um minuto.

A janela de treino são os **três primeiros meses** da **D-24** — e é a mesma
constante que o gerador usa para só injetar cenário depois dela. Treino e
avaliação disjuntos é a **D-17**; passar a mesma janela nas duas é o vazamento
que ela existe para impedir, e é por isso que o executor exige as duas
separadas em vez de derivar uma da outra.

## 2. A ingestão — a tradução

O gerador escreve CSV; o adaptador de `storage/arquivos.py` lê
`catalogo.json`, `eventos.jsonl` e os dois arquivos de estado. `ingest/` é o
elo, e **nada nele inventa dado**: cada campo sai de uma coluna ou de uma
correspondência declarada em `ingest/corp.py`.

**Três desencontros de vocabulário apareceram quando o elo foi construído**, e
nenhum era de formato:

| O quê | O gerador escreve | Os motores esperam |
|---|---|---|
| **Persona** | `day_admin`, `shift_ops`, `sales_traveler`, `hybrid_eng` | `office_daytime`, `shift`, `sales_travel`, `hybrid` |
| **Fuso** | deslocamento fixo, `UTC-3` | chave IANA, `America/Sao_Paulo` |
| **Privilégio** | `privileged`, booleano | `standard`, `elevated`, `admin` |

O do fuso **derrubou a pontuação no primeiro evento**, com
`ZoneInfoNotFoundError: UTC-3` — os motores chamam `ZoneInfo()` em sete lugares,
pelas **D-31** e **D-40**. A conversão é lícita porque nenhum dos dois fusos tem
horário de verão: o Brasil o extinguiu em 2019, e por isso deslocamento fixo e
fuso coincidem o ano inteiro. Os outros dois não quebravam nada — produziriam
nota errada em silêncio, que é pior.

O do privilégio se resolve lendo a primeira linha de `account_state.csv`: o
booleano de `employees.csv` não distingue `elevated` de `admin`, e a C0
distingue.

> **As três correspondências pendem de ratificação do Davi.** Elas estão
> nomeadas em constantes no topo de `ingest/corp.py`, e não escondidas no meio
> de um laço, exatamente para que a ratificação seja possível. Persona ou fuso
> novo no gerador faz a ingestão **recusar**, em vez de adivinhar.

## 3. O executor — as notas

Um laço por configuração, cada uma com o próprio hash e o próprio conjunto de
notas. Em escala cheia, as quatro configurações passeiam por 1,45 milhão de
eventos da janela de avaliação.

> ⚠️ **A C3 ainda não roda sobre dado gerado.** O gerador escreve estado diário
> **só do notebook** — `generator/normal.py`, `device_states` —, e a D3 exige
> estado do equipamento **do evento**, recusando-se a pontuar sem ele: *"sem
> ele, atualização e antivírus sairiam como se estivessem em ordem"*. Eventos de
> celular e de origem externa não têm esse estado. É decisão pendente, não
> defeito de código — ver [o que falta](o-que-falta.md).

## 4. O avaliador — as métricas

É o **único componente que lê `ground_truth/`**. A separação está nas portas de
`detection/ports.py` e no privilégio do banco: o usuário da aplicação não
conecta no gabarito.

As duas grandezas são as da **D-03**, operacionalizadas na seção 1.3 do
[plano](plano.md):

| Grandeza | Métrica |
|---|---|
| **Ruído** | FPR **com a revocação fixada no mesmo nível** nas quatro configurações |
| **Cobertura** | Revocação nos cenários longitudinais — a família `L` |

**Duas unidades de análise, as duas reportadas.** A **D-12** está aberta, e o
próprio plano avisa que um cenário longitudinal "pode render revocação de 0,15
medido por evento e 1,00 medido por episódio". Escolher uma dentro do código
fecharia a D-12 por omissão.

Três leituras que o relatório força, e que valem anotar:

- **Positivo é evento com rótulo `malicious`.** Evento sem rótulo é negativo: o
  gabarito só rotula o que pertence a um episódio
- **A família `N` é benigna por construção.** Alertar um `N` é falso positivo,
  não acerto — é a razão de a família existir
- **FPR de 100% não é lacuna, é resultado.** Toda revocação é alcançável
  baixando o limiar até alertar o log inteiro; a FPR e a fração do log alertada
  é que dizem se o ponto é operável

---

## O que os números de hoje ainda não são

**Uma semente só.** A **D-13** pede tratamento estatístico sobre múltiplas
sementes, e a Seção 3.7 do artigo descreve o desenho. Uma execução por
configuração não distingue ganho sistemático de variação de amostragem —
`--seeds N` no gerador é o que falta rodar.

**Com o limiar padrão.** O corte de alerta usado é o teto da faixa normal do
preset, e ele **não foi calibrado**: no limiar 20 as três configurações alarmam
em um quarto do log. A comparação que tem sentido hoje é a de **FPR a revocação
fixa**, não a do limiar de operação.

**Sem a C3.** Ver o passo 3.
