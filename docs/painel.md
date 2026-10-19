# O painel

A frente do SDCAC, em Streamlit. Lê a API de leitura e mostra **de onde veio a
nota** de cada evento — que é a pergunta que a [usabilidade](usabilidade.md) diz
que um número sozinho não responde.

> **O painel existe desde 19/10/2026, escrito pelo Davi com Claude Opus 5.** A
> **S9 continua sendo do Filipe**: o que entrou foi a base, e a tela que a banca
> avalia é a que ele revisar e completar. O que falta está na seção
> [O que ainda é da S9](#o-que-ainda-e-da-s9).

## Como rodar

Sem servidor nem banco, com as respostas gravadas:

```bash
python -m streamlit run frontend/dashboard/app.py
```

A barra lateral abre em **Exemplos gravados**. Para falar com a API de verdade,
troque a fonte para **API** e aponte o endereço — a API sobe com:

```bash
uvicorn backend.main:app
```

com a variável `SDCAC_DADOS` apontando para o diretório onde o executor gravou.

> **Streamlit não vem com `pip install pytest`.** Ele está nas dependências do
> projeto (`pyproject.toml`), mas o CI **não o instala** de propósito — ver
> [O que o CI não cobre](#o-que-o-ci-nao-cobre).

## As quatro telas

| Tela | Rota que a alimenta | O que mostra |
|---|---|---|
| **Execução** | `/runs/{id}` e `/configurations` | Preset, pesos, situação, `config_hash` e `code_sha` — o que torna a execução reproduzível |
| **Pessoas** | `/runs/{id}/employees` | A nota mais recente de cada pessoa, da maior para a menor |
| **Alertas** | `/runs/{id}/alerts` | A fila de triagem, filtrável por faixa e período |
| **Decomposição do risco** | `/runs/{id}/events/{id}` | De onde vieram os pontos, dimensão por dimensão, e qual regra disparou |

## O que não se decide no painel

As faixas, os limiares e os pesos moram em `detection/presets.toml`, e quem
classifica é `detection.integracao.band_of`. **O painel só pinta o que o motor
decidiu** — e há teste que reprova se a legenda discordar dele.

Quem decide sobre as faixas é a **Yasmin**.

## As duas regras que viraram teste

A [usabilidade](usabilidade.md) escreve duas exigências que um Pull Request
desfaz sem ninguém notar. As duas reprovam no `pytest`:

| Exigência | Onde mora | Como é conferida |
|---|---|---|
| **A cor não é o único meio visual** (WCAG 1.4.1) | `frontend/components/faixas.py` | Os rótulos e intervalos são **lidos da tabela da seção 5.1** da `usabilidade.md` e comparados com o código. Quem manda é o documento |
| **Contraste de 4,5:1** (WCAG 1.4.3) | `frontend/components/contraste.py` | Cada par texto/fundo é **calculado**, não afirmado |

Os quatro pares medem de **7,41:1 a 13,47:1**. O amarelo sobre branco, que a
própria `usabilidade.md` nomeia como armadilha, mede **1,43:1** pela mesma
função — e reprovaria.

**O octógono é desenhado em SVG**, com os oito vértices calculados: nenhuma
fonte de texto comum tem glifo de octógono preenchido, e desenhar um hexágono
com nome de octógono seria mentir na legenda.

## Duas coisas que a decomposição faz de propósito

**As duas parcelas da D3 ficam separadas**, pela **D-25**. Somar conduta com
postura esconderia qual delas causou o alerta, que é a pergunta de quem abre a
tela.

**Nulo não é zero.** Uma parcela `null` quer dizer que a configuração **não
liga** aquela dimensão — a `c0` numa execução C3, por exemplo — e sai como `não
ligada`, em cinza. Uma parcela `0.0` quer dizer que a dimensão rodou e não achou
nada. Mostrar as duas como "0" faria a C3 parecer avaliar regras fixas sem
encontrar nada, quando ela nem as liga.

## De onde vêm os dados

Duas fontes, atrás do mesmo protocolo — a tela não sabe qual está em uso.

**`FonteHTTP`** fala com a API. É a fonte de verdade.

**`FonteExemplos`** lê `backend/exemplos.json`, que guarda **respostas reais da
API**: a execução 4, preset C3, semente 1, validadas contra o contrato por
`tests/test_exemplos.py`. Nenhum valor foi inventado.

> **O que a semente de hoje não tem.** Dois funcionários, só eventos
> `FILE_ACCESS`, **ninguém na faixa `high`** e `/metrics` vazio. É o que o campo
> `_limites` do arquivo registra. As telas renderizam isso sem quebrar e **dizem**
> o que falta, em vez de parecerem vazias por defeito.

## O que ainda é da S9

- [ ] **Revisão do Filipe.** O painel foi escrito por outra pessoa com IA; o que
      a banca vê precisa bater com quem fez · **Filipe**
- [ ] **O critério de aceite não é demonstrável** no caminho do risco alto: não
      há ninguém em `high`. Depende do **gerador de eventos da S6** ·
      **Filipe**
- [ ] **Avaliação heurística**, que a [usabilidade](usabilidade.md) seção 6.2
      marca para a S9 · **Filipe**
- [ ] **Teste com usuários na S11**, onde o "menos de 1 min" deixa de ser
      estimativa e vira medida · **Filipe**
- [ ] **A tela de Métricas não existe** — `/metrics` responde vazio porque
      nenhum avaliador gravou métrica ainda · **Davi**

## O que o CI não cobre

**Nenhum teste importa o `app.py`.** O `frontend/dashboard/app.py` é o único
módulo que importa o Streamlit, e o
[workflow de validação](../.github/workflows/validacao.yml) **não instala o
Streamlit** — a lista de dependências do CI é explícita, e foi escrita quando
nenhum teste usava a biblioteca.

A consequência, dita por extenso: **um erro dentro do `app.py` não reprova no
CI.** Import quebrado, chamada de Streamlit com argumento errado, tela que não
monta — tudo isso passa verde. O que os testes cobrem é o que está em
`components/` e no `cliente.py`, que não dependem do Streamlit, e é por isso que
eles ficaram separados do `app.py`.

Enquanto o CI não instalar o Streamlit, **quem mexer no painel roda antes**:

```bash
python -m streamlit run frontend/dashboard/app.py
```

Mudar o workflow para instalar o Streamlit toca `.github/**`, que é arquivo
protegido pelo [`AGENTS.md`](../AGENTS.md): espera de 24 h e a seção `Arquivo
protegido` preenchida. **É decisão do Davi**, e está registrada como pendência.
