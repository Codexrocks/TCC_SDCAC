# 2. Referencial Teórico

> **Escrito pela Yasmin**, dona do referencial teórico e do conteúdo de
> segurança. Entregue em 28/09/2026 — o insumo como recebido está em
> [`docs/insumos/referencial-teorico-yasmin-v2.md`](../docs/insumos/referencial-teorico-yasmin-v2.md).
>
> **Reorganizado e ampliado em 13/10/2026**, a pedido do Davi, para a estrutura
> que o professor descreveu na 3ª reunião: delimitar o problema por elementos,
> apresentar como outros autores o resolveram e, ao final, identificar uma
> metodologia. **Nenhuma fonte nova foi acrescentada** — as treze são as mesmas
> da entrega da Yasmin, e o que cada uma sustenta não foi ampliado. O texto novo
> é prosa de ligação e desenvolvimento do que o próprio repositório já afirma.
>
> **2ª Versão** na numeração do professor · **entrega em 18/10/2026**.
>
> ✅ **As treze foram conferidas na fonte e entraram em
> [`referencias.md`](referencias.md)** em 13/10/2026, em ABNT NBR 6023. A
> conferência é declaração da **Yasmin**, confirmada pelo **Davi**; a conversão
> de formato foi assistida por IA, a partir dos dados do insumo.

***

A seção organiza-se em três movimentos. O primeiro delimita o problema, com cada
par de parágrafos tratando de um elemento que o caracteriza. O segundo apresenta
como a literatura o enfrentou. O terceiro identifica, a partir desse mesmo
material, o processo que este trabalho adota para implementar a solução.

## 2.1 Os elementos que caracterizam o problema

### O registro é a evidência, e ele é volumoso e heterogêneo

A segurança da informação organiza-se, normativamente, em torno da preservação da
confidencialidade, integridade e disponibilidade da informação (International
Organization for Standardization, 2022). Um evento de acesso pode ser lido como
uma tentativa, bem-sucedida ou não, de comprometer uma dessas propriedades, o que
fundamenta a leitura de registros de log como indicadores de risco, e não como
categorias arbitrárias.

O registro dessas evidências ocorre por meio de logs de segurança, cuja gestão
cobre geração, armazenamento e análise dos eventos relevantes à postura de
segurança de um sistema (Kent e Souppaya, 2006).
Entre os campos que tipicamente apoiam a identificação de comportamento suspeito
estão a identidade do sujeito, o instante do evento, a origem de rede, o
dispositivo e o recurso afetado. A mesma fonte observa que o crescimento em
quantidade e em diversidade desses registros amplia a complexidade de
interpretá-los — o volume que torna a evidência rica é o que torna a leitura
difícil.

### O evento isolado não distingue falha de autenticação de abuso de autorização

Autenticação e autorização descrevem processos distintos e sequenciais. A
primeira verifica a identidade de um sujeito a partir de evidências vinculadas a
essa identidade (Grassi et al., 2017); a segunda decide quais ações um sujeito já
autenticado pode executar, tipicamente mediada por papéis (Sandhu et al., 1996).

A distinção importa porque as duas deixam rastros de naturezas diferentes. Falhas
de autenticação — horário atípico, repetição de tentativas, origem não habitual —
produzem eventos discretos, delimitados e fáceis de registrar. Violações de
autorização, ao contrário, costumam consistir em ações individualmente
permitidas: o sujeito acessa o que lhe é facultado, na ordem, no volume ou na
combinação que destoam do que lhe é habitual. Reconhecê-las exige conhecer o
padrão esperado daquele sujeito, informação que o evento isolado, por definição,
não carrega.

### A correlação por regras escritas à mão não acompanha o ambiente

Sistemas de gerenciamento de informações e eventos de segurança (SIEM) combinam
coleta multifonte, normalização e correlação de eventos para gerar alertas
priorizados a um analista humano (Gonzalez-Granadillo et al., 2021). Os mesmos
autores documentam uma limitação estrutural amplamente relatada: a correlação
depende de regras escritas manualmente, e o volume de alertas gerado tende a
exceder a capacidade de análise disponível.

A consequência prática é que a qualidade da detecção fica limitada pela
capacidade de alguém antecipar, por escrito, as condições que caracterizam um
comportamento indevido. Regra que não foi escrita não dispara; regra escrita de
forma genérica dispara sobre o legítimo. Em ambientes com rotinas heterogêneas —
turnos, plantões, trabalho remoto, viagens —, o mesmo limiar aplicado a toda a
organização produz os dois efeitos ao mesmo tempo.

