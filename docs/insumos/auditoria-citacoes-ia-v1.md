# Auditoria das citações pendentes — v1

> **Insumo, versionado como recebido.** Esta página segue a regra da pasta: o
> material entra **sem edição**, e a correção — quando houver — mora na página de
> destino, não aqui.

| | |
|---|---|
| **Quem produziu** | **Uma IA**, em 12/11/2026, a pedido do Davi |
| **Entregue em** | 12/11/2026 |
| **Assistência de IA** | **Integral.** Não há parte humana neste documento |
| **Conferi tudo que a IA escreveu?** | **Não.** Ninguém abriu as obras |
| **Para onde vai** | `docs/citacoes-pendentes.md`, como **material de conferência** — não como conferência |

***

## ⚠️ Por que isto não fecha pendência nenhuma

O [`AGENTS.md`](../../AGENTS.md) seção 3 nomeia, entre o que nunca é aceitável,
**"referência bibliográfica que a IA produziu e ninguém conferiu na fonte"**.
Esta auditoria é exatamente isso: produzida por IA, e as obras não foram abertas
por nenhuma das três pessoas do grupo.

**A própria auditoria diz isso, no fim dela**, e vale citar porque é a parte mais
importante do documento:

> *"sua documentação estabelece que a pessoa responsável precisa abrir a fonte e
> assumir a conferência. Eu fiz a verificação técnica dos documentos e dos dados
> bibliográficos, mas não vou registrar Yasmin, Filipe ou você como responsáveis
> por uma conferência que não realizaram pessoalmente."*

**O que ela muda, então.** Ela não substitui a conferência — **encurta** o
trabalho dela. Antes, conferir uma pendência era procurar a obra, decidir se era
a certa e ler o trecho. Agora é abrir um documento nomeado e checar se o trecho
sustenta a afirmação. É menos trabalho, não trabalho nenhum.

**Uma distinção que a auditoria faz e que o projeto precisava ter escrito:**
confirmar que uma obra **existe** não é confirmar que ela **sustenta** a
afirmação à qual foi associada. As duas coisas foram separadas aqui, e é a razão
pela qual as três classificações dela — confirmada, confirmada com ressalva, não
confirmada — não se traduzem em "pendência fechada".

***

## O texto, como recebido

### Auditoria das citações pendentes

Vou tratar a conferência como uma auditoria bibliográfica acadêmica, separando
três situações:

1. **Confirmada:** a obra existe, os dados bibliográficos foram verificados e seu
   conteúdo sustenta a afirmação.
2. **Confirmada com ressalva:** a obra existe, mas há divergência de edição,
   autoria, ano ou adequação ao argumento.
3. **Não confirmada:** não há evidência suficiente para inserir a referência no
   artigo.

Um ponto importante: confirmar que um artigo científico existe não significa
confirmar que ele sustenta a afirmação à qual foi associado.

### 1. Pendências da metodologia — 5 fontes

| Citação | Resultado da conferência |
|---|---|
| WOHLIN et al. (2012) | Confirmada |
| DEMŠAR (2006) | Confirmada |
| WILCOXON (1945) | Confirmada |
| KAUFMAN et al. (2012) | **Ano incorreto** |
| SOMMER; PAXSON (2010) | Confirmada |

**1.1 Wohlin et al. (2012).** *Experimentation in Software Engineering*, Springer,
2012. Autores: Claes Wohlin, Per Runeson, Martin Höst, Magnus C. Ohlsson, Björn
Regnell, Anders Wesslén. O ano está correto. Ressalva de edição: a página da
Springer identifica a publicação de 2012 como 1ª edição, enquanto outros
registros a identificam como 2ª — **não inserir o número da edição sem conferir a
folha de rosto do exemplar usado**.

**1.2 Demšar (2006).** *Statistical Comparisons of Classifiers over Multiple Data
Sets*. Journal of Machine Learning Research, v. 7, p. 1–30, 2006. Recomenda o
Wilcoxon signed-ranks para dois classificadores. Ressalva: trata de comparação de
classificadores em múltiplos conjuntos de dados.

