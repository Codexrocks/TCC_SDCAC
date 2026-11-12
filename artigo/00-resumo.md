# Cabeçalho, Resumo e Abstract

> **Esta página é o bloco de abertura do documento montado**, e a ordem abaixo é
> a do [template COBEM](../docs/formato-do-artigo.md): título, autores,
> instituição, e-mails, resumo, palavras-chave. O bloco em inglês vem na
> sequência, pelo mesmo desenho.
>
> O orçamento de páginas reserva **0,5 página** para ele — ver
> [README](README.md).
>
> **De onde veio.** O Resumo e o Abstract estavam no fim da
> [Conclusão](05-conclusao.md), porque é lá que a 5ª Versão os cobra e era lá
> que foram escritos. Mudaram para cá em 11/11/2026, quando os resultados
> passaram a existir e as duas frases finais de cada um puderam ser escritas —
> no documento montado eles vão para o alto, e manter o texto em dois lugares
> apodreceria.

***

## Título

**Avaliação multidimensional de risco comportamental em logs de eventos:
comparação com regras fixas em ambiente corporativo simulado**

> Times New Roman, centralizado, negrito, corpo 14 — a instrução do template.

## Autores

**Davi Soares Dilly** · **Filipe Fernandes de Aguiar** · **Yasmin Teles Vales**

*Centro Universitário UNA*

> **Confirmar antes de publicar:** o template pede o endereço da instituição e os
> **e-mails** dos autores logo abaixo do nome, e é a forma usual em artigo de
> congresso. Este repositório é **público**, e a pasta `docs/` é publicada no
> GitBook — a decisão de expor os três endereços é da equipe, e precisa ser dita
> em voz alta uma vez em vez de passar por omissão. Os endereços entram na
> montagem do documento de entrega; aqui ficam de fora até a confirmação.

***

## Resumo

> **Completo desde 11/11/2026, e reescrito em 12/11/2026.** As três primeiras
> partes — contexto, objetivo e método — estavam escritas desde setembro. As
> **duas frases finais**, com o resultado principal e a conclusão, só foram
> escritas quando a execução registrada passou a existir: resumo redigido antes
> é resumo do que se pretendia fazer. Em 12/11 elas foram **reescritas sobre as
> dez sementes**, pela **D-13** — e a reescrita não foi cosmética: o teste
> pareado derrubou a afirmação de que a terceira dimensão superava as demais em
> revocação alta.
>
> Um parágrafo só, sem fórmula e sem chamada bibliográfica, em cerca de 300
> palavras — a instrução do template.

A crescente digitalização das organizações amplia o volume e a diversidade dos
registros de eventos produzidos por sistemas corporativos, e a análise desses
registros apoiada exclusivamente em regras fixas aplicadas a eventos isolados
não distingue atividade legítima incomum de comportamento efetivamente
indevido, nem identifica situações que se desenvolvem gradualmente. Este
trabalho desenvolve e avalia um modelo experimental de avaliação multidimensional
de risco comportamental, que combina o risco do evento individual, o desvio em
relação ao padrão de comportamento do próprio usuário e a exposição acumulada ao
risco, esta última reportada em duas parcelas distintas — conduta e postura de
segurança. O método consiste em um experimento comparativo conduzido em ambiente
corporativo simulado, no qual quatro configurações de avaliação — uma linha de
base de regras fixas e três configurações com acréscimo progressivo de dimensões
— são aplicadas aos mesmos conjuntos de eventos e cenários, permitindo medir
isoladamente a contribuição de cada dimensão. As grandezas de comparação são a taxa de falsos positivos a uma
mesma revocação e a revocação em cenários longitudinais. Em dez execuções
independentes, com 1.436.275 ± 9.681 eventos avaliados em cada uma, a
configuração que soma o risco do evento ao desvio em relação ao padrão
individual reduziu a taxa de falsos positivos de 18,44% para 0,40% à revocação
de 0,20 e elevou a revocação em cenários longitudinais de 35,0% para 100,0%,
medida por episódio, com significância em teste pareado em todos os níveis
examinados, enquanto a linha de base de regras fixas não alcançou revocação de
0,40 sem emitir alerta sobre todo o registro. O ganho não se mostrou gratuito: a mesma
configuração elevou de 75,8% para 96,0% a proporção de episódios legítimos que
produziram alerta, e o acréscimo da exposição acumulada não reduziu
significativamente a taxa de falsos positivos em nenhum regime, de modo que os
resultados autorizam afirmar redução de ruído e aumento de cobertura nos
cenários medidos, em regime de revocação declarado, e não ausência de custo.

