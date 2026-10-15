"""Adaptador de arquivo: cumpre todas as portas sem banco nenhum.

Um diretorio por experimento. Dentro dele:

```text
corp/
  catalogo.json           funcionarios, dispositivos, recursos, faixas
  eventos.jsonl           um evento por linha, em ordem cronologica
  estado-de-conta.json    account_state
  estado-de-equipamento.json  device_state_daily
sdcac/
  execucoes.json          scoring_runs
  padroes/<id>.json       baselines por execucao
  notas/<id>.jsonl        risk_scores por execucao
  alertas/<id>.json       alerts por execucao
```

A separacao em `corp/` e `sdcac/` nao e enfeite: ela espelha os bancos, e
nenhuma funcao deste arquivo escreve em `corp/`. **Tambem nao existe `ground_truth/`
aqui** — o gabarito e do avaliador, e o adaptador da aplicacao nao tem por que
saber que ele existe.

**A ordem cronologica e promessa do adaptador.** `events()` ordena antes de
devolver, em vez de confiar que o arquivo chegou ordenado: a C0, a D2 e a D3
dependem de janela, e janela fora de ordem produz nota errada sem erro nenhum.
"""

import json
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import asdict
from datetime import date, datetime
from ipaddress import ip_address, ip_network
from pathlib import Path

from detection.d2 import Baseline, Spread
from detection.integracao import Alert, RiskScore
from detection.model import (
    AccountState,
    Catalog,
    Device,
    DeviceKind,
    DeviceOwnership,
    DeviceState,
    Employee,
    Event,
    EventResult,
    EventType,
    NetworkKind,
    NetworkRange,
    Persona,
    Privilege,
    Resource,
    ResourceKind,
    RiskBand,
    RuleHit,
    Sensitivity,
)


class StorageError(Exception):
    """Arquivo ausente, malformado ou incoerente com o que a porta promete."""


def _le_json(caminho: Path) -> object:
    if not caminho.exists():
        raise StorageError(
            f"{caminho} nao existe. O adaptador de arquivo nao inventa dado "
            "ausente: pontuar sobre catalogo vazio produziria nota plausivel e "
            "sem sentido"
        )
    return json.loads(caminho.read_text(encoding="utf-8"))


def _grava_json(caminho: Path, dados: object) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Serializacao
# ---------------------------------------------------------------------------


def evento_de_dicionario(linha: Mapping[str, object]) -> Event:
    """Um evento a partir de uma linha do JSONL.

    Raises:
        StorageError: Se o instante vier sem fuso. O `Event` ja recusa, mas a
            mensagem dele nao diz de que arquivo veio.
    """
    try:
        instante = datetime.fromisoformat(str(linha["occurred_at"]))
    except (KeyError, ValueError) as erro:
        raise StorageError(f"evento sem occurred_at utilizavel: {linha}") from erro

    if instante.tzinfo is None:
        raise StorageError(
            f"evento {linha.get('event_id')!r} tem occurred_at sem fuso. Data sem "
            "fuso no arquivo viraria hora local silenciosa, e a janela da C0 "
            "mudaria de tamanho conforme a maquina"
        )

    return Event(
        run_id=int(linha["run_id"]),
        event_id=str(linha["event_id"]),
        employee_id=int(linha["employee_id"]),
        occurred_at=instante,
        event_type=EventType(linha["event_type"]),
        result=EventResult(linha["result"]),
        ip_address=ip_address(str(linha["ip_address"])),
        device_id=int(linha["device_id"]),
        session_id=str(linha["session_id"]),
        is_vpn=bool(linha["is_vpn"]),
        resource_id=(
            int(linha["resource_id"]) if linha.get("resource_id") is not None else None
        ),
        attributes=dict(linha.get("attributes") or {}),
    )


def evento_para_dicionario(event: Event) -> dict[str, object]:
    dados = asdict(event)
    dados["occurred_at"] = event.occurred_at.isoformat()
    dados["ip_address"] = str(event.ip_address)
    dados["event_type"] = event.event_type.value
    dados["result"] = event.result.value
    return dados


