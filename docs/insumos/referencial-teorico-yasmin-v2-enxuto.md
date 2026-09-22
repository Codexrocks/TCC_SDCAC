# Referencial Teórico — versão enxuta para o artigo (2ª etapa)

**Base:** `referencial-teorico-yasmin-v1.md` (levantamento anterior) · Reli `artigo/02-referencial-teorico.md`, `docs/cobem.md` e `docs/plano.md` antes de cortar.
**Extensão alvo:** 1,5–2 páginas do artigo (TNR 10, justificado, entrelinha simples) · **Extensão deste rascunho:** ≈ 1.150 palavras de corpo de texto, dentro da faixa.
**Não fiz:** pesquisa nova, tema novo, peso, threshold, regra nova, ou alteração de C0–C3. Só cortei e reescrevi o que já estava levantado.

---

## 1. Versão final enxuta do Referencial Teórico

> Numeração provisória (2.1–2.4), para caber nos três níveis do COBEM. Ajustar quando o texto for colado no artigo, conforme a numeração de seção que a Introdução e a Metodologia já tiverem fixado.

### 2.1 Segurança da informação, autenticação, autorização e logs

A segurança da informação organiza-se, normativamente, em torno da preservação da confidencialidade, integridade e disponibilidade da informação (ISO/IEC 27001:2022). Um evento de acesso pode ser lido como uma tentativa, bem-sucedida ou não, de comprometer uma dessas propriedades, o que fundamenta a leitura de eventos de log como indicadores de risco e não como categorias arbitrárias.

Autenticação e autorização descrevem processos distintos e sequenciais: a primeira verifica a identidade de um sujeito a partir de evidências vinculadas a essa identidade (Grassi et al., 2017); a segunda decide quais ações um sujeito já autenticado pode executar, tipicamente mediada por papéis (Sandhu et al., 1996). Essa distinção importa porque falhas de autenticação — horário atípico, força bruta, origem não habitual — geram eventos discretos e fáceis de registrar, enquanto violações de autorização exigem conhecer o padrão esperado do sujeito, não apenas o evento isolado.

O registro dessas evidências ocorre por meio de logs de segurança, cuja gestão cobre geração, armazenamento e análise de eventos relevantes à postura de segurança de um sistema (Kent e Souppaya, 2006). Entre os campos que tipicamente apoiam a identificação de comportamento suspeito estão identidade do sujeito, timestamp, origem de rede, dispositivo e o recurso afetado (Kent e Souppaya, 2006) — os mesmos atributos que compõem a base de eventos do protótipo.

### 2.2 SIEM, SOC e o problema do volume de alertas

Sistemas de gerenciamento de informações e eventos de segurança (SIEM) combinam coleta multifonte, normalização e correlação de eventos para gerar alertas priorizados a um analista humano (Gonzalez-Granadillo, Gonzalez-Zarzosa e Diaz, 2021). Os mesmos autores documentam uma limitação estrutural amplamente relatada: a correlação depende de regras escritas manualmente, e o volume de alertas gerado tende a exceder a capacidade de análise disponível.

Um Centro de Operações de Segurança (SOC) é a função organizacional responsável por monitorar essa correlação e conduzir a triagem dos alertas resultantes. A revisão sistemática de Vielberth et al. (2020) identifica, entre os desafios em aberto mais recorrentes da literatura de SOC, exatamente esse descompasso entre volume de alertas e capacidade humana de análise, agravado pela ausência de contexto comportamental na maior parte das ferramentas — o alerta sinaliza o evento, mas não diz se ele é habitual para aquele usuário específico.

### 2.3 UEBA, comportamento do usuário e ameaças internas

User and Entity Behavior Analytics (UEBA) desloca a pergunta de "este evento corresponde a um padrão de ataque conhecido?" para "este evento é normal para esta entidade específica, dado o que ela fez antes?", a partir da construção de um perfil de comportamento habitual por entidade e da avaliação do desvio de eventos novos em relação a esse perfil (Shashanka, Shen e Wan, 2016).

