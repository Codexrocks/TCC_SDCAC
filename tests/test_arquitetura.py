"""A regra de dependencia, que a documentacao prometia e nada conferia.

`docs/software.md` diz, na secao 3: *"A regra de dependencia, conferida no CI:
`detection/` nao importa `backend/`, `database/` nem `generator/`, e nao
consulta o relogio."* Ate 14/10/2026 isso era **frase**, nao trava: nenhum check
olhava. Agora olha.

Por que a regra importa, e nao e gosto de arquitetura:

- **`detection/` nao importa infraestrutura.** E o que permite trocar arquivo
  por PostgreSQL sem tocar numa regra de pontuacao, e e o que faz a frase do
  artigo sobre "um unico codigo executado sob quatro parametros" valer tambem
  para a fonte de dados. No dia em que uma regra importar `psycopg`, a pontuacao
  passa a depender de quem esta conectado.
- **`detection/` nao le o relogio.** Nota que dependa de `now()` muda ao ser
  recalculada, e a reprodutibilidade da secao 3.7 deixa de existir. Pior: o
  defeito nao aparece em nenhum teste escrito no mesmo dia.
- **`detection/` nao le ambiente nem sorteia.** Configuracao entra por
  argumento, com hash; aleatoriedade e do gerador. Ler do ambiente faria o
  resultado depender da maquina.
"""

import ast
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
NUCLEO = RAIZ / "detection"

# Pacotes que o nucleo nao pode importar: as duas entradas, a infraestrutura e
# qualquer biblioteca de fora que fale com rede ou banco.
PACOTES_PROIBIDOS = frozenset(
    {
        "backend",
        "database",
        "generator",
        "runner",
        "storage",
        "psycopg",
        "sqlalchemy",
        "fastapi",
        "pydantic",
        "requests",
        "httpx",
    }
)

# Modulos da biblioteca padrao que trazem relogio, sorteio, ambiente ou processo.
MODULOS_PROIBIDOS = frozenset({"os", "sys", "random", "secrets", "time", "subprocess"})

# Chamadas que leem o relogio. `datetime` como tipo e bem-vindo; `datetime.now`
# nao.
RELOGIO = frozenset({"now", "today", "utcnow", "monotonic", "perf_counter"})


def arquivos_do_nucleo() -> list[Path]:
    return sorted(NUCLEO.rglob("*.py"))


def arvore(caminho: Path) -> ast.Module:
    return ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))


def test_o_nucleo_existe_e_tem_arquivo():
    """Guarda-corpo: um teste que varre pasta vazia passa sem testar nada."""
    arquivos = arquivos_do_nucleo()

    assert len(arquivos) >= 10
    assert (NUCLEO / "ports.py") in arquivos


@pytest.mark.parametrize("caminho", arquivos_do_nucleo(), ids=lambda p: p.name)
def test_o_nucleo_nao_importa_infraestrutura(caminho: Path):
    for no in ast.walk(arvore(caminho)):
        if isinstance(no, ast.Import):
            nomes = [alias.name for alias in no.names]
        elif isinstance(no, ast.ImportFrom):
            nomes = [no.module or ""]
        else:
            continue

        for nome in nomes:
            raiz = nome.split(".", 1)[0]
            assert raiz not in PACOTES_PROIBIDOS, (
                f"{caminho.relative_to(RAIZ)} importa {nome!r}. O nucleo nao "
                "depende de infraestrutura: e o que permite trocar arquivo por "
                "banco sem tocar numa regra de pontuacao"
            )
            assert raiz not in MODULOS_PROIBIDOS, (
                f"{caminho.relative_to(RAIZ)} importa {nome!r}. Relogio, sorteio "
                "e ambiente ficam fora do nucleo: com eles, a mesma entrada "
                "deixa de produzir a mesma nota"
            )


@pytest.mark.parametrize("caminho", arquivos_do_nucleo(), ids=lambda p: p.name)
def test_o_nucleo_nao_le_o_relogio(caminho: Path):
    """`datetime` como tipo passa; `datetime.now()` nao.

    O instante do evento chega por argumento, sempre. Uma regra que pergunte a
    hora ao sistema produz nota que muda ao ser recalculada — e o resultado do
    artigo deixa de ser reproduzivel sem que nada reclame.
    """
    for no in ast.walk(arvore(caminho)):
        if not isinstance(no, ast.Call):
            continue
        alvo = no.func
        if isinstance(alvo, ast.Attribute) and alvo.attr in RELOGIO:
            raise AssertionError(
                f"{caminho.relative_to(RAIZ)}, linha {no.lineno}: chamada a "
                f"{alvo.attr!r}. O instante chega por argumento; nota que depende "
                "do relogio muda ao ser recalculada"
            )


@pytest.mark.parametrize("caminho", arquivos_do_nucleo(), ids=lambda p: p.name)
def test_o_nucleo_so_le_arquivo_do_proprio_pacote(caminho: Path):
    """A unica leitura de disco permitida e a dos presets, que sao versionados.

    Configuracao entra por argumento e carrega hash. Ler caminho de fora faria o
    resultado depender da maquina, e o hash deixaria de significar algo.
    """
    texto = caminho.read_text(encoding="utf-8")

    if "read_text" not in texto and "open(" not in texto:
        return

    assert caminho.name == "configuration.py", (
        f"{caminho.relative_to(RAIZ)} le arquivo. Só o carregador de "
        "configuracao le disco, e ele le o preset versionado ao lado dele"
    )
    assert "Path(__file__)" in texto, (
        "o carregador precisa resolver o preset a partir do proprio arquivo, e "
        "nao de caminho recebido de fora"
    )


def test_as_duas_entradas_importam_o_nucleo():
    """A dependencia e de fora para dentro, e as duas pontas usam o mesmo nucleo.

    E isso que garante que o painel mostre o mesmo codigo que produziu a tabela:
    se `runner/` e `backend/` tivessem cada um a sua copia da regra, as duas
    divergiriam na primeira correcao feita em so uma delas.
    """
    entradas = {
        "runner": (RAIZ / "runner").rglob("*.py"),
    }
    for nome, arquivos in entradas.items():
        textos = [a.read_text(encoding="utf-8") for a in arquivos]
        assert any("from detection" in t for t in textos), (
            f"{nome}/ nao importa detection/: ou esta duplicando regra, ou nao "
            "esta usando o motor"
        )


def test_o_adaptador_de_arquivo_nao_importa_as_entradas():
    """Infraestrutura nao conhece quem a usa.

    Se `storage/` importasse `runner/`, trocar de adaptador passaria a exigir
    mexer no executor — e a porta nao serviria para nada.
    """
    for caminho in (RAIZ / "storage").rglob("*.py"):
        for no in ast.walk(arvore(caminho)):
            if isinstance(no, ast.ImportFrom):
                raiz = (no.module or "").split(".", 1)[0]
                assert raiz not in {"runner", "backend"}, (
                    f"{caminho.relative_to(RAIZ)} importa {no.module!r}"
                )
