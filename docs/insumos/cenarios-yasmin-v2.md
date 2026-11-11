<!-- ARQUIVO DE REGISTRO — ver docs/insumos/README.md no repositório -->

# Insumo — Cenários, rótulos e desenho cego (D-06 e D-16), v2

| | |
|---|---|
| **Quem produziu** | **Yasmin** — dona dos cenários e rótulos, pelas decisões D-06 e D-16 |
| **Entregue em** | 10/11/2026 |
| **Substitui** | `cenarios-yasmin-v1.md`, que fica como registro — não foi editado, conforme a regra da pasta de insumos |
| **Assistência de IA** | Rascunho integral produzido por Claude Sonnet 5, a pedido direto |
| **Conferi tudo que a IA escreveu?** | **Ainda não** — proposta até leitura e confirmação |
| **Para onde vai** | `artigo/03-metodologia.md` § 3.4 (lacuna 1) · `docs/banco-simulado.md` § 10 (P18 a P23) · pendência nova para `generator/scenarios.py` (Filipe) |

---

## 1. O que mudou da v1 para a v2

A v1 ratificou o catálogo **tal como o código `generator/scenarios.py` o implementa hoje**: 19 episódios na família N (N01 a N05), 71 no total.

**A Yasmin decidiu, em 10/11/2026, que a versão correta é a de um artigo
consolidado que está na pasta do Google Drive** (fora do GitHub) —
`Artigo TCC - Avaliação multidimensional de risco comportamental em logs de
eventos_...docx`, e seu equivalente `.md`. A Metodologia desse artigo já traz a
§ 3.4 fechada, com uma família N de **seis** cenários (N01 a **N06**) e **72**
episódios, totalizando **124** por semente — não 71.

Esta v2 ratifica **essa** versão. A diferença entre as duas não é de opinião:
**é um cenário (N06) e uma prevalência que o código ainda não tem.** A v1 não
estava errada sobre o que o código faz hoje; está desatualizada em relação ao
que a Yasmin define como a versão correta do catálogo.

---

## 2. Conferência cruzada — o que bate, e o que não bate

| Família | Artigo do Drive (correto, por decisão da Yasmin) | `generator/scenarios.py` (código atual) | Bate? |
|---|---|---|---|
| P — pontuais | P01 a P06, 24 episódios | P01 a P06, 24 episódios | ✅ Idêntico |
| B — de contexto | B01 a B04, 16 episódios | B01 a B04, 16 episódios | ✅ Idêntico |
| L — longitudinais | L01 a L04, 12 episódios | L01 a L04, 12 episódios | ✅ Idêntico |
| **N — controle negativo** | **N01 a N06, 72 episódios** | **N01 a N05, 19 episódios** | ❌ **Falta o N06, e falta prevalência** |
| **Total** | **124** | 71 | ❌ |

Conferido no histórico do git (`git log -p --follow -- generator/scenarios.py`):
o arquivo **nunca** teve um `N06` desde que entrou, em 04/11/2026 pelo #89. Não
é regressão nem perda de código — é uma peça que ainda não foi escrita.

**P, B e L já estão certos.** Só a família N precisa de trabalho novo, e esse
trabalho é do Filipe, no gerador — não da Yasmin, que especifica o cenário, não
o implementa.

---

## 3. O cenário N06, especificado

O artigo do Drive nomeia o sexto cenário como **"janelas de manutenção noturna
de TI"**, sem detalhar a implementação. A especificação abaixo segue o mesmo
desenho cego da v1 — só com o catálogo de eventos e a matriz de acesso do
banco simulado, sem olhar `detection/*`.

**N06 — janelas de manutenção noturna de TI (legítimo)**

A persona **TI privilegiado** já prevê, pela **D-38**, calendário "seg-sex +
**12 janelas de manutenção noturnas**" — é tráfego de fundo que o gerador já
produz como rotina, não como cenário injetado. O N06 formaliza uma amostra
dessas janelas como episódio explícito no `ground_truth`, rotulado como **não
anômalo**: acesso ao console de infraestrutura (`restricted`, pela matriz da
**D-39**) fora do horário comercial, mas dentro de uma janela de manutenção
agendada, sem download de volume incomum, sem dispositivo removível e sem
alteração de privilégio além do necessário para a manutenção.

**Por que isso precisa existir como episódio rotulado, e não só como ruído de
fundo:** sem o rótulo explícito, a avaliação não consegue medir se o sistema
classifica esse acesso noturno privilegiado como falso positivo — e é
precisamente o tipo de acesso que a C0 (horário fixo 06h-22h) dispararia com
mais força, por tocar justamente o recurso `restricted`.

**Um ponto de desenho que o Filipe precisa resolver ao implementar:** o N06
tem sobreposição de superfície com o **B02** (recurso novo, já elegível para a
persona `it_privileged`) e com o **P03** (escalada de privilégio noturna, que
também usa o TI privilegiado à noite). A diferença pretendida: B02 é sobre
recurso que a pessoa nunca acessou; P03 é sobre conduta indevida (escalada,
MFA desligado); **N06 é acesso de rotina, a recurso já habitual da pessoa,
dentro de uma janela agendada e sem nenhuma conduta de risco.** Vale conferir,
na implementação, que os três não acabem competindo pelo mesmo sujeito na
mesma semente.

