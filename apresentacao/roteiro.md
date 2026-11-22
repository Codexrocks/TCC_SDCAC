# Roteiro da defesa — apresentação de 30 minutos

Roteiro do **Filipe**, que apresenta. A fala de cada slide é a mesma que está nas **notas do apresentador** de [`apresentacao-sdcac.pptx`](apresentacao-sdcac.pptx), com as palavras-chave e o tempo no começo. Os números são os do artigo e de [`results/agregado.md`](../results/agregado.md).

> **Quem escreveu.** O rascunho da fala é de uma IA (Claude Sonnet 5.5), a pedido da Yasmin, a partir do artigo. **Quem apresenta precisa ler em voz alta, ajustar ao próprio jeito e ensaiar com cronômetro.** Onde o roteiro diz o que não dizer, é porque o artigo não sustenta.

## Antes de começar

- Abra o `.pptx` no **modo apresentador** do PowerPoint: a fala está nas notas.
- Tenha um **cronômetro**. O tempo acumulado de cada slide está na tabela abaixo.
- Leve o arquivo em **PDF** também (Arquivo, Salvar como, PDF), para o caso de o computador da sala falhar.
- Ensaie cronometrado, como o cronograma pede (S16). Cada integrante precisa saber apresentar qualquer seção sob sorteio.
- **27 slides, 28:10 de fala, 1:50 de folga.** Os tempos são **estimativas**, a cerca de 140 palavras por minuto. O ritmo real do Filipe pode ser outro, e só o ensaio mede.

## Cola: palavras-chave de cada slide

| Slide | Tempo | Acumulado | Palavras-chave |
|---|---|---|---|
| 1. Capa | 0:30 | 0:30 | experimento controlado · protótipo de software · 4 configurações, mesmos dados |
| 2. Estrutura da apresentação | 0:20 | 0:50 | ordem do artigo · 7 blocos · 28 minutos |
| 3. O problema | 1:15 | 2:05 | evento isolado não tem padrão · autorização: ações permitidas · taxa-base, Axelsson · exaustão, Sundaramurthy · SOC sem contexto, Vielberth |
| 4. A falácia da taxa-base | 1:00 | 3:05 | P = TPR·p / (TPR·p + FPR·(1−p)) · p = 0,18% · C0: 1 verdadeiro a cada 513 · C2: 1 a cada 12 · cálculo nosso, não medida |
| 5. Referencial: o domínio | 1:15 | 4:20 | Kent e Souppaya: logs · Grassi e Sandhu: autenticação x autorização · Gonzalez-Granadillo: SIEM · Vielberth: SOC · Sundaramurthy e Alahmadi: custo humano · Cappelli e Homoliak: ameaça interna |
| 6. Referencial: a taxonomia de anomalias | 1:15 | 5:35 | Chandola 2009: pontual, contextual, coletiva · D1 = pontual · D2 = contextual: Denning, Shashanka · D3 = coletiva: Cappelli, Homoliak · lacuna: três leituras separáveis |
| 7. Referencial: o método | 1:15 | 6:50 | Wohlin 2012: experimentação em ES · Wilcoxon 1945 e Demšar 2006 · Kaufman 2012: vazamento · Sommer e Paxson 2010: realismo |
| 8. Pergunta, variáveis e hipótese | 1:00 | 7:50 | aplicada, quantitativa, experimental · VI: configuração C0 a C3 · VD: FPR a revocação fixa, revocação L · hipótese refutável · H0: mesma FPR na mesma semente |
| 9. Arquitetura do sistema | 1:15 | 9:05 | camadas, portas e adaptadores · detection puro: sem rede, relógio, banco · adaptador de arquivos e PostgreSQL · runner e API chamam o mesmo núcleo · regra de dependência testada · 765 testes, ~10 mil linhas |
| 10. Dados e ambiente simulado | 1:15 | 10:20 | 250 funcionários, 1 ano · 8 tipos de evento · estado diário lido na data · 3 bancos: corp, ground_truth, sdcac · aplicação não conecta no gabarito · sem dado real |
| 11. Cenários e gabarito | 1:00 | 11:20 | 20 cenários, 124 episódios · P 24 · B 16 · L 12 · N 72 · N = controle negativo · unidade: evento ou episódio · especificação sem ver as fórmulas |
| 12. C0: a linha de base | 1:00 | 12:20 | regras fixas, sem parâmetro aprendido · fora do horário 30 · origem externa 30 · recurso restrito 35 · força bruta 40: 10 falhas em 2 min |
| 13. D1: o risco do evento | 1:00 | 13:20 | privilégio 40 · dispositivo pessoal e download externo 25 · fora do expediente, download ≥ 50 MiB, removível 20 · sem MFA 15 · sensibilidade: 5 a 35 |
| 14. D2: o desvio do padrão da pessoa | 1:15 | 14:35 | padrão: 3 primeiros meses · mediana e MAD × 1,4826 · piso e teto 6, um lado só · 7 características · mín. 20 dias de atividade · janela disjunta |
| 15. D3: a exposição acumulada | 1:00 | 15:35 | conduta: decaimento 0,85/dia · janela de 14 dias · evento atual fora (D-18) · postura: estado do dia · duas parcelas separadas, 0 a 100 |
| 16. Integração e faixas de risco | 0:45 | 16:20 | um só conjunto de pesos · 5 parcelas guardadas · nulo ≠ zero · entrada que falta é erro · faixas: 20 · 50 · 75 |
| 17. Protocolo experimental | 1:15 | 17:35 | 5 etapas independentes · só a avaliação lê o gabarito · agregação recusa o incomparável · 10 sementes pareadas · semente + SHA-256 + versão do código |
| 18. Métricas e estatística | 1:15 | 18:50 | FPR a revocação fixa · Rec_L por episódio · Wilcoxon pareado exato · p_min = 2/2^n · n=5: 0,0625 · n=10: 0,0020 · critério: 45 alertas falsos por turno |
| 19. Resultado 1: ruído | 1:15 | 20:05 | revocação 0,20 · 18,44% para 0,40% · 0,30: 34,55% para 1,33% · C0 não chega a 0,40 · p = 0,0020 nos nove níveis |
| 20. Resultado 2: cobertura | 1:00 | 21:05 | família L: 35,0% para 100,0% · B: 28,7% para 98,8% · P: C0 já vai bem · N é alarme: menos é melhor · 75,8% para 96,0% · isso é o custo |
| 21. O contrapeso | 1:15 | 22:20 | 96,0% legítimos alertam · C3 sem ganho · 99,84% no corte 20 · limiar não calibrado · C2: 7 de 10 sementes · 45 alertas por turno |
| 22. O painel de análise | 1:00 | 23:20 | nota decomposta · “não ligada” não é zero · cor + rótulo + forma · WCAG 1.4.1 e 1.4.3 · 20 achados, nenhum grau 4 · um avaliador, sem usuários |
| 23. Qualidade e segurança | 1:15 | 24:35 | invariantes viram teste · reprodutibilidade: semente, hash, versão · WCAG calculada no teste · revisão: 7 achados, 3 corrigidos · CWE-79: HTML sem escape |
| 24. Processo e uso de IA | 0:50 | 25:25 | Pull Request + checks + revisão humana · IA declarada em commit e PR · fonte conferida por pessoa · erros da IA registrados · 2 afirmações de IA derrubadas |
| 25. Ameaças à validade | 1:15 | 26:40 | Wohlin: construto, interna, externa, conclusão · janela disjunta, Kaufman · simulado ≠ produção, Sommer e Paxson · circularidade do desenho · limiar, pesos, LGPD |
| 26. Conclusão e próximos passos | 1:15 | 27:55 | sim, nas duas grandezas · 18,44% para 0,40% · 35,0% para 100,0% · ganho vem da D2 · D3: segundo estágio de triagem · custo: mais alarme · próximos: limiar, dado real, produção |
| 27. Referências | 0:15 | 28:10 | obrigado · 21 referências conferidas · repositório público · quem responde o quê |

