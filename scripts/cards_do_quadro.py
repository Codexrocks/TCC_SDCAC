#!/usr/bin/env python3
"""Exporta os cards do quadro.toml em JSON, para o quadro compartilhado.

Uso:
    python scripts/cards_do_quadro.py cards.json

O quadro compartilhado e uma pagina publicada fora do repositorio, em
claude.ai, onde os tres marcam o que concluiram e escrevem o que estao
fazendo. Os cards dela saem DAQUI: mesma fonte de verdade que o
scripts/quadro.py le, para nao existir uma terceira copia dos prazos.

POR QUE ESTE ARQUIVO ESTA NO REPOSITORIO
----------------------------------------
Ele viveu num diretorio temporario entre 26/09 e 15/10, e **se perdeu** quando
o temporario foi limpo. Era a unica peca capaz de regerar os cards: sem ela, a
pagina publicada sO poderia ser atualizada a mao, card por card. Ferramenta que
o projeto depende nao mora em pasta temporaria.

O QUE ELE NAO FAZ
-----------------
Nao calcula situacao. "Atrasado", "vence em N dias" e a coluna do kanban saem da
propria pagina, contra a data de quem abre — pelo mesmo motivo que o
scripts/quadro.py calcula em vez de gravar. Daqui saem so fato e estado.
"""
import argparse
import json
import pathlib
import tomllib
from typing import Any

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PESSOAS = ("Davi", "Yasmin", "Filipe")

Registro = dict[str, Any]

# Paginas do GitBook publico. Os caminhos foram LIDOS do sitemap-pages.xml do
# proprio site, nao deduzidos do titulo: o slug vem do nome do arquivo, e nao do
# titulo do menu — "decisoes", nao "registro-de-decisoes".
GITBOOK = "https://tcc-sdcac.gitbook.io/tcc_sdcac-docs/"
PAGINAS = {
    "cronograma": "o-trabalho/cronograma",
    "decisoes": "o-trabalho/decisoes",
    "quadro": "o-trabalho/quadro",
    "usabilidade": "o-sistema/usabilidade",
    "citacoes": "o-artigo/citacoes-pendentes",
    "tarefa-01": "entregas/tarefa-01",
    "tarefa-02": "entregas/tarefa-02",
}

# Ancoras das decisoes que tem secao propria na pagina. Lidas do DOM da pagina
# publicada, nao deduzidas: o "/" de ISO/IEC vira hifen, e a da D-14 carrega o
# titulo inteiro. FRAGILIDADE: a ancora vem do TEXTO do titulo, entao renomear
# um desses titulos quebra o link em silencio.
ANCORAS = {
    "D-12": "#d-12-unidade-de-analise",
    "D-13": "#d-13-tratamento-estatistico",
    "D-14": "#d-14-a-metrica-primaria-pode-nao-existir-para-a-c0",
    "D-15": "#d-15-criterio-de-relevancia-declarado-antes",
    "D-16": "#d-16-falta-o-controle-negativo-longitudinal",
    "D-17": "#d-17-vazamento-no-baseline-da-d2",
    "D-18": "#d-18-dupla-contagem-e-escala-na-integracao",
    "D-19": "#d-19-a-vertente-lgpd-e-iso-iec-27001",
}


def pagina(chave: str) -> str:
    return GITBOOK + PAGINAS[chave]


def executor(donos: list[str]) -> str:
    """Normaliza os donos para a coluna de quem executa.

    "Davi (caneta)" -> davi. Dois ou mais nomes, ou "Todos", caem em equipe:
    card repetido em duas colunas confunde mais do que informa.
    """
    texto = " ".join(donos)
    if "Todos" in texto:
        return "equipe"
    achados = [p.lower() for p in PESSOAS if p in texto]
    return achados[0] if len(achados) == 1 else "equipe"


def doc_de(tipo: str, ident: str, onde: str = "") -> str | None:
    """Onde o GitBook explica este card."""
    if tipo in ("Semana", "Marco"):
        return pagina("cronograma")
    if tipo == "Decisão":
        return pagina("decisoes") + ANCORAS.get(ident, "")
    if tipo == "Professor":
        return pagina(ident) if ident in ("tarefa-01", "tarefa-02") else pagina("cronograma")
    if tipo == "Capítulo":
        return pagina("tarefa-02") if ident == "cap-1" else pagina("cronograma")
    if tipo == "Citação":
        return pagina("usabilidade") if "usabilidade" in onde else pagina("citacoes")
    return None


def card(
    tipo: str,
    ident: str,
    titulo: str,
    detalhe: str,
    donos: list[str],
    prazo: Any,
    extra: Registro | None = None,
) -> Registro:
    extra = extra or {}
    return {
        "id": ident,
        "tipo": tipo,
        "titulo": titulo,
        "detalhe": detalhe or "",
        "quem": ", ".join(donos) if donos else "—",
        "grupo": executor(donos),
        "prazo": prazo.isoformat() if prazo else None,
        "doc": doc_de(tipo, ident, extra.get("onde", "")),
        **extra,
    }


