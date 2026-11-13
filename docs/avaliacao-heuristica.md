# Avaliação heurística do painel — roteiro

Esta página é o **material de trabalho** da avaliação heurística prevista na
[usabilidade](usabilidade.md), seção 6.1, e que a Seção 4.4 do artigo hoje
declara como **não realizada**.

> **Nada aqui diz o que está errado no painel.** É de propósito: o método pede
> que cada avaliador chegue à tela sem a lista de outro na cabeça. Quem escreveu
> esta página — o assistente de IA — **não percorreu o painel para avaliá-lo**, a
> pedido do Davi em 12/11/2026, justamente para não contaminar as três
> passagens. O que está aqui é logística: o método, o caminho e a planilha.

***

## 1. As três regras que fazem o método funcionar

| | |
|---|---|
| **Sozinho** | Cada um percorre a interface **sem falar com os outros dois**. A seção 6.1 é explícita: *"Avaliar em grupo desde o início faz um avaliador contaminar o outro."* |
| **Até o fim** | Percorra o roteiro inteiro antes de consolidar. Interromper no meio enviesa o que vem depois |
| **Só depois** | As três planilhas se juntam **quando as três estiverem prontas**. Antes disso, não compare, não comente, não mande print |

**Por que três.** Nielsen recomenda de três a cinco avaliadores porque cada um
encontra cerca de um terço dos problemas. Com um só, a maior parte passa batido —
e a união só cresce se as passagens forem independentes.

## 2. Como abrir o painel

```bash
python -m streamlit run frontend/dashboard/app.py
```

A barra lateral abre em **Exemplos gravados**, que é um conjunto de respostas
guardadas — uma por rota. Para falar com a API, troque a fonte para **API**; ela
sobe com `uvicorn backend.main:app`, com `SDCAC_DADOS` apontando para o diretório
da execução. Detalhes em [o painel](painel.md).

> **Anote na planilha qual fonte você usou.** Achado encontrado nos exemplos
> gravados e achado encontrado contra a API não são a mesma coisa, e quem
> consolida precisa saber distinguir.

## 3. As dez heurísticas, e o que cada uma exige deste painel

A grade é a da [usabilidade](usabilidade.md), seção 2, escrita em setembro —
**antes** desta avaliação. A coluna da direita é o critério declarado pelo
projeto, não um achado.

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

**Uma heurística pode ser violada em vários lugares, e o mesmo lugar pode violar
várias.** Registre uma linha por par (heurística, lugar).

## 4. A escala de severidade

A de Nielsen, como a seção 6.1 adota:

| Grau | Significado | O que fazemos |
|---|---|---|
| **0** | Não é problema de usabilidade | Nada |
| **1** | Cosmético | Corrige se sobrar tempo |
| **2** | Menor | Entra no backlog |
| **3** | Maior | Corrige antes da entrega |
| **4** | Catastrófico | Bloqueia a entrega |

Severidade é **sua leitura do impacto sobre quem usa**, não do esforço de
corrigir. Um defeito trivial de consertar pode ser grau 4.

## 5. O roteiro

Percorra na ordem. Em cada parada, confronte o que está na tela com as dez
heurísticas — **todas as dez**, inclusive as que parecerem não se aplicar.

### 5.1 Antes de clicar em nada

Abra o painel e **pare**. Olhe a tela como quem nunca a viu: o que ela diz que é,
o que ela diz que está acontecendo, e o que ela oferece para fazer.

### 5.2 A barra lateral

1. A escolha da **fonte dos dados**, e o que muda ao trocar entre as duas
2. O campo de **endereço da API**, quando a fonte é API
3. O seletor de **execução**
4. A **legenda das faixas de risco**

### 5.3 Tela **Execução**

1. Os três blocos do topo — configuração, pesos, situação
2. O bloco com `config_hash`, `code_sha` e `run_id`
3. A tabela **Presets da ablação**

### 5.4 Tela **Pessoas**

1. A lista inteira: a ordem em que as pessoas aparecem
2. Um cartão de pessoa: o selo de faixa, a nota, o identificador, a linha do
   último evento e a barra de decomposição
