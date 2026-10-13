"""A pontuacao ponderada do evento.

Os oito atributos da **D-31**, mais as duas tabelas de peso — tipo de faixa de
rede e nivel de sigilo. A lista de atributos e a da decisao; o mapeamento de
cada um para uma condicao verificavel e o que este arquivo acrescenta, e esta
comentado caso por caso.

**Os pesos sao preliminares.** Eles vem de `presets.toml`, que declara a
origem: a versao 1 da arquitetura os tinha como ponto de partida, e a definicao
final e a decisao **D-09**, com analise de sensibilidade na S12. Nenhum numero
daqui vai ao artigo como valor justificado antes daquela analise.

Diferenca que importa em relacao a C0: o horario aqui usa o fuso do
**funcionario**. E o que faz quem encerra as 21:30 em Manaus nao ser alarmado
pela D1, enquanto a C0 o alarma por ser 22:30 no fuso da sede — o falso
positivo legitimo da **D-40**, que e o mecanismo central da pergunta de
pesquisa.
"""

from zoneinfo import ZoneInfo

from detection.configuration import Configuration, ConfigurationError
from detection.model import (
    Catalog,
    DeviceOwnership,
    DimensionScore,
    Event,
    EventType,
    RuleHit,
)

# Categorias de navegacao que contam como risco. Tudo que nao e trafego
# corporativo pode ser canal de saida de dado — nuvem e webmail sao os obvios,
# e `uncategorized` entra porque destino que o catalogo nao conhece e o pior
# caso, nao o mais inocente.
CATEGORIAS_DE_RISCO = frozenset(
    {"cloud_storage", "webmail", "uncategorized", "social_media"}
)

# Subtipos de SYSTEM_CONFIG que mexem em poder de acesso. Troca de senha nao
# entra: e higiene, e a D3 e que mede postura.
SUBTIPOS_DE_PRIVILEGIO = frozenset({"privilege_escalation", "permission_grant"})

# Destinos de download que saem do equipamento corporativo.
DESTINOS_EXTERNOS = frozenset({"external_storage", "removable"})


def _off_hours(event: Event, catalog: Catalog, parametros, pontos) -> RuleHit | None:
    """Fora do horario comercial, no fuso do FUNCIONARIO."""
    funcionario = catalog.employee(event.employee_id)
    fuso = ZoneInfo(funcionario.timezone)
    inicio = parametros.get("business_hour_start", 6)
    fim = parametros.get("business_hour_end", 22)

    local = event.occurred_at.astimezone(fuso)
    if inicio <= local.hour < fim:
        return None

    return RuleHit(
        rule="off_hours_employee",
        points=pontos["off_hours_employee"],
        reason=(
            f"evento as {local:%H:%M} no fuso de {funcionario.timezone}, "
            f"fora da janela de {inicio}h as {fim}h"
        ),
    )


def _network(event: Event, catalog: Catalog, config: Configuration) -> RuleHit | None:
    """Peso graduado por tipo de faixa: `home` nao e o mesmo que `external`.

    Raises:
        ValueError: Se o endereco nao cair em nenhuma faixa cadastrada. A D1
            precisa do tipo, e inventar um seria pontuar por suposicao.
    """
    faixa = catalog.range_of(event.ip_address)
    if faixa is None:
        raise ValueError(
            f"endereco {event.ip_address} fora de todas as faixas cadastradas: "
            "sem o tipo da faixa a D1 nao tem como ponderar a origem"
        )

    peso = config.dimension("d1")["network_kind"][faixa.kind.value]
    if not peso:
        return None

    return RuleHit(
        rule="network_kind",
        points=peso,
        reason=f"origem em faixa do tipo {faixa.kind.value} ({faixa.city})",
    )


def _sensitivity(
    event: Event, catalog: Catalog, config: Configuration
) -> RuleHit | None:
    """Peso por nivel de sigilo, e nao so o restrito como na C0."""
    if event.resource_id is None:
        return None

    recurso = catalog.resource(event.resource_id)
    peso = config.dimension("d1")["sensitivity"][recurso.sensitivity.value]
    if not peso:
        return None

    return RuleHit(
        rule="sensitivity",
        points=peso,
        reason=f"recurso {recurso.name!r} classificado como {recurso.sensitivity.value}",
    )


