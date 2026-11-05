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
| **S6** | Schema, migrações e **o gerador**, com as checagens passando | **Falta a ingestão.** O gerador escreve CSV e nada no repositório lê CSV: o adaptador de arquivo espera `catalogo.json` e `eventos.jsonl`, e não existe carga por `COPY`. O aceite pede "carga por COPY" |
| **S7** | C0 e motor D1, selecionáveis por configuração | O aceite pede que "cenários pontuais produzam o score esperado" — e os cenários nomeados dependem da **D-06** |
| **S8** | D2 e D3, com as duas parcelas separadas | O aceite pede "cenário longitudinal com exposição crescente sem alerta pontual", que depende da **D-16** |
| **S9** | As três telas do painel, com decomposição por dimensão | O aceite pede "por que um usuário está em **risco alto**", e continua sem ninguém em `high` — agora porque o dado gerado **não chega aos motores**, não porque não exista |

**O que o gerador já produz**, em escala cheia e 79 segundos: 1.905.130 eventos,
73.619 sessões, 124 episódios, e as 16 checagens da seção 9 passando — volume
anual na faixa da **D-23**, média por dia útil na faixa de cada persona pela
**D-38**, cenários depois do baseline de três meses pela **D-24**, e `corp` sem
rótulo nenhum pela **D-17**, com o gabarito separado em `ground_truth/`.

O experimento, porém, **continua rodando sobre os *fixtures* de teste** — 2
funcionários e um só tipo de evento —, porque falta o elo entre o CSV e os
motores.

> **A M3 venceu em 22/10** e o critério dela é "C0 a C3 rodando sobre **o mesmo
> gerador**". O gerador existe; as quatro configurações ainda rodam sobre
> *fixture*. **O que falta agora é a ingestão, e ela é do Davi** — ver a seção
> "O que não dá para dividir".

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

**A ingestão — e desde 04/11 ela é o elo que falta.** O gerador escreve CSV em
`corp/` e `ground_truth/`; o adaptador de arquivo espera `catalogo.json` e
`eventos.jsonl`, e a carga por `COPY` para o PostgreSQL não existe — `database/`
tem só o schema. Enquanto esse elo não existir, o experimento continua rodando
sobre *fixture* de 2 funcionários, e **nem a S6 nem a M3 fecham**. O
[quadro](quadro.md) registra a S6 como "Filipe (gerador), Davi (schema e
ingestão)": a metade do Filipe entrou.

**A D-15 — o critério de relevância declarado a priori.** A origem do número já
foi decidida em 14/10: argumento operacional, de quantos alertas falsos um
analista absorve por turno. **Falta o valor.** Ele perde o sentido no dia em que
a primeira execução for registrada: declarar o critério depois de existir
resultado não é rigor, é justificativa. É a **lacuna 3** da Metodologia, e vence
antes da S11.

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

~~Gerador~~ → **ingestão** → **cenários nomeados** → execução das quatro
configurações → tabela de ablação → Resultados → Conclusão.

O primeiro elo caiu em 04/11. Os dois seguintes são independentes entre si e
podem andar em paralelo — a **ingestão** é do Davi, os **cenários nomeados** são
da Yasmin pelas **D-06** e **D-16**, atrasadas desde 01/10. Depois deles, o resto
é sequência.

A **S10 é o único corte disponível** no cronograma: o Isolation Forest é opcional
por definição.
