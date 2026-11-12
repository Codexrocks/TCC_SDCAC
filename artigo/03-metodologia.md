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
> Os três blocos **A escrever** abaixo são lacunas conhecidas, com dono e
> prazo. Estão visíveis de propósito: comentário HTML desaparece quando o
> GitBook salva.

***

## 3.1 Natureza e tipo de pesquisa

Este trabalho caracteriza-se como pesquisa **aplicada**, de abordagem
**quantitativa** e procedimento **experimental**, na modalidade de
desenvolvimento de protótipo: há manipulação controlada de uma variável
independente — a configuração de avaliação empregada —, medição de seu efeito
sobre grandezas definidas previamente à execução, e comparação apoiada em
métricas numéricas e teste de hipótese. Não é exploratória: há hipótese
direcional declarada na pergunta de pesquisa e grupo de controle explícito.

## 3.2 Ambiente experimental simulado

A avaliação é conduzida sobre um ambiente corporativo simulado, gerado
integralmente por software, que representa uma organização de 250 funcionários ao
longo de um ano de operação, com volume médio de 20 a 50 eventos por dia útil por
funcionário.

Os registros cobrem oito tipos de evento — autenticação, acesso e transferência
de arquivos, dispositivos removíveis, navegação, *phishing* simulado e alteração
de configuração de conta —, cada um com atributos próprios e listas fechadas de
valores. Parte da postura de segurança não é evento, mas condição que dura:
atualização do dispositivo, antivírus, segundo fator e privilégio da conta são
registrados como **estado diário**, lidos na condição vigente na data do evento
avaliado.

A separação entre dados e gabarito é estrutural, e não procedimental: o ambiente
é distribuído em três bases — `corp`, com os eventos **sem rótulo**, a única
visível à aplicação; `ground_truth`, com os episódios e seus rótulos, lida
exclusivamente pela rotina de métricas; e `sdcac`, com padrões, notas e alertas.
O usuário de banco da aplicação **não recebe permissão de conexão** à
`ground_truth`, o que impede por construção o vazamento de rótulo.

**Não há dado de pessoa real** em nenhuma etapa: funcionários, recursos,
dispositivos e domínios são fictícios, estes no espaço reservado `.example`. E os
valores que descrevem a simulação são **parâmetros declarados do gerador**, e não
estimativas extraídas de organizações reais — nenhuma conclusão deste trabalho
depende de sua correspondência com o mundo real.

## 3.3 Desenho experimental

A comparação central é organizada como **estudo de ablação** — procedimento em
que as componentes de um modelo são ativadas progressivamente, uma por vez, de
modo que o ganho atribuível a cada uma possa ser isolado. São definidas quatro
configurações, executadas sobre os mesmos eventos, os mesmos cenários e as mesmas
métricas.

| Configuração | Composição | Papel no experimento |
|---|---|---|
| **C0** | Regras fixas sobre o evento isolado, com limiares idênticos para todos os usuários | Grupo de controle |
| **C1** | D1 — risco do evento individual | Ganho de atributos mais ricos sobre a mesma lógica pontual |
| **C2** | D1 + D2 — desvio em relação ao padrão do próprio funcionário | Ganho de contexto individual |
| **C3** | D1 + D2 + D3 — exposição acumulada e higiene de segurança | Contribuição original do trabalho |

A C0 cumpre a função de grupo de controle e **não possui parâmetro aprendido**:
seus limiares são fixos, idênticos para todos, e nenhuma regra consulta o padrão
individual — a noção de origem habitual vem de faixas de rede previamente
cadastradas, e não do histórico de cada usuário, para que a informação cuja
contribuição se pretende medir não esteja presente no controle. Mantém-se, por
outro lado, a contagem de falhas de autenticação em janela fixa de dois minutos,
que é correlação de curto prazo e não perfil individual; como a C0 dispõe dessa
regra, o reconhecimento de tentativas sucessivas **não pode ser atribuído como
ganho** às dimensões avaliadas.

