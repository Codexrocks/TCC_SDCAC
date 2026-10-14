"""Testes do executor — o experimento rodando de ponta a ponta.

E o teste que responde "o software esta operacional?". Ele le `corp/` por uma
porta, constroi os padroes, pontua os eventos nas quatro configuracoes, grava em
`sdcac/` por outra porta, e nada disso toca em banco nenhum.

Dois resultados valem mais que o resto:

- **as quatro execucoes produzem a mesma quantidade de notas**, porque e o mesmo
  codigo sob quatro parametros. Se uma pontuasse menos eventos que a outra, a
  tabela de ablacao estaria comparando amostras diferentes;
- **a mesma entrada produz a mesma nota**, duas execucoes seguidas. Sem isso, a
  secao 3.7 da Metodologia nao pode chamar o resultado de reproduzivel.
"""

from datetime import UTC, date, datetime, timedelta

import pytest
from fixtures_arquivos import (
    AVALIACAO_FIM,
    AVALIACAO_INICIO,
    JANELA_FIM,
    JANELA_INICIO,
    POR_DIA,
    escreve_corp,
    eventos_do_experimento,
    janela_de_avaliacao,
)
from fixtures_eventos import DIURNO, NOVATO, PLANTONISTA, evento

from detection.configuration import load_canonical, load_implemented
from runner import run_experiment
from storage.arquivos import ArquivoStorage

TREINO = (JANELA_INICIO, JANELA_FIM)


@pytest.fixture
def dados(tmp_path):
    escreve_corp(tmp_path)
    return ArquivoStorage(tmp_path)


def roda(storage, configs=None, **extras):
    campos = {
        "run_id": 1,
        "configs": configs if configs is not None else load_implemented(),
        "training": TREINO,
        "evaluation": janela_de_avaliacao(),
        "threshold": 20.0,
        "commit": "teste",
    }
    campos.update(extras)
    return run_experiment(storage, **campos)


# ---------------------------------------------------------------------------
# As quatro linhas, de ponta a ponta
# ---------------------------------------------------------------------------


def test_as_quatro_configuracoes_rodam_e_gravam(dados):
    resumos = roda(dados)

    assert [r.configuration for r in resumos] == ["C0", "C1", "C2", "C3"]
    assert all(r.scored > 0 for r in resumos)
    assert all(dados.load_scores(r.scoring_run_id) for r in resumos)


def test_as_quatro_pontuam_a_mesma_quantidade_de_eventos(dados):
    """Mesmo codigo, mesmos eventos. Quantidade diferente seria amostra diferente.

    Se a C3 pontuasse menos que a C0 — porque faltou retrato de postura num dia,
    por exemplo —, a tabela de ablacao compararia conjuntos distintos e a
    diferenca de FPR nao significaria nada.
    """
    resumos = roda(dados)

    assert len({r.scored for r in resumos}) == 1


def test_cada_configuracao_grava_o_proprio_hash(dados):
    resumos = roda(dados)

    hashes = {r.configuration: r.config_hash for r in resumos}

    assert len(set(hashes.values())) == 4
    for nome, hash_gravado in hashes.items():
        assert hash_gravado == load_canonical(nome).config_hash


def test_a_execucao_fica_registrada_e_fechada(dados):
    (resumo,) = roda(dados, configs=[load_canonical("C0")])

    registro = dados.run(resumo.scoring_run_id)

    assert registro["status"] == "done"
    assert registro["config_name"] == "C0"
    assert registro["code_sha"] == "teste"
    assert registro["run_id"] == 1


