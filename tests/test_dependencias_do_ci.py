"""O CI tem de instalar tudo que os testes importam — ou o verde mente.

**O defeito que este arquivo impede.** `pytest.importorskip` transforma
dependencia que falta em teste **pulado**, e teste pulado nao deixa o CI
vermelho: o verde passa a afirmar o que ninguem conferiu. O comentario do
`.github/workflows/validacao.yml` diz isso com outras palavras — *"teste pulado
em silencio e pior que teste ausente"* — e o repositorio ja foi mordido por esse
formato uma vez, quando o `tzdata` faltava, o CI (Linux) passava verde e a
maquina da equipe (Windows) quebrava com `ZoneInfoNotFoundError`.

**Como ele prende.** Le a linha de `pip install` do workflow, varre `tests/` por
tudo que e importado de fora da biblioteca padrao e do proprio projeto, e falha
se algum nao estiver na lista. Inclui o que aparece em `importorskip`, que e
justamente o caso que escapa.

Este arquivo **nao** importa nada de fora da biblioteca padrao, de proposito: se
importasse, dependeria da coisa que existe para medir.
"""

import ast
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WORKFLOW = RAIZ / ".github" / "workflows" / "validacao.yml"
TESTES = RAIZ / "tests"

# Modulos do proprio projeto. Nao se instalam: estao no repositorio.
DO_PROJETO = {
    "backend",
    "detection",
    "evaluator",
    "frontend",
    "generator",
    "ingest",
    "runner",
    "scripts",
    "storage",
    "tests",
    "conftest",
}

# Nome do modulo que se importa -> nome do pacote que se instala, quando
# diferem. O resto se assume igual.
PACOTE_DE = {"yaml": "pyyaml", "docx": "python-docx", "PIL": "pillow"}

# O que cada pacote da lista traz consigo. Declarado, e nao descoberto por
# introspecao: a pergunta e se o CI *garante* o modulo, e dependencia
# transitiva de terceiro pode mudar de versao para versao sem aviso.
TRAZIDOS_POR = {
    "fastapi": {"pydantic", "starlette", "pydantic_core", "typing_extensions"},
    "httpx": {"httpcore", "h11", "idna", "certifi", "anyio", "sniffio"},
    "pytest": {"pluggy", "iniconfig", "packaging"},
    "pandas": {"numpy", "dateutil", "pytz", "tzdata"},
}


def modulos_locais() -> set[str]:
    """Modulos que vivem no repositorio e nao se instalam.

    Os auxiliares de `tests/` e os verificadores de `scripts/`, que os testes
    importam depois de ajustar o `sys.path`. Lidos do disco em vez de listados
    a mao, para que um auxiliar novo nao vire falso positivo.
    """
    locais = set(DO_PROJETO)
    for pasta in (TESTES, RAIZ / "scripts"):
        if pasta.is_dir():
            locais.update(p.stem for p in pasta.glob("*.py"))
    return locais


def pacotes_que_o_ci_instala() -> set[str]:
    """Os pacotes da linha `pip install` do workflow de validacao."""
    texto = WORKFLOW.read_text(encoding="utf-8")
    achados: set[str] = set()
    for linha in re.findall(r"pip install[^\n]*", texto):
        for palavra in linha.split():
            if palavra.startswith("-") or palavra in ("pip", "install"):
                continue
            achados.add(re.split(r"[=<>!\[]", palavra)[0].lower())
    for pacote in list(achados):
        achados.update(m.lower() for m in TRAZIDOS_POR.get(pacote, ()))
    return achados


def _raiz_do_modulo(nome: str | None) -> str | None:
    return nome.split(".")[0] if nome else None


def modulos_importados_pelos_testes() -> dict[str, set[str]]:
    """Modulo de terceiro -> arquivos de teste que o importam."""
    locais = modulos_locais()
    saida: dict[str, set[str]] = {}
    for arquivo in sorted(TESTES.glob("*.py")):
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
        nomes: set[str] = set()
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                nomes.update(_raiz_do_modulo(a.name) for a in no.names)
            elif isinstance(no, ast.ImportFrom) and no.level == 0:
                nomes.add(_raiz_do_modulo(no.module))
            elif isinstance(no, ast.Call):
                # pytest.importorskip("numpy") -- o caso que escapa ao verde
                alvo = no.func
                if (
                    isinstance(alvo, ast.Attribute)
                    and alvo.attr == "importorskip"
                    and no.args
                    and isinstance(no.args[0], ast.Constant)
                    and isinstance(no.args[0].value, str)
                ):
                    nomes.add(_raiz_do_modulo(no.args[0].value))
        for nome in nomes:
            if not nome or nome in locais or nome in sys.stdlib_module_names:
                continue
            saida.setdefault(nome, set()).add(arquivo.name)
    return saida


def test_o_workflow_declara_uma_linha_de_instalacao():
    """Sem esta ancora, o teste abaixo passaria por nao achar nada."""
    assert WORKFLOW.exists(), f"{WORKFLOW} nao existe"
    assert pacotes_que_o_ci_instala(), (
        "nenhum `pip install` encontrado no workflow de validacao: o teste "
        "seguinte ficaria vazio e passaria sem medir nada"
    )


def test_o_ci_instala_tudo_que_os_testes_importam():
    """Dependencia que falta tem de deixar o CI vermelho, nao pular o teste."""
    instalados = pacotes_que_o_ci_instala()
    faltando: dict[str, set[str]] = {}
    for modulo, arquivos in modulos_importados_pelos_testes().items():
        pacote = PACOTE_DE.get(modulo, modulo).lower()
        if pacote not in instalados:
            faltando[f"{modulo} (pacote {pacote})"] = arquivos
    assert not faltando, (
        "o CI nao instala o que estes testes importam, e por isso eles seriam "
        "PULADOS na nuvem em vez de falhar:\n"
        + "\n".join(
            f"  {m}: {', '.join(sorted(a))}" for m, a in sorted(faltando.items())
        )
        + f"\n\nAcrescente ao `pip install` de {WORKFLOW.relative_to(RAIZ)} — e "
        "lembre que esse arquivo e protegido, com espera de 24 h."
    )


def test_o_proprio_teste_nao_depende_de_terceiro():
    """Medidor que precisa do que mede nao mede nada."""
    arvore = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    de_fora = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            de_fora.update(_raiz_do_modulo(a.name) for a in no.names)
        elif isinstance(no, ast.ImportFrom) and no.level == 0:
            de_fora.add(_raiz_do_modulo(no.module))
    terceiros = {
        n
        for n in de_fora
        if n and n not in sys.stdlib_module_names and n not in modulos_locais()
    }
    assert not terceiros, f"este arquivo passou a depender de {terceiros}"
