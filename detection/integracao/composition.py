"""A nota final, composta das dimensoes que a configuracao liga.

E aqui que a frase da Metodologia sobre "um unico codigo executado sob quatro
parametros" se cumpre ou se perde. O codigo e o mesmo nas quatro linhas da
tabela de ablacao; o que muda e quais dimensoes a configuracao liga e, por
consequencia, quais entradas ela exige.

**Pesos iguais nas quatro configuracoes.** O arquivo de presets tem um conjunto
so, e nao um por configuracao. Peso proprio por linha faria a tabela medir duas
coisas ao mesmo tempo — a dimensao acrescentada e o peso trocado —, e a
Metodologia promete ao leitor que a unica variavel e a dimensao.

**Entrada que falta e erro, nao zero.** Configuracao que liga a D2 sem padrao,
ou a D3 sem retrato de postura, para aqui com mensagem. Pontuar zero no lugar
produziria uma tabela de ablacao com numeros plausiveis e sem sentido, e
ninguem perceberia pela cara do resultado.

**As duas parcelas da D3 continuam separadas** depois da composicao: a nota
final as soma com pesos declarados, e o resultado guarda as duas em campos
proprios — como as colunas `d3_conduct` e `d3_posture` do banco. Guardar so o
total esconderia qual delas causou o alerta.
"""

from dataclasses import dataclass, field

from detection.c0 import score_c0
from detection.configuration import Configuration, ConfigurationError
from detection.d1 import score_d1
from detection.d2 import Baseline, score_d2
from detection.d3 import Posture, PriorScore, score_d3
from detection.model import Catalog, DimensionScore, Event, RiskBand, RuleHit


@dataclass(frozen=True, slots=True)
class EvaluationContext:
    """Tudo que as dimensoes podem precisar para avaliar um evento.

    O que cada configuracao exige e diferente, e a composicao reclama do que
    falta em vez de pontuar zero.

    Attributes:
        catalog: Funcionarios, dispositivos, recursos e faixas de rede.
        recent: Eventos anteriores da mesma conta, para a janela da C0 e as
            janelas da D2.
        baseline: O padrao do funcionario. Obrigatorio quando a D2 esta ligada.
        priors: Risco dos eventos anteriores, para a exposicao da D3.
        posture: Retrato do estado no dia. Obrigatorio quando a D3 esta ligada.
    """

    catalog: Catalog
    recent: tuple[Event, ...] = ()
    baseline: Baseline | None = None
    priors: tuple[PriorScore, ...] = ()
    posture: Posture | None = None


@dataclass(frozen=True, slots=True)
class RiskScore:
    """A nota de um evento, decomposta.

    Os campos espelham as colunas de `sdcac.risk_scores`. Nulo significa
    "dimensao nao avaliada nesta configuracao", e e diferente de zero, que
    significa "avaliada e sem risco".
    """

    event_id: str
    configuration: str
    config_hash: str
    c0: int | None = None
    d1: int | None = None
    d2: int | None = None
    d3_conduct: int | None = None
    d3_posture: int | None = None
    final_raw: float = 0.0
    band: RiskBand = RiskBand.NORMAL
    hits: tuple[RuleHit, ...] = field(default_factory=tuple)

    @property
    def fired(self) -> tuple[str, ...]:
        return tuple(hit.rule for hit in self.hits)


def band_of(points: float, config: Configuration) -> RiskBand:
    """A faixa de exibicao de uma nota.

    A avaliacao usa o score bruto, sem teto; a faixa existe para a tela. Faixa
    empatada no teto viraria degrau na curva precisao-revocacao da D-14.
    """
    faixas = config.parameters.get("bands", {})
    if points <= faixas.get("normal_max", 20):
        return RiskBand.NORMAL
    if points <= faixas.get("low_max", 50):
        return RiskBand.LOW
    if points <= faixas.get("medium_max", 75):
        return RiskBand.MEDIUM
    return RiskBand.HIGH


def _exige(valor, nome: str, config: Configuration, dimensao: str):
    if valor is None:
        raise ConfigurationError(
            f"a configuracao {config.name} liga {dimensao}, e o contexto nao "
            f"trouxe {nome}. Pontuar zero aqui produziria tabela de ablacao com "
            "numero plausivel e sem sentido"
        )
    return valor


def compose(
    event: Event, context: EvaluationContext, config: Configuration
) -> RiskScore:
    """Avalia um evento na configuracao dada e devolve a nota decomposta.

    Args:
        event: O evento a avaliar.
        context: As entradas das dimensoes ligadas.
        config: Um dos presets canonicos, ou uma configuracao exploratoria.

    Returns:
        A nota, com cada dimensao em campo proprio e as regras que dispararam.

    Raises:
        ConfigurationError: Se faltar entrada para uma dimensao ligada.
        ValueError: Se as janelas trouxerem evento de outra conta, evento
            posterior ao avaliado, ou retrato de postura de outro dia.
    """
    pesos = config.parameters.get("integration", {})
    achados: list[RuleHit] = []
    nota = RiskScore(
        event_id=event.event_id,
        configuration=config.name,
        config_hash=config.config_hash,
    )
    total = 0.0

    c0 = d1 = d2 = conduta = postura = None

    if config.enables("c0"):
        parcela: DimensionScore = score_c0(
            event, context.catalog, config, context.recent
        )
        c0 = parcela.points
        achados.extend(parcela.hits)
        # A C0 nao passa por peso: a nota dela e a soma dos pontos das regras
        # fixas, e e assim que o grupo de controle e definido.
        total += parcela.points

    if config.enables("d1"):
        parcela = score_d1(event, context.catalog, config)
        d1 = parcela.points
        achados.extend(parcela.hits)
        total += parcela.points * pesos.get("d1", 1.0)

    if config.enables("d2"):
        baseline = _exige(context.baseline, "o padrao do funcionario", config, "a D2")
        parcela = score_d2(event, context.recent, baseline, context.catalog, config)
        d2 = parcela.points
        achados.extend(parcela.hits)
        total += parcela.points * pesos.get("d2", 1.0)

    if config.enables("d3"):
        retrato = _exige(context.posture, "o retrato de postura", config, "a D3")
        terceira = score_d3(event, context.priors, retrato, context.catalog, config)
        conduta = terceira.conduct.points
        postura = terceira.posture.points
        achados.extend(terceira.conduct.hits)
        achados.extend(terceira.posture.hits)
        total += conduta * pesos.get("d3_conduct", 1.0)
        total += postura * pesos.get("d3_posture", 1.0)

    return RiskScore(
        event_id=nota.event_id,
        configuration=nota.configuration,
        config_hash=nota.config_hash,
        c0=c0,
        d1=d1,
        d2=d2,
        d3_conduct=conduta,
        d3_posture=postura,
        final_raw=round(total, 2),
        band=band_of(total, config),
        hits=tuple(achados),
    )
