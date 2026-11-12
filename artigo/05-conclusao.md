# 5. Conclusão

> **5ª Versão** na numeração do professor — que junta **Conclusão e
> Referências** numa seção só, pela decisão **D-20** · S14 do
> [cronograma](../docs/cronograma.md) · Davi (caneta).

***

## 5.1 Retomada da pergunta de pesquisa

A pergunta da Seção 1.4 indaga se a avaliação combinada do risco do evento
individual, do desvio comportamental do usuário e da exposição acumulada ao
risco reduz a taxa de falsos positivos, a uma mesma revocação, e aumenta a
revocação em cenários longitudinais, quando comparada à análise baseada
exclusivamente em regras fixas aplicadas a eventos individuais. São duas
grandezas, e cada uma recebe resposta própria.

**Quanto ao ruído, a resposta é afirmativa com margem ampla e com
significância estatística.** À revocação de 0,20 a taxa de falsos positivos caiu
de 18,44% para 0,40% na configuração que acrescenta o desvio em relação ao padrão
individual, e a diferença se repete nos **nove níveis examinados**, com
p = 0,0020 em cada um — o menor valor que dez pares produzem num teste de
Wilcoxon pareado bilateral exato. À revocação de 0,40 a linha de base **não
alcança o ponto em nenhuma das dez execuções** sem alertar sobre a totalidade do
registro. **Quanto à cobertura longitudinal, também é afirmativa:** medida por
episódio, passou de 35,0% para 100,0% — os doze cenários, nas dez execuções —, o
que é coerente com o desenho: eles foram construídos para que nenhum evento
isolado fosse notável, e é essa a situação que as regras fixas não alcançam.

**A contrapartida não estava na pergunta.** A mesma configuração elevou de 75,8%
para 96,0% a proporção de episódios de controle negativo que produziram alerta —
atividade legítima sinalizada. A pergunta mede ruído sobre o conjunto de eventos
e cobertura nos cenários longitudinais, não o alarme sobre comportamento legítimo
incomum: é nesse terceiro eixo, não interrogado, que o ganho encontra seu custo.
O que os dados autorizam afirmar é redução de ruído e aumento de cobertura nos
cenários medidos — não superioridade sem custo.

**Quanto à terceira dimensão, a resposta é negativa no eixo do ruído.** O
acréscimo da exposição acumulada **não reduz a taxa de falsos positivos em
nenhum regime de revocação**: o teste pareado não rejeita a hipótese nula em
seis dos nove níveis, e nos três em que a rejeita é a configuração completa que
apresenta taxa **maior**. A vantagem que a execução de semente única sugeria
acima de 0,40 de revocação não sobreviveu às dez. O ganho dessa dimensão aparece
em outro lugar: ela leva a detecção por episódio a 100% nas três famílias
maliciosas — e alarma em 100,0% da família de controle negativo, o que torna o
ganho inseparável do custo.

A leitura é coerente com o que a exposição acumulada mede: um termo que cresce
devagar e atinge muita gente alcança os casos que nenhum evento isolado denuncia
e **não** separa os de maior risco. **A contribuição original do trabalho se
verifica, portanto, na segunda dimensão — o desvio em relação ao padrão do
próprio usuário —, e não na terceira.**

Três restrições delimitam o alcance da resposta, declaradas na Seção 4.6: o
**limiar de operação não calibrado**, razão pela qual a comparação válida é a de
falsos positivos a revocação fixa; a **subestimação** de duas parcelas da
configuração completa — a postura, nos eventos sem estado de equipamento, e a
exposição, nos empates de instante —, que torna o resultado dela conservador
nesse recorte; e o fato de dez sementes medirem variação de amostragem, não
validade externa, já que todas saem do mesmo gerador.

## 5.2 Objetivos alcançados

Dos oito objetivos específicos da Seção 1.5.2, os seis primeiros estão cumpridos
e verificáveis no repositório: o modelo de eventos e o gerador de logs
sintéticos com gabarito em base separada (a); a linha de base de regras fixas,
sem parâmetro estimado de comportamento (b); a avaliação do evento individual
(c); a identificação de divergência em relação ao padrão de cada usuário, em
janela de treino disjunta (d); a avaliação da exposição acumulada em duas
parcelas separadas (e); e a integração numa classificação decomponível (f).

