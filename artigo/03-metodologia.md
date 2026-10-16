# 3. Metodologia

> **3ª Versão** na numeração do professor · S5 do
> [cronograma](../docs/cronograma.md) · caneta: **Davi**.
>
> **Rascunho assistido**, declarado pelo autor: a redação foi rascunhada por
> Claude Opus 5 a partir das fontes do próprio repositório, e o insumo como
> entregue está em
> [`docs/insumos/metodologia-davi-v1.md`](../docs/insumos/metodologia-davi-v1.md),
> com a procedência de cada subseção.
>
> **A chamada no texto segue a forma do template COBEM**, que chegou em
> 13/10/2026: autor-ano em caixa normal. A conversão valeu para o artigo
> inteiro de uma vez, como o [formato do artigo](../docs/formato-do-artigo.md)
> previa.
>
> ⚠️ **Nenhuma das sete citações foi conferida na fonte.** Elas estão
> registradas em [citações pendentes](../docs/citacoes-pendentes.md) e **não**
> entraram em [`referencias.md`](referencias.md), que só aceita entrada depois
> de alguém abrir a obra.
>
> Os quatro blocos **A escrever** abaixo são lacunas conhecidas, com dono e
> prazo. Estão visíveis de propósito: comentário HTML desaparece quando o
> GitBook salva.

***

## 3.1 Natureza e tipo de pesquisa

Este trabalho caracteriza-se como pesquisa de natureza **aplicada**, de abordagem
**quantitativa** e procedimento **experimental**, conduzida na modalidade de
**desenvolvimento de produto ou protótipo**. A classificação como experimental
decorre da existência de manipulação controlada de uma variável independente — a
configuração de avaliação empregada — e da medição de seu efeito sobre grandezas
definidas previamente à execução. O caráter quantitativo decorre de a comparação
entre configurações apoiar-se exclusivamente em métricas numéricas e em teste de
hipótese. Não se trata de pesquisa exploratória: há hipótese direcional declarada
na pergunta de pesquisa e grupo de controle explícito, descrito na Seção 3.3.

## 3.2 Ambiente experimental simulado

A avaliação é conduzida sobre um ambiente corporativo simulado, gerado
integralmente por software. O ambiente representa uma organização de 250
funcionários ao longo de um ano de operação, com volume médio de 20 a 50 eventos
por dia útil por funcionário, o que totaliza de 1,15 a 2,9 milhões de eventos por
semente de geração.

Os registros cobrem oito tipos de evento, abrangendo autenticação, acesso e
transferência de arquivos, conexão de dispositivos removíveis, navegação,
campanhas simuladas de *phishing* e alterações de configuração de conta. Cada
tipo carrega atributos próprios, especificados no catálogo de eventos que
acompanha o trabalho; a especificação completa, incluindo as listas fechadas de
valores e a estrutura das tabelas de apoio, não é reproduzida aqui.

Parte da postura de segurança não se expressa como evento, mas como condição que
dura: idade da última atualização do dispositivo, atividade do antivírus,
habilitação do segundo fator de autenticação e nível de privilégio da conta.
Esses atributos são registrados como estado diário e lidos sempre na condição
vigente na data do evento avaliado, nunca em seu estado final, de modo que
informação posterior não influencie a avaliação de um evento anterior.

A separação entre dados e gabarito é estrutural, e não apenas procedimental: o
ambiente é distribuído em três bases distintas. A base `corp` contém os eventos
sem qualquer rótulo e é a única visível à aplicação; a base `ground_truth` contém
os episódios e seus rótulos e é lida exclusivamente pela rotina de cálculo de
métricas; a base `sdcac` armazena os padrões, as notas e os alertas produzidos
pelo sistema. O usuário de banco utilizado pela aplicação não recebe permissão de
conexão à base `ground_truth`, o que impede por construção o vazamento de rótulo.
A integridade do conjunto gerado é verificada por testes automáticos executados
antes da carga, que rejeitam o lote em caso de violação de integridade
referencial ou de valor fora das listas fechadas.

Duas declarações se fazem necessárias. A primeira é que **não há dado de pessoa
real** em nenhuma etapa do trabalho: funcionários, recursos, dispositivos,
domínios e faixas de endereçamento são fictícios, e os domínios empregados
pertencem ao espaço reservado `.example`. A segunda é que os valores que
descrevem a simulação — número de funcionários, volume diário de eventos e
distribuição de perfis de uso — são **parâmetros declarados do gerador**,
escolhidos para produzir um ambiente plausível, e não estimativas empíricas
extraídas de organizações reais. Nenhuma conclusão deste trabalho depende de sua
correspondência com o mundo real.

