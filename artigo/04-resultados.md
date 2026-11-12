# 4. Resultados e Discussão

> **4ª Versão** na numeração do professor · S12 e S13 do
> [cronograma](../docs/cronograma.md) · Filipe e Davi nos números, discussão com
> todos.
>
> **Não escreva nada aqui antes de rodar os testes.** Número de resultado sai de
> execução registrada em `results/`, nunca de estimativa — de ninguém, e muito
> menos de uma IA.

**Primeira execução sobre dado gerado: 11/11/2026.** Todos os números desta
seção saem de `results/semente-1/metricas.json`, gravado pelo avaliador. A
procedência completa da execução está em
[`results/README.md`](../results/README.md) e o procedimento em
[execução do experimento](../docs/execucao-do-experimento.md).

| | |
|---|---|
| Eventos gerados | 1.905.111, em 124 episódios |
| Janela de treino | 01/01 a 31/03/2026 — os três meses da **D-24** |
| Janela de avaliação | 01/04 a 31/12/2026 — **1.435.546 eventos**, 2.638 maliciosos |
| Configurações executadas | **C0, C1 e C2** |
| Limiar de alerta | 20, o teto da faixa normal do preset |

> ⚠️ **Três ressalvas que valem para toda esta seção.** A execução usa **uma
> semente**, e a **D-13** pede tratamento estatístico sobre várias — nada aqui
> distingue ainda ganho sistemático de variação de amostragem. O **limiar não
> foi calibrado**. E a **C3 não entrou**: o gerador escreve estado diário apenas
> do notebook, e a terceira dimensão se recusa a pontuar evento cujo
> equipamento não tenha estado no dia. As três constam na Seção 4.6.

***

## 4.1 Execução dos cenários

Dos 124 episódios gerados, **109 caem na janela de avaliação** — os outros 15
ficam no baseline de três meses, onde o gerador não injeta cenário de ataque.
Um episódio conta como detectado quando **pelo menos um** de seus eventos
ultrapassa o limiar.

| Família | Episódios | C0 | C1 | C2 |
|---|---|---|---|---|
| **P** — pontual | 24 | 20 (83,3%) | 24 (100%) | 24 (100%) |
| **B** — comportamental | 16 | 5 (31,2%) | 7 (43,8%) | 15 (93,8%) |
| **L** — longitudinal | 12 | 3 (25,0%) | 9 (75,0%) | **12 (100%)** |
| **N** — normal, benigno por construção | 57 | 42 (73,7%) | 53 (93,0%) | 53 (93,0%) |

Duas leituras que a tabela impõe:

**A família N não é acerto.** Ela reúne atividade legítima que *parece*
estranha — plantão noturno, viagem, janela de manutenção de TI (`N06`) —, e
alertar sobre ela é falso positivo. A linha subiu de 73,7% para 93,0% junto com
a cobertura: **o modelo passou a gritar mais no que é normal, e não só no que é
ataque.**

**As regras fixas encontram o que é pontual, e pouco mais.** A C0 detecta 83,3%
da família P e apenas um quarto da longitudinal — o que é esperado por
construção, já que ela avalia eventos isolados. É a lacuna que a pergunta de
pesquisa nomeia.

> **A escrever, e depende da D-06.** A tabela por **cenário nomeado** — os
> P01 a P06, B01 a B04 e L01 a L04 com o escore obtido e o esperado — não entra
> antes de a **D-06** fechar o catálogo. Até lá o catálogo é `provisorio-v1`, e
> é o que o gabarito registra em cada episódio.

## 4.2 Matriz de confusão

Por evento, no limiar de operação 20, sobre os 1.435.546 eventos da janela:

| Config | VP | FP | VN | FN | Revocação | FPR | Precisão |
|---|---|---|---|---|---|---|---|
| **C0** | 769 | 287.310 | 1.145.598 | 1.869 | 29,15% | 20,05% | 0,27% |
| **C1** | 955 | 279.100 | 1.153.808 | 1.683 | 36,20% | 19,48% | 0,34% |
| **C2** | 1.593 | 315.140 | 1.117.768 | 1.045 | 60,39% | 21,99% | 0,50% |

**Nenhuma das três configurações é operável neste limiar**, e é o primeiro
resultado a declarar: 280 a 315 mil alertas em nove meses, com precisão abaixo
de 1%, significa um analista descartando mil alertas por dia. O limiar 20 é o
teto da faixa normal do preset, herdado dos testes de unidade, e **não foi
calibrado sobre dado em escala**.

