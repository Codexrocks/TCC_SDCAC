#!/usr/bin/env python3
"""Gera o quadro do TCC_SDCAC a partir de quadro.toml.

Uso:
    python scripts/quadro.py                    # regenera docs/quadro.md
    python scripts/quadro.py --conferir         # nao escreve; falha se estiver velho
    python scripts/quadro.py --hoje 2026-10-01  # finge outra data

Este script CALCULA. Ele nao interpreta, nao cobra ninguem e nao decide nada:
quem marca uma entrega como feita e uma pessoa, editando o quadro.toml num Pull
Request. A separacao e a mesma do scripts/atividade.py, e e proposital — numero
de relatorio de banca precisa ser reproduzivel, e texto gerado por IA nao e.

O que e FATO mora no TOML: data, dono, criterio, estado. O que e SITUACAO —
atrasado, em curso, vence em N dias — sai daqui, calculado contra a data de
hoje.

A razao e concreta. Em 26/09/2026 o docs/cronograma.md afirmava que a Tarefa 02
vencia "amanha"; o prazo era 24/09, dois dias antes. A frase estava certa no dia
em que foi escrita e nunca mais. Contagem regressiva escrita a mao envelhece em
silencio. Contagem calculada nao envelhece.

Regras do projeto em AGENTS.md. Rotulo textual junto do icone e exigencia de
docs/usabilidade.md, e vale aqui como vale no dashboard.
"""
import argparse
import datetime
import pathlib
import re
import sys
import tomllib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "quadro.toml"
QUADRO = RAIZ / "docs" / "quadro.md"

# Cada coluna leva icone E rotulo escrito. Cor sozinha nao informa quem nao
# distingue cor, e a regra de usabilidade do projeto e explicita quanto a isso.
COLUNAS = (
    ("atrasado", "⚠️", "Atrasado"),
    ("em-curso", "▶️", "Em curso"),
    ("a-vencer", "⏳", "A vencer em 7 dias"),
    ("depois", "🗓️", "Depois"),
    ("feito", "✅", "Feito"),
)

# Blocos injetados em paginas escritas a mao. A prosa em volta continua sendo
# de quem escreveu; so a tabela de fato e gerada. Fora dos marcadores nada e
# tocado.
BLOCOS = {
    "docs/cronograma.md": ("prazos-do-professor", "capitulos", "marcos"),
    "docs/decisoes.md": ("decisoes-abertas", "decisoes-a-confirmar"),
}

MARCA_DATA = "<!-- QUADRO:gerado-em %s -->"
RE_MARCA_DATA = re.compile(r"<!-- QUADRO:gerado-em (\d{4}-\d{2}-\d{2}) -->")
AVISO_GERADO = (
    "<!-- Bloco gerado por scripts/quadro.py a partir de quadro.toml. "
    "Editar aqui nao adianta: a proxima execucao reescreve. -->"
)


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------


def ler_se_existir(caminho):
    """Le o arquivo, ou devolve vazio se ele ainda nao nasceu.

    A primeira execucao gera docs/quadro.md do zero: comparar com um arquivo
    inexistente nao pode ser erro.
    """
    alvo = RAIZ / caminho
    return alvo.read_text(encoding="utf-8") if alvo.exists() else ""


def carregar():
    """Le o quadro.toml. Sai com erro legivel se ele nao existir ou nao casar."""
    if not FONTE.exists():
        sys.exit(f"Nao encontrei {FONTE.name} na raiz do repositorio.")
    try:
        with FONTE.open("rb") as arquivo:
            return tomllib.load(arquivo)
    except tomllib.TOMLDecodeError as erro:
        sys.exit(f"{FONTE.name} esta malformado: {erro}")


def data_registrada():
    """Devolve a data do ultimo retrato gravado em docs/quadro.md, ou None.

    O --conferir usa isto para comparar conteudo contra conteudo. Sem ele, a
    conferencia falharia todo dia so porque o calendario andou — e um check que
    falha sozinho todo dia e um check que as pessoas aprendem a ignorar.
    """
    if not QUADRO.exists():
        return None
    achado = RE_MARCA_DATA.search(QUADRO.read_text(encoding="utf-8"))
    return datetime.date.fromisoformat(achado.group(1)) if achado else None


