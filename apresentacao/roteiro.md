# Roteiro da defesa — apresentação de 15 minutos

Roteiro do **Filipe**, que apresenta. A fala de cada slide é a mesma que está nas notas do apresentador do deck, com o tempo no começo. Os números são os do artigo e de [`results/agregado.md`](../results/agregado.md).

> **Quem escreveu.** O rascunho da fala é de uma IA (Claude Sonnet 5.5), a pedido da Yasmin, a partir do artigo. **Quem apresenta precisa ler em voz alta, ajustar ao próprio jeito e ensaiar com cronômetro.** Onde o roteiro diz o que não dizer, é porque o artigo não sustenta.

## Antes de começar

- Abra o deck no **modo apresentador**: a fala está nas notas.
- Tenha um **cronômetro**. O tempo acumulado de cada slide está na tabela abaixo.
- Leve o deck em **PDF** também, para o caso de o computador da sala falhar.
- Ensaie cronometrado, como o cronograma pede (S16). Cada integrante precisa saber apresentar qualquer seção sob sorteio.
- **14 slides, 14:30 de fala, 30 segundos de folga.** O ritmo foi estimado em cerca de 140 palavras por minuto, e o ritmo real do Filipe pode ser outro.

## Cola: palavras-chave de cada slide

| Slide | Tempo | Acumulado | Palavras-chave |
|---|---|---|---|
| 1. Capa | 0:30 | 0:30 | contexto individual · alarme falso · analista |
| 2. Regra fixa sobre evento isolado não distingue o incomum do indevido | 1:00 | 1:30 | regra fixa · evento isolado · limite igual para todos · escalada gradual · Axelsson · Sundaramurthy |
| 3. Pergunta de pesquisa | 1:00 | 2:30 | ruído · cobertura · mesma revocação · hipótese refutável |
| 4. Três dimensões numa nota decomponível | 1:15 | 3:45 | D1 evento · D2 padrão da pessoa · 3 primeiros meses · mediana e MAD · D3 exposição acumulada · conduta e postura · nota decomponível |
| 5. Estudo de ablação: quatro configurações, um só código | 1:15 | 5:00 | ablação · um código, quatro configurações · C3 é a contribuição original · Wilcoxon pareado · piso p = 0,0020 · critério fixado em 12/11 |
| 6. Uma empresa simulada, com o gabarito guardado à parte | 1:00 | 6:00 | empresa simulada · 10 sementes · 1,44 milhão de eventos · 0,18% maliciosos · 124 episódios, 20 cenários · P B L N · gabarito em banco separado |
| 7. Falsos positivos caem de 18,44% para 0,40% | 1:30 | 7:30 | revocação 0,20 · 18,44% para 0,40% · 0,30: 34,55% para 1,33% · C0 não chega a 0,40 · p = 0,0020 nos nove níveis |
| 8. Nos cenários longitudinais, a cobertura vai de 35,0% a 100,0% | 1:00 | 8:30 | família L: 35,0% para 100,0% · B: 28,7% para 98,8% · P: C0 já vai bem · N é alarme: menos é melhor · 75,8% para 96,0% · isso é o custo |
| 9. Ganha nas duas grandezas e perde numa terceira | 1:30 | 10:00 | 96,0% legítimos alertam · C3 sem ganho · 99,84% no corte 20 · limiar não calibrado · C2: 7 de 10 sementes · 45 alertas por turno |
| 10. A nota decomposta, sem depender só de cor | 1:00 | 11:00 | nota decomposta · “não ligada” não é zero · cor + rótulo + forma · WCAG 1.4.1 · contraste 4,5:1 · 20 achados, nenhum grau 4 · um avaliador, sem usuários |
| 11. Um sistema que vigia log resiste ao log | 1:00 | 12:00 | gabarito isolado · só inserção, sem UPDATE/DELETE · 7 achados, 3 corrigidos com teste · HTML sem escape no painel · treino contamina o padrão · não foi medido |
| 12. O que este trabalho não prova | 1:00 | 13:00 | 10 sementes ≠ validade externa · limiar não calibrado · pesos sem sensibilidade · sintético ≠ produção · um avaliador · LGPD e ISO 27001 |
| 13. O que respondemos, e o que vem depois | 1:15 | 14:15 | sim, nas duas grandezas · 18,44% para 0,40% · 35,0% para 100,0% · ganho vem da D2 · D3: segundo estágio de triagem · custo: mais alarme · IA declarada |
| 14. Obrigado | 0:15 | 14:30 | obrigado · repositório público · quem responde o quê |

