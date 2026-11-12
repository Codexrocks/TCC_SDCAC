"""As metricas da D-03, com numeros que se conferem a mao.

**Por que este arquivo existe.** Metrica errada nao estoura: ela sai como
numero plausivel, vai para a Secao 4 do artigo e e defendida na banca. O
primeiro defeito deste modulo foi exatamente assim — o `is_malicious` de
`episodes.csv` vem como `1`, nao como `True`, e ler so `true` fez as familias
P, B e L virarem benignas em silencio. A tabela por episodio saiu **vazia nelas
sem um erro**, e so apareceu porque alguem olhou a tabela. O ultimo teste deste
arquivo e essa regressao.

Os casos usam dez eventos e duas classes, de proposito: revocacao e FPR se
conferem no papel, e teste de metrica que precisa de outra implementacao para
ser conferido nao confere nada.
"""

import csv
import gzip
from pathlib import Path

import pytest

from evaluator.metrics import (
    EvaluatorError,
    carrega_gabarito,
    fpr_a_revocacao_fixa,
    matriz_por_evento,
    revocacao_por_episodio,
)

# ev-m1 e ev-m2 sao os maliciosos. As notas foram escolhidas para que a curva
# tenha um ponto por valor e nenhum empate entre as classes.
NOTAS = [
    ("ev-m1", 100.0),
    ("ev-b1", 90.0),
    ("ev-b2", 50.0),
    ("ev-b3", 30.0),
    ("ev-b4", 20.0),
    ("ev-m2", 10.0),
    ("ev-b5", 5.0),
    ("ev-b6", 4.0),
    ("ev-b7", 3.0),
    ("ev-b8", 2.0),
]
MALICIOSOS = {"ev-m1", "ev-m2"}

EPISODIOS = [
    # `is_malicious` como `1` e `0`: e o que o `pandas` escreve, e o que
    # derrubou a primeira versao deste modulo.
    {
        "episode_id": "0",
        "run_id": "1",
        "family": "P",
        "scenario_code": "P01",
        "employee_id": "1",
        "description": "forca bruta",
        "is_malicious": "1",
        "started_at": "2026-04-01T00:00:00Z",
        "ended_at": "2026-04-01T01:00:00Z",
        "n_events": "2",
        "catalog_version": "provisorio-v1",
    },
    {
        "episode_id": "1",
        "run_id": "1",
        "family": "N",
        "scenario_code": "N06",
        "employee_id": "2",
        "description": "janela de manutencao noturna legitima",
        "is_malicious": "0",
        "started_at": "2026-04-02T00:00:00Z",
        "ended_at": "2026-04-02T03:00:00Z",
        "n_events": "3",
        "catalog_version": "provisorio-v1",
    },
    # De outra semente: nao pode entrar na contagem desta.
    {
        "episode_id": "2",
        "run_id": "2",
        "family": "L",
        "scenario_code": "L01",
        "employee_id": "3",
        "description": "exposicao crescente",
        "is_malicious": "1",
        "started_at": "2026-04-03T00:00:00Z",
        "ended_at": "2026-04-30T00:00:00Z",
        "n_events": "40",
        "catalog_version": "provisorio-v1",
    },
]

ROTULOS = [
    {"run_id": "1", "event_id": "ev-m1", "episode_id": "0", "label": "malicious"},
    {"run_id": "1", "event_id": "ev-m2", "episode_id": "0", "label": "malicious"},
    {"run_id": "1", "event_id": "ev-b5", "episode_id": "1", "label": "benign"},
    {"run_id": "1", "event_id": "ev-b6", "episode_id": "1", "label": "benign"},
    {"run_id": "1", "event_id": "ev-b7", "episode_id": "1", "label": "benign"},
]


@pytest.fixture
def gabarito(tmp_path: Path):
    """Um `ground_truth/` minimo, no formato que o gerador escreve."""
    gt = tmp_path / "run_001" / "ground_truth"
    gt.mkdir(parents=True)
    with (gt / "episodes.csv").open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(EPISODIOS[0]))
        escritor.writeheader()
        escritor.writerows(EPISODIOS)
    with gzip.open(gt / "event_labels.csv.gz", "wt", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(ROTULOS[0]))
        escritor.writeheader()
        escritor.writerows(ROTULOS)
    return carrega_gabarito(tmp_path / "run_001", run_id=1)


def test_a_matriz_por_evento_confere_no_papel():
    """No limiar 20 alertam cinco eventos: um malicioso e quatro benignos."""
    matriz = matriz_por_evento(NOTAS, MALICIOSOS, limiar=20.0)

    assert (matriz["tp"], matriz["fp"], matriz["fn"], matriz["tn"]) == (1, 4, 1, 4)
    assert matriz["revocacao"] == pytest.approx(0.5)
    assert matriz["fpr"] == pytest.approx(4 / 8)
    assert matriz["precisao"] == pytest.approx(1 / 5)


