<!-- ARQUIVO DE REGISTRO — ver docs/insumos/README.md no repositório -->

# Insumo — Pesos preliminares e plano de sensibilidade (D-09)

| | |
|---|---|
| **Quem produziu** | **Yasmin** — dona da D-09 |
| **Entregue em** | 10/11/2026 |
| **Assistência de IA** | Rascunho integral produzido por Claude Sonnet 5, a pedido direto |
| **Conferi tudo que a IA escreveu?** | **Ainda não** — proposta até leitura e confirmação |
| **Para onde vai** | `decisoes.md` (D-09, ratificação da D-43) · insumo para `detection/d1/` e `artigo/03-metodologia.md` |

---

## 1. Por que isto é declarado antes de ver o código de pontuação

A D-09 pede **valores preliminares**, não os valores finais — esses saem da
análise de sensibilidade da S12, sobre dados reais de execução. Declarar um peso
depois de ver como o código pontua hoje não é "preliminar", é confirmar o que já
existe: o mesmo problema que a D-15 evita para o critério de relevância. Por
isso esta proposta foi escrita **sem abrir** `detection/d1/scoring.py`,
`detection/d2/scoring.py`, `detection/d2/baseline.py`, `detection/d3/scoring.py`,
`detection/d3/posture.py` nem `detection/presets.toml` — só com o catálogo de
atributos da seção 7 do banco simulado e raciocínio de segurança.

---

## 2. Pesos de integração entre dimensões — ratificação da D-43

A **D-43** (aberta, "a confirmar", donos Davi e Yasmin) propõe: D1 = 1,0,
D2 = 1,0, conduta (D3) = 1,0, postura (D3) = 0,5, e C0 sem ponderação. **Ratifico
essa proposta**, com a justificativa que segue — porque ela ainda está "a
confirmar", e confirmar sem motivo registrado é o mesmo problema que a D-09
existe para evitar.

| Componente | Peso proposto | Por que faz sentido do ponto de vista de segurança |
|---|---|---|
| D1 — risco do evento | 1,0 | É o sinal mais direto: um evento concreto, com atributos observáveis no momento em que acontece |
| D2 — desvio do padrão | 1,0 | Mesmo peso de D1 é defensável: divergência do próprio hábito é evidência tão forte quanto o evento em si, e o desenho da ablação (C0→C1→C2→C3) depende de D1 e D2 pesarem de forma comparável, para que o ganho de C2 sobre C1 meça contexto, não um reequilíbrio de peso |
| D3, parcela de **conduta** | 1,0 | Exposição acumulada é a contribuição original do trabalho — não cabe subponderá-la por padrão, sob risco de a comparação C3 vs. C2 ficar estruturalmente desfavorável antes mesmo de os dados rodarem |
| D3, parcela de **postura** | 0,5 | A postura é **estado**, não ação: ela descreve uma condição que persiste (MFA desligado, patch atrasado), não algo que a pessoa fez naquele momento. Um estado degradado é fator de risco — aumenta a superfície de ataque — mas não é, por si, indício de comportamento indevido. Pesar metade do que se pesa uma ação concreta evita que alguém com equipamento desatualizado, por razão alheia à sua conduta (ex.: TI atrasado na distribuição de patch), acabe com nota equivalente à de quem efetivamente agiu mal |

**O ponto mais sensível para a análise de sensibilidade da S12 é justamente o
0,5 da postura** — é o único valor da D-43 que não é um empate simples (1,0 para
todo o resto), e é o que carrega a justificativa mais longa. Se a S12 mostrar
que o resultado muda muito perto desse valor, é o primeiro candidato a revisar.

---

## 3. Pesos preliminares dentro de D1 — risco do evento individual

A D-31 diz que "a D1 é pontuação ponderada sobre todos os atributos do evento".
A tabela abaixo propõe uma **ordenação por severidade**, em três níveis, para os
atributos que a seção 7 do banco simulado já relaciona à D1 — não um número
final, porque a escala exata (0-100, por componente, com teto) é decisão de
implementação que cabe a quem escreve `detection/d1/scoring.py`.

| Nível | Atributo | Por que entra nesse nível |
|---|---|---|
| **Alto** | `action_subtype` = escalada de privilégio ou MFA desligado | Muda a postura de autorização da conta — é o evento com maior potencial de dano subsequente, porque abre caminho para outros |
| **Alto** | Acesso a recurso `sensitivity = restricted` | Contato direto com o dado de maior sigilo da organização — Folha de pagamento, Dossiê de pessoal, Console de infraestrutura |
| **Alto** | `mfa_used = false` em login | Remove a camada de defesa mais relevante contra uso de credencial comprometida |
| **Alto** | Download grande com `destination` = `removable` ou `external_storage` | É o passo que materializa exfiltração — diferente de só acessar ou visualizar |
| **Médio** | Origem de faixa `external`, sem VPN | Plausível e ambíguo por natureza — viagem, cliente, home office não cadastrado — por isso não entra no nível alto sozinho |
| **Médio** | `category` de navegação de risco (`cloud_storage`, `webmail`, `social_media`) | Canal de saída de dado, mas a ação em si (navegar) é mais fraca que transferir arquivo |
| **Médio** | Horário fora do padrão ponderado (no fuso do funcionário) | A D1 já pondera por faixa em vez de cortar fixo (D-31); o peso médio reflete que isso sozinho raramente basta |
| **Baixo** | Dispositivo pessoal autorizado vs. corporativo | Diferença pequena quando o dispositivo já está cadastrado e autorizado (D-41) |
| **Baixo** | Faixa `home` vs. `vpn` | As duas são rotas de acesso legítimas e previstas; a diferença entre elas pesa menos que a diferença entre qualquer uma delas e `external` |

> **O que esta tabela não faz:** não propõe números absolutos (ex.: "50
> pontos"), porque isso depende da escala que `detection/d1/scoring.py` já
> usa — e eu deliberadamente não abri esse arquivo para escrever esta proposta
> (seção 1). Quem implementa mapeia os três níveis para a escala real; o que
> importa preservar é a **ordem relativa**.

---

## 4. Plano de análise de sensibilidade (S12)

1. **Um fator de cada vez.** Para cada peso (os de integração da seção 2 e, se
   o tempo permitir, os de D1 da seção 3), variar ±30% a ±50% mantendo os
   demais fixos, e medir o efeito sobre as duas métricas primárias — FPR a
   revocação fixa e revocação longitudinal.
2. **Reportar como gráfico de sensibilidade** (tipo *tornado*), ordenando os
   pesos pelo tamanho do efeito. O peso de postura (seção 2) é o candidato mais
   provável a aparecer no topo.
3. **AHP, se sobrar tempo.** O plano, seção 4, já registra "AHP se houver
   tempo" como mitigação ao risco de pesos arbitrários. Daria uma comparação
   par a par formal entre os atributos da seção 3, em vez da ordenação
   qualitativa proposta aqui. Não é bloqueante: a ordenação qualitativa já é
   preliminar por definição, e a S12 é quem decide se há tempo para o AHP.

---

## 5. O que falta

- [ ] **Minha leitura final** deste arquivo
- [ ] **O Davi** mapear a ordenação da seção 3 para os valores reais de
      `detection/d1/scoring.py`, ou confirmar que já bate
- [ ] **Fechar a D-09** e mover a D-43 de "a confirmar" para "fechada" em
      `decisoes.md`, com a ratificação desta seção 2 como motivo
- [ ] **A análise de sensibilidade em si** — é da S12, sobre dados reais, não
      desta proposta