## O que foi cortado para caber em 15 minutos

A primeira versão tinha 17 slides e 20:30. Saíram três slides e as falas foram enxugadas. Nenhum resultado saiu.

- **Referencial teórico:** virou uma frase no slide 2 (Axelsson e Sundaramurthy) e outra no slide 4 (Denning).
- **Métricas e estatística:** entraram no slide 5, o método, com o aviso de que o critério foi fixado depois da primeira execução.
- **Uso de IA:** virou uma frase na conclusão e uma linha no slide final. A resposta completa está nas perguntas da banca, mais abaixo.

## Se estourar no ensaio

Corte nesta ordem:

1. **Slide 10, o painel.** Fale só das faixas e da WCAG: 40 segundos em vez de 1:00.
2. **Slide 6, o ambiente.** Diga só “dez sementes, 1,4 milhão de eventos cada, 20 cenários em quatro famílias”: 45 segundos.
3. **Slide 4, o modelo.** Uma frase por dimensão.

**Nunca corte** os slides 7, 8 e 9 (resultados e contrapeso) nem o 12 (limitações). São o que a banca avalia.

## Slide a slide

### Slide 1 · Capa

**Palavras-chave:** contexto individual · alarme falso · analista

[0:30 · acumulado 0:30] Boa tarde. Eu sou o Filipe e apresento o trabalho que fizemos eu, o Davi e a Yasmin, com orientação do professor Euzébio.

Queremos saber se olhar o contexto de cada pessoa, e não só o evento isolado, ajuda a achar comportamento de risco sem afogar o analista em alarme falso.

As quatro etiquetas embaixo são as faixas de risco do nosso painel. Voltam no fim.

PASSE PARA: "Primeiro, o problema."

### Slide 2 · Regra fixa sobre evento isolado não distingue o incomum do indevido

**Palavras-chave:** regra fixa · evento isolado · limite igual para todos · escalada gradual · Axelsson · Sundaramurthy

[1:00 · acumulado 1:30] A forma mais comum de olhar log é uma regra fixa sobre cada evento: fora do horário, volume acima de um limite, origem desconhecida. O limite é igual para todos.

Isso tem dois defeitos. Atividade legítima, mas incomum, vira alerta: quem trabalha à noite, quem mudou de projeto. E há a escalada gradual: quando nenhum evento é notável sozinho, mas o conjunto, ao longo de semanas, é de risco, a regra por evento não enxerga.

A literatura sustenta os dois pontos. Axelsson mostra que a taxa de alarme falso é o que limita um detector. Sundaramurthy mostra o custo humano: o analista que se esgota. E o que é anômalo depende do contexto.

PASSE PARA: "Isso nos levou a uma pergunta."

### Slide 3 · Pergunta de pesquisa

**Palavras-chave:** ruído · cobertura · mesma revocação · hipótese refutável

[1:00 · acumulado 2:30] A pergunta tem duas grandezas.

A primeira é o ruído: os falsos positivos quando fixamos o quanto o sistema detecta. Fixar a revocação torna a comparação justa, porque qualquer sistema tem poucos falsos positivos se detectar pouco.

A segunda é a cobertura: a revocação nos cenários em que a escalada é gradual, onde a regra por evento é cega.

E a hipótese admite refutação: se a terceira dimensão não ganhar da segunda, a resposta é não, e o trabalho reporta assim. A pergunta completa está na seção 1.4 do artigo.

PASSE PARA: "Para responder, o modelo olha o risco em três dimensões."

### Slide 4 · Três dimensões numa nota decomponível

**Palavras-chave:** D1 evento · D2 padrão da pessoa · 3 primeiros meses · mediana e MAD · D3 exposição acumulada · conduta e postura · nota decomponível

[1:15 · acumulado 3:45] A D1 é o risco do evento: horário, origem, dispositivo e sensibilidade do recurso.

A D2 compara a pessoa com ela mesma, pelo padrão dos três primeiros meses. Usamos mediana e MAD, para que um dia de pico não esconda uma divergência real depois. É a ideia de perfil por sujeito, que Denning já propunha em 1987.