# ---------------------------------------------------------------------------
# Calculo de situacao
# ---------------------------------------------------------------------------


def semanas_por_id(dados):
    return {s["id"]: s for s in dados.get("semana", [])}


def resolver_prazo(item, semanas):
    """Devolve a data limite do item, venha ela de `prazo` ou de `prazo_semana`.

    Prazo que e uma semana ("fecha na S8") vira o ultimo dia daquela semana.
    Item sem prazo nenhum devolve None, e cai em "Depois" — visivel, em vez de
    sumido.
    """
    if item.get("prazo"):
        return item["prazo"]
    referencia = item.get("prazo_semana")
    if referencia and referencia in semanas:
        return semanas[referencia].get("fim") or semanas[referencia]["inicio"]
    return None


def coluna_de_prazo(prazo, hoje):
    if prazo is None:
        return "depois"
    dias = (prazo - hoje).days
    if dias < 0:
        return "atrasado"
    if dias <= 7:
        return "a-vencer"
    return "depois"


def frase_de_prazo(prazo, hoje):
    """Situacao em texto. Sempre com palavra junto do icone, nunca so o icone."""
    if prazo is None:
        return "🗓️ Sem prazo"
    dias = (prazo - hoje).days
    if dias < 0:
        return "⚠️ Atrasado há " + plural(abs(dias), "dia", "dias")
    if dias == 0:
        return "⏳ Vence hoje"
    if dias <= 7:
        return "⏳ Vence em " + plural(dias, "dia", "dias")
    return f"🗓️ Em {dias} dias"


def plural(quantidade, singular, plural_):
    """Concorda o numero com o substantivo. Pagina publica nao diz "1 item(ns)"."""
    return f"{quantidade} {singular if quantidade == 1 else plural_}"


def br(data):
    """Data no formato que se le em portugues."""
    return data.strftime("%d/%m/%Y") if data else "—"


def celula(texto):
    """Protege o conteudo de quebrar a tabela markdown."""
    return str(texto).replace("|", "\\|").replace("\n", " ").strip()


# ---------------------------------------------------------------------------
# Cartoes
# ---------------------------------------------------------------------------