Isso não invalida a comparação — invalida comparar as três *neste ponto*. A
grandeza que a **D-03** define justamente para contornar o problema é a da
seção seguinte: fixar a revocação e medir o ruído ali.

## 4.3 Métricas de desempenho

### Ruído: FPR com a revocação fixada

A primeira grandeza da pergunta de pesquisa. Cada célula é a taxa de falsos
positivos no limiar mais alto que ainda alcança aquela revocação, e entre
parênteses o **número de alertas** que o limiar produz na janela:

| Revocação | C0 | C1 | C2 |
|---|---|---|---|
| **0,10** | 1,60% (23.246) | **0,0001% (277)** | 0,02% (573) |
| **0,20** | 20,05% (288.079) | 11,13% (160.236) | **0,68% (10.272)** |
| **0,30** | 100% (1.435.546) | 19,48% (280.055) | **1,83% (27.077)** |
| **0,40** | 100% | 72,52% | **6,54%** |
| **0,50** | 100% | 72,52% | **8,59%** |
| **0,60** | 100% | 72,52% | **21,99%** |

**FPR de 100% não é lacuna: é resultado.** Toda revocação é alcançável baixando
o limiar até alertar o log inteiro, e é o que a linha da C0 diz a partir de
0,30 — a base de regras fixas só identifica três em cada dez eventos maliciosos
**abrindo alerta em cada evento do log**. No mesmo ponto a C2 usa 27.077
alertas: **53 vezes menos**.

Uma inversão que merece registro, porque contraria a tendência da tabela: a
**0,10 de revocação a C1 é melhor que a C2** — 277 alertas contra 573. Com o
limiar muito alto, a soma de duas dimensões eleva eventos benignos que a D1
sozinha deixaria abaixo do corte. O ganho da C2 aparece a partir de 0,20 e
cresce com a revocação exigida.

### Cobertura: revocação nos cenários longitudinais

A segunda grandeza. Medida na família **L** — aqueles em que o risco cresce ao
longo de dias sem que um evento isolado dispare alerta:

| Unidade de análise | C0 | C1 | C2 |
|---|---|---|---|
| **Por episódio** | 25,0% (3/12) | 75,0% (9/12) | **100% (12/12)** |

> **As duas unidades, porque a D-12 está aberta.** A escolha entre evento,
> usuário-dia e episódio é a **D-12**, e ela muda o número: um cenário
> longitudinal pode render revocação baixa medido por evento e completa medido
> por episódio, porque basta um evento da sequência cruzar o limiar. A tabela
> acima é por episódio. **Fechar a D-12 é pré-requisito para esta seção ir à
> banca**, e a decisão não pode ser tomada depois de ver qual unidade favorece a
> conclusão.

### A resposta às duas grandezas

**A direção declarada na pergunta se confirma nas duas.** À mesma revocação, a
FPR cai de 20,05% para 0,68% (revocação 0,20) e de 100% para 1,83% (revocação
0,30); a cobertura longitudinal vai de 25,0% a 100%.

**E vem com um contrapeso que a Seção 4.5 precisa enfrentar:** o alarme sobre a
família N — atividade legítima — subiu de 73,7% para 93,0%. O ganho não é de
graça, e a pergunta admitia exatamente esta resposta: *uma sobe e a outra não —
o modelo troca ruído por cobertura.* Aqui ele ganha nas duas grandezas medidas
**e perde na terceira, que a pergunta não mede.**

## 4.4 Verificação do painel de análise

> **A escrever.** A **D-02 fechou em 14/10/2026 pela opção A**: o painel é
> instrumento de análise, e não objeto de avaliação — como declara a Seção 3.9.
> **Não há escore SUS, métricas de tarefa nem participantes**, e esta subseção
> não reporta satisfação de usuário.
>
> O que entra aqui é a verificação do critério funcional declarado em
> [usabilidade](../docs/usabilidade.md): decomposição do risco visível por
> dimensão, rótulo textual acompanhando cada uso de cor e contraste mínimo de
> 4,5:1 — a seção 5 daquele documento —, somada à avaliação heurística da seção
> 6.1, que é feita por quem constrói e **não** requer participantes. As seções
> 6.2 e 6.3 de lá, teste com usuários e SUS, ficam fora pela **D-02**.
>
> A verificação é feita pelos autores sobre o painel construído, e o que se
> reporta é se o critério foi cumprido.
>
> As cinco parcelas que o painel precisa exibir separadas são as da Seção 3.3:
> regras fixas, risco do evento individual, desvio do padrão do próprio
> funcionário e as duas parcelas da terceira dimensão — exposição acumulada e
> postura de segurança —, que pelas decisões **D-25** e **D-30** não se agregam
> em um valor único.

