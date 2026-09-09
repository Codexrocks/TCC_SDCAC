# TCC_SDCAC

**Sistema de Detecção de Comportamentos Anômalos em Cybersecurity**

Trabalho de Conclusão de Curso · Prof. Euzébio D. de Souza · 2026/2
Davi · Yasmin · Filipe

> **O título está em revisão.** O [plano](plano.md) adota "Sistema de Avaliação
> Multidimensional de Risco Comportamental". A troca depende da decisão
> [D-01](decisoes.md), que precisa ser comunicada ao orientador — até lá, vale o
> título acima, que é o da Tarefa 01 entregue em 03/09.

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

## Onde fica cada coisa

| Você quer | Vá para |
|---|---|
| Saber o que o trabalho é | [Plano do TCC](plano.md) |
| Ver o que já foi decidido | [Registro de decisões](decisoes.md) |
| Saber quem faz o quê | [Equipe e papéis](equipe.md) |
| Trabalhar no repositório | [Processo de trabalho](processo.md) |
| Ver prazos | [Cronograma](cronograma.md) |
| Entender o sistema | [Arquitetura](arquitetura.md) |
| Saber como o artigo é formatado | [Formato COBEM](cobem.md) |
| Ver o que o professor pediu | [Entregas](entregas/tarefa-01.md) |
| Ler o histórico das sessões | [Relatórios](relatorios/README.md) |
