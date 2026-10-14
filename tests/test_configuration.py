"""Testes da configuracao do motor.

Duas decisoes sao verificadas aqui, e as duas protegem o resultado do artigo,
nao o codigo:

- **D-33**: os quatro presets sao canonicos e somente leitura. Configuracao de
  usuario nasce marcada como exploratoria e nao vai ao artigo.
- **D-34**: a configuracao carrega o proprio hash, e o hash e do conteudo. Sem
  isso, "esta execucao usou a mesma configuracao daquela" seria afirmacao de
  memoria, e a secao 3.7 da Metodologia promete ao leitor que e registro.
"""

import tomllib
from pathlib import Path

import pytest

from detection.configuration import (
    CONFIGURACOES_CANONICAS,
    PRESETS,
    Configuration,
    ConfigurationError,
    load_all_canonical,
    load_canonical,
    load_exploratory,
    load_implemented,
)

# ---------------------------------------------------------------------------
# Presets canonicos
# ---------------------------------------------------------------------------


def test_as_quatro_configuracoes_da_ablacao_estao_declaradas():
    """As quatro existem no arquivo, e nenhuma a mais.

    A ablacao e de quatro configuracoes pela D-05 e pela D-26. A leitura e feita
    direto do arquivo, sem passar pelo carregador: o que se confere aqui e a
    declaracao, e nao se ela carrega.
    """
    declaradas = tomllib.loads(PRESETS.read_text(encoding="utf-8"))["configurations"]

    assert list(declaradas) == list(CONFIGURACOES_CANONICAS) == ["C0", "C1", "C2", "C3"]


def test_cada_configuracao_liga_as_dimensoes_da_metodologia():
    """A tabela da secao 3.3 do artigo, em codigo.

    A C1 e a D1 sozinha, e nao a C0 somada a D1: a linha de base continua
    separada pela D-26. Se alguem trocar isso, a tabela de ablacao passa a
    medir outra coisa e o artigo continua dizendo o que dizia.
    """
    declaradas = tomllib.loads(PRESETS.read_text(encoding="utf-8"))["configurations"]
    dimensoes = {nome: tuple(bloco["dimensions"]) for nome, bloco in declaradas.items()}

    assert dimensoes["C0"] == ("c0",)
    assert dimensoes["C1"] == ("d1",)
    assert dimensoes["C2"] == ("d1", "d2")
    assert dimensoes["C3"] == ("d1", "d2", "d3")


def test_as_quatro_carregam():
    """O estado declarado em teste, em vez de suposto.

    Valeu ["C0", "C1"], depois ["C0", "C1", "C2"] quando a D2 entrou, e agora as
    quatro, com a D3. Cada vez o teste falhou primeiro, e o aviso foi esse.
    Teste que acompanha o escopo sem reclamar esconde escopo.
    """
    assert [c.name for c in load_implemented()] == ["C0", "C1", "C2", "C3"]


def test_configuracao_sem_parametro_diz_qual_secao_falta(tmp_path: Path):
    """A mensagem aponta a secao, e nao so recusa.

    Os quatro presets canonicos estao completos desde que a D3 entrou, entao o
    caso agora e arquivo exploratorio parcial — que e justamente quem vai
    aparecer na analise de sensibilidade da D-09.
    """
    arquivo = tmp_path / "sem-d3.toml"
    texto = PRESETS.read_text(encoding="utf-8")
    declaradas = tomllib.loads(texto)["configurations"]
    assert "d3" in declaradas["C3"]["dimensions"]

    # As duas secoes da D3 saem de uma vez. Renomear so o cabecalho [d3]
    # nao bastaria: [d3.posture] recriaria a tabela pai sozinho, e o
    # carregador acharia que a secao existe.
    arquivo.write_text(texto.replace("[d3", "[d3_desligada"), encoding="utf-8")

    with pytest.raises(ConfigurationError, match=r"C3 liga d3, mas falta a secao"):
        load_exploratory(arquivo, "C3")


def test_carregar_as_quatro_de_uma_vez_devolve_a_tabela_inteira():
    """A tabela de ablacao sai completa, ou nao sai.

    Devolver tres configuracoes caladas faria a tabela sair com tres linhas e
    ninguem notar. Agora que as quatro tem parametro, o que este teste guarda e
    o contrario: que nenhuma sumiu.
    """
    assert [c.name for c in load_all_canonical()] == ["C0", "C1", "C2", "C3"]


def test_nenhum_preset_canonico_e_exploratorio():
    assert all(not c.exploratory for c in load_implemented())


def test_nome_fora_dos_quatro_e_recusado():
    """D-33: nao existe preset canonico fora do arquivo versionado."""
    with pytest.raises(ConfigurationError, match="nao e preset canonico"):
        load_canonical("C4")


def test_a_configuracao_e_imutavel():
    configuracao = load_canonical("C0")

    with pytest.raises(AttributeError):
        configuracao.name = "C9"

    with pytest.raises(TypeError):
        configuracao.parameters["c0"] = {}


# ---------------------------------------------------------------------------
# O hash, que prende a configuracao ao resultado
# ---------------------------------------------------------------------------


def test_o_hash_e_estavel_entre_carregamentos():
    assert load_canonical("C0").config_hash == load_canonical("C0").config_hash


def test_configuracoes_diferentes_tem_hash_diferente():
    hashes = {c.name: c.config_hash for c in load_implemented()}

    assert len(set(hashes.values())) == len(hashes)


