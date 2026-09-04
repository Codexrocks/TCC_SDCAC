# Usabilidade

Por que esta página existe: num sistema de detecção, **a interface é onde a
detecção vira decisão**. Um alerta que ninguém entende, ou que se perde no meio
de outros trinta, é funcionalmente idêntico a um alerta que nunca disparou. Por
isso usabilidade aqui é requisito do sistema, com princípio declarado e
medição — não opinião de quem está montando a tela.

Cada princípio abaixo vem com **de quem é** e **onde está publicado**. Nada de
"boas práticas" sem dono: a banca pode perguntar de onde saiu, e a resposta
precisa ter autor, ano e veículo.

---

## 1. A definição que adotamos

> Usabilidade é a medida em que um sistema, produto ou serviço pode ser usado
> por usuários específicos para atingir objetivos específicos com **eficácia**,
> **eficiência** e **satisfação** num contexto de uso específico.

**Fonte:** ISO 9241-11:2018, *Ergonomics of human-system interaction — Part 11:
Usability: definitions and concepts*.

Isso tem consequência prática. Usabilidade não é uma nota geral do sistema: ela
só existe amarrada a **quem** usa, **para quê** e **em que contexto**. O nosso
recorte:

| Dimensão | O nosso caso |
|---|---|
| Usuário | Analista de segurança júnior, sem familiaridade prévia com o sistema |
| Objetivo | Identificar, classificar e priorizar eventos anômalos |
| Contexto | Monitoramento em tela, sob pressão de tempo e com vários alertas simultâneos |

As três dimensões da norma viram as três métricas da seção 6: eficácia = acertou
a classificação; eficiência = em quanto tempo; satisfação = SUS.

O processo de projeto centrado no usuário — pesquisar, projetar, avaliar,
iterar — segue a ISO 9241-210:2019, *Human-centred design for interactive
systems*.

---

## 2. Heurísticas de Nielsen

**Autor:** Jakob Nielsen. As dez heurísticas na forma atual são de 1994; o
método de avaliação heurística que as usa foi publicado por **Nielsen e Rolf
Molich** em 1990.

São o vocabulário mais usado do campo. Servem para duas coisas no projeto:
guiar o desenho do dashboard e, depois, servir de **grade de avaliação**
(seção 6.1).

| # | Heurística | O que exige do nosso dashboard |
|---|---|---|
| 1 | Visibilidade do estado do sistema | O painel mostra se está recebendo eventos agora, e há quanto tempo foi a última ingestão. Tela parada e sistema morto não podem ser indistinguíveis. |
| 2 | Correspondência com o mundo real | Vocabulário de SOC, não de banco de dados. "Tentativas de login malsucedidas", não `failed_auth_count`. |
| 3 | Controle e liberdade do usuário | Todo filtro aplicado pode ser desfeito. Marcar um alerta como falso positivo tem como voltar atrás. |
| 4 | Consistência e padrões | A mesma faixa de risco tem sempre a mesma cor, o mesmo rótulo e a mesma posição, em todas as telas. |
| 5 | Prevenção de erros | Ação destrutiva — descartar alerta, apagar filtro salvo — pede confirmação e diz o que vai acontecer. |
| 6 | Reconhecer em vez de lembrar | As faixas de risco aparecem rotuladas na tela. O analista não precisa decorar que 76 é ALTO. |
| 7 | Flexibilidade e eficiência | Filtros salvos e ordenação por score para quem já conhece a ferramenta, sem atrapalhar quem chegou agora. |
| 8 | Estética e design minimalista | Cada elemento na tela disputa atenção com um alerta real. O que não ajuda a decidir, sai. |
| 9 | Ajudar a reconhecer, diagnosticar e recuperar de erros | O alerta diz **qual regra** disparou e **com quantos pontos**, não só o total. Sem isso o analista não tem como julgar. |
| 10 | Ajuda e documentação | Cada regra de detecção tem uma explicação de uma linha acessível na própria tela. |

> A heurística 9 é a que mais muda o nosso sistema. Um Risk Score de 70 sem a
> decomposição — de onde vieram os 70 — é um número que o analista precisa
> aceitar sem poder verificar. Com a decomposição (horário +30, IP não habitual
> +40), ele julga. As regras e pesos estão em
> [`arquitetura.md`](arquitetura.md).