## 3.3 Desenho experimental

A comparação central do trabalho é organizada como um **estudo de ablação** —
procedimento em que as componentes de um modelo são ativadas progressivamente,
uma por vez, de modo que o ganho atribuível a cada uma possa ser isolado. São
definidas quatro configurações de avaliação, executadas sobre os mesmos eventos,
os mesmos cenários e as mesmas métricas.

| Configuração | Composição | Papel no experimento |
|---|---|---|
| **C0** | Regras fixas sobre o evento isolado, com limiares idênticos para todos os usuários | Grupo de controle |
| **C1** | D1 — risco do evento individual | Ganho de atributos mais ricos sobre a mesma lógica pontual |
| **C2** | D1 + D2 — desvio em relação ao padrão do próprio funcionário | Ganho de contexto individual |
| **C3** | D1 + D2 + D3 — exposição acumulada e higiene de segurança | Contribuição original do trabalho |

A configuração C0 cumpre a função de grupo de controle e **não possui
parâmetro aprendido**: seus limiares são fixos, idênticos para todos os
usuários, e nenhuma de suas regras consulta o padrão comportamental individual.
A formulação anterior da linha de base incluía a noção de endereço de origem
habitual, obtida do histórico de cada usuário; essa regra foi substituída pela
verificação de pertencimento a faixas de rede corporativas previamente
cadastradas, de modo que a informação cuja contribuição o experimento pretende
medir não esteja presente no grupo de controle.

Mantém-se, por outro lado, a regra de contagem de falhas de autenticação em
janela fixa de dois minutos. A distinção relevante é entre correlação de curto
prazo e perfil individual: a janela não possui parâmetro estimado a partir do
comportamento do usuário, aplica o mesmo limiar a todos os usuários e não retém
informação além de seu próprio intervalo. Trata-se da forma usual de regra de
correlação em ferramentas de gestão de eventos de segurança, e sua remoção
produziria um grupo de controle incapaz de identificar tentativas sucessivas de
autenticação — cenário cuja detecção é trivial para regras fixas e cujo
reconhecimento, portanto, não poderia ser atribuído como ganho às dimensões
avaliadas.

As quatro configurações não correspondem a quatro sistemas distintos, mas a um
único código executado sob quatro parâmetros. Essa decisão garante que a única
variável entre as linhas da tabela de resultados seja a dimensão acrescentada.

A terceira dimensão reporta **duas parcelas separadas** — exposição acumulada e
higiene de segurança —, que não são somadas em um valor único. A agregação
exigiria um peso relativo entre conduta e postura sem justificativa defensável, e
a separação preserva a decomponibilidade do risco por dimensão.

Registre-se, por fim, que a hipótese admite refutação: caso a configuração C3 não
apresente ganho mensurável sobre a C2, esse resultado responde negativamente à
pergunta de pesquisa e é reportado como tal.

## 3.4 Cenários e gabarito

Sobre o tráfego considerado normal são injetados cenários de teste, organizados em
quatro famílias, cada uma destinada a exercitar um aspecto distinto do modelo.

| Família | Exercita | Papel |
|---|---|---|
| **P** — pontuais | D1 | Verdadeiros positivos de evento isolado |
| **B** — de contexto | D2 | Redução de falso positivo por contexto individual |
| **L** — longitudinais | D3 | Escalada gradual sem evento individualmente notável |
| **N** — controle negativo | Todas | Falsos positivos sobre comportamento legítimo |

A família N dá medida ao falso positivo. Além do ruído legítimo já presente no
tráfego de fundo — férias, afastamento, mudança de cargo e trabalho remoto —, ela
inclui ao menos um cenário de **escalada legítima**: um funcionário que, por
mudança de projeto, passa a acessar mais recursos, em faixa horária mais ampla e
com maior volume, sem que haja conduta indevida. Sem esse cenário a terceira
dimensão não tem como ter seu falso positivo medido, e é ela a contribuição
original do trabalho.

O gabarito é produzido pelo próprio gerador: cada cenário injetado grava seu
identificador e seu rótulo na base `ground_truth`, à qual a aplicação não tem
acesso. A avaliação compara, portanto, a saída do sistema a um gabarito que ele
não pode consultar.

> **A escrever — lacuna 1 · Yasmin · 01/10.** A relação nominal dos cenários de
> cada família depende da **D-06** e da **D-16**. Entra aqui uma tabela com, no
> mínimo, um cenário nomeado por família e ao menos um de escalada legítima.
> **Não escrever antes de existir.**

