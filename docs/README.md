# TCC_SDCAC

**Sistema de Avaliação Multidimensional de Risco Comportamental**

Trabalho de Conclusão de Curso · Prof. Euzébio D. de Souza · 2026/2
Davi · Yasmin · Filipe

> **O título mudou em 23/09/2026**, comunicado ao orientador e registrado na
> decisão [D-01](decisoes.md). O anterior — "Sistema de Detecção de
> Comportamentos Anômalos em Cybersecurity" — consta na
> [Tarefa 01](entregas/tarefa-01.md), entregue em 03/09, e fica lá como registro
> do que foi entregue naquela data.

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

## ⚠️ O que está esperando decisão da equipe

O trabalho do Davi está travado por estas pendências, e não o contrário: as
decisões de escopo já fechadas estão em [decisões](decisoes.md), de **D-01 a
D-41**. O que falta abaixo é de quem produz cada frente.

**Yasmin — cybersecurity, cenários e rótulos**

| O que falta | Onde está | Prazo |
|---|---|---|
| **D-06** · cenários de contexto e longitudinais | [decisões](decisoes.md) | **01/10** |
| **D-16** · cenário de escalada legítima, o controle negativo | [decisões](decisoes.md) | **01/10** |
| **D-19** · vertente LGPD e ISO/IEC 27001, como limitação | [decisões](decisoes.md) | **01/10** |
| **P18 a P23** · catálogo de cenários, prevalência, modo de injeção, rótulos e desenho cego | [banco simulado](banco-simulado.md), seção 10 | antes da **S6** |
| **D-09** · pesos preliminares e análise de sensibilidade | [decisões](decisoes.md) | S8 |
| Confirmar quantas das 13 referências do referencial foram abertas na fonte | [insumos](insumos/README.md) | S5 |

**Filipe — dados, gerador e painel**

| O que falta | Onde está | Prazo |
|---|---|---|
| **D-14** · o que fazer se a C0 não alcançar revocação 0,90 | [decisões](decisoes.md) | **01/10** |
| **D-12** · unidade de análise das métricas, com o Davi | [decisões](decisoes.md) | **01/10** |
| **D-02** · o painel é instrumento, objetivo ou está fora do escopo — **aberta desde 08/09** | [decisões](decisoes.md) | vencida |
| **Gerador de eventos** — personas, calendário, rotina e ruído legítimo | [banco simulado](banco-simulado.md) | **S6, 02/10** |
| **P15 e P17** · proporção de cada tipo por persona e a taxa normal de senha errada | [banco simulado](banco-simulado.md), seção 10 | antes da **S6** |
| Painel de inspeção em Streamlit | [o software](software.md), seção 11 | S9 |

**Dos dois, juntos:** os seis blocos `[COMPLEMENTAÇÃO]` da
[Introdução](../artigo/01-introducao.md) — evidência de casos reais e números
setoriais — na **S5**.

**Dos três, com o Davi:** a **D-15**, que fixa qual redução de falso positivo
conta como resposta afirmativa, e a **D-07**, a caneta rotativa por seção. A
D-15 vence em **01/10**, e declarar o critério depois de existir número não é
rigor, é justificativa.

> **A D-02 é a mais atrasada e a que mexe no artigo.** A seção 3.9 da
> [Metodologia](../artigo/03-metodologia.md) foi escrita supondo painel como
> *instrumento de análise*. Se a escolha for tratá-lo como objeto de avaliação,
> aquela subseção é reescrita e passa a contradizer a declaração de que nenhum
> dado de pessoa real é coletado.

O estado completo, recalculado contra a data de hoje, está no
[quadro](quadro.md).

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
| Saber como o artigo é formatado | [Formato do artigo](formato-do-artigo.md) |
| Ler o que já está escrito do artigo | [`artigo/`](../artigo/README.md) — Introdução, Referencial teórico e Metodologia |
| Ver o material que a equipe entregou | [Insumos das encomendas](insumos/README.md) |
| Ver o que o professor pediu | [Tarefa 01](entregas/tarefa-01.md) · [Tarefa 02](entregas/tarefa-02.md) |
| Ler o histórico das sessões | [Relatórios](relatorios/README.md) |
