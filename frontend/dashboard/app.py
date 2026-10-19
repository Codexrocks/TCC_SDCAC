"""O painel do SDCAC — esqueleto.

**O que esta pronto:** a navegacao, a escolha da fonte, a selecao de execucao, o
indicador de saude e a apresentacao das faixas de risco, que e a parte com
exigencia escrita — rotulo junto da cor, forma propria e contraste conferido por
`frontend/components/contraste.py`.

**O que falta:** as tres telas analiticas. Cada uma esta marcada abaixo com a
rota que a alimenta, o que o aceite da S9 cobra dela e o que ainda falta para
ela ser demonstravel. **Dono: Filipe, S9 (23 a 29/10).**

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

from frontend.components.faixas import FAIXAS, legenda_html, selo_html
from frontend.dashboard.cliente import (
    FonteExemplos,
    FonteHTTP,
    Painel,
    SourceUnavailableError,
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


def a_escrever(titulo: str, rota: str, aceite: str, falta: str) -> None:
    """O lugar de uma tela que ainda nao existe, dizendo o que ela precisa.

    Tela vazia sem explicacao vira duvida de quem abre o painel. Esta diz qual
    rota a alimenta, o que o aceite cobra e o que falta — para o Filipe comecar
    sem reler o cronograma, e para quem abrir entender que falta, nao quebrou.
    """
    st.header(titulo)
    st.info(
        f"**A escrever — S9, Filipe.**\n\n"
        f"**Rota que alimenta:** `{rota}`\n\n"
        f"**O que o aceite cobra:** {aceite}\n\n"
        f"**O que falta:** {falta}",
        icon=":material/construction:",
    )
    st.markdown("**Como a faixa aparece, quando a tela existir:**")
    st.markdown(
        " ".join(
            selo_html(f.band, nota=nota)
            for f, nota in zip(FAIXAS.values(), (8, 34, 61, 88), strict=True)
        ),
        unsafe_allow_html=True,
    )
    st.caption(
        "Os selos acima usam `frontend/components/faixas.py`. Rotulo, forma e "
        "contraste ja estao conferidos por teste — a tela nova nao precisa "
        "escolher cor, so usar o selo."
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
        a_escrever(
            "Pessoas",
            f"/api/v1/runs/{execucao}/employees",
            "a lista ordenada por nota, com a faixa de cada pessoa legivel sem "
            "depender da cor.",
            "nada na API. A rota responde; a tela e que falta.",
        )
    elif tela == "Alertas":
        a_escrever(
            "Alertas",
            f"/api/v1/runs/{execucao}/alerts",
            "a fila de triagem, filtravel por faixa e periodo.",
            "o gerador de eventos da S6. A semente de hoje tem dois funcionarios "
            "e **ninguem na faixa `high`**, entao a fila de triagem nao tem o que "
            "triar — e nao se inventa alerta para a tela parecer cheia.",
        )
    else:
        a_escrever(
            "Decomposicao do risco",
            f"/api/v1/runs/{execucao}/events/{{event_id}}",
            "**o aceite da S9 em pessoa:** leitor externo identifica em menos de "
            "1 min por que um usuario esta em risco alto. Exige as cinco parcelas "
            "visiveis — `c0`, `d1`, `d2`, `d3_conduct` e `d3_posture`, as duas da "
            "D3 **separadas**, pela D-25 — e o `hits`, que traz o motivo em texto.",
            "a tela. A rota ja devolve tudo: parcelas, nota e motivo escrito. "
            "O que falta demonstrar e o caminho do risco alto, que depende da S6.",
        )


if __name__ == "__main__":
    principal()