A D3 mede a exposição acumulada: o que se repete e se combina no tempo. Tem duas parcelas, conduta e postura de segurança, mostradas separadas, porque somá-las esconderia qual causou o alerta.

O resultado é uma nota decomponível: o analista vê de onde veio cada ponto.

PASSE PARA: "Agora, como desenhamos o experimento."

### Slide 5 · Estudo de ablação: quatro configurações, um só código

**Palavras-chave:** ablação · um código, quatro configurações · C3 é a contribuição original · Wilcoxon pareado · piso p = 0,0020 · critério fixado em 12/11

[1:15 · acumulado 5:00] O método é um estudo de ablação: ligamos as dimensões uma por vez e medimos o ganho de cada uma.

A C0 é o controle, regras fixas sem parâmetro aprendido. A C1 soma a D1, a C2 soma a D2, e a C3 soma a D3, que é a contribuição original. É um único código com quatro conjuntos de parâmetros, então a única diferença entre as linhas é a dimensão acrescentada.

Medimos duas coisas: falsos positivos a revocação fixada, e revocação por episódio nos cenários longitudinais. O teste é Wilcoxon pareado, com p exato. Com dez sementes, o menor p possível é 0,0020, então 0,0020 é o piso da escala, e não "menor que isso".

E o critério de sucesso, 45 alertas falsos por turno, foi fixado em 12 de novembro, depois da primeira execução. O artigo declara isso.

PASSE PARA: "Sobre o que rodamos isso."

### Slide 6 · Uma empresa simulada, com o gabarito guardado à parte

**Palavras-chave:** empresa simulada · 10 sementes · 1,44 milhão de eventos · 0,18% maliciosos · 124 episódios, 20 cenários · P B L N · gabarito em banco separado

[1:00 · acumulado 6:00] Sem log de empresa real, o experimento roda numa empresa simulada. Cada semente gera cerca de 1,4 milhão de eventos, e rodamos dez. Só 0,18% são maliciosos, menos de dois em mil, e é isso que faz o falso positivo pesar.

Injetamos 20 cenários, 124 episódios por semente, em quatro famílias: P pontuais, B de contexto, L longitudinais, de escalada gradual, e N, o controle negativo, comportamento legítimo que serve para medir o falso positivo.

O gabarito fica num banco que a aplicação não consegue abrir. O sistema é comparado com uma resposta que ele não pode consultar.

PASSE PARA: "Vamos aos resultados. Primeiro, o ruído."

### Slide 7 · Falsos positivos caem de 18,44% para 0,40%

**Palavras-chave:** revocação 0,20 · 18,44% para 0,40% · 0,30: 34,55% para 1,33% · C0 não chega a 0,40 · p = 0,0020 nos nove níveis

[1:30 · acumulado 7:30] Este é o primeiro resultado, e responde à primeira metade da pergunta.

Com a revocação fixada em 0,20, a taxa de falsos positivos da C0, as regras fixas, é 18,44%. A C1 cai para 6,03%. A C2, com o padrão individual, cai para 0,40%. A C3 fica em 0,54%. As barras estão em escala, por isso a da C2 quase não aparece.

Em 0,30 de revocação, 34,55% contra 1,33%. E a C0 não alcança revocação de 0,40 sem alertar o registro inteiro. Para ela, esse nível só existe com 100% de falso positivo.

A C2 tem taxa menor que a C0 nos nove níveis, com p igual a 0,0020.

NÃO DIGA que o sistema está pronto para operar. A diferença é entre configurações, e o limiar não foi calibrado. Você volta a isso em dois slides.

PASSE PARA: "E a segunda metade: cobertura."

### Slide 8 · Nos cenários longitudinais, a cobertura vai de 35,0% a 100,0%

**Palavras-chave:** família L: 35,0% para 100,0% · B: 28,7% para 98,8% · P: C0 já vai bem · N é alarme: menos é melhor · 75,8% para 96,0% · isso é o custo

[1:00 · acumulado 8:30] A tabela mostra, por família de cenário, a fração dos episódios que cada configuração detecta.

Olhem a linha L, de escalada gradual, onde a regra por evento é cega. A C0 detecta 35,0%. A C2 detecta 100,0%. Em B, de contexto, de 28,7% para 98,8%. Nas pontuais, P, a C0 já vai bem, 83,3%, porque é o que regra fixa sabe fazer. Na família L, a C2 contra a C0 tem p igual a 0,0020.