def cartoes(dados, hoje):
    """Monta todo cartao do quadro e diz em que coluna ele cai.

    Cada cartao e uma tupla pronta para virar linha de tabela:
    (coluna, tipo, id, descricao, quem, prazo_em_texto, situacao).
    """
    semanas = semanas_por_id(dados)
    saida = []

    for tarefa in dados.get("tarefa_professor", []):
        estado = tarefa["estado"]
        prazo = tarefa.get("prazo")
        if estado.startswith("entregue"):
            coluna = "feito"
            quando = tarefa.get("entregue_em")
            parcial = " parcial" if estado == "entregue-parcial" else ""
            situacao = f"✅ Entregue{parcial} em {br(quando)}" if quando else "✅ Entregue"
        elif estado == "recorrente":
            coluna, situacao = "depois", "🔁 Recorrente"
        else:
            coluna, situacao = coluna_de_prazo(prazo, hoje), frase_de_prazo(prazo, hoje)
        saida.append(
            (
                coluna,
                "Professor",
                tarefa["titulo"],
                tarefa.get("ressalva", ""),
                "Todos",
                tarefa.get("quando") or br(prazo),
                situacao,
            )
        )

    for marco in dados.get("marco", []):
        estado = marco["estado"]
        if estado == "fechado":
            coluna, situacao = "feito", "✅ Fechado"
        elif estado == "parcial":
            coluna, situacao = "feito", "✅ Fechado em parte"
        else:
            coluna = coluna_de_prazo(marco["data"], hoje)
            situacao = frase_de_prazo(marco["data"], hoje)
        saida.append(
            (
                coluna,
                "Marco",
                f"{marco['id']} · {marco['titulo']}",
                marco.get("fecha", ""),
                "Todos",
                br(marco["data"]),
                situacao,
            )
        )

    for semana in dados.get("semana", []):
        inicio, fim = semana["inicio"], semana.get("fim")
        if semana.get("pronto"):
            coluna, situacao = "feito", "✅ Entregue"
        elif inicio <= hoje and (fim is None or hoje <= fim):
            restam = (fim - hoje).days if fim else None
            situacao = (
                "▶️ Em curso · " + plural(restam, "dia", "dias") + " até o fim"
                if restam is not None
                else "▶️ Em curso"
            )
            coluna = "em-curso"
        else:
            coluna = coluna_de_prazo(fim or inicio, hoje)
            situacao = frase_de_prazo(fim or inicio, hoje)
        rotulo = semana["id"] + (" · opcional" if semana.get("opcional") else "")
        saida.append(
            (
                coluna,
                "Semana",
                rotulo,
                semana["entregavel"],
                ", ".join(semana.get("donos", [])),
                f"{br(inicio)} a {br(fim)}" if fim else f"a partir de {br(inicio)}",
                situacao,
            )
        )

    for capitulo in dados.get("capitulo", []):
        semana = semanas.get(capitulo.get("semana", ""))
        prazo = (semana.get("fim") or semana.get("inicio")) if semana else None
        if capitulo.get("pronto"):
            coluna, situacao = "feito", "✅ Escrito"
        else:
            coluna, situacao = coluna_de_prazo(prazo, hoje), frase_de_prazo(prazo, hoje)
        saida.append(
            (
                coluna,
                "Capítulo",
                f"{capitulo['numero']}. {capitulo['titulo']}",
                capitulo["estado"],
                "Todos",
                capitulo.get("semana", "—"),
                situacao,
            )
        )

    for decisao in dados.get("decisao", []):
        if decisao["estado"] == "fechada":
            coluna = "feito"
            situacao = f"✅ Fechada em {br(decisao.get('fechada_em'))}"
            prazo_texto = br(decisao.get("fechada_em"))
        else:
            prazo = resolver_prazo(decisao, semanas)
            coluna, situacao = coluna_de_prazo(prazo, hoje), frase_de_prazo(prazo, hoje)
            prazo_texto = decisao.get("prazo_semana") or br(prazo)
            if decisao["estado"] == "a-confirmar":
                situacao += " · a confirmar"
        saida.append(
            (
                coluna,
                "Decisão",
                decisao["id"],
                decisao["titulo"],
                ", ".join(decisao.get("donos", [])) or "—",
                prazo_texto,
                situacao,
            )
        )

    return saida


# ---------------------------------------------------------------------------
# Desenho da pagina
# ---------------------------------------------------------------------------


def tabela(cabecalho, linhas):
    partes = ["| " + " | ".join(cabecalho) + " |"]
    partes.append("|" + "---|" * len(cabecalho))
    for linha in linhas:
        partes.append("| " + " | ".join(celula(c) for c in linha) + " |")
    return "\n".join(partes)


