"""O executor do experimento: os dois passos, orquestrados sobre as portas.

O que esta funcao faz e o que a Metodologia descreve: **passo 1** constroi o
padrao de cada pessoa na janela de treino; **passo 2** pontua cada evento da
janela de avaliacao, uma vez por configuracao. As duas janelas sao anteriores e
disjuntas pela **D-17**, e a assinatura exige as duas separadas justamente para
que ninguem passe a mesma por engano.

**Por que o executor nao sabe de banco nem de arquivo.** Ele recebe um objeto
que cumpre as portas de `detection.ports`. Hoje quem entra e o adaptador de
arquivo; quando o `sdcac` existir, entra o de PostgreSQL, e nada aqui muda. E o
que faz a frase do artigo sobre "um unico codigo executado sob quatro
parametros" valer tambem para a fonte de dados.

**Um laco por configuracao, e nao um laco com quatro ifs.** Cada configuracao
abre a propria execucao, com o proprio hash, e grava o proprio conjunto de
notas. Misturar as quatro num laco so economizaria uma passada pelos eventos e
tornaria impossivel reexecutar uma configuracao sozinha — que e exatamente o que
a analise de sensibilidade da **D-09** vai pedir.

**O padrao e construido uma vez.** A C2 e a C3 usam a mesma janela de treino e o
mesmo `min_active_days`; reconstruir para cada uma dobraria o passo 1 e
produziria o mesmo resultado. O padrao e gravado uma vez por execucao, porque a
tabela e por execucao — o que se evita e o recalculo, nao o registro.

**A exposicao da D3 vem do que ja foi pontuado.** `PriorScore` recebe a soma das
dimensoes de evento daquele evento — D1, ou D1 mais D2 —, acumulada ao longo do
laco. Repontuar o passado aqui seria calcular duas vezes a mesma coisa e abrir
caminho para as duas contagens divergirem.
"""

import subprocess
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from detection.configuration import Configuration
from detection.d2 import Baseline, build_baselines
from detection.d3 import PriorScore, build_posture
from detection.integracao import EvaluationContext, RiskScore, alert_for, compose

# Quantos dias de historico por pessoa o laco mantem em memoria. Precisa cobrir
# a maior janela que alguma dimensao pede: a da D3, de `window_days`. Guardar
# tudo faria o uso de memoria crescer com o tamanho do experimento.
MARGEM_DE_HISTORICO = 1


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    """O que uma configuracao produziu, para quem chamou saber sem reler nada."""

    configuration: str
    scoring_run_id: int
    config_hash: str
    scored: int
    alerts: int


