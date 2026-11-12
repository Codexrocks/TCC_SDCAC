# 4. Resultados e Discussão

> **4ª Versão** na numeração do professor · S12 e S13 do
> [cronograma](../docs/cronograma.md) · Filipe e Davi nos números, discussão com
> todos.
>
> **Não escreva nada aqui antes de rodar os testes.** Número de resultado sai de
> execução registrada em `results/`, nunca de estimativa — de ninguém, e muito
> menos de uma IA.

**Dez execuções independentes, em 12/11/2026.** Todos os números desta seção
saem de `results/agregado.json`, gravado pelo avaliador a partir das dez pastas
`results/semente-1` a `semente-10`. A procedência completa está em
[`results/README.md`](../results/README.md) e o procedimento em
[execução do experimento](../docs/execucao-do-experimento.md).

| | |
|---|---|
| Sementes | **dez**, as do gerador 42 a 51 |
| Eventos pontuados por semente | **1.436.275 ± 9.681**, dos quais **2.583 ± 54** maliciosos |
| Episódios na janela de avaliação | **111,9 ± 1,6** |
| Janela de treino | 01/01 a 31/03/2026 — os três meses da **D-24** |
| Janela de avaliação | 01/04 a 31/12/2026 |
| Configurações executadas | **as quatro**, em todas as dez |
| Limiar de alerta | 20, o teto da faixa normal do preset |

**Toda célula de toda tabela desta seção é média ± desvio-padrão amostral sobre
as dez sementes**, em pontos percentuais. O teste de hipótese é o de **Wilcoxon
de postos sinalizados, pareado, bilateral e com p-valor exato**: pareado porque
a mesma semente gera a mesma população para as quatro configurações, de postos
porque a taxa de falsos positivos se acumula perto de zero e tem teto em 1, e
exato porque com dez pares a distribuição nula é contável e a aproximação normal
é justamente pior em amostra pequena. O menor p-valor que dez pares produzem
nesse teste é **0,0020**; `p = 0,0020` está no piso da escala e não significa
"menor que isso".

> ⚠️ **Uma ressalva vale para toda esta seção.** O **limiar não foi
> calibrado**: no corte 20 nenhuma das quatro configurações é operável, e a C3
> alerta sobre praticamente todo o registro. Consta na Seção 4.6.

***

## 4.1 Execução dos cenários

Dos episódios gerados, **111,9 ± 1,6 caem na janela de avaliação** — os demais
ficam no baseline de três meses, onde o gerador não injeta cenário de ataque. Um
episódio conta como detectado quando **pelo menos um** de seus eventos
ultrapassa o limiar.

| Família | Episódios | C0 | C1 | C2 | C3 |
|---|---|---|---|---|---|
| **P** — pontual | 24,0 | 83,3 ± 0,0 | 100,0 ± 0,0 | 100,0 ± 0,0 | 100,0 ± 0,0 |
| **B** — comportamental | 16,0 | 28,7 ± 3,2 | 45,6 ± 3,0 | 98,8 ± 2,6 | 100,0 ± 0,0 |
| **L** — longitudinal | 12,0 | 35,0 ± 10,2 | 89,2 ± 7,9 | 100,0 ± 0,0 | 100,0 ± 0,0 |
| **N** — normal, benigno por construção | 59,9 | 75,8 ± 1,1 | 93,3 ± 0,2 | 96,0 ± 2,6 | **100,0 ± 0,0** |

Três leituras que a tabela impõe:

**A família N não é acerto.** Ela reúne atividade legítima que *parece*
estranha — plantão noturno, viagem, janela de manutenção de infraestrutura —, e
alertar sobre ela é falso positivo. A linha subiu junto com a cobertura, e o
aumento é significativo: **p = 0,0020** entre C2 e C0 e **p = 0,0039** entre C3
e C2. **O modelo passou a alertar mais no que é normal, e não só no que é
ataque.**

