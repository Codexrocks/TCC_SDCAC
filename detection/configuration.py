"""Carrega a configuracao do motor e a prende ao resultado.

Duas decisoes moram aqui:

- **D-33**: os quatro presets canonicos nascem de `presets.toml`, versionado no
  git, e nao ha como obter uma configuracao canonica de outro arquivo. O que vem
  de fora nasce marcado como exploratorio.
- **D-34**: a configuracao carrega o proprio hash. Quem grava uma execucao sem
  ele nao consegue — nao por disciplina, por falta do valor.

O hash e do conteudo lido, nao do arquivo em disco: dois arquivos com a mesma
configuracao e comentarios diferentes produzem o mesmo hash, e e isso que
permite dizer "esta execucao usou a mesma configuracao daquela".
"""

import hashlib
import json
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

PRESETS = Path(__file__).resolve().parent / "presets.toml"

CONFIGURACOES_CANONICAS = ("C0", "C1", "C2", "C3")

DIMENSOES = ("c0", "d1", "d2", "d3")


class ConfigurationError(Exception):
    """Configuracao malformada, incompleta ou desconhecida."""


def _hash(dados: Mapping[str, Any]) -> str:
    """Hash estavel do conteudo, independente da ordem das chaves."""
    texto = json.dumps(dados, sort_keys=True, ensure_ascii=True, default=str)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class Configuration:
    """Uma configuracao de avaliacao, pronta para pontuar.

    Attributes:
        name: C0 a C3, ou o nome dado a uma configuracao exploratoria.
        dimensions: Quais dimensoes esta configuracao liga, em ordem.
        parameters: Os parametros de cada dimensao, somente leitura.
        config_hash: O hash do conteudo, que vai junto de toda execucao.
        exploratory: Verdadeiro quando a configuracao nao e um preset canonico.
    """

    name: str
    dimensions: tuple[str, ...]
    parameters: Mapping[str, Any]
    config_hash: str
    exploratory: bool

    def dimension(self, nome: str) -> Mapping[str, Any]:
        """Os parametros de uma dimensao.

        Raises:
            ConfigurationError: Se a dimensao nao estiver configurada.
        """
        try:
            return self.parameters[nome]
        except KeyError:
            raise ConfigurationError(
                f"a configuracao {self.name} nao tem parametros para {nome}"
            ) from None

    def enables(self, nome: str) -> bool:
        return nome in self.dimensions


def _valida(dados: Mapping[str, Any]) -> None:
    """Confere a forma do arquivo, sem exigir parametro de dimensao.

    A exigencia dos parametros e por configuracao, em `_monta`, e nao aqui: as
    quatro configuracoes convivem no mesmo arquivo, e cada uma usa so uma parte
    dele. Validar o arquivo inteiro de uma vez faria carregar a C0 falhar por
    causa de uma secao da C3 — foi o que aconteceu na primeira execucao dos
    testes, quando a D2 e a D3 ainda nao tinham parametro. Vale igual para
    arquivo exploratorio parcial, que e o caso que sobrou.
    """
    if "configurations" not in dados:
        raise ConfigurationError("falta a secao [configurations]")

    for nome, bloco in dados["configurations"].items():
        dimensoes = bloco.get("dimensions")
        if not dimensoes:
            raise ConfigurationError(f"{nome} nao declara dimensoes")
        for dimensao in dimensoes:
            if dimensao not in DIMENSOES:
                raise ConfigurationError(
                    f"{nome} liga a dimensao desconhecida {dimensao!r}"
                )


def _monta(nome: str, dados: Mapping[str, Any], *, exploratory: bool) -> Configuration:
    bloco = dados["configurations"][nome]
    dimensoes = tuple(bloco["dimensions"])

    for dimensao in dimensoes:
        if dimensao not in dados:
            raise ConfigurationError(
                f"{nome} liga {dimensao}, mas falta a secao [{dimensao}]"
            )

    # So entram no hash os parametros que esta configuracao usa de fato. Assim,
    # mexer no peso da D3 nao invalida o resultado de uma execucao da C0.
    usados = {d: dados[d] for d in dimensoes}
    usados["bands"] = dados.get("bands", {})

    # Os pesos de integracao entram no hash de quem usa ponderacao. A C0 fica
    # de fora: a nota dela e a soma dos pontos das regras fixas, sem peso, e
    # mexer num peso de integracao nao pode invalidar o registro de uma
    # execucao da linha de base que nunca leu aquele numero.
    if dimensoes != ("c0",):
        usados["integration"] = dados.get("integration", {})

    return Configuration(
        name=nome,
        dimensions=dimensoes,
        parameters=MappingProxyType(usados),
        config_hash=_hash(usados),
        exploratory=exploratory,
    )


def load_canonical(name: str) -> Configuration:
    """Carrega um dos quatro presets canonicos.

    Args:
        name: C0, C1, C2 ou C3.

    Returns:
        A configuracao, com `exploratory` falso.

    Raises:
        ConfigurationError: Se o nome nao for um dos quatro.
    """
    if name not in CONFIGURACOES_CANONICAS:
        raise ConfigurationError(
            f"{name!r} nao e preset canonico. Os canonicos sao "
            f"{', '.join(CONFIGURACOES_CANONICAS)}, e configuracao de usuario "
            "entra por load_exploratory, marcada como exploratoria (D-33)"
        )

    dados = tomllib.loads(PRESETS.read_text(encoding="utf-8"))
    _valida(dados)
    return _monta(name, dados, exploratory=False)


def load_all_canonical() -> tuple[Configuration, ...]:
    """As quatro configuracoes da ablacao, na ordem da tabela de resultados.

    Raises:
        ConfigurationError: Se alguma das quatro nao tiver parametros, com a
            mensagem dizendo qual secao falta. Falhar e o comportamento certo:
            devolver tres configuracoes caladas faria a tabela de ablacao sair
            com tres linhas e ninguem notar. Desde que a D3 entrou, as quatro
            carregam — o que esta funcao protege agora e arquivo editado.
    """
    return tuple(load_canonical(nome) for nome in CONFIGURACOES_CANONICAS)


def load_implemented() -> tuple[Configuration, ...]:
    """As configuracoes canonicas que ja tem parametro, na ordem da tabela.

    Serviu ao executor enquanto o experimento estava incompleto, e a lista
    cresceu sozinha conforme a D2 e a D3 entraram: hoje devolve as quatro.
    Continua existindo porque configuracao pode ficar sem parametro de novo —
    arquivo exploratorio parcial, ou dimensao nova declarada antes de ter peso.
    """
    prontas = []
    for nome in CONFIGURACOES_CANONICAS:
        try:
            prontas.append(load_canonical(nome))
        except ConfigurationError:
            continue
    return tuple(prontas)


def load_exploratory(caminho: Path, name: str) -> Configuration:
    """Carrega uma configuracao de fora do repositorio.

    Serve para a analise de sensibilidade da D-09 e para tentativa livre. O
    resultado nasce com `exploratory` verdadeiro e **nao vai ao artigo** — a
    coluna existe no banco para que isso seja verificavel depois, e nao
    lembrado.
    """
    dados = tomllib.loads(caminho.read_text(encoding="utf-8"))
    _valida(dados)
    if name not in dados["configurations"]:
        raise ConfigurationError(f"{caminho} nao define a configuracao {name!r}")
    return _monta(name, dados, exploratory=True)
