"""Gera apresentacao/roteiro.md e apresentacao/README.md a partir de roteiro.json."""
import json
import shutil
from pathlib import Path

ESC = Path(__file__).parent
SAIDA = ESC.parent
R = json.loads((ESC / "roteiro.json").read_text(encoding="utf-8"))


L = []
L.append("# Roteiro da defesa — apresentação de 30 minutos\n")
L.append("Roteiro do **Filipe**, que apresenta. A fala de cada slide é a mesma que está nas **notas do apresentador** de "
         "[`apresentacao-sdcac.pptx`](apresentacao-sdcac.pptx), com as palavras-chave e o tempo no começo. Os números são "
         "os do artigo e de [`results/agregado.md`](../results/agregado.md).\n")
L.append("> **Quem escreveu.** O rascunho da fala é de uma IA (Claude Sonnet 5.5), a pedido da Yasmin, a partir do "
         "artigo. **Quem apresenta precisa ler em voz alta, ajustar ao próprio jeito e ensaiar com cronômetro.** "
         "Onde o roteiro diz o que não dizer, é porque o artigo não sustenta.\n")
L.append("## Antes de começar\n")
L.append("- Abra o `.pptx` no **modo apresentador** do PowerPoint: a fala está nas notas.")
L.append("- Tenha um **cronômetro**. O tempo acumulado de cada slide está na tabela abaixo.")
L.append("- Leve o arquivo em **PDF** também (Arquivo, Salvar como, PDF), para o caso de o computador da sala falhar.")
L.append("- Ensaie cronometrado, como o cronograma pede (S16). Cada integrante precisa saber apresentar "
         "qualquer seção sob sorteio.")
L.append("- **27 slides, 28:50 de fala, 1:10 de folga.** Os tempos são **estimativas**, a cerca de 140 palavras "
         "por minuto. O ritmo real do Filipe pode ser outro, e só o ensaio mede.\n")

L.append("## Cola: palavras-chave de cada slide\n")
L.append("| Slide | Tempo | Acumulado | Palavras-chave |")
L.append("|---|---|---|---|")
for d in R["slides"]:
    L.append(f"| {d['n']}. {d['titulo']} | {d['tempo']} | {d['acumulado']} | " + " · ".join(d["chaves"]) + " |")
L.append("\n*Tempos estimados, não medidos.*\n")

L.append("## Se estourar no ensaio\n")
L.append("Corte nesta ordem:\n")
for i, (a, b) in enumerate(R["cortes"], 1):
    L.append(f"{i}. **{a}.** {b}")
L.append("\n**Nunca corte** os slides 19, 20 e 21 (resultados e contrapeso) nem o 24 (ameaças à validade) e o 25 (conclusão). "
         "São o que a banca avalia.\n")

L.append("## Slide a slide\n")
for d in R["slides"]:
    L.append(f"### Slide {d['n']} · {d['titulo']}\n")
    L.append(f"*{d['tempo']} · acumulado {d['acumulado']} · no slide: {d['mostrar']}*\n")
    L.append("**Palavras-chave:** " + " · ".join(d["chaves"]) + "\n")
    for p in d["fala"]:
        L.append(p + "\n")
    if d.get("cuidado"):
        L.append("> **Cuidado:** " + d["cuidado"] + "\n")
    if d.get("passe"):
        L.append("**Passe para:** “" + d["passe"] + "”\n")

L.append("## As cinco frases que não podem faltar\n")
for i, t in enumerate(R["cinco_frases"], 1):
    L.append(f"{i}. “{t}”")
L.append("")
L.append("## O que não dizer\n")
for a, b in R["nao_dizer"]:
    L.append(f"- **{a}** {b}")
L.append("")
L.append("## Perguntas prováveis da banca\n")
for q, a, quem in R["qa"]:
    L.append(f"### {q}\n")
    L.append(a + "\n")
    L.append(f"*Quem responde: {quem}.*\n")
L.append("## Quem responde o quê\n")
L.append("| Assunto | Primeiro a responder | Se travar |")
L.append("|---|---|---|")
L.append("| Arquitetura, banco, API, gerador, ingestão | Davi | Passe para o Davi |")
L.append("| Segurança, LGPD, ISO/IEC 27001, referencial, cenários, pesos | Yasmin | Passe para a Yasmin |")
L.append("| Painel, usabilidade, resultados, avaliação heurística | Filipe | Responda com o que o slide mostra |")
L.append("| Metodologia e estatística | Davi | Filipe, pelos slides 17 e 18 |")
L.append("")
(SAIDA / "roteiro.md").write_text("\n".join(L), encoding="utf-8", newline="\n")

(SAIDA / "README.md").write_text("""# Apresentação do TCC

Material da defesa, em 30 minutos, apresentada pelo Filipe.

| O que | Onde |
|---|---|
| **A apresentação**, em PowerPoint, com a fala nas notas do apresentador | [`apresentacao-sdcac.pptx`](apresentacao-sdcac.pptx) |
| **O roteiro**, com a fala, o tempo e as palavras-chave de cada slide e as perguntas prováveis da banca | [`roteiro.md`](roteiro.md) |
| **O mesmo roteiro em PDF**, em página pequena, para ler no celular | [`roteiro-filipe.pdf`](roteiro-filipe.pdf) |
| **De onde vem cada número**, e como a precisão implícita do slide 4 é calculada | [`fontes-dos-numeros.md`](fontes-dos-numeros.md) |
| **Os scripts que geram** o `.pptx`, o roteiro e o PDF | [`gerador/`](gerador/README.md) |

## Sobre a apresentação

São **27 slides**, com pegada técnico-científica e de engenharia de software: problema, referencial (autores do artigo), pergunta e hipótese, arquitetura, dados, as quatro configurações com as fórmulas de cada dimensão, protocolo, métricas e estatística, resultados, contrapeso, qualidade, ameaças à validade (Wohlin et al.), conclusão e referências. Usa as cores do painel do SDCAC, com rótulo e forma junto da cor. Os gráficos são nativos do PowerPoint, e portanto editáveis. Os números vêm do artigo e de [`results/agregado.md`](../results/agregado.md); o artigo não foi alterado.

O arquivo foi gerado por script e **conferido abrindo-o no PowerPoint 2007 e renderizando os 27 slides**. Num PowerPoint mais novo, as fontes (Cambria e Calibri) são as do próprio Office.

## Quem escreveu

O texto dos slides e do roteiro foi redigido por uma IA (Claude Sonnet 5.5), a pedido da Yasmin, a partir do artigo e de
`results/agregado.md`, e **precisa ser lido e ensaiado por quem apresenta**. A declaração de uso de IA e os erros dela
estão no [relatório da sessão 60](../docs/relatorios/2026-11-21-sessao-60.md).
""", encoding="utf-8", newline="\n")
print("ok")