Agora a última linha, N. Ela é benigna por construção: a coluna ali é alarme sobre atividade legítima, e menos é melhor. Repararam que sobe: de 75,8% na C0 para 96,0% na C2 e 100% na C3. Isso é o custo.

PASSE PARA: "Então o resultado tem um contrapeso."

### Slide 9 · Ganha nas duas grandezas e perde numa terceira

**Palavras-chave:** 96,0% legítimos alertam · C3 sem ganho · 99,84% no corte 20 · limiar não calibrado · C2: 7 de 10 sementes · 45 alertas por turno

[1:30 · acumulado 10:00] Este é o slide mais importante para a honestidade do trabalho. O modelo ganha nas duas grandezas que a pergunta mede e perde numa terceira, que a pergunta não mede.

Primeiro: 96,0% dos episódios legítimos geram alerta na C2, contra 75,8% na C0. O ganho de cobertura não foi de graça.

Segundo: a exposição acumulada, a C3, não reduziu os falsos positivos de forma significativa em nenhum regime. A hipótese admitia essa resposta, e ela é reportada.

Terceiro: no limiar herdado, o corte 20, a C3 alerta sobre 99,84% do registro. O limiar não foi calibrado, e nesse corte nenhuma das quatro configurações é operável. É o primeiro trabalho futuro.

Para não ficar só no lado ruim: a 0,20 de revocação, a C2 cumpre o critério de 45 alertas falsos por turno em 7 das 10 sementes.

NÃO DIGA "o sistema funciona". DIGA: "reduz ruído e aumenta cobertura nos cenários medidos, e não é livre de custo".

PASSE PARA: "O que o analista vê: o painel."

### Slide 10 · A nota decomposta, sem depender só de cor

**Palavras-chave:** nota decomposta · “não ligada” não é zero · cor + rótulo + forma · WCAG 1.4.1 · contraste 4,5:1 · 20 achados, nenhum grau 4 · um avaliador, sem usuários

[1:00 · acumulado 11:00] O painel usa as cores que vocês viram na capa. A ideia é que o analista não receba um número que precise aceitar sem poder verificar: a nota aparece decomposta por dimensão, e uma parcela que a configuração não liga aparece como "não ligada", e não como zero.

Cada faixa tem cor, rótulo e forma: círculo, triângulo, octógono. Isso cumpre o critério 1.4.1 da WCAG 2.2, de que cor não pode ser o único meio de informação. O contraste é de pelo menos 4,5 para 1, e esse número é calculado no teste, não afirmado. Quarenta casos de teste automáticos conferem isso.

DIGA COM CLAREZA: a avaliação heurística teve 20 achados e nenhum de severidade 4, mas com um avaliador só e sem usuários. O que se afirma é que esses problemas existem, não que a interface seja adequada ao uso.

PASSE PARA: "A Yasmin cuidou da segurança do próprio sistema."

### Slide 11 · Um sistema que vigia log resiste ao log

**Palavras-chave:** gabarito isolado · só inserção, sem UPDATE/DELETE · 7 achados, 3 corrigidos com teste · HTML sem escape no painel · treino contamina o padrão · não foi medido

[1:00 · acumulado 12:00] Um sistema que lê log de uma empresa precisa resistir ao que está no log. Duas travas vêm do banco: a aplicação não tem permissão de conectar no banco do gabarito, e ninguém recebe permissão de alterar ou apagar o log, que só aceita inserção.

A revisão de segurança do código achou sete pontos, e três foram corrigidos com teste. O principal: o painel montava HTML com campos que vêm do log, como o nome de um recurso, sem escapar. Num painel que existe para vigiar log, isso inverte a confiança.

E o limite mais importante, que é do modelo: a D2 compara a pessoa com o padrão dos três primeiros meses. Quem já age mal nesse período contamina o próprio padrão. Nenhum número mede esse caso, porque os cenários só começam depois.

DIGA: é revisão por leitura de código, não teste de intrusão.

PASSE PARA: "Agora, o que o trabalho não prova."

### Slide 12 · O que este trabalho não prova

**Palavras-chave:** 10 sementes ≠ validade externa · limiar não calibrado · pesos sem sensibilidade · sintético ≠ produção · um avaliador · LGPD e ISO 27001