**As regras fixas encontram o que é pontual, e pouco mais.** A C0 detecta 83,3%
da família P — exatamente vinte dos vinte e quatro em todas as dez sementes,
porque os quatro que escapam dependem de um limiar que ela nunca cruza — e cerca
de um terço da longitudinal. É a lacuna que a pergunta de pesquisa nomeia, e ela
se reproduz semente a semente.

**A coluna da C3 não é resultado de detecção.** Neste limiar ela alerta sobre
99,84 ± 0,01% do registro, e detectar todos os episódios é consequência
aritmética disso, não evidência de discriminação. A C3 só se compara às outras
no ponto de revocação fixa da Seção 4.3.

## 4.2 Matriz de confusão

Por evento, no limiar de operação 20:

| Config | Revocação | FPR | Precisão | Alertas por semente | Por dia útil |
|---|---|---|---|---|---|
| **C0** | 32,27 ± 2,66 | 18,44 ± 1,49 | 0,32 ± 0,04 | 265.168 ± 21.576 | 1.403 ± 114 |
| **C1** | 44,00 ± 3,97 | 17,97 ± 1,52 | 0,44 ± 0,05 | 258.757 ± 21.933 | 1.369 ± 116 |
| **C2** | 65,40 ± 2,47 | 20,75 ± 1,36 | 0,57 ± 0,04 | 299.182 ± 19.582 | 1.583 ± 104 |
| **C3** | 99,99 ± 0,03 | 99,84 ± 0,01 | 0,18 ± 0,00 | 1.434.003 ± 9.703 | 7.587 ± 51 |

**Nenhuma das quatro configurações é operável neste limiar**, e é o primeiro
resultado a declarar: mais de mil e trezentos alertas por dia útil nas três
primeiras, com precisão abaixo de 1%, é um analista descartando alerta em tempo
integral. A linha da **C3 é o caso extremo**: ela deixa escapar menos de um
evento malicioso por semente e, para isso, alerta sobre 1,43 milhão — a parcela
de exposição acumulada cresce ao longo da janela e empurra praticamente todas as
notas acima do corte.

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
| **0,10** | 1,15 ± 0,71 | **0,01 ± 0,02** | 0,04 ± 0,02 | 0,05 ± 0,03 |
| **0,20** | 18,44 ± 1,49 | 6,03 ± 2,75 | **0,40 ± 0,19** | 0,54 ± 0,29 |
| **0,30** | 34,55 ± 34,52 | 14,05 ± 4,21 | **1,33 ± 0,55** | 1,70 ± 0,94 |
| **0,40** | 100,00 ± 0,00 | 23,27 ± 17,36 | **3,18 ± 1,60** | 3,47 ± 1,36 |
| **0,50** | 100,00 ± 0,00 | 58,75 ± 21,51 | **6,85 ± 1,01** | 7,18 ± 2,12 |
| **0,60** | 100,00 ± 0,00 | 72,09 ± 0,47 | **11,93 ± 4,13** | 14,04 ± 4,48 |
| **0,70** | 100,00 ± 0,00 | 72,09 ± 0,47 | **26,75 ± 4,24** | 28,33 ± 8,84 |
| **0,80** | 100,00 ± 0,00 | 72,09 ± 0,47 | **47,42 ± 14,82** | 52,87 ± 11,11 |
| **0,90** | 100,00 ± 0,00 | 100,00 ± 0,00 | 76,00 ± 1,41 | **73,69 ± 6,75** |

**FPR de 100% não é lacuna: é resultado.** Toda revocação é alcançável baixando
o limiar até alertar o registro inteiro, e é o que as linhas da C0 dizem a
partir de 0,40: **em dez de dez sementes**, a base de regras fixas só identifica
quatro em cada dez eventos maliciosos abrindo alerta em cada evento do registro.
A 0,20 de revocação ela usa 265.168 ± 21.576 alertas contra 6.308 ± 2.685 da
C2 — **49 ± 19 vezes mais**, com o menor fator observado em 25 e o maior em 80.

