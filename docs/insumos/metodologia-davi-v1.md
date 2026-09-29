<!-- ARQUIVO DE REGISTRO — NÃO EDITAR O CORPO. Ver docs/insumos/README.md -->

# Insumo — Metodologia, 1º rascunho

| | |
|---|---|
| **Quem entregou** | **Davi** — caneta da Metodologia pelo cronograma |
| **Como foi produzido** | **Rascunho assistido por Claude Opus 5**, a partir das fontes do próprio repositório. Declarado pelo autor no cabeçalho do arquivo entregue |
| **Entregue em** | 28/09/2026 |
| **Arquivo recebido** | `03-metodologia.md` |
| **Para onde foi** | [`artigo/03-metodologia.md`](../../artigo/03-metodologia.md) |

> **O corpo abaixo está como foi entregue.** Nada foi cortado, acrescentado ou
> reescrito. O que mudou na passagem para o artigo está listado logo abaixo.

## O que mudou ao levar para o artigo

| O que | Por quê |
|---|---|
| **Os quatro comentários `<!-- LACUNA -->` viraram blocos visíveis** | **O GitBook apaga comentário HTML ao salvar.** Em 06/09 ele exportou os seis capítulos com todos os marcadores apagados. Deixá-los como comentário dentro de `artigo/` seria perdê-los sem ninguém perceber — é a regra do [`artigo/README.md`](../../artigo/README.md) |
| **A chamada no texto foi convertida para a NBR 10520** — `(WOHLIN et al., 2012)` no lugar de `(Wohlin et al., 2012)` | Mesma conversão feita no referencial teórico. A Introdução entregue em 24/09 usa essa forma, e o [formato do artigo](../formato-do-artigo.md) manda mantê-la até o template do COBEM 2026 chegar. **É conversão de forma, não de conteúdo** |
| **As sete referências não foram para `artigo/referencias.md`** | O próprio insumo declara que **nenhuma foi conferida na fonte**. Aquela página só aceita entrada depois de alguém abrir a obra. As sete estão em [citações pendentes](../citacoes-pendentes.md) |
| **Os três blocos finais não vão para o artigo** | Lacunas, citações a conferir e procedência são registro de trabalho. Ficam aqui, e as partes acionáveis foram distribuídas para os arquivos que as cobram |
| **Dois links relativos foram reapontados** | `../docs/cronograma.md` e `referencias.md` valiam a partir de `artigo/` e quebravam aqui. Link quebrado em página publicada é defeito, e o `validar.py` reprova. Só o caminho mudou — o destino é o mesmo |

## Três observações sobre o insumo, sem alterá-lo

- **A divergência nº 1 está desatualizada.** O insumo diz que a **D-11** e o
  `docs/cronograma.md` apontam CREEM 2026. Não apontam mais: a D-11 foi fechada
  em **23/09** como **COBEM 2026**, e o CREEM está registrado ali como engano de
  arquivo. A divergência que o insumo levanta já estava resolvida quando ele foi
  escrito
- **A divergência nº 2 procede**, e virou pendência: o [plano](../plano.md) §1.5
  lista **OE1 a OE6** e a [Introdução](../../artigo/01-introducao.md) lista
  **a) a h)**. É granularidade, não contradição — mas quem lê o artigo é a banca
- **O `docs/cobem.md` citado no insumo não existe** com esse nome. É a segunda
  vez que esse arquivo é citado por um insumo; o equivalente é
  [`docs/formato-do-artigo.md`](../formato-do-artigo.md)

---

# 3. Metodologia

> **3ª Versão** na numeração do professor · S5 do
> [cronograma](../cronograma.md) · caneta: Davi.
>
> **Este bloco de citação e os três blocos ao final não fazem parte do artigo —
> apague-os antes de diagramar.** O que está entre eles é texto de seção.
>
> **Rascunho assistido.** A redação desta seção foi rascunhada por Claude Opus 5
> a partir das fontes do próprio repositório, listadas no bloco *Procedência*.
> Nenhuma citação foi conferida na fonte, e nenhum número foi estimado. Ler
> inteiro e reescrever o que não for seu antes de assinar.

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
| **C0** | Regras fixas sobre o evento isolado, sem histórico do funcionário | Grupo de controle |
| **C1** | D1 — risco do evento individual | Ganho de atributos mais ricos sobre a mesma lógica pontual |
| **C2** | D1 + D2 — desvio em relação ao padrão do próprio funcionário | Ganho de contexto individual |
| **C3** | D1 + D2 + D3 — exposição acumulada e higiene de segurança | Contribuição original do trabalho |