### O volume de alertas excede a capacidade humana de triagem

Um Centro de Operações de Segurança (SOC) é a função organizacional responsável
por monitorar essa correlação e conduzir a triagem dos alertas resultantes. A
revisão sistemática de Vielberth et al. (2020) identifica, entre os desafios em
aberto mais recorrentes da literatura de SOC, exatamente esse descompasso entre o
volume de alertas e a capacidade humana de análise.

Os mesmos autores apontam um agravante que interessa diretamente a este trabalho:
a ausência de contexto comportamental na maior parte das ferramentas. O alerta
sinaliza que um evento ocorreu e que ele cruzou um limiar, mas não informa se
aquele evento é habitual para aquele usuário específico — que é precisamente a
informação de que o analista precisa para decidir se vale investigar.

### A raridade do evento malicioso faz o falso positivo dominar a fila

A rigidez do limiar fixo tem um efeito quantificável quando eventos maliciosos
são raros em relação ao volume total de eventos legítimos. Mesmo um detector com
taxa de falso positivo percentualmente pequena produz, em termos absolutos, uma
fila de alertas dominada por falsos positivos — a *base-rate fallacy*,
demonstrada formalmente por Axelsson (2000) no contexto da detecção de intrusão.

O resultado é que a precisão percebida de um detector não decorre apenas da sua
acurácia, mas da proporção entre as classes no ambiente em que ele opera. Dois
detectores com a mesma taxa de erro produzem experiências operacionais muito
diferentes conforme a raridade do que procuram, e essa diferença não aparece em
métricas que ignoram o desbalanceamento.

### O ruído se converte em exaustão, e a exaustão degrada a triagem

Em operação contínua, esse volume de ruído é uma das causas documentadas de
exaustão do analista de segurança, com impacto direto na qualidade da triagem
(Sundaramurthy et al., 2015). O problema deixa de ser apenas estatístico e passa
a ser organizacional: a fila que não se consegue examinar é, na prática, uma fila
não examinada.

Isso estabelece um critério de avaliação que a mera contagem de acertos não
captura. Um detector que encontra o que procura, mas ao custo de uma fila que
ninguém consegue percorrer, não resolve o problema de quem o opera — e é por isso
que a redução do falso positivo, e não apenas o ganho de cobertura, precisa
figurar entre as grandezas medidas.

### O agente interno tem credencial válida e não dispara o perímetro

A ameaça interna é um caso estruturalmente difícil para abordagens baseadas
apenas em autenticação e perímetro: o agente possui credencial válida e não
aciona os controles desenhados para deter um invasor externo.

Cappelli et al. (2012), a partir da análise de casos reais documentados pelo
CERT, distinguem padrões recorrentes de sabotagem, roubo de propriedade
intelectual e fraude. Homoliak et al. (2019), em revisão mais recente,
sistematizam essas taxonomias e os métodos de detecção associados a cada padrão,
incluindo abordagens comportamentais. Dos padrões descritos nesses trabalhos
interessa, para o problema aqui delimitado, o que se desenvolve ao longo do
tempo: a conduta que se instala gradualmente, sem que nenhum episódio isolado
reúna, sozinho, elementos suficientes para caracterizá-la.

### O limiar fixo não representa nem a diferença entre usuários nem a evolução temporal

A ideia de inferir atividade maliciosa a partir do desvio em relação a um perfil
de uso normal remonta a Denning (1987). Chandola et al. (2009) formalizam essa
ideia distinguindo três tipos de anomalia: a pontual, quando uma instância
isolada destoa do restante; a contextual, quando a mesma instância só é anômala
dentro de um contexto específico, como o histórico de um usuário; e a coletiva,
quando uma sequência de instâncias, nenhuma anômala isoladamente, é anômala em
conjunto.

A classificação explicita o limite da detecção por limiar fixo sobre eventos
individuais: ela endereça bem o primeiro tipo e, por construção, não representa
os outros dois. Um acesso noturno é anômalo para quem trabalha em horário
comercial e rotineiro para quem cumpre plantão — diferença contextual que o
limiar único não distingue. Uma sequência de acessos individualmente ordinários,
crescendo em volume e em abrangência ao longo de semanas, é anômala apenas em
conjunto — e nenhum dos seus eventos, lido isoladamente, justifica alerta.