def test_a_mesma_entrada_produz_a_mesma_nota(dados, tmp_path):
    """Determinismo, que e o que a secao 3.7 promete ao leitor.

    Nada no caminho pode depender de ordem de dicionario, de relogio ou de
    semente de aleatoriedade — e a unica forma de saber e rodar duas vezes.
    """
    primeira = roda(dados, configs=[load_canonical("C3")])

    segundo_diretorio = tmp_path.parent / "segunda"
    escreve_corp(segundo_diretorio)
    segunda = roda(ArquivoStorage(segundo_diretorio), configs=[load_canonical("C3")])

    notas_a = dados.load_scores(primeira[0].scoring_run_id)
    notas_b = ArquivoStorage(segundo_diretorio).load_scores(segunda[0].scoring_run_id)

    assert [n.final_raw for n in notas_a] == [n.final_raw for n in notas_b]
    assert [n.hits for n in notas_a] == [n.hits for n in notas_b]


# ---------------------------------------------------------------------------
# As duas janelas, que sao a trava da D-17
# ---------------------------------------------------------------------------


def test_janela_de_avaliacao_dentro_do_treino_e_recusada(dados):
    """Cruzamento faz o anomalo entrar na definicao do que e normal.

    E o resultado fica bom pelo motivo errado, sem nenhum sinal na saida. Por
    isso o executor recusa antes de comecar, e nao avisa no fim.
    """
    inicio, fim = janela_de_avaliacao()
    dentro = (inicio.replace(year=2026, month=3, day=15), fim)

    with pytest.raises(ValueError, match="janelas disjuntas"):
        roda(dados, evaluation=dentro)


def test_so_os_eventos_da_janela_de_avaliacao_sao_pontuados(dados):
    """O passo 2 nao pontua o treino: ele seria contado como resultado.

    A conta esperada sai da propria fixture, e nao de aritmetica no teste. O
    motivo e concreto: a janela de avaliacao e declarada em UTC e o turno do
    diurno atravessa a meia-noite, entao o ultimo evento do ultimo dia cai fora.
    "Duas pessoas vezes seis eventos vezes tres dias" da 36, e o certo e 35 — a
    primeira versao deste teste errou exatamente ai.
    """
    inicio, fim = janela_de_avaliacao()
    (resumo,) = roda(dados, configs=[load_canonical("C0")])

    notas = dados.load_scores(resumo.scoring_run_id)
    na_janela = [e for e in eventos_do_experimento() if inicio <= e.occurred_at <= fim]

    assert len(notas) == len(na_janela)
    assert resumo.scored == len(notas)
    # Os prefixos do treino sao "r-" e "p-"; os da avaliacao, "a-" e "ap-".
    assert not [n for n in notas if n.event_id.startswith(("r-", "p-"))]
    # E o evento aparado e exatamente um: o ultimo do turno do diurno no ultimo
    # dia. Deixar o numero explicito e o que faz o teste reclamar se a janela
    # mudar de semantica em silencio.
    dias = (AVALIACAO_FIM - AVALIACAO_INICIO).days + 1
    assert len(na_janela) == 2 * POR_DIA * dias - 1


def test_o_padrao_e_gravado_para_quem_usa_d2(dados):
    """Padrao que so existiu em memoria nao e auditavel por ninguem."""
    resumos = roda(dados)
    por_nome = {r.configuration: r.scoring_run_id for r in resumos}

    padroes = dados.load_baselines(por_nome["C2"])

    # O novato nao tem evento nenhum na fixture, e recebe padrao de pares pela
    # D-29: carga incompleta nao pode estourar no meio da pontuacao.
    assert set(padroes) == {DIURNO, PLANTONISTA, NOVATO}
    assert padroes[NOVATO].peer_group is True
    assert padroes[PLANTONISTA].peer_group is False
    assert padroes[PLANTONISTA].window_start == JANELA_INICIO
    assert padroes[PLANTONISTA].window_end == JANELA_FIM
    assert padroes[PLANTONISTA].active_days == 30


def test_quem_nao_usa_d2_nao_grava_padrao(dados):
    """A C0 e a C1 nao olham o passado, e e isso que as define."""
    from storage.arquivos import StorageError

    (resumo,) = roda(dados, configs=[load_canonical("C1")])

    with pytest.raises(StorageError):
        dados.load_baselines(resumo.scoring_run_id)


