"""PDF do roteiro do Filipe, em página pequena para ler no celular."""
import json
import os
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)

ESC = Path(__file__).parent
SAIDA = sys.argv[1]
R = json.loads((ESC / "roteiro.json").read_text(encoding="utf-8"))

FONTS = Path(os.environ.get("FONTES", r"C:\Windows\Fonts"))  # Arial: arial.ttf, arialbd.ttf, ariali.ttf, arialbi.ttf
pdfmetrics.registerFont(TTFont("F", str(FONTS / "arial.ttf")))
pdfmetrics.registerFont(TTFont("F-B", str(FONTS / "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("F-I", str(FONTS / "ariali.ttf")))
pdfmetrics.registerFont(TTFont("F-BI", str(FONTS / "arialbi.ttf")))
pdfmetrics.registerFontFamily("F", normal="F", bold="F-B", italic="F-I", boldItalic="F-BI")

INK = colors.HexColor("#1F2430")
GRAY = colors.HexColor("#4A5568")
MIST = colors.HexColor("#C9D0DC")
PAPER = colors.HexColor("#EDEFF2")
BLUE = colors.HexColor("#0B3B8C")
BLUE_BG = colors.HexColor("#D8E6FF")
AMBER = colors.HexColor("#5A4100")
AMBER_BG = colors.HexColor("#FFF0BF")
RED = colors.HexColor("#8C1007")
RED_BG = colors.HexColor("#FFDAD6")


def st(nome, **kw):
    base = dict(fontName="F", fontSize=11.5, leading=16, textColor=INK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(nome, **base)


H1 = st("h1", fontName="F-B", fontSize=21, leading=25, spaceAfter=4)
H2 = st("h2", fontName="F-B", fontSize=15, leading=19, textColor=BLUE, spaceBefore=4, spaceAfter=6)
H3 = st("h3", fontName="F-B", fontSize=13, leading=17, spaceAfter=3)
SUB = st("sub", fontSize=10.5, leading=14, textColor=GRAY, spaceAfter=6)
BODY = st("body", spaceAfter=7)
FALA = st("fala", fontSize=12, leading=17.5, spaceAfter=8)
KEY = st("key", fontName="F-B", fontSize=11, leading=15, textColor=BLUE, spaceAfter=7)
SMALL = st("small", fontSize=9.5, leading=12.5, textColor=GRAY)
CELL = st("cell", fontSize=9.5, leading=12.5)
CELLB = st("cellb", fontName="F-B", fontSize=9.5, leading=12.5)
ALERT = st("alert", fontSize=10.5, leading=14.5, textColor=RED)
PASSE = st("passe", fontSize=10.5, leading=14.5, textColor=BLUE)
CARE = st("care", fontSize=10.5, leading=14.5, textColor=AMBER)


def P(t, s=BODY):
    return Paragraph(escape(t).replace("\n", "<br/>"), s)


def caixa(texto, estilo, fundo):
    t = Table([[Paragraph(escape(texto), estilo)]], colWidths=[None])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fundo), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


# ---- slides: titulo e fala vindos de roteiro.json, a mesma fonte das notas do .pptx
slides = []
for d in R["slides"]:
    paras = list(d["fala"])
    if d.get("cuidado"):
        paras.append("CUIDADO: " + d["cuidado"])
    if d.get("passe"):
        paras.append("PASSE PARA: “" + d["passe"] + "”")
    slides.append((d["n"], d["titulo"], paras))
assert len(slides) == 27


def rodape(c, d):
    c.saveState()
    c.setFont("F", 8.5)
    c.setFillColor(GRAY)
    c.drawString(14 * mm, 8 * mm, "Roteiro da defesa · Filipe · SDCAC")
    c.drawRightString(A5[0] - 14 * mm, 8 * mm, f"{d.page}")
    c.restoreState()


doc = BaseDocTemplate(SAIDA, pagesize=A5, leftMargin=14 * mm, rightMargin=14 * mm, topMargin=13 * mm,
                      bottomMargin=16 * mm, title="Roteiro da defesa — SDCAC", author="Yasmin Teles Vales",
                      subject="Roteiro do Filipe para a defesa do TCC, em 30 minutos")
fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f", leftPadding=0, rightPadding=0,
           topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=rodape)])
LARG = doc.width