*Tempos estimados, não medidos.*

## Se estourar no ensaio

Corte nesta ordem:

1. **Slides 12 e 13, as regras da C0 e da D1.** Diga só “a C0 e a D1 são regras com pontos, em tabela”: economiza 1:30.
2. **Slide 24, o processo e a IA.** Reduza a duas frases, que já estão no slide 26: economiza 0:35.
3. **Slide 2, a estrutura.** Pule: economiza 0:20.

**Nunca corte** os slides 19, 20 e 21 (resultados e contrapeso) nem o 25 (ameaças à validade). São o que a banca avalia.

## Slide a slide

### Slide 1 · Capa

*0:30 · acumulado 0:30 · no slide: Título, autores, orientador, palavras-chave do artigo.*

**Palavras-chave:** experimento controlado · protótipo de software · 4 configurações, mesmos dados

Boa tarde. Eu sou o Filipe e apresento o trabalho que fizemos eu, o Davi e a Yasmin, com orientação do professor Euzébio.

Estudamos se avaliar o risco do evento junto com o padrão da pessoa e com a exposição acumulada reduz o ruído no monitoramento de logs. Fizemos isso como um experimento controlado, com um protótipo de software que roda quatro configurações sobre os mesmos dados.

**Passe para:** “Vou seguir a ordem de um artigo científico.”

### Slide 2 · Estrutura da apresentação

*0:20 · acumulado 0:50 · no slide: Sete blocos, na ordem do artigo, com os slides de cada um.*

**Palavras-chave:** ordem do artigo · 7 blocos · 28 minutos

Primeiro o contexto e o referencial, depois a pergunta, o sistema e o modelo, o método, os resultados, a qualidade e as ameaças à validade, e por fim a conclusão.

**Passe para:** “Começando pelo problema.”

### Slide 3 · O problema

*1:15 · acumulado 2:05 · no slide: Três limites da regra fixa, cada um com o autor que o documenta.*

**Palavras-chave:** evento isolado não tem padrão · autorização: ações permitidas · taxa-base, Axelsson · exaustão, Sundaramurthy · SOC sem contexto, Vielberth

O ponto de partida é a regra fixa sobre evento isolado, e ela tem três limites documentados.

Primeiro, o evento isolado não carrega o padrão esperado de quem o produziu. Falhas de autenticação são eventos discretos, mas o abuso de autorização costuma ser feito de ações permitidas, e o que destoa é a ordem, o volume ou a combinação.

Segundo, a raridade do evento malicioso faz o falso positivo dominar a fila: é a falácia da taxa-base, de Axelsson.

Terceiro, o custo é humano. Sundaramurthy mostra o esgotamento do analista, e Vielberth aponta o descompasso entre o volume de alertas e a capacidade de triagem, agravado pela falta de contexto comportamental nas ferramentas.

**Passe para:** “Vale ver a taxa-base com os nossos números.”

### Slide 4 · A falácia da taxa-base

*1:00 · acumulado 3:05 · no slide: A fórmula de Axelsson e um gráfico da precisão implícita de cada configuração.*

**Palavras-chave:** P = TPR·p / (TPR·p + FPR·(1−p)) · p = 0,18% · C0: 1 verdadeiro a cada 513 · C2: 1 a cada 12 · cálculo nosso, não medida

