# Figuras da Seção 4

Duas figuras entram no artigo, e **as duas nascem de formas diferentes** — o que
muda o que é preciso guardar de cada uma.

| Arquivo | Como nasce | É reprodutível por comando? |
|---|---|---|
| `fpr-por-revocacao.svg` | `python -m evaluator.figuras_cli`, a partir de [`results/agregado.json`](../agregado.json) | **Sim.** Mesma entrada, mesma saída |
| `fpr-por-revocacao.png` | Conversão do SVG acima | Sim, com ferramenta de fora |
| `painel-decomposicao.png` | **Captura de tela** do painel, feita à mão em 12/11/2026 | **Não.** Ver as condições abaixo |

## A figura que sai do dado

```bash
python -m evaluator.figuras_cli
```

Lê o agregado das dez sementes e grava o **SVG**, que é o que se versiona: SVG é
texto, e um diff mostra o que mudou entre duas execuções. O PNG é derivado, e
está versionado só porque o montador do artigo precisa de imagem raster —
`python-docx` não embute SVG.

A conversão foi feita com o LibreOffice, que não é dependência do projeto:

```bash
soffice --headless --convert-to png --outdir results/figuras results/figuras/fpr-por-revocacao.svg
```

**Por que não matplotlib.** Não é por ele ser dependência nova — o
`pyproject.toml` **já o declara**, e ele só não está instalado nesta máquina. É
porque o CI instala `pytest pyyaml fastapi httpx` e mais nada: um teste que
importasse matplotlib seria **pulado em silêncio** na nuvem —
exatamente o modo de falhar que `tests/test_dependencias_do_ci.py` existe para
pegar. O desenho em SVG sai de função pura, e função pura tem teste.

**Preto, traço e marcador — não cor.** A [usabilidade](../../docs/usabilidade.md)
seção 5.1 diz que a cor não pode ser o único meio visual, e a razão vale igual no
papel: o artigo pode ser impresso em preto e branco. Cada série se distingue por
**traço, marcador e legenda** — três meios, nenhum deles a cor.

## A captura do painel, e o que ela não é

`painel-decomposicao.png` é uma **captura de tela**, feita à mão. Não há comando
que a refaça igual, e por isso as condições ficam escritas aqui:

| | |
|---|---|
| **Quando** | 12/11/2026 |
| **O que estava rodando** | `python -m streamlit run frontend/dashboard/app.py` |
| **Fonte dos dados** | **Exemplos gravados** — [`backend/exemplos.json`](../../backend/exemplos.json), e não a API |
| **Execução** | `4 — C3` |
| **Evento** | `ap-8-2-5` · `FILE_ACCESS` · 03/04 13:30 |
| **Tema** | claro, para impressão |
| **Recorte** | a coluna de conteúdo, do selo de faixa até a última parcela |

**Só existe um evento nos exemplos gravados**, e é esse. Não houve escolha de
qual mostrar — o conjunto gravado tem um, e a captura é dele.

> **O que a captura mostra, e é o que a Seção 4.4 reporta:** as cinco parcelas
> separadas, cada uma com a pergunta escrita em palavras; a parcela que a
> configuração não liga aparecendo como **—**, e não como zero; e o selo de
> faixa trazendo **rótulo textual junto da cor**.

## Se o painel mudar

A captura envelhece, e envelhece em silêncio: a tela muda, o arquivo fica. Ao
mexer no painel, **refaça a captura nas condições da tabela acima** ou troque a
figura. Uma imagem que não corresponde mais à tela é pior do que nenhuma.