def _padrao_para_dicionario(base: Baseline) -> dict[str, object]:
    return {
        "employee_id": base.employee_id,
        "window_start": base.window_start.isoformat(),
        "window_end": base.window_end.isoformat(),
        "active_days": base.active_days,
        "peer_group": base.peer_group,
        "daily_volume": {
            "median": base.daily_volume.median,
            "mad": base.daily_volume.mad,
        },
        "daily_failures": {
            "median": base.daily_failures.median,
            "mad": base.daily_failures.mad,
        },
        "hour_share": list(base.hour_share),
        "resources": sorted(base.resources),
        "ranges": sorted(base.ranges),
        "devices": sorted(base.devices),
        "sensitive_share": base.sensitive_share,
    }


def _padrao_de_dicionario(dados: Mapping[str, object]) -> Baseline:
    return Baseline(
        employee_id=int(dados["employee_id"]),
        window_start=date.fromisoformat(str(dados["window_start"])),
        window_end=date.fromisoformat(str(dados["window_end"])),
        active_days=int(dados["active_days"]),
        peer_group=bool(dados["peer_group"]),
        daily_volume=Spread(**dados["daily_volume"]),
        daily_failures=Spread(**dados["daily_failures"]),
        hour_share=tuple(float(h) for h in dados["hour_share"]),
        resources=frozenset(int(r) for r in dados["resources"]),
        ranges=frozenset(int(r) for r in dados["ranges"]),
        devices=frozenset(int(d) for d in dados["devices"]),
        sensitive_share=float(dados["sensitive_share"]),
    )


def _nota_para_dicionario(nota: RiskScore) -> dict[str, object]:
    return {
        "event_id": nota.event_id,
        "configuration": nota.configuration,
        "config_hash": nota.config_hash,
        "c0": nota.c0,
        "d1": nota.d1,
        "d2": nota.d2,
        "d3_conduct": nota.d3_conduct,
        "d3_posture": nota.d3_posture,
        "final_raw": nota.final_raw,
        "band": nota.band.value,
        "hits": [
            {"rule": h.rule, "points": h.points, "reason": h.reason} for h in nota.hits
        ],
    }


def _nota_de_dicionario(dados: Mapping[str, object]) -> RiskScore:
    return RiskScore(
        event_id=str(dados["event_id"]),
        configuration=str(dados["configuration"]),
        config_hash=str(dados["config_hash"]),
        c0=dados.get("c0"),
        d1=dados.get("d1"),
        d2=dados.get("d2"),
        d3_conduct=dados.get("d3_conduct"),
        d3_posture=dados.get("d3_posture"),
        final_raw=float(dados["final_raw"]),
        band=RiskBand(dados["band"]),
        hits=tuple(
            RuleHit(rule=h["rule"], points=h["points"], reason=h["reason"])
            for h in dados.get("hits", [])
        ),
    )


# ---------------------------------------------------------------------------
# O adaptador
# ---------------------------------------------------------------------------


