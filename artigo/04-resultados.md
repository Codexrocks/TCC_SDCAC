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
procedência completa está em [`results/README.md`](../results/README.md) e o
procedimento em
[execução do experimento](../docs/execucao-do-experimento.md).

| | |
|---|---|
| Eventos gerados | 1.905.111, em 124 episódios |
| Janela de treino | 01/01 a 31/03/2026 — os três meses da **D-24** |
| Janela de avaliação | 01/04 a 31/12/2026 — **1.435.546 eventos**, 2.638 maliciosos |
| Configurações executadas | **as quatro** |
| Limiar de alerta | 20, o teto da faixa normal do preset |

> ⚠️ **Duas ressalvas que valem para toda esta seção.** A execução usa **uma
> semente**, e a **D-13** pede tratamento estatístico sobre várias — nada aqui
> distingue ainda ganho sistemático de variação de amostragem. E o **limiar não
> foi calibrado**: no corte 20 nenhuma das quatro configurações é operável, e a
> C3 alerta sobre praticamente todo o registro. As duas constam na Seção 4.6.

***

## 4.1 Execução dos cenários

Dos 124 episódios gerados, **109 caem na janela de avaliação** — os outros 15
ficam no baseline de três meses, onde o gerador não injeta cenário de ataque. Um
episódio conta como detectado quando **pelo menos um** de seus eventos
ultrapassa o limiar.

| Família | Episódios | C0 | C1 | C2 | C3 |
|---|---|---|---|---|---|
| **P** — pontual | 24 | 20 (83,3%) | 24 (100%) | 24 (100%) | 24 (100%) |
| **B** — comportamental | 16 | 5 (31,2%) | 7 (43,8%) | 15 (93,8%) | 16 (100%) |
| **L** — longitudinal | 12 | 3 (25,0%) | 9 (75,0%) | 12 (100%) | 12 (100%) |
| **N** — normal, benigno por construção | 57 | 42 (73,7%) | 53 (93,0%) | 53 (93,0%) | **57 (100%)** |

Três leituras que a tabela impõe:

**A família N não é acerto.** Ela reúne atividade legítima que *parece*
estranha — plantão noturno, viagem, janela de manutenção de infraestrutura —, e
alertar sobre ela é falso positivo. A linha subiu junto com a cobertura: **o
modelo passou a alertar mais no que é normal, e não só no que é ataque.**

**As regras fixas encontram o que é pontual, e pouco mais.** A C0 detecta 83,3%
da família P e apenas um quarto da longitudinal — o que é esperado por
construção, já que ela avalia eventos isolados. É a lacuna que a pergunta de
pesquisa nomeia.

**A coluna da C3 não é resultado de detecção.** Neste limiar ela alerta sobre
99,8% do registro, e detectar todos os 109 episódios é consequência aritmética
disso, não evidência de discriminação. A C3 só se compara às outras no ponto de
revocação fixa da Seção 4.3.

## 4.2 Matriz de confusão

Por evento, no limiar de operação 20, sobre os 1.435.546 eventos da janela:

| Config | VP | FP | VN | FN | Revocação | FPR | Precisão |
|---|---|---|---|---|---|---|---|
| **C0** | 769 | 287.310 | 1.145.598 | 1.869 | 29,15% | 20,05% | 0,27% |
| **C1** | 955 | 279.100 | 1.153.808 | 1.683 | 36,20% | 19,48% | 0,34% |
| **C2** | 1.593 | 315.140 | 1.117.768 | 1.045 | 60,39% | 21,99% | 0,50% |
| **C3** | 2.637 | 1.430.522 | 2.386 | 1 | 99,96% | 99,83% | 0,18% |

**Nenhuma das quatro configurações é operável neste limiar**, e é o primeiro
resultado a declarar: 279 a 315 mil alertas em nove meses nas três primeiras,
com precisão abaixo de 1%, significa um analista descartando mil alertas por
dia. A linha da **C3 é o caso extremo**: ela deixa escapar um único evento
malicioso e, para isso, alerta sobre 1,43 milhão — a parcela de exposição
acumulada cresce ao longo da janela e empurra praticamente todas as notas acima
do corte.