A precisão de um alerta depende da taxa de acerto, da taxa de falso positivo e da proporção p de eventos maliciosos. É a fórmula que Axelsson demonstrou.

Aqui p é 0,18%. Aplicando a fórmula a uma revocação de 0,20 e à taxa de falso positivo que medimos em cada configuração, a precisão implícita é de cerca de 0,2% na C0, um verdadeiro a cada 513 alertas, e de cerca de 8,3% na C2, um a cada doze.

É um cálculo nosso a partir da fórmula, e não uma medida do experimento. A precisão medida no limiar de operação, que não foi calibrado, é de 0,32% na C0 e 0,57% na C2.

> **Cuidado:** Os valores do gráfico são calculados pela fórmula, com p = 0,18%, revocação 0,20 e a FPR medida de cada configuração. O slide diz isso. Não chame de resultado do experimento.

**Passe para:** “O referencial organiza o problema em três blocos.”

### Slide 5 · Referencial: o domínio

*1:15 · acumulado 4:20 · no slide: Tabela: autor, contribuição e uso no trabalho, para o domínio de segurança e logs.*

**Palavras-chave:** Kent e Souppaya: logs · Grassi e Sandhu: autenticação x autorização · Gonzalez-Granadillo: SIEM · Vielberth: SOC · Sundaramurthy e Alahmadi: custo humano · Cappelli e Homoliak: ameaça interna

Este slide reúne a base de domínio, autor por autor.

Kent e Souppaya, do NIST, tratam da gestão de logs e de como o volume e a diversidade dificultam a leitura. Grassi e Sandhu distinguem autenticação de autorização, o que explica por que o abuso é feito de ações permitidas.

Gonzalez-Granadillo descreve o SIEM e o limite das regras escritas à mão. Vielberth, numa revisão sistemática de SOC, aponta o descompasso de volume e a falta de contexto. Sundaramurthy e Alahmadi mostram o custo humano do ruído.

E Cappelli e Homoliak descrevem a ameaça interna, em padrões que se desenvolvem no tempo.

**Passe para:** “Esses autores se organizam numa taxonomia.”

### Slide 6 · Referencial: a taxonomia de anomalias

*1:15 · acumulado 5:35 · no slide: Tabela: tipo de anomalia (Chandola et al., 2009), exemplo, autores e a dimensão que cobre. E a lacuna.*

**Palavras-chave:** Chandola 2009: pontual, contextual, coletiva · D1 = pontual · D2 = contextual: Denning, Shashanka · D3 = coletiva: Cappelli, Homoliak · lacuna: três leituras separáveis

O referencial usa a taxonomia de Chandola e colegas, de 2009, que distingue três tipos de anomalia.

A pontual, quando um evento destoa sozinho: é o que a regra fixa enxerga, e é a nossa D1.

A contextual, quando o evento só é anômalo no histórico de quem o produziu. É a ideia de perfil por sujeito, de Denning, 1987, e a análise de usuário e entidade, de Shashanka, 2016. É a nossa D2.

E a coletiva, quando uma sequência de eventos ordinários é anômala em conjunto. Cappelli e Homoliak descrevem a ameaça interna se instalando assim, e é a nossa D3.

A lacuna, na seção 2.2 do artigo, é que nenhuma avaliação trata as três leituras de forma separável. Não propomos um mecanismo inédito: medimos quanto cada leitura acrescenta.

> **Cuidado:** O trabalho NÃO afirma ter criado um método novo de detecção. A contribuição é a avaliação comparativa, com as três leituras separáveis.

**Passe para:** “E para medir, o referencial metodológico.”

### Slide 7 · Referencial: o método

*1:15 · acumulado 6:50 · no slide: Tabela: autor, contribuição e onde entra no desenho do experimento.*

**Palavras-chave:** Wohlin 2012: experimentação em ES · Wilcoxon 1945 e Demšar 2006 · Kaufman 2012: vazamento · Sommer e Paxson 2010: realismo

Do lado metodológico, são quatro apoios.

Wohlin e colegas organizam a experimentação em engenharia de software e as quatro categorias de ameaça à validade. Wilcoxon, de 1945, é o teste pareado, e Demšar o recomenda para comparar configurações sobre vários conjuntos de dados.

Kaufman descreve o vazamento de informação no treino, que nos obriga a usar uma janela de padrão disjunta da avaliação. E Sommer e Paxson, de 2010, alertam que avaliar um detector de anomalias só sobre atividade simulada tende a carecer de realismo, o que declaramos como ameaça externa.

**Passe para:** “Com isso, a pergunta e a hipótese.”

### Slide 8 · Pergunta, variáveis e hipótese

*1:00 · acumulado 7:50 · no slide: A pergunta e a tabela de variáveis, hipótese e hipótese nula.*

**Palavras-chave:** aplicada, quantitativa, experimental · VI: configuração C0 a C3 · VD: FPR a revocação fixa, revocação L · hipótese refutável · H0: mesma FPR na mesma semente

É pesquisa aplicada, quantitativa e experimental. A variável independente é a configuração de avaliação, de C0 a C3. As variáveis dependentes são a taxa de falsos positivos a revocação fixa e a revocação por episódio nos cenários longitudinais.

A hipótese tem direção e admite refutação: se a C3 não ganhar da C2, a resposta é não. A hipótese nula do teste é que duas configurações têm a mesma taxa na mesma semente.

> **Cuidado:** A pergunta completa está na seção 1.4 do artigo, se a banca pedir.

**Passe para:** “Vamos ao software que testa isso.”

### Slide 9 · Arquitetura do sistema

