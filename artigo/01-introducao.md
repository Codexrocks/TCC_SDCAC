# 1. Introdução

> **1ª Versão** na numeração do professor · entregue em **24/09/2026** ·
> caneta: Davi, com complementação de Yasmin e Filipe.
>
> **Este Markdown foi sincronizado em 13/10/2026 com o texto que o Davi
> preencheu no template COBEM.** O arquivo entregue ao professor estava à frente
> do repositório desde 24/09 — os seis blocos `[COMPLEMENTAÇÃO]` foram
> preenchidos fora daqui, e o que não está no repositório não existe para a
> banca.
>
> **Dois ajustes entraram junto, e estão declarados no fim desta página:** a
> dimensão 3 passou a incluir a higiene de segurança, pela **D-25**, e a seção
> foi encurtada para caber no teto de duas páginas.
>
> **Limites desta seção, do professor:** mínimo 1 e máximo 2 páginas, **sem
> figura, gráfico ou tabela**.

***

## Contextualização

A crescente digitalização das organizações tem ampliado significativamente a
quantidade de informações geradas pelos sistemas computacionais. Atividades como
autenticações, acessos a arquivos, alterações de credenciais, conexões de
dispositivos e demais interações realizadas pelos usuários são registradas na
forma de eventos e logs, constituindo uma importante fonte de informação para o
monitoramento e a compreensão do funcionamento dos ambientes corporativos.

A gestão adequada desses registros é fundamental para a análise das atividades
realizadas nos sistemas, e sua análise permite identificar padrões de utilização,
desvios comportamentais e situações que demandam maior atenção das equipes
responsáveis pela segurança. Entretanto, o aumento da quantidade e da diversidade
dos dados registrados amplia a complexidade associada à sua interpretação,
especialmente quando o comportamento considerado incomum depende do contexto em
que determinado evento ocorre (National Institute of Standards and Technology,
2006).

A análise de eventos isolados pode ser útil para identificar situações
previamente conhecidas ou condições que ultrapassam determinados limites.
Entretanto, uma atividade considerada incomum segundo uma regra genérica não
representa necessariamente uma ameaça ou comportamento malicioso. O conceito de
anomalia está relacionado à identificação de observações que divergem de um
comportamento esperado, sendo necessário considerar o contexto e as
características do conjunto analisado para interpretar adequadamente esses
desvios (Chandola et al., 2009).

Um acesso realizado fora do horário convencional, por exemplo, pode representar
uma situação incomum para determinado usuário, mas pode ser compatível com a
rotina de outro profissional que exerce atividades em regime de plantão ou possui
uma jornada diferenciada. Dessa forma, a utilização de parâmetros genéricos pode
apresentar limitações quando aplicada a usuários que possuem padrões de
comportamento distintos.

Além disso, determinadas situações potencialmente relevantes podem não ser
identificadas quando cada evento é analisado individualmente. Uma sequência de
atividades aparentemente pouco significativas pode, quando observada ao longo do
tempo, indicar mudanças graduais no comportamento ou uma exposição progressiva ao
risco. Nesse contexto, torna-se relevante investigar abordagens capazes de
integrar diferentes níveis de informação, considerando simultaneamente as
características do evento individual, o comportamento histórico do usuário e a
evolução temporal das atividades registradas.

## Problema

A análise de segurança baseada exclusivamente em eventos individuais e regras
fixas apresenta limitações relacionadas à interpretação do contexto em que as
atividades ocorrem. Uma divergência em relação a uma regra previamente
estabelecida não representa, necessariamente, uma ameaça, uma vez que atividades
legítimas podem apresentar características consideradas incomuns por mecanismos
genéricos de detecção.

Essa limitação está relacionada ao próprio desafio de definir o que caracteriza
um comportamento anômalo em ambientes complexos. Conforme discutido por Chandola
et al. (2009), a identificação de anomalias depende da compreensão dos padrões
considerados normais dentro do contexto analisado, podendo diferentes métodos
apresentar interpretações distintas sobre os desvios observados.