Os objetivos (g) e (h) estão **cumpridos**: a comparação cobre as quatro
configurações, as duas grandezas primárias foram apuradas e o tratamento
estatístico da Seção 3.7 foi aplicado sobre **dez sementes de geração
independentes**, com teste de Wilcoxon pareado de p-valor exato. A análise é,
nesse sentido, inferencial e não apenas descritiva — e foi a inferência que
derrubou uma das conclusões que a execução de semente única autorizava, o que é
precisamente a razão de ela vir antes da conclusão e não depois.

## 5.3 Contribuições

O trabalho deixa cinco artefatos versionados: o **protótipo**, cuja camada de
avaliação é independente do meio de armazenamento, o que permite reproduzir o
experimento sem servidor de banco de dados; as **quatro configurações
canônicas**, semeadas e somente-leitura, que tornam a ablação repetível; o
**conjunto de regras e pesos** versionado, com resumo criptográfico preso a cada
execução, de modo que duas execuções só são comparáveis se os resumos
coincidirem; os **cenários de teste automatizados**, com as invariantes de
desenho da Seção 3.8 impostas por teste a cada alteração do código; e o
**contrato de leitura versionado**, que torna a nota decomponível inspecionável
fora da interface. A avaliação de usabilidade **não** é contribuição deste
trabalho, como declara a Seção 3.9.

## 5.4 Trabalhos futuros

Três desdobramentos decorrem das limitações da Seção 4.6. O primeiro, e mais
imediato, é **calibrar o limiar de operação** sobre dado em escala: sem isso,
nenhuma das quatro configurações é operável no corte herdado, e a única
comparação que o trabalho pode fazer é a de falsos positivos a revocação fixa.
A ele se soma o **reexame da terceira dimensão**, que no desenho atual não
contribui para a separação e talvez pertença a um segundo estágio de triagem, e
não ao mesmo corte das demais. O segundo é a **implantação sobre dado real à luz
da Lei nº
13.709/2018 e dos controles aplicáveis da ISO/IEC 27001:2022**: base legal,
transparência ao titular, minimização e retenção. O terceiro é a **validação
contra tráfego de produção**, que o ambiente simulado não substitui — acurácia
elevada sobre dado sintético pode indicar gerador previsível em vez de modelo
adequado, e só o registro real distingue as duas hipóteses.

> **A caneta desta seção é do Davi**, pela S14. O texto acima foi redigido a
> partir dos resultados registrados e dos itens que as instruções anteriores
> desta página enumeravam — **nada foi acrescentado além do que está no
> repositório** —, e precisa da leitura de quem assina.

***

## Resumo e Abstract

> **Mudaram para [o bloco de abertura](00-resumo.md) em 11/11/2026.**
>
> Eles moravam aqui porque é nesta etapa — a **5ª Versão** — que as diretrizes
> institucionais os cobram, e porque era aqui que seriam escritos. Em 11/11 as
> duas frases que faltavam em cada um — o resultado principal e a conclusão —
> puderam ser escritas, e no documento montado o bloco vai para o alto, logo
> depois dos autores.
>
> Manter o texto nos dois lugares é como a documentação deste projeto já
> apodreceu duas vezes. A entrega da 5ª Versão continua sendo esta seção; o
> texto do resumo mora em um arquivo só.

***

## O que esta seção ainda precisa

* [ ] Resposta direta à pergunta de pesquisa da Introdução
* [ ] Cada objetivo específico avaliado, inclusive os não cumpridos
* [ ] Resumo escrito — contexto, objetivo e método já estão; faltam resultado e
      conclusão, que dependem da Seção 4
* [x] Palavras-chave definidas — recuperadas do `.docx`, em 15/10/2026
* [ ] Abstract conferido por uma pessoa — foi redigido com auxílio de IA
* [x] Necessidade de abstract confirmada com o orientador — 04/09/2026