*1:15 · acumulado 9:05 · no slide: Figura 1: arquitetura em camadas, com portas e adaptadores, e os números de engenharia.*

**Palavras-chave:** camadas, portas e adaptadores · detection puro: sem rede, relógio, banco · adaptador de arquivos e PostgreSQL · runner e API chamam o mesmo núcleo · regra de dependência testada · 765 testes, ~10 mil linhas

Do lado da engenharia de software, o desenho é em camadas, com portas e adaptadores.

O núcleo, detection, é puro: não acessa rede, relógio nem banco, e só conhece as interfaces declaradas em ports.py. Quem fornece os dados são adaptadores: um sobre arquivos, que permite reproduzir o experimento sem servidor, e outro sobre PostgreSQL.

O mesmo núcleo é chamado por duas entradas: o runner, em lote, que gera a tabela de resultados, e a API FastAPI, só de leitura, que alimenta o painel. Por isso o painel mostra o mesmo código que produziu os números.

A regra de dependência é testada: um teste reprova se detection importar backend, database ou generator. São cerca de dez mil linhas de código e dez mil de testes, com 765 testes automáticos.

> **Cuidado:** As linhas são contagem de wc em arquivos Python (código e testes), sem descontar vazias e comentários. Diga “cerca de”.

**Passe para:** “E os dados sobre os quais isso roda.”

### Slide 10 · Dados e ambiente simulado

*1:15 · acumulado 10:20 · no slide: Fatos do ambiente e a Figura 2: quem acessa qual banco, e o acesso que não existe.*

**Palavras-chave:** 250 funcionários, 1 ano · 8 tipos de evento · estado diário lido na data · 3 bancos: corp, ground_truth, sdcac · aplicação não conecta no gabarito · sem dado real

O ambiente é simulado, gerado por software: 250 funcionários ao longo de um ano, com 20 a 50 eventos por dia útil por funcionário, em oito tipos de evento. Parte da postura não é evento, é estado diário, lido na data do evento.

A separação entre dados e gabarito é estrutural: três bancos. O corp tem os eventos sem rótulo. O ground_truth tem os episódios e os rótulos. O sdcac tem padrões, notas e alertas.

O usuário da aplicação não tem permissão de conectar no ground_truth, e só a rotina de métricas o lê. Não há dado de pessoa real em nenhuma etapa.

> **Cuidado:** Os valores que descrevem a simulação são parâmetros declarados do gerador, e não estimativas de organizações reais. Nenhuma conclusão depende de corresponderem ao mundo real.

**Passe para:** “Sobre esse ambiente, os cenários.”

### Slide 11 · Cenários e gabarito

*1:00 · acumulado 11:20 · no slide: Tabela das quatro famílias, o que cada uma exercita e a unidade de análise.*

**Palavras-chave:** 20 cenários, 124 episódios · P 24 · B 16 · L 12 · N 72 · N = controle negativo · unidade: evento ou episódio · especificação sem ver as fórmulas

Sobre o tráfego normal injetamos 20 cenários, 124 episódios por semente, em quatro famílias. P, pontuais, 24 episódios, medidos por evento. B, de contexto, 16, e L, longitudinais, 12, medidos por episódio, que é o par funcionário e cenário. E N, o controle negativo, 72 episódios, dos quais 53 são a janela de manutenção noturna de TI, legítima.

A unidade importa: num cenário longitudinal que só cruza o limiar no oitavo dia, a medição por evento dá revocação perto de 0,15, e por episódio, 1,00. Por isso nenhuma tabela mistura as duas.

A especificação dos cenários foi feita sem acesso às fórmulas de pontuação.

**Passe para:** “Agora, o modelo, dimensão por dimensão. Primeiro a linha de base.”

### Slide 12 · C0: a linha de base

*1:00 · acumulado 12:20 · no slide: As quatro regras fixas da C0 e seus pontos.*

**Palavras-chave:** regras fixas, sem parâmetro aprendido · fora do horário 30 · origem externa 30 · recurso restrito 35 · força bruta 40: 10 falhas em 2 min

A C0 é a linha de base: regras fixas sobre o evento, com limites iguais para os 250 funcionários e nenhum parâmetro aprendido.

Fora do horário, das 6 às 22 no fuso do site, vale 30 pontos. Origem externa, 30. Acesso a recurso restrito, 35. E força bruta, dez falhas de autenticação em dois minutos, 40.

A noção de origem habitual vem de faixas de rede cadastradas, e não do histórico de cada pessoa, para que a informação que queremos medir não esteja no controle. A regra de dois minutos é correlação de curto prazo, por isso o reconhecimento de tentativas sucessivas não conta como ganho das dimensões.

**Passe para:** “A D1 enriquece o evento.”

### Slide 13 · D1: o risco do evento

*1:00 · acumulado 13:20 · no slide: Tabela de regras e pontos da D1, e os pontos por origem de rede e sensibilidade.*

**Palavras-chave:** privilégio 40 · dispositivo pessoal e download externo 25 · fora do expediente, download ≥ 50 MiB, removível 20 · sem MFA 15 · sensibilidade: 5 a 35

A D1 avalia o evento com mais atributos. Mudança de privilégio vale 40. Dispositivo pessoal e download para destino externo, 25 cada. Horário fora do expediente no fuso do funcionário, download grande, a partir de 50 megabytes, e dispositivo removível, 20. Login sem segundo fator, 15, e navegação de risco, 10.

Somam-se pontos pela origem de rede, casa 10 e externa 30, e pela sensibilidade do recurso, de 5 para interno até 35 para restrito. Os pontos ordenam o que o detector prioriza, e não a gravidade conceitual de cada sinal.