Essa mudança de pergunta é o que torna a ameaça interna um caso estruturalmente difícil para abordagens baseadas apenas em autenticação e perímetro: o agente possui credencial válida e não dispara os controles desenhados para deter um invasor externo. Cappelli, Moore e Trzeciak (2012), a partir da análise de casos reais documentados pelo CERT, distinguem padrões recorrentes de sabotagem, roubo de propriedade intelectual e fraude; Homoliak et al. (2019), em revisão mais recente, sistematizam essas taxonomias e os métodos de detecção associados a cada padrão, incluindo abordagens comportamentais.

### 2.4 Detecção de anomalias, falsos positivos e o desenho experimental

A ideia de inferir atividade maliciosa a partir do desvio em relação a um perfil de uso normal remonta a Denning (1987). Chandola, Banerjee e Kumar (2009) formalizam essa ideia em três tipos: anomalia pontual, quando uma instância isolada destoa do restante; contextual, quando a mesma instância só é anômala dentro de um contexto específico, como o histórico de um usuário; e coletiva, quando uma sequência de instâncias, nenhuma anômala isoladamente, é anômala em conjunto. Detecção baseada em regras com limiares fixos, por construção, não distingue variações legítimas de comportamento entre usuários e contextos — uma limitação que motiva diretamente a incorporação de contexto individual e temporal proposta neste trabalho.

Essa rigidez tem um efeito quantificável quando eventos maliciosos são raros em relação ao volume total de eventos legítimos: mesmo um detector com taxa de falso positivo percentualmente pequena produz, em termos absolutos, uma fila de alertas dominada por falsos positivos — a base-rate fallacy, demonstrada formalmente por Axelsson (2000). Em operação contínua, esse volume de ruído é uma das causas documentadas de exaustão do analista de segurança, com impacto direto na qualidade da triagem (Sundaramurthy et al., 2015).

O mapeamento entre essas categorias e as quatro configurações do desenho de ablação C0→C3 é uma leitura aplicada deste trabalho, e não uma classificação proposta pelos autores citados: C0/C1 são aqui entendidas como tratamento do evento como anomalia pontual, na lógica de correlação estática de um SIEM; C2, como aproximação de anomalia contextual, ao introduzir o desvio em relação ao histórico do próprio usuário; C3, como aproximação de anomalia coletiva, ao avaliar recorrência e evolução ao longo de dias — padrão de escalada gradual discutido na literatura de ameaça interna. Sob essa leitura, reduzir a taxa de falsos positivos sem perda de revocação, comparando as quatro configurações, é uma tentativa experimental de mitigar o efeito descrito por Axelsson (2000) sem abrir mão da cobertura que uma análise por regras sobre eventos isolados, por definição, não alcança.

---

## 2. Lista exata das referências usadas nesta versão

Ordem alfabética pelo sobrenome do primeiro autor, formato autor-ano do COBEM. Todas já constavam do levantamento anterior — nenhuma nova.