**1.3 Wilcoxon (1945).** *Individual Comparisons by Ranking Methods*. Biometrics
Bulletin, v. 1, n. 6, p. 80–83, 1945. DOI 10.2307/3001968. É a publicação
original do teste.

**1.4 Kaufman et al. — o ano está errado.** Os dados corretos: Shachar Kaufman,
Saharon Rosset e Claudia Perlich, *Leakage in Data Mining: Formulation,
Detection, and Avoidance*, **KDD '11, p. 556–563, 2011**, DOI
10.1145/2020408.2020496. A chamada deve passar a `(KAUFMAN; ROSSET; PERLICH,
2011)`.

**1.5 Sommer e Paxson (2010).** *Outside the Closed World: On Using Machine
Learning for Network Intrusion Detection*. IEEE Symposium on Security and
Privacy, 2010. Ressalva: o artigo trata de limitações de generalização e da
distância entre ambiente experimental e operacional — **não atribuir aos autores
uma afirmação específica sobre dados sintéticos sem conferir o trecho**.

### 2. Pendências adicionais da metodologia

**2.1 NIST SP 800-92 — correlação de eventos: confirmada.** A seção 3.2 do
documento explica que a forma mais comum de correlação de eventos é a baseada em
regras; a seção 5.2.2 apresenta a frequência de eventos como critério de
priorização. Redação sugerida:

> A contagem de falhas de autenticação em uma janela temporal fixa constitui uma
> aplicação de regras de correlação baseadas na frequência dos registros,
> abordagem compatível com as práticas de gerenciamento e análise de logs
> descritas por Kent e Souppaya (2006).

**Atenção: os dois minutos são decisão do projeto, não recomendação do NIST.**

**2.2 Detecção trivial por regras fixas: resolvida por reformulação.** A
explicação atual da seção 3.3 já resolve — como a C0 tem a regra, o
reconhecimento não pode ser atribuído às dimensões adicionais. É consequência
lógica do desenho, não afirmação que exija fonte externa. **Retirar da lista.**

### 3. Lei nº 13.709/2018 — dados oficiais confirmados

| Campo | Informação |
|---|---|
| Assinatura | 14/08/2018 |
| Publicação | 15/08/2018 |
| Veículo | Diário Oficial da União, seção 1, p. 59 |

Entrada recomendada:

> BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Dispõe sobre a proteção de
> dados pessoais e altera a Lei nº 12.965, de 23 de abril de 2014 (Marco Civil da
> Internet). Diário Oficial da União: seção 1, Brasília, DF, p. 59, 15 ago. 2018.

Ressalva de conteúdo: como o protótipo usa dados fictícios, a LGPD deve ser
contextualizada como requisito de uma eventual implantação com dados reais.

### 4. Os quatro exemplos reais da Introdução

**4.1 Target — confirmada com ressalva de ano.** Riley, Elgin, Lawrence e
Matlack, *Missed Alarms and 40 Million Stolen Credit Card Numbers: How Target
Blew It*, Bloomberg Businessweek, 13 mar. **2014**. O evento é de 2013, a
publicação de 2014 — **a chamada deve ser (Riley et al., 2014)**. A página
original da Bloomberg não foi acessada; o relatório da audiência do Senado
norte-americano reproduz a referência e as informações, e serve como fonte
alternativa.

**4.2 General Electric / Zheng — confirmada.** U.S. Department of Justice,
*Niskayuna Man Charged With Theft of Trade Secrets*, 1º ago. 2018, U.S.
Attorney's Office, Northern District of New York. Confirma a acusação de uso de
esteganografia para ocultar segredos comerciais numa imagem. **Ressalva: é
comunicado de acusação — o texto deve dizer que era alegação.**

