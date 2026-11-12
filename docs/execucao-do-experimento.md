# Execução do experimento, ponta a ponta

Cinco comandos, na ordem. Até 11/11/2026 os dois do meio não existiam, e era
por isso que o experimento rodava sobre *fixture* de dois funcionários enquanto
o gerador produzia 1,9 milhão de eventos que ninguém lia. O quinto entrou em
12/11/2026, quando passaram a existir dez sementes para agregar.

```bash
python -m generator --out out                       # 1. gera
python -m ingest --origem out/run_001 --destino dados/semente-1   # 2. traduz
python -m runner --dados dados/semente-1 --run-id 1 \            # 3. pontua
    --treino 2026-01-01:2026-03-31 --avaliacao 2026-04-01:2026-12-31
python -m evaluator --dados dados/semente-1 --gerado out/run_001 \ # 4. mede
    --run-id 1 --limiar 20 --saida results/semente-1
python -m evaluator.agregado_cli results/semente-* --saida results/  # 5. agrega
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

> ✅ **A C3 passou a rodar em 11/11/2026**, pela decisão de que a D3 pontua a
> conduta e deixa a parcela de postura como **não avaliada** quando o
> equipamento do evento não tem estado no dia. O gerador escreve estado diário
> **só do notebook**, e por isso 79.456 eventos — 5,5% da janela — foram
> pontuados sem essa parcela, com a ausência registrada em cada nota e contada
> na saída do executor. O efeito é **conservador**: subestima a postura nos
> eventos afetados.
>
> **A C3 não é operável no limiar padrão.** Ela alerta sobre 99,8% do registro,
> porque a exposição acumulada cresce ao longo da janela. A comparação que vale
> para ela é a de revocação fixa — e nela a C3 passa a ser a melhor
> configuração a partir de 0,40 de revocação.

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

## 5. O agregado — as dez sementes juntas

Uma semente é uma amostra. O passo 5 lê as dez pastas de `results/` e grava
`agregado.json` e `agregado.md` com **média, desvio-padrão amostral e teste de
Wilcoxon pareado** de cada métrica.

**Pareado, de postos, bilateral e exato** — e cada uma dessas quatro palavras é
uma escolha:

| Escolha | Por quê |
|---|---|
| **Pareado** | A mesma semente gera a mesma população para as quatro configurações. Comparar dentro da semente tira a variação do sorteio de dentro do erro |
| **De postos** | A FPR não é normal: acumula perto de zero e tem teto em 1. Um teste *t* suporia o que o dado não tem |
| **Bilateral** | A hipótese é de diferença, não de direção. Unilateral seria escolher o lado depois de ver o resultado |
| **Exato** | Com dez pares a distribuição nula é contável, e a aproximação normal do Wilcoxon é justamente pior em amostra pequena. Sai por contagem de subconjuntos, sem biblioteca de fora |

O menor p-valor que dez pares produzem num teste bilateral exato é **0,0020** —
2 em 1024. Resultado reportado como `p = 0,0020` está no piso da escala, e não
quer dizer "p menor que isso".

**O agregado recusa o que não é comparável**, e é essa a parte que importa:
limiares diferentes, níveis de revocação diferentes, conjuntos de configuração
diferentes, ou a mesma pasta contada duas vezes. Média de coisas incomparáveis
sai plausível, e nada no número final acusaria.

> **O `run_id` não é a semente.** Cada semente tem o seu próprio conjunto
> gerado, que começa em `run_001` — as dez trazem `run_id` igual a 1. A
> identidade de uma execução é o **nome da pasta**, e a semente do gerador está
> no `procedencia.txt` de cada uma, na linha `run 1 (seed M)`.

### Rodar as dez

O gerador aceita `--seeds N`, que produz N conjuntos numa só chamada. Em escala
cheia, porém, **cada semente ocupa cerca de 3,7 GB** entre CSV e banco de
arquivos, e dez de uma vez somariam 37 GB. O procedimento usado em 12/11/2026
roda uma semente por vez, avalia, e **apaga os brutos** antes da seguinte,
guardando só `results/semente-N/` — quatro semanas depois a execução se repete
do zero, porque regerar é determinístico.

```bash
treino=2026-01-01:2026-03-31
avaliacao=2026-04-01:2026-12-31

for n in $(seq 1 10); do
    python -m generator --seeds 1 --seed0 $((41 + n)) --out tmp/gerado > tmp/procedencia.txt
    python -m ingest --origem tmp/gerado/run_001 --destino tmp/dados
    python -m runner --dados tmp/dados --run-id 1 --treino $treino --avaliacao $avaliacao
    python -m evaluator --dados tmp/dados --gerado tmp/gerado/run_001 --run-id 1 --limiar 20 --saida results/semente-$n
    cp tmp/procedencia.txt results/semente-$n/procedencia.txt
    rm -rf tmp/gerado tmp/dados
done

python -m evaluator.agregado_cli results/semente-* --saida results/
```

Quatro em paralelo, as dez levaram **cerca de duas horas** numa máquina comum —
o gasto está no executor, que passeia por 1,45 milhão de eventos quatro vezes
por semente.

---

## O que os números de hoje ainda não são

**Dez sementes medem variação de amostragem, não validade externa.** A **D-13**
está atendida desde 12/11/2026: o que o Wilcoxon afasta é a hipótese de a
diferença ter vindo do sorteio. O que ele **não** afasta é a de o gerador ser
previsível — todas as dez saem do mesmo gerador, com o mesmo catálogo de
cenários. Essa ameaça está declarada na Seção 3.8 do artigo e não se resolve com
mais sementes.

**Com o limiar padrão.** O corte de alerta usado é o teto da faixa normal do
preset, e ele **não foi calibrado**: no limiar 20 as três primeiras
configurações alarmam em cerca de um quinto do registro, e a quarta em 99,8%. A comparação que tem sentido hoje é a de **FPR a revocação
fixa**, não a do limiar de operação.

**Com a C3 sem a parcela de postura em 5,5% dos eventos.** Ver o passo 3.