**O desvio-padrão de 34,52 em 0,30 é informação, não imprecisão de medida.** Ele
é quase do tamanho da média porque a linha mistura dois comportamentos: em
**oito das dez sementes** a C0 alcança 0,30 com FPR em torno de 18%, e em
**duas** só alcança alertando tudo. A fragilidade da base de regras fixas não é
só de nível médio — é de **previsibilidade**: em que população aquele nível de
cobertura vai ser alcançável não se sabe de antemão.

O teste pareado nos nove níveis:

| Comparação | Resultado |
|---|---|
| **C2 contra C0** | FPR menor em **todos os nove** níveis, com **p = 0,0020** em cada um |
| **C1 contra C0** | FPR menor em oito dos nove, com p = 0,0020; idênticas em 0,90 |
| **C2 contra C1** | FPR menor em oito dos nove, p ≤ 0,0098; **maior em 0,10**, com p = 0,0039 |
| **C3 contra C2** | nula **não rejeitada** em seis dos nove; nos três restantes a FPR da C3 é **maior** (p = 0,0020 em 0,10 e p = 0,0488 em 0,20 e 0,60) |

Três achados que as dez sementes sustentam e uma só não sustentava:

* **a C1 é a melhor configuração a 0,10 de revocação**, e agora com
  significância: com limiar muito alto, somar dimensões eleva eventos benignos
  que a D1 sozinha deixaria abaixo do corte;
* **a C2 domina de 0,20 a 0,80**, e a vantagem sobre a C0 é de uma a duas ordens
  de grandeza;
* **a quarta dimensão não reduz o ruído.** A vantagem que a execução de semente
  única atribuía à C3 acima de 0,40 **não sobrevive ao teste pareado**: nos seis
  níveis em que a média favorece a C3, nenhuma diferença é significativa; nos
  três em que o teste rejeita a nula, é a C3 que está pior. O ganho da C3 está
  na cobertura por episódio da Seção 4.1 — ao preço de alarmar em 100% da
  família de controle negativo.

A leitura é coerente com o que cada dimensão mede. A exposição acumulada é um
termo que cresce devagar e atinge muita gente: ela alcança casos que nenhum
evento isolado denuncia e **não** separa os poucos eventos de maior risco. Dez
sementes mostram que o primeiro efeito aparece na contagem de episódios e o
segundo, na FPR — e que a troca, no desenho atual, não compensa.

### 4.3.2 Cobertura: revocação nos cenários longitudinais

A segunda grandeza. Medida na família **L** — aqueles em que o risco cresce ao
longo de dias sem que um evento isolado dispare alerta:

| Unidade de análise | C0 | C1 | C2 | C3 |
|---|---|---|---|---|
| **Por episódio**, no limiar de operação | 35,0 ± 10,2 | 89,2 ± 7,9 | **100,0 ± 0,0** | 100,0 ± 0,0 |

A C2 detecta **os doze episódios longitudinais em todas as dez sementes** —
desvio-padrão zero. Contra a C0 o ganho é significativo (p = 0,0020) e contra a
C1 também (p = 0,0078 sobre os oito pares que não empataram em 100%).

> **As duas unidades, porque a D-12 está aberta.** A escolha entre evento,
> usuário-dia e episódio é a **D-12**, e ela muda o número: um cenário
> longitudinal pode render revocação baixa medido por evento e completa medido
> por episódio, porque basta um evento da sequência cruzar o limiar. A tabela
> acima é por episódio. **Fechar a D-12 é pré-requisito para esta seção ir à
> banca**, e a decisão não pode ser tomada depois de ver qual unidade favorece a
> conclusão.

### 4.3.3 A resposta às duas grandezas

**A direção declarada na pergunta se confirma nas duas, e agora com
significância estatística.** À mesma revocação a FPR cai de 18,44% para 0,40% em
0,20 e de 34,55% para 1,33% em 0,30, com p = 0,0020 em todos os nove níveis
testados; a cobertura longitudinal vai de 35,0% a 100,0%, com p = 0,0020.

