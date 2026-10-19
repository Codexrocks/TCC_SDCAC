"""O painel do SDCAC.

Quatro telas: **Execucao**, que identifica a rodada e os presets; **Pessoas**,
**Alertas** e **Decomposicao do risco**, em `telas.py`.

A apresentacao das faixas e a parte com exigencia escrita — rotulo junto da cor,
forma propria e contraste conferido por `frontend/components/contraste.py`, com
teste que reprova se qualquer uma das duas regredir.

> **O aceite da S9 nao e demonstravel com a semente de hoje.** Ele diz: "leitor
> externo identifica em menos de 1 min por que um usuario esta em risco alto".
> O `_limites` de `backend/exemplos.json` registra que a semente tem dois
> funcionarios, so eventos `FILE_ACCESS` e **ninguem na faixa `high`** — porque o
> gerador de eventos da S6 ainda nao existe. O painel aguenta isso e **diz** que
> aguenta; povoar a tela com numero inventado para a demonstracao parecer
> completa e o que a secao 3 do AGENTS.md chama de inaceitavel.

Para rodar:

    streamlit run frontend/dashboard/app.py

A fonte padrao e o arquivo de exemplos, que roda sem servidor nem banco.
"""

import streamlit as st

from frontend.components.faixas import legenda_html
from frontend.dashboard.cliente import (
    FonteExemplos,
    FonteHTTP,
    Painel,
    SourceUnavailableError,
)
from frontend.dashboard.telas import (
    tela_alertas,
    tela_decomposicao,
    tela_pessoas,
)

TELAS = ("Execucao", "Pessoas", "Alertas", "Decomposicao do risco")


def monta_fonte(escolha: str, base: str):
    """A fonte que o usuario escolheu na barra lateral."""
    if escolha == "API":
        return FonteHTTP(base)
    return FonteExemplos()


def barra_lateral() -> tuple[Painel, str | None]:
    """A escolha de fonte e de execucao. Devolve o painel e a execucao ativa."""
    st.sidebar.title("SDCAC")
    st.sidebar.caption("Avaliacao multidimensional de risco comportamental")

    escolha = st.sidebar.radio(
        "Fonte dos dados",
        ("Exemplos gravados", "API"),
        help=(
            "Os exemplos sao respostas reais da API, gravadas em "
            "backend/exemplos.json. Rodam sem servidor nem banco."
        ),
    )
    base = ""
    if escolha == "API":
        base = st.sidebar.text_input("Endereco da API", "http://127.0.0.1:8000")

    painel = Painel(monta_fonte(escolha, base))

    saude = None
    try:
        resposta = painel.saude()
        if resposta.ok:
            saude = resposta.corpo
    except SourceUnavailableError as erro:
        st.sidebar.error(str(erro))
        return painel, None

    if saude:
        st.sidebar.success(
            f"{saude.get('status')} · adaptador {saude.get('adapter')} · "
            f"{saude.get('runs')} execucoes"
        )

    execucao = seletor_de_execucao(painel)
    st.sidebar.divider()
    st.sidebar.markdown("**Faixas de risco**", unsafe_allow_html=True)
    st.sidebar.markdown(legenda_html(), unsafe_allow_html=True)
    return painel, execucao


def seletor_de_execucao(painel: Painel) -> str | None:
    """A execucao ativa, escolhida entre as que a fonte conhece."""
    try:
        pagina = painel.execucoes().exigir()
    except SourceUnavailableError as erro:
        st.sidebar.warning(str(erro))
        return None

    itens = pagina.get("items", []) if isinstance(pagina, dict) else []
    if not itens:
        st.sidebar.warning("Nenhuma execucao de pontuacao nesta fonte.")
        return None

    def rotulo(execucao: dict) -> str:
        marca = " · exploratoria" if execucao.get("exploratory") else ""
        return f"{execucao['scoring_run_id']} — {execucao['config_name']}{marca}"

    escolhida = st.sidebar.selectbox("Execucao", itens, format_func=rotulo)
    return escolhida["scoring_run_id"]


def tela_execucao(painel: Painel, execucao: int) -> None:
    """A identidade da execucao: preset, pesos e o commit que a produziu."""
    st.header("Execucao")
    try:
        dados = painel.execucao(execucao).exigir()
    except SourceUnavailableError as erro:
        st.error(str(erro))
        return

    a, b, c = st.columns(3)
    a.metric("Configuracao", dados.get("config_name", "?"))
    b.metric("Pesos", dados.get("weights_version", "?"))
    c.metric("Situacao", dados.get("status", "?"))

    st.caption(
        "O `config_hash` e o `code_sha` sao o que torna a execucao reproduzivel: "
        "dizem com qual parametrizacao e com qual commit do motor ela rodou."
    )
    st.code(
        f"config_hash  {dados.get('config_hash', '?')}\n"
        f"code_sha     {dados.get('code_sha', '?')}\n"
        f"run_id       {dados.get('run_id', '?')}",
        language="text",
    )

    if dados.get("exploratory"):
        st.warning(
            "Execucao **exploratoria**: nao entra na tabela de ablacao do artigo.",
            icon=":material/science:",
        )

    st.subheader("Presets da ablacao")
    try:
        presets = painel.configuracoes().exigir()
    except SourceUnavailableError as erro:
        st.warning(str(erro))
        return
    st.dataframe(
        [
            {
                "Configuracao": p["name"],
                "Dimensoes ligadas": ", ".join(p["dimensions"]),
                "Exploratoria": "sim" if p["exploratory"] else "nao",
            }
            for p in presets
        ],
        hide_index=True,
        width="stretch",
    )


def principal() -> None:
    """Monta a pagina."""
    st.set_page_config(page_title="SDCAC — painel", layout="wide")
    painel, execucao = barra_lateral()

    tela = st.radio("Tela", TELAS, horizontal=True, label_visibility="collapsed")

    if execucao is None:
        st.warning("Escolha uma fonte com execucoes para ver as telas.")
        return

    if tela == "Execucao":
        tela_execucao(painel, execucao)
    elif tela == "Pessoas":
        tela_pessoas(painel, execucao)
    elif tela == "Alertas":
        tela_alertas(painel, execucao)
    else:
        tela_decomposicao(painel, execucao)


if __name__ == "__main__":
    principal()