Quando características individuais dos usuários não são consideradas durante o
processo de avaliação, atividades legítimas podem ser classificadas como
suspeitas apenas por apresentarem divergências em relação a padrões gerais. Além
disso, a análise isolada de cada evento dificulta a identificação de situações
que se desenvolvem gradualmente, uma vez que determinados comportamentos somente
se tornam relevantes quando avaliados em conjunto e ao longo de determinado
período.

A problemática central deste trabalho consiste, portanto, em investigar em que
medida a incorporação de informações contextuais relacionadas ao comportamento
individual dos usuários e à evolução temporal dos eventos pode contribuir para a
avaliação de comportamentos potencialmente anômalos, em comparação com uma
abordagem baseada exclusivamente em regras fixas aplicadas a eventos isolados.

## Justificativa

A necessidade de aprimorar os mecanismos de interpretação de eventos
computacionais torna relevante a investigação de abordagens capazes de considerar
diferentes níveis de contexto durante a avaliação de riscos. Enquanto a análise
isolada permite identificar características específicas de cada evento, a
inclusão do histórico comportamental possibilita considerar as particularidades
associadas a cada usuário. Adicionalmente, a análise temporal permite observar
situações em que o risco não se manifesta de forma imediata, mas pode se
desenvolver progressivamente por meio da recorrência e da combinação de
atividades.

A proposta deste trabalho busca contribuir para essa discussão por meio do
desenvolvimento de um modelo experimental de avaliação multidimensional de risco
comportamental. A abordagem será estruturada para permitir a comparação entre
diferentes configurações de avaliação, partindo de uma linha de base baseada em
regras fixas e incorporando progressivamente novas dimensões de análise.

A primeira dimensão considera características associadas diretamente ao evento
registrado, incluindo atributos como horário, endereço de origem, dispositivo
utilizado, localização e demais características relevantes ao contexto da
atividade. A segunda dimensão considera a relação entre os eventos observados e o
padrão comportamental previamente estabelecido para cada usuário. A terceira
dimensão avalia a exposição acumulada ao risco, a partir da recorrência,
combinação e evolução temporal dos comportamentos observados, em conjunto com a
postura de segurança associada à conta e ao dispositivo utilizados; as duas
parcelas são reportadas separadamente, e não agregadas em um valor único.

A relevância científica da proposta está na possibilidade de avaliar
separadamente a contribuição das dimensões consideradas por meio de uma
comparação experimental realizada sobre os mesmos eventos e cenários. Dessa
forma, busca-se analisar o efeito da inclusão progressiva das diferentes
dimensões de avaliação, evitando atribuir os resultados observados a uma única
solução sem a possibilidade de comparação com uma linha de base.

Do ponto de vista tecnológico, o trabalho possibilita a aplicação integrada de
conceitos de Engenharia de Software, análise de dados e sistemas de avaliação de
risco. A construção de uma arquitetura capaz de gerar, ingerir, armazenar e
avaliar eventos de forma estruturada permite a realização de experimentos
controlados e reprodutíveis, mantendo condições equivalentes entre as diferentes
configurações analisadas.

## Pergunta de pesquisa

Diante das limitações associadas à análise isolada de eventos e à utilização
exclusiva de regras fixas, formula-se a seguinte pergunta de pesquisa:

> A avaliação combinada do risco do evento individual, do desvio comportamental
> do usuário e da exposição acumulada ao risco reduz a taxa de falsos positivos,
> a uma mesma revocação, e aumenta a revocação em cenários longitudinais na
> identificação de comportamentos potencialmente anômalos, quando comparada à
> análise baseada exclusivamente em regras fixas aplicadas a eventos individuais,
> em ambiente corporativo simulado?

A investigação será conduzida por meio da comparação entre diferentes
configurações de avaliação, aplicadas aos mesmos conjuntos de eventos e cenários
experimentais, de modo que a contribuição de cada dimensão possa ser medida
isoladamente.

## Objetivos

### Objetivo geral