---

## 3. Princípios de Norman

**Autor:** Donald A. Norman, em *The Design of Everyday Things* (edição revista
de 2013; publicado originalmente em 1988 como *The Psychology of Everyday
Things*).

Onde Nielsen dá uma lista de conferência, Norman explica **por que** as coisas
funcionam ou não. Os conceitos que usamos:

| Conceito | Definição | No dashboard |
|---|---|---|
| **Affordance** | A relação entre as propriedades do objeto e as capacidades de quem usa, que determina o que é possível fazer | Uma linha da tabela de incidentes é clicável porque se comporta como clicável |
| **Significante** | A pista perceptível que comunica onde a ação deve acontecer | O cursor muda, a linha destaca no *hover*. Termo introduzido na edição de 2013 |
| **Mapeamento** | A correspondência entre controle e efeito | O filtro de severidade fica junto da coluna de severidade, não num menu distante |
| **Feedback** | Informação de retorno sobre o que acabou de acontecer | Aplicou filtro? A contagem muda na hora e diz quantos itens ficaram escondidos |
| **Restrição** | Limite que reduz as alternativas erradas | O filtro de data não deixa escolher intervalo futuro |
| **Modelo conceitual** | A explicação, ainda que simplificada, de como a coisa funciona | O analista precisa entender que o score é uma **soma de regras**, não uma predição estatística opaca |

---

## 4. Regras de ouro de Shneiderman

**Autor:** Ben Shneiderman, *Designing the User Interface* (1ª edição em 1986;
edições recentes com Catherine Plaisant e outros).

São oito, e se sobrepõem em parte às de Nielsen. Registramos porque duas delas
não têm equivalente direto nas outras listas e importam aqui:

- **Projetar diálogos que deem encerramento** — o analista precisa saber quando
  terminou de tratar um alerta. Sem um estado de "tratado", ele reabre o mesmo
  incidente três vezes.
- **Reduzir a carga de memória de curto prazo** — comparar dois incidentes não
  pode exigir decorar o primeiro para depois abrir o segundo.

As outras seis: buscar consistência, buscar usabilidade universal, oferecer
feedback informativo, prevenir erros, permitir reversão fácil de ações e manter
o usuário no controle.

---

## 5. Acessibilidade — WCAG 2.2

**Autoria:** W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*,
Recomendação de outubro de 2023. Organiza-se em quatro princípios, conhecidos
pela sigla **POUR**: conteúdo perceptível (*Perceivable*), operável
(*Operable*), compreensível (*Understandable*) e robusto (*Robust*).

Adotamos o **nível AA** como alvo. Dois critérios mudam o projeto agora.

### 5.1 O uso da cor — e um problema já identificado

O critério **1.4.1 (Uso da cor)** diz que a cor não pode ser o **único** meio
visual de transmitir informação.

As faixas de risco definidas em [`arquitetura.md`](arquitetura.md) hoje estão
descritas assim: indicação azul, alerta amarelo, alerta crítico vermelho.
**Como está, o dashboard falharia no critério 1.4.1.** Vermelho e amarelo são
justamente o par mais afetado pela deficiência de visão de cores mais comum.

A correção não é trocar de cor, é **parar de depender só dela**. Toda faixa
carrega, além da cor:

| Faixa | Cor | Rótulo textual | Forma / ícone |
|---|---|---|---|
| 0–20 | neutra | `NORMAL` | — |
| 21–50 | azul | `RISCO BAIXO` | círculo |
| 51–75 | amarelo | `RISCO MÉDIO` | triângulo |
| 76–100 | vermelho | `RISCO ALTO` | octógono preenchido |

Vale para tabela, gráfico e legenda. Um gráfico de barras por severidade precisa
de rótulo ou textura, não só de cor.

> Esta é uma mudança de **apresentação**, não das faixas nem dos pesos. As
> faixas continuam as de `arquitetura.md` — quem decide sobre elas é a Yasmin.

### 5.2 Contraste

O critério **1.4.3 (Contraste mínimo)** exige razão de pelo menos **4,5:1**
entre texto e fundo, e **3:1** para texto grande. Vale também para o texto
dentro dos gráficos. Amarelo sobre branco é a armadilha clássica, e reprova.