> **Cuidado:** Os pontos são parâmetros declarados, preliminares e sem análise de sensibilidade. Diga isso se a banca perguntar “por que 40?”.

**Passe para:** “A D2 muda a referência: a própria pessoa.”

### Slide 14 · D2: o desvio do padrão da pessoa

*1:15 · acumulado 14:35 · no slide: A fórmula do desvio robusto e a tabela das sete características e seus pontos.*

**Palavras-chave:** padrão: 3 primeiros meses · mediana e MAD × 1,4826 · piso e teto 6, um lado só · 7 características · mín. 20 dias de atividade · janela disjunta

A D2 compara a pessoa com ela mesma. O padrão vem dos três primeiros meses, uma janela disjunta da avaliação, e quem teve menos de 20 dias de atividade nela não recebe padrão próprio.

O desvio é em dispersões robustas: mediana e MAD escalado por 1,4826, com um piso para quem é perfeitamente regular e um teto de seis. É de um lado só, porque fazer menos que o habitual não é risco. Os pontos são proporcionais ao desvio.

São sete características: volume e falhas, por desvio robusto; a mistura de sigilo, por distância de distribuição; recurso, origem e dispositivo novos, por novidade; e o horário incomum. A nota é o maior entre duas janelas, sessão e usuário-dia. Quem não tem histórico suficiente cai no padrão do grupo de pares.

**Passe para:** “E a D3 acumula no tempo.”

### Slide 15 · D3: a exposição acumulada

*1:00 · acumulado 15:35 · no slide: A fórmula da conduta e a tabela da postura de segurança.*

**Palavras-chave:** conduta: decaimento 0,85/dia · janela de 14 dias · evento atual fora (D-18) · postura: estado do dia · duas parcelas separadas, 0 a 100

A D3 tem duas parcelas separadas, cada uma de 0 a 100. A conduta é o que a pessoa fez: a soma dos pontos dos eventos anteriores, com decaimento de 0,85 ao dia numa janela de 14 dias. O evento atual fica de fora, para não contar o mesmo risco duas vezes.

A postura é o estado da conta e do equipamento na data do evento: segundo fator desligado, privilégio de administrador, atualização atrasada, antivírus desligado, e o desfecho de campanhas de phishing. O código recusa um retrato de outro dia, para o futuro não vazar para o passado.

As duas parcelas ficam guardadas em campos separados, para o analista ver qual delas causou o alerta. Na nota final elas se somam com pesos declarados, e a postura entra com metade do peso, por ser estado e não ação.

**Passe para:** “Resta integrar tudo numa nota.”

### Slide 16 · Integração e faixas de risco

*0:45 · acumulado 16:20 · no slide: A nota S, os campos guardados e as faixas.*

**Palavras-chave:** um só conjunto de pesos · 5 parcelas guardadas · nulo ≠ zero · entrada que falta é erro · faixas: 20 · 50 · 75

A nota final é a soma ponderada das parcelas que a configuração liga, com um único conjunto de pesos para as quatro configurações, para que a única variável seja a dimensão.

O resultado é decomponível: guarda as cinco parcelas em campos próprios, e uma parcela não ligada é nula, e não zero. Entrada que falta é erro, e não zero, para a tabela de ablação não ter números plausíveis e sem sentido.

As faixas, normal até 20, baixo até 50, médio até 75 e alto acima, existem só para a tela. A avaliação usa a nota bruta.

**Passe para:** “Agora, como o experimento foi conduzido.”

### Slide 17 · Protocolo experimental

*1:15 · acumulado 17:35 · no slide: O pipeline de cinco etapas e o que cada uma faz.*

**Palavras-chave:** 5 etapas independentes · só a avaliação lê o gabarito · agregação recusa o incomparável · 10 sementes pareadas · semente + SHA-256 + versão do código

O protocolo segue a experimentação em engenharia de software, de Wohlin e colegas. São cinco etapas, cada uma um programa independente: geração, tradução, pontuação, avaliação e agregação.

Só a avaliação lê o gabarito. E a agregação recusa reunir execuções não comparáveis: limiar distinto, níveis de revocação distintos, conjunto de configurações distinto ou a mesma execução contada duas vezes, porque a média de execuções incomparáveis é um número plausível que nada denunciaria.

As quatro configurações rodam sobre as mesmas dez sementes, então a comparação é pareada. Cada execução grava a semente, o SHA-256 da configuração e a versão do código.

**Passe para:** “As métricas e o teste estatístico.”

### Slide 18 · Métricas e estatística

*1:15 · acumulado 18:50 · no slide: As fórmulas das métricas e um gráfico do menor p possível em função do número de sementes.*

**Palavras-chave:** FPR a revocação fixa · Rec_L por episódio · Wilcoxon pareado exato · p_min = 2/2^n · n=5: 0,0625 · n=10: 0,0020 · critério: 45 alertas falsos por turno

São duas métricas. A taxa de falsos positivos, falso positivo sobre falso positivo mais verdadeiro negativo, no ponto em que todas as configurações atingem a mesma revocação. E a revocação por episódio, só na família longitudinal.

O teste é Wilcoxon pareado, como Demšar recomenda, com p exato. O menor p possível com n pares é 2 sobre 2 elevado a n. Com cinco pares seria 0,0625, acima de 0,05; com dez, 0,0020. Por isso o piso de dez sementes. E 0,0020 é o piso da escala, e não “menor que isso”.

O critério de sucesso é operacional: até 45 alertas falsos por turno, e revocação longitudinal de pelo menos 0,80. Os dois valores foram fixados em 12 de novembro, depois da primeira execução, e o artigo declara isso.