def render_quadro(dados, hoje):
    """Desenha docs/quadro.md inteiro."""
    todos = cartoes(dados, hoje)
    contagem = {chave: 0 for chave, _, _ in COLUNAS}
    for cartao in todos:
        contagem[cartao[0]] += 1

    entrega = dados["projeto"]["entrega"]
    faltam = (entrega - hoje).days

    linhas = [
        "# Quadro",
        "",
        "> **Página gerada — não edite aqui.** Quem manda é o",
        "> [`quadro.toml`](../quadro.toml), na raiz do repositório. Esta página é",
        "> reescrita por `scripts/quadro.py`, e edição feita à mão desaparece na",
        "> execução seguinte.",
        ">",
        "> As colunas não estão escritas em lugar nenhum: são **calculadas** contra a",
        "> data do retrato. É o que impede esta página de dizer \"amanhã\" três dias",
        "> depois — que foi exatamente o que o cronograma fez em 26/09/2026.",
        "",
        MARCA_DATA % hoje.isoformat(),
        "",
        f"**{dados['projeto']['nome']}** · {dados['projeto']['disciplina']}",
        "",
        f"**Retrato de {br(hoje)}.** Entrega do TCC em **{br(entrega)}**, daqui a "
        f"**{plural(faltam, 'dia', 'dias')}**.",
        "",
        "## Resumo",
        "",
        tabela(
            ["Coluna", "Itens"],
            [
                [f"{icone} {rotulo}", str(contagem[chave])]
                for chave, icone, rotulo in COLUNAS
            ],
        ),
        "",
    ]

    for chave, icone, rotulo in COLUNAS:
        da_coluna = [c for c in todos if c[0] == chave]
        linhas.append(f"## {icone} {rotulo}")
        linhas.append("")
        if not da_coluna:
            linhas.append("Nada nesta coluna.")
            linhas.append("")
            continue
        linhas.append(plural(len(da_coluna), "item", "itens") + ".")
        linhas.append("")
        linhas.append(
            tabela(
                ["Tipo", "Item", "O que é", "Quem", "Prazo", "Situação"],
                [[c[1], f"**{c[2]}**", c[3], c[4], c[5], c[6]] for c in da_coluna],
            )
        )
        linhas.append("")

    abertas = {"em-curso", "a-vencer"}
    agora = [
        s
        for s in dados.get("semana", [])
        if not s.get("pronto")
        and any(
            c[0] in abertas and c[1] == "Semana" and c[2].startswith(s["id"])
            for c in todos
        )
    ]
    if agora:
        linhas.append("## Critério de aceite do que está aberto")
        linhas.append("")
        linhas.append(
            "Só das semanas em curso ou vencendo. Critério é o que permite dizer"
        )
        linhas.append(
            "\"pronto\" sem discussão — e sem ele escrito, recusar uma entrega vira"
        )
        linhas.append("atrito.")
        linhas.append("")
        linhas.append(
            tabela(
                ["Semana", "Entregável", "Critério de aceite", "Quem"],
                [
                    [
                        f"**{s['id']}**",
                        s["entregavel"],
                        s["criterio"],
                        ", ".join(s.get("donos", [])),
                    ]
                    for s in agora
                ],
            )
        )
        linhas.append("")

    alertas = [d for d in dados.get("decisao", []) if d.get("alerta")]
    if alertas:
        linhas.append("## Alertas registrados nas decisões")
        linhas.append("")
        linhas.append(
            "Ficam aqui porque são contradições conhecidas entre o que uma decisão"
        )
        linhas.append("promete e o prazo em que ela foi cobrada.")
        linhas.append("")
        for decisao in alertas:
            linhas.append(f"- **{decisao['id']}** — {decisao['alerta']}")
        linhas.append("")

    citacoes = dados.get("citacao", [])
    linhas.append("## Dívida bibliográfica")
    linhas.append("")
    linhas.append(
        plural(len(citacoes), "pendência", "pendências")
        + ". Referência não conferida na fonte é o único"
    )
    linhas.append(
        "item deste quadro que pode reprovar o trabalho por fraude acadêmica, e é o"
    )
    linhas.append("que some mais fácil de vista.")
    linhas.append("")
    linhas.append(
        tabela(
            ["Onde", "O que falta", "Quem", "Aberta desde", "Idade"],
            [
                [
                    f"`{c['onde']}`",
                    c["o_que"],
                    c["dono"],
                    br(c["desde"]),
                    f"{(hoje - c['desde']).days} dias",
                ]
                for c in sorted(citacoes, key=lambda c: c["desde"])
            ],
        )
    )
    linhas.append("")
    linhas.append("## O que ficou fora desta versão")
    linhas.append("")
    linhas.append(
        "Honestidade sobre o limite, porque quadro que finge cobrir tudo esconde o"
    )
    linhas.append("que não cobre:")
    linhas.append("")
    linhas.append(
        "- **A tabela das onze semanas** em [`cronograma.md`](cronograma.md) continua"
    )
    linhas.append(
        "  escrita à mão. As datas dela também estão no `quadro.toml`, então são duas"
    )
    linhas.append(
        "  cópias — é a duplicação que sobrou. O `--conferir` avisa quando divergirem."
    )
    linhas.append(
        "- **A tabela de decisões fechadas** em [`decisoes.md`](decisoes.md) também."
    )
    linhas.append(
        "  Decisão fechada não tem prazo que envelheça, e a prosa do \"o que ficou\" é"
    )
    linhas.append("  conteúdo, não estado.")
    linhas.append("")

    return "\n".join(linhas).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Blocos injetados
# ---------------------------------------------------------------------------