As quatro configurações não são quatro sistemas, mas um único código sob quatro
parâmetros, de modo que a única variável entre as linhas da tabela de resultados
seja a dimensão acrescentada. Os pesos e os pontos de cada regra são
**parâmetros declarados** do modelo, preliminares e sujeitos a análise de
sensibilidade: eles ordenam o que o detector prioriza, e não a gravidade
conceitual dos sinais de segurança, que é questão distinta. A terceira dimensão reporta **duas parcelas
separadas** — exposição acumulada e higiene de segurança —, que não são somadas:
a agregação exigiria um peso relativo entre conduta e postura sem justificativa
defensável, e a separação preserva a decomponibilidade do risco por dimensão.

A hipótese admite refutação: caso a C3 não apresente ganho mensurável sobre a C2,
esse resultado responde negativamente à pergunta de pesquisa e é reportado como
tal.

## 3.4 Cenários e gabarito

Sobre o tráfego normal são injetados cenários de teste em quatro famílias: **P**,
pontuais, exercita a D1 sobre evento isolado; **B**, de contexto, exercita a D2;
**L**, longitudinais, exercita a D3 com escalada gradual sem evento
individualmente notável; e **N**, controle negativo, submete todas as dimensões a
comportamento legítimo.

A família N dá medida ao falso positivo. Além do ruído legítimo do tráfego de
fundo — férias, afastamento, mudança de cargo e trabalho remoto —, ela inclui um
cenário de **escalada legítima**: um funcionário que, por mudança de projeto,
passa a acessar mais recursos, em horário mais amplo e com maior volume, sem
conduta indevida. Sem ele a terceira dimensão não tem como ter seu falso positivo
medido.

O gabarito é produzido pelo próprio gerador: cada cenário grava seu identificador
e seu rótulo na base `ground_truth`, à qual a aplicação não tem acesso. A
avaliação compara, portanto, a saída do sistema a um gabarito que ele não pode
consultar.

O catálogo implementado reúne **20 cenários nomeados** — 6 em P, 4 em B, 4 em L
e 6 em N — e produz **124 episódios por semente**: 24, 16, 12 e 72,
respectivamente. O desequilíbrio da família N é deliberado, porque o controle
negativo precisa ser frequente para que o falso positivo tenha massa onde ser
medido; um de seus cenários, a janela de manutenção noturna, não é injetado e
pertence à rotina normal do gerador, respondendo por 53 dos 72 episódios da
família.

Cada episódio do gabarito registra a versão do catálogo que o produziu, e a
especificação dos cenários foi produzida **sem acesso às fórmulas de
pontuação** — as duas coisas importam para a objeção de desenho não cego da
Seção 3.8.

## 3.5 Unidade de análise

A escolha da unidade de análise altera substantivamente o valor das métricas, e
por isso é declarada de forma explícita. São adotadas duas unidades, aplicadas a
conjuntos distintos de cenários e reportadas separadamente: para os cenários
pontuais a unidade é o **evento**, classificado individualmente; para os de
contexto e longitudinais é o **episódio**, definido como o par funcionário ×
cenário — um cenário que se desenvolve ao longo de dez dias constitui um único
episódio, detectado ou não.

A distinção não é de forma: num cenário longitudinal cujo risco só cruza o limiar
no oitavo dia, a medição por evento rende revocação próxima de 0,15 ainda que o
episódio tenha sido identificado como se pretendia, enquanto a medição por
episódio rende 1,00. Toda tabela de resultados identifica a unidade em que cada
valor foi apurado, e nenhuma linha combina as duas.

## 3.6 Métricas e critério de sucesso

São definidas duas métricas primárias, ambas derivadas da pergunta de pesquisa. A
primeira é a **taxa de falsos positivos a revocação fixa**: para cada
configuração determina-se o limiar em que todas atingem uma mesma revocação de
referência, e comparam-se as taxas nesse ponto.

$$\mathrm{FPR} = \frac{FP}{FP + VN}$$

A segunda é a **revocação em cenários longitudinais**, calculada exclusivamente
sobre a família L, em unidade de episódio.

$$\mathrm{Revocação}_{L} = \frac{VP_{L}}{VP_{L} + FN_{L}}$$

