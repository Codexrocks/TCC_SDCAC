"""O gerador medido pelo que ele produz, e nao pelas constantes que declara.

**Por que este arquivo existe, separado do `test_gerador.py`.** Aquele mede a
aderencia do baseline a D-24 lendo `generator/config.py`, que nao importa nada —
e por isso roda no CI mesmo sem numpy. Este **executa o gerador**, e por isso
depende de numpy e pandas.

Era o unico modulo do projeto sem teste do proprio comportamento. A falta nao era
de trabalho: o CI instalava `pytest pyyaml fastapi httpx`, e um teste assim
**seria pulado em silencio** na nuvem. O `pip install` do
`.github/workflows/validacao.yml` passou a trazer numpy e pandas no mesmo Pull
Request que este arquivo, e o `test_dependencias_do_ci.py` prende as duas pontas.

**A propriedade mais importante que aqui se mede e o determinismo.** Toda a
cadeia de resultados do trabalho depende dela: os brutos das dez sementes foram
**apagados** depois de avaliados, e `results/README.md` promete que regerar
reconstroi o mesmo dado. Se a mesma semente deixar de produzir a mesma saida,
essa promessa cai e nenhum numero da Secao 4 e reproduzivel.

O `.csv.gz` e comparado **descomprimido**: o gzip grava o instante da compressao
no cabecalho, e por isso os bytes comprimidos diferem a cada execucao mesmo
quando o conteudo e identico. Comparar comprimido daria falha a cada rodada.
"""

import csv
import gzip
import hashlib
import io
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

pytest.importorskip("numpy", reason="o gerador nao roda sem numpy")
pytest.importorskip("pandas", reason="o gerador nao roda sem pandas")

RAIZ = Path(__file__).resolve().parent.parent
ESCALA = "0.02"
DIAS = "270"

# Numeros fixos do CATALOG de `generator/scenarios.py`: execucoes por semente
# vezes o numero de cenarios da familia. Nao escalam com a populacao.
EPISODIOS_FIXOS = {"P": 24, "B": 16, "L": 12}


