"""Apresentação do SDCAC, em PowerPoint, com pegada técnico-científica (python-pptx). 27 slides, 30 min."""
import json
import re
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import (XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION,
                             XL_TICK_MARK)
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

AQUI = Path(__file__).parent
R = json.loads((AQUI / "roteiro.json").read_text(encoding="utf-8"))
SAIDA = sys.argv[1]

INK, PAPER, WHITE, GRAY, MIST = "1F2430", "EDEFF2", "FFFFFF", "4A5568", "C9D0DC"
BLUE, BLUE2, BLUE3, BLUE_BG = "0B3B8C", "3B6FC4", "7FA6E8", "D8E6FF"
AMBER, AMBER_BG, RED, RED_BG = "5A4100", "FFF0BF", "8C1007", "FFDAD6"
HEAD, BODY, MONO = "Cambria", "Calibri", "Consolas"
W, MX = 13.333, 0.7
TOTAL = len(R["slides"])

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
_n = [0]


def rgb(h):
    return RGBColor.from_string(h)


def novo(dark=False):
    _n[0] += 1
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(INK if dark else WHITE)
    return s


def _run(p, texto, o, base):
    r = p.add_run()
    r.text = texto
    f = r.font
    f.name = o.get("font", base["font"])
    f.size = Pt(o.get("size", base["size"]))
    f.bold = o.get("bold", base["bold"])
    f.italic = o.get("italic", base["italic"])
    f.color.rgb = rgb(o.get("color", base["color"]))