**E vem com um contrapeso que a Seção 4.5 precisa enfrentar:** o alarme sobre a
família N — atividade legítima — subiu de 75,8% para 96,0% na C2 e para 100,0%
na C3, e o aumento é significativo nas duas comparações. O ganho não é de graça,
e a pergunta admitia exatamente esta resposta: *uma sobe e a outra não — o
modelo troca ruído por cobertura.* Aqui ele ganha nas duas grandezas medidas
**e perde na terceira, que a pergunta não mede.**

**O que as dez sementes acrescentam, e que uma não dava:** a diferença entre C2
e C0 não é variação de amostragem — o teste pareado a rejeita no menor p-valor
que o desenho permite. E a diferença entre C3 e C2, que a semente única
sugeria, **não se sustenta**. A estatística serviu nas duas direções, e é por
isso que ela entra antes da conclusão e não depois.

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

> **Rascunho de IA, redigido em 12/11/2026 a partir dos números já registrados.**
> A caneta desta subseção é do **Filipe**, pela S13, e **ele ainda não a leu**.
> Nenhuma chamada bibliográfica aqui é nova: todas as sete são da lista já
> conferida na fonte, e nenhuma afirmação quantitativa vem de fora de
> `results/agregado.json`.

A comparação respondeu às duas grandezas da pergunta de pesquisa, e produziu
três resultados que a pergunta não previa. Esta subseção trata deles, porque são
eles que decidem se o modelo serve.

**A taxa de falsos positivos não é operável, e o motivo é aritmético antes de
ser técnico.** No limiar herdado, as três primeiras configurações produzem mais
de mil e trezentos alertas por dia útil e precisão abaixo de 1%. A tentação é ler
isso como defeito de calibração, mas o número não melhora muito com calibração:
há 2.583 ± 54 eventos maliciosos em 1.436.275 ± 9.681, isto é, **menos de dois em
cada mil**. Com uma base-taxa dessa ordem, mesmo a FPR de 0,40% que a C2 alcança
a 0,20 de revocação deixa a precisão na casa de poucas unidades percentuais. É
exatamente o argumento de Axelsson (2000): em detecção de intrusão o fator
limitante é a taxa de falsos positivos, e não a de detecção, porque a raridade do
evento de interesse amplifica o erro. **O desenho de revocação fixa da Seção
4.3.1 existe por causa disso** — ele compara configurações no único eixo em que a
base-taxa não contamina a comparação.

O custo recai sobre o analista, e a fadiga de alerta é causa documentada de
abandono do posto (Sundaramurthy et al., 2015; Vielberth et al., 2020). Daí a
pergunta útil não ser "a FPR é baixa?", mas **a que revocação o sistema cabe num
turno**: a 0,20 a C2 produz **33 ± 14 alertas por dia útil** contra **1.403 ±
114** da linha de base — a diferença entre uma fila que se lê e uma que se
ignora.

**O erro dominante não é deixar ataque passar: é chamar de anômalo o que é só
incomum.** A C2 perde 0,2 ± 0,4 episódio da família comportamental e a C0 perde
11,4 ± 0,5; mas as quatro configurações alarmam em mais de 75% dos episódios da
família N, e a C3 em 100%. A família N não é ruído do experimento — é a
operacionalização da distinção que Chandola, Banerjee e Kumar (2009) põem no
centro do problema: **anômalo não é sinônimo de malicioso**, e um modelo que mede
desvio mede desvio, não intenção. Plantão noturno, viagem e janela de manutenção
são desvio legítimo, e separá-los exige informação que o registro de eventos não
carrega. Que o alarme sobre eles **cresça** junto com a cobertura é o achado mais
incômodo desta seção, e o primeiro que uma implantação real enfrentaria.

**O ganho vem da segunda dimensão, não da terceira.** A D1 sozinha acrescenta
pouco sobre a linha de base na família comportamental — 45,6% contra 28,7% — e
muito na longitudinal — 89,2% contra 35,0%. O salto na família comportamental só
aparece com a D2, que é o desvio em relação ao histórico da própria pessoa:
98,8%, com p = 0,0020. É a validação empírica da ideia original de Denning
(1987), de que o perfil de referência é por sujeito e não por população, e é o
que a literatura de análise de comportamento de usuário e entidade retomou
(Shashanka, Shen e Wan, 2016). Cenários desenhados para que nenhum evento
isolado seja notável — a forma pela qual a ameaça interna costuma se desenvolver
(Cappelli, Moore e Trzeciak, 2012; Homoliak et al., 2019) — são precisamente os
que a linha de base não alcança.