## 4.5 Discussão

> **A escrever** — a caneta é do Filipe, pela S13. Os números já estão nas
> seções acima, e o que falta é o argumento. Quatro perguntas que a banca vai
> fazer, e que esta execução já permite atacar:

**A taxa de falsos positivos é operável?** No limiar herdado, não: 280 a 315 mil
alertas em nove meses. A pergunta útil é outra — **a que revocação o sistema
cabe num turno?** A 0,20 de revocação a C2 produz 10.272 alertas em nove meses,
ou cerca de 38 por dia útil; a C0, 288.079, ou mais de mil por dia. É aqui que a
**D-15** entra, e é por isso que ela tem de ser declarada **antes** de se olhar
esta tabela.

**Onde o sistema errou.** O único cenário que escapa à C2 é um episódio da
família B; a C0 perde 11 dos 16. E as três configurações alarmam em mais de 70%
dos episódios legítimos da família N — o erro dominante não é deixar ataque
passar, é **chamar de anômalo o que é só incomum**.

**O que os pesos das regras não capturam.** A D1 sozinha (C1) ganha pouco sobre
a C0 na família B e muito na L; o salto na B só vem com a D2, que é a dimensão
do desvio em relação ao próprio histórico da pessoa. É o argumento central a
favor da linha de base por funcionário.

**Comparação com o Isolation Forest**, se a S10 acontecer — opcional pela
**D-10**.

## 4.6 Limitações

> **A escrever.** Seção obrigatória, e a que mais protege o trabalho. As três
> primeiras já estão medidas e não dependem de mais nada:

**Uma semente.** A **D-13** pede tratamento estatístico sobre múltiplas
execuções, e a Seção 3.7 descreve o desenho. Com uma semente, nenhuma diferença
desta seção está distinguida de variação de amostragem — nem a favor nem
contra. É a limitação mais séria dos resultados atuais.

**O limiar não foi calibrado.** Os números da Seção 4.2 são de um corte herdado
dos testes de unidade, não escolhido sobre dado em escala. A comparação válida
hoje é a de revocação fixa.

**A C3 não foi executada.** A terceira dimensão exige o estado do equipamento
no dia do evento, e o gerador o escreve apenas para notebooks — eventos de
celular e de origem externa ficam sem. A coluna da C3 na tabela de ablação não
existe, e com ela falta a parcela de exposição acumulada, que é metade do que a
pergunta de pesquisa propõe avaliar.

**Ambiente simulado não é produção.** A massa de dados foi gerada por nós, e
acurácia alta sobre dado sintético pode indicar gerador previsível em vez de
modelo bom — a ameaça está declarada na Seção 3.8. O conjunto de regras é
pequeno. O painel não foi avaliado com usuários, por decisão da **D-02**, de
modo que nada se afirma sobre sua usabilidade.

**O tratamento de dados pessoais entra aqui, e a Seção 3.8 já se comprometeu
com isso.** Monitorar comportamento de colaborador é tratamento de dado pessoal
quando aplicado a organização real; este trabalho opera só sobre dado
sintético, e por isso a legislação não o vincula operacionalmente. O que cabe
dizer é o que uma implantação real exigiria à luz da Lei nº 13.709/2018 e dos
controles aplicáveis da ISO/IEC 27001:2022 — base legal, transparência ao
titular, minimização e retenção. É a **D-19**, prevista para a S13, e o par dela
em trabalhos futuros está na Seção 5.4.

Limitação declarada é honestidade científica. Limitação escondida que a banca
descobre é outra coisa.

***

## O que esta seção ainda precisa

* [x] Todos os números vindos de execução registrada em `results/`
* [x] Resultado ruim relatado como resultado, não escondido — a família N e o
  limiar não calibrado estão nas Seções 4.1, 4.2 e 4.6
* [ ] **Múltiplas sementes**, pela D-13 — é a limitação mais séria de hoje
* [ ] **A C3**, que depende do estado de equipamento no gerador
* [ ] **A D-12 fechada** antes de a unidade de análise ir à banca
* [ ] **A D-15 declarada** antes de se discutir se a FPR é operável
* [ ] A tabela por cenário nomeado, que depende da **D-06**
* [ ] Limitações escritas antes de a banca perguntar