A especificação dos cenários foi produzida **sem acesso às fórmulas de
pontuação**: quem desenhou as famílias, os rótulos e os casos de escalada
legítima não dispunha dos pesos, dos limiares nem da forma de composição das
dimensões. A separação de papéis é registrada aqui porque é a resposta mais
direta à objeção de circularidade tratada na Seção 3.8 — a de avaliar um detector
com cenários moldados para que ele passe.

## 3.5 Unidade de análise

A escolha da unidade de análise altera substantivamente o valor das métricas, e
por isso é declarada de forma explícita. São adotadas duas unidades, aplicadas a
conjuntos distintos de cenários e reportadas separadamente. Para os cenários
pontuais a unidade é o **evento**: cada registro é classificado individualmente.
Para os cenários de contexto e longitudinais a unidade é o **episódio**, definido
como o par funcionário × cenário; um cenário longitudinal que se desenvolve ao
longo de dez dias constitui um único episódio, detectado ou não.

A distinção não é de forma. Considere-se um cenário longitudinal de dez dias, com
cerca de quarenta eventos, nenhum deles individualmente notável, em que a
terceira dimensão ultrapassa o limiar no oitavo dia. Medida por evento, a
detecção rende revocação próxima de 0,15, ainda que o sistema tenha identificado
o episódio exatamente como se pretendia. Medida por episódio, o mesmo caso rende
0,00 para a linha de base contra 1,00 para a configuração completa — valores que
descrevem o que efetivamente ocorreu.

A taxa de falsos positivos utiliza denominador único em todas as configurações:
falsos positivos por **funcionário-dia**. Apurá-la por evento compararia uma taxa
medida em eventos a detecções que só existem em janelas temporais. Toda tabela de
resultados identifica a unidade em que cada valor foi apurado, e nenhuma linha
combina as duas.

## 3.6 Métricas e critério de sucesso

São definidas duas métricas primárias, ambas derivadas diretamente da pergunta de
pesquisa. A primeira é a **taxa de falsos positivos a revocação fixa**: para cada
configuração determina-se o limiar em que todas atingem uma mesma revocação de
referência, e comparam-se as taxas de falsos positivos nesse ponto, apuradas em
funcionário-dia:

$$\mathrm{FPR} = \frac{FP}{FP + VN}$$

A segunda é a **revocação em cenários longitudinais**, calculada exclusivamente
sobre a família L, em unidade de episódio:

$$\mathrm{Revocação}_{L} = \frac{VP_{L}}{VP_{L} + FN_{L}}$$

Como métrica secundária reporta-se a **precisão@k**, isto é, a precisão restrita
aos *k* alertas de maior risco. A justificativa é operacional: o analista consome
o início de uma fila ordenada por risco, não a fila inteira, e a precisão no topo
descreve melhor a utilidade prática do detector do que a precisão global.

A comparação a revocação fixa pressupõe que a linha de base alcance a revocação
de referência em algum limiar. Como a configuração C0 combina um número reduzido
de regras discretas e não dispara em cenários longitudinais, essa condição pode
não se verificar. Nesse caso a comparação passa a ser feita entre **curvas de
precisão e revocação** completas, e não entre pontos isolados; em problemas de
classe fortemente desbalanceada, como é o caso, a curva de precisão-revocação é
mais informativa que a curva ROC (Davis e Goadrich, 2006; Saito e Rehmsmeier,
2015).

> **A escrever — lacuna 3 · Davi · imediato.** O critério de sucesso declarado
> a priori, da **D-15**.
>
> **A origem do número está decidida:** entre as três que a decisão admitia —
> literatura, linha de base medida da C0, ou argumento operacional —, adotou-se o
> **argumento operacional**, de quantos alertas falsos um analista absorve por
> turno. É a origem defensável sem resultado na mão, e dialoga com a fadiga de
> alerta tratada na [usabilidade](../docs/usabilidade.md).
>
> **Falta o número.** A frase a escrever fixa três valores: o teto de alertas
> falsos por turno que se considera absorvível; a redução de falsos positivos
> sobre a configuração C0 que daí decorre; e a revocação longitudinal mínima.
>
> **Ainda dá tempo de ser *a priori*:** em 14/10/2026 nenhum resultado havia sido
> versionado. A partir da primeira execução registrada, esta frase deixa de ser
> critério e passa a ser justificação de resultado — e a diferença entre as duas
> é o que a Seção 3.8 chama de ameaça à validade.

## 3.7 Execução e reprodutibilidade