A terceira dimensão, por sua vez, **não reduz o ruído em nenhum regime**, e a
Seção 4.3.1 mostra por quê: a exposição acumulada é um termo que cresce devagar e
atinge muita gente. Ela é boa para alcançar o caso que nenhum evento denuncia e
ruim para ordenar a fila. A leitura que os dados sustentam é que ela **pertence a
um segundo estágio de triagem** — uma lista de pessoas a examinar, com periodicidade
própria — e não ao mesmo corte que decide se um evento gera alerta agora.

**O que esta comparação não resolve.** Os números saem de registro sintético e
por isso **não se comparam a FPR publicada sobre registro real**: base-taxa,
diversidade de normalidade e sofisticação do atacante são todas escolhas nossas.
O que a comparação sustenta é interna — qual configuração é melhor sobre o mesmo
dado —, e é só isso que a pergunta afirma. O detector não supervisionado previsto
como opcional pela **D-10** responderia a uma pergunta diferente e igualmente
limitada, e não substituiria a validação contra tráfego de produção.

## 4.6 Limitações

> **A escrever.** Seção obrigatória, e a que mais protege o trabalho. As
> primeiras já estão medidas e não dependem de mais nada:

**Dez sementes medem variação de amostragem, não validade externa.** A **D-13**
está atendida, e o que o teste pareado afasta é a hipótese de a diferença ter
vindo do sorteio. O que ele **não** afasta é a de o gerador ser previsível:
todas as dez saem do mesmo gerador, com o mesmo catálogo de cenários e as mesmas
regras de normalidade. Essa ameaça está declarada na Seção 3.8 e **não se
resolve com mais sementes**.

**O limiar não foi calibrado.** Os números da Seção 4.2 são de um corte herdado
dos testes de unidade, não escolhido sobre dado em escala. A comparação válida
hoje é a de revocação fixa, e a tabela da Seção 4.2 serve para mostrar o
problema, não para comparar configurações.

**A parcela de postura não foi avaliada em parte dos eventos.** O gerador
escreve estado diário de equipamento apenas para notebooks, e os eventos de
celular e de origem externa — **79.456, ou 5,5% da janela, na semente 42** —
foram pontuados pela C3 sem a parcela de postura, com a ausência registrada em
cada nota. A decisão de pontuar sem ela, em vez de interromper a execução, está
registrada no projeto, e o efeito sobre a C3 é de subestimação dessa parcela nos
eventos afetados. Como eles concentram parte dos cenários de origem externa, o
resultado da C3 é **conservador** nesse recorte.

**A exposição acumulada é subestimada nos empates de instante.** O desenho
exclui o evento corrente do termo de exposição, e a implementação exclui também
os eventos de instante idêntico, por não haver como distingui-los na resolução
de segundo: **962 ocorrências na semente 42**. O efeito é no mesmo sentido
conservador.

**A C3 não é operável no limiar de operação.** Ela alerta sobre 99,84 ± 0,01% do
registro. A única comparação que vale para ela é a de revocação fixa — e nela,
como a Seção 4.3.1 mostra, a quarta dimensão não traz vantagem significativa.

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
* [x] **Dez sementes com tratamento estatístico**, pela D-13 — desde 12/11/2026
* [x] Resultado ruim relatado como resultado, não escondido — a família N, o
  limiar não calibrado, a C3 inoperável no corte 20 e a quarta dimensão sem
  vantagem significativa estão nas Seções 4.1, 4.2, 4.3.1 e 4.6
* [ ] **O limiar calibrado**, sem o qual a Seção 4.2 não compara nada
* [ ] **A D-12 fechada** antes de a unidade de análise ir à banca
* [ ] **A D-15 declarada**, com a data em que foi declarada
* [ ] Limitações escritas antes de a banca perguntar