O limiar 20 é o teto da faixa normal do preset, herdado dos testes de unidade, e
**não foi calibrado sobre dado em escala**. Isso não invalida a comparação —
invalida comparar as quatro *neste ponto*. A grandeza que a **D-03** define
justamente para contornar o problema é a da seção seguinte.

## 4.3 Métricas de desempenho

### 4.3.1 Ruído: FPR com a revocação fixada

A primeira grandeza da pergunta de pesquisa. Cada célula é a taxa de falsos
positivos no limiar mais alto que ainda alcança aquela revocação:

| Revocação | C0 | C1 | C2 | C3 |
|---|---|---|---|---|
| **0,10** | 1,60% | **<0,01%** | 0,02% | 0,02% |
| **0,20** | 20,05% | 11,13% | **0,68%** | 0,83% |
| **0,30** | 100% | 19,48% | **1,83%** | 2,32% |
| **0,40** | 100% | 72,52% | 6,54% | **4,58%** |
| **0,50** | 100% | 72,52% | 8,59% | **7,34%** |
| **0,60** | 100% | 72,52% | 21,99% | **14,70%** |
| **0,70** | 100% | 72,52% | 37,98% | **30,64%** |
| **0,80** | 100% | 72,52% | 75,52% | **61,47%** |
| **0,90** | 100% | 100% | 79,67% | **75,18%** |

**FPR de 100% não é lacuna: é resultado.** Toda revocação é alcançável baixando
o limiar até alertar o registro inteiro, e é o que a linha da C0 diz a partir de
0,30 — a base de regras fixas só identifica três em cada dez eventos maliciosos
**abrindo alerta em cada evento do registro**. No mesmo ponto a C2 usa 27.077
alertas: **53 vezes menos**.

**O acréscimo de cada dimensão não se comporta do mesmo modo em toda a faixa**, e
é o achado mais fino desta execução:

* **a C1 é a melhor configuração a 0,10 de revocação** — 277 alertas, contra 573
  da C2 e 582 da C3. Com limiar muito alto, somar dimensões eleva eventos
  benignos que a D1 sozinha deixaria abaixo do corte;
* **a C2 domina entre 0,20 e 0,30**, com 0,68% e 1,83%;
* **a C3 passa a dominar de 0,40 em diante**, e a vantagem cresce com a
  revocação exigida: a 0,60 são 14,70% contra 21,99%, e a 0,80 são 61,47%
  contra 75,52%.

A leitura é coerente com o que cada dimensão mede. A exposição acumulada é um
termo que cresce devagar e atinge muita gente: ela é ruim para separar os poucos
eventos de maior risco, e boa para alcançar os casos que nenhum evento isolado
denuncia. **Operar com revocação alta é exatamente o regime em que ela
compensa.**

### 4.3.2 Cobertura: revocação nos cenários longitudinais

A segunda grandeza. Medida na família **L** — aqueles em que o risco cresce ao
longo de dias sem que um evento isolado dispare alerta:

| Unidade de análise | C0 | C1 | C2 | C3 |
|---|---|---|---|---|
| **Por episódio**, no limiar de operação | 25,0% (3/12) | 75,0% (9/12) | **100% (12/12)** | 100% (12/12) |

> **As duas unidades, porque a D-12 está aberta.** A escolha entre evento,
> usuário-dia e episódio é a **D-12**, e ela muda o número: um cenário
> longitudinal pode render revocação baixa medido por evento e completa medido
> por episódio, porque basta um evento da sequência cruzar o limiar. A tabela
> acima é por episódio. **Fechar a D-12 é pré-requisito para esta seção ir à
> banca**, e a decisão não pode ser tomada depois de ver qual unidade favorece a
> conclusão.

### 4.3.3 A resposta às duas grandezas

**A direção declarada na pergunta se confirma nas duas.** À mesma revocação a
FPR cai de 20,05% para 0,68% em 0,20, e de 100% para 1,83% em 0,30; a cobertura
longitudinal vai de 25,0% a 100%.