**4.3 Capital One — confirmada, fonte complementada.** U.S. Department of
Justice, *Seattle Tech Worker Arrested for Data Theft Involving Large Financial
Services Company*, 29 jul. 2019, Western District of Washington. Confirma a
configuração incorreta de um firewall de aplicação web. **Substituir a URL
genérica `usao-wdwa` por esta referência.** Sobre o número de afetados, a própria
Capital One divulgou ~100 milhões nos EUA e 6 milhões no Canadá.

**4.4 Tesla / Tripp — fonte primária localizada.** *Tesla, Inc. v. Martin Tripp —
Complaint*, United States District Court, District of Nevada, protocolo de 20
jun. 2018. Usar a petição inicial em vez do artigo secundário. **Ressalva
jurídica: a petição são as alegações da Tesla, não comprovação.**

### 5. Pendências da documentação

**5.1 Nielsen e Landauer (1993).** *A Mathematical Model of the Finding of
Usability Problems*, CHI '93, p. 206–213. O modelo é `P(n) = N[1 − (1 − L)^n]`, e
31% é a taxa típica de descoberta por participante. **Ajuste necessário: não
escrever que os autores estabeleceram cinco participantes como regra** — o estudo
oferece um modelo, e cinco é escolha de planejamento. E o modelo **não** é
justificativa estatística para o tamanho de amostra de um experimento
quantitativo.

**5.2 Bangor, Kortum e Miller (2009).** *Determining What Individual SUS Scores
Mean*, Journal of Usability Studies, v. 4, n. 3, p. 114–123. Os autores
apresentam **médias e desvios-padrão** por classificação adjetiva, **não limites
matemáticos rígidos entre faixas**. A média geral da amostra deles é **69,5**, e
não 68.

| Classificação | Média SUS | Desvio-padrão |
|---|---|---|
| Worst Imaginable | 12,5 | 13,1 |
| Awful | 20,3 | 11,3 |
| Poor | 35,7 | 12,6 |
| OK | 50,9 | 13,8 |
| Good | 71,4 | 11,6 |
| Excellent | 85,5 | 10,4 |
| Best Imaginable | 90,9 | 13,4 |

**5.3 Fadiga de alertas em SOC — duas fontes.** Sundaramurthy et al. (2015),
*A Human Capital Model for Mitigating Security Analyst Burnout*, SOUPS 2015,
p. 347–359, fundamenta o esgotamento. E **Tariq et al. (2025)**, *Alert Fatigue in
Security Operations Centres*, ACM Computing Surveys, v. 57, n. 9, art. 224, DOI
10.1145/3723158, trata diretamente da fadiga de alertas.

**5.4 Shneiderman — 6ª edição, 2016.** *Designing the User Interface*, Pearson,
com Plaisant, Cohen, Jacobs, Elmqvist e Diakopoulos. Os dados estão adequados;
**falta o Filipe confirmar se foi essa a edição consultada**.

### 6. Correções consolidadas

| Referência | Alteração |
|---|---|
| KAUFMAN et al. (2012) | Corrigir para **KAUFMAN; ROSSET; PERLICH (2011)** |
| WOHLIN et al. (2012) | Conferir a edição na folha de rosto do exemplar |
| NIELSEN; LANDAUER (1993) | Acrescentar p. 206–213 |
| BANGOR; KORTUM; MILLER (2009) | Acrescentar p. 114–123 |
| Capital One | Substituir a URL genérica pelo comunicado oficial |
| Target | Usar **2014** como ano da publicação |
| LGPD | Incluir a referência normativa na lista |
| Fadiga de alertas | Acrescentar Tariq et al. (2025), após conferência humana |
| Shneiderman | Manter 6ª ed., 2016, se confirmada como a consultada |

### 7. Resultado geral

- **11** pendências analisadas
- **10** fontes identificadas com conteúdo compatível
- **1** afirmação que deve ser removida
- **3** pendências que exigem confirmação de exemplar ou assinatura humana

> *"A contagem distingue a identificação técnica da aprovação humana exigida
> pelas regras do repositório."*