def monta(dados: Registro) -> list[Registro]:
    """Um card por item do quadro.toml, sem perder nenhum."""
    semanas = {s["id"]: s for s in dados["semana"]}
    cards: list[Registro] = []

    for t in dados["tarefa_professor"]:
        if t["estado"] == "recorrente":
            continue
        cards.append(
            card(
                "Professor", t["id"], t["titulo"], t.get("ressalva", ""),
                ["Todos"], t.get("prazo"),
                {
                    "pronto": t["estado"].startswith("entregue"),
                    "parcial": t["estado"] == "entregue-parcial",
                    "fazendo": bool(t.get("andamento")),
                    "andamento": t.get("andamento", ""),
                    "quando": t.get("quando"),
                },
            )
        )

    for m in dados["marco"]:
        cards.append(
            card(
                "Marco", m["id"], f"{m['id']} · {m['titulo']}", m.get("fecha", ""),
                ["Todos"], m["data"],
                {
                    "pronto": m["estado"] == "fechado",
                    "parcial": m["estado"] == "parcial",
                    "fazendo": bool(m.get("andamento")),
                    "andamento": m.get("andamento", ""),
                },
            )
        )

    for s in dados["semana"]:
        cards.append(
            card(
                "Semana", s["id"], f"{s['id']} — {s['entregavel']}", s["criterio"],
                s.get("donos", []), s.get("fim"),
                {
                    "pronto": bool(s.get("pronto")),
                    "fazendo": bool(s.get("andamento")),
                    "andamento": s.get("andamento", ""),
                    "opcional": bool(s.get("opcional")),
                    "inicio": s["inicio"].isoformat(),
                },
            )
        )

    for c in dados["capitulo"]:
        sem = semanas.get(c.get("semana", ""))
        cards.append(
            card(
                "Capítulo", f"cap-{c['numero']}", f"{c['numero']}. {c['titulo']}",
                c["estado"], c.get("donos", ["Todos"]),
                (sem.get("fim") or sem["inicio"]) if sem else None,
                {
                    "pronto": bool(c.get("pronto")),
                    "fazendo": bool(c.get("andamento")),
                    "andamento": c.get("andamento", ""),
                    "semana": c.get("semana"),
                },
            )
        )

    for d in dados["decisao"]:
        prazo = d.get("prazo")
        if not prazo and d.get("prazo_semana") in semanas:
            ref = semanas[d["prazo_semana"]]
            prazo = ref.get("fim") or ref["inicio"]
        fechada = d["estado"] == "fechada"
        cards.append(
            card(
                "Decisão", d["id"], f"{d['id']} · {d['titulo']}", d.get("proposta", ""),
                d.get("donos", []), d.get("fechada_em") if fechada else prazo,
                {
                    "pronto": fechada,
                    "fazendo": bool(d.get("andamento")),
                    "andamento": d.get("andamento", ""),
                    "aConfirmar": d["estado"] == "a-confirmar",
                    "alerta": d.get("alerta", ""),
                },
            )
        )

    for i, c in enumerate(dados["citacao"], start=1):
        cards.append(
            card(
                "Citação", f"cit-{i}", c["onde"], c["o_que"], [c["dono"]], None,
                {"pronto": False, "fazendo": False, "andamento": "",
                 "desde": c["desde"].isoformat(), "onde": c["onde"]},
            )
        )

    return cards


def main() -> None:
    analisador = argparse.ArgumentParser(
        description="Exporta os cards do quadro.toml em JSON."
    )
    analisador.add_argument("destino", help="arquivo JSON a gravar")
    argumentos = analisador.parse_args()

    with (RAIZ / "quadro.toml").open("rb") as arquivo:
        dados = tomllib.load(arquivo)
    cards = monta(dados)

    saida = {
        "projeto": dados["projeto"]["nome"],
        "disciplina": dados["projeto"]["disciplina"],
        "entrega": dados["projeto"]["entrega"].isoformat(),
        "cards": cards,
    }
    pathlib.Path(argumentos.destino).write_text(
        json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    por_grupo: dict[str, int] = {}
    for c in cards:
        por_grupo[c["grupo"]] = por_grupo.get(c["grupo"], 0) + 1
    print(f"{len(cards)} cards")
    print(f"  por executor: {por_grupo}")
    print(f"  prontos:      {sum(1 for c in cards if c.get('pronto'))}")
    print(f"  em andamento: {sum(1 for c in cards if c.get('fazendo'))}")


if __name__ == "__main__":
    main()