- Axelsson, S., 2000. "The base-rate fallacy and the difficulty of intrusion detection". *ACM Transactions on Information and System Security*, Vol. 3, No. 3, pp. 186-205.
- Cappelli, D.M., Moore, A.P. and Trzeciak, R.F., 2012. *The CERT Guide to Insider Threats: How to Prevent, Detect, and Respond to Information Technology Crimes*. Boston: Addison-Wesley.
- Chandola, V., Banerjee, A. and Kumar, V., 2009. "Anomaly detection: a survey". *ACM Computing Surveys*, Vol. 41, No. 3, Article 15.
- Denning, D.E., 1987. "An intrusion-detection model". *IEEE Transactions on Software Engineering*, Vol. SE-13, No. 2, pp. 222-232.
- Gonzalez-Granadillo, G., Gonzalez-Zarzosa, S. and Diaz, R., 2021. "Security information and event management (SIEM): analysis, trends, and usage in critical infrastructures". *Sensors*, Vol. 21, No. 14, Article 4759.
- Grassi, P.A. et al., 2017. *Special Publication 800-63-3 — Digital Identity Guidelines*. Gaithersburg: NIST.
- Homoliak, I., Toffalini, F., Guarnizo, J., Elovici, Y. and Ochoa, M., 2019. "Insight into insiders and IT: a survey of insider threat taxonomies, analysis, modeling, and countermeasures". *ACM Computing Surveys*, Vol. 52, No. 2, Article 30, pp. 30:1–30:40.
- International Organization for Standardization, 2022. *ISO/IEC 27001:2022 — Information security, cybersecurity and privacy protection — Information security management systems — Requirements*. Geneva: ISO.
- Kent, K. and Souppaya, M., 2006. *Special Publication 800-92 — Guide to Computer Security Log Management*. Gaithersburg: NIST.
- Sandhu, R.S., Coyne, E.J., Feinstein, H.L. and Youman, C.E., 1996. "Role-based access control models". *IEEE Computer*, Vol. 29, No. 2, pp. 38-47.
- Shashanka, M., Shen, M.-Y. and Wan, J., 2016. "User and entity behavior analytics for enterprise security". In: *2016 IEEE International Conference on Big Data*. Washington, D.C.: IEEE, pp. 1867-1874.
- Sundaramurthy, S.C., Bardas, A.G., Case, J., Ou, X., Wesch, M., McHugh, J. and Rajagopalan, S.R., 2015. "A human capital model for mitigating security analyst burnout". In: *Proceedings of the Eleventh Symposium on Usable Privacy and Security (SOUPS 2015)*. Ottawa: USENIX Association, pp. 347-359.
- Vielberth, M., Böhm, F., Fichtinger, I. and Pernul, G., 2020. "Security operations center: a systematic study and open challenges". *IEEE Access*, Vol. 8, pp. 227756-227779.

**13 referências**, contra 17 no levantamento — 4 descartadas (seção 3).

---

## 3. Fontes descartadas nesta versão, e por quê

| Fonte | Motivo do corte |
|---|---|
| CISA — "Defining Insider Threats" | Redundante com Cappelli et al. (2012) e Homoliak et al. (2019), que já cobrem definição e tipologia com mais densidade acadêmica; página institucional sem data de publicação específica pesava mais como reforço do que como argumento novo. |
| NIST SP 800-61 Rev. 2 — *Computer Security Incident Handling Guide* | Formaliza o ciclo de resposta a incidentes, mas o SDCAC não implementa resposta a incidente (a delimitação em `plano.md` exclui bloqueio automático e resposta autônoma) — manter essa referência puxaria o texto para um processo que o projeto explicitamente não cobre. |
| Zimmerman — *Ten/Eleven Strategies of a World-Class Cybersecurity Operations Center* (MITRE) | Descreve a operação prática de um SOC real; Vielberth et al. (2020) já sustenta, sozinho e com peso acadêmico maior (revisão sistemática, IEEE Access), a mesma afirmação sobre volume de alertas e falta de contexto comportamental — as duas citações juntas seriam repetição na versão enxuta. |
| Sommer e Paxson (2010) — "Outside the Closed World" | O argumento central (limitação de ML/regras por desbalanceamento de classes) já está coberto por Chandola et al. (2009) nesta versão compacta; além disso, essa fonte já está citada em `docs/decisoes.md` no contexto do risco de dados sintéticos, não da fundamentação teórica — manter os dois usos apontando para o mesmo artigo era redundância entre seções do próprio TCC, não uma perda de conteúdo. |

Nenhuma citação foi removida por dúvida quanto à existência da fonte — todas as 4 continuam válidas para uso em outras partes do artigo (Metodologia, Discussão, Limitações), só não entraram nesta versão compacta do Referencial Teórico.