> **Cuidado:** Não diga “p menor que 0,0020”. Com dez pares, 0,0020 é o piso. E diga que o critério foi fixado depois da primeira execução.

**Passe para:** “Vamos aos resultados. Primeiro, o ruído.”

### Slide 19 · Resultado 1: ruído

*1:15 · acumulado 20:05 · no slide: Barras da taxa de falsos positivos a revocação 0,20: 18,44%, 6,03%, 0,40% e 0,54%.*

**Palavras-chave:** revocação 0,20 · 18,44% para 0,40% · 0,30: 34,55% para 1,33% · C0 não chega a 0,40 · p = 0,0020 nos nove níveis

Com a revocação fixada em 0,20, a taxa de falsos positivos da C0, as regras fixas, é 18,44%. A C1 cai para 6,03%. A C2, com o padrão individual, cai para 0,40%. A C3 fica em 0,54%. As barras estão em escala, por isso a da C2 quase não aparece.

Em 0,30 de revocação, 34,55% contra 1,33%. E a C0 não alcança revocação de 0,40 sem alertar o registro inteiro: para ela, esse nível só existe com 100% de falso positivo.

A C2 tem taxa menor que a C0 nos nove níveis, com p igual a 0,0020, o piso do teste com dez sementes.

> **Cuidado:** NÃO DIGA que o sistema está pronto para operar. A diferença é entre configurações, e o limiar não foi calibrado. Você volta a isso no slide 21.

**Passe para:** “E a segunda metade: cobertura.”

### Slide 20 · Resultado 2: cobertura

*1:00 · acumulado 21:05 · no slide: Colunas por família de cenário e, à direita, a família N (alarme sobre atividade legítima).*

**Palavras-chave:** família L: 35,0% para 100,0% · B: 28,7% para 98,8% · P: C0 já vai bem · N é alarme: menos é melhor · 75,8% para 96,0% · isso é o custo

O gráfico mostra, por família de cenário, a fração dos episódios que cada configuração detecta.

Olhem a família L, de escalada gradual, onde a regra por evento é cega. A C0 detecta 35,0%. A C2 detecta 100,0%. Em B, de contexto, de 28,7% para 98,8%. Nas pontuais, P, a C0 já vai bem, 83,3%, porque é o que regra fixa sabe fazer.

Agora a família N, à direita. Ela é benigna por construção: o número ali é alarme sobre atividade legítima, e menos é melhor. Sobe: de 75,8% na C0 para 96,0% na C2 e 100% na C3. Isso é o custo.

**Passe para:** “Então o resultado tem um contrapeso.”

### Slide 21 · O contrapeso

*1:15 · acumulado 22:20 · no slide: Três números: 96,0%, “sem ganho” e 99,84%.*

**Palavras-chave:** 96,0% legítimos alertam · C3 sem ganho · 99,84% no corte 20 · limiar não calibrado · C2: 7 de 10 sementes · 45 alertas por turno

Este é o slide mais importante para a honestidade do trabalho. O modelo ganha nas duas grandezas que a pergunta mede e perde numa terceira, que a pergunta não mede.

Primeiro: 96,0% dos episódios legítimos geram alerta na C2, contra 75,8% na C0. O ganho de cobertura não foi de graça.

Segundo: a exposição acumulada, a C3, não reduziu os falsos positivos de forma significativa em nenhum regime. A hipótese admitia essa resposta, e ela é reportada.

Terceiro: no limiar herdado, o corte 20, a C3 alerta sobre 99,84% do registro. O limiar não foi calibrado, e nesse corte nenhuma das quatro configurações é operável. É o primeiro trabalho futuro.

Para não ficar só no lado ruim: a 0,20 de revocação, a C2 cumpre o critério de 45 alertas falsos por turno em 7 das 10 sementes.

> **Cuidado:** NÃO DIGA “o sistema funciona”. DIGA: “reduz ruído e aumenta cobertura nos cenários medidos, e não é livre de custo”.

**Passe para:** “O que o analista vê: o painel.”

### Slide 22 · O painel de análise

*1:00 · acumulado 23:20 · no slide: As quatro faixas com cor, rótulo e forma, e um exemplo de nota decomposta.*

**Palavras-chave:** nota decomposta · “não ligada” não é zero · cor + rótulo + forma · WCAG 1.4.1 e 1.4.3 · 20 achados, nenhum grau 4 · um avaliador, sem usuários

O painel existe para o analista não receber um número que precise aceitar sem poder verificar: a nota aparece decomposta por dimensão, e uma parcela que a configuração não liga aparece como “não ligada”, e não como zero.

Cada faixa tem cor, rótulo e forma: círculo, triângulo, octógono. Isso cumpre o critério 1.4.1 da WCAG 2.2: cor não pode ser o único meio de informação. O contraste é de pelo menos 4,5 para 1, critério 1.4.3, calculado no teste.

A avaliação heurística achou 20 problemas, nenhum de severidade 4, com um avaliador só e sem usuários.

> **Cuidado:** Diga com clareza: o que se afirma é que esses problemas existem, e não que a interface seja adequada ao uso. O painel é instrumento de análise, não objeto de avaliação. A barra de exemplo é ilustrativa, e está escrito assim nela.

**Passe para:** “Do lado da engenharia, como garantimos a qualidade.”

### Slide 23 · Qualidade e segurança

*1:15 · acumulado 24:35 · no slide: Tabela: o que é verificado e como.*

**Palavras-chave:** invariantes viram teste · reprodutibilidade: semente, hash, versão · WCAG calculada no teste · revisão: 7 achados, 3 corrigidos · CWE-79: HTML sem escape

As invariantes do desenho viram testes automáticos que rodam a cada alteração: o gabarito é inacessível à aplicação, o log só aceita inserção, e uma parcela não ligada aparece como ausente, e não como zero.