Cada configuração é executada sobre *N* sementes de geração independentes, com
*N* entre 10 e 20, e as mesmas sementes são utilizadas nas quatro configurações.
Cada valor da tabela de resultados é reportado como média e desvio-padrão sobre
as *N* execuções, e não como valor único.

O uso das mesmas sementes nas quatro configurações torna a comparação **pareada**:
para cada semente existe uma diferença observada entre configurações, e o
conjunto dessas *N* diferenças é submetido ao teste de Wilcoxon para amostras
pareadas (Wilcoxon, 1945), adequado por não pressupor normalidade das diferenças
e recomendado para a comparação de configurações sobre múltiplos conjuntos de
dados (Demšar, 2006).

O piso de dez sementes decorre da aritmética do próprio teste, e não de
convenção: no Wilcoxon pareado exato, o menor valor de *p* bilateral obtenível
com *n* pares é $2/2^{n}$, atingido quando todas as diferenças têm o mesmo sinal.
Com *n* = 5 esse limite vale 0,0625 — acima de 0,05 ainda que uma configuração
superasse a outra em todas as execuções — e com *n* = 10 cai a aproximadamente
0,002.

A reprodutibilidade é assegurada pelo registro de execução. Cada execução grava
identificador, semente, configuração e versão dos pesos, além de dois valores que
permitem reconstituí-la: o resumo SHA-256 do conteúdo da configuração,
serializada em ordem canônica — de modo que configurações equivalentes produzam o
mesmo resumo, independentemente da ordem em que seus campos foram escritos —, e o
identificador do *commit* do código em execução. Cada avaliação produzida
referencia a execução que a originou, e comparar duas configurações consiste,
operacionalmente, em comparar dois identificadores de execução sobre o mesmo
conjunto de eventos.

O protótipo é implementado em Python 3.12, e a camada de avaliação não conhece o
meio de armazenamento: o acesso aos dados é declarado por interfaces, e duas
implementações as cumprem. A primeira opera sobre PostgreSQL, banco relacional
escolhido pela necessidade de janelas temporais por funcionário sobre volume da
ordem de milhões de registros. A segunda opera sobre arquivos em disco e existe
por razão metodológica: ela permite executar o experimento completo sem servidor
de banco de dados, o que reduz o custo de reprodução por terceiros. As
invariantes de desenho declaradas na Seção 3.8 — janelas de treino e de avaliação
disjuntas, exclusão do evento corrente do termo de exposição acumulada e
independência entre a camada de avaliação e o meio de armazenamento — são
verificadas por testes automatizados executados a cada alteração do código. A
interface de inspeção dos resultados é construída em Streamlit.

## 3.8 Ameaças à validade

Esta seção declara as ameaças à validade identificadas e as medidas adotadas,
organizadas segundo as quatro categorias usuais em experimentação em engenharia
de software (Wohlin et al., 2012).

**Validade de construto.** O risco comportamental é um construto, e não uma
grandeza diretamente observável; o que se mede é a concordância entre a saída do
sistema e um gabarito construído pelos próprios autores. A ameaça é mitigada pela
declaração explícita da unidade de análise (Seção 3.5) e pelo reporte separado
das parcelas da terceira dimensão, que evita agregar em um número único grandezas
de naturezas distintas.

**Validade interna.** O padrão individual de cada funcionário é constituído sobre
os três primeiros meses do período simulado, janela **anterior e disjunta** da
janela de avaliação. Calculá-lo sobre os mesmos dias que contêm os cenários
injetados faria o comportamento anômalo integrar a definição do que é normal para
aquele funcionário, e o desempenho observado seria bom pelo motivo errado
(Kaufman et al., 2012). Pela mesma razão, os atributos de estado são lidos na
condição vigente na data do evento, e não em seu estado final. O termo de exposição
acumulada é calculado sobre a janela que **antecede** o evento avaliado,
excluindo-o: incluí-lo contaria o risco do evento corrente duas vezes, elevando
seu peso efetivo à soma dos dois coeficientes, e — como a exposição soma o risco
de vários dias, em escala uma ordem de magnitude superior à do evento isolado —
faria o termo dominar a nota final inclusive nos cenários pontuais. Por fim, a linha de base é mantida puramente
estática, conforme a Seção 3.3, para que não incorpore a informação cuja
contribuição se pretende medir.

