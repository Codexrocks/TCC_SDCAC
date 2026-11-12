"""O agregado de sementes: a estatistica e as recusas que protegem a media.

O teste mais importante deste arquivo nao e o da media: e o de recusa. Agregar
sementes que nao sao comparaveis — limiares diferentes, a mesma semente contada
duas vezes — produziria um numero plausivel e errado, e **nada no resultado
final acusaria**. Foi assim que um rotulo lido errado esvaziou a tabela de
episodios na sessao 41.

O Wilcoxon e conferido contra valores que se calculam a mao, nao contra o que o
proprio codigo devolveu da primeira vez.
"""

import json
from pathlib import Path

import pytest

from evaluator.agregado import (
    AgregadoError,
    agrega,
    agrega_diretorios,
    carrega,
    postos,
    resume,
    wilcoxon,
)
from evaluator.agregado_md import escreve_markdown, num, valor_p

NIVEIS = [0.10, 0.20]


def metricas(run_id: int, fpr: dict[str, float], taxa_n: float = 0.5) -> dict:
    """Um `metricas.json` minimo, com uma FPR por configuracao."""
    return {
        "run_id": run_id,
        "limiar_de_operacao": 20.0,
        "niveis_de_revocacao": NIVEIS,
        "configuracoes": {
            nome: {
                "scoring_run_id": i + 1,
                "eventos_pontuados": 1000,
                "eventos_maliciosos": 10,
                "por_evento": {
                    "limiar": 20.0,
                    "tp": 5,
                    "fp": 50,
                    "tn": 940,
                    "fn": 5,
                    "revocacao": 0.5,
                    "precisao": 0.09,
                    "fpr": valor,
                },
                "fpr_a_revocacao_fixa": {
                    "0.10": {
                        "limiar": 30.0,
                        "fpr": valor / 2,
                        "revocacao_obtida": 0.11,
                        "alertados": 10,
                        "fracao_do_log": 0.01,
                    },
                    "0.20": {
                        "limiar": 20.0,
                        "fpr": valor,
                        "revocacao_obtida": 0.21,
                        "alertados": 20,
                        "fracao_do_log": 0.02,
                    },
                },
                "por_episodio": {
                    "L": {
                        "descricao": "longitudinal",
                        "episodios_na_janela": 12,
                        "detectados": 6,
                        "taxa": 0.5,
                        "eventos": 100,
                    },
                    "N": {
                        "descricao": "normal (benigno por construcao)",
                        "episodios_na_janela": 50,
                        "detectados": int(50 * taxa_n),
                        "taxa": taxa_n,
                        "eventos": 400,
                    },
                },
            }
            for i, (nome, valor) in enumerate(fpr.items())
        },
    }


# ---------------------------------------------------------------- estatistica
def test_postos_dao_a_media_das_posicoes_empatadas():
    """Dois empatados em primeiro ficam com 1,5 cada, nao com 1 e 2."""
    assert postos([10.0, 10.0, 30.0]) == [1.5, 1.5, 3.0]


def test_desvio_padrao_e_o_amostral():
    """Com [1, 2, 3] o desvio de n-1 e 1,0; o populacional seria 0,816."""
    r = resume([1.0, 2.0, 3.0])
    assert r.media == pytest.approx(2.0)
    assert r.desvio == pytest.approx(1.0)
    assert r.n == 3


def test_uma_semente_tem_desvio_zero_e_nao_estoura():
    assert resume([0.4]).desvio == 0.0


def test_serie_vazia_e_recusada():
    with pytest.raises(AgregadoError, match="serie vazia"):
        resume([])


def test_wilcoxon_com_todas_as_diferencas_no_mesmo_sentido():
    """Dez pares, todos na mesma direcao: o p-valor exato bilateral e 2/1024.

    E o menor p-valor que dez pares podem produzir, e confere o limite inferior
    da escala: nenhum resultado deste trabalho pode reportar menos que isso com
    dez sementes.
    """
    a = [1.0] * 10
    b = [2.0] * 10
    r = wilcoxon(a, b)
    assert r.n_efetivo == 10
    assert r.estatistica == 0.0
    assert r.p == pytest.approx(2 / 1024)


def test_wilcoxon_de_series_identicas_nao_tem_o_que_testar():
    r = wilcoxon([1.0, 2.0], [1.0, 2.0])
    assert r.n_efetivo == 0
    assert r.p == 1.0
    assert not r.conclusivo