A reprodutibilidade vem do registro de cada execução: semente, hash da configuração e versão do código. A acessibilidade do painel é calculada no teste.

Fizemos uma revisão de segurança do código, por leitura: sete achados e três corrigidos com teste. O principal foi HTML montado com campos do log sem escapar, a classe CWE-79, num painel que existe para vigiar log. Os outros dois foram um curinga aceito no CORS e uma permissão herdada no banco.

> **Cuidado:** Diga: a revisão de segurança é por leitura de código, não teste de intrusão, e nenhum achado foi explorado.

**Passe para:** “E o processo por trás disso.”

### Slide 24 · Processo e uso de IA

*0:50 · acumulado 25:25 · no slide: Quatro práticas de rastreabilidade, e o que a conferência das fontes encontrou.*

**Palavras-chave:** Pull Request + checks + revisão humana · IA declarada em commit e PR · fonte conferida por pessoa · erros da IA registrados · 2 afirmações de IA derrubadas

Todo commit e todo Pull Request declara qual IA ajudou e em quê. Referência que a IA produziu só entra depois de conferida na fonte, e conferência feita por máquina é dita assim, porque a decisão de aceitar é de uma pessoa.

Cada sessão tem um relatório com os erros da IA e quem os pegou. Um exemplo recente: na conferência das fontes da página de segurança, duas afirmações escritas pela IA não se sustentaram e foram corrigidas.

**Passe para:** “Agora, o que o trabalho não prova.”

### Slide 25 · Ameaças à validade

*1:15 · acumulado 26:40 · no slide: Tabela das quatro categorias de Wohlin et al. (2012): ameaça e mitigação, mais três limites.*

**Palavras-chave:** Wohlin: construto, interna, externa, conclusão · janela disjunta, Kaufman · simulado ≠ produção, Sommer e Paxson · circularidade do desenho · limiar, pesos, LGPD

Declaramos as ameaças à validade nas quatro categorias de Wohlin e colegas.

De construto: o gabarito é feito pelos próprios autores, e o risco é um construto. Mitigamos com a unidade de análise explícita. Interna: o padrão vem de uma janela disjunta da avaliação, para não ter vazamento, como alerta Kaufman. Há ainda a circularidade do desenho, em que a D3 foi feita para a escalada gradual e os cenários longitudinais também. Mitigamos com um controle negativo longitudinal e separando quem especifica os cenários de quem implementa as fórmulas.

Externa: o ambiente é simulado, e Sommer e Paxson avisam que avaliar só sobre atividade simulada tende a carecer de realismo. Conclusão estatística: dez sementes e teste pareado.

E há limites: o limiar não foi calibrado, os pesos não passaram por análise de sensibilidade, e dado pessoal real exige a LGPD.

**Passe para:** “Com isso, a conclusão.”

### Slide 26 · Conclusão e próximos passos

*1:15 · acumulado 27:55 · no slide: Respostas, contribuições e próximos passos.*

**Palavras-chave:** sim, nas duas grandezas · 18,44% para 0,40% · 35,0% para 100,0% · ganho vem da D2 · D3: segundo estágio de triagem · custo: mais alarme · próximos: limiar, dado real, produção

Voltando à pergunta: nos cenários medidos, sim, nas duas grandezas, com significância estatística. A taxa de falsos positivos cai de 18,44% para 0,40% a 0,20 de revocação, e a cobertura longitudinal vai de 35,0% para 100,0%.

O ganho vem do padrão individual, a D2. A D3 não acrescentou, e a leitura que os dados sustentam, seção 4.5, é que ela pertence a um segundo estágio de triagem. E o ganho tem custo: sobe o alarme sobre atividade legítima.

O trabalho deixa cinco contribuições: o protótipo, as quatro configurações canônicas, as regras e pesos com SHA-256, os cenários de teste automatizados e o contrato de leitura da API.

Os próximos passos decorrem das limitações: calibrar o limiar e analisar a sensibilidade dos pesos; implantar sobre dado real, com LGPD e ISO/IEC 27001; e validar contra tráfego de produção.

**Passe para:** “Obrigado.”

### Slide 27 · Referências

*0:15 · acumulado 28:10 · no slide: As 21 referências do artigo, em ABNT, e o endereço do repositório.*

**Palavras-chave:** obrigado · 21 referências conferidas · repositório público · quem responde o quê

Obrigado. As referências estão neste slide, e o código, os dados e os relatórios de cada sessão estão no repositório público. Ficamos à disposição para as perguntas.

> **Cuidado:** Se a pergunta for sobre uma parte que não é sua: diga o que você sabe e passe para quem cuidou. Davi: arquitetura, banco, API, gerador. Yasmin: segurança, referencial, cenários, pesos. Filipe: painel, usabilidade, resultados.

## As cinco frases que não podem faltar

1. “A pergunta tem duas grandezas: falsos positivos a uma mesma revocação, e revocação nos cenários longitudinais.”
2. “A taxonomia de Chandola liga cada dimensão a um tipo de anomalia: D1 pontual, D2 contextual, D3 coletiva.”
3. “A taxa de falsos positivos cai de 18,44% para 0,40%, e a cobertura longitudinal vai de 35,0% para 100,0%.”
4. “O ganho tem custo, e a terceira dimensão não ajudou: a hipótese admitia essa resposta.”
5. “O limiar não foi calibrado, e os resultados valem para o ambiente simulado.”

## O que não dizer