---

## 4. A tabela nominal — versão corrigida para a lacuna 1 da Metodologia § 3.4

(As famílias P, B e L repetem a v1, sem mudança — reproduzidas aqui só para a
tabela ficar completa num lugar só.)

### P — pontuais (D1, verdadeiro positivo de evento isolado) — 24 episódios

| Código | O que é |
|---|---|
| P01 | Força bruta: 15-40 tentativas em <2 min, de faixa externa, sucesso após bloqueio |
| P02 | Download de recurso restrito seguido de dispositivo removível |
| P03 | Escalada de privilégio noturna, MFA desligado, acesso ao console |
| P04 | Acesso externo sem VPN e sem MFA, madrugada |
| P05 | Exfiltração rápida via nuvem, mesma sessão |
| P06 | Conta comum tenta alterar permissões à noite, bloqueada |

### B — de contexto (D2, divergência do padrão individual) — 16 episódios

| Código | O que é |
|---|---|
| B01 | Volume ~5× o habitual, dentro do horário e da faixa de rede do escritório |
| B02 | Varredura de recursos já permitidos, nunca tocados, sigilo baixo |
| B03 | Sessão 20h-22h, dentro do corte fixo da C0, fora do hábito da pessoa |
| B04 | Origem doméstica inédita, sem viagem declarada, no horário |

### L — longitudinais (D3, escalada gradual) — 12 episódios

| Código | O que é |
|---|---|
| L01 | 21 dias de downloads crescentes migrando para storage externo |
| L02 | 20 dias ampliando acesso a recursos novos, do sigilo baixo ao alto |
| L03 | MFA desligado, patch parado, cópia física recorrente, phishing clicado |
| L04 | 20 dias de sessão remota noturna deslizando de 19h para 2h |

### N — controle negativo (todas, falso positivo legítimo) — **72 episódios**

| Código | O que é |
|---|---|
| **N01** | **Escalada legítima por mudança de projeto — é o cenário da D-16** |
| N02 | MFA desligado e religado na mesma noite, por troca de aparelho |
| N03 | Volume ~2× e expediente até 21h30, fechamento financeiro mensal |
| N04 | Troca de senha seguida de bloqueio por erro de digitação |
| N05 | Entrega de projeto: download grande para disco local, não removível |
| **N06** | **Janela de manutenção noturna de TI, agendada e sem conduta de risco — especificado na seção 3** |

O N01 continua sendo o que fecha a D-16 diretamente — isso não mudou entre a
v1 e a v2.

---

## 5. P18 a P23, atualizadas

As respostas da v1 continuam valendo para P18 (catálogo, com N06 acrescido),
P21 (rótulos) e P22 (desenho cego — a leitura do artigo do Drive para esta v2
também não envolveu nenhum arquivo de `detection/`). **Duas mudam:**

| Pergunta | O que muda na v2 |
|---|---|
| **P19 — prevalência** | A família N passa de 19 para **72** episódios por semente. O código ainda reflete 19 (3-4 por tipo); chegar a 72 com 6 tipos não é só "acrescentar N06 com a mesma cadência das outras" — **é recálculo que cabe ao Filipe**, não uma conta que a Yasmin deva inventar aqui |
| **P23 — seleção de sujeitos** | O alerta da v1 sobre L01/L02 não coincidir com N01 na mesma semente continua valendo, e ganha um segundo: **B02, P03 e N06 competem pelo mesmo perfil (`it_privileged`)** — o Filipe precisa garantir que o sorteio não sobreponha os três no mesmo funcionário na mesma semente, ou a leitura dos resultados fica ambígua |

---

## 6. O que ainda falta para fechar de vez

- [ ] **Minha leitura final** deste arquivo
- [ ] **O Filipe implementar o N06** em `generator/scenarios.py` e recalibrar a
      prevalência da família N de 19 para 72 episódios — **é o item novo e
      bloqueante que esta v2 traz**
- [ ] **O Filipe confirmar** que B02, P03 e N06 não sorteiam o mesmo sujeito na
      mesma semente, pelo mesmo motivo do L01/N01 já registrado na v1
- [ ] **O Davi** registrar o fechamento de D-06 e D-16 em `decisoes.md` e
      `quadro.toml`, e atualizar `banco-simulado.md` § 10 com os 124 episódios
      como número correto (hoje a seção 9 ainda fala em "124 episódios" obtidos
      de uma execução real — **conferir se aquela execução já tinha o N06**, ou
      se o número de 124 foi copiado do artigo do Drive sem rodar o código. As
      duas hipóteses levam a ações diferentes)
- [ ] **Colar a tabela da seção 4** na `artigo/03-metodologia.md` § 3.4, no
      lugar do bloco "A escrever — lacuna 1" — ela já é, em essência, a mesma
      tabela que o artigo do Drive usa, só com a procedência de cada linha
      explicitada