# ---------------------------------------------------------------------------
# A nota que sai
# ---------------------------------------------------------------------------


def test_a_nota_da_c0_so_tem_a_parcela_c0(dados):
    (resumo,) = roda(dados, configs=[load_canonical("C0")])

    for nota in dados.load_scores(resumo.scoring_run_id):
        assert nota.c0 is not None
        assert (nota.d1, nota.d2, nota.d3_conduct, nota.d3_posture) == (None,) * 4


def test_a_nota_da_c3_tem_as_quatro_parcelas_de_dimensao(dados):
    (resumo,) = roda(dados, configs=[load_canonical("C3")])

    for nota in dados.load_scores(resumo.scoring_run_id):
        assert nota.c0 is None
        assert nota.d1 is not None
        assert nota.d2 is not None
        assert nota.d3_conduct is not None
        assert nota.d3_posture is not None


def test_a_madrugada_e_desvio_para_o_diurno_e_rotina_para_o_plantonista(tmp_path):
    """O exemplo do projeto, agora pelo executor inteiro.

    Mesmo horario, duas pessoas: as 3h da manha sao divergencia para quem
    trabalha de dia e rotina para quem faz plantao. A C0 nao distingue os dois —
    ela alarma igual. A D2 distingue, e e isso que a C2 acrescenta.

    Se este teste cair, a reducao de falso positivo que a pergunta de pesquisa
    alega medir deixou de acontecer no caminho completo, e nao so na funcao.
    """
    madrugada = evento(
        event_id="a-madrugada",
        employee_id=DIURNO,
        occurred_at=datetime.combine(AVALIACAO_INICIO, datetime.min.time(), tzinfo=UTC)
        + timedelta(hours=6),  # 03h00 em Sao Paulo
        session_id="madrugada",
        device_id=70,
    )
    escreve_corp(tmp_path, eventos=eventos_do_experimento() + (madrugada,))
    storage = ArquivoStorage(tmp_path)

    (resumo,) = roda(storage, configs=[load_canonical("C2")])
    notas = {n.event_id: n for n in storage.load_scores(resumo.scoring_run_id)}

    do_plantonista = [n for n in notas.values() if n.event_id.startswith("ap-")]

    assert notas["a-madrugada"].d2 > 0  # fora do padrao dele
    assert do_plantonista
    assert all(n.d2 == 0 for n in do_plantonista)  # dentro do padrao dele


def test_a_c0_nao_distingue_as_duas_madrugadas(tmp_path):
    """A contrapartida: a linha de base trata as duas iguais.

    E o que faz a comparacao C0 contra C2 significar algo. Se a C0 tambem
    distinguisse, ela teria parametro aprendido — e deixaria de ser controle.
    """
    madrugada = evento(
        event_id="a-madrugada",
        employee_id=DIURNO,
        occurred_at=datetime.combine(AVALIACAO_INICIO, datetime.min.time(), tzinfo=UTC)
        + timedelta(hours=6),
        session_id="madrugada",
        device_id=70,
    )
    escreve_corp(tmp_path, eventos=eventos_do_experimento() + (madrugada,))
    storage = ArquivoStorage(tmp_path)

    (resumo,) = roda(storage, configs=[load_canonical("C0")])
    notas = {n.event_id: n for n in storage.load_scores(resumo.scoring_run_id)}
    primeira_do_plantonista = min(
        (n for n in notas.values() if n.event_id.startswith("ap-")),
        key=lambda n: n.event_id,
    )

    assert notas["a-madrugada"].c0 == primeira_do_plantonista.c0 > 0