A configuração C0 cumpre a função de grupo de controle e é **puramente
estática**: nenhuma de suas regras consulta o histórico do funcionário. A
restrição é deliberada e corrige uma formulação anterior, em que duas das quatro
regras da linha de base — a noção de endereço de origem habitual e a janela de
contagem de falhas de autenticação — utilizavam histórico individual. Mantê-las
contaminaria o grupo de controle com a própria informação cuja contribuição o
experimento pretende medir.

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

<!-- LACUNA 1 — a relação nominal dos cenários de cada família depende da D-06 e
da D-16, de responsabilidade da Yasmin, com prazo em 01/10. Inserir aqui uma
tabela com, no mínimo, um cenário nomeado por família e ao menos um cenário de
escalada legítima. Não escrever antes de existir. -->

<!-- LACUNA 2 — desenho cego. Se a especificação dos cenários tiver de fato
ocorrido sem acesso às fórmulas de pontuação, acrescentar uma frase declarando
isso: é a resposta mais forte à objeção de circularidade tratada na Seção 3.8.
Se não tiver ocorrido, não escrever. -->

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

<!-- LACUNA 3 — o critério de sucesso declarado a priori (D-15). Falta a frase
que fixa, EM NÚMEROS, qual redução de falsos positivos e qual revocação
longitudinal contam como resposta afirmativa à pergunta de pesquisa. A frase é
deliberadamente deixada em branco: seu valor metodológico está em ser escolhida
pelos autores antes de existir resultado, e o número precisa ter origem
declarável — literatura, linha de base medida da C0, ou argumento operacional de
quantos falsos positivos um analista absorve por turno. Escrever antes da S6. -->

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
convenção. No teste de Wilcoxon pareado exato, o menor valor de *p* bilateral
obtenível com *n* pares é $2/2^{n}$, correspondente ao caso em que todas as
diferenças têm o mesmo sinal. Com *n* = 5 esse limite é 0,0625, de modo que
nenhum resultado poderia ser declarado significativo ao nível de 0,05 ainda que
uma configuração superasse a outra em todas as execuções; com *n* = 10 o limite é
de aproximadamente 0,002.

A reprodutibilidade é assegurada pelo registro de execução: cada execução grava
identificador, semente, configuração e pesos utilizados, e cada avaliação
produzida referencia a execução que a originou. Comparar duas configurações
consiste, operacionalmente, em comparar dois identificadores de execução sobre o
mesmo conjunto de eventos. O protótipo é implementado em Python 3.12 sobre
PostgreSQL — banco relacional escolhido pela necessidade de janelas temporais por
funcionário sobre volume da ordem de milhões de registros — e a interface de
inspeção dos resultados é construída em Streamlit.

## 3.8 Ameaças à validade

Esta seção declara as ameaças à validade identificadas e as medidas adotadas,
organizadas segundo as quatro categorias usuais em experimentação em engenharia
de software (Wohlin *et al.*, 2012).

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
(Kaufman *et al.*, 2012). Pela mesma razão, os atributos de estado são lidos na
condição vigente na data do evento, e não em seu estado final. Ainda no mesmo
eixo, o termo de exposição acumulada é calculado sobre a janela que **antecede** o
evento avaliado, excluindo-o: incluí-lo faria o risco do evento corrente ser
contado duas vezes — uma no termo do evento, outra no de exposição —, de modo que
seu peso efetivo seria a soma dos dois coeficientes, e não o que lhe é atribuído;
além disso, como a exposição soma o risco de vários dias, sua escala é uma ordem
de magnitude superior à do evento isolado e o termo dominaria a nota final
inclusive nos cenários pontuais. Por fim, a linha de base é mantida puramente
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

<!-- LACUNA 4 — esta subseção pressupõe a opção A da D-02 (painel como
instrumento), que é a proposta registrada no plano, seção 1.5, mas a decisão está
aberta desde 08/09. Se a escolha for a opção B — segundo experimento, com
avaliação heurística e SUS —, esta subseção é reescrita por inteiro e passa a
contradizer a declaração de ausência de dado de pessoa real da Seção 3.2. Se a
escolha for C, a subseção é removida. Decidir antes de congelar o M2. -->

***

## Lacunas marcadas no texto

| # | Onde | O que falta | Dono | Prazo |
|---|---|---|---|---|
| 1 | 3.4 | Relação nominal dos cenários por família | Yasmin | 01/10 |
| 2 | 3.4 | Confirmar se o desenho cego ocorreu de fato | Davi + Yasmin | 01/10 |
| 3 | 3.6 | **A frase da D-15, com número** | Os três | 01/10 |
| 4 | 3.9 | Fechar a D-02 antes de validar a subseção | Davi + Filipe | 01/10 |