def test_a_fpr_a_revocacao_fixa_pega_o_limiar_mais_alto_que_alcanca():
    """Meia revocacao sai com a nota mais alta: um malicioso, zero falso.

    E revocacao cheia exige descer ate 10, onde quatro benignos ja alertaram.
    """
    pontos = fpr_a_revocacao_fixa(NOTAS, MALICIOSOS, niveis=(0.50, 0.90))

    assert pontos["0.50"]["limiar"] == 100.0
    assert pontos["0.50"]["fpr"] == pytest.approx(0.0)
    assert pontos["0.90"]["limiar"] == 10.0
    assert pontos["0.90"]["fpr"] == pytest.approx(4 / 8)
    assert pontos["0.90"]["revocacao_obtida"] == pytest.approx(1.0)


def test_toda_revocacao_tem_resposta_e_a_fpr_e_que_a_qualifica():
    """Nao existe "nao alcanca": existe alcancar alertando tudo.

    Este teste comeca como o oposto — a primeira versao do avaliador devolvia
    `None` para o nivel "inalcancavel", e esse `None` nao tinha como acontecer:
    o ultimo ponto da curva alerta o log inteiro e chega a 1,0. O relatorio
    anunciava um comportamento que o codigo nao tinha.

    Quem qualifica o ponto e a FPR e a fracao do log alertada, e e por isso que
    as duas saem no relatorio.
    """
    pontos = fpr_a_revocacao_fixa(NOTAS, MALICIOSOS, niveis=(0.50, 1.00))

    assert pontos["1.00"]["revocacao_obtida"] == pytest.approx(1.0)
    assert pontos["1.00"]["alertados"] == 6
    assert pontos["1.00"]["fracao_do_log"] == pytest.approx(0.6)
    # Meia revocacao sai alertando um evento em dez: e a comparacao que tem
    # sentido, e a que o ponto de revocacao cheia nao tem.
    assert pontos["0.50"]["fracao_do_log"] == pytest.approx(0.1)


def test_malicioso_fora_da_janela_nao_desconta_da_revocacao():
    """O denominador sao os maliciosos **pontuados**, nao os do gabarito.

    Evento malicioso fora da janela de avaliacao nunca foi oferecido ao motor.
    Cobra-lo seria descontar da revocacao o que a janela da D-17 escondeu de
    proposito.
    """
    com_ausente = fpr_a_revocacao_fixa(
        NOTAS, MALICIOSOS | {"ev-ausente"}, niveis=(1.00,)
    )
    sem_ausente = fpr_a_revocacao_fixa(NOTAS, MALICIOSOS, niveis=(1.00,))

    assert com_ausente["1.00"] == sem_ausente["1.00"]


def test_janela_de_uma_classe_so_e_recusada():
    """Sem as duas classes nao existe revocacao nem FPR — e nem silencio."""
    with pytest.raises(EvaluatorError, match="sem as duas classes"):
        fpr_a_revocacao_fixa(NOTAS, maliciosos=set())


def test_o_episodio_conta_como_detectado_por_um_evento_so(gabarito):
    """A unidade da D-12, que esta aberta.

    O episodio P tem um evento de nota 100 e outro de nota 10. Por evento a
    revocacao e 0,5; por episodio e 1,0 — que e exatamente a diferenca que o
    plano avisa que existe nos cenarios longitudinais.
    """
    por_familia = revocacao_por_episodio(NOTAS, gabarito, limiar=20.0)

    assert por_familia["P"]["episodios_na_janela"] == 1
    assert por_familia["P"]["detectados"] == 1
    assert por_familia["P"]["taxa"] == pytest.approx(1.0)
    assert por_familia["P"]["eventos"] == 2


def test_a_familia_normal_conta_alarme_e_nao_acerto(gabarito):
    """Alertar um episodio `N` e falso positivo, e e para isso que ele existe.

    As tres notas do episodio benigno sao 5, 4 e 3 — nenhuma passa de 20, e por
    isso a taxa e zero. Taxa alta aqui e defeito, nao desempenho.
    """
    por_familia = revocacao_por_episodio(NOTAS, gabarito, limiar=20.0)

    assert por_familia["N"]["episodios_na_janela"] == 1
    assert por_familia["N"]["detectados"] == 0
    assert por_familia["N"]["taxa"] == pytest.approx(0.0)

    # Baixando o limiar, o episodio legitimo passa a alarmar.
    assert revocacao_por_episodio(NOTAS, gabarito, limiar=4.0)["N"]["detectados"] == 1


def test_episodio_de_outra_semente_nao_entra_na_contagem(gabarito):
    """O `run_id` filtra o gabarito, e o episodio L da semente 2 nao e desta."""
    assert 2 not in gabarito.familia_de
    por_familia = revocacao_por_episodio(NOTAS, gabarito, limiar=20.0)
    assert por_familia["L"]["episodios_na_janela"] == 0
    assert por_familia["L"]["taxa"] is None


def test_is_malicious_como_um_e_lido_como_malicioso(gabarito):
    """A regressao do primeiro defeito deste modulo.

    O `pandas` escreveu a coluna como inteiro, o avaliador leu `"1" == "true"`
    e todo episodio malicioso virou benigno. Nada estourou: as familias P, B e
    L saíram com zero episodio na janela, e a tabela parecia so vazia.
    """
    assert gabarito.maliciosos_por_episodio[0] is True
    assert gabarito.maliciosos_por_episodio[1] is False
    assert gabarito.episodios_da_familia("P", maliciosos=True) == {0}
    assert gabarito.episodios_da_familia("N", maliciosos=False) == {1}
