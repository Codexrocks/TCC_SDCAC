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

O código das semanas 6 a 9 **está escrito e testado**: schema, ingestão, as
quatro configurações, o experimento ponta a ponta, a API de leitura e o painel.
Nenhuma das quatro pode ser dada por aceita, e é pelo mesmo motivo.

| Semana | O que existe | Por que o aceite não fecha |
|---|---|---|
| **S6** | Schema, migrações e ingestão | **Falta o gerador de eventos.** O aceite pede "uma semente completa gerada" |
| **S7** | C0 e motor D1, selecionáveis por configuração | O aceite pede que "cenários pontuais produzam o score esperado" — e os cenários dependem da **D-06** |
| **S8** | D2 e D3, com as duas parcelas separadas | O aceite pede "cenário longitudinal com exposição crescente sem alerta pontual" |
| **S9** | As três telas do painel, com decomposição por dimensão | O aceite pede que o leitor entenda "por que um usuário está em **risco alto**" — e **não existe ninguém em `high`** em nenhum dado obtenível |

O experimento hoje roda sobre os *fixtures* de teste: **2 funcionários e um só
tipo de evento**. Isso prova que a tubulação funciona e não povoa painel nenhum.

> **A M3 vence em 22/10**, e o critério dela é "C0 a C3 rodando sobre **o mesmo
> gerador**". As quatro rodam — sobre *fixture*. O gerador está escrito dentro
> do critério que ele mesmo trava.

---

## Filipe — dados, gerador e painel

**Primeiro, e antes de tudo:**

1. **O gerador de eventos** — personas, calendário, rotina e ruído legítimo,
   especificado em [banco simulado](banco-simulado.md). É o item acima: destrava
   S6, S7, S8, S9 e a M3 de uma vez
2. **As sete checagens do catálogo**, que o aceite da S6 exige
3. **Os parâmetros P15 e P17** — proporção de cada tipo por persona e a taxa
   normal de senha errada — em [banco simulado](banco-simulado.md), seção 10

**Depois, na ordem do cronograma:**

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

Três coisas continuam no Davi por construção, não por combinação:

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

**Gerador → semente completa → cenários nomeados → execução das quatro
configurações → tabela de ablação → Resultados → Conclusão.**

Cada elo depende do anterior, e o primeiro está atrasado desde 08/10. A
**S10 é o único corte disponível** no cronograma: o Isolation Forest é opcional
por definição.
