"""O teste de contrato das portas — a especificacao executavel dos adaptadores.

Este arquivo nao testa o adaptador de arquivo. Ele testa **qualquer** objeto que
se diga adaptador: a lista `ADAPTADORES` cresce quando o de PostgreSQL existir, e
as mesmas assercoes passam a valer para ele sem uma linha nova.

E essa a resposta para "como o banco vai entrar sem quebrar nada": ele entra
cumprindo isto. Implementacao que mentir sobre ordem cronologica, sobre recorte
de janela ou sobre a exigencia do hash reprova aqui, e nao no resultado do
experimento.

**Por que o `runtime_checkable` nao basta.** `isinstance(obj, EventSource)` so
confere que o metodo existe — nao que ele devolve em ordem, nem que respeita o
recorte. As duas coisas sao o que as dimensoes dependem, e por isso cada uma tem
teste proprio aqui.
"""

from datetime import UTC, datetime, timedelta

import pytest
from fixtures_arquivos import (
    AVALIACAO_INICIO,
    escreve_corp,
    eventos_do_experimento,
)
from fixtures_eventos import DIURNO, PLANTONISTA

from detection.d2 import build_baseline
from detection.integracao import Alert, RiskScore
from detection.model import RiskBand
from detection.ports import (
    BaselineStore,
    CatalogSource,
    EventSource,
    RunRegistry,
    ScoreSink,
    StateSource,
)
from storage.arquivos import ArquivoStorage, StorageError


def de_arquivo(tmp_path):
    escreve_corp(tmp_path)
    return ArquivoStorage(tmp_path)


# Quando o adaptador de PostgreSQL existir, ele entra nesta lista e tudo abaixo
# passa a valer para ele. E o unico lugar que precisa mudar.
ADAPTADORES = [pytest.param(de_arquivo, id="arquivo")]


@pytest.fixture(params=ADAPTADORES)
def storage(request, tmp_path):
    return request.param(tmp_path)


# ---------------------------------------------------------------------------
# A forma: os metodos existem
# ---------------------------------------------------------------------------


def test_o_adaptador_cumpre_as_sete_portas(storage):
    for porta in (
        CatalogSource,
        EventSource,
        StateSource,
        RunRegistry,
        BaselineStore,
        ScoreSink,
    ):
        assert isinstance(storage, porta), f"nao cumpre {porta.__name__}"


# ---------------------------------------------------------------------------
# Entrada: catalogo
# ---------------------------------------------------------------------------


def test_o_catalogo_volta_inteiro(storage):
    catalogo = storage.catalog(1)

    assert catalogo.employee(DIURNO).timezone == "America/Sao_Paulo"
    assert catalogo.device(70).ownership.value == "corporate"
    assert catalogo.resource(3).sensitivity.value == "restricted"
    assert catalogo.range_of(__import__("ipaddress").ip_address("10.0.0.5")) is not None


def test_o_catalogo_volta_somente_leitura(storage):
    """Regra que altera o catalogo contamina a pontuacao dos eventos seguintes."""
    catalogo = storage.catalog(1)

    with pytest.raises(TypeError):
        catalogo.employees[99] = None


# ---------------------------------------------------------------------------
# Entrada: eventos — ordem e recorte, que e do que as janelas dependem
# ---------------------------------------------------------------------------


def test_os_eventos_voltam_em_ordem_cronologica(storage):
    """A promessa e do adaptador, e nao esperanca sobre o arquivo.

    A janela da C0, as duas da D2 e a da D3 dependem da ordem. Fora de ordem,
    elas produzem nota errada **sem erro nenhum** — que e o pior desfecho
    possivel.
    """
    instantes = [e.occurred_at for e in storage.events(1)]

    assert instantes == sorted(instantes)
    assert len(instantes) == len(eventos_do_experimento())