def test_wilcoxon_descarta_o_par_empatado_e_diz_quantos_sobraram():
    """Oito empates e dois pares com diferenca: o n efetivo e 2, nao 10."""
    a = [1.0] * 8 + [1.0, 1.0]
    b = [1.0] * 8 + [2.0, 3.0]
    r = wilcoxon(a, b)
    assert r.n_efetivo == 2
    assert r.p == pytest.approx(2 / 4)


def test_wilcoxon_de_um_par_so():
    """Com um par, bilateral, o p-valor exato e 1,0 — nao da para concluir."""
    assert wilcoxon([1.0], [2.0]).p == pytest.approx(1.0)


def test_wilcoxon_e_simetrico_na_ordem_dos_argumentos():
    a = [0.1, 0.5, 0.2, 0.9, 0.3]
    b = [0.4, 0.2, 0.8, 0.1, 0.7]
    assert wilcoxon(a, b).p == pytest.approx(wilcoxon(b, a).p)


def test_wilcoxon_recusa_series_de_tamanhos_diferentes():
    with pytest.raises(AgregadoError, match="tamanhos diferentes"):
        wilcoxon([1.0, 2.0], [1.0])


def test_wilcoxon_conhecido_a_mao():
    """Caso de cinco pares com um sinal contrario, conferido na mao.

    Diferencas -1, +2, +3, +4, +5 -> postos 1, 2, 3, 4, 5. A soma dos postos
    negativos e 1, dos positivos 14, e W = 1. Sob a nula, os subconjuntos com
    min(soma, 15 - soma) <= 1 sao os de soma 0, 1, 14 e 15 — quatro em 32.
    """
    a = [1.0, 4.0, 5.0, 6.0, 7.0]
    b = [2.0, 2.0, 2.0, 2.0, 2.0]
    r = wilcoxon(a, b)
    assert r.estatistica == 1.0
    assert r.p == pytest.approx(4 / 32)


# ---------------------------------------------------------------- agregacao
def test_agrega_tira_media_por_configuracao():
    sementes = [
        metricas(1, {"C0": 0.20, "C2": 0.02}),
        metricas(2, {"C0": 0.30, "C2": 0.04}),
    ]
    saida = agrega(sementes)
    bloco = saida["fpr_a_revocacao_fixa"]["0.20"]["por_configuracao"]
    assert bloco["C0"]["media"] == pytest.approx(0.25)
    assert bloco["C2"]["media"] == pytest.approx(0.03)
    assert saida["sementes"] == 2


def test_agrega_marca_a_familia_benigna():
    """A familia N precisa sair marcada: ali detectar mais e piorar."""
    sementes = [metricas(1, {"C0": 0.2}), metricas(2, {"C0": 0.3})]
    saida = agrega(sementes)
    assert saida["familia_invertida"] == "N"
    assert saida["por_episodio"]["N"]["alerta_e_falso_positivo"] is True
    assert saida["por_episodio"]["L"]["alerta_e_falso_positivo"] is False


def test_agrega_recusa_uma_semente_so():
    with pytest.raises(AgregadoError, match="duas sementes"):
        agrega([metricas(1, {"C0": 0.2})])


def test_agrega_recusa_nomes_em_numero_diferente():
    sementes = [metricas(1, {"C0": 0.2}), metricas(2, {"C0": 0.3})]
    with pytest.raises(AgregadoError, match="nomes para"):
        agrega(sementes, ["uma"])


def test_agrega_usa_os_nomes_dados_como_procedencia():
    sementes = [metricas(1, {"C0": 0.2}), metricas(1, {"C0": 0.3})]
    saida = agrega(sementes, ["semente-7", "semente-8"])
    assert saida["nomes"] == ["semente-7", "semente-8"]


def test_agrega_ignora_configuracao_ausente():
    """Agregar C0 e C2 nao deve inventar coluna de C1 nem de C3."""
    sementes = [
        metricas(1, {"C0": 0.2, "C2": 0.02}),
        metricas(2, {"C0": 0.3, "C2": 0.04}),
    ]
    saida = agrega(sementes)
    assert saida["configuracoes"] == ["C0", "C2"]
    assert "C2 vs C0" in saida["fpr_a_revocacao_fixa"]["0.20"]["wilcoxon"]
    assert "C2 vs C1" not in saida["fpr_a_revocacao_fixa"]["0.20"]["wilcoxon"]


# ---------------------------------------------------------------- leitura
def grava(pasta: Path, nome: str, dado: dict) -> Path:
    destino = pasta / nome
    destino.mkdir(parents=True)
    (destino / "metricas.json").write_text(
        json.dumps(dado, ensure_ascii=False), encoding="utf-8"
    )
    return destino


