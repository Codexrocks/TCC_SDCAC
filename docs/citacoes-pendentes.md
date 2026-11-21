# Citações pendentes

Lista do que ainda precisa de fonte conferida. Uma linha por pendência, com o
lugar exato e o que falta.

Existe por uma razão prática e uma técnica.

**A prática:** modelo de linguagem inventa referência plausível — autor real,
revista real, ano real, artigo que não existe. As
[diretrizes institucionais](diretrizes.md) vedam expressamente *"qualquer forma
de plágio, cópia indevida ou fraude acadêmica"*, e referência fabricada cai
nessa cláusula. Anotar a dívida é o que a mantém visível até alguém pagá-la.

**A técnica:** dentro de `artigo/` não dá para anotar no lugar. O GitBook apaga
comentário HTML ao salvar, e em 06/09/2026 ele exportou os seis arquivos do
artigo com todos os marcadores apagados — a dívida sumiu sem ninguém perceber.
As páginas de `docs/` não têm esse problema, porque o GitBook só lê daqui.

> **Regra:** `FALTA CITAÇÃO` dentro de `artigo/` reprova na validação. A
> pendência do artigo se registra **aqui**.

***

## Pendentes — artigo

> **As três linhas que estavam aqui saíram em 13/10/2026**, e saíram pelo mesmo
> fato: as três apontavam para obras que **já estavam entre as 13 do
> referencial**.
>
> | Linha que saiu | Por quê |
> |---|---|
> | ISO 2022, no referencial § 2.1 | É `INTERNATIONAL ORGANIZATION FOR STANDARDIZATION, 2022`, uma das 13 |
> | NIST 2006, na Introdução | É a **mesma obra** que `KENT; SOUPPAYA, 2006` — a NIST SP 800-92. A suspeita estava registrada aqui desde 26/09 e se confirmou. A chamada da Introdução passou a `(Kent e Souppaya, 2006)`, que é o que a ABNT pede quando a obra tem autor pessoal |
> | Chandola 2009, na Introdução | Mesma obra citada no referencial. Uma conferência resolveu as duas, como a linha previa |

**Duas entraram em 13/10/2026**, com a reescrita da seção 3.3 que a D-42
trouxe. Nenhuma das duas tem chamada: são afirmações soltas, e é por isso
que estão aqui e não na lista de referências.

