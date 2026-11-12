# O que falta, e de quem é

Divisão do trabalho que resta, de 19/10/2026 até a entrega em 10/12.

> **Esta página não é lista de pendência.** Ela diz **quem responde por cada
> frente** e **qual é o critério de aceite** — fatos que mudam devagar. O estado
> ao vivo, recalculado contra a data de hoje, está no [quadro](quadro.md) e na
> [página inicial](README.md), as duas geradas do `quadro.toml`. Lista de
> pendência escrita à mão apodrece, e esta documentação já aprendeu isso duas
> vezes.

---

## A peça que trava quatro semanas

O código das semanas 6 a 9 **está escrito e testado**: schema, as quatro
configurações, o experimento ponta a ponta, a API de leitura, o painel e — desde
**04/11/2026, pelo #89** — o gerador de eventos. Nenhuma das quatro fecha ainda,
e **o motivo mudou**.

| Semana | O que existe | Por que o aceite não fecha |
|---|---|---|
| **S6** | Schema, migrações, **o gerador** e **a ingestão** — o experimento roda sobre dado gerado desde 11/11/2026 | O aceite pede **"carga por `COPY`"**, e o caminho que existe é outro: a ingestão traduz o CSV para o formato do adaptador de arquivo. O dado chega aos motores; a carga para o PostgreSQL não existe. **O Davi decide se o critério se cumpre por este caminho** ou se o `COPY` continua exigido |
| **S7** | C0 e motor D1, selecionáveis por configuração | O aceite pede que "cenários pontuais produzam o score esperado" — e os cenários nomeados dependem da **D-06**. A família P já é detectada em 100% dos episódios pela C1, mas "o escore esperado" só existe depois do catálogo |
| **S8** | D2 e D3, com as duas parcelas separadas | O aceite pede "cenário longitudinal com exposição crescente sem alerta pontual", que depende da **D-16** — e a **C3 ainda não executa** (ver abaixo) |
| **S9** | As três telas do painel, com decomposição por dimensão | O aceite pede "por que um usuário está em **risco alto**", e agora **há dado para isso**: a execução de 11/11 produziu 280 a 315 mil alertas. Falta apontar o painel para uma execução registrada |

**O que o gerador produz**, em escala cheia e 67 segundos: 1.905.111 eventos,
73.604 sessões, 124 episódios, e as 17 checagens da seção 9 passando — volume
anual na faixa da **D-23**, média por dia útil na faixa de cada persona pela
**D-38**, cenários depois do baseline de três meses pela **D-24**, e `corp` sem
rótulo nenhum pela **D-17**, com o gabarito separado em `ground_truth/`.

> ✅ **A ingestão entrou em 11/11/2026, e com ela o avaliador.** O experimento
> deixou de rodar sobre *fixture* de 2 funcionários: **1.435.546 eventos
> pontuados** pelas configurações C0, C1 e C2, com as métricas da **D-03** em
> [`results/semente-1`](../results/README.md) e a §4 do artigo escrita sobre
> elas. Procedimento em
> [execução do experimento](execucao-do-experimento.md).

> ⚠️ **A C3 não executa, e é decisão — não defeito.** O gerador escreve estado
> diário **só do notebook** (`generator/normal.py`, `device_states`), e a D3
> exige o estado do equipamento **do evento**, recusando-se a pontuar sem ele:
> *"sem ele, atualização e antivírus sairiam como se estivessem em ordem"*.
> Eventos de celular e de origem externa não têm esse estado. Três caminhos, e
> o terceiro campo é o que a escolha custa:
>
> | Caminho | O que muda | O que custa |
> |---|---|---|
> | Gerador escreve estado de celular | trabalho do **Filipe** | o que é "idade de patch" de um celular precisa de decisão própria |
> | D3 pontua sem a parcela de postura quando falta estado | muda a **semântica da D-30** | abre a porta para a parcela sumir em silêncio, que é o que a recusa atual impede |
> | Experimento restringe-se a eventos de notebook | nada no código | tira do experimento os eventos de origem externa, que são onde estão vários cenários |
>
> **Sem a C3 a tabela de ablação tem três colunas, e falta a parcela de
> exposição acumulada — metade do que a pergunta de pesquisa propõe avaliar.**