3. O rodapé com a contagem

### 5.5 Tela **Alertas**

1. Os três filtros — **Faixa**, **Desde (ISO 8601)** e **Até (ISO 8601)**
2. Aplique um filtro de faixa. Depois tente **voltar ao estado anterior**
3. Escreva uma data nos campos ISO. Tente escrever uma **data inválida**
4. A fila com os filtros aplicados, e a fila sem nenhum

### 5.6 Tela **Decomposição do risco**

1. O seletor de **funcionário**, e o de **evento**
2. O selo de faixa e a linha de identificação do evento
3. **De onde vieram os pontos** — as cinco parcelas, a barra, e o que aparece na
   parcela que a configuração não liga
4. **Qual regra disparou** — o nome da regra, os pontos e o motivo escrito

### 5.7 Atravessando as telas

Com as quatro já vistas, volte e compare: a mesma faixa, a mesma pessoa e o mesmo
evento, vistos em telas diferentes.

### 5.8 O caminho torto

1. Aponte a fonte para a API **sem a API no ar**
2. Escolha uma execução e troque de tela no meio
3. Recarregue a página com filtros aplicados

> **Se o painel quebrar, isso é um achado** — registre e siga. Reiniciar o
> Streamlit não invalida a passagem.

## 6. A planilha

**Copie a tabela abaixo** para o Excel, para o Google Planilhas ou para o que
preferir — uma cópia por pessoa:

| avaliador | fonte | heuristica | onde | o_que_observei | por_que_viola | severidade | correcao_sugerida |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

> O mesmo cabeçalho está em
> [`docs/avaliacao-heuristica-planilha.csv`](https://github.com/Codexrocks/TCC_SDCAC/blob/main/docs/avaliacao-heuristica-planilha.csv),
> no repositório, pronto para baixar. **O site publicado não serve arquivo
> `.csv`** — ele publica páginas, e um link relativo para o arquivo dá "página
> não encontrada". Por isso a tabela está aqui também.

As colunas:

| Coluna | O que vai nela |
|---|---|
| `avaliador` | Seu nome |
| `fonte` | `exemplos gravados` ou `API` |
| `heuristica` | O número de 1 a 10 |
| `onde` | A tela e o elemento. *"Alertas, campo Desde"* — não *"na tela de alertas"* |
| `o_que_observei` | **O que a tela faz**, em uma frase. Fato, não opinião |
| `por_que_viola` | Por que isso contraria a heurística |
| `severidade` | 0 a 4 |
| `correcao_sugerida` | O que você faria. Pode ficar vazio |

**Escreva o que observou, não o que concluiu.** *"O filtro de faixa não tem como
voltar para 'todas' sem recarregar"* é verificável; *"os filtros são ruins"* não
é.

**Linha vazia é resultado.** Se você percorreu tudo e não achou violação de uma
heurística, não invente — a ausência é dado.

## 7. Quando as três estiverem prontas

1. O Davi reúne as três planilhas
2. Achados repetidos viram uma linha, com os nomes de quem encontrou e a
   **severidade mais alta** atribuída
3. O consolidado vira a tabela `heurística violada | onde | severidade |
   correção` em `docs/relatorios/`, como a seção 6.1 manda
4. A **Seção 4.4 do artigo** deixa de dizer que a avaliação não foi realizada, e
   passa a reportar o que ela encontrou

> **Achado de grau 4 bloqueia a entrega**, pela própria escala. Se aparecer um,
> ele é assunto antes de 19/11, não depois.

## 8. O que esta avaliação não é

- **Não é teste com usuários.** Não há participante, não há tarefa cronometrada,
  não há escore de satisfação — a **D-02** fechou por aí, e a Seção 3.9 do artigo
  declara isso
- **Não é avaliação de acessibilidade automática.** Contraste de 4,5:1, rótulo
  junto da cor e as cinco parcelas separadas já estão presos por teste, e a
  Seção 4.4 já os reporta. Se você vir uma violação **nova** desses pontos, ela é
  achado — e também um teste que falta
- **Não é revisão de código**
