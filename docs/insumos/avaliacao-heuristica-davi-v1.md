<!-- ARQUIVO DE REGISTRO — ver docs/insumos/README.md no repositório -->

# Insumo — Avaliação heurística do painel, passagem do Davi

| | |
|---|---|
| **Quem produziu** | **Davi** |
| **Entregue em** | 12/11/2026 |
| **Assistência de IA** | **Nenhuma.** A passagem foi feita a mão, percorrendo o painel pelo [roteiro](../avaliacao-heuristica.md) |
| **Conferi tudo que a IA escreveu?** | Não se aplica — não há texto de IA neste insumo |
| **Para onde vai** | `artigo/04-resultados.md`, § 4.4 e § 4.6 |

O arquivo como recebido é
[`avaliacao-heuristica-davi-v1.csv`](https://github.com/Codexrocks/TCC_SDCAC/blob/main/docs/insumos/avaliacao-heuristica-davi-v1.csv).
Esta página o transcreve — o GitBook publica página, não serve arquivo solto, e
em 12/11 um `.csv` linkado como se fosse página deu 404 na véspera da avaliação.

***

## Por que esta passagem entrou sozinha

O [roteiro](../avaliacao-heuristica.md) e a
[usabilidade](../usabilidade.md), § 6.1, pedem **três avaliadores**, porque é o
que Nielsen e Molich recomendam: cada avaliador encontra cerca de um terço dos
problemas, e a união só cresce se as passagens forem independentes.

**As passagens da Yasmin e do Filipe não chegaram.** Elas foram pedidas em
12/11, o roteiro e a planilha foram publicados no mesmo dia, e o link que dava
404 foi corrigido em 13/11. A dois dias da entrega, em **17/11/2026, o Davi
decidiu consolidar com uma passagem só** — a dele —, pela **D-46**.

O que isso custa está declarado no artigo, na § 4.6, e não escondido: **os 20
achados são um piso, não um inventário.**

> ⚠️ **Se a Yasmin ou o Filipe percorrerem o painel depois de hoje, a passagem
> não será mais independente** — esta página está publicada, e quem a ler chega
> à tela com a lista de outro na cabeça. É a contaminação que a § 6.1 descreve.
> Uma passagem posterior continua valendo como revisão; **não** como avaliador
> independente para efeito de cobertura.

## Os números da passagem

| | |
|---|---|
| Achados | **20** |
| Fonte | **19** nos exemplos gravados · **1** contra a API |
| Severidade | **5** maiores (grau 3) · **12** menores (grau 2) · **3** cosméticos (grau 1) |
| **Grau 4, catastrófico** | **nenhum** — nada bloqueia a entrega pela escala adotada |
| Heurísticas com achado | 1, 2, 3, 4, 5, 6, 7 e 9 |
| **Heurísticas sem achado** | **8** (estética e minimalismo) e **10** (ajuda e documentação) |
| Campos essenciais vazios | nenhum |

**Linha vazia é resultado**, como o roteiro diz: as heurísticas 8 e 10 foram
percorridas e não produziram violação.

## Um achado já estava corrigido quando a planilha chegou

O **achado 19** registra a fonte API derrubando a tela inteira com
`ModuleNotFoundError` e caminhos locais à mostra, grau 3, e sugere *"capturar o
erro e mostrar que não foi possível falar com a API"*. **É exatamente o que o
PR #114 fez**, mergeado em 13/11/2026.

A consequência não é descartar a linha, é saber o que ela diz: **a passagem
rodou sobre o painel de antes do #114.** Fica registrada como encontrada e
corrigida, com o número do PR — descartá-la esconderia que o defeito existiu.

## Os 20 achados, como recebidos

Transcrição do `.csv`, sem edição de conteúdo. **H** é a heurística da
[usabilidade](../usabilidade.md), § 2; **Sev** é a escala de Nielsen, de 0 a 4.

| # | H | Sev | Onde | O que observei | Por que viola | Correção sugerida |
|---|---|---|---|---|---|---|
| 1 | 1 | **3** | Barra lateral, caixa verde de status | A caixa mostra só "ok · adaptador ArquivoRepository · 4 execucoes"; nenhuma tela mostra data/hora da última ingestão nem se há eventos chegando agora. | O critério da heurística 1 pede que tela parada e sistema morto não sejam indistinguíveis; aqui não há como distinguir. | Mostrar "última ingestão: <data/hora>" na barra lateral e destacar quando passar de um limite. |
| 2 | 4 | **2** | Barra lateral, seletor Execucao × tela Execução, bloco run_id | O seletor está em "4 — C3" e o bloco da tela Execução mostra run_id 1 para a mesma execução. | O mesmo identificador de execução aparece com valores diferentes em dois lugares da mesma tela. | Usar o mesmo identificador no seletor e no bloco, ou rotular o número do seletor como posição na lista. |
| 3 | 2 | **2** | Alertas, campo Faixa | As opções são em inglês (todas, normal, low, medium, high), enquanto os selos e a legenda usam RISCO BAIXO, RISCO MÉDIO e RISCO ALTO. | Vocabulário misturado e termo técnico em inglês onde o analista espera o rótulo que vê na legenda. | Exibir NORMAL, RISCO BAIXO, RISCO MÉDIO e RISCO ALTO nas opções, guardando low/medium/high só internamente. |
| 4 | 4 | **2** | Alertas, campo Faixa × selos e legenda | As opções do filtro (low, medium, high) não coincidem com os rótulos usados nos selos da fila e na legenda da barra lateral. | A mesma faixa de risco tem um nome no filtro e outro nas demais telas. | Padronizar o rótulo da faixa em todas as telas. |
| 5 | 1 | **3** | Alertas, filtro Faixa | Ao escolher "high" e depois "medium" a fila continuou com as mesmas 14 linhas (RISCO BAIXO e NORMAL) e o rodapé continuou em "14 alerta(s)". | O filtro parece não ter efeito e a tela não informa isso: o analista não sabe se o filtro foi aplicado, se não há resultado ou se falhou. Não testado contra a API. | Aplicar o filtro, ou dizer na tela que está sem efeito nesta fonte; mostrar "0 alerta(s) para este filtro" quando vazio. |
| 6 | 9 | **3** | Alertas, campo Desde (ISO 8601) | Digitar "banana" e dar Enter foi aceito: sem mensagem de erro, sem aviso de formato inválido, e a fila ficou igual. | O sistema não diz que a data é inválida nem como corrigir. | Validar o formato e mostrar mensagem ao lado do campo, ex.: "use AAAA-MM-DDThh:mm:ssZ". |
| 7 | 5 | **2** | Alertas, campos Desde e Ate (ISO 8601) | Os campos são texto livre; não há seletor de data nem restrição de formato, e uma data inválida é aceita. | Um campo de texto livre convida ao erro que a validação deveria impedir. | Trocar por seletor de data e hora. |
| 8 | 4 | **2** | Alertas, texto de abertura × fila | O texto diz que "faixa normal nao entra na fila de proposito", mas a fila lista o evento ap-8-0-0 com selo NORMAL (01/04 06:00 · limiar 20). | A tela descreve um comportamento e faz outro. | Alinhar o texto ao comportamento (ou tirar o evento NORMAL da fila). |
| 9 | 9 | **3** | Alertas, linha de cada alerta | Cada linha mostra faixa, id do evento, data e "limiar 20"; não mostra a nota nem a regra que disparou. Para ver a regra é preciso ir à tela Decomposição e escolher pessoa e evento de novo. | O analista não consegue julgar o alerta na própria fila, sem qual regra e quantos pontos. | Incluir a nota e o nome da regra na linha, ou um link para a decomposição daquele evento. |
| 10 | 7 | **2** | Alertas, fila | A fila está em ordem de data decrescente; não há controle de ordenação (por nota) nem filtros salvos. | Quem já conhece a ferramenta não tem atalho para ver o mais grave primeiro. | Ordenar por nota por padrão, ou oferecer o controle de ordenação; permitir salvar filtros. |
| 11 | 3 | **2** | Alertas, linhas da fila | Nenhuma linha oferece ação (marcar falso positivo, descartar); não há como marcar nem desfazer. | O critério da heurística 3 pede que marcar falso positivo possa ser desfeito; a ação não existe na tela. | Adicionar "falso positivo" com opção de desfazer, se a ação fizer parte do escopo. |
| 12 | 7 | **2** | Pessoas, cartões × Decomposição do risco | O texto diz "Escolha uma para ver o historico e abrir a decomposicao", mas clicar no cartão do Funcionário 8 não fez nada; é preciso ir à tela Decomposição e escolher Funcionário e Evento nos seletores. | Sem atalho da pessoa para a decomposição dela; a promessa do texto não é cumprida. | Tornar o cartão clicável, levando à decomposição do último evento. |
| 13 | 2 | **2** | Decomposição do risco, "Qual regra disparou" | O nome da regra aparece como identificador de código (accumulated_exposure); só a frase de motivo abaixo está em português. | Vocabulário de banco de dados, não de SOC. | Mostrar um nome em português (ex.: "Exposição acumulada") com o código como detalhe secundário. |
| 14 | 2 | **1** | Decomposição do risco, linha de identificação do evento | A linha mostra o tipo do evento como FILE_ACCESS e o id como ap-8-2-5. | Códigos internos em vez de termos que o analista reconhece. | Traduzir o tipo (ex.: "Acesso a arquivo"). |
| 15 | 6 | **2** | Decomposição do risco, "De onde vieram os pontos", barra | A barra é uma única faixa cinza de largura fixa acima das linhas C0 a D3b, sem cores por parcela, rótulo ou legenda; não mostra qual parcela representa nem a proporção. | A barra não é legível sem ler os números; o analista precisa deduzir o significado. | Segmentar a barra por parcela, com cor e rótulo iguais aos das linhas da tabela. |
| 16 | 6 | **2** | Barra lateral, legenda Faixas de risco | A legenda traz só os quatro nomes (NORMAL, RISCO BAIXO, RISCO MÉDIO, RISCO ALTO), sem intervalo de pontos. | O analista tem de decorar onde cada faixa começa (ex.: que 34 é BAIXO). | Mostrar o intervalo ao lado de cada rótulo (ex.: "BAIXO · 20–49"). |
| 17 | 2 | **1** | Títulos e navegação (Execucao, Configuracao, Decomposicao do risco, Ate (ISO 8601)) | Os textos da interface estão sem acentuação. | Português sem acento passa a impressão de ferramenta inacabada. | Acentuar os textos. |
| 18 | 9 | **3** | Barra lateral, fonte API, tela inteira | Ao trocar para API (endereço http://127.0.0.1:8000) a tela principal foi substituída por um traceback ModuleNotFoundError: No module named 'httpx', com caminhos locais C:\Users\...\frontend\dashboard\app.py; só há "Copy", "Ask Google" e "Ask ChatGPT". A causa é a dependência ausente neste computador; a API não foi testada no ar. | Mensagem técnica sem explicação em português nem caminho de recuperação; expõe caminhos locais. | Capturar o erro e mostrar "não foi possível falar com a API em <endereço>" com orientação para voltar a Exemplos gravados. |
| 19 | 1 | **2** | Menu de telas (Execucao, Pessoas, Alertas, Decomposicao), depois de voltar da fonte API | Ao voltar para Exemplos gravados, o menu mostrava "Execucao" selecionada, mas o conteúdo exibido era a tela Decomposição do risco; continuou assim após esperar 2 s. | O controle de navegação não reflete a tela em que o analista está. | Sincronizar o menu com a tela ou reiniciar na tela Execução ao trocar de fonte. |
| 20 | 7 | **1** | Recarregar a página com filtro aplicado (Alertas, Faixa) | Depois de recarregar (navegação à mesma URL), a página voltou para a tela Execução e o filtro de Faixa voltou para "todas"; a execução escolhida (4 — C3) permaneceu. | Tela e filtros não persistem; quem recarrega perde o contexto. | Guardar tela e filtros na URL. |

***

## O que esta página não é

Não é a correção do painel, nem compromisso de corrigir. É o que um avaliador
observou numa passagem datada. Os cinco achados de grau 3 são os que a escala
manda **corrigir antes da entrega**, e a decisão sobre cada um é do Davi — a
entrega de 19/11 é do artigo, não do software.
