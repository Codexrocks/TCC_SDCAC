"""As tres telas analiticas do painel.

**Pessoas** — quem esta em que faixa, nesta execucao.
**Alertas** — a fila de triagem, filtravel por faixa e periodo.
**Decomposicao do risco** — de onde vieram os pontos de um evento.

A terceira e a que o aceite da S9 cobra por nome, e as outras duas existem para
chegar ate ela: a pergunta "por que esta pessoa esta em risco alto" se responde
indo da lista ao evento, e do evento as parcelas.

**O que a semente de hoje permite mostrar.** Dois funcionarios, so eventos
`FILE_ACCESS`, ninguem na faixa `high` e nenhuma metrica gravada. As telas
renderizam isso sem quebrar e **dizem** o que falta, em vez de parecerem vazias
por defeito. Quando o gerador da S6 existir, as mesmas telas mostram o resto sem
uma linha nova.
"""

from typing import Any

import streamlit as st

from frontend.components.faixas import faixa_de, selo_html
from frontend.components.parcelas import (
    barra_html,
    motivo_html,
    parcelas_de,
    soma_das_parcelas,
)
from frontend.dashboard.cliente import Painel, SourceUnavailableError

FAIXAS_DO_FILTRO = ("todas", "normal", "low", "medium", "high")


def _pagina(painel_resposta) -> tuple[list[dict], int]:
    """Os itens e o total de uma resposta paginada."""
    corpo = painel_resposta.exigir()
    if isinstance(corpo, list):
        return corpo, len(corpo)
    return corpo.get("items", []), corpo.get("total", 0)


def _instante(iso: str | None) -> str:
    """`2026-04-03T13:30:00Z` vira `03/04 13:30`, que e o que se le numa fila."""
    if not iso:
        return "—"
    try:
        data, hora = iso.replace("Z", "").split("T")
        ano, mes, dia = data.split("-")
        return f"{dia}/{mes} {hora[:5]}"
    except ValueError:
        return iso


def _rotulo_da_pessoa(pessoas: list[dict], identificador: int) -> str:
    """`Funcionario 8 · RISCO BAIXO 34` — a faixa aparece antes de escolher."""
    pessoa = next((p for p in pessoas if p["employee_id"] == identificador), None)
    if pessoa is None:
        return f"Funcionario {identificador}"
    faixa = faixa_de(pessoa["band"])
    return (
        f"Funcionario {identificador} · {faixa.rotulo} {pessoa.get('final_raw', 0):g}"
    )


def _aviso_da_semente(quantos: int, oque: str) -> None:
    """Diz que a lista e curta por causa da semente, e nao por erro."""
    if quantos:
        return
    st.info(
        f"Nenhum {oque} nesta execucao. A semente de hoje tem dois funcionarios "
        "e so eventos `FILE_ACCESS` — o gerador de eventos da **S6** e o que "
        "falta para esta tela ter o que mostrar.",
        icon=":material/info:",
    )


# ---------------------------------------------------------------------------
# Pessoas
# ---------------------------------------------------------------------------


def tela_pessoas(painel: Painel, execucao: int) -> None:
    """A nota mais recente de cada pessoa, com a faixa legivel sem a cor."""
    st.header("Pessoas")
    st.caption(
        "A nota mais recente de cada pessoa nesta execucao. Escolha uma para ver "
        "o historico e abrir a decomposicao de um evento."
    )
    try:
        itens, total = _pagina(painel.funcionarios(execucao))
    except SourceUnavailableError as erro:
        st.error(str(erro))
        return

    _aviso_da_semente(total, "funcionario pontuado")
    if not itens:
        return

    ordenados = sorted(itens, key=lambda i: i.get("final_raw", 0), reverse=True)
    for pessoa in ordenados:
        with st.container(border=True):
            esquerda, direita = st.columns([1, 2])
            esquerda.markdown(
                selo_html(pessoa["band"], nota=pessoa.get("final_raw", 0)),
                unsafe_allow_html=True,
            )
            esquerda.markdown(f"**Funcionario {pessoa['employee_id']}**")
            direita.caption(
                f"ultimo evento `{pessoa['event_id']}` em "
                f"{_instante(pessoa.get('occurred_at'))} · configuracao "
                f"{pessoa.get('configuration', '?')}"
            )
            try:
                direita.markdown(
                    barra_html(parcelas_de(pessoa), largura=320), unsafe_allow_html=True
                )
            except ValueError as erro:
                direita.warning(str(erro))

    st.caption(f"{total} pessoa(s) nesta execucao.")


# ---------------------------------------------------------------------------
# Alertas
# ---------------------------------------------------------------------------


