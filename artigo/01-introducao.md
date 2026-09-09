# 1. Introdução

> **Entrega: 10/09/2026** — Tarefa 02 do professor. Responsável: todos. Esta é a seção mais urgente do artigo.
>
> **Formato COBEM**, lido do template oficial em 07/09/2026. O que muda está em [COBEM](../docs/cobem.md#o-que-isto-muda-no-artigo), e a primeira consequência é de tamanho: **o artigo inteiro tem de 4 a 8 páginas.**
>
> A Contextualização abaixo pedia "duas ou três páginas" — um terço do artigo antes de chegar ao problema. Combine a divisão com a equipe antes de escrever.
>
> O que está abaixo é **estrutura, não conteúdo**. Cada bloco começa com uma instrução **A escrever**. Apague a instrução quando preencher o bloco — ela existe para ser substituída pelo seu texto.\
> <br>
>
> > **Nota de versão:** Esta é uma versão parcial da Introdução. Os trechos sinalizados para complementação correspondem às contribuições específicas dos demais integrantes da equipe e serão incorporados nas etapas subsequentes de desenvolvimento e revisão do artigo.

***

## Contextualização

> A crescente digitalização das organizações tem ampliado significativamente a quantidade de informações geradas pelos sistemas computacionais. Atividades como autenticações, acessos a arquivos, alterações de credenciais, conexões de dispositivos e demais interações realizadas pelos usuários são registradas na forma de eventos e logs, constituindo uma importante fonte de informação para o monitoramento e a compreensão do funcionamento dos ambientes corporativos.
>
> A gestão adequada desses registros é fundamental para a análise de atividades realizadas nos sistemas, permitindo reunir informações relevantes sobre eventos ocorridos em uma infraestrutura computacional. Entretanto, o aumento da quantidade e da diversidade dos dados registrados também amplia a complexidade associada à sua interpretação e ao acompanhamento das atividades realizadas pelos usuários (NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY, 2006).
>
> A análise desses registros permite identificar padrões de utilização, desvios comportamentais e situações que demandam maior atenção por parte das equipes responsáveis pela segurança e pela gestão dos sistemas. Contudo, a elevada quantidade de eventos produzidos diariamente e a diversidade de comportamentos legítimos tornam a interpretação desses dados uma atividade complexa, especialmente quando o comportamento considerado incomum depende do contexto em que determinado evento ocorre.
>
>
>
> **\[COMPLEMENTAÇÃO — YASMIN]**
>
> > **Responsabilidade:** contextualização especializada sobre segurança da informação e análise comportamental.
> >
> > **Inserir conteúdos relacionados a:**
> >
> > * monitoramento de segurança;
> > * análise de eventos e logs;
> > * ameaças internas;
> > * SIEM e SOC;
> > * UEBA ou análise comportamental de usuários;
> > * importância da contextualização na identificação de atividades potencialmente anômalas.
> >
> > **Critério de aceite:** texto acadêmico integrado ao fluxo desta seção, com referências bibliográficas reais e citações no padrão adotado pelo artigo.
>
>
>
> **\[COMPLEMENTAÇÃO — FILIPE]**
>
> > **Responsabilidade:** fundamentação quantitativa do contexto.
> >
> > **Inserir conteúdos relacionados a:**
> >
> > * volume de eventos gerados em ambientes corporativos;
> > * quantidade de alertas;
> > * índices ou impactos relacionados a falsos positivos;
> > * fadiga de alertas;
> > * impacto operacional da análise manual.
> >
> > **Critério de aceite:** apresentar dados com fonte, ano, contexto e referência bibliográfica verificável.
>
>
>
> A análise de eventos isolados pode ser útil para identificar situações previamente conhecidas ou condições que ultrapassam determinados limites. Entretanto, uma atividade considerada incomum segundo uma regra genérica não representa necessariamente uma ameaça ou comportamento malicioso. O conceito de anomalia está relacionado à identificação de observações que divergem de um comportamento esperado, sendo necessário considerar o contexto e as características do conjunto analisado para interpretar adequadamente esses desvios (CHANDOLA; BANERJEE; KUMAR, 2009).
>
> Um acesso realizado fora do horário convencional, por exemplo, pode representar uma situação incomum para determinado usuário, mas pode ser compatível com a rotina de outro profissional que exerce atividades em regime de plantão ou possui uma jornada diferenciada. Dessa forma, a utilização de parâmetros genéricos pode apresentar limitações quando aplicada a usuários que possuem padrões de comportamento distintos.
>
> Além disso, determinadas situações potencialmente relevantes podem não ser identificadas quando cada evento é analisado individualmente. Uma sequência de atividades aparentemente pouco significativas pode, quando observada ao longo do tempo, indicar mudanças graduais no comportamento ou uma exposição progressiva ao risco. Nesse contexto, torna-se relevante investigar abordagens capazes de integrar diferentes níveis de informação, considerando simultaneamente as características do evento individual, o comportamento histórico do usuário e a evolução temporal das atividades registradas.

## Problema

>
>
> A análise de segurança baseada exclusivamente em eventos individuais e regras fixas apresenta limitações relacionadas à interpretação do contexto em que as atividades ocorrem. Uma divergência em relação a uma regra previamente estabelecida não representa, necessariamente, uma ameaça, uma vez que atividades legítimas podem apresentar características consideradas incomuns por mecanismos genéricos de detecção.
>
> Essa limitação está relacionada ao próprio desafio de definir o que caracteriza um comportamento anômalo em ambientes complexos. Conforme discutido por Chandola, Banerjee e Kumar (2009), a identificação de anomalias depende da compreensão dos padrões considerados normais dentro do contexto analisado, podendo diferentes métodos apresentar interpretações distintas sobre os desvios observados.
>
> Quando características individuais dos usuários não são consideradas durante o processo de avaliação, atividades legítimas podem ser classificadas como suspeitas apenas por apresentarem divergências em relação a padrões gerais. Além disso, a análise isolada de cada evento pode dificultar a identificação de situações que se desenvolvem gradualmente, uma vez que determinados comportamentos somente se tornam relevantes quando avaliados em conjunto e ao longo de determinado período.
>
> Assim, uma abordagem baseada exclusivamente em regras fixas aplicadas a eventos individuais apresenta limitações para representar diferenças entre os padrões comportamentais dos usuários e para considerar situações em que a exposição ao risco se desenvolve progressivamente a partir da recorrência ou combinação de eventos.
>
> A problemática central deste trabalho consiste, portanto, em investigar em que medida a incorporação de informações contextuais relacionadas ao comportamento individual dos usuários e à evolução temporal dos eventos pode contribuir para a avaliação de comportamentos potencialmente anômalos em comparação com uma abordagem baseada exclusivamente em regras fixas aplicadas a eventos isolados.
>
> Nesse sentido, busca-se analisar se a integração das diferentes dimensões de risco permite uma avaliação mais contextualizada dos eventos e contribui para a diferenciação entre comportamentos legítimos e atividades que apresentam características potencialmente divergentes no ambiente corporativo simulado.
>
>
>
> **\[COMPLEMENTAÇÃO — YASMIN]**
>
> > **Responsabilidade:** aprofundamento da fundamentação do problema no domínio da segurança.
> >
> > **Inserir conteúdos relacionados a:**
> >
> > * limitações da detecção baseada exclusivamente em regras;
> > * diferença entre comportamento normal e anômalo;
> > * ameaças internas;
> > * relevância da análise comportamental;
> > * desafios da identificação de comportamentos suspeitos.
> >
> > **Critério de aceite:** fundamentar os argumentos com referências científicas, evitando repetir conceitos já apresentados na contextualização.
>
>
>
> **\[COMPLEMENTAÇÃO — FILIPE]**
>
> > **Responsabilidade:** aprofundamento quantitativo do problema.
> >
> > **Inserir conteúdos relacionados a:**
> >
> > * falsos positivos;
> > * grande volume de eventos;
> > * impacto operacional da geração excessiva de alertas;
> > * métricas ou estudos que demonstrem a dimensão quantitativa do problema.
> >
> > **Critério de aceite:** utilizar dados verificáveis e conectar explicitamente os indicadores apresentados à problemática da pesquisa.

## Justificativa

>
>
> A necessidade de aprimorar os mecanismos de interpretação de eventos computacionais torna relevante a investigação de abordagens capazes de considerar diferentes níveis de contexto durante a avaliação de riscos. Enquanto a análise isolada permite identificar características específicas de cada evento, a inclusão do histórico comportamental possibilita considerar as particularidades associadas a cada usuário. Adicionalmente, a análise temporal permite observar situações em que o risco não se manifesta de forma imediata, mas pode se desenvolver progressivamente por meio da recorrência e da combinação de atividades.
>
> A proposta deste trabalho busca contribuir para essa discussão por meio do desenvolvimento de um modelo experimental de avaliação multidimensional de risco comportamental. A abordagem será estruturada para permitir a comparação entre diferentes configurações de avaliação, partindo de uma linha de base baseada em regras fixas e incorporando progressivamente novas dimensões de análise.
>
> A primeira dimensão considera características associadas diretamente ao evento registrado, incluindo atributos como horário, endereço de origem, dispositivo utilizado, localização e demais características relevantes ao contexto da atividade. A segunda dimensão considera a relação entre os eventos observados e o padrão comportamental previamente estabelecido para cada usuário. A terceira dimensão busca avaliar a exposição acumulada ao risco a partir da recorrência, combinação e evolução temporal dos comportamentos observados.
>
> A relevância científica da proposta está na possibilidade de avaliar separadamente a contribuição das dimensões consideradas por meio de uma comparação experimental realizada sobre os mesmos eventos e cenários. Dessa forma, busca-se analisar o efeito da inclusão progressiva das diferentes dimensões de avaliação, evitando atribuir os resultados observados a uma única solução sem a possibilidade de comparação com uma linha de base.
>
> Do ponto de vista tecnológico, o trabalho também possibilita a aplicação integrada de conceitos de Engenharia de Software, análise de dados e sistemas de avaliação de risco. A construção de uma arquitetura capaz de gerar, ingerir, armazenar e avaliar eventos de forma estruturada permite a realização de experimentos controlados e reprodutíveis, mantendo condições equivalentes entre as diferentes configurações analisadas.
>
>
>
> **\[COMPLEMENTAÇÃO — YASMIN]**
>
> > **Responsabilidade:** justificar a relevância da proposta para o domínio da segurança.
> >
> > **Inserir conteúdos relacionados a:**
> >
> > * relevância da análise comportamental;
> > * importância da contextualização de eventos;
> > * necessidade de investigar comportamentos potencialmente anômalos;
> > * contribuição da proposta para os processos de monitoramento e análise.
> >
> > **Critério de aceite:** conectar diretamente a relevância da segurança ao problema apresentado na seção anterior.
>
>
>
> **\[COMPLEMENTAÇÃO — FILIPE]**
>
> > **Responsabilidade:** justificar quantitativamente a necessidade da proposta.
> >
> > **Inserir conteúdos relacionados a:**
> >
> > * custos operacionais;
> > * impacto de falsos positivos;
> > * quantidade de alertas;
> > * necessidade de mecanismos de priorização ou contextualização.
> >
> > **Critério de aceite:** apresentar evidências quantitativas e evitar repetir os mesmos dados utilizados na contextualização.

## Pergunta de pesquisa

> Diante das limitações associadas à análise isolada de eventos e à utilização exclusiva de regras fixas, este trabalho busca responder à seguinte pergunta de pesquisa:
>
> > A avaliação combinada do risco do evento individual, do desvio comportamental do usuário e da exposição acumulada ao risco **reduz a taxa de falsos positivos, a uma mesma revocação, e aumenta a revocação em cenários longitudinais** na identificação de comportamentos potencialmente anômalos, quando comparada à análise baseada exclusivamente em regras fixas aplicadas a eventos individuais, em ambiente corporativo simulado?
>
> A investigação será conduzida por meio da comparação entre diferentes configurações de avaliação aplicadas aos mesmos conjuntos de logs e cenários experimentais. Dessa forma, será possível analisar a contribuição progressiva das dimensões consideradas e avaliar seus efeitos em relação à linha de base estabelecida.

## Objetivos

### Objetivo geral

> Desenvolver um modelo de avaliação de risco baseado na análise integrada de eventos individuais, padrões comportamentais e exposição acumulada ao risco, avaliando sua contribuição em comparação com uma linha de base baseada em regras fixas aplicadas a eventos individuais, em um ambiente corporativo simulado.

### Objetivos específicos

> Para alcançar o objetivo geral, foram definidos os seguintes objetivos específicos:
>
> a) definir e modelar os tipos de eventos e os atributos necessários para representar atividades de usuários em um ambiente corporativo simulado, bem como gerar logs sintéticos correspondentes aos cenários experimentais;
>
> b) implementar uma linha de base baseada em regras fixas aplicadas a eventos individuais, a ser utilizada como referência para a comparação experimental;
>
> c) desenvolver um mecanismo de avaliação de risco do evento individual a partir de características previamente definidas, incluindo horário, endereço de origem, dispositivo, localização e demais atributos relevantes ao contexto do evento;
>
> d) implementar mecanismos capazes de identificar divergências entre os eventos observados e o padrão comportamental previamente estabelecido para cada usuário;
>
> e) desenvolver uma abordagem para avaliar a exposição acumulada ao risco a partir da recorrência, combinação e evolução temporal dos comportamentos observados;
>
> f) integrar as diferentes dimensões de avaliação em uma classificação final de risco;
>
> g) comparar as diferentes configurações de avaliação utilizando os mesmos conjuntos de eventos e cenários experimentais; e
>
> h) analisar os resultados obtidos por meio das métricas e critérios definidos para o experimento.

