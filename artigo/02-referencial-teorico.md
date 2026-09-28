# 2. Referencial Teórico

> **Escrito pela Yasmin**, dona do referencial teórico e do conteúdo de
> segurança. Entregue em 28/09/2026 e versionado pelo Davi — o insumo como
> recebido está em
> [`docs/insumos/referencial-teorico-yasmin-v2.md`](../docs/insumos/referencial-teorico-yasmin-v2.md).
>
> **2ª Versão** na numeração do professor · S5 do
> [cronograma](../docs/cronograma.md).
>
> **Extensão:** ≈ 1.150 palavras, dentro da faixa de 1,5 a 2 páginas do
> [orçamento](README.md#divisão-de-páginas).
>
> ⚠️ **As 13 referências ainda não entraram em [`referencias.md`](referencias.md).**
> Aquela página só aceita entrada depois de alguém abrir a fonte; as pendências
> estão em [citações pendentes](../docs/citacoes-pendentes.md), com a Yasmin
> como responsável.

***

## 2.1 Segurança da informação, autenticação, autorização e logs

A segurança da informação organiza-se, normativamente, em torno da preservação
da confidencialidade, integridade e disponibilidade da informação
(INTERNATIONAL ORGANIZATION FOR STANDARDIZATION, 2022). Um evento de acesso pode
ser lido como uma tentativa, bem-sucedida ou não, de comprometer uma dessas
propriedades, o que fundamenta a leitura de eventos de log como indicadores de
risco e não como categorias arbitrárias.

Autenticação e autorização descrevem processos distintos e sequenciais: a
primeira verifica a identidade de um sujeito a partir de evidências vinculadas a
essa identidade (GRASSI et al., 2017); a segunda decide quais ações um sujeito já
autenticado pode executar, tipicamente mediada por papéis (SANDHU et al., 1996).
Essa distinção importa porque falhas de autenticação — horário atípico, força
bruta, origem não habitual — geram eventos discretos e fáceis de registrar,
enquanto violações de autorização exigem conhecer o padrão esperado do sujeito,
não apenas o evento isolado.

O registro dessas evidências ocorre por meio de logs de segurança, cuja gestão
cobre geração, armazenamento e análise de eventos relevantes à postura de
segurança de um sistema (KENT; SOUPPAYA, 2006). Entre os campos que tipicamente
apoiam a identificação de comportamento suspeito estão identidade do sujeito,
timestamp, origem de rede, dispositivo e o recurso afetado (KENT; SOUPPAYA,
2006) — os mesmos atributos que compõem a base de eventos do protótipo.

## 2.2 SIEM, SOC e o problema do volume de alertas

Sistemas de gerenciamento de informações e eventos de segurança (SIEM) combinam
coleta multifonte, normalização e correlação de eventos para gerar alertas
priorizados a um analista humano (GONZALEZ-GRANADILLO; GONZALEZ-ZARZOSA; DIAZ,
2021). Os mesmos autores documentam uma limitação estrutural amplamente relatada:
a correlação depende de regras escritas manualmente, e o volume de alertas gerado
tende a exceder a capacidade de análise disponível.

Um Centro de Operações de Segurança (SOC) é a função organizacional responsável
por monitorar essa correlação e conduzir a triagem dos alertas resultantes. A
revisão sistemática de Vielberth et al. (2020) identifica, entre os desafios em
aberto mais recorrentes da literatura de SOC, exatamente esse descompasso entre
volume de alertas e capacidade humana de análise, agravado pela ausência de
contexto comportamental na maior parte das ferramentas — o alerta sinaliza o
evento, mas não diz se ele é habitual para aquele usuário específico.

## 2.3 UEBA, comportamento do usuário e ameaças internas

*User and Entity Behavior Analytics* (UEBA) desloca a pergunta de "este evento
corresponde a um padrão de ataque conhecido?" para "este evento é normal para
esta entidade específica, dado o que ela fez antes?", a partir da construção de
um perfil de comportamento habitual por entidade e da avaliação do desvio de
eventos novos em relação a esse perfil (SHASHANKA; SHEN; WAN, 2016).

Essa mudança de pergunta é o que torna a ameaça interna um caso estruturalmente
difícil para abordagens baseadas apenas em autenticação e perímetro: o agente
possui credencial válida e não dispara os controles desenhados para deter um
invasor externo. Cappelli, Moore e Trzeciak (2012), a partir da análise de casos
reais documentados pelo CERT, distinguem padrões recorrentes de sabotagem, roubo
de propriedade intelectual e fraude; Homoliak et al. (2019), em revisão mais
recente, sistematizam essas taxonomias e os métodos de detecção associados a cada
padrão, incluindo abordagens comportamentais.

## 2.4 Detecção de anomalias, falsos positivos e o desenho experimental

A ideia de inferir atividade maliciosa a partir do desvio em relação a um perfil
de uso normal remonta a Denning (1987). Chandola, Banerjee e Kumar (2009)
formalizam essa ideia em três tipos: anomalia pontual, quando uma instância
isolada destoa do restante; contextual, quando a mesma instância só é anômala
dentro de um contexto específico, como o histórico de um usuário; e coletiva,
quando uma sequência de instâncias, nenhuma anômala isoladamente, é anômala em
conjunto. Detecção baseada em regras com limiares fixos, por construção, não
distingue variações legítimas de comportamento entre usuários e contextos — uma
limitação que motiva diretamente a incorporação de contexto individual e temporal
proposta neste trabalho.

Essa rigidez tem um efeito quantificável quando eventos maliciosos são raros em
relação ao volume total de eventos legítimos: mesmo um detector com taxa de falso
positivo percentualmente pequena produz, em termos absolutos, uma fila de alertas
dominada por falsos positivos — a *base-rate fallacy*, demonstrada formalmente
por Axelsson (2000). Em operação contínua, esse volume de ruído é uma das causas
documentadas de exaustão do analista de segurança, com impacto direto na
qualidade da triagem (SUNDARAMURTHY et al., 2015).

O mapeamento entre essas categorias e as quatro configurações do desenho de
ablação C0→C3 é uma leitura aplicada deste trabalho, e não uma classificação
proposta pelos autores citados: C0/C1 são aqui entendidas como tratamento do
evento como anomalia pontual, na lógica de correlação estática de um SIEM; C2,
como aproximação de anomalia contextual, ao introduzir o desvio em relação ao
histórico do próprio usuário; C3, como aproximação de anomalia coletiva, ao
avaliar recorrência e evolução ao longo de dias — padrão de escalada gradual
discutido na literatura de ameaça interna. Sob essa leitura, reduzir a taxa de
falsos positivos sem perda de revocação, comparando as quatro configurações, é
uma tentativa experimental de mitigar o efeito descrito por Axelsson (2000) sem
abrir mão da cobertura que uma análise por regras sobre eventos isolados, por
definição, não alcança.

***

## O que esta seção ainda precisa

* [ ] **As 13 fontes confirmadas como abertas na fonte** · **Yasmin** · as
      pendências estão em [citações pendentes](../docs/citacoes-pendentes.md)
* [ ] **As 13 entradas em [`referencias.md`](referencias.md)**, em ABNT NBR
      6023, depois da confirmação acima · **Davi**
* [ ] **Decidir se a usabilidade aplicada à segurança entra aqui.** O esqueleto
      anterior tinha uma subseção 2.7 para isso, e a versão enxuta não a
      trouxe — o que é coerente com o corte para 1,5 a 2 páginas. O material já
      existe e tem fontes em [usabilidade](../docs/usabilidade.md), seção 7, e a
      §2.4 já cobre a fadiga de alerta por Sundaramurthy et al. (2015).
      **A chamada é da Yasmin** · até a S12, quando os Resultados forem escritos
* [ ] **Versionar o `referencial-teorico-yasmin-v1.md`**, o levantamento de 17
      fontes que deu origem a esta versão · **Yasmin** · o que não está no
      repositório não existe para a banca
* [ ] Ligação explícita entre 2.3 / 2.4 e as regras de
      [arquitetura](../docs/arquitetura.md) — a §2.4 já faz o mapeamento C0→C3;
      confirmar que os nomes das dimensões batem com a página