[1:00 · acumulado 13:00] Quero ser direto sobre o que o trabalho não prova, porque isso também é resultado.

Dez sementes medem variação de amostragem, não validade externa. Dado sintético pode ter um gerador previsível, em que acertar é fácil. O limiar de operação não foi calibrado. Os pesos não passaram por análise de sensibilidade: foi prevista e não executada, e está declarada. A avaliação do painel teve um avaliador só.

E há o lado legal: monitorar comportamento de colaborador é tratar dado pessoal. Uma implantação real precisa de base legal, transparência ao titular, minimização e retenção, à luz da Lei 13.709 de 2018 e da ISO/IEC 27001. Aqui os dados são sintéticos.

PASSE PARA: "Com isso, a conclusão."

### Slide 13 · O que respondemos, e o que vem depois

**Palavras-chave:** sim, nas duas grandezas · 18,44% para 0,40% · 35,0% para 100,0% · ganho vem da D2 · D3: segundo estágio de triagem · custo: mais alarme · IA declarada

[1:15 · acumulado 14:15] Voltando à pergunta: nos cenários medidos, sim, nas duas grandezas, com significância estatística. A taxa de falsos positivos cai de 18,44% para 0,40% a 0,20 de revocação, e a cobertura longitudinal vai de 35,0% para 100,0%.

O ganho vem do padrão individual, a D2. A exposição acumulada, a D3, não acrescentou, e a leitura que os dados sustentam é que ela pertence a um segundo estágio de triagem. E o ganho tem custo: sobe o alarme sobre atividade legítima.

Os próximos passos decorrem das limitações: calibrar o limiar e analisar a sensibilidade dos pesos; implantar sobre dado real, com LGPD e ISO/IEC 27001; e validar contra tráfego de produção.

Sobre IA, que a banca sempre pergunta: todo commit e todo Pull Request do repositório declara a IA usada, e referência produzida por IA só entra depois de conferida por uma pessoa.

PASSE PARA: "Obrigado."

### Slide 14 · Obrigado

**Palavras-chave:** obrigado · repositório público · quem responde o quê

[0:15 · acumulado 14:30] Obrigado. O código, os dados e os relatórios de cada sessão estão no repositório público. Ficamos à disposição para as perguntas.

SE A PERGUNTA FOR SOBRE UMA PARTE QUE NÃO É SUA: diga o que você sabe e passe para quem cuidou. Davi: arquitetura, banco, API, gerador. Yasmin: segurança, referencial, cenários, pesos. Filipe: painel, usabilidade, resultados.

## As cinco frases que não podem faltar

1. “A pergunta tem duas grandezas: falsos positivos a uma mesma revocação, e revocação nos cenários longitudinais.”
2. “A taxa de falsos positivos cai de 18,44% para 0,40%, e a cobertura longitudinal vai de 35,0% para 100,0%.”
3. “O ganho tem custo: o alarme sobre atividade legítima sobe de 75,8% para 96,0%.”
4. “A terceira dimensão não ajudou, e a hipótese admitia essa resposta.”
5. “O limiar não foi calibrado, e os resultados valem para o ambiente simulado.”

## O que não dizer

- **“O sistema funciona” ou “está pronto”.** O artigo não sustenta isso. Diga “reduz ruído e aumenta cobertura nos cenários medidos”.
- **“A D3 melhora o resultado”.** Não melhorou. Foi reportado como tal.
- **“p menor que 0,0020”.** Com dez sementes, 0,0020 é o piso do teste, então é “p igual a 0,0020”.
- **“Testamos com usuários”.** Não houve usuários, e a avaliação heurística teve um avaliador.
- **“Um insider que age no começo seria detectado” (ou o contrário).** Isso não foi medido.
- **“Os dados são reais”.** São sintéticos.

## Perguntas prováveis da banca

### Por que dado sintético? Isso não invalida o resultado?

Não temos acesso a log de empresa real, e só em simulação existe um gabarito confiável de quem é malicioso. O trabalho declara que ambiente simulado não é produção e que acerto alto em dado sintético pode indicar gerador previsível. Os números valem para os cenários medidos.

*Quem responde: Davi (gerador) ou Yasmin (cenários).*

### Por que a terceira dimensão não ajudou?