## 2.2 Como a literatura enfrentou o problema

A resposta recorrente na literatura consultada consiste em deslocar a referência
da avaliação: em vez de comparar o evento a um limiar externo, compara-se o
evento ao comportamento previamente observado da própria entidade que o produziu.

*User and Entity Behavior Analytics* (UEBA) formula esse deslocamento de modo
explícito, substituindo a pergunta "este evento corresponde a um padrão de ataque
conhecido?" por "este evento é normal para esta entidade específica, dado o que
ela fez antes?". A abordagem constrói um perfil de comportamento habitual por
entidade e avalia o desvio dos eventos novos em relação a esse perfil (Shashanka
et al., 2016). O perfil individual responde ao elemento contextual do problema: o
mesmo evento passa a ter leituras diferentes conforme a rotina de quem o
produziu.

O tratamento do elemento temporal aparece de forma menos unificada. A
classificação de Chandola et al. (2009) nomeia a anomalia coletiva, mas trata-a
como categoria de um problema geral de detecção, e não como objeto de um
mecanismo próprio. Na literatura de ameaça interna, Homoliak et al. (2019)
registram abordagens comportamentais entre os métodos associados aos padrões que
se desenvolvem ao longo do tempo. O que o conjunto consultado não oferece é uma
avaliação que trate conjuntamente as três leituras — o evento, o desvio
individual e a acumulação temporal — mantendo-as **separáveis**, de modo que a
contribuição de cada uma possa ser medida isoladamente.

É nessa lacuna que este trabalho se situa. A proposta não é introduzir um
mecanismo de detecção inédito, e sim avaliar experimentalmente quanto cada uma
dessas leituras acrescenta sobre uma linha de base de regras fixas, medindo o
efeito sobre as duas grandezas que a literatura associa ao problema: a redução do
ruído, pelo argumento de Axelsson (2000) e de Sundaramurthy et al. (2015), e a
cobertura dos casos que só se manifestam em conjunto, pelo argumento de Chandola
et al. (2009) e de Homoliak et al. (2019).

## 2.3 A metodologia que se extrai deste referencial

Do material reunido nesta seção decorre um processo de implementação com quatro
passos, que a Metodologia detalha e executa.

O primeiro é **constituir o padrão individual** de cada usuário a partir de uma
janela de observação anterior e separada daquela em que a avaliação ocorre, de
modo que o comportamento a avaliar não participe da definição do que é normal
para aquele usuário.

O segundo é **avaliar o evento em três leituras distintas e separáveis**: as
características do evento em si, o desvio em relação ao padrão individual
constituído no passo anterior, e a acumulação ao longo de uma janela temporal.
Mantê-las separáveis é o que permite medir a contribuição de cada uma.

O terceiro é **estabelecer uma linha de base de regras fixas sobre eventos
isolados**, sem acesso ao histórico individual, para funcionar como grupo de
controle — a condição que a literatura descreve como o estado corrente do
problema.

O quarto é **comparar as configurações resultantes sobre os mesmos registros e
os mesmos cenários**, ativando uma leitura por vez, e medir o efeito sobre a taxa
de falsos positivos e sobre a cobertura dos casos temporais. O desenho de ablação
resultante, as métricas e o tratamento estatístico adotados são descritos na
seção seguinte.

***

## O que esta seção ainda precisa

* [ ] **As treze fontes conferidas na fonte** · **Yasmin** · antes de qualquer
      uma entrar em [`referencias.md`](referencias.md). É o bloqueio da entrega
      de **18/10**
* [ ] **Leitura da Yasmin sobre a reorganização.** O texto é dela; a estrutura
      nova e a prosa de ligação foram escritas a pedido do Davi, e nenhuma fonte
      nova entrou. **Ela precisa concordar com o que ficou atribuído a cada
      obra** · **Yasmin** · antes de 18/10
* [ ] **Conferir a extensão no template**, não na contagem de palavras — o
      professor pede **2 a 3 páginas** · **Davi**
* [ ] **Decidir se a usabilidade aplicada à segurança entra.** O material existe
      e tem fontes conferidas em [usabilidade](../docs/usabilidade.md), seção 7,
      e a §2.1 já trata da exaustão do analista · **Yasmin**