def bloco_prazos_do_professor(dados, hoje):
    linhas = []
    for tarefa in dados.get("tarefa_professor", []):
        estado = tarefa["estado"]
        prazo = tarefa.get("prazo")
        if estado.startswith("entregue"):
            parcial = " parcial" if estado == "entregue-parcial" else ""
            texto = f"✅ **Entregue{parcial} em {br(tarefa.get('entregue_em'))}**"
            if tarefa.get("registro"):
                texto += f" — [registro]({tarefa['registro']})"
        elif estado == "recorrente":
            texto = "🔁 Recorrente"
        else:
            texto = frase_de_prazo(prazo, hoje)
        quando = tarefa.get("quando") or (
            f"**{prazo.strftime('%d/%m/%y')}**" if prazo else "—"
        )
        linhas.append([quando, tarefa["titulo"], texto])
    return tabela(["Data", "Entrega", "Estado"], linhas)


def bloco_capitulos(dados, hoje):
    semanas = semanas_por_id(dados)
    linhas = []
    for capitulo in dados.get("capitulo", []):
        semana = semanas.get(capitulo.get("semana", ""))
        prazo = (semana.get("fim") or semana.get("inicio")) if semana else None
        prevista = capitulo.get("semana", "—")
        if semana and semana["inicio"] <= hoje and (
            semana.get("fim") is None or hoje <= semana["fim"]
        ):
            prevista += " · ▶️ em curso"
        linhas.append(
            [
                f"{capitulo['numero']}. {capitulo['titulo']}",
                capitulo["estado"],
                prevista,
                "✅ Escrito" if capitulo.get("pronto") else frase_de_prazo(prazo, hoje),
            ]
        )
    return tabela(["Capítulo", "Estado", "Semana prevista", "Situação"], linhas)


def bloco_marcos(dados, hoje):
    linhas = []
    for marco in dados.get("marco", []):
        if marco["estado"] == "fechado":
            situacao = "✅ Fechado"
        elif marco["estado"] == "parcial":
            situacao = "✅ Fechado em parte"
        else:
            situacao = frase_de_prazo(marco["data"], hoje)
        linhas.append(
            [
                f"**{marco['id']}** {marco['titulo']}",
                f"**{marco['data'].strftime('%d/%m')}**",
                marco.get("fecha", "—"),
                marco.get("porque", "—"),
                situacao,
            ]
        )
    return tabela(
        ["Marco", "Data", "O que fecha", "Por que é marco", "Situação"], linhas
    )


def _tabela_de_decisoes(dados, hoje, estado):
    semanas = semanas_por_id(dados)
    linhas = []
    for decisao in dados.get("decisao", []):
        if decisao["estado"] != estado:
            continue
        prazo = resolver_prazo(decisao, semanas)
        linhas.append(
            [
                decisao["id"],
                decisao["titulo"],
                decisao.get("proposta", "—"),
                ", ".join(decisao.get("donos", [])) or "—",
                decisao.get("prazo_semana") or br(prazo),
                frase_de_prazo(prazo, hoje),
            ]
        )
    return tabela(
        ["ID", "Decisão", "Proposta", "Dono", "Prazo", "Situação"], linhas
    )


def bloco_decisoes_abertas(dados, hoje):
    return _tabela_de_decisoes(dados, hoje, "aberta")


def bloco_decisoes_a_confirmar(dados, hoje):
    return _tabela_de_decisoes(dados, hoje, "a-confirmar")


DESENHISTAS = {
    "prazos-do-professor": bloco_prazos_do_professor,
    "capitulos": bloco_capitulos,
    "marcos": bloco_marcos,
    "decisoes-abertas": bloco_decisoes_abertas,
    "decisoes-a-confirmar": bloco_decisoes_a_confirmar,
}


def injetar(texto, nome, conteudo):
    """Troca o miolo entre os marcadores do bloco `nome`. Fora deles, nada muda.

    O marcador e comentario HTML. Em docs/ isso e seguro: o GitBook so LE dessa
    pasta. Em artigo/ ele escreve de volta e apaga comentario — foi assim que os
    avisos dos seis capitulos sumiram em 06/09/2026. Por isso nenhum bloco deste
    script mora em artigo/.
    """
    abre = f"<!-- QUADRO:inicio {nome} -->"
    fecha = f"<!-- QUADRO:fim {nome} -->"
    if abre not in texto or fecha not in texto:
        raise SystemExit(f"marcador do bloco {nome!r} nao encontrado")
    antes, resto = texto.split(abre, 1)
    _, depois = resto.split(fecha, 1)
    return f"{antes}{abre}\n{AVISO_GERADO}\n\n{conteudo}\n{fecha}{depois}"


