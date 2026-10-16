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

O trabalho do Davi está travado por pendência de escopo, e não o contrário.
Duas páginas dizem o que falta, e elas não se sobrepõem:

| O que | Onde |
|---|---|
| Decisões abertas, de quem é cada uma e quanto falta para o prazo | **[Quadro](quadro.md)** — recalculado contra a data de hoje |
| Parâmetros do gerador ainda sem valor, de **P15** a **P23** | [Banco da corporação simulada](banco-simulado.md), seção 10 |

Esta página não repete essa lista de propósito. Até 15/10/2026 ela repetia, e
anunciava como abertas três decisões já fechadas: cópia manual de estado
apodrece, e foi o mesmo defeito que fez o cronograma dizer "amanhã" três dias
depois do prazo.

O histórico de tudo que já foi decidido está no
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
| Saber como o artigo é formatado | [Formato do artigo](formato-do-artigo.md) |
| Ler o que já está escrito do artigo | [`artigo/`](../artigo/README.md) — Introdução, Referencial teórico e Metodologia |
| Ver o material que a equipe entregou | [Insumos das encomendas](insumos/README.md) |
| Ver o que o professor pediu | [Tarefa 01](entregas/tarefa-01.md) · [Tarefa 02](entregas/tarefa-02.md) |
| Ler o histórico das sessões | [Relatórios](relatorios/README.md) |