**O critério de sucesso é declarado em termos operacionais**, em dois valores:
considera-se absorvível por um analista o teto de **45 alertas falsos por turno**,
do que decorre a exigência de alcançar a revocação de referência de 0,20 sem
ultrapassar esse volume; e exige-se **revocação longitudinal mínima de 0,80**,
medida por episódio sobre a família L. Ambos foram fixados **em 12/11/2026,
posteriormente à primeira execução registrada**, e por isso se registra sua
procedência: vêm do argumento operacional sobre a capacidade de triagem, e não da
tabela de resultados — critério derivado do resultado não é critério, é
justificação.

A comparação a revocação fixa pressupõe que a linha de base alcance a revocação
de referência em algum limiar. Como a C0 reúne poucas regras discretas e não
dispara em cenários longitudinais, essa condição pode verificar-se apenas no
limiar mínimo — e aí a taxa de falsos positivos resultante é o próprio resultado:
alcançar a revocação alertando o registro inteiro.

> ✅ **Lacuna 3 fechada em 12/11/2026.** O critério da **D-15** está declarado
> acima, em 45 alertas falsos por turno, com a data em que foi declarado.
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
> ⚠️ **O prazo venceu em 11/11/2026**, com a primeira execução registrada. O
> texto anterior desta nota dizia que "ainda dá tempo de ser *a priori*", e a
> condição que ele descrevia deixou de valer: existe resultado versionado. O que
> resta é declarar o número **pelo argumento operacional, sem olhar a tabela da
> Seção 4.3**, e registrar que foi declarado depois — porque critério escrito
> depois do resultado não é critério, é justificação, e a diferença entre as duas
> é exatamente o que a Seção 3.8 chama de ameaça à validade. Declarar e admitir a
> data é defensável; declarar e omitir, não.

## 3.7 Execução e reprodutibilidade

Cada configuração é executada sobre *N* sementes de geração independentes, com
*N* entre 10 e 20, e as mesmas sementes são utilizadas nas quatro. Cada valor da
tabela de resultados é reportado como média e desvio-padrão sobre as *N*
execuções, e não como valor único.

O uso das mesmas sementes nas quatro configurações torna a comparação
**pareada**: para cada semente existe uma diferença observada entre
configurações, e o conjunto dessas *N* diferenças é submetido ao teste de
Wilcoxon para amostras pareadas (Wilcoxon, 1945), adequado por não pressupor
normalidade e recomendado para comparar configurações sobre múltiplos conjuntos
de dados (Demšar, 2006). O piso de dez sementes decorre da aritmética do teste, e
não de convenção: o menor valor de *p* bilateral obtenível com *n* pares é
$2/2^{n}$, de modo que com *n* = 5 o limite é 0,0625 — acima de 0,05 ainda que
uma configuração superasse a outra em todas as execuções — e com *n* = 10 cai a
cerca de 0,002.

A reprodutibilidade é assegurada pelo registro de execução: cada execução grava
identificador, semente, configuração, versão dos pesos, o resumo SHA-256 da
configuração serializada em ordem canônica e o *commit* do código. Comparar duas
configurações consiste, operacionalmente, em comparar dois identificadores de
execução sobre o mesmo conjunto de eventos.

O protótipo é implementado em Python 3.12, e a camada de avaliação não conhece o
meio de armazenamento: o acesso é declarado por interfaces, cumpridas por uma
implementação sobre PostgreSQL e outra sobre arquivos em disco — esta por razão
metodológica, pois permite reproduzir o experimento sem servidor de banco. As
invariantes da Seção 3.8 são verificadas por testes automatizados a cada
alteração do código.

A execução se dá em cinco etapas encadeadas, cada uma um programa independente:
geração, tradução, pontuação, avaliação e agregação. A avaliação é a única que
acessa o gabarito, em coerência com a separação de permissões da Seção 3.2, e as
métricas da Seção 4 são lidas do arquivo que a agregação grava, não transcritas à
mão. A agregação **recusa** reunir execuções não comparáveis — limiar distinto,
níveis de revocação distintos, conjunto de configurações distinto, ou a mesma
execução contada duas vezes —, porque a média de execuções incomparáveis é um
número plausível que nada no resultado final denunciaria.