**Circularidade do desenho.** A terceira dimensão é projetada para capturar
escalada gradual, os cenários longitudinais são projetados como escalada gradual,
e o experimento mede se a primeira detecta os segundos. Isoladamente, esse
arranjo demonstra que a implementação funciona, não que a abordagem seja
adequada. Duas medidas reduzem a objeção: a inclusão do controle negativo
longitudinal descrito na Seção 3.4, que penaliza um detector excessivamente
sensível, e a separação entre quem especifica os cenários e quem implementa as
fórmulas de pontuação.

**Validade externa.** Os resultados valem para o ambiente simulado descrito e não
são extrapoláveis a dados de produção. Acurácia elevada sobre dados sintéticos
deve ser lida como indício de que o gerador pode ser demasiadamente previsível,
e não como evidência de qualidade do modelo (Sommer e Paxson, 2010). A mitigação
adotada é a presença de ruído legítimo no tráfego de fundo — viagens, trabalho
remoto, afastamentos e mudanças de cargo —, de modo que o comportamento normal
não seja artificialmente homogêneo.

**Validade de conclusão estatística.** Uma única execução por configuração não
permitiria distinguir ganho sistemático de variação de amostragem. A mitigação é
o desenho descrito na Seção 3.7: múltiplas sementes, comparação pareada e teste
de hipótese sobre as diferenças.

**Tratamento de dados pessoais.** O monitoramento de comportamento de
colaboradores constitui tratamento de dado pessoal quando aplicado a uma
organização real. Como este trabalho opera exclusivamente sobre dados sintéticos,
a legislação não o vincula do ponto de vista operacional; a discussão das
implicações de uma implantação real, à luz da Lei nº 13.709/2018 e dos controles
aplicáveis da norma ISO/IEC 27001:2022, é tratada entre as limitações e os
trabalhos futuros.

## 3.9 O painel de análise

O painel construído no trabalho é tratado como **instrumento de análise**, e não
como objeto de avaliação. Sua função é tornar a nota de risco decomponível por
dimensão, de modo que a contribuição de cada componente seja inspecionável
durante a análise dos resultados. Não se realiza avaliação de usabilidade com
participantes, e nenhum dado de pessoa real é coletado, em coerência com a
declaração da Seção 3.2. O critério de aceite do painel é funcional e está
registrado na documentação do projeto.

A **D-02 fechou em 14/10/2026 pela opção A**: o painel é instrumento de
análise, e não objeto de um segundo experimento. Não há avaliação com
participantes, o que mantém coerente a declaração de ausência de dado de pessoa
real da Seção 3.2.

***

## O que esta seção ainda precisa

* [x] ~~Lacuna 2~~ — desenho cego declarado em 14/10, confirmado pelo Davi
* [x] ~~Lacuna 4~~ — **D-02 fechada pela opção A** em 14/10
* [ ] **Lacuna 1** · **Yasmin** — a relação nominal dos cenários. Depende da
      **D-06** e da **D-16**, e de o gerador de eventos existir: em 14/10 não há
      gerador nem cenário nomeado no repositório
* [ ] **Lacuna 3** · **Davi** · **imediato** — o número do critério a priori. A
      origem já está escolhida; falta o valor, e ele perde o sentido no dia em
      que a primeira execução for registrada
* [ ] **As sete fontes conferidas na fonte** · **Davi** · antes de qualquer uma
      entrar em [`referencias.md`](referencias.md). As pendências estão em
      [citações pendentes](../docs/citacoes-pendentes.md), e o ano de
      `WOHLIN et al., 2012` está marcado como merecedor de atenção redobrada
* [ ] **Fundamentação da Seção 3.1, se o professor exigir.** Não há citação ali;
      a via usual é uma obra de metodologia científica em computação · **Davi**
* [ ] **Alinhar a granularidade dos objetivos** com a
      [Introdução](01-introducao.md), que lista **a) a h)** onde o
      [plano](../docs/plano.md) §1.5 lista **OE1 a OE6**. Não é contradição, é
      recorte — mas quem lê o artigo é a banca · **Davi**
* [ ] **A Introdução ainda descreve a dimensão 3 só como exposição acumulada**,
      e esta seção a descreve como exposição **e higiene**, com duas parcelas
      separadas (**D-25**). Enquanto não for ajustada, os dois capítulos se
      contradizem · **Davi** · S5
* [ ] **Confirmar se o template aceita fórmula em `$$…$$`**; se não aceitar,
      viram imagem ou texto corrido · **Davi** · quando o template do COBEM 2026
      chegar
* [ ] **Confirmar o tempo verbal.** A seção está no presente — "o ambiente
      representa", "cada configuração é executada" —, que lê corretamente antes
      e depois da execução. Se preferir futuro, a troca é mecânica · **Davi**
