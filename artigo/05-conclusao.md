# 5. Conclusão

> **5ª Versão** na numeração do professor — que junta **Conclusão e
> Referências** numa seção só, pela decisão **D-20** · S14 do
> [cronograma](../docs/cronograma.md) · Davi (caneta).

***

## 5.1 Retomada da pergunta de pesquisa

> **A escrever.** Responda **exatamente** esta pergunta, transcrita da
> [Introdução](01-introducao.md) para que a resposta não derive para uma
> parecida e mais fácil:
>
> *A avaliação combinada do risco do evento individual, do desvio comportamental
> do usuário e da exposição acumulada ao risco reduz a taxa de falsos positivos,
> a uma mesma revocação, e aumenta a revocação em cenários longitudinais na
> identificação de comportamentos potencialmente anômalos, quando comparada à
> análise baseada exclusivamente em regras fixas aplicadas a eventos individuais,
> em ambiente corporativo simulado?*
>
> São **duas** grandezas, e as duas precisam de resposta: falso positivo a
> revocação fixa, e revocação longitudinal. Responder só a uma é responder
> metade. Se a resposta for "parcialmente", diga parcialmente e explique o que
> faltou.

## 5.2 Objetivos alcançados

> **A escrever.** Percorra os objetivos específicos da Introdução, um a um,
> dizendo se foram cumpridos e com que evidência.
>
> Objetivo não cumprido se declara — a banca compara esta seção com a
> Introdução.

## 5.3 Contribuições

> **A escrever.** O que o trabalho deixa. Cinco itens existem e são
> verificáveis — não prometa nada além do que estiver no repositório:
>
> * o **protótipo**, com a camada de avaliação independente do meio de
>   armazenamento, o que permite reproduzir o experimento sem servidor de banco
> * as **quatro configurações canônicas** semeadas e somente-leitura, que tornam
>   a ablação repetível
> * o **conjunto de regras e pesos** versionado, com resumo criptográfico preso
>   a cada execução
> * os **cenários de teste automatizados**, e as invariantes de desenho da Seção
>   3.8 impostas por teste
> * o **contrato de leitura versionado**, que torna a nota decomponível
>   inspecionável por fora do painel
>
> Note que **a avaliação de usabilidade não é contribuição deste trabalho**: a
> **D-02** fechou pela opção A, e a Seção 3.9 declara o painel como instrumento.

## 5.4 Trabalhos futuros

> **A escrever.** O que ficou de fora e por quê. Amarrado às limitações da
> seção 4.6, item a item.
>
> Três já estão identificados, e os três têm origem registrada:
>
> * **Implantação sobre dado real, à luz da Lei nº 13.709/2018 e da ISO/IEC
>   27001:2022** — base legal, transparência ao titular, minimização e retenção.
>   É o par da limitação da Seção 4.6, e é a **D-19**
> * **Validação contra tráfego de produção**, que o ambiente simulado não
>   substitui — a Seção 3.8 declara a ameaça de validade externa
> * **Comparação com detector não supervisionado**, se a S10 não acontecer
>   dentro do prazo

***

## Resumo

> **Este é o item mais fácil de esquecer do TCC inteiro.** As diretrizes
> institucionais pedem o Resumo nesta mesma etapa, mas ele **não tem semana
> própria** no nosso cronograma. Ver [diretrizes](../docs/diretrizes.md).
>
> **Parcialmente escrito.** O parágrafo abaixo cobre **contexto, objetivo e
> método** — as três partes que não dependem de resultado. **Falta o resultado
> principal e a conclusão**, e eles não podem ser escritos antes de existirem:
> resumo redigido antes é resumo do que se pretendia fazer, não do que foi feito.
> Quem fechar a Seção 4 acrescenta as duas últimas frases aqui.

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
— são aplicadas aos mesmos conjuntos de eventos e cenários, sobre múltiplas
sementes de geração independentes, permitindo medir isoladamente a contribuição
de cada dimensão. As grandezas de comparação são a taxa de falsos positivos a uma
mesma revocação e a revocação em cenários longitudinais.

> **A escrever.** Duas frases finais: o resultado principal, com os números da
> Seção 4, e a conclusão que responde à pergunta de pesquisa.

**Palavras-chave:** risco comportamental. Análise de logs. Detecção de anomalias.
Regras fixas. Ambiente corporativo simulado.

> **Recuperadas do `.docx` entregue**, onde já estavam escritas e separadas por
> vírgula. Aqui ficam separadas por ponto, como a NBR 6028 pede e como o
> [README](README.md) desta pasta instrui.

***

## Abstract

> **O abstract em inglês é obrigatório**, além do Resumo em português —
> confirmado com o orientador em 04/09/2026, e exigido também pela estrutura do
> [formato do artigo](../docs/formato-do-artigo.md).
>
> ⚠️ **Onde o bloco em inglês fica no documento depende do template COBEM 2026**,
> que ainda não está no repositório. Na família ABCM ele costuma ir depois da
> lista de referências; confirmar quando o arquivo chegar.
>
> **É a única parte do artigo em inglês.** O resto é todo em português, decidido
> em 07/09/2026.
>
> No documento final este bloco vai para **o alto**, logo depois dos autores —
> antes da Introdução. Ele mora aqui porque é a 5ª Versão que a instituição
> cobra, e porque é quando ele é escrito.
>
> **Parcialmente escrito**, nas mesmas três partes do Resumo: contexto,
> objetivo e método. **Falta o resultado e a conclusão**, pelo mesmo motivo.
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
events and scenarios, over multiple independent generation seeds, so that the
contribution of each dimension can be measured in isolation. The comparison
quantities are the false positive rate at a fixed recall and the recall on
longitudinal scenarios.

> **A escrever.** As duas frases finais, espelhando as do Resumo.

**Keywords:** behavioural risk. Log analysis. Anomaly detection. Fixed rules.
Simulated corporate environment.

***

## O que esta seção ainda precisa

* [ ] Resposta direta à pergunta de pesquisa da Introdução
* [ ] Cada objetivo específico avaliado, inclusive os não cumpridos
* [ ] Resumo escrito — contexto, objetivo e método já estão; faltam resultado e
      conclusão, que dependem da Seção 4
* [x] Palavras-chave definidas — recuperadas do `.docx`, em 15/10/2026
* [ ] Abstract conferido por uma pessoa — foi redigido com auxílio de IA
* [x] Necessidade de abstract confirmada com o orientador — 04/09/2026
