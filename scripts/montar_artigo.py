#!/usr/bin/env python3
"""Monta o artigo no formato COBEM a partir do Markdown de `artigo/`.

Uso:
    python scripts/montar_artigo.py                 # grava artigo/artigo-cobem.docx
    python scripts/montar_artigo.py --saida /tmp/x.docx
    python scripts/montar_artigo.py --resultados outra/04.md   # para medir de outra branch

**Por que este programa existe no repositorio.** Ate 12/11/2026 ele vivia na
maquina de quem montava, e o `.docx` de entrega so se produzia ali. Isso torna a
entrega dependente de uma pessoa, e torna **impossivel conferir** se o documento
que foi entregue corresponde ao Markdown versionado. Com o programa aqui,
qualquer um da equipe remonta e compara.

**O Markdown e a fonte da verdade; este arquivo so aplica o template.** Ele nao
reescreve texto, nao corrige e nao decide nada. Descarta duas coisas, e as duas
sao andaime do repositorio: todo **bloco de citacao** (`>`), que e instrucao
para quem escreve, e as **secoes de controle** listadas em `SECOES_DE_CONTROLE`.

As regras de formatacao sao as do `templates/COBEM-2025-template.docx`, lidas do
proprio arquivo: A4, margem superior de 3 cm e as outras de 2 cm, Times New
Roman 10, entrelinha simples, texto justificado, primeira linha recuada 0,5 cm,
titulo centralizado em negrito corpo 14, autores em negrito 10, instituicao em
9, resumo e palavras-chave em italico 10 com a barra vertical a esquerda,
titulos de secao a esquerda em negrito 10 numerados com algarismos arabes
separados por ponto, tabelas centralizadas, e **paginas sem numero**.

⚠️ **O template do COBEM 2026 nao esta no repositorio.** O que esta versionado e
o de 2025, e foi dele que estas regras sairam. Divergencia de 2025 para 2026
muda este programa, nao o texto.

**O `python-docx` e importado com tolerancia a falta.** As funcoes que leem
Markdown -- `blocos` e `trechos`, que e onde os defeitos moram -- rodam sem a
biblioteca, e por isso tem teste em `tests/test_montar_artigo.py`. O CI instala
so `pytest pyyaml fastapi httpx`, e um teste que exigisse `docx` seria pulado em
silencio.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt

    DOCX_DISPONIVEL = True
except ImportError:  # pragma: no cover - so importa quem vai montar o documento
    DOCX_DISPONIVEL = False

RAIZ = Path(__file__).resolve().parent.parent

FONTE = "Times New Roman"
CORPO_PT = 10.0

# A coluna de texto tem 17 cm. A figura entra menor de proposito: a 17 cm
# as duas do artigo passariam de 9 cm de altura cada uma, e o documento tem
# teto de 12 paginas.
LARGURA_FIGURA_CM = 12.0

SECOES_DE_CONTROLE = (
    "O que esta seção ainda precisa",
    "O que esta página ainda precisa",
    "O que mudou em 13/10, e por quê",
    "Resumo e Abstract",
    "Título",
    "Autores",
    "Resumo",
    "Abstract",
    "Modelos por tipo",
    "Lista",
    "Critérios aplicados na conversão",
    "Aproveitáveis de outras páginas",
)


# ------------------------------------------------------------- verificacao
def confere_legendas(caminhos: list[Path]) -> list[str]:
    """Cada tabela precisa de legenda numerada em sequencia e de fonte.

    E a exigencia que o orientador apontou na entrega de 12/11/2026. Fica como
    verificacao, e nao como lembrete, porque lembrete nao reprova nada.
    """
    erros: list[str] = []
    esperado = 0
    esperado_fig = 0
    for caminho in caminhos:
        lidos = blocos(caminho.read_text(encoding="utf-8"))
        nesta_pagina = 0
        for k, (tipo, _nivel, conteudo) in enumerate(lidos):
            if tipo == "titulo" and conteudo in SECOES_DE_CONTROLE:
                break
            if tipo == "imagem":
                # na figura a ordem se inverte: imagem, legenda, fonte. E a
                # forma do template, e e a convencao de todo lugar.
                esperado_fig += 1
                onde = f"{caminho.name}, figura {esperado_fig} ({conteudo})"
                legenda = lidos[k + 1] if k + 1 < len(lidos) else ("", 0, "")
                fonte = lidos[k + 2] if k + 2 < len(lidos) else ("", 0, "")
                if legenda[0] != "legenda":
                    erros.append(f"{onde}: sem legenda abaixo")
                    continue
                m = re.match(r"^\*\*Figura (\d+)\.", str(legenda[2]))
                if m and int(m.group(1)) != esperado_fig:
                    erros.append(
                        f"{onde}: legenda numerada {m.group(1)}, "
                        f"esperada {esperado_fig}"
                    )
                if fonte[0] != "fonte":
                    erros.append(f"{onde}: sem fonte abaixo da legenda")
                continue
            if tipo != "tabela":
                continue
            # a posicao no arquivo, e a primeira linha, para o erro dizer qual
            # tabela e sem obrigar a contar blocos de Markdown a mao
            nesta_pagina += 1
            primeira = str(conteudo[0])[:48] if conteudo else ""
            onde = f"{caminho.name}, {nesta_pagina}a tabela ({primeira})"
            antes = lidos[k - 1] if k else ("", 0, "")
            depois = lidos[k + 1] if k + 1 < len(lidos) else ("", 0, "")
            if antes[0] != "legenda":
                erros.append(f"{onde}: sem legenda acima")
                continue
            esperado += 1
            m = re.match(r"^\*\*(?:Tabela|Figura) (\d+)\.", str(antes[2]))
            if m and int(m.group(1)) != esperado:
                erros.append(
                    f"{onde}: legenda numerada {m.group(1)}, esperada {esperado}"
                )
            if depois[0] != "fonte":
                erros.append(f"{onde}: sem fonte abaixo")
    return erros


# ---------------------------------------------------------------- leitura
def blocos(texto: str) -> list[tuple[str, int, object]]:
    """Quebra o Markdown em blocos, descartando o que e andaime do repositorio."""
    saida = []
    linhas = texto.split("\n")
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        if linha.startswith(">"):  # bloco de instrucao: fora
            while i < len(linhas) and (
                linhas[i].startswith(">") or not linhas[i].strip()
            ):
                i += 1
            continue
        if linha.strip() in ("***", "---"):
            i += 1
            continue
        m = re.match(r"^(#{1,3}) (.+)$", linha)
        if m:
            saida.append(("titulo", len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        m = re.match(r"^!\[[^\]]*\]\(([^)]+)\)$", linha.strip())
        if m:
            saida.append(("imagem", 0, m.group(1)))
            i += 1
            continue
        if re.match(r"^\*\*(Tabela|Figura) \d+\.\*\*", linha.strip()):
            saida.append(("legenda", 0, linha.strip()))
            i += 1
            continue
        if linha.strip().startswith("Fonte:"):
            saida.append(("fonte", 0, linha.strip()))
            i += 1
            continue
        if linha.lstrip().startswith("|"):
            tabela = []
            while i < len(linhas) and linhas[i].lstrip().startswith("|"):
                tabela.append(linhas[i].strip())
                i += 1
            saida.append(("tabela", 0, tabela))
            continue
        if linha.strip().startswith("$$"):
            saida.append(("formula", 0, linha.strip().strip("$")))
            i += 1
            continue
        if re.match(r"^\s*[*+-] ", linha) or re.match(r"^\s*[a-z]\) ", linha):
            item = [linha.strip()]
            i += 1
            while (
                i < len(linhas)
                and linhas[i].strip()
                and not re.match(r"^\s*([*+-] |#|\||>)", linhas[i])
            ):
                item.append(linhas[i].strip())
                i += 1
            saida.append(("item", 0, " ".join(item)))
            continue
        if linha.strip():
            paragrafo = [linha.strip()]
            i += 1
            while (
                i < len(linhas)
                and linhas[i].strip()
                and not re.match(r"^\s*(#|\||>|[*+-] |\$\$)", linhas[i])
            ):
                paragrafo.append(linhas[i].strip())
                i += 1
            saida.append(("paragrafo", 0, " ".join(paragrafo)))
            continue
        i += 1
    return saida


# ---------------------------------------------------------------- escrita
def estilo(doc):
    normal = doc.styles["Normal"]
    normal.font.name = FONTE
    normal.font.size = Pt(CORPO_PT)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONTE)
    p = normal.paragraph_format
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    p.line_spacing = 1.0

    for s in doc.sections:
        s.page_width, s.page_height = Cm(21), Cm(29.7)
        s.top_margin = Cm(3)
        s.left_margin = s.right_margin = s.bottom_margin = Cm(2)


def trechos(texto: str) -> list[tuple[str, bool, bool, bool]]:
    """Quebra em (texto, negrito, italico, mono) por `**`, `*` e crase."""
    saida = []
    for parte in re.split(r"(\*\*[^*]+\*\*|(?<!\*)\*[^*]+\*(?!\*)|`[^`]+`)", texto):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**"):
            saida.append((parte[2:-2], True, False, False))
        elif parte.startswith("`") and parte.endswith("`"):
            saida.append((parte[1:-1], False, False, True))
        elif parte.startswith("*") and parte.endswith("*"):
            saida.append((parte[1:-1], False, True, False))
        else:
            saida.append((parte, False, False, False))
    return saida


def escreve(
    doc,
    texto,
    *,
    negrito=False,
    italico=False,
    tamanho=None,
    centro=False,
    recuo=True,
    antes=0,
    depois=0,
    recuo_esq=None,
):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER if centro else WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Cm(0.5) if recuo else Cm(0)
    if recuo_esq is not None:
        pf.left_indent = recuo_esq
    pf.space_before, pf.space_after = Pt(antes), Pt(depois)
    for conteudo, n, it, mono in trechos(texto):
        r = p.add_run(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", conteudo))
        r.bold = n or negrito
        r.italic = it or italico
        r.font.size = tamanho or Pt(CORPO_PT)
        r.font.name = "Consolas" if mono else FONTE
    return p


def imagem(doc, caminho: Path):
    """A figura, centralizada, na largura fixa -- a altura sai da proporcao."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.first_line_indent = Cm(0)
    pf.space_before, pf.space_after = Pt(5.75), Pt(2)
    p.add_run().add_picture(str(caminho), width=Cm(LARGURA_FIGURA_CM))
    return p