def test_o_hash_e_do_conteudo_e_nao_do_arquivo(tmp_path: Path):
    """Comentario a mais nao muda o hash; numero a mais muda.

    E o que permite dizer que duas execucoes usaram a mesma configuracao sem
    comparar arquivo byte a byte — e o que faz o hash mudar quando alguem
    mexe num peso.
    """
    original = PRESETS.read_text(encoding="utf-8")

    so_comentario = tmp_path / "comentario.toml"
    so_comentario.write_text(
        original + "\n# comentario que nao muda nada\n", encoding="utf-8"
    )

    peso_trocado = tmp_path / "peso.toml"
    peso_trocado.write_text(
        original.replace("off_hours = 30", "off_hours = 31"), encoding="utf-8"
    )

    canonico = load_canonical("C0").config_hash

    assert load_exploratory(so_comentario, "C0").config_hash == canonico
    assert load_exploratory(peso_trocado, "C0").config_hash != canonico


def test_mexer_na_d3_nao_muda_o_hash_de_uma_execucao_da_c0(tmp_path: Path):
    """So entra no hash o que aquela configuracao usa.

    Sem isso, mexer num peso da D3 invalidaria o registro de execucoes da C0
    que nunca leram aquele numero — e a analise de sensibilidade da D-09
    obrigaria a reexecutar o experimento inteiro a cada ajuste.

    Enquanto a D3 nao tinha parametro, este teste acrescentava a secao ao
    arquivo. A secao existe agora, e o que se mexe e o valor — que e o caso
    real, e o que tambem permite conferir o outro lado: na C3 o hash muda.
    """
    arquivo = tmp_path / "outra-d3.toml"
    arquivo.write_text(
        PRESETS.read_text(encoding="utf-8").replace(
            "decay_per_day = 0.85", "decay_per_day = 0.5"
        ),
        encoding="utf-8",
    )

    assert (
        load_exploratory(arquivo, "C0").config_hash == load_canonical("C0").config_hash
    )
    assert (
        load_exploratory(arquivo, "C3").config_hash != load_canonical("C3").config_hash
    )

    assert (
        load_exploratory(arquivo, "C0").config_hash == load_canonical("C0").config_hash
    )


def test_mexer_no_peso_de_integracao_muda_o_hash_de_quem_pondera(tmp_path: Path):
    """O peso de integracao e parametro de execucao, e entra no registro.

    Trocar o peso da D2 muda a nota final da C2 e da C3. Se o hash nao mudasse,
    duas execucoes com notas diferentes ficariam gravadas como "mesma
    configuracao" — exatamente o que a D-34 existe para impedir.
    """
    arquivo = tmp_path / "peso-de-integracao.toml"
    arquivo.write_text(
        PRESETS.read_text(encoding="utf-8").replace("d2 = 1.0", "d2 = 0.5"),
        encoding="utf-8",
    )

    assert (
        load_exploratory(arquivo, "C2").config_hash != load_canonical("C2").config_hash
    )
    assert (
        load_exploratory(arquivo, "C0").config_hash == load_canonical("C0").config_hash
    )


def test_a_c0_nao_tem_peso_de_integracao():
    """A linha de base soma os pontos das regras fixas, sem ponderacao.

    Peso para a C0 seria um botao capaz de mexer no grupo de controle, e grupo
    de controle que alguem ajusta deixa de medir.
    """
    assert "integration" not in load_canonical("C0").parameters
    assert "integration" in load_canonical("C1").parameters


# ---------------------------------------------------------------------------
# Configuracao de fora
# ---------------------------------------------------------------------------


def test_configuracao_de_fora_nasce_exploratoria(tmp_path: Path):
    arquivo = tmp_path / "minha.toml"
    arquivo.write_text(PRESETS.read_text(encoding="utf-8"), encoding="utf-8")

    assert load_exploratory(arquivo, "C0").exploratory is True


def test_arquivo_sem_a_configuracao_pedida_e_recusado(tmp_path: Path):
    arquivo = tmp_path / "parcial.toml"
    dados = tomllib.loads(PRESETS.read_text(encoding="utf-8"))
    assert "C3" in dados["configurations"]

    arquivo.write_text(
        """
[configurations.C0]
dimensions = ["c0"]

[c0]
site_timezone = "America/Sao_Paulo"
business_hour_start = 6
business_hour_end = 22
points = { off_hours = 30, external_origin = 30, restricted_access = 35 }
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="nao define a configuracao 'C3'"):
        load_exploratory(arquivo, "C3")


def test_dimensao_sem_secao_de_parametros_e_recusada(tmp_path: Path):
    """Configuracao que liga uma dimensao sem configurar e erro, nao zero."""
    arquivo = tmp_path / "quebrada.toml"
    arquivo.write_text(
        """
[configurations.C0]
dimensions = ["c0", "d2"]

[c0]
site_timezone = "America/Sao_Paulo"
business_hour_start = 6
business_hour_end = 22
points = { off_hours = 30, external_origin = 30, restricted_access = 35 }
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match=r"liga d2.*falta a secao"):
        load_exploratory(arquivo, "C0")


def test_dimensao_desconhecida_e_recusada(tmp_path: Path):
    arquivo = tmp_path / "inventada.toml"
    arquivo.write_text(
        """
[configurations.C0]
dimensions = ["d9"]

[d9]
peso = 1
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="dimensao desconhecida"):
        load_exploratory(arquivo, "C0")


def test_pedir_dimensao_que_a_configuracao_nao_liga_e_erro():
    """A C0 nao tem parametro de D1. Devolver vazio esconderia o engano."""
    c0: Configuration = load_canonical("C0")

    with pytest.raises(ConfigurationError, match="nao tem parametros para d1"):
        c0.dimension("d1")