def test_o_recorte_e_inclusivo_no_inicio_e_exclusivo_no_fim(storage):
    """Janelas adjacentes nao podem contar o mesmo evento duas vezes."""
    todos = list(storage.events(1))
    meio = todos[len(todos) // 2].occurred_at

    antes = list(storage.events(1, end=meio))
    depois = list(storage.events(1, start=meio))

    assert len(antes) + len(depois) == len(todos)
    assert all(e.occurred_at < meio for e in antes)
    assert all(e.occurred_at >= meio for e in depois)


def test_o_recorte_por_funcionario_traz_so_aquela_pessoa(storage):
    de_um = list(storage.events(1, employee_id=PLANTONISTA))

    assert de_um
    assert {e.employee_id for e in de_um} == {PLANTONISTA}


def test_semente_que_nao_existe_devolve_vazio_e_nao_estoura(storage):
    """Semente descartada e caso previsto pela D-13, nao erro."""
    assert list(storage.events(999)) == []


def test_todo_evento_volta_com_fuso(storage):
    """Data sem fuso viraria hora local silenciosa, e a janela mudaria de tamanho."""
    assert all(e.occurred_at.tzinfo is not None for e in storage.events(1))


# ---------------------------------------------------------------------------
# Entrada: estado
# ---------------------------------------------------------------------------


def test_o_estado_de_conta_volta_ordenado_e_com_fim_aberto(storage):
    estados = storage.account_states(1, DIURNO)

    assert estados
    assert [e.valid_from for e in estados] == sorted(e.valid_from for e in estados)
    assert estados[-1].valid_to is None  # ainda vigente
    assert all(e.employee_id == DIURNO for e in estados)


def test_o_estado_de_equipamento_e_do_dia_pedido(storage):
    do_dia = storage.device_states(1, device_id=70, day=AVALIACAO_INICIO)

    assert len(do_dia) == 1
    assert do_dia[0].state_date == AVALIACAO_INICIO
    assert do_dia[0].device_id == 70


def test_dia_sem_estado_de_equipamento_volta_vazio(storage):
    """Vazio e a resposta honesta. Inventar "em ordem" esconderia carga faltando."""
    assert (
        storage.device_states(1, device_id=70, day=AVALIACAO_INICIO.replace(year=2020))
        == ()
    )


# ---------------------------------------------------------------------------
# Saida: o registro de execucao, que e a trava da D-34
# ---------------------------------------------------------------------------


def _abre(storage, **extras):
    campos = {
        "run_id": 1,
        "config_name": "C0",
        "config_hash": "abc123",
        "code_sha": "deadbeef",
        "weights_version": "presets-v1",
        "exploratory": False,
    }
    campos.update(extras)
    return storage.open_run(**campos)


def test_a_execucao_guarda_o_hash_da_configuracao(storage):
    scoring_run_id = _abre(storage)

    registro = storage.run(scoring_run_id)

    assert registro["config_hash"] == "abc123"
    assert registro["config_name"] == "C0"
    assert registro["code_sha"] == "deadbeef"
    assert registro["exploratory"] is False


def test_execucao_sem_hash_nao_se_grava(storage):
    """D-34: quem grava sem o hash nao consegue, por falta do valor."""
    with pytest.raises((StorageError, ValueError), match="hash"):
        _abre(storage, config_hash="")


def test_cada_execucao_recebe_identificador_proprio(storage):
    primeira = _abre(storage, config_name="C0")
    segunda = _abre(storage, config_name="C1", config_hash="def456")

    assert primeira != segunda


def test_a_execucao_fecha_com_estado(storage):
    scoring_run_id = _abre(storage)

    storage.close_run(scoring_run_id, status="done")

    assert storage.run(scoring_run_id)["status"] == "done"


def test_fechar_execucao_que_nao_existe_e_erro(storage):
    with pytest.raises((StorageError, KeyError, ValueError)):
        storage.close_run(4242, status="done")


def test_a_configuracao_exploratoria_fica_marcada(storage):
    """D-33: resultado de configuracao livre nao vai ao artigo sem aviso."""
    scoring_run_id = _abre(storage, exploratory=True, config_hash="xpl")

    assert storage.run(scoring_run_id)["exploratory"] is True


# ---------------------------------------------------------------------------
# Saida: padroes, notas e alertas
# ---------------------------------------------------------------------------


def test_o_padrao_volta_igual_ao_que_entrou(storage):
    """Padrao que muda ao passar pelo armazenamento muda a nota da D2.

    E muda em silencio: a D2 compara contra ele, e nao tem como saber que o
    numero chegou diferente.
    """
    eventos = tuple(storage.events(1, employee_id=DIURNO))
    original = build_baseline(
        DIURNO,
        eventos,
        timezone="America/Sao_Paulo",
        catalog=storage.catalog(1),
        window_start=eventos[0].occurred_at.date(),
        window_end=AVALIACAO_INICIO,
    )
    scoring_run_id = _abre(storage)

    storage.save_baselines(scoring_run_id, {DIURNO: original})
    devolvido = storage.load_baselines(scoring_run_id)[DIURNO]

    assert devolvido == original


def test_a_nota_volta_com_as_cinco_parcelas_e_os_motivos(storage):
    nota = RiskScore(
        event_id="e-1",
        configuration="C3",
        config_hash="abc123",
        c0=None,
        d1=30,
        d2=12,
        d3_conduct=5,
        d3_posture=20,
        final_raw=57.0,
        band=RiskBand.MEDIUM,
    )
    scoring_run_id = _abre(storage)

    storage.save_scores(scoring_run_id, [nota])
    (devolvida,) = storage.load_scores(scoring_run_id)

    assert devolvida == nota


def test_parcela_nula_volta_nula_e_nao_zero(storage):
    """Nulo e "nao avaliada"; zero e "avaliada e sem risco".

    Se o armazenamento trocasse nulo por zero, a tabela de ablacao de uma
    execucao da C1 ficaria indistinguivel de uma da C3 em que nada disparou.
    """
    nota = RiskScore(
        event_id="e-2",
        configuration="C1",
        config_hash="abc123",
        d1=0,
        final_raw=0.0,
        band=RiskBand.NORMAL,
    )
    scoring_run_id = _abre(storage)

    storage.save_scores(scoring_run_id, [nota])
    (devolvida,) = storage.load_scores(scoring_run_id)

    assert devolvida.d1 == 0
    assert devolvida.c0 is None
    assert devolvida.d2 is None


def test_as_notas_entram_em_lote_e_se_acumulam(storage):
    """A porta recebe iteravel porque sao milhoes, e o lote nao substitui o anterior."""
    scoring_run_id = _abre(storage)
    notas = [
        RiskScore(
            event_id=f"e-{i}",
            configuration="C0",
            config_hash="abc123",
            c0=i,
            final_raw=float(i),
            band=RiskBand.NORMAL,
        )
        for i in range(5)
    ]

    storage.save_scores(scoring_run_id, notas[:3])
    storage.save_scores(scoring_run_id, notas[3:])

    assert len(storage.load_scores(scoring_run_id)) == 5


def test_o_alerta_guarda_o_limiar_que_o_levantou(storage):
    """ "Quantos alertas a C2 levantou" e pergunta sem resposta sem o limiar."""
    scoring_run_id = _abre(storage)
    alerta = Alert(
        band=RiskBand.HIGH,
        threshold=50.0,
        raised_at=datetime(2026, 4, 1, 12, tzinfo=UTC),
        event_id="e-1",
    )

    storage.save_alerts(scoring_run_id, [alerta])
    (devolvido,) = storage.load_alerts(scoring_run_id)

    assert devolvido["threshold"] == 50.0
    assert devolvido["event_id"] == "e-1"
    assert devolvido["employee_id"] is None


def test_execucao_sem_nota_nenhuma_volta_vazia(storage):
    """Configuracao que nao pontuou nada nao pode parecer configuracao ausente."""
    scoring_run_id = _abre(storage)

    assert storage.load_scores(scoring_run_id) == ()
    assert storage.load_alerts(scoring_run_id) == ()


# ---------------------------------------------------------------------------
# O gabarito nao tem porta, e isso e verificavel
# ---------------------------------------------------------------------------


def test_nenhuma_porta_le_rotulo_de_cenario():
    """Porta de leitura de rotulo seria vazamento com nome de arquitetura.

    O `ground_truth` e lido **so** pelo avaliador, e o usuario da aplicacao nao
    tem permissao de conectar naquele banco. Se alguem acrescentar um metodo que
    leia rotulo, este teste cai.
    """
    import detection.ports as portas

    suspeitas = ("label", "ground_truth", "scenario", "rotulo", "gabarito", "injected")
    for nome in dir(portas):
        objeto = getattr(portas, nome)
        if not isinstance(objeto, type):
            continue
        for metodo in dir(objeto):
            assert not any(s in metodo.lower() for s in suspeitas), (
                f"{nome}.{metodo} parece ler o gabarito"
            )


def test_o_adaptador_de_arquivo_nao_tem_pasta_de_gabarito(tmp_path):
    """O adaptador da aplicacao nao sabe que o gabarito existe."""
    storage = de_arquivo(tmp_path)
    _abre(storage)

    assert not (tmp_path / "ground_truth").exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["corp", "sdcac"]


def test_a_escrita_nao_toca_em_corp(storage, tmp_path):
    """Quem escreve em `corp/` e o gerador. O executor so le."""
    antes = {caminho: caminho.read_bytes() for caminho in (tmp_path / "corp").iterdir()}

    scoring_run_id = _abre(storage)
    storage.save_scores(
        scoring_run_id,
        [
            RiskScore(
                event_id="e-9",
                configuration="C0",
                config_hash="abc123",
                c0=1,
                final_raw=1.0,
                band=RiskBand.NORMAL,
            )
        ],
    )

    assert {c: c.read_bytes() for c in (tmp_path / "corp").iterdir()} == antes


def test_eventos_com_margem_de_tempo_cobrem_a_janela_de_treino(storage):
    """Guarda-corpo da fixture: sem treino, o padrao sai vazio e a D2 nao mede."""
    primeiro = next(iter(storage.events(1)))
    ultimo = list(storage.events(1))[-1]

    assert (ultimo.occurred_at - primeiro.occurred_at) > timedelta(days=60)