def barra_lateral(p):
    """A linha preta de 2 1/4 pt na extrema esquerda do bloco de abertura."""
    propriedades = p._p.get_or_add_pPr()
    bordas = propriedades.makeelement(qn("w:pBdr"), {})
    esquerda = propriedades.makeelement(qn("w:left"), {})
    esquerda.set(qn("w:val"), "single")
    esquerda.set(qn("w:sz"), "18")  # 18 oitavos de ponto = 2,25 pt
    esquerda.set(qn("w:space"), "4")
    esquerda.set(qn("w:color"), "000000")
    bordas.append(esquerda)
    propriedades.append(bordas)


def tabela(doc, linhas):
    corpo = [linha for linha in linhas if not re.match(r"^\|[\s:|-]+\|$", linha)]
    celulas = [
        [c.strip() for c in linha.strip().strip("|").split("|")] for linha in corpo
    ]
    largura = max(len(c) for c in celulas)
    t = doc.add_table(rows=0, cols=largura)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, linha in enumerate(celulas):
        cel = t.add_row().cells
        for j in range(largura):
            texto = linha[j] if j < len(linha) else ""
            p = cel[j].paragraphs[0]
            p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.first_line_indent = Cm(0)
            for conteudo, n, it, mono in trechos(texto):
                r = p.add_run(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", conteudo))
                r.bold = n or i == 0
                r.italic = it
                r.font.size = Pt(9)
                r.font.name = "Consolas" if mono else FONTE


# ---------------------------------------------------------------- montagem
def abertura(doc, raiz):
    texto = (raiz / "artigo" / "00-resumo.md").read_text(encoding="utf-8")

    titulo = re.search(r"## Título\n+\*\*(.+?)\*\*", texto, re.S).group(1)
    titulo = " ".join(titulo.split())
    autores = re.search(r"## Autores\n+(.+?)\n", texto).group(1)
    instituicao = re.search(r"\n\*(Centro[^*]+)\*", texto).group(1)

    resumo = re.search(
        r"## Resumo\n.*?\n\nA crescente(.+?)\n\n\*\*Palavras-chave", texto, re.S
    )
    resumo = "A crescente " + " ".join(resumo.group(1).split())
    chaves = re.search(r"\*\*Palavras-chave:\*\*(.+?)\n\n", texto, re.S).group(1)
    # O Abstract saiu em 12/11/2026, por autorizacao do orientador. O montador
    # aceita os dois formatos: se a pagina voltar a te-lo, ele entra de novo.
    m = re.search(r"## Abstract\n.*?\n\nThe growing(.+?)\n\n\*\*Keywords", texto, re.S)
    abstract = "The growing " + " ".join(m.group(1).split()) if m else None
    m = re.search(r"\*\*Keywords:\*\*(.+?)\n\n", texto, re.S)
    keywords = m.group(1) if m else None

    p = escreve(
        doc,
        titulo,
        negrito=True,
        tamanho=Pt(14),
        centro=True,
        recuo=False,
        depois=10,
        recuo_esq=Cm(0.1),
    )
    barra_lateral(p)
    for linha, tam in ((autores.replace(" · ", "\n"), Pt(10)), (instituicao, Pt(9))):
        for parte in linha.split("\n"):
            p = escreve(
                doc,
                parte,
                negrito=(tam == Pt(10)),
                tamanho=tam,
                centro=True,
                recuo=False,
                recuo_esq=Cm(0.1),
            )
            barra_lateral(p)
    p = escreve(doc, "", recuo=False, recuo_esq=Cm(0.1))
    barra_lateral(p)
    blocos = [("Resumo.", resumo)]
    if abstract and keywords:
        blocos.append(("Abstract.", abstract))
    for rotulo, corpo_texto in blocos:
        p = escreve(
            doc,
            f"**{rotulo}** {corpo_texto}",
            italico=True,
            recuo=False,
            recuo_esq=Cm(0.1),
        )
        barra_lateral(p)
        p = escreve(doc, "", recuo=False, recuo_esq=Cm(0.1))
        barra_lateral(p)
        rot = "Palavras-chave:" if rotulo == "Resumo." else "Keywords:"
        valor = chaves if rotulo == "Resumo." else keywords
        p = escreve(
            doc,
            f"**{rot}** {' '.join(valor.split())}",
            italico=True,
            recuo=False,
            recuo_esq=Cm(0.1),
        )
        barra_lateral(p)
        p = escreve(doc, "", recuo=False, recuo_esq=Cm(0.1))
        barra_lateral(p)


def secao(doc, caminho, *, titulo_de_nivel1=True):
    for tipo, nivel, conteudo in blocos(caminho.read_text(encoding="utf-8")):
        if tipo == "titulo":
            if conteudo in SECOES_DE_CONTROLE:
                return
            if nivel == 1 and not titulo_de_nivel1:
                continue
            escreve(
                doc,
                conteudo.upper() if nivel == 1 else conteudo,
                negrito=True,
                recuo=False,
                antes=5.75,
                depois=5.75,
            )
        elif tipo == "legenda":
            # titulo acima da tabela, centralizado, colado nela: e a forma do
            # template da familia ABCM ("Tabela 1. Exemplo de tabela.")
            escreve(doc, conteudo, centro=True, recuo=False, antes=5.75, depois=2)
        elif tipo == "fonte":
            # a fonte vai abaixo, menor, pela NBR 6023 -- exigencia do
            # orientador na entrega de 12/11/2026
            escreve(
                doc,
                conteudo,
                tamanho=Pt(9),
                centro=True,
                recuo=False,
                antes=2,
                depois=5.75,
            )
        elif tipo == "imagem":
            # o caminho do Markdown e relativo ao arquivo que o escreveu
            imagem(doc, (caminho.parent / str(conteudo)).resolve())
        elif tipo == "tabela":
            tabela(doc, conteudo)
        elif tipo == "formula":
            escreve(
                doc,
                conteudo,
                italico=True,
                centro=True,
                recuo=False,
                antes=5.75,
                depois=5.75,
            )
        elif tipo == "item":
            escreve(doc, conteudo.lstrip("*+- "), recuo=False, recuo_esq=Cm(0.5))
        else:
            escreve(doc, conteudo)


def referencias(doc, raiz):
    texto = (raiz / "artigo" / "referencias.md").read_text(encoding="utf-8")
    bloco = texto.split("## Lista", 1)[1].split("### Critérios", 1)[0]
    escreve(doc, "5.5 Referências", negrito=True, recuo=False, antes=5.75, depois=5.75)
    for entrada in re.split(r"\n\s*\n", bloco):
        entrada = entrada.strip()
        if not entrada or entrada.startswith(">"):
            continue
        # Sem espaco entre entradas: as 12 linhas de 6 pt somavam 72 pt de
        # branco puro, e era o que empurrava a ultima referencia para a 13a
        # pagina. Nao e exigencia do template -- era escolha deste programa.
        escreve(doc, " ".join(entrada.split()), recuo=False, depois=0)


def monta_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python scripts/montar_artigo.py",
        description="Monta o artigo no formato COBEM a partir do Markdown de artigo/.",
    )
    parser.add_argument(
        "--raiz",
        type=Path,
        default=RAIZ,
        help="raiz do repositorio (por omissao, esta)",
    )
    parser.add_argument(
        "--saida", type=Path, help="onde gravar; por omissao, artigo/artigo-cobem.docx"
    )
    parser.add_argument(
        "--resultados",
        type=Path,
        help=(
            "um 04-resultados.md de outro lugar. Serve para medir o documento com "
            "a Secao 4 de uma branch que ainda nao entrou na main"
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Monta o documento e devolve o codigo de saida do processo."""
    args = monta_parser().parse_args(argv)
    if not DOCX_DISPONIVEL:
        print(
            "python-docx nao esta instalado. Instale com `pip install python-docx` "
            "-- ele nao esta na lista do CI porque nenhum teste o usa.",
            file=sys.stderr,
        )
        return 1

    raiz = args.raiz
    quatro = args.resultados or raiz / "artigo" / "04-resultados.md"
    destino = args.saida or raiz / "artigo" / "artigo-cobem.docx"

    paginas = [
        raiz / "artigo" / "01-introducao.md",
        raiz / "artigo" / "02-referencial-teorico.md",
        raiz / "artigo" / "03-metodologia.md",
        quatro,
        raiz / "artigo" / "05-conclusao.md",
    ]
    erros = confere_legendas(paginas)
    if erros:
        print(
            "Tabela sem legenda numerada ou sem fonte. O orientador apontou isso "
            "na entrega de 12/11/2026, e o documento nao e montado assim:",
            file=sys.stderr,
        )
        for erro in erros:
            print(f"  {erro}", file=sys.stderr)
        return 1

    doc = Document()
    estilo(doc)
    abertura(doc, raiz)
    for caminho in paginas:
        secao(doc, caminho)
    referencias(doc, raiz)
    destino.parent.mkdir(parents=True, exist_ok=True)
    doc.save(destino)
    print(f"gravado: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