- **“O sistema funciona” ou “está pronto”.** O artigo não sustenta isso. Diga “reduz ruído e aumenta cobertura nos cenários medidos”.
- **“Criamos um novo método de detecção”.** O trabalho avalia quanto cada leitura acrescenta. Não propõe mecanismo inédito.
- **“A D3 melhora o resultado”.** Não melhorou. Foi reportado como tal.
- **“p menor que 0,0020”.** Com dez sementes, 0,0020 é o piso do teste, então é “p igual a 0,0020”.
- **“A precisão da C2 é 8%”.** É um cálculo pela fórmula de Axelsson, e não uma medida. A precisão medida no limiar de operação é 0,57%.
- **“Testamos com usuários”.** Não houve usuários, e a avaliação heurística teve um avaliador.
- **“Os dados são reais”.** São sintéticos.

## Perguntas prováveis da banca

### Se 96,0% dos episódios legítimos geram alerta na C2, a quem serve o ganho de cobertura?

No corte herdado, o corte 20, a ninguém: o limiar não foi calibrado, e nenhuma configuração é operável. O que se afirma é outra coisa: com o limiar escolhido para uma revocação fixa de 0,20, a C2 tem 0,40% de falsos positivos e cumpre o critério de 45 alertas falsos por turno em 7 das 10 sementes. Calibrar o limiar é o primeiro trabalho futuro.

*Quem responde: Filipe.*

### Por que dado sintético? Isso não invalida o resultado?

Não temos acesso a log de empresa real, e só em simulação existe um gabarito confiável de quem é malicioso. O trabalho declara que ambiente simulado não é produção e cita Sommer e Paxson, que avisam que avaliar só sobre atividade simulada tende a carecer de realismo. Os números valem para os cenários medidos.

*Quem responde: Davi (gerador) ou Yasmin (cenários).*

### Por que a terceira dimensão não ajudou?

O que se mediu é que a C3 não reduziu os falsos positivos de forma significativa em nenhum regime, e a hipótese admitia essa resposta. A seção 4.5 do artigo diz que a leitura que os dados sustentam é que a D3 pertence a um segundo estágio de triagem, uma lista de pessoas a examinar com periodicidade própria, e não ao mesmo corte que decide se um evento gera alerta agora.

*Quem responde: Filipe.*

### O sistema é operável?

No limiar herdado, o corte 20, nenhuma das quatro configurações é: a C3 alerta sobre 99,84% do registro. Com a revocação fixada em 0,20, a C2 cumpre o critério de 45 alertas falsos por turno em 7 das 10 sementes. Calibrar o limiar é o primeiro trabalho futuro.

*Quem responde: Filipe.*

### O critério de sucesso foi fixado depois da primeira execução. Isso não é ajustar a meta ao resultado?

É um risco, e por isso está declarado no artigo com a data: 12 de novembro, depois da primeira execução registrada. O número de 45 alertas por turno veio de um argumento operacional, quantos alertas falsos um analista absorve, e não do resultado.

*Quem responde: Davi.*

### Como vocês garantem que o gabarito não vazou para o motor?

O gabarito fica em um banco separado, e a aplicação não tem permissão de conectar nele. Um teste automático reprova se alguém conceder essa permissão. A especificação dos cenários também foi feita sem acesso às fórmulas de pontuação. O artigo trata a objeção de desenho não cego na seção 3.8.

*Quem responde: Yasmin.*

### Por que Wilcoxon, e por que só dez sementes?

Wilcoxon porque o teste é pareado: a mesma semente gera a mesma população para as quatro configurações, e Demšar o recomenda para comparar configurações sobre vários conjuntos de dados. De postos porque a taxa de falsos positivos se acumula perto de zero. Exato porque, com dez pares, a distribuição é contável. Com cinco sementes, o menor p seria 0,0625.

*Quem responde: Davi ou Filipe.*

### Por que uma arquitetura de portas e adaptadores?

Para o núcleo de avaliação não conhecer o meio de armazenamento. Isso permite rodar o experimento sem servidor de banco, por razão metodológica, e garante que o runner, que gera a tabela, e a API, que alimenta o painel, chamem o mesmo código. Um teste reprova se o núcleo importar backend, banco ou gerador.

*Quem responde: Davi.*

### Como a reprodutibilidade é garantida?

Cada execução grava a semente, a configuração, a versão dos pesos, o SHA-256 da configuração em ordem canônica e o identificador da versão do código. Duas execuções só são comparáveis se os hashes coincidirem, e a agregação recusa reunir execuções incomparáveis.

*Quem responde: Davi.*

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

### Por que esses pontos e pesos?

São parâmetros declarados, preliminares, e não passaram por análise de sensibilidade, o que está declarado como limitação e trabalho futuro. Os pontos ordenam o que o detector prioriza, e não a gravidade conceitual de cada sinal. Há um só conjunto de pesos para as quatro configurações, para que a única variável seja a dimensão.

*Quem responde: Yasmin ou Davi.*

### Quem fez o quê?

Todos sabem explicar o projeto inteiro. Por área: o Davi cuidou da arquitetura, do banco, da API e do gerador; a Yasmin, da segurança, do referencial, dos cenários e dos pesos; o Filipe, do painel, da usabilidade e dos resultados.

*Quem responde: Qualquer um dos três.*

## Quem responde o quê

| Assunto | Primeiro a responder | Se travar |
|---|---|---|
| Arquitetura, banco, API, gerador, ingestão | Davi | Passe para o Davi |
| Segurança, LGPD, ISO/IEC 27001, referencial, cenários, pesos | Yasmin | Passe para a Yasmin |
| Painel, usabilidade, resultados, avaliação heurística | Filipe | Responda com o que o slide mostra |
| Metodologia e estatística | Davi | Filipe, pelos slides 17 e 18 |
