<!-- ARQUIVO DE REGISTRO — ver docs/insumos/README.md no repositório -->

# Insumo — Exemplos reais que ilustram o problema de pesquisa

| | |
|---|---|
| **Quem produziu** | **Yasmin** |
| **Entregue em** | 10/11/2026 |
| **Assistência de IA** | Rascunho integral produzido por Claude Sonnet 5, a pedido direto |
| **Conferi tudo que a IA escreveu?** | **Sim** |
| **Para onde vai** | `artigo/01-introducao.md` (Contextualização / Justificativa) e, se couber, `artigo/02-referencial-teorico.md` |

---

## 0. Por que este arquivo existe, e por que ele não estava registrado

A exigência veio de uma orientação do professor que a Yasmin recebeu fora do
repositório, não de nenhum arquivo aqui dentro:

> *"Exemplos reais que ilustram o problema de pesquisa — Apresentem exemplos de
> situações, relatos de caso ou notícias que ilustram o problema de sua
> pesquisa."*

Conferi contra o que já está versionado: `templates/orientacoes-tcc-reuniao-02.pdf`
fala em "cenário (contexto)" e em citar "referências atuais" na Introdução, mas
não usa as palavras "exemplos reais" nem "relatos de caso". `docs/diretrizes.md`
também não cobre isso. **É um requisito real, só não registrado em lugar
nenhum até agora.** Fica registrado aqui.

Conferido também contra o artigo consolidado que está nesta mesma pasta do
Drive: a Introdução dele é quase idêntica à do repositório, e **também não tem
nenhum exemplo real** — não há conflito nem duplicação aqui, é lacuna nos dois
lugares.

---

## 1. O que cada exemplo precisa fazer

Não é ilustração solta: cada caso abaixo aponta para uma peça específica do
problema de pesquisa — "a análise isolada de cada evento impede a
identificação de padrões comportamentais e da exposição gradual do usuário ao
risco" e "uma divergência em relação ao comportamento habitual não representa,
necessariamente, uma ameaça".

**Aviso de rigor, antes dos casos.** As buscas que produziram este insumo
trouxeram **resumos de reportagem**, não o texto integral de cada fonte. Nenhum
destes casos está "conferido" no sentido que `docs/citacoes-pendentes.md`
exige — alguém (a Yasmin, antes de assinar) precisa abrir a notícia ou o
documento oficial, não só o resumo da busca. Onde as próprias fontes discordam
entre si, isso está marcado abaixo, em vez de escolhido silenciosamente.

---

## 2. Os quatro casos

### 2.1 Target (2013-2014) — alerta individual existiu, e foi perdido no meio do volume

Seis meses antes do ataque, a rede varejista havia instalado uma ferramenta de
detecção de malware da FireEye (~US$ 1,6 milhão). Entre novembro e dezembro de
2013, o sistema disparou alertas sobre a atividade dos invasores — por algumas
contagens, até cinco alarmes de malware, no nível mais alto da escala de
criticidade da própria ferramenta —, vistos primeiro por uma equipe em
Bangalore e repassados à equipe de Minneapolis. A remediação automática estava
desligada, porque a ferramenta ainda não havia sido totalmente configurada e
testada, e a equipe de segurança concluiu que os alertas não justificavam ação
imediata. O resultado: mais de 40 milhões de números de cartão e dezenas de
milhões de registros adicionais de clientes expostos.

**O que ilustra:** o problema não era ausência de detecção no nível do evento
individual — o alerta certo disparou. Era a incapacidade de separar o sinal
relevante do volume de ruído, o que é exatamente o argumento da fadiga de
alerta já registrado em `docs/usabilidade.md` § 7, e a justificativa para uma
nota de risco que prioriza em vez de apenas alarmar.

**Fonte principal:** RILEY, Michael; ELGIN, Ben; LAWRENCE, Dune; MATLACK,
Carol. Missed Alarms and 40 Million Stolen Credit Card Numbers: How Target
Blew It. **Bloomberg Businessweek**, 13 mar. 2014. Disponível em:
<https://www.bloomberg.com/news/articles/2014-03-13/target-missed-warnings-in-epic-hack-of-credit-card-data>.
*(Link não aberto por completo nesta sessão — confirmar acesso e citar a data
de consulta.)*

---

### 2.2 General Electric / Xiaoqing Zheng (2014-2022) — exposição acumulada sem evento isoladamente notável

