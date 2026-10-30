# TCC_SDCAC

**Sistema de Avaliação Multidimensional de Risco Comportamental**

Trabalho de Conclusão de Curso · Prof. Euzébio D. de Souza · 2026/2
Davi · Yasmin · Filipe

> O título mudou em 23/09/2026 pela decisão [D-01](decisoes.md). O anterior
> consta na [Tarefa 01](entregas/tarefa-01.md) como registro do que foi
> entregue em 03/09.

---

## O problema

Ambientes corporativos geram um volume de logs que ninguém consegue ler à mão.
Comportamentos anômalos — um login às 3h da manhã, quinze senhas erradas em dois
minutos, um acesso vindo de um IP que aquele usuário nunca usou — ficam
enterrados no meio do ruído.

Regras fixas sobre eventos isolados enxergam parte disso e cobram caro pelo
resto. Elas alarmam o plantonista que sempre entra às 3h, porque não sabem que
ele sempre entra às 3h. E não enxergam o risco que cresce ao longo de dias sem
que nenhum evento isolado passe do limiar.

## A proposta

Um **estudo comparativo**. O protótipo avalia o risco em três dimensões — o
evento em si, o desvio em relação ao comportamento habitual daquele usuário, e a
exposição acumulada ao longo de dias — e mede o resultado contra uma linha de
base de regras fixas.

```text
C0 ──────► C1 ──────► C2 ──────► C3
regras     + risco    + desvio    + exposição
fixas      do evento  do usuário  acumulada
(controle) (D1)       (D1+D2)     (D1+D2+D3)
```

São quatro configurações do **mesmo código**, ligadas por uma opção de execução.
Assim a única variável entre as linhas da tabela de resultados é a dimensão
acrescentada.

**A pergunta que o trabalho responde:** a avaliação combinada das três dimensões
reduz a taxa de falsos positivos, a uma mesma revocação, e aumenta a revocação em
cenários longitudinais, quando comparada à análise baseada exclusivamente em
regras fixas aplicadas a eventos individuais?

Ela admite "não" — e "não" também é resultado. A formulação completa e a
operacionalização das duas métricas estão no [plano](plano.md).

## O que está esperando decisão

O trabalho do Davi está travado por pendência de escopo, e não o contrário. A
lista abaixo **é gerada** a partir do [`quadro.toml`](../quadro.toml) — ela não é
escrita à mão, e por isso não envelhece. Até 15/10/2026 era escrita à mão, e
anunciava como abertas três decisões já fechadas.

<!-- QUADRO:inicio pendencias-por-pessoa -->
<!-- Bloco gerado por scripts/quadro.py a partir de quadro.toml. Editar aqui nao adianta: a proxima execucao reescreve. -->

**Davi** — 4 pendências

| ID | Decisão | Estado | Situação |
|---|---|---|---|
| D-05 | Ablação em quatro configurações (C0 a C3) | A confirmar | ⚠️ Atrasado há 29 dias |
| D-07 | Caneta rotativa por seção | Aberta | 🗓️ Sem prazo |
| D-15 | Critério de relevância declarado a priori | Aberta | ⚠️ Atrasado há 29 dias |
| D-43 | Pesos de integração das dimensões na nota final | A confirmar | ⚠️ Atrasado há 8 dias |

**Yasmin** — 7 pendências

| ID | Decisão | Estado | Situação |
|---|---|---|---|
| D-06 | Cenários de contexto (B) e longitudinais (L) | Aberta | ⚠️ Atrasado há 29 dias |
| D-07 | Caneta rotativa por seção | Aberta | 🗓️ Sem prazo |
| D-09 | Pesos preliminares e análise de sensibilidade | Aberta | ⚠️ Atrasado há 8 dias |
| D-15 | Critério de relevância declarado a priori | Aberta | ⚠️ Atrasado há 29 dias |
| D-16 | Controle negativo longitudinal | Aberta | ⚠️ Atrasado há 29 dias |
| D-19 | Vertente LGPD e ISO/IEC 27001 | Aberta | ⚠️ Atrasado há 29 dias |
| D-43 | Pesos de integração das dimensões na nota final | A confirmar | ⚠️ Atrasado há 8 dias |

**Filipe** — 3 pendências

| ID | Decisão | Estado | Situação |
|---|---|---|---|
| D-07 | Caneta rotativa por seção | Aberta | 🗓️ Sem prazo |
| D-10 | Isolation Forest como benchmark opcional | A confirmar | ⏳ Vence em 6 dias |
| D-15 | Critério de relevância declarado a priori | Aberta | ⚠️ Atrasado há 29 dias |

<!-- QUADRO:fim pendencias-por-pessoa -->

Os parâmetros do gerador ainda sem valor — de **P15** a **P23** — não entram
aqui: eles vivem no [banco da corporação simulada](banco-simulado.md), seção 10.

A tabela acima são as **decisões**. O que falta de trabalho — o gerador, os
cenários, a avaliação heurística, as seções do artigo — está dividido em
**[o que falta](o-que-falta.md)**, com o critério de aceite de cada frente.

O mesmo estado agrupado por **urgência**, e não por pessoa, está no
[quadro](quadro.md). O histórico do que já foi decidido está no
[registro de decisões](decisoes.md).

## Onde fica cada coisa

| Você quer | Vá para |
|---|---|
| Saber o que o trabalho é | [Plano do TCC](plano.md) |
| Ver o que já foi decidido | [Registro de decisões](decisoes.md) |
| Saber quem faz o quê | [Equipe e papéis](equipe.md) |
| Trabalhar no repositório | [Processo de trabalho](processo.md) |
| Ver prazos | [Cronograma](cronograma.md) |
| Entender o sistema | [Arquitetura](arquitetura.md) |
| Ver o que o gerador precisa produzir | [Banco da corporação simulada](banco-simulado.md) |
| Ver o que o software faz com os dados | [O software de análise](software.md) |
| Ver o estado de tudo, contra a data de hoje | [Quadro](quadro.md) |
| Saber o que falta e de quem é | [O que falta](o-que-falta.md) |
| Saber como o artigo é formatado | [Formato do artigo](formato-do-artigo.md) |
| Ler o que já está escrito do artigo | [`artigo/`](../artigo/README.md) — Introdução, Referencial teórico e Metodologia |
| Ver o material que a equipe entregou | [Insumos das encomendas](insumos/README.md) |
| Ver o que o professor pediu | [Tarefa 01](entregas/tarefa-01.md) · [Tarefa 02](entregas/tarefa-02.md) |
| Ler o histórico das sessões | [Relatórios](relatorios/README.md) |
