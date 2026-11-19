# O que falta, e de quem é

Divisão do trabalho que resta até a entrega em **10/12/2026**. Retrato de
**18/11/2026**.

> **O estado ao vivo está no [quadro](quadro.md)** e na
> [página inicial](README.md), as duas geradas do `quadro.toml` e recalculadas
> contra a data de hoje. Esta página diz **quem responde por cada frente** e
> **o que precisa acontecer para ela fechar** — e por isso envelhece. Quando
> discordar do quadro, vale o quadro.
>
> A versão anterior desta página, que acompanhou a construção de 19/10 a
> 12/11, está no histórico do Git. Ela foi reescrita em 18/11 porque descrevia
> como pendente o que já tinha fechado: a ingestão, a C3, a D-09, a D-15 e o
> teste do gerador no CI.

---

## Onde o trabalho está

**A construção acabou.** O caminho crítico — gerador, ingestão, C3, dez
sementes, cenários nomeados, tabela de ablação, Resultados, Conclusão — fechou
em 12/11/2026, e as semanas **S5 a S11** foram dadas como prontas pelo Davi em
18/11/2026.

| | |
|---|---|
| Experimento | Dez sementes, as quatro configurações em cada uma, Wilcoxon pareado — [`results/agregado.md`](../results/README.md) |
| Artigo montado | **12 páginas**, o teto do template, por `scripts/montar_artigo.py` |
| Referências | 21 na lista: 20 conferidas e confirmadas, e Alahmadi et al. (2022) à espera da confirmação do Davi |
| Template | O do professor chegou em 18/11 e é, no conteúdo, o COBEM 2025 que o artigo já seguia |
| Decisões | Todas fechadas, menos a **D-07** (caneta rotativa), que não tem prazo |

**O que resta não é construção: é leitura de quem assina, envio e diagramação.**

### O que fechou em 18/11/2026, por decisão do Davi

| O quê | Como ficou |
|---|---|
| **D-05** | Confirmada: quatro configurações, como a D-26 já dizia |
| **D-10** | **O Isolation Forest não entra.** A S10 fecha sem ele |
| **D-43** | Fechada com os pesos com que as dez sementes rodaram, com a concordância da Yasmin |
| **Critério da S6** | A carga por `COPY` foi substituída pela ingestão do CSV em `ingest/` |
| **Análise de sensibilidade dos pesos** | **Não foi executada.** Entrou como limitação na § 4.6 e como trabalho futuro na § 5.4, e a § 3.3 deixou de prometê-la |

---

## Todos

1. **Reenviar a Seção de Resultados ao orientador — prazo 19/11/2026.** As
   correções que ele pediu, legenda e fonte em toda tabela e figura, estão na
   `main` desde o #109 e o #127. O envio é de uma pessoa
2. **Ler o que cada um assina.** Nenhum capítulo está marcado como pronto no
   quadro, e o motivo é o mesmo em todos: o texto existe e falta a leitura de
   quem responde por ele. A divisão está nas seções abaixo
3. **S15 — a versão final, até 10/12.** Montar com
   `python scripts/montar_artigo.py`, converter e conferir as 12 páginas.
   Falta conferir no template como ele numera equação — por referência
   cruzada, e não em `$$…$$`
4. **S16 — slides e ensaio da defesa**, depois da entrega. O critério é que
   cada um apresente qualquer seção sob sorteio

---

## Davi

1. **Ler a § 5.4**, reescrita em 18/11 para incluir a análise de
   sensibilidade e o par de trabalho futuro das limitações de medição — é o
   que o critério da S13 pede: *"cada limitação nomeada tem proposta de
   trabalho futuro"*
2. **Ratificar as três correspondências da ingestão**, nomeadas no topo de
   `ingest/corp.py`:

   | O quê | O gerador escreve | Os motores esperam |
   |---|---|---|
   | **Persona** | `day_admin`, `shift_ops`, `sales_traveler`, `hybrid_eng` | `office_daytime`, `shift`, `sales_travel`, `hybrid` |
   | **Fuso** (D-31, D-40) | deslocamento fixo, `UTC-3` | chave IANA, `America/Sao_Paulo` |
   | **Privilégio** | `privileged`, booleano | `standard`, `elevated`, `admin` |

3. **Ratificar as assunções do gerador** — `_CAT_W`, `MFA0_*` e
   `PATCH_MEDIAN`, e os parâmetros **P15** e **P17** —, em
   [banco simulado](banco-simulado.md), seção 10
4. **Responder a pergunta do `generator/checks.py`**: as faixas da D-23 e da
   D-38 valem por **dia de semana** ou por **dia com atividade**? Hoje o filtro
   é `tot >= 10` eventos no dia. Uma linha de resposta
5. **Os achados 2 e 10 da avaliação heurística**, de severidade 3. Os dois
   exigem mudar o contrato de leitura da API — ver [o painel](painel.md)
6. **A tela de Métricas**, pela D-45, depois de o avaliador gravar as métricas
   na API. Não bloqueia o artigo
7. **O merge** de todo Pull Request. O ruleset recusa qualquer outra origem

## Filipe

1. **Ler as §§ 4.3.3 e 4.4**, reescritas em 17/11, e a limitação dos pesos que
   entrou na § 4.6 em 18/11. É a caneta da S13
2. **A revisão do painel**, que [o painel](painel.md) ainda lista em seu nome
3. **Três citações em [`usabilidade.md`](usabilidade.md)** — §§ 6.2, 6.3 e 9.
   Estão na documentação, não no artigo, em
   [citações pendentes](citacoes-pendentes.md)

## Yasmin

1. **Reler a reorganização do Referencial**, de 13/10, e concordar com o que
   ficou atribuído a cada obra
2. **Introdução, com o Filipe:**
   - A extensão **cabe**: no documento montado em 18/11 ela vai da metade da
     página 1 ao alto da página 3, cerca de 1,6 página para um teto de 2
   - ~~**As referências do contexto não cumprem a regra dos 5 anos.**~~ As
     orientações pedem publicação de até 5 anos no contexto
     ([formato do artigo](formato-do-artigo.md)), e as duas chamadas da § 1.1
     eram de 2006 e 2009. **Entrou Alahmadi et al. (2022) em 19/11**, aberta e
     conferida pelo assistente no PDF dos anais; **falta o Davi confirmar**, em
     [citações pendentes](citacoes-pendentes.md)
   - Alinhar a granularidade dos objetivos ao plano
3. **Uma citação em [`usabilidade.md`](usabilidade.md) § 7**, sobre fadiga de
   alerta em SOC

> **Os quatro casos reais** (Target, GE, Capital One, Tesla) **não estão mais
> no artigo**, e as linhas deles em [citações pendentes](citacoes-pendentes.md)
> ficam vencidas de propósito: só voltam a valer se um caso voltar à
> Introdução.

---

## Depois da entrega

Dívida técnica que não muda o artigo, registrada no relatório da sessão 52:

- O `confere_legendas` não confere se a legenda descreve a tabela
- A trava do #113 não cobre `scripts/`
- O PR do quadro nunca recebe check, e só entra por liberação de administrador
- `scripts/` tem 31 apontamentos de Ruff, e o CI não roda o Ruff
- A docstring de `scripts/montar_artigo.py` ainda diz que o template de 2026
  não está no repositório. É arquivo protegido, e a correção espera 24 h