h = []
h += [P("Roteiro da defesa", H1),
      P("Para o Filipe · 30 minutos · 27 slides · 28:10 de fala, 1:50 de folga", SUB),
      caixa("Rascunho de IA, a pedido da Yasmin, a partir do artigo. Leia em voz alta, ajuste ao seu jeito e "
            "ensaie com cronômetro: o ritmo foi estimado, não medido.", CARE, AMBER_BG),
      Spacer(1, 8),
      P("Cola: palavras-chave de cada slide", H2)]

linhas = [[Paragraph("Slide", CELLB), Paragraph("Tempo", CELLB), Paragraph("Palavras-chave", CELLB)]]
for (n, tit, _), d in zip(slides, R["slides"]):
    linhas.append([Paragraph(f"<b>{n}</b>", CELL), Paragraph(f"{d['tempo']}<br/><font color='#4A5568'>{d['acumulado']}</font>", CELL),
                   Paragraph(f"<b>{escape(tit)}</b><br/>" + escape(" · ".join(d["chaves"]).replace("≠", "não é")), CELL)])
tab = Table(linhas, colWidths=[11 * mm, 15 * mm, LARG - 26 * mm], repeatRows=1)
tab.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PAPER), ("LINEBELOW", (0, 0), (-1, -1), 0.4, MIST),
                         ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4),
                         ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                         ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
h += [tab, PageBreak()]

h += [P("As cinco frases que não podem faltar", H2)]
for i, t in enumerate(R["cinco_frases"], 1):
    h.append(P(f"<b>{i}.</b> “{t}”".replace("<b>", "").replace("</b>", ""), BODY))
h += [Spacer(1, 4), P("O que não dizer", H2)]
for a, b in R["nao_dizer"]:
    h.append(caixa(f"{a} {b}", ALERT, RED_BG))
    h.append(Spacer(1, 4))
corte = [Spacer(1, 6), P("Se estourar no ensaio", H2), P("Corte nesta ordem:", BODY)]
for i, (a, b) in enumerate(R["cortes"], 1):
    corte.append(P(f"{i}. {a}. {b}", BODY))
corte.append(caixa("Nunca corte os slides 19, 20 e 21 (resultados e contrapeso) nem o 25 (ameaças à validade). São o que a "
                   "banca avalia.", CARE, AMBER_BG))
h.append(KeepTogether(corte))
h.append(PageBreak())

h.append(P("Slide a slide", H1))
for (n, tit, paras), d in zip(slides, R["slides"]):
    bloco = [P(f"Slide {n} · {d['tempo']} · acumulado {d['acumulado']}", st(f"t{n}", fontName="F-B", fontSize=9.5,
              leading=12, textColor=GRAY, spaceBefore=10)),
             P(tit, H3), P("No slide: " + d["mostrar"], SMALL), Spacer(1, 3),
             P("Palavras-chave: " + " · ".join(d["chaves"]).replace("≠", "não é"), KEY)]
    extras = []
    for p in paras:
        if p.startswith("PASSE PARA:"):
            extras.append(Spacer(1, 2))
            extras.append(caixa(p, PASSE, BLUE_BG))
        elif p.startswith("CUIDADO:"):
            vermelho = p.startswith("CUIDADO: NÃO DIGA")
            extras.append(Spacer(1, 2))
            extras.append(caixa(p, ALERT if vermelho else CARE, RED_BG if vermelho else AMBER_BG))
        else:
            bloco.append(P(p, FALA))
    h.append(KeepTogether(bloco[:5]))
    h += bloco[5:] + extras
h.append(PageBreak())

h.append(P("Perguntas prováveis da banca", H1))
for q, a, quem in R["qa"]:
    h.append(KeepTogether([P(q, H3), P(a, FALA), P(f"Quem responde: {quem}", SMALL), Spacer(1, 6)]))
h += [Spacer(1, 4), P("Quem responde o quê", H2)]
resp = [["Assunto", "Primeiro a responder"],
        ["Arquitetura, banco, API, gerador, ingestão", "Davi"],
        ["Segurança, LGPD, ISO/IEC 27001, referencial, cenários, pesos", "Yasmin"],
        ["Painel, usabilidade, resultados, avaliação heurística", "Filipe"],
        ["Metodologia e estatística", "Davi; Filipe pelos slides 17 e 18"]]
t = Table([[Paragraph(c, CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(resp)],
          colWidths=[LARG - 38 * mm, 38 * mm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PAPER), ("LINEBELOW", (0, 0), (-1, -1), 0.4, MIST),
                       ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 3)]))
h.append(t)
doc.build(h)
print("gravado:", SAIDA)