def test_carrega_recusa_limiares_diferentes(tmp_path):
    """Media de FPR medida em limiares diferentes nao significa nada."""
    a = grava(tmp_path, "semente-1", metricas(1, {"C0": 0.2}))
    outra = metricas(2, {"C0": 0.3})
    outra["limiar_de_operacao"] = 30.0
    b = grava(tmp_path, "semente-2", outra)
    with pytest.raises(AgregadoError, match="limiares diferentes"):
        carrega([a, b])


def test_carrega_recusa_o_mesmo_diretorio_duas_vezes(tmp_path):
    """Contar a mesma semente em dobro estreita o desvio-padrao em silencio."""
    a = grava(tmp_path, "semente-1", metricas(1, {"C0": 0.2}))
    with pytest.raises(AgregadoError, match="duas vezes"):
        carrega([a, a])


def test_carrega_recusa_niveis_de_revocacao_diferentes(tmp_path):
    a = grava(tmp_path, "semente-1", metricas(1, {"C0": 0.2}))
    outra = metricas(2, {"C0": 0.3})
    outra["niveis_de_revocacao"] = [0.10]
    b = grava(tmp_path, "semente-2", outra)
    with pytest.raises(AgregadoError, match="outros niveis"):
        carrega([a, b])


def test_carrega_recusa_conjuntos_de_configuracao_diferentes(tmp_path):
    """Semente com quatro configuracoes nao se mistura com semente de duas."""
    a = grava(tmp_path, "semente-1", metricas(1, {"C0": 0.2, "C2": 0.02}))
    b = grava(tmp_path, "semente-2", metricas(2, {"C0": 0.3}))
    with pytest.raises(AgregadoError, match="avaliou"):
        carrega([a, b])


def test_carrega_recusa_diretorio_sem_metricas(tmp_path):
    a = grava(tmp_path, "semente-1", metricas(1, {"C0": 0.2}))
    vazio = tmp_path / "semente-2"
    vazio.mkdir()
    with pytest.raises(AgregadoError, match="nao existe"):
        carrega([a, vazio])


def test_carrega_ordena_semente_10_depois_da_9(tmp_path):
    """Ordem alfabetica poria a 10 antes da 2; a procedencia ficaria torta."""
    pastas = [
        grava(tmp_path, f"semente-{n}", metricas(n, {"C0": 0.2 + n / 100}))
        for n in (1, 2, 9, 10)
    ]
    nomes = [nome for nome, _ in carrega(pastas)]
    assert nomes == ["semente-1", "semente-2", "semente-9", "semente-10"]


def test_agrega_diretorios_leva_os_nomes_para_o_relatorio(tmp_path):
    pastas = [
        grava(tmp_path, f"semente-{n}", metricas(n, {"C0": 0.2 + n / 100}))
        for n in (1, 2)
    ]
    saida = agrega_diretorios(pastas)
    assert saida["nomes"] == ["semente-1", "semente-2"]


# ---------------------------------------------------------------- relatorio
def test_numero_sai_em_formato_brasileiro():
    assert num(1436275.0, 0) == "1.436.275"
    assert num(0.0488, 4) == "0,0488"


def test_p_valor_minusculo_nao_vira_zero():
    """`p = 0,0000` leria como certeza; o relatorio escreve o limite."""
    assert valor_p({"p": 1e-9, "n_efetivo": 10}, 10) == "p < 0,0001"


def test_p_valor_anota_o_n_quando_empates_derrubaram_pares():
    assert "(n=7)" in valor_p({"p": 0.0156, "n_efetivo": 7}, 10)
    assert "(n=" not in valor_p({"p": 0.0156, "n_efetivo": 10}, 10)


def test_p_valor_anota_o_n_tambem_com_mais_de_dez_sementes():
    """O corte e o numero de sementes, nao o dez fixo."""
    assert "(n=10)" in valor_p({"p": 0.02, "n_efetivo": 10}, 15)


def test_relatorio_diz_que_a_familia_benigna_se_le_ao_contrario():
    sementes = [metricas(1, {"C0": 0.2}), metricas(2, {"C0": 0.3})]
    texto = escreve_markdown(agrega(sementes, ["semente-1", "semente-2"]))
    assert "alarme sobre atividade legitima" in texto
    assert "⚠️ alarme" in texto
    assert "semente-1, semente-2" in texto


def test_relatorio_escreve_o_nivel_com_virgula():
    sementes = [metricas(1, {"C0": 0.2}), metricas(2, {"C0": 0.3})]
    texto = escreve_markdown(agrega(sementes))
    assert "| **0,20** |" in texto
    assert "| **0.20** |" not in texto
