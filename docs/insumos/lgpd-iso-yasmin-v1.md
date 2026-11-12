<!-- ARQUIVO DE REGISTRO — ver docs/insumos/README.md no repositório -->

# Insumo — A vertente LGPD e ISO/IEC 27001 (D-19)

| | |
|---|---|
| **Quem produziu** | **Yasmin** — dona da D-19 |
| **Entregue em** | 10/11/2026 |
| **Assistência de IA** | Rascunho integral produzido por Claude Sonnet 5, a pedido direto |
| **Conferi tudo que a IA escreveu?** | **Ainda não** — proposta até leitura e confirmação |
| **Para onde vai** | `artigo/04-resultados.md` § 4.6 (Limitações) · `artigo/05-conclusao.md` § 5.4 (Trabalhos futuros) |

---

## 1. O que já existe, e o que esta proposta acrescenta

As duas seções do artigo **já têm texto sobre a D-19** — não são blocos vazios.
A § 4.6 diz que "o que cabe dizer é o que uma implantação real exigiria à luz da
Lei nº 13.709/2018 e dos controles aplicáveis da ISO/IEC 27001:2022 — base
legal, transparência ao titular, minimização e retenção", e a § 5.4 lista isso
como o primeiro item de trabalhos futuros. O texto existe; falta a
especificidade que só quem responde pela vertente de segurança consegue dar —
que artigo da lei, qual base legal se aplicaria, qual controle da norma. É isto
que proponho abaixo, para substituir o parágrafo genérico. (O artigo
consolidado que está nesta mesma pasta do Drive não chega a esse nível de
detalhe — tem a mesma frase genérica, na seção de Ameaças à Validade — então
esta proposta continua sendo contribuição nova, não duplicada.)

**Importante: isto não fecha a D-19 sozinho.** Citação de lei e de norma não é
"citação pendente" no sentido do `docs/citacoes-pendentes.md` — é texto legal
público —, mas precisa da mesma disciplina: **conferir o artigo exato na fonte
oficial antes de assinar**, porque errar um número de artigo numa lei é erro
factual, não estilístico.

---

## 2. Texto proposto para a § 4.6 (Limitações)

> O monitoramento de comportamento de colaborador constitui tratamento de dado
> pessoal nos termos do art. 5º, X, da Lei nº 13.709/2018 (Lei Geral de Proteção
> de Dados Pessoais). Este trabalho opera exclusivamente sobre dados sintéticos
> e fictícios — nenhum evento, atributo ou padrão corresponde a pessoa real —,
> de modo que a legislação não vincula o protótipo do ponto de vista
> operacional. Uma implantação sobre dados reais, no entanto, precisaria
> satisfazer os princípios do art. 6º da Lei, em especial finalidade (uso
> restrito à segurança da informação, não à avaliação de desempenho),
> necessidade (coleta limitada aos atributos que o modelo de risco
> efetivamente consome) e transparência (ciência prévia do colaborador de que o
> monitoramento ocorre e com que propósito). A base legal mais plausível para
> esse tipo de tratamento é o legítimo interesse do controlador (art. 7º, IX),
> que o art. 10 condiciona a um Relatório de Impacto à Proteção de Dados
> Pessoais quando a Autoridade Nacional de Proteção de Dados (ANPD) o exigir —
> exigência que se espera razoável para monitoramento comportamental contínuo,
> dado o potencial de afetar direitos do titular. Do lado normativo, o
> controle 8.16 (Atividades de monitoramento) do Anexo A da ABNT NBR ISO/IEC
> 27001:2022 trata exatamente da definição de escopo, retenção e resposta a
> eventos de monitoramento, e serviria de referência para desenhar os limites
> de uma implantação real. A separação estrutural entre as bases `corp`,
> `ground_truth` e `sdcac`, adotada neste trabalho por razão metodológica
> (Seção 3.2), é também, incidentalmente, uma prática alinhada ao princípio de
> minimização de acesso que uma implantação real exigiria.

---

## 3. Texto proposto para a § 5.4 (Trabalhos futuros)

> **Implantação sobre dado real, à luz da LGPD e da ISO/IEC 27001:2022.** Uma
> implantação em organização real exigiria, no mínimo: (i) base legal explícita
> para o tratamento — tipicamente o legítimo interesse do art. 7º, IX, da Lei
> nº 13.709/2018, acompanhado do Relatório de Impacto à Proteção de Dados
> Pessoais que o art. 10 prevê; (ii) transparência ativa ao titular, com
> política de monitoramento comunicada antes da coleta, não depois; (iii)
> minimização, restringindo a coleta aos atributos que o modelo de risco
> efetivamente consome, e não à integralidade da navegação ou das comunicações
> do colaborador — delimitação que este trabalho já adota por desenho (Seção
> 1.6 do plano); (iv) retenção limitada, com descarte dos logs após prazo
> definido; e (v) adequação ao controle 8.16 do Anexo A da ISO/IEC 27001:2022,
> com trilha de auditoria e acesso restrito aos próprios registros de
> monitoramento — o que a separação entre `corp`, `ground_truth` e `sdcac`
> antecipa estruturalmente, embora tenha sido adotada por outro motivo.

---

## 4. O que a Yasmin ainda precisa conferir antes de assinar

- [ ] **Art. 5º, X; art. 6º; art. 7º, IX; e art. 10** da Lei nº 13.709/2018, na
      fonte oficial (planalto.gov.br) — números de artigo e inciso conferidos
      de memória, não copiados de uma fonte secundária
- [ ] **Se existe orientação publicada da ANPD** especificamente sobre
      monitoramento de empregados, e citar o documento certo — não inventar
      título de guia que a Autoridade não tenha publicado. Se não houver
      orientação específica e citável, a frase deve dizer isso, não presumir
- [ ] **A redação exata do controle 8.16** na ABNT NBR ISO/IEC 27001:2022 — o
      texto da norma é protegido por direito autoral e não pode ser reproduzido
      literalmente; a citação deve se limitar ao número, ao título e à
      ABNT NBR ISO/IEC 27001:2022 como fonte, sem transcrever o texto da norma
- [ ] **Confirmar com o Filipe** (caneta da S13) e o Davi (caneta da S14) se o
      texto acima cabe no espaço disponível, já que o artigo tem piso de 8
      páginas e teto de 12

---

## 5. O que falta

- [ ] **Minha leitura final**, incluindo a conferência dos artigos de lei acima
- [ ] **Entregar ao Filipe** para colar na § 4.6, e ao Davi para a § 5.4
- [ ] **Fechar a D-19** em `decisoes.md` depois que o texto entrar no artigo
