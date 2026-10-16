# 4. Resultados e Discussão

> **4ª Versão** na numeração do professor · S12 e S13 do
> [cronograma](../docs/cronograma.md) · Filipe e Davi nos números, discussão com
> todos.
>
> **Não escreva nada aqui antes de rodar os testes.** Número de resultado sai de
> execução registrada em `results/`, nunca de estimativa — de ninguém, e muito
> menos de uma IA.

***

## 4.1 Execução dos cenários

> **A escrever.** Os seis cenários, o score obtido e o esperado, em tabela.

## 4.2 Matriz de confusão

> **A escrever.** Verdadeiro positivo, falso positivo, verdadeiro negativo,
> falso negativo.

## 4.3 Métricas de desempenho

> **A escrever.** Taxa de falsos positivos a revocação fixa e revocação
> longitudinal, as duas da decisão D-03, com os
> números reais.

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

> **A escrever.** Onde os números viram argumento. O que a banca vai cobrar:
>
> * a taxa de falsos positivos é operável, ou geraria fadiga de alerta?
> * onde o sistema errou, e por quê
> * o que os pesos das regras não capturam
> * comparação com o Isolation Forest, se a S10 acontecer

## 4.6 Limitações

> **A escrever.** Seção obrigatória, e a que mais protege o trabalho.
>
> Ambiente simulado não é produção. A massa de dados foi gerada por nós, e
> acurácia alta sobre dado sintético pode indicar gerador previsível em vez de
> modelo bom — a ameaça está declarada na Seção 3.8. O conjunto de regras é
> pequeno. O painel não foi avaliado com usuários, por decisão da **D-02**, de
> modo que nada se afirma sobre sua usabilidade.
>
> **O tratamento de dados pessoais entra aqui, e a Seção 3.8 já se comprometeu
> com isso.** Monitorar comportamento de colaborador é tratamento de dado pessoal
> quando aplicado a organização real; este trabalho opera só sobre dado
> sintético, e por isso a legislação não o vincula operacionalmente. O que cabe
> dizer é o que uma implantação real exigiria à luz da Lei nº 13.709/2018 e dos
> controles aplicáveis da ISO/IEC 27001:2022 — base legal, transparência ao
> titular, minimização e retenção. É a **D-19**, prevista para a S13, e o par
> dela em trabalhos futuros está na Seção 5.4.
>
> Limitação declarada é honestidade científica. Limitação escondida que a banca
> descobre é outra coisa.

***

## O que esta seção ainda precisa

* [ ] Todos os números vindos de execução registrada em `results/`
* [ ] Resultado ruim relatado como resultado, não escondido
* [ ] Limitações escritas antes de a banca perguntar