---

## 6. Como vamos medir

Princípio sem medição é alegação. Três instrumentos, em momentos diferentes do
[cronograma](cronograma.md).

### 6.1 Avaliação heurística — durante a construção (S9)

**Método:** Nielsen e Molich (1990). Cada avaliador percorre a interface sozinho
confrontando-a com as dez heurísticas da seção 2, anota as violações, e só
depois os resultados são consolidados. Avaliar em grupo desde o início faz um
avaliador contaminar o outro.

**Quem:** os três integrantes. Nielsen recomenda de três a cinco avaliadores —
com um só, a maior parte dos problemas passa batido.

**Severidade** — escala de Nielsen, de 0 a 4:

| Grau | Significado | O que fazemos |
|---|---|---|
| 0 | Não é problema de usabilidade | Nada |
| 1 | Cosmético | Corrige se sobrar tempo |
| 2 | Menor | Entra no backlog |
| 3 | Maior | Corrige antes da entrega |
| 4 | Catastrófico | Bloqueia a entrega |

**Saída:** tabela `heurística violada | onde | severidade | correção` em
`docs/relatorios/`.

### 6.2 Teste com usuários — S11, junto dos cenários

Aproveitamos os seis cenários de teste que já existem em
[`arquitetura.md`](arquitetura.md). O participante recebe a tarefa
("identifique o incidente de maior risco da última hora e diga qual regra
disparou") e trabalha sem ajuda.

| Métrica | Como se mede | Ligação com a ISO 9241-11 |
|---|---|---|
| Taxa de sucesso | tarefas concluídas corretamente ÷ tarefas tentadas | Eficácia |
| Tempo por tarefa | do início ao fim, em segundos | Eficiência |
| Erros de classificação | quantas vezes o participante errou a severidade | Eficácia |

> **Quantos participantes.** Nielsen e Landauer (1993) modelaram
> matematicamente a descoberta de problemas de usabilidade; daí vem a
> recomendação, muito citada, de que poucos participantes já revelam a maior
> parte dos problemas. Para um TCC, cinco participantes por rodada é o número
> praticável.
> <!-- FALTA CITAÇÃO --> conferir a formulação exata e a porcentagem na fonte
> antes de citar o número no artigo.

### 6.3 SUS — satisfação, ao fim de cada rodada

**Instrumento:** System Usability Scale, de **John Brooke (1996)**, publicado em
*Usability Evaluation in Industry*.

Dez afirmações, resposta de 1 (discordo totalmente) a 5 (concordo totalmente),
alternando entre positivas e negativas. O cálculo: nos itens ímpares, subtraia 1
da resposta; nos pares, subtraia a resposta de 5; some tudo e multiplique por
2,5. O resultado vai de 0 a 100.

> **Não é porcentagem.** 70 no SUS não significa "70% de aprovação". É um escore
> numa escala própria.

Para interpretar, usamos a escala adjetiva de **Bangor, Kortum e Miller (2009)**,
que associa faixas do escore a adjetivos e situa a média em torno de 68.
<!-- FALTA CITAÇÃO --> conferir os limites exatos de cada faixa adjetiva na
fonte antes de publicar a tabela no artigo.

**Meta do projeto:** SUS ≥ 68 na rodada final. Abaixo disso, o resultado entra
na seção de limitações do artigo — e não é um fracasso, é um achado. Resultado
ruim relatado com honestidade vale mais na banca que número inflado.

---

## 7. Usabilidade aplicada à segurança

Segurança tem literatura própria de usabilidade, e ela existe porque o campo
aprendeu na marra que sistema seguro que ninguém consegue operar não é seguro.

- **Adams e Sasse (1999), "Users Are Not the Enemy"**, *Communications of the
  ACM*. O argumento que fundou a área: usuários burlam controles de segurança
  quando esses controles atrapalham o trabalho — e a culpa é do projeto, não do
  usuário.
- **Whitten e Tygar (1999), "Why Johnny Can't Encrypt"**, *USENIX Security
  Symposium*. Avaliação de usabilidade do PGP 5.0 que mostrou usuários
  competentes cometendo erros graves de segurança por causa da interface.
- **Cranor e Garfinkel (2005), *Security and Usability***, O'Reilly. Coletânea
  que consolidou o campo.

### Fadiga de alerta

O risco mais concreto para o nosso sistema. Um dashboard que dispara alerta
demais treina o analista a ignorar alertas — e aí a taxa de falsos positivos
deixa de ser uma métrica estatística e vira um problema de usabilidade.

É por isso que a faixa 0–20 **não gera alerta** e a 21–50 é registro preventivo,
sem interromper ninguém. Só 51+ chama atenção ativamente. A decisão já está em
[`arquitetura.md`](arquitetura.md); aqui fica registrado o motivo do ponto de
vista de usabilidade.

A taxa de falsos positivos medida na S12 é, portanto, também um indicador de
usabilidade — e deve ser lida junto do SUS na discussão dos resultados.

<!-- FALTA CITAÇÃO --> há literatura específica sobre carga de trabalho e
fadiga de alerta em analistas de SOC. Yasmin: vale procurar na S4, quando o
referencial cobrir SIEM e SOC.

---

## 8. Onde isso entra no artigo

| Seção do artigo | O que vai | Quem |
|---|---|---|
| Referencial teórico | Seções 1 a 5 e 7 desta página — princípios, norma e usabilidade em segurança | Yasmin + Felipe |
| Metodologia | Seção 6 — os três instrumentos e como foram aplicados | Felipe |
| Resultados | Escores SUS, tabela de violações heurísticas, métricas de tarefa | Felipe |
| Discussão | Fadiga de alerta cruzando taxa de falsos positivos com satisfação | Todos |

---

## 9. Referências

Formatação ABNT NBR 6023. Antes da submissão, conferir cada entrada na fonte —
principalmente páginas e edição.

ADAMS, Anne; SASSE, Martina Angela. Users are not the enemy. **Communications
of the ACM**, v. 42, n. 12, 1999.

BANGOR, Aaron; KORTUM, Philip; MILLER, James. Determining what individual SUS
scores mean: adding an adjective rating scale. **Journal of Usability Studies**,
v. 4, n. 3, 2009.

BROOKE, John. SUS: a quick and dirty usability scale. In: JORDAN, Patrick W. et
al. (org.). **Usability Evaluation in Industry**. London: Taylor & Francis, 1996.

CRANOR, Lorrie Faith; GARFINKEL, Simson (org.). **Security and Usability:
designing secure systems that people can use**. Sebastopol: O'Reilly, 2005.

INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO 9241-11:2018** —
Ergonomics of human-system interaction — Part 11: Usability: definitions and
concepts. Geneva: ISO, 2018.

INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO 9241-210:2019** —
Ergonomics of human-system interaction — Part 210: Human-centred design for
interactive systems. Geneva: ISO, 2019.

NIELSEN, Jakob. Enhancing the explanatory power of usability heuristics. In:
**Proceedings of the SIGCHI Conference on Human Factors in Computing Systems
(CHI '94)**. New York: ACM, 1994.

NIELSEN, Jakob; LANDAUER, Thomas K. A mathematical model of the finding of
usability problems. In: **Proceedings of the INTERACT '93 and CHI '93
Conference on Human Factors in Computing Systems**. New York: ACM, 1993.

NIELSEN, Jakob; MOLICH, Rolf. Heuristic evaluation of user interfaces. In:
**Proceedings of the SIGCHI Conference on Human Factors in Computing Systems
(CHI '90)**. New York: ACM, 1990.

NORMAN, Donald A. **The Design of Everyday Things**: revised and expanded
edition. New York: Basic Books, 2013.

SHNEIDERMAN, Ben et al. **Designing the User Interface**: strategies for
effective human-computer interaction. 6. ed. Boston: Pearson, 2016.
<!-- FALTA CITAÇÃO --> conferir edição e ano da que a equipe efetivamente
consultar.

W3C. **Web Content Accessibility Guidelines (WCAG) 2.2**. W3C Recommendation,
2023. Disponível em: https://www.w3.org/TR/WCAG22/

WHITTEN, Alma; TYGAR, J. D. Why Johnny can't encrypt: a usability evaluation of
PGP 5.0. In: **Proceedings of the 8th USENIX Security Symposium**. Berkeley:
USENIX Association, 1999.