def render_tudo(dados, hoje):
    """Devolve {caminho relativo: conteudo final} para todo arquivo gerado."""
    saidas = {"docs/quadro.md": render_quadro(dados, hoje)}
    for caminho, nomes in BLOCOS.items():
        texto = (RAIZ / caminho).read_text(encoding="utf-8")
        for nome in nomes:
            texto = injetar(texto, nome, DESENHISTAS[nome](dados, hoje))
        saidas[caminho] = texto
    return saidas


# ---------------------------------------------------------------------------
# Conferencia da duplicacao que sobrou
# ---------------------------------------------------------------------------


def checar_semanas_no_cronograma(dados):
    """A tabela das onze semanas continua a mao. Aqui se confere que nao divergiu.

    Nao tenta entender markdown: so exige que o intervalo de cada semana do TOML
    apareca escrito na pagina. Conferencia burra que pega o caso real — alguem
    mudar uma data num lugar so.
    """
    texto = (RAIZ / "docs" / "cronograma.md").read_text(encoding="utf-8")
    faltando = []
    for semana in dados.get("semana", []):
        fim = semana.get("fim")
        if not fim:
            continue
        inicio = semana["inicio"]
        # O cronograma escreve "25/09-01/10" e "30/10-05/11": dia/mes, com o
        # mes do inicio omitido quando e o mesmo dos dois.
        candidatos = (
            f"{inicio.strftime('%d/%m')}–{fim.strftime('%d/%m')}",
            f"{inicio.strftime('%d')}–{fim.strftime('%d/%m')}",
        )
        if not any(c in texto for c in candidatos):
            faltando.append(f"{semana['id']} ({candidatos[0]} ou {candidatos[1]})")
    return faltando


# ---------------------------------------------------------------------------
# Linha de comando
# ---------------------------------------------------------------------------


def main():
    analisador = argparse.ArgumentParser(
        description="Gera o quadro do TCC a partir de quadro.toml."
    )
    analisador.add_argument(
        "--conferir",
        action="store_true",
        help="nao escreve nada; sai com 1 se o gerado estiver diferente do gravado",
    )
    analisador.add_argument(
        "--hoje", help="finge outra data de hoje, no formato AAAA-MM-DD"
    )
    argumentos = analisador.parse_args()

    dados = carregar()

    if argumentos.conferir:
        # Compara conteudo contra conteudo: regenera usando a data do proprio
        # retrato gravado. Sem isso a conferencia falharia todo dia so porque o
        # calendario andou, e check que falha sozinho todo dia e check ignorado.
        hoje = data_registrada()
        if hoje is None:
            sys.exit("docs/quadro.md nao existe ou nao tem a marca de data. Rode sem --conferir.")
    elif argumentos.hoje:
        hoje = datetime.date.fromisoformat(argumentos.hoje)
    else:
        hoje = datetime.date.today()

    saidas = render_tudo(dados, hoje)
    divergentes = [
        caminho
        for caminho, conteudo in saidas.items()
        if ler_se_existir(caminho) != conteudo
    ]
    faltando = checar_semanas_no_cronograma(dados)

    if argumentos.conferir:
        for caminho in divergentes:
            print(f"  desatualizado  {caminho}")
        for item in faltando:
            print(f"  divergente     semana {item} nao aparece em docs/cronograma.md")
        if divergentes or faltando:
            print("")
            print("O quadro nao corresponde ao quadro.toml.")
            print("Rode: python scripts/quadro.py")
            sys.exit(1)
        print(f"Quadro em dia (retrato de {br(hoje)}).")
        return

    for caminho, conteudo in saidas.items():
        (RAIZ / caminho).write_text(conteudo, encoding="utf-8", newline="\n")
        marca = "atualizado" if caminho in divergentes else "sem mudanca"
        print(f"  {marca:12} {caminho}")
    for item in faltando:
        print(f"  aviso        semana {item} nao aparece em docs/cronograma.md")
    print(f"\nQuadro gerado para {br(hoje)}.")


if __name__ == "__main__":
    main()