O que se mediu é que a C3 não reduziu os falsos positivos de forma significativa em nenhum regime, e a hipótese admitia essa resposta. A seção 4.5 do artigo diz que a leitura que os dados sustentam é que a D3 pertence a um segundo estágio de triagem, uma lista de pessoas a examinar com periodicidade própria, e não ao mesmo corte que decide se um evento gera alerta agora. Os trabalhos futuros incluem reexaminar a D3.

*Quem responde: Filipe.*

### O sistema é operável?

No limiar herdado, o corte 20, nenhuma das quatro configurações é: a C3 alerta sobre 99,84% do registro. Com a revocação fixada em 0,20, a C2 cumpre o critério de 45 alertas falsos por turno em 7 das 10 sementes. Calibrar o limiar é o primeiro trabalho futuro.

*Quem responde: Filipe.*

### O critério de sucesso foi fixado depois da primeira execução. Isso não é ajustar a meta ao resultado?

É um risco, e por isso está declarado no artigo com a data: 12 de novembro, depois da primeira execução registrada. O número de 45 alertas por turno veio de um argumento operacional, quantos alertas falsos um analista absorve, e não do resultado.

*Quem responde: Davi.*

### Como vocês garantem que o gabarito não vazou para o motor?

O gabarito fica em um banco separado, e a aplicação não tem permissão de conectar nele. Um teste automático reprova se alguém conceder essa permissão. A especificação dos cenários também foi feita sem acesso às fórmulas de pontuação. O artigo trata a objeção de desenho não cego na seção 3.8, ameaças à validade.

*Quem responde: Yasmin.*

### Por que Wilcoxon, e por que só dez sementes?

Wilcoxon porque o teste é pareado: a mesma semente gera a mesma população para as quatro configurações. De postos porque a taxa de falsos positivos se acumula perto de zero. Exato porque, com dez pares, a distribuição é contável. Dez sementes medem variação de amostragem, e não validade externa, e isso está nas limitações.

*Quem responde: Davi ou Filipe.*

### E se o atacante já age durante os três meses de treino?

Aí a D2 aprende o comportamento dele como normal, porque compara a pessoa com o próprio padrão. Isso não foi medido: os cenários só começam depois do período de treino. Está registrado como limitação do modelo, e a literatura trata disso como ataque causativo, em que o adversário atua sobre o treino.

*Quem responde: Yasmin.*

### E a LGPD? Monitorar funcionário pode?

Aqui os dados são sintéticos. Uma implantação real exige base legal, transparência ao titular, minimização e retenção, à luz da Lei 13.709/2018 e dos controles da ISO/IEC 27001. É trabalho futuro declarado no artigo.

*Quem responde: Yasmin.*

### Como vocês usaram IA, e como sabemos o que é de vocês?

Todo commit e todo Pull Request declara a IA usada. Referência que a IA produziu só entra depois de conferida na fonte, por uma pessoa. Cada sessão tem um relatório com os erros da IA e quem os pegou. Na conferência recente das fontes, duas afirmações escritas pela IA não se sustentaram e foram corrigidas.

*Quem responde: Qualquer um dos três.*

### Por que mediana e MAD, e não média e desvio padrão?

Porque um dia de pico dentro da janela de treino inflaria o desvio padrão e mascararia uma divergência real nos meses seguintes. A mediana e o MAD são robustos a isso. Há também um piso de dispersão, para que quem tem comportamento perfeitamente regular não dispare alarme por qualquer variação.

*Quem responde: Yasmin.*

### Quem fez o quê?

Todos sabem explicar o projeto inteiro. Por área: o Davi cuidou da arquitetura, do banco, da API e do gerador; a Yasmin, da segurança, do referencial, dos cenários e dos pesos; o Filipe, do painel, da usabilidade e dos resultados.

*Quem responde: Qualquer um dos três.*

## Quem responde o quê

| Assunto | Primeiro a responder | Se travar |
|---|---|---|
| Arquitetura, banco, API, gerador, ingestão | Davi | Passe para o Davi |
| Segurança, LGPD, ISO/IEC 27001, referencial, cenários, pesos | Yasmin | Passe para a Yasmin |
| Painel, usabilidade, resultados, avaliação heurística | Filipe | Responda com o que o slide mostra |
| Metodologia e estatística | Davi | Filipe, pelo slide 5 |
