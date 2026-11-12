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

**Quanto ao ruído, a resposta é afirmativa com margem ampla.** À revocação de
0,20 a taxa de falsos positivos caiu de 20,05% na linha de base para 0,68% na
configuração que acrescenta o desvio em relação ao padrão individual. À
revocação de 0,30 a linha de base só alcança o ponto emitindo alerta sobre a
totalidade do registro, enquanto a configuração com duas dimensões o alcança com
1,83%. **Quanto à cobertura longitudinal, também é afirmativa:** medida por
episódio, a revocação passou de 25,0% para 100%, o que é coerente com o desenho
— aqueles cenários foram construídos para que nenhum evento isolado fosse
notável, e é essa a situação que as regras fixas não alcançam.

**A contrapartida não estava na pergunta.** A mesma configuração elevou de 73,7%
para 93,0% a proporção de episódios de controle negativo que produziram alerta,
isto é, de atividade legítima sinalizada. A pergunta mede ruído sobre o conjunto
de eventos e cobertura sobre os cenários longitudinais, e não o alarme sobre
comportamento legítimo incomum; é nesse terceiro eixo, não interrogado, que o
ganho encontra seu custo. O que os dados autorizam afirmar é redução de ruído e
aumento de cobertura nos cenários medidos — não superioridade sem custo.

Três restrições delimitam o alcance da resposta, todas declaradas na Seção 4.6:
**uma única semente** de geração, de modo que nenhuma diferença está distinguida
de variação de amostragem; limiar de operação não calibrado, razão pela qual a
comparação válida é a de falsos positivos a revocação fixa; e a quarta
configuração não executada. Como é a exposição acumulada a contribuição original
do trabalho, **a pergunta está respondida para a composição de duas dimensões e
permanece aberta para a de três**.

## 5.2 Objetivos alcançados

Dos oito objetivos específicos da Seção 1.5.2, os seis primeiros estão cumpridos
e verificáveis no repositório: o modelo de eventos e o gerador de logs
sintéticos com gabarito em base separada (a); a linha de base de regras fixas,
sem parâmetro estimado de comportamento (b); a avaliação do evento individual
(c); a identificação de divergência em relação ao padrão de cada usuário, em
janela de treino disjunta (d); a avaliação da exposição acumulada em duas
parcelas separadas (e); e a integração numa classificação decomponível (f).

O objetivo (g) está cumprido para três das quatro configurações, e o (h)
**parcialmente**: as duas grandezas primárias foram apuradas, mas o tratamento
estatístico da Seção 3.7 pressupõe de dez a vinte sementes e a execução
reportada usa uma. A análise é, nesse sentido, descritiva e não inferencial.

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
imediato, é **completar o desenho estatístico previsto** — executar o
experimento sobre as dez a vinte sementes da Seção 3.7, com o teste pareado, e
calibrar o limiar de operação —, que é o que converte a análise descritiva em
inferencial. O segundo é a **implantação sobre dado real à luz da Lei nº
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
