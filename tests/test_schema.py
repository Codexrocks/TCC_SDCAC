"""Testes do schema dos tres bancos.

Estes testes nao precisam de PostgreSQL rodando: eles comparam o SQL de
`database/` com a especificacao de `docs/banco-simulado.md` e com as decisoes
que o schema precisa cumprir.

O motivo de existirem e um defeito que ja aconteceu neste projeto: a
especificacao foi consolidada a partir de dois documentos em versoes
diferentes, e o `SYSTEM_CONFIG` ficou sem o valor que religa o MFA. Ninguem
percebeu por dias. Divergencia entre o documento e a implementacao nao se
resolve com atencao — se resolve com teste.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "database"
ESPECIFICACAO = (RAIZ / "docs" / "banco-simulado.md").read_text(encoding="utf-8")

CORP = (BANCO / "corp" / "001_schema.sql").read_text(encoding="utf-8")
CORP_PRIV = (BANCO / "corp" / "002_privilegios.sql").read_text(encoding="utf-8")
GABARITO = (BANCO / "ground_truth" / "001_schema.sql").read_text(encoding="utf-8")
GABARITO_PRIV = (BANCO / "ground_truth" / "002_privilegios.sql").read_text(
    encoding="utf-8"
)
SDCAC = (BANCO / "sdcac" / "001_schema.sql").read_text(encoding="utf-8")
SDCAC_PRIV = (BANCO / "sdcac" / "002_privilegios.sql").read_text(encoding="utf-8")
BANCOS = (BANCO / "00_bancos_e_papeis.sql").read_text(encoding="utf-8")

TODOS_OS_SQL = [CORP, CORP_PRIV, GABARITO, GABARITO_PRIV, SDCAC, SDCAC_PRIV, BANCOS]


# ---------------------------------------------------------------------------
# Leitura do SQL e da especificacao
# ---------------------------------------------------------------------------


def sem_comentarios(sql: str) -> str:
    """Tira as linhas de comentario do SQL.

    Sem isso, um teste que procura `GRANT UPDATE` acha a frase no comentario
    que explica por que aquele GRANT nao existe — e reprova o arquivo certo.
    Aconteceu na primeira execucao destes testes.
    """
    return "\n".join(
        linha for linha in sql.splitlines() if not linha.lstrip().startswith("--")
    )


def enums_do_sql(sql: str) -> dict[str, list[str]]:
    """Devolve {nome do tipo: valores} de cada CREATE TYPE ... AS ENUM."""
    achados = {}
    for nome, corpo in re.findall(
        r"CREATE TYPE (\w+) AS ENUM \((.*?)\);", sql, re.DOTALL
    ):
        achados[nome] = re.findall(r"'([^']+)'", corpo)
    return achados


def tabela_de_listas_fechadas() -> dict[str, list[str]]:
    """Le a tabela "Listas fechadas" da especificacao."""
    trecho = ESPECIFICACAO.split("### Listas fechadas", 1)[1]
    trecho = trecho.split("###", 1)[0]
    listas = {}
    for linha in trecho.splitlines():
        if not linha.startswith("|") or "---" in linha:
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if len(celulas) != 2 or celulas[0] == "Campo":
            continue
        campo = celulas[0].strip("`")
        valores = re.findall(r"`([^`]+)`", celulas[1])
        if valores:
            listas[campo] = valores
    return listas


def campos_do_envelope() -> list[str]:
    """Le os nomes de campo da tabela do envelope, secao 2 da especificacao."""
    trecho = ESPECIFICACAO.split("## 2. O envelope", 1)[1].split("## 3.", 1)[0]
    campos = []
    for linha in trecho.splitlines():
        if not linha.startswith("| `"):
            continue
        primeira = linha.strip("|").split("|")[0].strip()
        campos.append(primeira.strip("`"))
    return campos


# ---------------------------------------------------------------------------
# O SQL nao pode divergir da especificacao
# ---------------------------------------------------------------------------

# Como o nome do campo na especificacao se chama no SQL.
EQUIVALENCIA = {
    "event_type": "event_type",
    "result": "event_result",
    "sensitivity": "sensitivity_level",
    "Tipo de faixa de rede": "network_kind",
}


def test_listas_fechadas_batem_com_a_especificacao():
    listas = tabela_de_listas_fechadas()
    enums = enums_do_sql(CORP)

    assert listas, "nao achei a tabela de listas fechadas na especificacao"

    for campo, valores in listas.items():
        tipo = EQUIVALENCIA[campo]
        assert tipo in enums, f"o tipo {tipo} nao existe no schema do corp"
        assert enums[tipo] == valores, (
            f"{tipo} no SQL tem {enums[tipo]}, e a especificacao diz {valores}"
        )


def test_envelope_tem_todos_os_campos_da_especificacao():
    colunas = CORP.split("CREATE TABLE events (", 1)[1].split(") PARTITION BY", 1)[0]
    for campo in campos_do_envelope():
        assert re.search(rf"^\s+{campo}\s", colunas, re.MULTILINE), (
            f"o campo {campo} do envelope nao existe na tabela events"
        )


def test_tabelas_de_apoio_e_de_estado_existem():
    """As tabelas das secoes 4, 5 e 6 da especificacao."""
    esperadas = {
        CORP: [
            "runs",
            "departments",
            "positions",
            "sites",
            "resources",
            "resource_access",
            "network_ranges",
            "employees",
            "devices",
            "sessions",
            "hr_calendar",
            "device_state_daily",
            "account_state",
            "events",
        ],
        GABARITO: ["episodes", "labels"],
        SDCAC: ["baselines", "scoring_runs", "risk_scores", "alerts", "metrics"],
    }
    for sql, tabelas in esperadas.items():
        for tabela in tabelas:
            assert f"CREATE TABLE {tabela} (" in sql, f"falta a tabela {tabela}"


# ---------------------------------------------------------------------------
# As travas que o schema carrega
# ---------------------------------------------------------------------------


def test_sensitivity_nao_entra_no_jsonb():
    """Checagem da secao 9: sensibilidade e atributo do recurso, nao do evento."""
    assert "NOT (attributes ? 'sensitivity')" in CORP


def test_eventos_nao_guardam_rotulo():
    """O gabarito mora em outro banco. Rotulo no corp e vazamento."""
    colunas = CORP.split("CREATE TABLE events (", 1)[1].split(") PARTITION BY", 1)[0]
    for proibida in ("label", "is_anomalous", "scenario", "episode"):
        assert proibida not in colunas.lower(), (
            f"a tabela events tem coluna de rotulo: {proibida}"
        )


def test_aplicacao_nao_conecta_no_gabarito():
    """A trava contra vazamento de rotulo, equivalente estrutural da D-17."""
    bancos = sem_comentarios(BANCOS)
    assert "REVOKE CONNECT ON DATABASE ground_truth FROM PUBLIC;" in bancos

    concessoes = re.findall(
        r"GRANT CONNECT ON DATABASE ground_truth TO ([^;]+);", bancos
    )
    assert concessoes, "ninguem recebe CONNECT no ground_truth"
    for linha in concessoes:
        assert "sdcac_app" not in linha, (
            "sdcac_app recebeu CONNECT no ground_truth: a trava caiu"
        )

    assert "sdcac_app" not in sem_comentarios(GABARITO_PRIV), (
        "sdcac_app aparece nos privilegios do ground_truth"
    )


def test_eventos_so_aceitam_insercao():
    """Log e evidencia: ninguem recebe UPDATE nem DELETE."""
    for sql in (CORP_PRIV, GABARITO_PRIV, SDCAC_PRIV):
        comandos = sem_comentarios(sql)
        assert not re.search(
            r"GRANT[^;]*\bUPDATE\b", comandos, re.DOTALL | re.IGNORECASE
        )
        assert not re.search(
            r"GRANT[^;]*\bDELETE\b", comandos, re.DOTALL | re.IGNORECASE
        )


def test_avaliador_nao_escreve_nota():
    """Quem ve o gabarito nao mexe no score."""
    insercoes = re.findall(r"GRANT INSERT ON ([^;]+) TO evaluator;", SDCAC_PRIV)
    assert insercoes == ["metrics"], (
        f"o evaluator insere em {insercoes}, e devia inserir so em metrics"
    )


def test_execucao_sem_hash_de_configuracao_e_erro():
    """D-34: configuracao presa ao resultado, nao opcional."""
    bloco = SDCAC.split("CREATE TABLE scoring_runs (", 1)[1].split(");", 1)[0]
    for coluna in ("config_hash", "weights_version", "code_sha", "config"):
        assert re.search(rf"{coluna}\s+\S+\s+NOT NULL", bloco), (
            f"{coluna} precisa ser NOT NULL em scoring_runs"
        )


def test_configuracao_exploratoria_e_marcada():
    """D-33: resultado de configuracao livre nao pode ir ao artigo sem aviso."""
    assert "exploratory" in SDCAC


def test_nota_guarda_as_cinco_parcelas():
    """D-36: numero unico impediria a decomponibilidade da secao 3.9 do artigo."""
    bloco = SDCAC.split("CREATE TABLE risk_scores (", 1)[1].split(");", 1)[0]
    for parcela in ("c0", "d1", "d2", "d3_conduct", "d3_posture"):
        assert re.search(rf"^\s+{parcela}\s", bloco, re.MULTILINE), (
            f"falta a parcela {parcela} em risk_scores"
        )


def test_a_parcela_c0_aceita_nulo():
    """Na C1 a C3 a parcela c0 e nula, porque a linha de base e uma configuracao.

    A coluna era NOT NULL ate 14/10/2026, o que tornava impossivel gravar
    qualquer execucao de C1 a C3 — e contradizia o comentario da propria tabela.
    O defeito apareceu ao escrever a porta de escrita, nao em execucao: nunca
    houve banco para recusar o INSERT.
    """
    bloco = SDCAC.split("CREATE TABLE risk_scores (", 1)[1].split(");", 1)[0]
    linha_do_c0 = next(
        linha for linha in bloco.splitlines() if linha.strip().startswith("c0 ")
    )

    assert "NOT NULL" not in linha_do_c0


def test_nota_sem_parcela_nenhuma_e_recusada():
    """Nulo nas cinco seria nota que ninguem calculou.

    Sem o CHECK, tornar o c0 anulavel abriria a porta para linha vazia com
    `final_raw` preenchido — numero sem decomposicao, que e exatamente o que a
    D-36 proibe.
    """
    assert "risk_scores_alguma_parcela" in SDCAC
    assert "num_nonnulls(c0, d1, d2, d3_conduct, d3_posture) >= 1" in sem_comentarios(
        SDCAC
    )


def test_alerta_e_por_evento_ou_por_janela():
    """A D-12 no schema: a D3 alarma sobre alguem num periodo, nao sobre um evento."""
    assert "alerts_alvo_definido" in SDCAC


def test_eventos_sao_particionados_por_semente():
    """D-13: descartar uma semente precisa ser instantaneo."""
    assert "PARTITION BY LIST (run_id)" in CORP
    assert "PARTITION OF events" in CORP, "falta o exemplo de criacao de particao"
    assert "DEFAULT" not in CORP.split("PARTITION BY LIST (run_id)", 1)[1].replace(
        "DEFAULT de proposito", ""
    ), "particao DEFAULT esconde carga sem particao criada"


def test_nenhum_segredo_no_sql():
    """Repositorio publico. Senha de papel se define fora daqui."""
    for sql in TODOS_OS_SQL:
        assert not re.search(r"(?i)password\s+'", sql), "senha literal no SQL"