## 3.8 Ameaças à validade

Esta seção declara as ameaças à validade identificadas e as medidas adotadas,
segundo as quatro categorias usuais em experimentação em engenharia de software
(Wohlin et al., 2012).

**Validade de construto.** O risco comportamental é um construto: o que se mede
é a concordância entre a saída do sistema e um gabarito construído pelos próprios
autores. Mitigam a ameaça a declaração explícita da unidade de análise (Seção
3.5) e o reporte separado das parcelas da terceira dimensão.

**Validade interna.** O padrão individual é constituído sobre os três primeiros
meses do período simulado, janela **anterior e disjunta** da de avaliação:
calculá-lo sobre os dias que contêm os cenários injetados faria o comportamento
anômalo integrar a definição de normal, e o desempenho seria bom pelo motivo
errado (Kaufman et al., 2012). Pela mesma razão os atributos de estado são lidos
na condição vigente na data do evento, e o termo de exposição acumulada é
calculado sobre a janela que **antecede** o evento avaliado, excluindo-o —
incluí-lo contaria o risco do evento corrente duas vezes e, como a exposição soma
vários dias, faria o termo dominar a nota inclusive nos cenários pontuais. A
linha de base é mantida puramente estática, conforme a Seção 3.3.

**Circularidade do desenho.** A terceira dimensão é projetada para capturar
escalada gradual, os cenários longitudinais são projetados como escalada gradual,
e o experimento mede se a primeira detecta os segundos — arranjo que,
isoladamente, demonstra que a implementação funciona, não que a abordagem seja
adequada. Reduzem a objeção o controle negativo longitudinal da Seção 3.4 e a
separação entre quem especifica os cenários e quem implementa as fórmulas.

**Validade externa.** Os resultados valem para o ambiente simulado e não são
extrapoláveis a dados de produção: acurácia elevada sobre dados sintéticos deve
ser lida como indício de gerador demasiadamente previsível, e não como evidência
de qualidade do modelo (Sommer e Paxson, 2010). A mitigação é o ruído legítimo do
tráfego de fundo — viagens, trabalho remoto, afastamentos e mudanças de cargo —,
que impede o comportamento normal de ser artificialmente homogêneo.

**Validade de conclusão estatística.** Uma única execução por configuração não
distinguiria ganho sistemático de variação de amostragem; a mitigação é o desenho
da Seção 3.7.

**Tratamento de dados pessoais.** O monitoramento de comportamento de
colaboradores constitui tratamento de dado pessoal quando aplicado a organização
real; como este trabalho opera exclusivamente sobre dados sintéticos, a
legislação não o vincula operacionalmente. As implicações de uma implantação
real, à luz da Lei nº 13.709/2018 e dos controles aplicáveis da ISO/IEC
27001:2022, são tratadas entre as limitações e os trabalhos futuros.

## 3.9 O painel de análise

O painel é tratado como **instrumento de análise**, e não como objeto de
avaliação — decisão tomada em 14/10/2026. Sua função é tornar a nota decomponível
por dimensão, de modo que a contribuição de cada componente seja inspecionável
durante a análise dos resultados. **Não se realiza avaliação de usabilidade com
participantes**, o que mantém coerente a declaração de ausência de dado de pessoa
real da Seção 3.2, e o critério de aceite é funcional, registrado na documentação
do projeto.

***

## O que esta seção ainda precisa

* [x] ~~Lacuna 2~~ — desenho cego declarado em 14/10, confirmado pelo Davi
* [x] ~~Lacuna 4~~ — **D-02 fechada pela opção A** em 14/10
* [x] ~~**Lacuna 1**~~ — a **D-06** e a **D-16** fecharam em 12/11/2026, com a
      confirmação da Yasmin. O catálogo da § 3.4 descreve o que o gerador
      implementa, e cada episódio registra a versão que o produziu
* [x] ~~**Lacuna 3**~~ — o critério da D-15 foi declarado em 12/11/2026, em 45
      alertas falsos por turno, com a data registrada. A revocação longitudinal
      mínima continua por declarar
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
