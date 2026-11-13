"""Tudo que a aplicacao importa precisa estar declarado no `pyproject.toml`.

**O defeito que este arquivo existe para impedir**, achado em 12/11/2026 num
ambiente virtual recem-criado: `frontend/dashboard/cliente.py` importa `httpx`
para falar com a API de leitura, e o `pyproject.toml` **nao o declarava**. O CI
instala httpx por conta propria -- o `TestClient` do FastAPI depende dele --, de
modo que os testes passavam verdes enquanto quem rodasse `pip install -e .`
montava um ambiente em que a fonte "API" do painel estoura com
`ModuleNotFoundError` na primeira chamada.

E o par do `tests/test_dependencias_do_ci.py`, por outro lado: la se confere que
o CI instala o que os **testes** importam; aqui, que o `pyproject.toml` declara o
que a **aplicacao** importa. Os dois lados do mesmo buraco.

**O que fica de fora, e por que.** `scripts/` e ferramenta de quem mantem o
repositorio, nao a aplicacao: o `montar_artigo.py` importa `docx` e **trata a
ausencia dele**, dizendo o que falta em vez de estourar. `tests/` fica de fora
porque e o outro arquivo que cuida dele.
"""

import ast
import sys
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Os pacotes da aplicacao -- o que roda em producao, nao o que a mantem.
APLICACAO = (
    "backend",
    "detection",
    "evaluator",
    "frontend",
    "generator",
    "ingest",
    "runner",
    "storage",
)

# Nome na linha de dependencia -> nome no `import`. Quando diferem, e porque a
# distribuicao se chama de um jeito e o modulo de outro.
MODULO_DA_DISTRIBUICAO = {
    "pyyaml": "yaml",
    "scikit-learn": "sklearn",
    "python-docx": "docx",
    "python-dateutil": "dateutil",
    "pillow": "PIL",
}


def declaradas() -> set[str]:
    """Os modulos que o `pyproject.toml` declara, pelo nome do `import`."""
    dados = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))
    projeto = dados["project"]
    linhas = list(projeto.get("dependencies", []))
    for extra in projeto.get("optional-dependencies", {}).values():
        linhas += list(extra)

    nomes = set()
    for linha in linhas:
        # "uvicorn[standard]>=0.30" -> "uvicorn"
        nome = linha.split("[", 1)[0]
        for corte in (">=", "<=", "==", "!=", "~=", ">", "<", ";"):
            nome = nome.split(corte, 1)[0]
        nome = nome.strip().lower()
        nomes.add(MODULO_DA_DISTRIBUICAO.get(nome, nome.replace("-", "_")))
    return nomes


def locais() -> set[str]:
    """Os pacotes do proprio repositorio."""
    return {
        caminho.name
        for caminho in RAIZ.iterdir()
        if caminho.is_dir() and (caminho / "__init__.py").exists()
    } | set(APLICACAO)


def importados() -> dict[str, list[str]]:
    """Modulo de terceiro -> arquivos que o importam.

    Pega tambem o `import` escrito dentro de funcao, que e justamente a forma
    do defeito: o de `cliente.py` so acontece quando alguem escolhe a fonte
    "API", e nunca na carga do modulo.
    """
    achados: dict[str, list[str]] = {}
    de_fora = set(sys.stdlib_module_names) | locais()
    for pacote in APLICACAO:
        for arquivo in (RAIZ / pacote).rglob("*.py"):
            arvore = ast.parse(arquivo.read_text(encoding="utf-8"), str(arquivo))
            for no in ast.walk(arvore):
                if isinstance(no, ast.Import):
                    nomes = [alias.name for alias in no.names]
                elif isinstance(no, ast.ImportFrom) and no.level == 0 and no.module:
                    nomes = [no.module]
                else:
                    continue
                for nome in nomes:
                    raiz = nome.split(".", 1)[0]
                    if raiz in de_fora or raiz.startswith("_"):
                        continue
                    achados.setdefault(raiz, []).append(
                        str(arquivo.relative_to(RAIZ)).replace("\\", "/")
                    )
    return achados


def test_a_aplicacao_so_importa_o_que_o_pyproject_declara():
    """O defeito do httpx, preso.

    Se este teste cair, o `pip install -e .` passa a produzir um ambiente em
    que alguma tela ou algum programa estoura com `ModuleNotFoundError` -- e o
    CI nao avisa, porque ele instala a lista dele e nao a do projeto.
    """
    conhecidas = declaradas()
    faltando = {
        modulo: sorted(set(arquivos))
        for modulo, arquivos in importados().items()
        if modulo not in conhecidas
    }
    assert not faltando, (
        "modulo importado pela aplicacao e nao declarado em pyproject.toml: "
        + "; ".join(f"{m} ({', '.join(f)})" for m, f in sorted(faltando.items()))
    )


def test_o_httpx_do_painel_esta_declarado():
    """O caso concreto, nomeado, para o teste acima nao virar abstracao."""
    assert "httpx" in declaradas()
    assert "httpx" in importados()


def test_a_leitura_da_dependencia_tira_marcador_e_extra():
    """`uvicorn[standard]>=0.30` e `uvicorn`; `pyyaml` e `yaml`."""
    nomes = declaradas()
    assert "uvicorn" in nomes
    assert "psycopg" in nomes
    assert not any("[" in nome or ">" in nome for nome in nomes)


def test_o_que_a_aplicacao_importa_inclui_import_dentro_de_funcao():
    """O `import httpx` do `cliente.py` esta dentro de um metodo."""
    assert "frontend/dashboard/cliente.py" in importados()["httpx"]