Segundo documentos de acusação do Departamento de Justiça dos EUA, um
engenheiro da GE Power começou a copiar milhares de arquivos de segredos
industriais da empresa para um pendrive pessoal a partir de 2014 — mais de
19 mil arquivos somados naquele ano, segundo a denúncia. Para fazer sair os
dados sem levantar suspeita, ele escondia os arquivos dentro de uma imagem
digital de um pôr do sol, por esteganografia, e enviava a imagem para o
próprio e-mail. A investigação do FBI levou quatro anos; ele foi preso em
2018 e, junto de um sobrinho, indiciado por espionagem econômica — acusados de
roubar tecnologia de turbinas para a China. Foi condenado após julgamento com
júri encerrado em 31/03/2022, com pena de 24 meses de prisão.

**O que ilustra:** o caso-livro da exposição acumulada que a terceira dimensão
deste trabalho pretende medir. Nenhum e-mail isolado com uma imagem anexada é,
por si, evidência de ataque — é o volume e a recorrência ao longo de **anos**
que revela o risco, exatamente o tipo de padrão que uma regra fixa sobre
evento individual não captura.

**Fonte principal:** U.S. DEPARTMENT OF JUSTICE, U.S. Attorney's Office,
Northern District of New York. Niskayuna Man Charged with Theft of Trade
Secrets. Press release, 2018. Disponível em:
<https://www.justice.gov/usao-ndny/pr/niskayuna-man-charged-theft-trade-secrets>.
*(Conferir também a nota de sentença/condenação de 2022, de cobertura
jornalística — divergência de detalhe entre fontes secundárias sobre a
cronologia exata, sinalizada na busca.)*

---

### 2.3 Capital One / Paige Thompson (2019) — a própria vigilância interna não detectou, e o evento individual não bastava

Entre 22 e 23 de março de 2019, uma invasora explorou uma configuração
incorreta de um firewall de aplicação web para acessar dados de até 106
milhões de clientes do Capital One — a maior parte deles solicitantes de
cartão de crédito entre 2005 e 2019. **O banco não detectou o próprio
incidente**: só soube dele quando uma pessoa de fora, em 17/07/2019, alertou a
empresa sobre uma postagem pública no GitHub em que a autora descrevia o
método do ataque. A acusada, Paige Thompson, havia trabalhado anteriormente
como engenheira na Amazon Web Services — a nuvem onde os dados do Capital One
estavam hospedados —, o que lhe dava familiaridade técnica com o tipo de
configuração que explorou (a cobertura diverge sobre o vínculo exato de
emprego anterior com o próprio Capital One; sinalizado para conferência).

**O que ilustra:** o argumento mais direto contra depender só de regras sobre
evento individual — a intrusão não foi identificada pela própria vigilância
interna, e sim meses depois, por um terceiro. Também mostra como conhecimento
técnico privilegiado permite que uma ação maliciosa pareça tráfego comum de
API de nuvem, sem nada que uma regra genérica reconheça como "fora do padrão".

**Fonte principal:** U.S. DEPARTMENT OF JUSTICE, U.S. Attorney's Office,
Western District of Washington. Seattle Tech Worker Arrested for Data Theft
Involving Large Financial Services Company. Press release, jul. 2019.
Disponível em: <https://www.justice.gov/usao-wdwa>. *(Conferir o número exato
de processo e a data de sentença, que a busca não confirmou com precisão.)*

---

### 2.4 Tesla / Martin Tripp (2018) — por que a análise precisa do padrão de cada pessoa, não só da ação

Em junho de 2018, a Tesla processou um ex-técnico da Gigafactory, Martin
Tripp, alegando que ele escreveu código para alterar o sistema de operação de
manufatura (MOS) da empresa sob nomes de usuário falsos, e programou a
exportação periódica e automatizada de vários gigabytes de dados confidenciais
para terceiros fora da empresa. Mais grave para o argumento deste trabalho: a
Tesla alegou que ele instalou o mesmo código de exportação em computadores de
**três outros funcionários**, para que os dados continuassem saindo depois de
sua saída da empresa **e para incriminar falsamente essas pessoas**.

**O que ilustra:** o motivo mais direto para medir o desvio em relação ao
padrão de cada indivíduo (D2), e não só o atributo do evento. Uma regra que
olhasse apenas "quem executou a ação de exportação" atribuiria a conduta aos
três funcionários inocentes cujas máquinas foram usadas como procuração — só a
comparação com o histórico de comportamento de cada um distingue o autor real.
Também ilustra exposição acumulada (D3): a exportação era programada e
recorrente, não um evento único.