Desenvolver um modelo de avaliação de risco baseado na análise integrada de
eventos individuais, padrões comportamentais e exposição acumulada ao risco,
avaliando sua contribuição em comparação com uma linha de base baseada em regras
fixas aplicadas a eventos individuais, em um ambiente corporativo simulado.

### Objetivos específicos

Para alcançar o objetivo geral, foram definidos os seguintes objetivos
específicos:

a) definir e modelar os tipos de eventos e os atributos necessários para
representar atividades de usuários em um ambiente corporativo simulado, bem como
gerar logs sintéticos correspondentes aos cenários experimentais;

b) implementar uma linha de base baseada em regras fixas aplicadas a eventos
individuais, a ser utilizada como referência para a comparação experimental;

c) desenvolver um mecanismo de avaliação de risco do evento individual a partir
de características previamente definidas, incluindo horário, endereço de origem,
dispositivo, localização e demais atributos relevantes ao contexto do evento;

d) implementar mecanismos capazes de identificar divergências entre os eventos
observados e o padrão comportamental previamente estabelecido para cada usuário;

e) desenvolver uma abordagem para avaliar a exposição acumulada ao risco a partir
da recorrência, combinação e evolução temporal dos comportamentos observados;

f) integrar as diferentes dimensões de avaliação em uma classificação final de
risco;

g) comparar as diferentes configurações de avaliação utilizando os mesmos
conjuntos de eventos e cenários experimentais; e

h) analisar os resultados obtidos por meio das métricas e critérios definidos
para o experimento.

## Estrutura do trabalho

Esta introdução apresenta a contextualização do tema, o problema de pesquisa, a
justificativa, a pergunta de pesquisa e os objetivos estabelecidos. Em seguida, o
referencial teórico delimita os elementos que caracterizam o problema, apresenta
como a literatura o enfrentou e identifica o processo adotado para implementar a
solução. A metodologia descreve a natureza da pesquisa, o ambiente experimental,
o desenho de comparação, as métricas e os critérios definidos. A seção de
resultados e discussão apresenta os dados obtidos, a comparação entre as
configurações e a análise das métricas. Por fim, a conclusão sintetiza as
contribuições, apresenta as limitações identificadas e indica possibilidades para
trabalhos futuros.

***

## O que mudou em 13/10, e por quê

| O que | Por quê |
|---|---|
| **A dimensão 3 passou a incluir a postura de segurança**, com as duas parcelas reportadas separadamente | É a **D-25**, fechada em 23/09. Sem o ajuste, a Introdução e a Metodologia descreviam a mesma dimensão de formas diferentes **dentro do mesmo arquivo entregue** |
| **Dois parágrafos da Contextualização viraram um** | Diziam a mesma coisa: o segundo falava em "complexidade associada à interpretação" e o terceiro, em "interpretação desses dados uma atividade complexa" |
| **Saiu o parágrafo final do Problema**, que começava com "Assim, uma abordagem baseada exclusivamente…" | Repetia, em outras palavras, os três parágrafos anteriores |
| **Saiu "uma avaliação mais contextualizada"** do fecho do Problema | O [plano](../docs/plano.md), seção 1.3, registra que essa expressão fica **fora** da formulação: ela é a conclusão que os números autorizam ou não, não a hipótese |
| **A Estrutura do trabalho foi condensada** de seis parágrafos para um | Era a seção mais repetitiva, e o conteúdo não se perdeu |
| **A chamada no texto ficou como está** — autor-ano em caixa normal | É a forma do template, que chegou em 13/10. A conversão valeu para o artigo inteiro de uma vez |

## O que esta seção ainda precisa

* [ ] **Conferir a extensão no template** — o teto é **2 páginas**, e a versão de
      24/09 estava em 2,1 · **Davi**
* [ ] **As fontes da contextualização conferidas**, e com até 5 anos de
      publicação, como o professor exige · **Davi**
* [ ] **Alinhar a granularidade dos objetivos** com o [plano](../docs/plano.md),
      que lista **OE1 a OE6** onde esta seção lista **a) a h)** · **Davi**