class ArquivoStorage:
    """Cumpre as sete portas de `detection.ports` contra um diretorio.

    Uma classe so, e nao sete: separar em sete objetos faria o executor receber
    sete argumentos que sempre apontam para o mesmo lugar. Quem quiser trocar
    uma porta de implementacao passa outro objeto em uma, e a assinatura
    continua a mesma — e o teste de contrato confere que as duas combinam.
    """

    def __init__(self, raiz: Path | str) -> None:
        self.raiz = Path(raiz)

    # ------------------------------------------------------------ entradas

    def catalog(self, run_id: int) -> Catalog:
        dados = _le_json(self.raiz / "corp" / "catalogo.json")
        if not isinstance(dados, dict):
            raise StorageError("catalogo.json nao e um objeto JSON")

        funcionarios = {
            int(f["employee_id"]): Employee(
                employee_id=int(f["employee_id"]),
                department_id=int(f["department_id"]),
                site_id=int(f["site_id"]),
                persona=Persona(f["persona"]),
                privilege=Privilege(f["privilege"]),
                timezone=str(f["timezone"]),
            )
            for f in dados.get("employees", [])
        }
        dispositivos = {
            int(d["device_id"]): Device(
                device_id=int(d["device_id"]),
                employee_id=int(d["employee_id"]),
                kind=DeviceKind(d["kind"]),
                ownership=DeviceOwnership(d["ownership"]),
            )
            for d in dados.get("devices", [])
        }
        recursos = {
            int(r["resource_id"]): Resource(
                resource_id=int(r["resource_id"]),
                kind=ResourceKind(r["kind"]),
                name=str(r["name"]),
                sensitivity=Sensitivity(r["sensitivity"]),
                owner_department_id=r.get("owner_department_id"),
            )
            for r in dados.get("resources", [])
        }
        faixas = tuple(
            NetworkRange(
                range_id=int(f["range_id"]),
                cidr=ip_network(str(f["cidr"])),
                kind=NetworkKind(f["kind"]),
                country=str(f["country"]),
                city=str(f["city"]),
            )
            for f in dados.get("ranges", [])
        )

        if not funcionarios:
            raise StorageError(
                "catalogo.json nao tem funcionario nenhum. Catalogo vazio faria "
                "toda regra que consulta cadastro estourar no meio da pontuacao"
            )

        return Catalog(
            employees=funcionarios,
            resources=recursos,
            ranges=faixas,
            devices=dispositivos,
        )

    def events(
        self,
        run_id: int,
        *,
        start: datetime | None = None,
        end: datetime | None = None,
        employee_id: int | None = None,
    ) -> Iterator[Event]:
        caminho = self.raiz / "corp" / "eventos.jsonl"
        if not caminho.exists():
            raise StorageError(f"{caminho} nao existe")

        eventos: list[Event] = []
        for numero, linha in enumerate(
            caminho.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not linha.strip():
                continue
            try:
                eventos.append(evento_de_dicionario(json.loads(linha)))
            except (json.JSONDecodeError, StorageError, KeyError, ValueError) as erro:
                raise StorageError(f"{caminho}, linha {numero}: {erro}") from erro

        # A ordem e promessa da porta, e nao esperanca sobre o arquivo.
        eventos.sort(key=lambda e: (e.occurred_at, e.event_id))

        for evento in eventos:
            if evento.run_id != run_id:
                continue
            if employee_id is not None and evento.employee_id != employee_id:
                continue
            if start is not None and evento.occurred_at < start:
                continue
            if end is not None and evento.occurred_at >= end:
                continue
            yield evento

    def account_states(self, run_id: int, employee_id: int) -> tuple[AccountState, ...]:
        dados = _le_json(self.raiz / "corp" / "estado-de-conta.json")
        estados = []
        for linha in dados:  # type: ignore[union-attr]
            if int(linha["run_id"]) != run_id:
                continue
            if int(linha["employee_id"]) != employee_id:
                continue
            fim = linha.get("valid_to")
            estados.append(
                AccountState(
                    employee_id=int(linha["employee_id"]),
                    valid_from=datetime.fromisoformat(str(linha["valid_from"])),
                    mfa_enabled=bool(linha["mfa_enabled"]),
                    privilege=Privilege(linha["privilege"]),
                    valid_to=datetime.fromisoformat(str(fim)) if fim else None,
                )
            )
        return tuple(sorted(estados, key=lambda e: e.valid_from))

    def device_states(
        self, run_id: int, *, device_id: int, day: date
    ) -> tuple[DeviceState, ...]:
        dados = _le_json(self.raiz / "corp" / "estado-de-equipamento.json")
        return tuple(
            DeviceState(
                device_id=int(linha["device_id"]),
                state_date=date.fromisoformat(str(linha["state_date"])),
                patch_age_days=int(linha["patch_age_days"]),
                antivirus_on=bool(linha["antivirus_on"]),
            )
            for linha in dados  # type: ignore[union-attr]
            if int(linha["run_id"]) == run_id
            and int(linha["device_id"]) == device_id
            and date.fromisoformat(str(linha["state_date"])) == day
        )

    # -------------------------------------------------------------- saidas

    @property
    def _execucoes(self) -> Path:
        return self.raiz / "sdcac" / "execucoes.json"

    def _registros(self) -> list[dict]:
        """As execucoes gravadas, ou lista vazia se nenhuma foi aberta ainda.

        Arquivo ausente e estado valido — ninguem abriu execucao. O que nao e
        valido e perguntar por uma execucao que nao existe, e isso cada chamada
        trata por conta.
        """
        if not self._execucoes.exists():
            return []
        return json.loads(self._execucoes.read_text(encoding="utf-8"))

    def open_run(
        self,
        *,
        run_id: int,
        config_name: str,
        config_hash: str,
        code_sha: str,
        weights_version: str,
        exploratory: bool,
    ) -> int:
        if not config_hash:
            raise StorageError(
                "execucao sem hash de configuracao nao se grava (D-34): sem ele, "
                '"esta execucao usou a mesma configuracao daquela" seria '
                "afirmacao de memoria"
            )

        registros = self._registros()
        scoring_run_id = max((r["scoring_run_id"] for r in registros), default=0) + 1
        registros.append(
            {
                "scoring_run_id": scoring_run_id,
                "run_id": run_id,
                "config": config_name,
                "config_name": config_name,
                "config_hash": config_hash,
                "code_sha": code_sha,
                "weights_version": weights_version,
                "exploratory": exploratory,
                "status": "running",
            }
        )
        _grava_json(self._execucoes, registros)
        return scoring_run_id

    def close_run(self, scoring_run_id: int, *, status: str) -> None:
        registros = self._registros()
        for registro in registros:
            if registro["scoring_run_id"] == scoring_run_id:
                registro["status"] = status
                break
        else:
            raise StorageError(f"execucao {scoring_run_id} nao existe")
        _grava_json(self._execucoes, registros)

    def run(self, scoring_run_id: int) -> Mapping[str, object]:
        registros = self._registros()
        for registro in registros:
            if registro["scoring_run_id"] == scoring_run_id:
                return registro
        raise StorageError(f"execucao {scoring_run_id} nao existe")

    def save_baselines(
        self, scoring_run_id: int, baselines: Mapping[int, Baseline]
    ) -> None:
        _grava_json(
            self.raiz / "sdcac" / "padroes" / f"{scoring_run_id}.json",
            [_padrao_para_dicionario(b) for b in baselines.values()],
        )

    def load_baselines(self, scoring_run_id: int) -> dict[int, Baseline]:
        dados = _le_json(self.raiz / "sdcac" / "padroes" / f"{scoring_run_id}.json")
        padroes = [_padrao_de_dicionario(d) for d in dados]  # type: ignore[union-attr]
        return {b.employee_id: b for b in padroes}

    def save_scores(self, scoring_run_id: int, scores: Iterable[RiskScore]) -> None:
        caminho = self.raiz / "sdcac" / "notas" / f"{scoring_run_id}.jsonl"
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with caminho.open("a", encoding="utf-8") as arquivo:
            for nota in scores:
                arquivo.write(
                    json.dumps(_nota_para_dicionario(nota), ensure_ascii=False) + "\n"
                )

    def load_scores(self, scoring_run_id: int) -> tuple[RiskScore, ...]:
        caminho = self.raiz / "sdcac" / "notas" / f"{scoring_run_id}.jsonl"
        if not caminho.exists():
            return ()
        return tuple(
            _nota_de_dicionario(json.loads(linha))
            for linha in caminho.read_text(encoding="utf-8").splitlines()
            if linha.strip()
        )

    def save_alerts(self, scoring_run_id: int, alerts: Iterable[Alert]) -> None:
        caminho = self.raiz / "sdcac" / "alertas" / f"{scoring_run_id}.json"
        existentes = (
            json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else []
        )
        for alerta in alerts:
            existentes.append(
                {
                    "band": alerta.band.value
                    if isinstance(alerta.band, RiskBand)
                    else alerta.band,
                    "threshold": alerta.threshold,
                    "raised_at": alerta.raised_at.isoformat(),
                    "event_id": alerta.event_id,
                    "employee_id": alerta.employee_id,
                    "window_start": alerta.window_start.isoformat()
                    if alerta.window_start
                    else None,
                    "window_end": alerta.window_end.isoformat()
                    if alerta.window_end
                    else None,
                }
            )
        _grava_json(caminho, existentes)

    def load_alerts(self, scoring_run_id: int) -> tuple[Mapping[str, object], ...]:
        caminho = self.raiz / "sdcac" / "alertas" / f"{scoring_run_id}.json"
        if not caminho.exists():
            return ()
        return tuple(json.loads(caminho.read_text(encoding="utf-8")))
