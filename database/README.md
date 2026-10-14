# Schema dos três bancos

O schema que a [especificação do banco](../docs/banco-simulado.md) descreve, em
SQL aplicável. Esta pasta é a **S6** do cronograma, e o que ela entrega é a base
sobre a qual o motor da S7 e o gerador rodam.

A especificação é a fonte: se o SQL e a página divergirem, **a página está certa
e o SQL está errado** — e `tests/test_schema.py` reprova a divergência antes de
alguém descobrir pelo caminho difícil.

## Ordem de aplicação

```bash
# 1. Bancos e papéis — uma vez, como superusuário
psql -v ON_ERROR_STOP=1 -f database/00_bancos_e_papeis.sql

# 2. Schema e privilégios de cada banco
psql -d corp         -v ON_ERROR_STOP=1 -f database/corp/001_schema.sql
psql -d corp         -v ON_ERROR_STOP=1 -f database/corp/002_privilegios.sql
psql -d ground_truth -v ON_ERROR_STOP=1 -f database/ground_truth/001_schema.sql
psql -d ground_truth -v ON_ERROR_STOP=1 -f database/ground_truth/002_privilegios.sql
psql -d sdcac        -v ON_ERROR_STOP=1 -f database/sdcac/001_schema.sql
psql -d sdcac        -v ON_ERROR_STOP=1 -f database/sdcac/002_privilegios.sql
```

**Os arquivos são imutáveis depois de aplicados.** Mudança de schema entra como
arquivo novo numerado — `003_`, `004_` — no mesmo Pull Request do código que
depende dela. Editar um arquivo já aplicado deixa o banco de quem já rodou
diferente do banco de quem rodar depois, e nada avisa.

## A senha não está aqui, e não vai estar

Os papéis nascem sem senha. Cada um recebe a sua fora do repositório, a partir
do `.env` da máquina:

```bash
psql -c "ALTER ROLE generator PASSWORD '<do seu .env>'"
```

O repositório é público. `scripts/validar.py` reprova senha literal no diff, e
isso vale também para SQL de ambiente local.

## Quem pode o quê

| Papel | `corp` | `ground_truth` | `sdcac` |
|---|---|---|---|
| `generator` | lê e insere, e cria partição | lê e insere | — sem `CONNECT` |
| `sdcac_app` | **só lê** | **sem `CONNECT`** | lê e insere padrão, nota e alerta |
| `evaluator` | só lê | só lê | lê tudo, insere métrica |

Três linhas dessa tabela são travas, não convenções:

- **`sdcac_app` não conecta no `ground_truth`.** É a barreira contra vazamento
  de rótulo, e é o equivalente estrutural da **D-17**. Em banco separado, nem
  por engano uma consulta cruza evento com gabarito: o PostgreSQL não atravessa
  banco sem extensão, e nenhuma está instalada.
- **Ninguém recebe `UPDATE` nem `DELETE` em `events`.** Log é evidência. Para
  descartar uma semente avaliada, derruba-se a partição.
- **O `evaluator` não escreve nota.** Quem vê o gabarito não mexe no score.

## O preço da separação em três bancos

Não existe chave estrangeira de `ground_truth.labels` nem de
`sdcac.risk_scores` para `corp.events`: são bancos diferentes. A integridade
entre eles é **convenção conferida em teste**, não garantia do banco. Duas
checagens que o avaliador faz antes de publicar métrica:

- todo rótulo aponta para um evento que existe;
- todo episódio tem pelo menos um rótulo.

Foi uma escolha, e o motivo está acima: a trava de `CONNECT` vale mais que a
chave estrangeira. Está registrado na seção 8 da especificação.

## Partição por semente

A tabela `events` é particionada por `run_id` e **não tem partição `DEFAULT`**,
de propósito: carga de semente sem partição criada deve falhar alto, não cair
num depósito onde ninguém procura.

```sql
-- antes de carregar a semente 7
CREATE TABLE events_run_7 PARTITION OF events FOR VALUES IN (7);

-- depois de avaliar e guardar as métricas
DROP TABLE events_run_7;
```

É o que torna a **D-13** viável: 10 a 20 sementes geradas, avaliadas e
descartadas, com só a de referência guardada por inteiro.

## O que ainda não está aqui

| O que falta | Por quê |
|---|---|
| Valores de `network_ranges` e do calendário | **P12 e P13**, abertas. A estrutura existe; a lista, não |
| Carga por `COPY` | Entra com o gerador, que é a frente do Filipe na S6 |
| Tabelas da v2 — usuários, configurações, fila de job, auditoria | **D-32**: a v2 começa na S9, e tabela sem código que use é pasta vazia com outro nome |
| Teste contra um PostgreSQL de verdade | Precisa de serviço no CI, que mexe em `.github/**` — espera 24 h e justificativa |