## Citações a conferir na fonte

Nenhuma das entradas abaixo foi verificada. Conferir cada uma, registrar quem
conferiu e quando em [referências](../../artigo/referencias.md) e remover deste bloco. Os anos
marcados com `?` são os que merecem atenção redobrada — podem corresponder a
outra edição.

| Chamada no texto | Obra | Sustenta | Conferida |
|---|---|---|---|
| Wohlin *et al.*, 2012 `?` | *Experimentation in Software Engineering*, Springer | A taxonomia das quatro categorias de validade | [ ] |
| Demšar, 2006 | *Statistical Comparisons of Classifiers over Multiple Data Sets*, JMLR | A escolha do Wilcoxon pareado | [ ] |
| Wilcoxon, 1945 | *Individual Comparisons by Ranking Methods*, Biometrics Bulletin | O teste em si | [ ] |
| Davis e Goadrich, 2006 | *The Relationship Between Precision-Recall and ROC Curves*, ICML | Curva PR sobre ROC em classe desbalanceada | [ ] |
| Saito e Rehmsmeier, 2015 | *The Precision-Recall Plot Is More Informative…*, PLOS ONE | idem | [ ] |
| Kaufman *et al.*, 2012 | *Leakage in Data Mining*, ACM TKDD | Vazamento na constituição do padrão | [ ] |
| Sommer e Paxson, 2010 | *Outside the Closed World*, IEEE S&P | Limite das avaliações sobre dado sintético | [ ] |

Não há citação na Seção 3.1. Se o professor exigir fundamentação para a
classificação do tipo de pesquisa, a via usual é uma obra de metodologia
científica em computação — o mapa de trabalho aponta Wazlawick, também a
conferir.

## Procedência — de onde saiu cada afirmação

Para que a revisão possa conferir sem reabrir tudo, e para separar o que veio do
repositório do que foi formulado na redação.

| Subseção | Fonte no repositório |
|---|---|
| 3.1 | `docs/diretrizes.md` §Natureza · `docs/plano.md` §1.8 |
| 3.2 | `docs/banco-simulado.md` §2 a §9 · D-23, D-25 |
| 3.3 | `docs/plano.md` §2 · D-05, D-25, D-26 · P30 |
| 3.4 | D-06, D-16 · `docs/banco-simulado.md` §6 (`hr_calendar`), §8 |
| 3.5 | D-12, incluindo o exemplo numérico do cenário longitudinal |
| 3.6 | D-03, D-14 |
| 3.7 | D-13, incluindo a derivação do piso de dez sementes |
| 3.8 | D-16, D-17, D-18, D-19 · `docs/plano.md` §1.6 · `banco-simulado.md` §4 |
| 3.9 | `docs/plano.md` §1.5, nota sobre a D-02 |

### Três divergências encontradas nas fontes, não resolvidas aqui

1. **CREEM ou COBEM.** A **D-11** e o `docs/cronograma.md` dizem **CREEM 2026**;
   o mapa de trabalho da S5 diz **COBEM 2026** em todas as menções, e a
   contradição nº 5 do próprio mapa cita um `docs/cobem.md` numa branch. Esta
   seção não nomeia o template, para não propagar o erro — mas a divergência
   precisa ser resolvida antes de diagramar.
2. **Seis objetivos ou oito.** O `docs/plano.md` §1.5 lista **OE1 a OE6**; o
   `artigo/01-introducao.md` lista **a) a h)**. Não é contradição, é granularidade:
   as alíneas f, g e h correspondem ao OE6. Vale alinhar a redação dos dois, já
   que a banca lê o artigo.
3. **MTTD removido.** O esqueleto anterior pedia MTTD entre as métricas. A
   especificação do ambiente declara `ingested_at` como "latência de engenharia,
   **nunca métrica do TCC**". Seguiu-se a especificação: o MTTD **não** aparece
   nesta seção. Se a decisão for mantê-lo como informativo, é preciso reintroduzi-lo
   declarando a limitação de medi-lo em ambiente simulado.

### Duas escolhas de redação, para você confirmar ou trocar

- **Tempo verbal: presente.** "O ambiente representa", "cada configuração é
  executada". Lê corretamente antes e depois da execução, e poupa uma revisão em
  dezembro. Se preferir futuro, a troca é mecânica.
- **Fórmulas em `$$…$$`.** Conferir se o template aceita; se não, viram imagem ou
  texto corrido.
