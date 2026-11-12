# Cabeçalho e Resumo

> **Esta página é o bloco de abertura do documento montado**, e a ordem abaixo é
> a do [template COBEM](../docs/formato-do-artigo.md): título, autores,
> instituição, e-mails, resumo, palavras-chave. **O bloco em inglês saiu em
> 12/11/2026**, por autorização do orientador — ver a seção Abstract abaixo.
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
segurança. O método é um experimento comparativo em ambiente corporativo simulado, no qual
quatro configurações — uma linha de base de regras fixas e três com acréscimo
progressivo de dimensões — são aplicadas aos mesmos eventos e cenários,
permitindo medir isoladamente a contribuição de cada dimensão. As grandezas de comparação são a taxa de falsos positivos a uma
mesma revocação e a revocação em cenários longitudinais. Em dez execuções
independentes, com 1.436.275 ± 9.681 eventos avaliados em cada uma, a
configuração que soma o risco do evento ao desvio em relação ao padrão
individual reduziu a taxa de falsos positivos de 18,44% para 0,40% à revocação
de 0,20 e elevou a revocação em cenários longitudinais de 35,0% para 100,0%,
medida por episódio, com significância em teste pareado em todos os níveis
examinados, enquanto a linha de base de regras fixas não alcançou revocação de
0,40 sem emitir alerta sobre todo o registro. O ganho não foi gratuito: a mesma configuração elevou de
75,8% para 96,0% a proporção de episódios legítimos que produziram alerta, e o
acréscimo da exposição acumulada não reduziu significativamente a taxa de falsos
positivos em nenhum regime. Os resultados autorizam afirmar redução de ruído e
aumento de cobertura nos cenários medidos, e não ausência de custo.

**Palavras-chave:** risco comportamental, análise de logs, detecção de anomalias,
regras fixas, ambiente corporativo simulado

> **Separadas por vírgula**, e não por ponto. A regra de convivência do
> [README](README.md) é explícita: a lista de referências segue a ABNT NBR 6023,
> e **todo o resto segue o template COBEM** — que pede "up to 5 keywords
> separated by commas". A forma anterior, com ponto, vinha da NBR 6028 e valia
> enquanto a instrução do template não estava escrita.

***

## Abstract

> ⚠️ **Removido em 12/11/2026, por autorização do orientador relatada pelo
> Davi.** Esta página dizia, desde **04/09/2026**, que o abstract em inglês era
> **obrigatório** e que isso havia sido *"confirmado com o orientador"*. A
> autorização de agora **reverte** aquela confirmação, e fica registrada aqui com
> data e com quem a trouxe, em vez de o texto simplesmente desaparecer.
>
> **O que isso vale em páginas:** o bloco em inglês ocupava cerca de 0,4 página
> das 0,89 da abertura, e o artigo estava três páginas acima do teto de 12.
>
> **O texto não se perdeu.** Ele está no histórico do git, no commit que o
> removeu, e pode voltar inteiro se a autorização for revista — o que vale saber
> porque ele **nunca foi lido por uma pessoa**: a nota anterior registrava que
> tinha sido redigido com auxílio de IA e que precisava de leitura antes de ser
> assinado. Se voltar, volta com essa pendência.
>
> **Confirme por escrito com o orientador quando puder.** O que sustenta esta
> remoção hoje é um relato verbal; o que sustentava a exigência era uma
> confirmação de setembro registrada nesta página. A assimetria é do tipo que uma
> banca pergunta.

***

## O que esta página ainda precisa

* [x] As duas frases finais do Resumo, com o resultado principal e a conclusão
* [x] ~~As duas frases finais do Abstract~~ — o Abstract saiu em 12/11/2026
* [x] **Reescritas sobre múltiplas sementes** em 12/11/2026, pela **D-13** — dez
  execuções independentes, com média, desvio-padrão e teste pareado
* [x] **A quarta configuração**, executada em 11/11/2026 pela **D-44**
* [ ] **A decisão sobre os e-mails** no bloco de autores, por ser repositório
  público
* [x] ~~Uma pessoa ler o Abstract inteiro~~ — não se aplica: ele saiu antes de
  ser lido, e isso está dito na seção Abstract