**E vem com um contrapeso que a Seção 4.5 precisa enfrentar:** o alarme sobre a
família N — atividade legítima — subiu de 73,7% para 93,0% na C2 e para 100% na
C3. O ganho não é de graça, e a pergunta admitia exatamente esta resposta: *uma
sobe e a outra não — o modelo troca ruído por cobertura.* Aqui ele ganha nas
duas grandezas medidas **e perde na terceira, que a pergunta não mede.**

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

**A taxa de falsos positivos é operável?** No limiar herdado, não: 279 a 315 mil
alertas em nove meses nas três primeiras configurações, e 1,43 milhão na quarta.
A pergunta útil é outra — **a que revocação o sistema cabe num turno?** A 0,20
de revocação a C2 produz 10.272 alertas em nove meses, ou cerca de 38 por dia
útil; a C0, 288.079, ou mais de mil por dia. É aqui que a **D-15** entra, e é por
isso que ela tinha de ser declarada **antes** de se olhar esta tabela.

**Onde o sistema errou.** O único cenário que escapa à C2 é um episódio da
família B; a C0 perde 11 dos 16. E as quatro configurações alarmam em mais de
70% dos episódios legítimos da família N — o erro dominante não é deixar ataque
passar, é **chamar de anômalo o que é só incomum**.

**O que os pesos das regras não capturam.** A D1 sozinha ganha pouco sobre a C0
na família B e muito na L; o salto na B só vem com a D2, que é a dimensão do
desvio em relação ao próprio histórico da pessoa. É o argumento central a favor
da linha de base por funcionário. A terceira dimensão, por sua vez, **não
melhora a separação no topo da fila e melhora a cobertura no regime de revocação
alta** — o que sugere que ela pertence a um segundo estágio de triagem, e não ao
mesmo corte das demais.

**Comparação com o Isolation Forest**, se a S10 acontecer — opcional pela
**D-10**.

## 4.6 Limitações

> **A escrever.** Seção obrigatória, e a que mais protege o trabalho. As quatro
> primeiras já estão medidas e não dependem de mais nada:

**Uma semente.** A **D-13** pede tratamento estatístico sobre múltiplas
execuções, e a Seção 3.7 descreve o desenho. Com uma semente, nenhuma diferença
desta seção está distinguida de variação de amostragem — nem a favor nem
contra. É a limitação mais séria dos resultados atuais.

**O limiar não foi calibrado.** Os números da Seção 4.2 são de um corte herdado
dos testes de unidade, não escolhido sobre dado em escala. A comparação válida
hoje é a de revocação fixa, e a tabela da Seção 4.2 serve para mostrar o
problema, não para comparar configurações.

**A parcela de postura não foi avaliada em 5,5% dos eventos.** O gerador escreve
estado diário de equipamento apenas para notebooks, e **79.456 eventos** — de
celular e de origem externa — foram pontuados pela C3 sem a parcela de postura,
com a ausência registrada em cada nota. A decisão de pontuar sem ela, em vez de
interromper a execução, está registrada no projeto, e o efeito sobre a C3 é de
subestimação dessa parcela nos eventos afetados. Como eles concentram parte dos
cenários de origem externa, o resultado da C3 é **conservador** nesse recorte.

**A exposição acumulada é subestimada nos empates de instante.** O desenho exclui
o evento corrente do termo de exposição, e a implementação exclui também os
eventos de instante idêntico, por não haver como distingui-los na resolução de
segundo: **962 ocorrências** na execução reportada. O efeito é no mesmo sentido
conservador.

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
* [x] **As quatro configurações**, desde 11/11/2026
* [x] Resultado ruim relatado como resultado, não escondido — a família N, o
  limiar não calibrado e a C3 inoperável no corte 20 estão nas Seções 4.1, 4.2 e
  4.6
* [ ] **Múltiplas sementes**, pela D-13 — é a limitação mais séria de hoje
* [ ] **O limiar calibrado**, sem o qual a Seção 4.2 não compara nada
* [ ] **A D-12 fechada** antes de a unidade de análise ir à banca
* [ ] **A D-15 declarada**, com a data em que foi declarada
* [ ] Limitações escritas antes de a banca perguntar