def test_o_alerta_guarda_o_limiar_usado(dados):
    resumos = roda(dados, threshold=10.0)
    com_alerta = [r for r in resumos if r.alerts]

    assert com_alerta, "nenhuma configuracao levantou alerta no limiar de 10"
    for resumo in com_alerta:
        for alerta in dados.load_alerts(resumo.scoring_run_id):
            assert alerta["threshold"] == 10.0
            assert alerta["event_id"] is not None


def test_limiar_mais_alto_levanta_menos_alerta(dados):
    """ "Quantos alertas a C2 levantou" depende do corte, e o corte varia (D-14)."""
    baixo = roda(dados, configs=[load_canonical("C0")], threshold=5.0)
    alto = roda(dados, configs=[load_canonical("C0")], threshold=500.0)

    assert baixo[0].alerts > alto[0].alerts == 0


# ---------------------------------------------------------------------------
# A exposicao da D3, que depende de ter pontuado antes
# ---------------------------------------------------------------------------


def test_a_exposicao_acumula_ao_longo_da_janela(dados):
    """A D3 soma o que ja foi medido, e nao repontua o passado.

    Por isso a conduta do primeiro evento de uma pessoa e sempre zero: nao ha
    nada antes dele. Se o primeiro evento ja viesse com exposicao, alguem estaria
    contando o proprio evento — que e a D-18 sendo furada.
    """
    (resumo,) = roda(dados, configs=[load_canonical("C3")])
    notas = dados.load_scores(resumo.scoring_run_id)

    primeira = notas[0]

    assert primeira.d3_conduct == 0
    assert any(n.d3_conduct and n.d3_conduct > 0 for n in notas), (
        "nenhum evento acumulou exposicao: a janela da D3 nao esta recebendo o "
        "que foi pontuado antes"
    )


def test_a_postura_entra_igual_para_quem_esta_em_ordem(dados):
    """A fixture tem equipamento em dia e MFA ligado: postura limpa, nota zero."""
    (resumo,) = roda(dados, configs=[load_canonical("C3")])

    for nota in dados.load_scores(resumo.scoring_run_id):
        assert nota.d3_posture == 0


def test_dia_sem_estado_de_equipamento_interrompe_a_execucao(dados, tmp_path):
    """Falhar e melhor que pontuar como se o equipamento estivesse em ordem.

    Carga incompleta produziria postura limpa para todo mundo, e a parcela
    inteira passaria a valer zero sem ninguem notar.
    """
    (tmp_path / "corp" / "estado-de-equipamento.json").write_text("[]", "utf-8")

    with pytest.raises(ValueError, match="nenhum estado do equipamento"):
        roda(dados, configs=[load_canonical("C3")])


def test_executar_sem_configuracao_nenhuma_nao_grava_nada(dados):
    assert roda(dados, configs=[]) == ()
    assert dados._registros() == []


def test_a_janela_de_treino_vazia_ainda_produz_padrao_de_pares(dados):
    """Carga incompleta nao pode estourar no meio da pontuacao.

    Quem nao tem historico suficiente cai no grupo de pares, pela D-29 — e isso
    aparece no resultado como limitacao declarada, nao como erro.
    """
    vazio = (date(2026, 2, 1), date(2026, 2, 1))

    resumos = roda(dados, configs=[load_canonical("C2")], training=vazio)
    padroes = dados.load_baselines(resumos[0].scoring_run_id)

    assert all(p.peer_group for p in padroes.values())


def test_o_executor_le_o_commit_do_codigo_quando_nao_recebe(dados):
    from runner import code_sha

    sha = code_sha()

    assert sha
    assert sha == "desconhecido" or len(sha) == 40


def test_a_margem_de_historico_cobre_a_janela_da_d3(dados):
    """Guarda-corpo: historico curto faria a D3 perder exposicao em silencio."""
    from runner.experiment import _janela_de_historico

    janela = _janela_de_historico(load_canonical("C3"))

    assert janela >= timedelta(days=load_canonical("C3").dimension("d3")["window_days"])