def _personal_device(event: Event, catalog: Catalog, pontos) -> RuleHit | None:
    """Dispositivo pessoal, que a C0 nao enxerga.

    Dispositivo pessoal existe no trafego legitimo pela **D-41**: 25 celulares
    autorizados. Se so aparecesse em cenario, viraria detector perfeito.
    """
    dispositivo = catalog.device(event.device_id)
    if dispositivo.ownership is not DeviceOwnership.PERSONAL:
        return None

    return RuleHit(
        rule="personal_device",
        points=pontos["personal_device"],
        reason=f"dispositivo {event.device_id} e pessoal",
    )


def _login_without_mfa(event: Event, pontos) -> RuleHit | None:
    if event.event_type is not EventType.LOGIN:
        return None
    if event.attributes.get("mfa_used", True):
        return None

    return RuleHit(
        rule="login_without_mfa",
        points=pontos["login_without_mfa"],
        reason="autenticacao sem segundo fator",
    )


def _privilege_change(event: Event, pontos) -> RuleHit | None:
    if event.event_type is not EventType.SYSTEM_CONFIG:
        return None
    subtipo = event.attributes.get("action_subtype")
    if subtipo not in SUBTIPOS_DE_PRIVILEGIO:
        return None

    return RuleHit(
        rule="privilege_change",
        points=pontos["privilege_change"],
        reason=f"alteracao de privilegio: {subtipo}",
    )


def _download(event: Event, config: Configuration, pontos) -> list[RuleHit]:
    """Volume e destino do download, que sao duas coisas diferentes."""
    if event.event_type is not EventType.FILE_DOWNLOAD:
        return []

    achados = []
    limite = config.dimension("d1")["thresholds"]["large_download_bytes"]
    tamanho = event.attributes.get("size_bytes", 0)
    if tamanho > limite:
        achados.append(
            RuleHit(
                rule="large_download",
                points=pontos["large_download"],
                reason=f"download de {tamanho} bytes, acima de {limite}",
            )
        )

    destino = event.attributes.get("destination")
    if destino in DESTINOS_EXTERNOS:
        achados.append(
            RuleHit(
                rule="download_to_external",
                points=pontos["download_to_external"],
                reason=f"download com destino {destino}",
            )
        )
    return achados


def _removable_device(event: Event, pontos) -> RuleHit | None:
    if event.event_type is not EventType.EXTERNAL_DEVICE:
        return None

    tipo = event.attributes.get("device_type", "dispositivo removivel")
    return RuleHit(
        rule="removable_device",
        points=pontos["removable_device"],
        reason=f"uso de {tipo}",
    )


def _risky_browsing(event: Event, pontos) -> RuleHit | None:
    if event.event_type is not EventType.WEB_BROWSING:
        return None
    categoria = event.attributes.get("category")
    if categoria not in CATEGORIAS_DE_RISCO:
        return None

    return RuleHit(
        rule="risky_browsing",
        points=pontos["risky_browsing"],
        reason=f"navegacao em categoria {categoria}",
    )


def score_d1(event: Event, catalog: Catalog, config: Configuration) -> DimensionScore:
    """Soma os pesos dos atributos do evento.

    Args:
        event: O evento a avaliar.
        catalog: Funcionarios, dispositivos, recursos e faixas de rede. Tudo
            cadastro: nenhuma consulta olha o passado do funcionario.
        config: Um preset que ligue a dimensao `d1`.

    Returns:
        A nota da D1, com as regras que a formaram.

    Raises:
        ConfigurationError: Se a configuracao nao ligar a dimensao `d1`.
        ValueError: Se a origem do evento nao cair em faixa cadastrada.
    """
    if not config.enables("d1"):
        raise ConfigurationError(f"a configuracao {config.name} nao liga a dimensao d1")

    parametros = config.dimension("d1")
    pontos = parametros["points"]

    achados: list[RuleHit | None] = [
        _off_hours(event, catalog, parametros, pontos),
        _network(event, catalog, config),
        _sensitivity(event, catalog, config),
        _personal_device(event, catalog, pontos),
        _login_without_mfa(event, pontos),
        _privilege_change(event, pontos),
        _removable_device(event, pontos),
        _risky_browsing(event, pontos),
    ]
    achados.extend(_download(event, config, pontos))

    disparadas = tuple(hit for hit in achados if hit is not None)
    return DimensionScore(
        points=sum(hit.points for hit in disparadas),
        hits=disparadas,
    )