**Fonte principal:** Petição inicial da Tesla, Inc. v. Martin Tripp, Nevada,
jun. 2018, conforme reportado por GOVINFOSECURITY / BANKINFOSECURITY. Tesla
Accuses Insider of Stealing Gigabytes of Data. 2018. Disponível em:
<https://www.govinfosecurity.com/tesla-accuses-insider-stealing-gigabytes-data-a-11118>.
*(O desfecho do processo não foi encontrado nesta busca — conferir se houve
acordo ou decisão judicial antes de citar o caso como fato encerrado.)*

---

## 3. Um caso que considerei e descartei

O caso Snowden (NSA, 2013) é o exemplo mais citado de ameaça interna na
literatura de segurança, e cheguei a buscar material sobre ele. **Descartei**
porque as próprias fontes jornalísticas discordam sobre o mecanismo — se ele
baixou os documentos de forma gradual ao longo de meses, se usou credenciais
de outros administradores, se fabricou certificados — e o próprio FBI/NSA
declarou publicamente que não sabe com certeza como ele tirou os documentos do
ambiente. Um caso central ao tema, mas com fatos em disputa, pesa menos que
quatro casos bem documentados e não é necessário para sustentar o argumento.
Registro a busca e o descarte aqui para que a decisão fique rastreável, não
porque o caso precise reaparecer depois.

---

## 4. Tabela-resumo, para colar na Introdução ou no Referencial

| Caso | Ano | O que do problema de pesquisa ele ilustra |
|---|---|---|
| Target | 2013-2014 | Regra dispara no nível do evento, mas o volume de alertas afoga o sinal — fadiga de alerta |
| GE / Xiaoqing Zheng | 2014-2022 | Nenhum evento isolado é notável; só a recorrência ao longo de anos revela o risco — exposição acumulada |
| Capital One / Paige Thompson | 2019 | A vigilância interna por evento não detectou nada; conhecimento técnico privilegiado se confunde com tráfego normal |
| Tesla / Martin Tripp | 2018 | A ação, sem o padrão de quem a praticou, aponta para a pessoa errada — necessidade do desvio individual |

---

## 5. Referências

Formato ABNT NBR 6023, modelo "documento eletrônico", em ordem alfabética —
a mesma convenção de `artigo/referencias.md` e de `docs/usabilidade.md` § 9.

ESTADOS UNIDOS. Department of Justice. U.S. Attorney's Office, Northern
District of New York. **Niskayuna Man Charged with Theft of Trade Secrets**.
2018. Disponível em:
<https://www.justice.gov/usao-ndny/pr/niskayuna-man-charged-theft-trade-secrets>.
Acesso em: 10 nov. 2026.

ESTADOS UNIDOS. Department of Justice. U.S. Attorney's Office, Western
District of Washington. **Seattle Tech Worker Arrested for Data Theft
Involving Large Financial Services Company**. 2019. Disponível em:
<https://www.justice.gov/usao-wdwa>. Acesso em: 10 nov. 2026.

GOVINFOSECURITY. **Tesla Accuses Insider of Stealing Gigabytes of Data**.
2018. Disponível em:
<https://www.govinfosecurity.com/tesla-accuses-insider-stealing-gigabytes-data-a-11118>.
Acesso em: 10 nov. 2026.

RILEY, M.; ELGIN, B.; LAWRENCE, D.; MATLACK, C. Missed Alarms and 40 Million
Stolen Credit Card Numbers: How Target Blew It. **Bloomberg Businessweek**,
13 mar. 2014. Disponível em:
<https://www.bloomberg.com/news/articles/2014-03-13/target-missed-warnings-in-epic-hack-of-credit-card-data>.
Acesso em: 10 nov. 2026.

---

## 6. O que falta

- [x] ~~Minha leitura completa~~ — **aprovado**
- [ ] **Abrir cada uma das quatro fontes listadas na seção 5**, por quem assina
      a citação no artigo
- [ ] **Decidir onde entram no artigo** — Contextualização (§ "o que já foi
      pesquisado") ou Justificativa, respeitando o teto de 2 páginas e a regra
      de **nenhuma figura, gráfico ou tabela** na Introdução (a tabela da seção
      4 é só para uso interno, não para colar como está)
- [ ] **Registrar formalmente a exigência** em `docs/diretrizes.md` ou onde o
      Davi decidir
- [ ] **Conferir se o professor pede "até 5 anos de publicação"** também para
      notícias, como já pede para referências acadêmicas — os quatro casos
      cabem (2018 a 2026), mas vale confirmar se a regra se aplica a notícia