## Estrutura do trabalho

> O presente trabalho está organizado de forma a apresentar progressivamente os fundamentos teóricos, os procedimentos metodológicos e a avaliação da proposta desenvolvida.
>
> Inicialmente, esta introdução apresenta a contextualização do tema, o problema de pesquisa, a justificativa, a pergunta de pesquisa e os objetivos estabelecidos para o desenvolvimento do estudo.
>
> Em seguida, o referencial teórico apresenta os principais conceitos necessários para a compreensão do problema e da proposta, incluindo os fundamentos relacionados à análise de eventos, comportamentos potencialmente anômalos, avaliação de riscos e demais conceitos necessários à fundamentação do estudo.
>
> Posteriormente, a metodologia descreve a natureza da pesquisa, o ambiente experimental, os procedimentos utilizados para a geração e o tratamento dos eventos, as configurações avaliadas e os critérios definidos para a comparação dos resultados.
>
> A seção de resultados e discussões apresenta os dados obtidos durante os experimentos, a comparação entre as diferentes configurações e a análise das métricas utilizadas para avaliar os resultados alcançados.
>
> Por fim, a conclusão sintetiza as principais contribuições do trabalho, apresenta as limitações identificadas durante o desenvolvimento e indica possibilidades para trabalhos futuros.

***

## O que esta seção ainda precisa

* [ ] Contextualização com pelo menos três referências conferidas na fonte
* [x] Problema formulado como afirmação, não como pergunta
* [x] Pergunta de pesquisa única e respondível
* [x] Objetivo geral em uma frase
* [x] Objetivos específicos verificáveis, alinhados ao cronograma
* [ ] Revisão de português por alguém que não escreveu
* [ ] Conteúdo transposto para o template COBEM, dentro do limite de páginas