def txt(s, content, x, y, w, h, size=16, bold=False, italic=False, color=INK, font=BODY, align="l",
        anchor="t", after=0):
    """content: str ou lista de str/dict. Dict: {'t': texto} ou {'runs': [(texto, opts), ...]}."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE}[anchor]
    base = {"font": font, "size": size, "bold": bold, "italic": italic, "color": color}
    itens = content if isinstance(content, list) else [content]
    for i, it in enumerate(itens):
        d = it if isinstance(it, dict) else {"t": it}
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[d.get("align", align)]
        p.space_after = Pt(d.get("after", after))
        b = dict(base)
        for k in ("font", "size", "bold", "italic", "color"):
            if k in d:
                b[k] = d[k]
        for texto, o in (d["runs"] if "runs" in d else [(d["t"], {})]):
            _run(p, texto, o, b)
        if d.get("bullet"):
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", "228600")
            pPr.set("indent", "-228600")
            etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Arial")
            etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
    return tb


def forma(s, tipo, x, y, w, h, fill, linha=None, lw=0.75, raio=None):
    sh = s.shapes.add_shape(tipo, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = rgb(fill)
    if linha:
        sh.line.color.rgb = rgb(linha)
        sh.line.width = Pt(lw)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    if raio is not None:
        sh.adjustments[0] = raio
    return sh


def linha(s, x1, y1, x2, y2, cor=GRAY, lw=1.0):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(cor)
    c.line.width = Pt(lw)
    return c


def seta(s, x1, y1, x2, y2, cor=GRAY, lw=1.5):
    c = linha(s, x1, y1, x2, y2, cor, lw)
    etree.SubElement(c.line._get_or_add_ln(), qn("a:tailEnd")).set("type", "triangle")


def titulo(s, t, dark=False):
    txt(s, t, MX, 0.5, W - 2 * MX, 1.2, size=30, bold=True, color=PAPER if dark else INK, font=HEAD)


def rodape(s, dark=False):
    c = MIST if dark else GRAY
    txt(s, "SDCAC · TCC 2026/2", MX, 7.0, 5, 0.3, size=11, color=c)
    txt(s, f"{_n[0]} / {TOTAL}", W - MX - 1.5, 7.0, 1.5, 0.3, size=11, color=c, align="r")


def legenda(s, t, x, y, w):
    txt(s, t, x, y, w, 0.3, size=12, italic=True, color=GRAY)


def notas(s):
    d = R["slides"][_n[0] - 1]
    partes = ["PALAVRAS-CHAVE: " + "  ·  ".join(d["chaves"]), f"[{d['tempo']}  ·  acumulado {d['acumulado']}]",
              "\n\n".join(d["fala"])]
    if d.get("cuidado"):
        partes.append("CUIDADO: " + d["cuidado"])
    if d.get("passe"):
        partes.append("PASSE PARA: “" + d["passe"] + "”")
    s.notes_slide.notes_text_frame.text = "\n\n".join(partes)


def tabela(s, x, y, colw, linhas, alturas, size=14, hsize=12, cab=True, negrito_1a=False):
    """Tabela de artigo: réguas finas, sem fundo e sem linhas verticais. linhas[0] é o cabeçalho."""
    total = sum(colw)
    linha(s, x, y, x + total, y, INK, 1.5)
    cy = y
    for r, (cels, h) in enumerate(zip(linhas, alturas)):
        cx = x
        for c, (cel, w) in enumerate(zip(cels, colw)):
            e_cab = cab and r == 0
            conteudo = cel if isinstance(cel, (list, dict)) else {"t": cel}
            if isinstance(conteudo, dict):
                conteudo = [conteudo]
            txt(s, conteudo, cx + 0.08, cy + 0.07, w - 0.16, h - 0.1, size=hsize if e_cab else size,
                bold=e_cab or (negrito_1a and c == 0), color=GRAY if e_cab else INK)
            cx += w
        cy += h
        ultimo = r == len(linhas) - 1
        linha(s, x, cy, x + total, cy, INK if (r == 0 and cab) or ultimo else MIST,
              0.75 if (r == 0 and cab) else (1.5 if ultimo else 0.5))
    return cy


def bloco_formula(s, x, y, w, h, linhas_txt, rotulo=None, size=13):
    forma(s, MSO_SHAPE.RECTANGLE, x, y, w, h, PAPER)
    itens = []
    if rotulo:
        itens.append({"t": rotulo, "font": BODY, "size": 12, "bold": True, "color": GRAY, "after": 3})
    for l in linhas_txt:
        itens.append({"t": l, "font": MONO, "size": size, "after": 2})
    txt(s, itens, x + 0.15, y + 0.1, w - 0.3, h - 0.15)


def estilo_chart(chart, leg=None):
    chart.font.name = BODY
    chart.font.size = Pt(13)
    chart.font.color.rgb = rgb(INK)
    if leg is None:
        chart.has_legend = False
    else:
        chart.has_legend = True
        chart.legend.position = leg
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(13)


def barras_h(s, x, y, w, h, cats, vals, cores, fmt, maxv, fonte_rot=14):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("serie", vals)
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    estilo_chart(ch)
    ch.has_title = False
    ser = ch.plots[0].series[0]
    for i, cor in enumerate(cores):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(cor)
    pl = ch.plots[0]
    pl.gap_width = 45
    pl.has_data_labels = True
    dl = pl.data_labels
    dl.number_format = fmt
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(15)
    dl.font.bold = True
    dl.font.color.rgb = rgb(INK)
    ch.category_axis.reverse_order = True
    ch.category_axis.tick_labels.font.size = Pt(fonte_rot)
    ch.category_axis.format.line.fill.background()
    ch.value_axis.tick_label_position = XL_TICK_LABEL_POSITION.NONE
    ch.value_axis.major_tick_mark = XL_TICK_MARK.NONE
    ch.value_axis.format.line.fill.background()
    ch.value_axis.visible = False
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.minimum_scale = 0
    ch.value_axis.maximum_scale = maxv
    return ch


FAIXAS = [("NORMAL", None, PAPER, INK, GRAY, "sem forma", "≤ 20"),
          ("RISCO BAIXO", MSO_SHAPE.OVAL, BLUE_BG, BLUE, None, "círculo", "≤ 50"),
          ("RISCO MÉDIO", MSO_SHAPE.ISOSCELES_TRIANGLE, AMBER_BG, AMBER, None, "triângulo", "≤ 75"),
          ("RISCO ALTO", MSO_SHAPE.OCTAGON, RED_BG, RED, None, "octógono", "> 75")]


def chip(s, x, y, w, h, f, faixa_num=False):
    rot, tipo, bgc, fg, borda, nome, lim = f
    forma(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, bgc, linha=borda or bgc, lw=1 if borda else 0.5, raio=0.12)
    tx = x + 0.2
    if tipo is not None:
        g = h * 0.42
        forma(s, tipo, x + 0.2, y + (h - g) / 2, g, g, fg)
        tx = x + 0.2 + g + 0.12
    sufixo = f"  ·  {lim}" if faixa_num else f"  ·  {nome}"
    txt(s, rot + sufixo, tx, y, w - (tx - x) - 0.1, h, size=13, bold=True, color=fg, anchor="m")


def cit(t, size=13):
    return (t, {"color": BLUE, "size": size})


# ================================================================== 1 capa
s = novo(True)
txt(s, "Avaliação multidimensional de risco comportamental em logs de eventos", MX, 1.3, 10.8, 1.9,
    size=38, bold=True, color=PAPER, font=HEAD)
txt(s, "Comparação com regras fixas em ambiente corporativo simulado", MX, 3.2, 10.8, 0.5, size=22, color=MIST)
txt(s, "Davi Soares Dilly  ·  Filipe Fernandes de Aguiar  ·  Yasmin Teles Vales", MX, 4.5, 11, 0.4, size=18, color=PAPER)
txt(s, "Centro Universitário UNA  ·  Orientador: Prof. Euzébio D. de Souza  ·  TCC 2026/2", MX, 4.95, 11, 0.4,
    size=15, color=MIST)
txt(s, [{"runs": [("Palavras-chave: ", {"bold": True}),
                  ("risco comportamental · análise de logs · detecção de anomalias · regras fixas · "
                   "ambiente corporativo simulado", {})]}], MX, 6.35, 11.8, 0.6, size=14, color=MIST)
notas(s)

# ============================================================== 2 estrutura
s = novo()
titulo(s, "Estrutura da apresentação")
blocos = [("Contexto e referencial", "slides 3 a 7"), ("Pergunta e hipótese", "slide 8"),
          ("Sistema e modelo", "slides 9 a 16"), ("Método", "slides 17 e 18"), ("Resultados", "slides 19 a 21"),
          ("Qualidade e validade", "slides 22 a 24"), ("Conclusão e referências", "slides 25 a 27")]
for i, (a, b) in enumerate(blocos):
    y = 1.75 + i * 0.7
    txt(s, str(i + 1), MX, y, 0.6, 0.6, size=28, bold=True, color=BLUE, font=HEAD)
    txt(s, a, MX + 0.8, y + 0.05, 7.0, 0.5, size=22, bold=True)
    txt(s, b, 9.0, y + 0.1, 3.6, 0.5, size=16, color=GRAY)
rodape(s)
notas(s)

# ================================================================ 3 problema
s = novo()
titulo(s, "A regra fixa sobre evento isolado tem três limites")
itens = [
    ("1", "O evento isolado não carrega o padrão esperado de quem o produziu.",
     "Falha de autenticação é evento discreto; abuso de autorização é feito de ações permitidas, e destoa a ordem, o volume ou a combinação.",
     "[Kent e Souppaya, 2006; Grassi et al., 2017; Sandhu et al., 1996]"),
    ("2", "A raridade do evento malicioso faz o falso positivo dominar a fila.",
     "Falácia da taxa-base: com a proporção de ataques pequena, a precisão cai mesmo com FPR baixa.", "[Axelsson, 2000]"),
    ("3", "O custo é humano: o ruído vira exaustão e degrada a triagem.",
     "Descompasso entre o volume de alertas e a capacidade de análise, sem contexto comportamental.",
     "[Sundaramurthy et al., 2015; Vielberth et al., 2020]"),
]
for i, (n, a, b, c) in enumerate(itens):
    y = 1.85 + i * 1.65
    txt(s, n, MX, y, 0.6, 0.8, size=40, bold=True, color=BLUE, font=HEAD)
    txt(s, [{"t": a, "size": 19, "bold": True, "after": 3}, {"t": b, "size": 16, "color": GRAY, "after": 3},
            {"runs": [cit(c, 14)]}], MX + 0.8, y, 10.8, 1.5)
rodape(s)
notas(s)

# =========================================================== 4 taxa-base
s = novo()
titulo(s, "A falácia da taxa-base, com os números do experimento")
bloco_formula(s, MX, 1.85, 5.2, 1.25, ["P(malicioso | alerta) =", "TPR·p / ( TPR·p + FPR·(1 − p) )"],
              rotulo="Axelsson (2000)", size=14)
txt(s, [{"runs": [("p = 0,18%", {"bold": True, "color": BLUE}), ("  dos eventos são maliciosos (2.583 de 1.436.275 por semente).", {})], "after": 8},
        {"runs": [("TPR = 0,20", {"bold": True, "color": BLUE}), ("  e a FPR que medimos em cada configuração.", {})], "after": 8},
        {"t": "Resultado: um alerta verdadeiro a cada 513 na C0, e a cada 12 na C2.", "bold": True}],
    MX, 3.35, 5.2, 2.2, size=15)
txt(s, [{"runs": [("Atenção: ", {"bold": True, "color": RED}),
                  ("os valores do gráfico vêm da fórmula, e não são medida do experimento. A precisão medida no limiar de "
                   "operação, que não foi calibrado, é 0,32% na C0 e 0,57% na C2.", {})]}], MX, 5.6, 5.2, 1.3, size=13, color=GRAY)
barras_h(s, 6.3, 1.85, 6.4, 4.4, ["C0  (1 em 513)", "C1  (1 em 168)", "C2  (1 em 12)", "C3  (1 em 16)"],
         [0.20, 0.59, 8.26, 6.26], [GRAY, GRAY, BLUE, BLUE], '0.00"%"', 10.5)
legenda(s, "Figura 1 — Precisão implícita, em %, com TPR = 0,20 e p = 0,18%. Cálculo dos autores a partir de Axelsson (2000) e de results/agregado.md.",
        6.3, 6.3, 6.4)
rodape(s)
notas(s)

# ==================================================== 5 referencial: domínio
s = novo()
titulo(s, "Referencial: o domínio do problema")
rows = [
    ["Autor (ano)", "Contribuição", "Uso no trabalho"],
    ["Kent e Souppaya (2006)", "Gestão de logs (NIST SP 800-92); volume e diversidade dificultam a leitura.", "O registro é a evidência."],
    ["Grassi et al. (2017); Sandhu et al. (1996)", "Autenticação verifica a identidade; autorização decide as ações, por papéis.", "Abuso é feito de ações permitidas."],
    ["Gonzalez-Granadillo et al. (2021)", "SIEM: correlação por regras escritas à mão, com volume acima da triagem.", "Limite da regra fixa."],
    ["Vielberth et al. (2020)", "Revisão de SOC: volume excede a capacidade; falta contexto comportamental.", "Motivação do contexto individual."],
    ["Axelsson (2000)", "Falácia da taxa-base em detecção de intrusão.", "Revocação fixa; FPR como grandeza."],
    ["Sundaramurthy et al. (2015); Alahmadi et al. (2022)", "Exaustão do analista; alertas majoritariamente benignos.", "Custo humano do falso positivo."],
    ["Cappelli et al. (2012); Homoliak et al. (2019)", "Ameaça interna: sabotagem, roubo de PI, fraude; taxonomias.", "Padrões que se desenvolvem no tempo."],
]
tabela(s, MX, 1.55, [3.3, 5.3, 3.3], rows, [0.4, 0.62, 0.62, 0.62, 0.62, 0.55, 0.62, 0.62], size=12.5, hsize=11.5,
       negrito_1a=True)
legenda(s, "Tabela 1 — Fontes do domínio e seu uso. Fonte: elaborada pelos autores (2026), a partir da seção 2.1 do artigo.", MX, 6.75, 11.9)
rodape(s)
notas(s)

# ============================================== 6 referencial: taxonomia
s = novo()
titulo(s, "Referencial: tipos de anomalia e as três dimensões")
rows = [
    ["Tipo de anomalia (Chandola et al., 2009)", "Como aparece no problema", "Autores que o tratam", "Dimensão"],
    ["Pontual", "Um evento destoa sozinho.", "Kent e Souppaya (2006), gestão de logs; Gonzalez-Granadillo et al. (2021), regras de SIEM", "D1 (e C0)"],
    ["Contextual", "Só é anômalo no histórico de quem o produziu.", "Denning (1987), perfil por sujeito; Shashanka et al. (2016), análise de usuário e entidade (UEBA)", "D2"],
    ["Coletiva", "Sequência de eventos ordinários, anômala em conjunto.", "Cappelli et al. (2012) e Homoliak et al. (2019), ameaça interna", "D3"],
]
tabela(s, MX, 1.95, [3.2, 3.2, 4.2, 1.3], rows, [0.75, 0.95, 0.95, 0.95], size=15, hsize=12, negrito_1a=True)
legenda(s, "Tabela 2 — Tipos de anomalia e as dimensões que os cobrem. Fonte: elaborada pelos autores (2026), a partir da seção 2 do artigo.",
        MX, 5.65, 11.9)
txt(s, [{"runs": [("Lacuna (seção 2.2). ", {"bold": True}),
                  ("Nenhuma avaliação trata as três leituras de forma separável. O trabalho mede quanto cada uma "
                   "acrescenta sobre uma linha de base de regras fixas, e não propõe mecanismo inédito.", {})]}],
    MX, 6.05, 11.9, 0.8, size=16)
rodape(s)
notas(s)

# ================================================= 7 referencial: método
s = novo()
titulo(s, "Referencial: o método de avaliação")
rows = [
    ["Autor (ano)", "Contribuição", "Onde entra no desenho"],
    ["Wohlin et al. (2012)", "Experimentação em engenharia de software; quatro categorias de ameaça à validade.", "Desenho do experimento e seção 3.8."],
    ["Wilcoxon (1945)", "Teste de postos sinalizados, para amostras pareadas.", "Comparar configurações, semente a semente."],
    ["Demšar (2006)", "Recomenda o teste de Wilcoxon para comparar configurações sobre vários conjuntos de dados.", "Justifica o teste estatístico."],
    ["Kaufman et al. (2012)", "Vazamento de informação (leakage) entre treino e avaliação.", "Padrão em janela disjunta; exposição exclui o evento atual."],
    ["Sommer e Paxson (2010)", "Avaliar detector de anomalias só em atividade simulada tende a carecer de realismo.", "Ameaça externa, declarada."],
]
tabela(s, MX, 1.85, [3.0, 5.4, 3.5], rows, [0.45, 0.8, 0.7, 0.8, 0.8, 0.8], size=14, hsize=12, negrito_1a=True)
legenda(s, "Tabela 3 — Fontes metodológicas e seu uso. Fonte: elaborada pelos autores (2026), a partir das seções 3.7 e 3.8 do artigo.",
        MX, 6.3, 11.9)
rodape(s)
notas(s)

# ================================================================ 8 hipótese
s = novo()
titulo(s, "Pergunta, variáveis e hipótese")
txt(s, "A avaliação combinada do risco do evento, do desvio do próprio usuário e da exposição acumulada reduz os "
       "falsos positivos, a uma mesma revocação, e aumenta a revocação em cenários longitudinais, em comparação "
       "com regras fixas?", MX, 1.8, 11.9, 1.4, size=20, italic=True, font=HEAD)
rows = [
    ["Elemento", "Definição"],
    ["Tipo de pesquisa", "Aplicada, quantitativa, experimental, na modalidade de desenvolvimento de protótipo."],
    ["Variável independente", "Configuração de avaliação: C0, C1, C2 ou C3."],
    ["Variáveis dependentes", "(1) FPR com a revocação r fixada, r de 0,10 a 0,90.  (2) Revocação por episódio, família L."],
    ["Hipótese", "FPR(C3) < FPR(C0) na mesma revocação, e Rec_L(C3) > Rec_L(C0). Se C3 não ganhar da C2, a resposta é não."],
    ["Hipótese nula", "Duas configurações têm a mesma FPR na mesma semente (Wilcoxon pareado, bilateral)."],
]
tabela(s, MX, 3.45, [2.9, 9.0], rows, [0.5, 0.55, 0.5, 0.55, 0.7, 0.55], size=14, hsize=12, negrito_1a=True)
rodape(s)
notas(s)

# ============================================================ 9 arquitetura
s = novo()
titulo(s, "Arquitetura em camadas, com portas e adaptadores")
camadas = [
    ("Apresentação", [("frontend/", "Streamlit, 4 telas"), ("backend/", "FastAPI, só leitura")]),
    ("Aplicação", [("runner/", "lote, CLI: gera a tabela"), ("evaluator/", "métricas, lê o gabarito")]),
    ("Domínio", [("detection/", "c0 · d1 · d2 · d3 · integração"), ("ports.py", "contrato de E/S")]),
    ("Adaptadores", [("storage/", "arquivos, sem servidor"), ("PostgreSQL", "corp · ground_truth · sdcac")]),
]
ycam = [1.85, 3.05, 4.25, 5.45]
for (nome, mods), y in zip(camadas, ycam):
    forma(s, MSO_SHAPE.RECTANGLE, MX, y, 8.4, 0.95, PAPER)
    txt(s, nome, MX + 0.12, y, 1.5, 0.95, size=13, bold=True, color=GRAY, anchor="m")
    for j, (a, b) in enumerate(mods):
        bx = MX + 1.7 + j * 3.3
        forma(s, MSO_SHAPE.RECTANGLE, bx, y + 0.13, 3.15, 0.69, WHITE, linha=BLUE2, lw=1)
        txt(s, [{"t": a, "font": MONO, "size": 13, "bold": True, "color": BLUE, "align": "c"},
                {"t": b, "size": 12, "color": INK, "align": "c"}], bx, y + 0.18, 3.15, 0.6)
for y in ycam[:-1]:
    seta(s, MX + 4.2, y + 0.95, MX + 4.2, y + 1.2, GRAY)
legenda(s, "Figura 2 — Arquitetura em camadas. As dependências apontam para o domínio. Fonte: elaborada pelos autores (2026).",
        MX, 6.55, 8.4)
txt(s, "Em números", 9.5, 1.85, 3.1, 0.4, size=16, bold=True, font=HEAD, color=BLUE)
for i, (a, b) in enumerate([("≈10,1 mil", "linhas de código (Python)"), ("≈10,2 mil", "linhas de testes"),
                            ("765", "testes automáticos"), ("1 código", "4 configurações, por flag")]):
    y = 2.4 + i * 1.0
    txt(s, a, 9.5, y, 3.1, 0.5, size=24, bold=True, font=HEAD)
    txt(s, b, 9.5, y + 0.48, 3.1, 0.4, size=14, color=GRAY)
rodape(s)
notas(s)

# ======================================================== 10 dados e ambiente
s = novo()
titulo(s, "Dados e ambiente simulado")
fatos = [("250", "funcionários, ao longo de um ano"), ("20 a 50", "eventos por dia útil, por funcionário"),
         ("8", "tipos de evento, com listas fechadas"), ("diário", "estado de postura, lido na data do evento")]
for i, (a, b) in enumerate(fatos):
    y = 1.85 + i * 1.15
    txt(s, a, MX, y, 2.4, 0.6, size=28, bold=True, color=BLUE, font=HEAD)
    txt(s, b, MX + 2.5, y + 0.1, 2.3, 0.9, size=14, color=GRAY)
txt(s, "Nenhum dado de pessoa real, em nenhuma etapa.", MX, 6.45, 5.0, 0.4, size=14, italic=True)
rows = [
    ["Papel", "corp\n(eventos, sem rótulo)", "ground_truth\n(episódios e rótulos)", "sdcac\n(padrões, notas, alertas, métricas)"],
    ["generator", "lê e insere", "lê e insere", "sem acesso"],
    ["sdcac_app", "lê", [{"t": "SEM ACESSO", "bold": True, "color": RED}], "lê e insere"],
    ["evaluator", "lê", "lê", "lê; insere só métricas"],
]
tabela(s, 5.9, 1.85, [1.3, 1.7, 1.8, 1.95], rows, [0.95, 0.65, 0.65, 0.65], size=13, hsize=11, negrito_1a=True)
legenda(s, "Tabela 4 — Permissões por papel de banco. Ninguém recebe UPDATE nem DELETE. Fonte: database/*/002_privilegios.sql.",
        5.9, 4.95, 6.75)
txt(s, [{"t": "A separação é trava, não organização: a aplicação não tem como cruzar evento com gabarito, nem por engano.", "bullet": True, "after": 4},
        {"t": "Só a rotina de métricas lê o gabarito, e só ela insere métrica.", "bullet": True}], 5.9, 5.65, 6.75, 1.2, size=14)
rodape(s)
notas(s)

# ============================================================ 11 cenários
s = novo()
titulo(s, "Cenários e gabarito: quatro famílias, duas unidades")
rows = [
    ["Família", "O que exercita", "Unidade", "Episódios por semente"],
    ["P  pontuais", "D1, sobre o evento isolado", "evento", "24"],
    ["B  de contexto", "D2, o padrão da pessoa", "episódio", "16"],
    ["L  longitudinais", "D3, escalada gradual sem evento notável", "episódio", "12"],
    ["N  controle negativo", "Todas, com comportamento legítimo; mede o falso positivo", "episódio", "72 (53 de manutenção noturna)"],
]
tabela(s, MX, 1.85, [2.6, 5.0, 1.6, 2.7], rows, [0.5, 0.6, 0.6, 0.7, 0.8], size=14, hsize=12, negrito_1a=True)
legenda(s, "Tabela 5 — 20 cenários (6 P, 4 B, 4 L, 6 N) e 124 episódios por semente. Fonte: artigo, seção 3.4.", MX, 5.1, 11.9)
txt(s, [{"runs": [("Episódio", {"bold": True}), (" = par funcionário × cenário. Num cenário longitudinal que só cruza o limiar no oitavo dia, "
                   "a medição por evento rende revocação próxima de 0,15, e por episódio, 1,00. Por isso nenhuma tabela mistura as unidades.", {})], "after": 6},
        {"runs": [("O gabarito ", {"bold": True}), ("é gravado pelo gerador em ground_truth, e a especificação dos cenários foi feita "
                   "sem acesso às fórmulas de pontuação.", {})]}], MX, 5.5, 11.9, 1.4, size=15)
rodape(s)
notas(s)

# =============================================================== 12 C0
s = novo()
titulo(s, "C0: a linha de base, sem parâmetro aprendido")
rows = [
    ["Regra", "Pontos", "Condição"],
    ["off_hours", "30", "Fora do expediente (6h às 22h), no fuso do site"],
    ["external_origin", "30", "Origem de rede fora das faixas corporativas"],
    ["restricted_access", "35", "Acesso a recurso classificado como restrito"],
    ["brute_force", "40", "10 falhas de autenticação em janela fixa de 2 minutos"],
]
tabela(s, MX, 1.85, [2.6, 1.0, 4.0], rows, [0.45, 0.62, 0.62, 0.62, 0.62], size=14, hsize=12, negrito_1a=True)
legenda(s, "Tabela 6 — Regras da C0. Fonte: detection/presets.toml.", MX, 5.0, 7.6)
txt(s, "Por que é o controle", 8.9, 1.85, 3.8, 0.4, size=16, bold=True, font=HEAD, color=BLUE)
txt(s, [{"t": "Limites iguais para os 250 funcionários.", "bullet": True, "after": 6},
        {"t": "A origem habitual vem de faixas de rede cadastradas, e não do histórico de cada pessoa: a informação que se mede não está no controle.", "bullet": True, "after": 6},
        {"t": "A regra de 2 minutos é correlação de curto prazo, e não perfil individual. Por isso o reconhecimento de tentativas sucessivas não conta como ganho das dimensões.", "bullet": True}],
    8.9, 2.4, 3.8, 4.2, size=13)
rodape(s)
notas(s)

# =============================================================== 13 D1
s = novo()
titulo(s, "D1: o risco do evento, por regras com pontos")
rows = [
    ["Regra", "Pontos", "Condição"],
    ["privilege_change", "40", "Alteração de privilégio"],
    ["personal_device", "25", "Dispositivo pessoal"],
    ["download_to_external", "25", "Download com destino externo"],
    ["off_hours_employee", "20", "Fora do expediente, no fuso do funcionário"],
    ["large_download", "20", "Download de 50 MiB ou mais"],
    ["removable_device", "20", "Uso de dispositivo removível"],
    ["login_without_mfa", "15", "Login sem segundo fator"],
    ["risky_browsing", "10", "Navegação em categoria de risco"],
]
tabela(s, MX, 1.85, [2.9, 0.9, 3.6], rows, [0.42] + [0.5] * 8, size=13, hsize=12, negrito_1a=True)
rows2 = [["Origem de rede", "Pontos"], ["escritório, VPN", "0"], ["casa", "10"], ["externa", "30"]]
tabela(s, 8.6, 1.85, [2.6, 1.4], rows2, [0.42, 0.45, 0.45, 0.45], size=13, hsize=12)
rows3 = [["Sensibilidade do recurso", "Pontos"], ["público", "0"], ["interno", "5"], ["confidencial", "20"], ["restrito", "35"]]
tabela(s, 8.6, 3.95, [2.6, 1.4], rows3, [0.42, 0.45, 0.45, 0.45, 0.45], size=13, hsize=12)
legenda(s, "Tabela 7 — Pontos da D1. Fonte: detection/presets.toml. Parâmetros declarados, preliminares, sem análise de sensibilidade.",
        MX, 6.55, 11.9)
rodape(s)
notas(s)

# =============================================================== 14 D2
s = novo()
titulo(s, "D2: o desvio em relação ao padrão da própria pessoa")
bloco_formula(s, MX, 1.85, 6.6, 1.55, ["z = min( max(0, (x − med) / max(1,4826·MAD, piso)), 6 )",
                                       "piso = max(1 ; 0,1·med)", "pontos = round(peso · z / 6)"],
              rotulo="Desvio robusto (contagens: volume, falhas)")
txt(s, [{"t": "Padrão dos 3 primeiros meses, em janela disjunta da avaliação.", "bullet": True, "after": 4},
        {"t": "Um lado só: fazer menos que o habitual não é risco.", "bullet": True, "after": 4},
        {"t": "A nota da D2 é o maior de dois desvios: sessão e usuário-dia.", "bullet": True, "after": 4},
        {"t": "Menos de 20 dias de atividade no treino: sem padrão próprio, cai no grupo de pares.", "bullet": True}],
    MX, 3.6, 6.6, 2.9, size=14)
rows = [["Característica", "Como compara", "Pontos"],
        ["Volume diário", "desvio robusto", "25"], ["Falhas de autenticação", "desvio robusto", "30"],
        ["Mistura de sigilo", "distância de distribuição", "25"], ["Recurso novo", "novidade", "30"],
        ["Origem nova", "novidade", "20"], ["Dispositivo novo", "novidade", "20"], ["Horário incomum", "faixa horária", "20"]]
tabela(s, 7.6, 1.85, [2.2, 2.0, 0.85], rows, [0.42] + [0.52] * 7, size=12.5, hsize=11.5, negrito_1a=True)
legenda(s, "Tabela 8 — Características da D2. Fonte: detection/presets.toml.", 7.6, 6.0, 5.05)
txt(s, "A novidade pesa mais quando o recurso é de sigilo alto (de ×0,5, público, a ×2,0, restrito).", 7.6, 6.4, 5.05, 0.5, size=12, color=GRAY)
rodape(s)
notas(s)

# =============================================================== 15 D3
s = novo()
titulo(s, "D3: a exposição acumulada, em duas parcelas separadas")
bloco_formula(s, MX, 1.85, 6.4, 1.3, ["D3c(e) = min(100, round(100 · Σ pᵢ · 0,85^Δᵢ / 300))",
                                      "Δᵢ ≤ 14 dias · o evento atual fica de fora"], rotulo="Conduta: o que a pessoa fez")
txt(s, [{"t": "Decaimento de 0,85 ao dia, janela deslizante de 14 dias.", "bullet": True, "after": 4},
        {"t": "Excluir o evento atual evita contar o mesmo risco duas vezes (D-18).", "bullet": True, "after": 4},
        {"t": "A postura é lida como estava no dia do evento: o código recusa o retrato de outro dia.", "bullet": True, "after": 4},
        {"t": "As parcelas ficam em campos separados: o analista vê qual causou o alerta. Na nota, a postura pesa 0,5.", "bullet": True}],
    MX, 3.4, 6.4, 3.1, size=14)
rows = [["Postura de segurança", "Pontos"], ["phishing: credenciais enviadas", "35"], ["segundo fator desligado", "30"],
        ["phishing: clicou", "25"], ["atualização atrasada (> 30 dias)", "20"], ["antivírus desligado", "20"],
        ["privilégio de administrador", "15"], ["uso de dispositivo removível", "10"], ["navegação de risco", "5"]]
tabela(s, 7.5, 1.85, [3.9, 1.2], rows, [0.42] + [0.5] * 8, size=13, hsize=12)
legenda(s, "Tabela 9 — Postura (D3p), de 0 a 100, com peso 0,5. Fonte: detection/presets.toml.", 7.5, 6.35, 5.1)
rodape(s)
notas(s)

# ============================================================== 16 integração
s = novo()
titulo(s, "Integração: uma nota decomponível, e as faixas de exibição")
bloco_formula(s, MX, 1.85, 6.6, 0.95, ["S(e) = 1,0·D1 + 1,0·D2 + 1,0·D3c + 0,5·D3p"], rotulo="Nota final: um só conjunto de pesos")
bloco_formula(s, MX, 2.95, 6.6, 1.6, ["event_id", "c0 · d1 · d2 · d3_conduct · d3_posture", "final_raw · band · hits", "config_hash"],
              rotulo="RiskScore: o que é guardado")
txt(s, [{"t": "Nulo significa “dimensão não avaliada nesta configuração”, e é diferente de zero.", "bullet": True, "after": 4},
        {"t": "Entrada que falta é erro, e não zero.", "bullet": True}], MX, 4.8, 6.6, 1.5, size=14)
txt(s, "Faixas de exibição", 8.0, 1.85, 4.7, 0.4, size=16, bold=True, font=HEAD, color=BLUE)
for i, f in enumerate(FAIXAS):
    chip(s, 8.0, 2.4 + i * 0.75, 4.65, 0.58, f, True)
txt(s, "A avaliação usa a nota bruta; a faixa existe só para a tela.", 8.0, 5.55, 4.65, 0.7, size=13, color=GRAY)
legenda(s, "Fonte: detection/presets.toml e detection/integracao/composition.py.", MX, 6.6, 8)
rodape(s)
notas(s)

# ============================================================ 17 protocolo
s = novo()
titulo(s, "Protocolo experimental: cinco etapas, cada uma um programa")
etapas = [("1  Geração", "semente"), ("2  Tradução", "ingest"), ("3  Pontuação", "C0 a C3"),
          ("4  Avaliação", "único que lê o gabarito"), ("5  Agregação", "média ± dp, Wilcoxon")]
for i, (a, b) in enumerate(etapas):
    x = MX + i * 2.4
    forma(s, MSO_SHAPE.PENTAGON, x, 1.9, 2.3, 1.0, BLUE if i != 3 else BLUE2)
    txt(s, [{"t": a, "size": 15, "bold": True, "color": WHITE}, {"t": b, "size": 12, "color": WHITE}],
        x + 0.12, 2.0, 1.85, 0.85, anchor="m")
legenda(s, "Figura 3 — Pipeline de execução. Fonte: elaborada pelos autores (2026), a partir da seção 3.7 do artigo.", MX, 3.0, 11.9)
txt(s, [{"t": "Mesmas 10 sementes nas 4 configurações: comparação pareada.", "bullet": True, "after": 6},
        {"t": "A agregação recusa reunir execuções incomparáveis: limiar distinto, níveis de revocação distintos, conjunto de configurações distinto ou a mesma execução contada duas vezes.", "bullet": True, "after": 6},
        {"t": "As métricas do artigo são lidas do arquivo que a agregação grava, e não transcritas à mão.", "bullet": True}],
    MX, 3.6, 6.2, 3.0, size=15)
bloco_formula(s, 7.3, 3.6, 5.35, 1.7, ["semente", "SHA-256 da configuração", "versão do código"], rotulo="Cada execução grava")
txt(s, [{"runs": [cit("[Wohlin et al., 2012] "), ("Desenho experimental e reprodutibilidade.", {"color": GRAY, "size": 13})]}],
    7.3, 5.5, 5.35, 0.6)
rodape(s)
notas(s)

# ======================================================= 18 métricas e estatística
s = novo()
titulo(s, "Métricas e estatística")
bloco_formula(s, MX, 1.85, 6.0, 1.25, ["FPR = FP / (FP + VN)    na revocação r fixada", "Rec_L = VP_L / (VP_L + FN_L)    por episódio"],
              rotulo="Métricas primárias", size=13)
bloco_formula(s, MX, 3.3, 6.0, 0.9, ["p_min = 2 / 2ⁿ    (bilateral, exato)"], rotulo="Menor p possível com n pares", size=13)
txt(s, [{"runs": [cit("[Wilcoxon, 1945; Demšar, 2006] "), ("Teste pareado, não paramétrico.", {})], "bullet": True, "after": 4},
        {"t": "Critério de sucesso: até 45 alertas falsos por turno, e revocação longitudinal ≥ 0,80.", "bullet": True, "after": 4},
        {"t": "Os dois valores foram fixados em 12/11/2026, depois da primeira execução.", "bullet": True}],
    MX, 4.45, 6.0, 2.2, size=14)
cd = CategoryChartData()
cd.categories = ["n = 5", "n = 6", "n = 7", "n = 8", "n = 9", "n = 10"]
cd.add_series("p mínimo", [0.0625, 0.0313, 0.0156, 0.0078, 0.0039, 0.0020])
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7.0), Inches(1.85), Inches(5.65), Inches(4.2), cd).chart
estilo_chart(ch)
ch.has_title = False
ser = ch.plots[0].series[0]
for i in range(6):
    pt = ser.points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = rgb(GRAY if i == 0 else BLUE)
pl = ch.plots[0]
pl.gap_width = 40
pl.has_data_labels = True
dl = pl.data_labels
dl.number_format = "0.0000"
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(12)
dl.font.bold = True
ch.category_axis.tick_labels.font.size = Pt(13)
ch.value_axis.tick_label_position = XL_TICK_LABEL_POSITION.NONE
ch.value_axis.major_tick_mark = XL_TICK_MARK.NONE
ch.value_axis.format.line.fill.background()
ch.value_axis.visible = False
ch.value_axis.has_major_gridlines = False
ch.value_axis.minimum_scale = 0
ch.value_axis.maximum_scale = 0.075
legenda(s, "Figura 4 — Menor p-valor bilateral exato do Wilcoxon pareado, em função do número de sementes. Com n = 5 o piso é 0,0625, acima de 0,05.",
        7.0, 6.1, 5.65)
rodape(s)
notas(s)

# ======================================================== 19 resultado: ruído
s = novo()
titulo(s, "Resultado 1: falsos positivos caem de 18,44% para 0,40%")
barras_h(s, MX, 1.85, 7.9, 4.5, ["C0  regras fixas", "C1  + evento", "C2  + padrão da pessoa", "C3  + exposição acumulada"],
         [18.44, 6.03, 0.40, 0.54], [GRAY, GRAY, BLUE, BLUE], '0.00"%"', 23)
legenda(s, "Figura 5 — FPR com a revocação fixada em 0,20. Média das dez sementes. Fonte: results/agregado.md.", MX, 6.45, 7.9)
for i, (a, b) in enumerate([("34,55% para 1,33%", "em 0,30 de revocação, C0 contra C2"),
                            ("100% de FPR", "é o que a C0 precisa para chegar a 0,40 de revocação"),
                            ("p = 0,0020", "C2 contra C0, nos nove níveis de revocação (piso do teste)")]):
    y = 1.95 + i * 1.55
    txt(s, a, 9.0, y, 3.7, 0.5, size=22, bold=True, color=BLUE, font=HEAD)
    txt(s, b, 9.0, y + 0.55, 3.7, 0.8, size=14, color=GRAY)
rodape(s)
notas(s)

# ===================================================== 20 resultado: cobertura
s = novo()
titulo(s, "Resultado 2: na escalada, cobertura de 35,0% a 100,0%")
cd = CategoryChartData()
cd.categories = ["P  pontuais", "B  de contexto", "L  longitudinais"]
cd.add_series("C0", [83.3, 28.7, 35.0])
cd.add_series("C1", [100.0, 45.6, 89.2])
cd.add_series("C2", [100.0, 98.8, 100.0])
cd.add_series("C3", [100.0, 100.0, 100.0])
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(MX), Inches(1.85), Inches(8.5), Inches(4.6), cd).chart
estilo_chart(ch, XL_LEGEND_POSITION.TOP)
for ser, cor in zip(ch.plots[0].series, [GRAY, "9AA3B5", BLUE, BLUE3]):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = rgb(cor)
pl = ch.plots[0]
pl.gap_width = 55
pl.has_data_labels = True
dl = pl.data_labels
dl.number_format = "0.0"
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(11)
dl.font.color.rgb = rgb(INK)
ch.category_axis.tick_labels.font.size = Pt(14)
ch.value_axis.visible = False
ch.value_axis.has_major_gridlines = False
ch.value_axis.minimum_scale = 0
ch.value_axis.maximum_scale = 115
legenda(s, "Figura 6 — Revocação por episódio, em %, no limiar de operação. Média das dez sementes. Fonte: results/agregado.md.",
        MX, 6.5, 8.5)
txt(s, "Família N", 9.6, 1.95, 3.1, 0.4, size=18, bold=True, font=HEAD)
txt(s, "Legítimos: o número é alarme sobre atividade legítima. Menos é melhor.", 9.6, 2.4, 3.1, 1.0, size=14, color=GRAY)
for i, (a, b) in enumerate([("C0", "75,8%"), ("C2", "96,0%"), ("C3", "100,0%")]):
    y = 3.6 + i * 0.7
    txt(s, a, 9.6, y, 0.8, 0.55, size=15, color=GRAY, anchor="m")
    txt(s, b, 10.4, y, 2.3, 0.55, size=28, bold=True, color=RED, font=HEAD, anchor="m")
txt(s, "Esse é o custo.", 9.6, 5.8, 3.1, 0.4, size=16, italic=True)
rodape(s)
notas(s)

# ============================================================ 21 contrapeso
s = novo(True)
titulo(s, "Contrapeso: ganha em duas grandezas e perde em outra", True)
col = [("96,0%", "dos episódios legítimos geram alerta na C2, contra 75,8% na C0. O ganho de cobertura tem custo."),
       ("Sem ganho", "A exposição acumulada (C3) não reduziu os falsos positivos de forma significativa em nenhum regime."),
       ("99,84%", "do registro gera alerta na C3 no limiar herdado, o corte 20. O limiar não foi calibrado.")]
for i, (a, b) in enumerate(col):
    x = MX + i * 4.15
    txt(s, a, x, 2.0, 3.6, 0.95, size=44, bold=True, color=BLUE_BG, font=HEAD)
    txt(s, b, x, 3.15, 3.5, 2.3, size=17, color=PAPER)
    if i:
        linha(s, x - 0.32, 2.05, x - 0.32, 5.3, GRAY)
txt(s, "A 0,20 de revocação, a C2 cumpre o critério de 45 alertas falsos por turno em 7 das 10 sementes.",
    MX, 5.9, 11.9, 0.8, size=18, italic=True, color=MIST)
rodape(s, True)
notas(s)

# ================================================================== 22 painel
s = novo()
titulo(s, "O painel: a nota decomposta, sem depender só de cor")
for i, f in enumerate(FAIXAS):
    chip(s, MX, 1.85 + i * 0.85, 4.6, 0.68, f)
legenda(s, "Figura 7 — Faixas de risco: cor, rótulo e forma.", MX, 5.3, 4.6)
txt(s, "Nota de uma pessoa, decomposta", 5.8, 1.85, 6.8, 0.4, size=16, bold=True)
sx = 5.8
for nome, larg, cor, ct in [("D1", 2.05, BLUE, WHITE), ("D2", 1.7, BLUE2, WHITE), ("D3 conduta", 2.05, BLUE3, INK),
                            ("D3 postura", 1.0, BLUE_BG, INK)]:
    forma(s, MSO_SHAPE.RECTANGLE, sx, 2.35, larg, 0.75, cor, linha=WHITE, lw=1.5)
    txt(s, nome, sx, 2.35, larg, 0.75, size=13, bold=True, color=ct, align="c", anchor="m")
    sx += larg
legenda(s, "Exemplo ilustrativo, não é dado do experimento.", 5.8, 3.17, 6.8)
bul = ["Quatro telas: execução, pessoas, alertas e decomposição do risco.",
       "Cor, rótulo e forma em cada faixa: a cor nunca é o único sinal (WCAG 2.2, critério 1.4.1).",
       "Contraste de pelo menos 4,5 para 1, calculado e testado (critério 1.4.3).",
       "Parcela que a configuração não liga aparece como “não ligada”, e não como zero.",
       "Avaliação heurística: 20 achados, nenhum de severidade 4. Um avaliador, sem usuários."]
txt(s, [{"t": b, "size": 15, "bullet": True, "after": 6} for b in bul], 5.8, 3.7, 6.8, 3.0)
rodape(s)
notas(s)

# ======================================================= 23 qualidade e segurança
s = novo()
titulo(s, "Qualidade e segurança: o que é verificado, e como")
rows = [
    ["Aspecto", "Como é verificado"],
    ["Invariantes do desenho", "765 testes automáticos a cada alteração: gabarito inacessível à aplicação, log só de inserção, parcela não ligada ≠ zero."],
    ["Reprodutibilidade", "Por execução: semente, SHA-256 da configuração e versão do código."],
    ["Acessibilidade", "WCAG 2.2: critérios 1.4.1 (rótulo e forma) e 1.4.3 (contraste 4,5:1), calculados no teste."],
    ["Segurança", "Revisão por leitura: 7 achados, 3 corrigidos com teste (CWE-79, CWE-942 e CREATE herdado no schema public)."],
    ["Rastreabilidade", "Decisões numeradas (D-xx) e um relatório por sessão de trabalho."],
]
tabela(s, MX, 1.85, [2.8, 9.1], rows, [0.45, 0.8, 0.6, 0.8, 0.8, 0.6], size=14, hsize=12, negrito_1a=True)
legenda(s, "Tabela 10 — Verificações. A revisão de segurança é por leitura de código, e não teste de intrusão.", MX, 6.05, 11.9)
rodape(s)
notas(s)

# ============================================================== 24 validade
s = novo()
titulo(s, "Ameaças à validade, segundo Wohlin et al. (2012)")
rows = [
    ["Categoria", "Ameaça", "Mitigação"],
    ["Construto", "O risco é um construto; o gabarito é dos próprios autores.", "Unidade de análise explícita; parcelas da D3 separadas."],
    ["Interna", "Padrão calculado sobre dias com cenário faria o anômalo virar normal [Kaufman et al., 2012].", "Janela disjunta; exposição exclui o evento atual."],
    ["Interna: circularidade", "A D3 foi feita para a escalada gradual, e os cenários L também.", "Controle negativo longitudinal; quem especifica os cenários não escreve as fórmulas."],
    ["Externa", "Simulado tende a carecer de realismo [Sommer e Paxson, 2010].", "Ruído legítimo no tráfego de fundo; limites declarados."],
    ["Conclusão estatística", "Uma execução não separa ganho de variação.", "Dez sementes, Wilcoxon pareado exato."],
]
tabela(s, MX, 1.85, [2.3, 5.0, 4.6], rows, [0.45, 0.7, 0.85, 0.85, 0.7, 0.6], size=13, hsize=12, negrito_1a=True)
txt(s, [{"runs": [("Limites declarados: ", {"bold": True}),
                  ("limiar de operação não calibrado · pesos sem análise de sensibilidade · dado pessoal real exige "
                   "a LGPD (Lei 13.709/2018) e a ISO/IEC 27001.", {})]}], MX, 6.15, 11.9, 0.7, size=14)
rodape(s)
notas(s)

# ================================================================ 25 conclusão: respostas
s = novo()
titulo(s, "Conclusão: o que os resultados mostram e não mostram")
linhas = [
    ("A pergunta", "Nos cenários medidos, a avaliação combinada reduz falsos positivos a uma mesma revocação e aumenta a revocação "
                   "longitudinal. FPR de 18,44% para 0,40% a 0,20 de revocação, e cobertura L de 35,0% para 100,0% (p = 0,0020)."),
    ("De onde vem", "O ganho vem da D2: comparar o evento com o padrão da própria pessoa leva a FPR de 6,03% (C1, só o evento) "
                    "para 0,40% (C2)."),
    ("O que não se confirmou", "A D3 não acrescentou sobre a C2: FPR de 0,54% contra 0,40%, com a cobertura L já em 100,0%. "
                               "A leitura que os dados sustentam (seção 4.5) é que ela pertence a um segundo estágio de triagem."),
    ("O custo", "Sobe o alarme sobre atividade legítima: de 75,8% dos episódios na C0 para 96,0% na C2. A C2 cumpre o critério "
                "de 45 alertas falsos por turno em 7 de 10 sementes."),
]
y = 1.85
for rot, texto in linhas:
    txt(s, rot, MX, y, 2.7, 0.5, size=16, bold=True, color=BLUE, font=HEAD)
    txt(s, texto, 3.6, y, 9.0, 1.1, size=15)
    y += 1.2
rodape(s)
notas(s)

# ============================================== 26 conclusão: contribuições e próximos passos
s = novo()
titulo(s, "Contribuições, limites e próximos passos")
txt(s, "Contribuições", MX, 1.85, 5.8, 0.4, size=19, bold=True, color=BLUE, font=HEAD)
c = ["Protótipo com avaliação independente do meio de armazenamento.",
     "Quatro configurações canônicas, semeadas e só de leitura.",
     "Regras e pesos com SHA-256 preso a cada execução.",
     "Cenários de teste automatizados, com gabarito separado do motor.",
     "Contrato de leitura da API e painel que mostra a nota decomposta."]
txt(s, [{"t": t, "size": 15, "bullet": True, "after": 8} for t in c], MX, 2.35, 5.8, 4.0)
txt(s, "O que o resultado não autoriza", 6.9, 1.85, 5.7, 0.4, size=19, bold=True, color=BLUE, font=HEAD)
l = ["Dizer que o sistema está pronto: o ambiente é simulado e o limiar não foi calibrado.",
     "Dizer que o painel é usável: houve um avaliador, e nenhum usuário."]
txt(s, [{"t": t, "size": 14, "bullet": True, "after": 6} for t in l], 6.9, 2.35, 5.7, 1.9)
txt(s, "Próximos passos", 6.9, 4.3, 5.7, 0.4, size=19, bold=True, color=BLUE, font=HEAD)
p = ["Calibrar o limiar e analisar a sensibilidade dos pesos.",
     "Implantar sobre dado real, com LGPD e ISO/IEC 27001.",
     "Validar contra tráfego de produção."]
txt(s, [{"t": t, "size": 14, "bullet": True, "after": 6} for t in p], 6.9, 4.8, 5.7, 1.8)
rodape(s)
notas(s)

# ============================================================== 27 referências
s = novo()
titulo(s, "Referências")
t = (AQUI.parent.parent / "artigo" / "referencias.md").read_text(encoding="utf-8")
bloco = t[t.index("## Lista"):t.index("### Critérios")]
ents = []
for par in re.split(r"\n\s*\n", bloco):
    par = " ".join(par.strip().split())
    if par and not par.startswith((">", "#")) and re.match(r"^[A-ZÀ-Ú]{3,}", par):
        ents.append(par.replace("**", ""))
acum, meio = 0, 0
total_c = sum(len(e) + 60 for e in ents)
for i_e, e in enumerate(ents):
    acum += len(e) + 60
    if acum >= total_c / 2:
        meio = i_e + 1
        break
for k, grupo in enumerate((ents[:meio], ents[meio:])):
    txt(s, [{"t": e, "size": 10, "after": 3} for e in grupo], MX + k * 6.1, 1.5, 5.85, 5.0, color=INK)
txt(s, [{"runs": [("Repositório público: ", {"bold": True}), ("github.com/Codexrocks/TCC_SDCAC", {"color": BLUE, "bold": True}),
                  ("  ·  código, dados de execução e relatórios de sessão.", {})]}], MX, 6.6, 11.9, 0.35, size=12)
rodape(s)
notas(s)

assert _n[0] == TOTAL, (_n[0], TOTAL)
prs.core_properties.title = "SDCAC — Apresentação do TCC"
prs.core_properties.author = "Davi Soares Dilly, Filipe Fernandes de Aguiar, Yasmin Teles Vales"
prs.save(SAIDA)
print("gravado:", SAIDA, "| slides:", _n[0])