def tela_alertas(painel: Painel, execucao: int) -> None:
    """A fila de triagem, com os filtros que o contrato oferece."""
    st.header("Alertas")
    st.caption(
        "A fila que um analista triaria. O limiar e o da configuracao: alerta so "
        "sobe acima dele, e faixa normal nao entra na fila de proposito."
    )

    a, b, c = st.columns(3)
    faixa = a.selectbox("Faixa", FAIXAS_DO_FILTRO)
    desde = b.text_input("Desde (ISO 8601)", "", placeholder="2026-04-01T00:00:00Z")
    ate = c.text_input("Ate (ISO 8601)", "", placeholder="2026-04-03T23:59:59Z")

    filtrando = faixa != "todas" or desde or ate
    try:
        resposta = painel.alertas(
            execucao,
            band=None if faixa == "todas" else faixa,
            since=desde or None,
            until=ate or None,
        )
        itens, total = _pagina(resposta)
    except SourceUnavailableError as erro:
        if filtrando:
            st.warning(
                "A fonte de exemplos guarda uma resposta por rota e **nao aplica "
                "filtro**. Para filtrar, aponte a barra lateral para a API.",
                icon=":material/filter_alt_off:",
            )
        else:
            st.error(str(erro))
        return

    _aviso_da_semente(total, "alerta")
    if not itens:
        return

    for alerta in itens:
        com_janela = alerta.get("window_start") and alerta.get("window_end")
        linha = st.columns([2, 3, 2])
        linha[0].markdown(selo_html(alerta["band"]), unsafe_allow_html=True)
        alvo = (
            f"evento `{alerta['event_id']}`"
            if alerta.get("event_id")
            else f"funcionario {alerta.get('employee_id')}"
        )
        janela = (
            f" · janela {_instante(alerta['window_start'])} a "
            f"{_instante(alerta['window_end'])}"
            if com_janela
            else ""
        )
        linha[1].markdown(f"{alvo}{janela}")
        linha[2].caption(
            f"{_instante(alerta.get('raised_at'))} · limiar {alerta.get('threshold', 0):g}"
        )

    st.caption(f"{total} alerta(s).")
    if all(a["band"] == "low" for a in itens):
        st.info(
            "Todos os alertas desta execucao estao na faixa **RISCO BAIXO**. "
            "Nao ha ninguem em `high` na semente atual — ver o campo `_limites` "
            "de `backend/exemplos.json`.",
            icon=":material/info:",
        )


# ---------------------------------------------------------------------------
# Decomposicao do risco
# ---------------------------------------------------------------------------


def tela_decomposicao(painel: Painel, execucao: int) -> None:
    """De onde vieram os pontos de um evento — a tela do aceite da S9."""
    st.header("Decomposicao do risco")
    st.caption(
        "Escolha a pessoa e o evento. A tela mostra quanto cada dimensao somou e "
        "qual regra disparou, com o motivo escrito."
    )

    try:
        pessoas, _ = _pagina(painel.funcionarios(execucao))
    except SourceUnavailableError as erro:
        st.error(str(erro))
        return
    if not pessoas:
        _aviso_da_semente(0, "funcionario pontuado")
        return

    # Da maior nota para a menor: numa fila de triagem, quem se investiga
    # primeiro e quem esta pior, e e nele que a tela precisa abrir sozinha.
    por_risco = sorted(pessoas, key=lambda p: p.get("final_raw", 0), reverse=True)
    quem = st.selectbox(
        "Funcionario",
        [p["employee_id"] for p in por_risco],
        format_func=lambda i: _rotulo_da_pessoa(por_risco, i),
    )

    try:
        eventos, _ = _pagina(painel.funcionario(execucao, quem))
    except SourceUnavailableError as erro:
        st.warning(
            f"{erro}\n\nA fonte de exemplos guarda uma resposta por rota, e o "
            "historico desta pessoa nao esta entre elas. Para ver qualquer "
            "pessoa, aponte a barra lateral para a **API**.",
            icon=":material/history_toggle_off:",
        )
        return
    if not eventos:
        st.info("Esta pessoa nao tem evento pontuado nesta execucao.")
        return

    escolhido = st.selectbox(
        "Evento",
        eventos,
        format_func=lambda e: (
            f"{e['event_id']} · {_instante(e.get('occurred_at'))} · "
            f"{faixa_de(e['band']).rotulo} {e.get('final_raw', 0):g}"
        ),
    )
    mostra_evento(escolhido)


def mostra_evento(evento: dict[str, Any]) -> None:
    """A nota de um evento, decomposta por dimensao e por regra."""
    total = evento.get("final_raw", 0)
    st.markdown(selo_html(evento["band"], nota=total), unsafe_allow_html=True)
    st.caption(
        f"evento `{evento['event_id']}` · {evento.get('event_type', '?')} · "
        f"{_instante(evento.get('occurred_at'))} · configuracao "
        f"{evento.get('configuration', '?')}"
    )

    try:
        parcelas = parcelas_de(evento)
    except ValueError as erro:
        st.error(str(erro))
        return

    st.subheader("De onde vieram os pontos")
    st.markdown(barra_html(parcelas), unsafe_allow_html=True)

    for parcela in parcelas:
        colunas = st.columns([3, 5, 1])
        if parcela.ligada:
            colunas[0].markdown(f"**{parcela.dimensao.rotulo}**")
            colunas[1].caption(parcela.dimensao.pergunta)
            colunas[2].markdown(f"**{parcela.texto}**")
        else:
            colunas[0].markdown(
                f"<span style='opacity:.55'>{parcela.dimensao.rotulo}</span>",
                unsafe_allow_html=True,
            )
            colunas[1].caption("a configuracao nao liga esta dimensao")
            colunas[2].markdown(
                "<span style='opacity:.55'>—</span>", unsafe_allow_html=True
            )

    soma = soma_das_parcelas(parcelas)
    if abs(soma - total) > 0.01:
        st.warning(
            f"As parcelas somam {soma:g} e a nota final e {total:g}. A diferenca "
            "vem dos pesos da configuracao, que a nota final aplica e a soma crua "
            "nao — ver `detection/presets.toml`.",
            icon=":material/calculate:",
        )

    st.subheader("Qual regra disparou")
    acertos = evento.get("hits") or []
    if not acertos:
        st.info("Nenhuma regra registrou motivo para este evento.")
        return
    for hit in acertos:
        st.markdown(motivo_html(hit), unsafe_allow_html=True)