| Onde | O que falta | Quem | Desde |
|---|---|---|---|
| `artigo/referencias.md` (entrada `SHASHANKA; SHEN; WAN`) e `artigo/04-resultados.md` § 4.2 (`Shashanka, Shen e Wan, 2016`) | **Erro de autor, não falta de fonte:** o terceiro autor é **Jisheng Wang**, e não "Wan". Fonte: [DBLP](https://dblp.org/rec/conf/bigdataconf/ShashankaSW16), consultada em 21/11/2026. Conferir na folha de rosto do artigo, corrigir os dois lugares e remontar o documento, porque a folga é de meia linha. A § 2.3 usa `et al.` e não muda | Davi | 21/11/2026 |

### 1 da Introdução — **aberta pelo assistente em 19/11/2026, por confirmar**

As orientações pedem referência de **até 5 anos no contexto**, e as duas
chamadas da § 1.1 eram de 2006 e 2009. Entrou uma de 2022. **O assistente de IA
abriu o PDF dos anais** e conferiu título, autores, evento, páginas 2783 a 2800
e a frase do resumo que sustenta o texto — *"most are attributed to benign
triggers"*. Falta a segunda etapa do arranjo de 17/11: **uma pessoa conferir e
confirmar**.

| Onde | O que falta | Quem | Desde |
|---|---|---|---|
| `01-introducao.md` § 1.1 e [`usabilidade.md`](usabilidade.md) § 7 — **Alahmadi et al., 2022** | Abrir <https://www.usenix.org/system/files/sec22-alahmadi.pdf>, ler o resumo e confirmar que a frase da Introdução diz o que ele diz | Davi | 19/11/2026 |

### As 4 dos exemplos reais — **entregues em 10/11/2026, por conferir**

O insumo [exemplos reais](insumos/exemplos-reais-yasmin-v1.md) traz quatro casos
para a Introdução, com fonte. **O rascunho foi produzido integralmente por IA**
(Claude Sonnet 5), e o cabeçalho do arquivo declara "Conferi tudo que a IA
escreveu? **Sim**" — enquanto o `README.md` do pacote entregue dizia que nenhum
arquivo havia sido conferido. **As duas não podem valer juntas**, e é o campo que
decide se as referências podem entrar.

Até isso ficar resolvido, nenhuma delas vai ao artigo. O `AGENTS.md` seção 3 é
explícito: referência que a IA produziu e ninguém conferiu na fonte **não entra**.

| Onde | O que falta | Quem | Desde |
|---|---|---|---|
| `01-introducao.md` — caso **Target, 2013** | Confirmar na fonte: RILEY; ELGIN; LAWRENCE; MATLACK, *Bloomberg Businessweek*, 13 mar. 2014. Abrir o artigo e conferir que ele sustenta o que o texto afirma | Yasmin | 10/11/2026 |
| `01-introducao.md` — caso **GE / Zheng, 2018** | Confirmar na fonte: U.S. DOJ, *Niskayuna man charged theft trade secrets*, 2018. Abrir o *press release* e conferir autor, data e conteúdo | Yasmin | 10/11/2026 |
| `01-introducao.md` — caso **Capital One, 2019** | Confirmar na fonte: U.S. DOJ, `usao-wdwa`. **O próprio insumo admite estar incompleto** — *"conferir o número exato"* —, com URL genérica e sem o documento | Yasmin | 10/11/2026 |
| `01-introducao.md` — caso **Tesla / Tripp, 2018** | Confirmar na fonte: petição inicial *Tesla, Inc. v. Martin Tripp* (Nevada) **ou** *GovInfoSecurity*, 2018. São duas fontes para o mesmo caso, e a petição não tem link: decidir qual sustenta a afirmação | Yasmin | 10/11/2026 |

> ✅ **As quatro estão vencidas desde 17/11/2026, e não por conferência: os
> quatro casos não estão mais no artigo.** Foi conferido arquivo por arquivo —
> `Target`, `Capital One`, `Tesla`, `Zheng`, `General Electric`, `Bloomberg` e
> `DOJ` **não aparecem em nenhum dos cinco arquivos de `artigo/`**. Saíram no
> resumo da Introdução, e as quatro linhas continuaram aqui como dívida de um
> texto que já não existia.
>
> **A tabela acima fica, e fica vencida de propósito.** Se algum dos casos voltar
> à Introdução, a linha volta a valer exatamente como está — inclusive a
> contradição do campo *"Conferi tudo que a IA escreveu"*, que é o que impedia as
> quatro de entrarem e continua impedindo.

***

### As 13 do referencial teórico — **conferidas em 13/10/2026**

> **A Yasmin declarou ter conferido cada uma na fonte**, e o **Davi confirmou a
> declaração**. As 13 entraram em
> [`artigo/referencias.md`](../artigo/referencias.md), em ABNT NBR 6023.
>
> **O que a IA fez e o que a IA não fez.** A conversão de formato — do autor-ano
> do COBEM, como estava no
> [insumo de 28/09](insumos/referencial-teorico-yasmin-v2.md), para a NBR 6023 —
> foi assistida por IA, e cada dado veio do insumo. **A conferência na fonte não
> foi feita por IA, e não poderia ser:** quem abre a fonte é quem assume a
> referência.
>
> Ficou uma divergência de **paginação**, não de existência: o insumo registra
> `Article 15` para Chandola, Banerjee e Kumar (2009), e o `.docx` entregue ao
> professor registra `pp. 1–58`. Está anotada em
> [`referencias.md`](../artigo/referencias.md) para o Davi fechar.

### As 7 da metodologia

> 📦 **Uma auditoria de IA identificou as obras em 12/11/2026**, e está em
> [insumos](insumos/auditoria-citacoes-ia-v1.md). **Ela não fecha nenhuma destas
> linhas** — o `AGENTS.md` seção 3 veda referência que a IA produziu e ninguém
> conferiu na fonte, e a própria auditoria recusou assinar pela equipe.
>
> **O que ela faz é encurtar a conferência:** cada obra está nomeada com veículo,
> volume, páginas e DOI, e em vários casos com o trecho que sustenta a afirmação.
> Conferir passou de "procurar a obra" para "abrir este documento e checar o
> trecho".
>
> ⚠️ **Três apontamentos dela mudam o que o artigo afirma**, e nenhum foi
> aplicado:
>
> | Chamada | O que a auditoria aponta |
> |---|---|
> | `(KAUFMAN et al., 2012)` | O ano seria **2011** — a publicação é do KDD '11, com DOI 10.1145/2020408.2020496 |
> | `(SOMMER; PAXSON, 2010)` | O artigo trata de **generalização** e da distância entre ambiente experimental e operacional — **não** especificamente de dado sintético, que é o que a § 3.8 lhe atribui |
> | `(WOHLIN et al., 2012)` | O ano confere, mas a **edição é divergente** entre registros: não inserir o número sem conferir a folha de rosto do exemplar usado |
>
> O segundo é o mais sério, e é do tipo que a validação automática não pega: a
> obra existe, está citada, e **o que o texto afirma não é o que ela diz**.
>
> ⚠️ **E a entrada criada em 17/11/2026 não resolve nenhum dos três.** Entrada na
> lista de referências responde *"a obra existe e está identificada"*. Os
> apontamentos acima são de outra ordem:
>
> | Apontamento | O que a conferência de 17/11 resolveu |
> |---|---|
> | `KAUFMAN et al.` — o ano seria 2011 | **Resolvido.** Existem as duas publicações: o artigo do KDD '11 e o da **ACM TKDD, v. 6, n. 4, art. 15, dez. 2012**. A entrada é da segunda, e o ano de 2012 do texto está certo |
> | `WOHLIN et al.` — edição divergente | **Metade.** A edição de 2012 da Springer existe, revisão da original de 2000, que era da Kluwer. A entrada entrou **sem número de edição**, como a auditoria recomendou. Qual das duas foi lida, só o Davi diz |
> | `SOMMER; PAXSON` — o texto afirma o que a obra não diz | ✅ **Resolvido em 17/11/2026, e pelo único caminho possível: lendo o artigo.** A § 3.8 foi reescrita para dizer o que a obra diz, e a inferência que era nossa ficou onde não precisa de fonte — a § 4.6, sem chamada |

Situação diferente, e mais exigente. O
[insumo entregue pelo Davi](insumos/metodologia-davi-v1.md) em 28/09 declara, no
próprio cabeçalho, que a redação foi **rascunhada por IA** e que **nenhuma das
sete citações foi conferida na fonte**.

> O [`AGENTS.md`](../AGENTS.md), seção 3, é categórico: *"referência
> bibliográfica que a IA produziu e ninguém conferiu na fonte"* está entre o que
> **nunca é aceitável**. Por isso as sete estão aqui, e não em
> [`referencias.md`](../artigo/referencias.md) — e o capítulo avisa disso no
> cabeçalho, à vista de quem for escrever.

> 🔄 **A ordem se inverteu em 17/11/2026, e vale saber por quê.** A instrução
> aqui era *"ao conferir, apague a linha e acrescente a referência na `## Lista`"*
> — primeiro a conferência, depois a entrada. **As sete entradas foram inseridas
> antes**, porque a falta delas tinha um custo imediato e visível: o artigo citava
> sete obras que não apareciam na lista de referências, e é a última página que
> uma banca abre para procurar uma delas.
>
> **A fonte de cada uma foi aberta pelo assistente de IA em 17/11**, e os dados de
> publicação vêm de lá. Isso **não** fecha estas linhas: o `AGENTS.md` seção 3
> veda referência que a IA produziu e ninguém conferiu, e máquina abrindo a fonte
> não é pessoa assumindo a referência. O que mudou é a natureza da dívida —
> de **chamada sem referência** para **referência a confirmar**, que é o mesmo
> estado em que as 13 do referencial estiveram entre a conversão e a confirmação
> do Davi.
>
> **Ao confirmar, apague a linha.** A entrada já está na `## Lista`.

> ✅ **As sete fecharam em 17/11/2026.** O Davi conferiu campo por campo e
> confirmou, no pedido *"confirmo"*. As linhas saíram da fila, como esta página
> manda fazer ao confirmar.
>
> | Entrada | Conferida contra | |
> |---|---|---|
> | `BRASIL.` Lei nº 13.709/2018 | Planalto — número, data e ementa | ✅ |
> | `DEMŠAR, 2006` | Página do JMLR — `7(1):1−30, 2006` | ✅ sem o fascículo, que a NBR admite |
> | `KAUFMAN et al., 2012` | DOI `10.1145/2382577.2382579`, ACM TKDD, dez. 2012 | ✅ e **o de 2011 é o do KDD, outra publicação** |
> | `SOMMER; PAXSON, 2010` | DOI `10.1109/SP.2010.25` **e o artigo lido** | ✅ dados **e** conteúdo |
> | `WILCOXON, 1945` | DOI `10.2307/3001968` | ✅ |
> | `WOHLIN et al., 2012` | Springer, DOI `10.1007/978-3-642-29044-2` | ✅ **o Davi leu a de 2012** |
> | `WORLD WIDE WEB CONSORTIUM`, WCAG 2.2 | w3.org — *W3C Recommendation, 12 dez. 2024*; critérios 1.4.1 e 1.4.3, 4,5:1 | ✅ e confirma o que a § 4.4 afirma |
>
> **A divisão de trabalho fica registrada, porque é a pergunta da banca:** a
> máquina abriu a fonte e montou a entrada em ABNT; **a pessoa conferiu e
> assinou.** Nenhuma das sete entrou sob a palavra da IA.


> ✅ **A § 3.8 foi corrigida em 17/11/2026, e o caminho fica registrado porque é
> o que a banca vai perguntar.** O artigo de Sommer e Paxson foi aberto e lido —
> a seção *Difficulties with Evaluation*, que é onde o assunto está. O que ele
> sustenta:
>
> - *"Evaluating an anomaly detection system that strives to find novel attacks
>   using only simulated activity will often lack any plausible degree of realism
>   or relevance"*
> - *"Conclusions drawn from analyzing a small environment cannot be generalized
>   to settings of larger scale"*
> - e a exigência de *"acknowledge shortcomings that one's evaluation dataset
>   might impose"*
>
> **O que ele não sustenta** é a frase que estava na § 3.8: que acurácia elevada
> sobre dado sintético indique **gerador previsível**. Isso é inferência nossa, e
> a obra não a faz.
>
> A § 3.8 passou a citá-los pelo que afirmam. **A inferência não foi apagada** —
> ela já estava na § 4.6, *"acurácia alta sobre dado sintético pode indicar
> gerador previsível em vez de modelo bom"*, **sem chamada bibliográfica**, que é
> o lugar certo de uma leitura que é do trabalho e não da fonte.


| Chamada, como está no texto | Onde | O que sustenta | Quem | Desde |
|---|---|---|---|---|

> **Duas baixas em 12/11/2026, e não por conferência.** As chamadas
> `(DAVIS; GOADRICH, 2006)` e `(SAITO; REHMSMEIER, 2015)` sustentavam uma
> contingência da § 3.6 — comparar curvas de precisão-revocação completas caso a
> linha de base não alcançasse a revocação de referência. **A contingência não se
> materializou:** a C0 alcança todos os níveis, e a FPR de 100% com que o faz é o
> próprio resultado, como a § 4.3.1 reporta. Ao resumir a Metodologia para caber
> no teto de 12 páginas, a contingência saiu e as duas chamadas com ela.
>
> **Isto não as declara conferidas.** Se a comparação por curva voltar ao texto,
> as duas voltam para esta fila como estavam.

> ✅ **Mais duas baixas no mesmo dia, e estas porque a frase saiu do artigo.**
> As afirmações
> *"forma usual de regra de correlação em ferramentas de gestão de eventos de
> segurança"* e *"trivial para regras fixas"* **não estão mais na § 3.3** — elas
> saíram no resumo da Metodologia, junto com o parágrafo que as continha. O que a
> seção diz hoje é só a consequência do desenho: como a C0 tem a regra da janela
> de dois minutos, o reconhecimento de tentativas sucessivas não pode ser
> atribuído como ganho às dimensões.
>
> **Não é baixa por conferência.** Se qualquer uma das duas frases voltar ao
> texto, as duas pendências voltam a esta fila como estavam. A primeira tinha a
> `KENT; SOUPPAYA, 2006` como candidata, e aquela obra **continua na fila do
> referencial** por outro motivo.
>
> A [auditoria de 12/11](insumos/auditoria-citacoes-ia-v1.md) chegou à mesma
> conclusão sobre a segunda, por outro caminho — *"é consequência lógica do
> desenho experimental, não uma afirmação que exige fundamentação externa"*. É
> corroboração, e não o motivo: o motivo é o texto não estar mais lá.

> **A `SOMMER; PAXSON, 2010` já era conhecida do repositório:** ela aparece no
> [plano](plano.md), seção 4, como apoio ao risco de dados sintéticos fáceis
> demais, e o insumo da Yasmin a descartou do referencial por já estar citada
> ali. **Uma conferência resolve os dois usos.**

## Pendentes — documentação

Estas ficam marcadas **na própria linha**, com `<!-- FALTA CITAÇÃO -->`. O
comentário é invisível no site publicado e sobrevive, porque o GitBook não
escreve em `docs/`.

| Onde | O que falta | Quem | Desde |
|---|---|---|---|
| [`usabilidade.md`](usabilidade.md) § 6.2 | Formulação exata e porcentagem de Nielsen e Landauer | Filipe | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 6.3 | Limites exatos de cada faixa adjetiva do SUS, em Bangor, Kortum e Miller (2009) | Filipe | 03/09/2026 |
| [`usabilidade.md`](usabilidade.md) § 9 | Edição e ano da obra de Shneiderman efetivamente consultada | Filipe | 03/09/2026 |

***

## Como usar

**Ao escrever e precisar de uma fonte que você ainda não abriu:** acrescente uma
linha na tabela do artigo. Escreva o capítulo, a seção e o que falta — "falta
citação" sozinho não ajuda ninguém daqui a dois meses.

**Ao conferir a fonte:** apague a linha daqui e acrescente a referência em
[`artigo/referencias.md`](../artigo/referencias.md).

**Nunca:** apagar a linha sem ter aberto a fonte. É o único jeito de esta página
mentir, e ela só serve enquanto for verdadeira.

## Antes de entregar

Esta tabela precisa estar **vazia** — as duas. Página com pendência aberta é
seção que ainda não pode ser entregue.

**Situação em 13/10/2026:** das 27 pendências de 28/09 restam **11** — as **7 da
metodologia** e as **4 da documentação**. As 13 do referencial e as 3 do artigo
saíram juntas, porque as 3 apontavam para obras entre as 13.

As 7 da metodologia são o que ainda impede a entrega de 18/10: a § 3.6, a § 3.7 e
a § 3.8 têm chamada no texto **sem entrada na lista**, e a página de referências
diz isso por escrito em vez de fingir que está completa.