**Palavras-chave:** risco comportamental, análise de logs, detecção de anomalias,
regras fixas, ambiente corporativo simulado

> **Separadas por vírgula**, e não por ponto. A regra de convivência do
> [README](README.md) é explícita: a lista de referências segue a ABNT NBR 6023,
> e **todo o resto segue o template COBEM** — que pede "up to 5 keywords
> separated by commas". A forma anterior, com ponto, vinha da NBR 6028 e valia
> enquanto a instrução do template não estava escrita.

***

## Abstract

> **O abstract em inglês é obrigatório**, além do Resumo em português —
> confirmado com o orientador em 04/09/2026, e exigido também pela estrutura do
> [formato do artigo](../docs/formato-do-artigo.md).
>
> **É a única parte do artigo em inglês.** O resto é todo em português, decidido
> em 07/09/2026.
>
> **Onde ele fica:** logo depois do bloco em português, antes da Introdução. O
> template do COBEM 2025 põe o bloco de abstract no alto, imediatamente após os
> autores, e esta página segue esse desenho. A observação anterior — de que na
> família ABCM ele costuma ir depois das referências — não se confirmou no
> template que está no repositório. **Confirmar quando o COBEM 2026 chegar.**
>
> ⚠️ **Este texto foi redigido com auxílio de IA e precisa ser lido por uma
> pessoa antes de ser assinado** — está declarado no Pull Request que o
> introduziu. Abstract gerado por máquina que ninguém conferiu é o mesmo
> problema da referência inventada.

The growing digitalization of organizations increases both the volume and the
diversity of event records produced by corporate systems. Analysing such records
solely through fixed rules applied to isolated events fails to distinguish
unusual but legitimate activity from genuinely improper behaviour, and does not
identify situations that develop gradually over time. This work develops and
evaluates an experimental model for multidimensional assessment of behavioural
risk, combining the risk of the individual event, the deviation from each user's
own behavioural baseline, and the accumulated exposure to risk, the latter
reported as two separate components — conduct and security posture. The method
is a comparative experiment conducted in a simulated corporate environment, in
which four assessment configurations — a fixed-rule baseline and three
configurations adding dimensions progressively — are applied to the same sets of
events and scenarios, so that the contribution of each dimension can be
measured in isolation. The comparison
quantities are the false positive rate at a fixed recall and the recall on
longitudinal scenarios. Across ten independent executions, with 1,436,275 ±
9,681 events assessed in each, the configuration that adds the deviation from
the individual baseline to the event risk reduced the false positive rate from
18.44% to 0.40% at a recall of 0.20 and raised the recall on longitudinal
scenarios from 35.0% to 100.0%, measured per episode, significantly so under a
paired Wilcoxon test at every recall level examined, whereas the fixed-rule
baseline did not reach a recall of 0.40 without raising an alert on every event
in the log. The gain was not free: the same
configuration raised from 75.8% to 96.0% the share of legitimate episodes that
produced an alert, and adding accumulated exposure did not significantly reduce
the false positive rate under any recall regime, so that the results support a
claim of reduced noise and increased coverage on the measured scenarios, at a
declared recall regime, and not one of absent cost.

**Keywords:** behavioural risk, log analysis, anomaly detection, fixed rules,
simulated corporate environment

***

## O que esta página ainda precisa

* [x] As duas frases finais do Resumo, com o resultado principal e a conclusão
* [x] As duas frases finais do Abstract, espelhando as do Resumo
* [x] **Reescritas sobre múltiplas sementes** em 12/11/2026, pela **D-13** — dez
  execuções independentes, com média, desvio-padrão e teste pareado
* [x] **A quarta configuração**, executada em 11/11/2026 pela **D-44**
* [ ] **A decisão sobre os e-mails** no bloco de autores, por ser repositório
  público
* [ ] **Uma pessoa ler o Abstract inteiro** antes de assinar
