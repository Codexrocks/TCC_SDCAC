# Registro de decisões

Toda decisão de escopo, arquitetura ou processo entra aqui, com data, dono e
status. **Uma decisão só existe quando está registrada.**

Este registro é o Anexo A do [plano](plano.md), vivo. Enquanto uma decisão
estiver aberta, o plano descreve a *proposta*, não o combinado.

## O que entra aqui, e o que não entra

| Natureza | Onde vive | Fecha com |
|---|---|---|
| **Decisão** — uma escolha a fazer | Esta página | Uma escolha registrada, que continua legível |
| **Tarefa** — algo a executar | Issue no GitHub | Um commit |
| **Prazo** — quando cada coisa acontece | [Cronograma](cronograma.md) | A semana passar |

Decisão não vira issue. O valor de uma decisão é permanecer visível; issue
fechada fica enterrada.

---

## Abertas

| ID | Decisão | Proposta | Dono | Prazo |
|---|---|---|---|---|
| D-01 | Mudança de título | Adotar "Avaliação Multidimensional de Risco Comportamental"; atualizar README e comunicar ao orientador | Davi | Próxima reunião |
| D-02 | Dashboard: objetivo, instrumento ou fora do escopo | Instrumento de análise, descrito na Metodologia e na [arquitetura](arquitetura.md) | Davi + Filipe | 08/09 |
| D-06 | Cenários de contexto (B) e longitudinais (L) | Adotados; desenho detalhado na S5 | Yasmin | 01/10 |
| D-07 | Caneta rotativa por seção | Uma pessoa redige, duas revisam, a caneta gira | Os três | Ratificação na [issue #20](https://github.com/Codexrocks/TCC_SDCAC/issues/20) |
| D-09 | Pesos preliminares e análise de sensibilidade | Valores preliminares; sensibilidade na S12 | Yasmin | S8 |
| D-12 | Unidade de análise das métricas | Duas unidades declaradas separadamente: evento para os cenários pontuais, episódio para os de contexto e longitudinais | Davi + Filipe | 01/10 |
| D-13 | Tratamento estatístico dos resultados | 20 a 30 sementes, as mesmas nas quatro configurações; Wilcoxon pareado | Filipe | 01/10 |
| D-14 | O que fazer se a C0 não alcançar revocação 0,90 | Comparar curvas precisão-revocação, em vez de pontos únicos | Filipe | 01/10 |
| D-15 | Critério de relevância declarado a priori | Uma frase na Metodologia dizendo qual redução de FPR e qual revocação longitudinal contam como resposta afirmativa | Os três | 01/10 |
| D-16 | Controle negativo longitudinal | Acrescentar cenário de escalada legítima aos cenários de teste | Yasmin | 01/10 |
| D-17 | Janela de constituição do baseline da D2 | Janela de treino anterior e disjunta da janela de avaliação | Davi | 01/10 |
| D-18 | Dupla contagem e escala na integração | Excluir o evento atual da janela de exposição | Davi | 01/10 |
| D-19 | Vertente LGPD e ISO/IEC 27001 | Entra como limitação e trabalho futuro na S13 | Yasmin | 01/10 |
| D-20 | Sexto capítulo do artigo (`04-desenvolvimento`), proposto pelo plano | Não acrescentar. A estrutura de cinco seções é da instituição, e o [COBEM](cobem.md) limita o artigo inteiro a 6–10 páginas — um capítulo a mais agrava o orçamento de páginas em vez de resolvê-lo | Davi | Próxima reunião |

## Adotadas, a confirmar

| ID | Decisão | Confirmação |
|---|---|---|
| D-05 | Ablação em quatro configurações (C0 a C3) | M2 — 01/10 |
| D-10 | Isolation Forest como benchmark opcional | Cortável na S10, se as métricas estiverem em risco |

## Fechadas

| ID | Decisão | O que ficou | Data |
|---|---|---|---|
| D-03 | Operacionalização de "resultados diferentes" | FPR a revocação fixa **e** revocação longitudinal, com a **direção declarada** na pergunta. Precisão@k é secundária. Ver [plano, seção 1.3](plano.md) | 07/09/2026 |
| D-04 | Dono da Justificativa | Evidência de Yasmin e Filipe; tese e redação de Davi | 06/09/2026 |
| D-08 | SLA de resposta a Pull Request | 24 horas. PR sem resposta em 24 h é item obrigatório de pauta | 06/09/2026 |
| D-11 | Formato do artigo: ABNT ou template de evento | **COBEM** — template da ABCM, versionado em [`templates/`](../templates/README.md). Corrige o registro de 04/09, que dizia ABNT. Ver [COBEM](cobem.md) | 07/09/2026 |
| D-21 | Idioma do artigo | Texto inteiro em **português**; só o *abstract* e as *keywords* em inglês. O template pede inglês, mas quem define para o TCC é a coordenação | 07/09/2026 |

---

## Detalhamento — as lacunas metodológicas

D-12 a D-19 vêm de uma revisão crítica do plano feita em 06/09. Nenhuma delas
muda o texto da Introdução; **todas** mudam o que a S12 conseguirá afirmar. Por
isso vencem em M2, quando a metodologia congela.

### D-12 · Unidade de análise

A mesma detecção rende números opostos conforme a unidade escolhida. Tome o
cenário longitudinal L1 — dez dias, dezenas de eventos, nenhum acima de 50
pontos, a D3 dispara no dia 8:

```text
POR EVENTO
  Quais dos ~40 eventos são "anomalous"? Todos? Só os dos dias 8 a 10?
  C0: 0 de 40        C3: talvez 6 de 40   →   revocação ≈ 0,15
  O número parece péssimo, e o sistema fez exatamente o que devia.

POR EPISÓDIO (par usuário × cenário)
  L1 é UM episódio, detectado ou não.
  C0: 0 de 1         C3: 1 de 1           →   0,00 contra 1,00
  O número descreve o que aconteceu.
```

O falso positivo precisa do mesmo denominador: **FP por usuário-dia**, não por
evento — senão compara-se uma taxa medida em eventos com uma detecção que só
existe em janelas.

**Proposta:** duas unidades, declaradas separadamente. Evento para os cenários
pontuais; episódio ou usuário-dia para os de contexto e longitudinais. A tabela
final ganha uma coluna e para de misturar grandezas.

### D-13 · Tratamento estatístico

Hoje o desenho prevê uma semente e uma execução por configuração: quatro
números. Com isso não há como distinguir "a C3 é melhor" de "a C3 deu sorte
nesta semente".

```text
PROPOSTA: N sementes (20 a 30) × 4 configurações
          cada célula vira média ± desvio
          as MESMAS sementes nas quatro configurações → comparação pareada
          teste de Wilcoxon pareado sobre as N diferenças

CUSTO:    um laço no script da S11. Horas de CPU, não de pessoa.
GANHO:    a diferença entre "a tabela mostra" e "a diferença é
          estatisticamente significativa (p < 0,05, n = 30)".
```

A semente já é configurável no gerador e já é gravada em cada execução. Falta
usar.

### D-14 · A métrica primária pode não existir para a C0

A C0 soma no máximo quatro regras discretas e não dispara em cenários
longitudinais. Se ela não alcançar revocação de 0,90 em limiar nenhum, "FPR a
revocação 0,90" não existe para o grupo de controle — e a métrica primária fica
sem par de comparação.

**Proposta:** comparar curvas precisão-revocação em vez de pontos únicos. Em
classe muito desbalanceada, que é o caso aqui, a curva PR informa mais que a
ROC.

### D-15 · Critério de relevância declarado antes

Sem dizer de antemão quanto de redução conta como sucesso, a discussão dos
resultados vira racionalização do que deu. Declarar o critério *antes* de
existir número é rigor; declará-lo depois é justificativa.

**Proposta:** uma frase na Metodologia (S5) fixando qual redução de FPR e qual
revocação longitudinal contam como resposta afirmativa.

### D-16 · Falta o controle negativo longitudinal

Os cenários preveem verdadeiros positivos longitudinais e ruído pontual, mas
**não existe cenário de escalada legítima** — alguém que muda de projeto e passa
a acessar mais coisas, mais tarde, com mais volume. Sem ele, o falso positivo da
D3 fica sem medida, e a D3 é justamente a contribuição original.

Há um problema de circularidade junto: a D3 é projetada para capturar escalada
gradual, o cenário L1 é projetado como escalada gradual, e mede-se se a D3 pega
a L1. Isso prova que a implementação funciona, não que a abordagem serve.

**Proposta:** acrescentar o cenário de escalada legítima e, se der para
organizar, desenho cego — a Yasmin especifica os cenários sem ver a fórmula da
D3. Ela já é a dona dos cenários; a separação sai de graça.

### D-17 · Vazamento no baseline da D2

Se o baseline de cada usuário for calculado sobre os mesmos 30 dias que já
contêm os cenários injetados, o comportamento anômalo entra na definição do que
é normal. O resultado fica bom pelo motivo errado.

**Proposta:** separação temporal explícita — janela de constituição do baseline
anterior e disjunta da janela de avaliação. Precisa aparecer no artigo: é
pergunta que a banca faz.

### D-18 · Dupla contagem e escala na integração

```text
exposure(u,t) = Σ (event_risk_e + behavioral_risk_e) · λ^(t−t_e)
                e ∈ [t−W, t]

O evento atual está nessa janela, com t_e = t  →  λ⁰ = 1
Logo exposure JÁ CONTÉM o risco do evento atual.

final = α·event_risk + β·behavioral_risk + γ·exposure
        └───────────┬───────────┘         └──┬──┘
           contados aqui...           ...e de novo aqui
```

Duas consequências:

1. **Pesos deixam de ser interpretáveis** — o peso efetivo do evento atual é
   α + γ, não α.
2. **Escala** — `event_risk` vai de 0 a 100; `exposure` soma até 14 dias de
   eventos, na ordem de centenas ou milhares. O termo de exposição domina o
   score final em todos os casos, inclusive nos pontuais.

**Proposta:** excluir o evento atual da janela de exposição — ela passa a ser "o
que veio antes". Normalizar `exposure` para 0–100 resolve a escala, mas não a
dupla contagem; excluir o evento resolve as duas.

### D-19 · A vertente LGPD e ISO/IEC 27001

Monitorar comportamento de colaborador é tratamento de dado pessoal. Com dados
sintéticos a LGPD não vincula o trabalho operacionalmente — mas discutir o que a
implantação real implicaria é matéria de limitações e trabalhos futuros, e é
diferencial de baixo custo perante a banca.

**Proposta:** entra na S13, apoiada na Lei 13.709/2018, no material da ANPD
sobre monitoramento no ambiente de trabalho e no controle 8.16 da ISO/IEC
27001:2022.

---

## Como registrar uma decisão nova

1. Próximo ID livre da sequência
2. Uma linha em **Abertas**, com proposta, dono e prazo
3. Quando fechar: mover para **Fechadas**, com a data e o que ficou combinado
4. Se a decisão mudar o [plano](plano.md), alterar o plano no mesmo Pull Request

Decisão que muda regra de processo, padrão ou workflow exige **duas** aprovações
— ver [`AGENTS.md`](../AGENTS.md), seção 4.