def code_sha() -> str:
    """O commit em execucao, para gravar junto da execucao.

    Fora de um clone git, devolve `desconhecido` em vez de estourar: o executor
    tem de rodar num diretorio copiado, e perder a identificacao do codigo e
    pior que nao ter nenhuma — mas nao e motivo para nao rodar.
    """
    try:
        # Lista de argumentos fixa, sem shell e sem nada vindo de fora: nao ha
        # entrada do usuario neste comando. O caminho e parcial de proposito —
        # exigir o absoluto quebraria em qualquer maquina com git em outro
        # lugar, e nenhuma delas e um ambiente hostil.
        saida = subprocess.run(  # noqa: S603
            ["git", "rev-parse", "HEAD"],  # noqa: S607
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "desconhecido"
    return saida.stdout.strip() or "desconhecido"


def _janela_de_historico(config: Configuration) -> timedelta:
    dias = 1
    if config.enables("d3"):
        dias = max(dias, int(config.dimension("d3")["window_days"]))
    return timedelta(days=dias + MARGEM_DE_HISTORICO)


def run_experiment(
    storage,
    *,
    run_id: int,
    configs: Sequence[Configuration],
    training: tuple[date, date],
    evaluation: tuple[datetime, datetime],
    threshold: float,
    weights_version: str = "presets-v1",
    commit: str | None = None,
) -> tuple[ExperimentResult, ...]:
    """Roda o experimento inteiro e devolve o resumo de cada configuracao.

    Args:
        storage: Objeto que cumpre as portas de `detection.ports`.
        run_id: A semente do gerador que esta sendo pontuada.
        configs: As configuracoes a executar, normalmente as quatro canonicas.
        training: Janela de treino do passo 1, em datas locais, inclusive nas
            duas pontas.
        evaluation: Janela de avaliacao do passo 2, inclusiva no inicio e
            exclusiva no fim.
        threshold: Corte de alerta. Vai gravado junto de cada alerta, porque
            "quantos alertas a C2 levantou" depende dele.
        weights_version: Rotulo da versao dos pesos, gravado na execucao.
        commit: O commit do codigo. Lido do git quando nao vier.

    Returns:
        Um resumo por configuracao, na ordem em que foram pedidas.

    Raises:
        ValueError: Se a janela de avaliacao comecar antes do fim da janela de
            treino. Janelas que se cruzam sao a falha da D-17, e falhar aqui e
            mais barato que descobrir no resultado.
    """
    treino_inicio, treino_fim = training
    avaliacao_inicio, avaliacao_fim = evaluation

    if avaliacao_inicio.date() <= treino_fim:
        raise ValueError(
            f"a janela de avaliacao comeca em {avaliacao_inicio.date()}, dentro da "
            f"janela de treino que termina em {treino_fim}. A D-17 exige janelas "
            "disjuntas: com cruzamento, o comportamento anomalo entra na "
            "definicao do que e normal e o resultado fica bom pelo motivo errado"
        )

    sha = commit or code_sha()
    catalogo = storage.catalog(run_id)
    padroes: dict[int, Baseline] | None = None
    resumos: list[ExperimentResult] = []

    for config in configs:
        if config.enables("d2") and padroes is None:
            parametros = config.dimension("d2")
            # Le tudo o que vem antes da avaliacao e deixa o
            # `build_baselines` recortar pela janela declarada: o recorte dele e
            # por data LOCAL de cada pessoa, e um corte em UTC aqui perderia ou
            # sobraria algumas horas para quem nao esta na sede.
            eventos_de_treino = tuple(storage.events(run_id, end=avaliacao_inicio))
            padroes = build_baselines(
                eventos_de_treino,
                catalog=catalogo,
                window_start=treino_inicio,
                window_end=treino_fim,
                min_active_days=int(parametros["min_active_days"]),
            )

        scoring_run_id = storage.open_run(
            run_id=run_id,
            config_name=config.name,
            config_hash=config.config_hash,
            code_sha=sha,
            weights_version=weights_version,
            exploratory=config.exploratory,
        )

        if config.enables("d2"):
            storage.save_baselines(scoring_run_id, padroes or {})

        pontuadas, alertas = _pontua(
            storage,
            run_id=run_id,
            scoring_run_id=scoring_run_id,
            config=config,
            catalogo=catalogo,
            padroes=padroes or {},
            evaluation=evaluation,
            threshold=threshold,
        )
        storage.close_run(scoring_run_id, status="done")

        resumos.append(
            ExperimentResult(
                configuration=config.name,
                scoring_run_id=scoring_run_id,
                config_hash=config.config_hash,
                scored=pontuadas,
                alerts=alertas,
            )
        )

    return tuple(resumos)


def _conta(storage, run_id: int, employee_id: int, cache: dict) -> tuple:
    if employee_id not in cache:
        cache[employee_id] = storage.account_states(run_id, employee_id)
    return cache[employee_id]


def _equipamento(storage, run_id: int, device_id: int, day: date, cache: dict) -> tuple:
    chave = (device_id, day)
    if chave not in cache:
        cache[chave] = storage.device_states(run_id, device_id=device_id, day=day)
    return cache[chave]


def _pontua(
    storage,
    *,
    run_id: int,
    scoring_run_id: int,
    config: Configuration,
    catalogo,
    padroes: dict[int, Baseline],
    evaluation: tuple[datetime, datetime],
    threshold: float,
) -> tuple[int, int]:
    """O passo 2 de uma configuracao: percorre os eventos e grava as notas."""
    inicio, fim = evaluation
    memoria = _janela_de_historico(config)

    historico: dict[int, list] = defaultdict(list)
    anteriores: dict[int, list[PriorScore]] = defaultdict(list)
    # Estado de conta e de equipamento sao dado historico: nao mudam durante a
    # execucao. Sem o cache, o adaptador de arquivo releria o JSON uma vez por
    # evento — e o de banco faria uma consulta por evento, o que e pior.
    cache_de_conta: dict[int, tuple] = {}
    cache_de_equipamento: dict[tuple[int, date], tuple] = {}
    lote: list[RiskScore] = []
    alertas = []
    pontuadas = 0

    for evento in storage.events(run_id, start=inicio, end=fim):
        pessoa = evento.employee_id
        corte = evento.occurred_at - memoria
        historico[pessoa] = [e for e in historico[pessoa] if e.occurred_at >= corte]
        anteriores[pessoa] = [p for p in anteriores[pessoa] if p.occurred_at >= corte]
        recentes = tuple(historico[pessoa])

        postura = None
        if config.enables("d3"):
            # O dia e o LOCAL da pessoa, o mesmo que o `build_posture` vai
            # calcular. Buscar pelo dia em UTC traria o estado errado para todo
            # evento perto da meia-noite — e sempre para o mesmo lado.
            fuso = ZoneInfo(catalogo.employee(pessoa).timezone)
            dia = evento.occurred_at.astimezone(fuso).date()
            postura = build_posture(
                evento,
                account_states=_conta(storage, run_id, pessoa, cache_de_conta),
                device_states=_equipamento(
                    storage, run_id, evento.device_id, dia, cache_de_equipamento
                ),
                recent=recentes,
                catalog=catalogo,
                config=config,
            )

        nota = compose(
            evento,
            EvaluationContext(
                catalog=catalogo,
                recent=recentes,
                baseline=padroes.get(pessoa),
                priors=tuple(anteriores[pessoa]),
                posture=postura,
            ),
            config,
        )
        lote.append(nota)
        pontuadas += 1

        alerta = alert_for(nota, threshold=threshold, raised_at=evento.occurred_at)
        if alerta is not None:
            alertas.append(alerta)

        historico[pessoa].append(evento)
        if config.enables("d3"):
            anteriores[pessoa].append(
                PriorScore(
                    occurred_at=evento.occurred_at,
                    points=(nota.d1 or 0) + (nota.d2 or 0),
                )
            )

        if len(lote) >= 1000:
            storage.save_scores(scoring_run_id, lote)
            lote.clear()

    if lote:
        storage.save_scores(scoring_run_id, lote)
    if alertas:
        storage.save_alerts(scoring_run_id, alertas)

    return pontuadas, len(alertas)