> **A M3 venceu em 22/10** e o critério dela é "C0 a C3 rodando sobre **o mesmo
> gerador**". Três das quatro rodam. **O que falta é a C3**, e ela depende da
> decisão acima.

---

## Filipe — dados, gerador e painel

> ✅ **O gerador entrou em 04/11/2026**, pelo [#89](https://github.com/Codexrocks/TCC_SDCAC/pull/89)
> — 9 arquivos, 1.170 linhas, as checagens da seção 9 passando. Era o item que
> travava quatro semanas, e saiu do caminho crítico. Os parâmetros **P15** e
> **P17** ficaram embutidos no gerador e seguem valendo como registro em
> [banco simulado](banco-simulado.md), seção 10.

**O que ficou dele, e é dívida de qualidade do próprio gerador:**

1. **Nenhum teste.** São 1.170 linhas em 9 arquivos, sem um `test_` — o único
   módulo do repositório nessa situação, contra a seção 8 de
   [padrões de código](padroes-codigo.md)
2. **226 apontamentos do Ruff**, sendo 141 de vários comandos na mesma linha
   (`E701`/`E702`) e 42 de nomenclatura (`N803`/`N806`/`N812`). O Ruff não roda
   no CI, então não reprova — mas a seção 3 de padrões de código põe a
   formatação como não negociável
3. **Três grupos de parâmetros sem procedência** — `_CAT_W`, `MFA0_*` e
   `PATCH_MEDIAN` não citam decisão nem se declaram assunção, contra a regra que
   o próprio `config.py` enuncia no cabeçalho. Detalhe em
   [banco simulado](banco-simulado.md), seção 10 · ratificação do **Davi**
> ✅ **O baseline foi alinhado em 04/11, pelo #92:** o `EVAL_START_DAY` passou de
> 100 para **90** — os três meses exatos da **D-24** —, entrou a checagem que
> mede a decisão em vez do parâmetro, e `tests/test_gerador.py` tornou-se o
> primeiro teste do módulo. Detalhe em
> [banco simulado](banco-simulado.md), seção 10.

**Na ordem do cronograma:**

4. **Revisar o painel** da S9. Ele foi escrito por outra pessoa com IA, e o que
   a banca vê precisa bater com quem assina — ver [o painel](painel.md)
5. **Avaliação heurística** do painel, pela [usabilidade](usabilidade.md), § 6.1.
   É feita por quem constrói, **sem participantes**, pela **D-02**
6. **D-10** — confirmar se o Isolation Forest da S10 entra. É opcional por
   definição, e cortá-lo não compromete o TCC
7. **S12** — tabela de ablação, sensibilidade dos pesos e gráficos, com o Davi.
   Cada número sai de notebook versionado
8. **S13** — a caneta do [`artigo/04-resultados.md`](../artigo/04-resultados.md)
9. **Três chamadas bibliográficas** por conferir na fonte, em
   [citações pendentes](citacoes-pendentes.md)

---

## Yasmin — cenários, rótulos e o recorte de segurança

**As duas que travam a Metodologia e a S7:**

1. **D-06** — cenários de contexto (B) e longitudinais (L)
2. **D-16** — o cenário de escalada legítima, que é o controle negativo

Das duas sai a **lacuna 1** da Metodologia: a relação nominal dos cenários, com
no mínimo um por família e um de escalada legítima. Enquanto ela não existe, a
§ 3.4 do artigo fica com um bloco *A escrever* aberto, e o aceite da S7 não tem
contra o que ser medido.

**O resto:**

3. **P18 a P23** — catálogo de cenários, prevalência, modo de injeção, rótulos e
   desenho cego, em [banco simulado](banco-simulado.md), seção 10
4. **D-09** — pesos preliminares e análise de sensibilidade
5. **D-19** — a vertente LGPD e ISO/IEC 27001. Já está declarada na § 3.8 do
   artigo como ameaça à validade; falta o par dela nas **limitações da § 4.6** e
   nos **trabalhos futuros da § 5.4**, que é onde a S13 a cobra
6. **S11** — a execução de todos os cenários nas quatro configurações, que é de
   todos e tem a condução dela
7. **Uma chamada bibliográfica** por conferir na fonte

---

## O que não dá para dividir

Quatro coisas continuam no Davi por construção, não por combinação:

> ✅ **A ingestão entrou em 11/11/2026** — `ingest/` e `evaluator/`, com 21
> testes. O elo que faltava desde 04/11 saiu do caminho crítico, e o
> experimento passou a rodar sobre dado gerado.

**O que ficou dela, e é do Davi:** ratificar as **três correspondências** que a
tradução precisou declarar, e que estão nomeadas em constantes no topo de
`ingest/corp.py` justamente para serem ratificáveis:

| O quê | O gerador escreve | Os motores esperam |
|---|---|---|
| **Persona** | `day_admin`, `shift_ops`, `sales_traveler`, `hybrid_eng` | `office_daytime`, `shift`, `sales_travel`, `hybrid` |
| **Fuso** (D-31, D-40) | deslocamento fixo, `UTC-3` | chave IANA, `America/Sao_Paulo` |
| **Privilégio** | `privileged`, booleano | `standard`, `elevated`, `admin` |

O do fuso **derrubou a pontuação no primeiro evento**; os outros dois não
quebravam nada — produziriam nota errada em silêncio. Persona ou fuso novo no
gerador faz a ingestão **recusar**, em vez de adivinhar.

**A carga por `COPY` continua não existindo** — `database/` tem só o schema, e é
dela que o critério de aceite da S6 fala. Ver a tabela acima.

**A D-15 — o critério de relevância declarado a priori.** A origem do número já
foi decidida em 14/10: argumento operacional, de quantos alertas falsos um
analista absorve por turno. **Falta o valor, e o prazo já passou.** O texto
desta seção dizia que o número "perde o sentido no dia em que a primeira
execução for registrada" — **esse dia foi 11/11/2026**. O que resta é declarar o
valor pelo argumento operacional, sem olhar a tabela da §4.3, e registrar que
foi declarado depois. É a **lacuna 3** da Metodologia.

**O merge.** O ruleset `Merge restrito ao líder` recusa qualquer outra origem, e
o GitHub não deixa ninguém aprovar o próprio Pull Request. Todo trabalho da
Yasmin e do Filipe chega ao repositório pela mão dele — ver
[cronograma](cronograma.md#como-o-trabalho-chega-ao-repositório).

**Nove das treze chamadas bibliográficas** por conferir estão no nome dele, em
[citações pendentes](citacoes-pendentes.md). Referência que ninguém abriu na
fonte não entra no artigo, e a validação não pega isso — a banca pega.

Além dessas, seguem em aberto e são dele ou compartilhadas: a **D-05**, a
**D-07** (a caneta rotativa, dos três), a **D-43** (com a Yasmin), a decisão de
o CI passar a instalar o Streamlit, a tela de Métricas — que depende de um
avaliador que grave métrica — e a caneta da **S14**.

---

## O caminho crítico, em uma frase

~~Gerador~~ → ~~ingestão~~ → **a C3** · **cenários nomeados** → execução das
quatro configurações → tabela de ablação → ~~Resultados~~ → Conclusão.

O gerador caiu em 04/11, a ingestão em 11/11 — e a **Seção 4 do artigo já está
escrita sobre números de execução registrada**, com três das quatro
configurações. Os dois elos restantes são independentes entre si: a **C3** é
decisão do Davi, os **cenários nomeados** são da Yasmin pelas **D-06** e
**D-16**, atrasadas desde 01/10.

Duas decisões passaram a vencer antes da banca, e não depois:

- **A D-12** — evento, usuário-dia ou episódio. Os resultados de hoje reportam
  as duas unidades porque ela está aberta, e escolher depois de ver qual
  favorece a conclusão não é rigor
- **A D-15** — o critério de relevância. A execução de 11/11 **já existe**, e
  cada dia que passa torna a declaração a priori menos a priori

A **S10 é o único corte disponível** no cronograma: o Isolation Forest é opcional
por definição.