def gera(destino: Path, semente: int) -> Path:
    """Roda o gerador num canto e devolve o `run_001`."""
    saida = subprocess.run(  # noqa: S603 -- argumentos sao constantes deste arquivo
        [
            sys.executable,
            "-m",
            "generator",
            "--seeds",
            "1",
            "--seed0",
            str(semente),
            "--scale",
            ESCALA,
            "--days",
            DIAS,
            "--out",
            str(destino),
        ],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    assert saida.returncode == 0, f"o gerador falhou:\n{saida.stdout}\n{saida.stderr}"
    assert "FALHA" not in saida.stdout, (
        f"as checagens da secao 9 do gerador reprovaram:\n{saida.stdout}"
    )
    return destino / "run_001"


def conteudo(caminho: Path) -> bytes:
    """Os bytes do arquivo, descomprimidos quando for `.gz`."""
    cru = caminho.read_bytes()
    return gzip.decompress(cru) if caminho.suffix == ".gz" else cru


def impressao(raiz: Path) -> dict[str, str]:
    """Resumo por arquivo, do conteudo e nao dos bytes comprimidos."""
    return {
        str(p.relative_to(raiz)).replace("\\", "/"): hashlib.sha256(
            conteudo(p)
        ).hexdigest()
        for p in sorted(raiz.rglob("*"))
        if p.is_file()
    }


def episodios(run: Path) -> list[dict[str, str]]:
    """As linhas de `ground_truth/episodes.csv`."""
    caminho = run / "ground_truth" / "episodes.csv"
    texto = conteudo(caminho).decode("utf-8")
    return list(csv.DictReader(io.StringIO(texto)))


@pytest.fixture(scope="module")
def duas_vezes_a_mesma_semente(tmp_path_factory):
    """A semente 3, gerada duas vezes em diretorios diferentes."""
    base = tmp_path_factory.mktemp("determinismo")
    return gera(base / "a", 3), gera(base / "b", 3)


@pytest.fixture(scope="module")
def outra_semente(tmp_path_factory):
    return gera(tmp_path_factory.mktemp("outra") / "c", 4)


# ------------------------------------------------------------- determinismo
def test_a_mesma_semente_produz_o_mesmo_conteudo(duas_vezes_a_mesma_semente):
    """A promessa de `results/README.md`: regerar reconstroi o mesmo dado.

    Os brutos das dez sementes foram apagados depois de avaliados. Sem esta
    propriedade, nenhum numero da Secao 4 e reproduzivel — e o defeito seria
    descoberto no dia em que alguem tentasse refazer a execucao.
    """
    a, b = duas_vezes_a_mesma_semente
    ia, ib = impressao(a), impressao(b)
    assert set(ia) == set(ib), "as duas execucoes gravaram arquivos diferentes"
    diferentes = [nome for nome in ia if ia[nome] != ib[nome]]
    assert not diferentes, (
        f"a mesma semente produziu conteudo diferente em {diferentes}"
    )


def test_o_gzip_muda_os_bytes_mesmo_com_conteudo_igual(duas_vezes_a_mesma_semente):
    """Prende o motivo de a comparacao ser descomprimida.

    Se um dia o gerador passar a gravar `mtime=0`, este teste falha e o de cima
    pode ser simplificado. Enquanto ele passar, comparar bytes comprimidos daria
    falha a cada rodada — e alguem concluiria que o gerador nao e deterministico.
    """
    a, b = duas_vezes_a_mesma_semente
    gz = [p for p in sorted(a.rglob("*.gz")) if p.is_file()]
    assert gz, "nenhum .csv.gz para comparar"
    cru_diferente = [
        p.name for p in gz if p.read_bytes() != (b / p.relative_to(a)).read_bytes()
    ]
    assert cru_diferente, (
        "os bytes comprimidos ficaram iguais: o gerador passou a gravar instante "
        "fixo, e a comparacao descomprimida deixou de ser necessaria"
    )


def test_semente_diferente_produz_dado_diferente(
    duas_vezes_a_mesma_semente, outra_semente
):
    """A semente tem de mudar a populacao, senao as dez execucoes seriam uma."""
    a, _ = duas_vezes_a_mesma_semente
    eventos_a = conteudo(a / "corp" / "events.csv.gz")
    eventos_c = conteudo(outra_semente / "corp" / "events.csv.gz")
    assert eventos_a != eventos_c, (
        "duas sementes diferentes produziram o mesmo log: o teste pareado da "
        "Secao 4 estaria comparando a mesma populacao dez vezes"
    )


# ---------------------------------------------------------------- catalogo
def test_as_familias_maliciosas_tem_o_numero_de_episodios_do_catalogo(
    duas_vezes_a_mesma_semente,
):
    """P, B e L nao escalam com a populacao: o CATALOG fixa quantos injetar."""
    a, _ = duas_vezes_a_mesma_semente
    por_familia = Counter(linha["family"] for linha in episodios(a))
    for familia, esperado in EPISODIOS_FIXOS.items():
        assert por_familia[familia] == esperado, (
            f"familia {familia}: {por_familia[familia]} episodios, "
            f"e o CATALOG declara {esperado}"
        )


def test_o_n06_existe_e_vem_da_rotina_normal(duas_vezes_a_mesma_semente):
    """O N06 nao esta no CATALOG, e por isso ler so `scenarios.py` o perde.

    Em 10/11/2026 um insumo afirmou que o codigo "nunca teve um N06". Ele esta em
    `generator/normal.py`, porque e atividade legitima e pertence a rotina, nao a
    injecao de cenarios. Este teste existe para que a afirmacao nao se repita.
    """
    a, _ = duas_vezes_a_mesma_semente
    codigos = Counter(linha["scenario_code"] for linha in episodios(a))
    n06 = [c for c in codigos if c.startswith("N06")]
    assert n06, f"nenhum episodio N06 no gabarito; codigos vistos: {sorted(codigos)}"
    assert sum(codigos[c] for c in n06) > 0


def test_a_familia_n_e_benigna_por_construcao(duas_vezes_a_mesma_semente):
    """Alertar um `N` e falso positivo, e e a razao de a familia existir.

    Se um episodio da familia N chegasse marcado como malicioso, a tabela de
    episodios da Secao 4.1 passaria a contar acerto onde conta erro — e o numero
    sairia plausivel.
    """
    a, _ = duas_vezes_a_mesma_semente
    maliciosos = {
        linha["scenario_code"]
        for linha in episodios(a)
        if linha["family"] == "N"
        and linha["is_malicious"] not in ("0", "false", "False")
    }
    assert not maliciosos, (
        f"episodios da familia N marcados como maliciosos: {maliciosos}"
    )


def test_as_familias_maliciosas_estao_marcadas_como_maliciosas(
    duas_vezes_a_mesma_semente,
):
    """O espelho do teste acima: P, B e L contam como positivo."""
    a, _ = duas_vezes_a_mesma_semente
    benignos = {
        linha["scenario_code"]
        for linha in episodios(a)
        if linha["family"] in EPISODIOS_FIXOS
        and linha["is_malicious"] in ("0", "false", "False")
    }
    assert not benignos, f"episodios maliciosos marcados como benignos: {benignos}"


def test_todo_episodio_registra_a_versao_do_catalogo(duas_vezes_a_mesma_semente):
    """A Secao 3.4 do artigo promete isso, e dela depende a objecao de desenho."""
    a, _ = duas_vezes_a_mesma_semente
    sem_versao = [
        linha["episode_id"]
        for linha in episodios(a)
        if not (linha.get("catalog_version") or "").strip()
    ]
    assert not sem_versao, f"{len(sem_versao)} episodios sem catalog_version"


# ------------------------------------------------------------------- D-17
def test_o_log_corporativo_nao_carrega_rotulo(duas_vezes_a_mesma_semente):
    """A D-17: `corp/` e o que a aplicacao ve, e o gabarito mora separado.

    Rotulo vazado para `corp/` seria vazamento de gabarito: o motor poderia
    pontuar usando a resposta, e a Secao 4 mediria o proprio gabarito.
    """
    a, _ = duas_vezes_a_mesma_semente
    proibidos = {"is_malicious", "family", "scenario_code", "episode_id", "label"}
    for arquivo in sorted((a / "corp").iterdir()):
        cabecalho = conteudo(arquivo).decode("utf-8").split("\n", 1)[0]
        colunas = {c.strip().strip('"') for c in cabecalho.split(",")}
        vazadas = colunas & proibidos
        assert not vazadas, f"{arquivo.name} carrega coluna de gabarito: {vazadas}"
