"""De onde o painel tira os dados, e como se troca isso.

Duas fontes cumprem o mesmo protocolo. A escolha e do painel, nao das telas:
uma tela pede `painel.evento(4, "ap-8-2-5")` e nao sabe se aquilo veio de uma
requisicao HTTP ou de um arquivo.

**`FonteHTTP`** fala com a API de leitura. E a fonte de verdade.

**`FonteExemplos`** le `backend/exemplos.json`, que guarda **respostas reais da
API** — a execucao 4, preset C3, semente 1, lida pela propria API e validada
contra o contrato por `tests/test_exemplos.py`. Com ela, o painel se escreve e
se testa **sem subir servidor nem banco**, e e para isso que aquele arquivo
existe.

> **A fonte de exemplos nao e dado de mentira.** Nenhum valor ali foi inventado.
> O que ela tem de limitado esta escrito no proprio arquivo, no campo
> `_limites`: a semente tem dois funcionarios, so eventos `FILE_ACCESS`,
> **ninguem na faixa `high`** e `/metrics` vazio. O painel precisa aguentar isso
> sem quebrar — e a tela de triagem so se prova quando o gerador de eventos da
> S6 existir.

**Por que o protocolo, e nao um `if` na tela.** O mesmo motivo de
`detection/ports.py`: quando a fonte mudar, muda aqui e em nenhuma tela. E uma
terceira fonte — um gravador de respostas para o teste de usabilidade da S11,
por exemplo — entra cumprindo isto, sem tocar no painel.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable
from urllib.parse import urlencode

RAIZ_DA_API = "/api/v1"
EXEMPLOS = Path(__file__).resolve().parents[2] / "backend" / "exemplos.json"


class SourceUnavailableError(RuntimeError):
    """A fonte nao respondeu, ou respondeu o que o painel nao sabe ler."""


@dataclass(frozen=True)
class Resposta:
    """O que uma fonte devolve: o codigo e o corpo, sem interpretacao."""

    status: int
    corpo: Any

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    def exigir(self) -> Any:
        """O corpo, ou erro se o status nao for de sucesso.

        A tela que precisa do dado chama isto; a que sabe lidar com ausencia le
        `ok` e decide. Devolver corpo de erro como se fosse dado e o que faria o
        painel mostrar grafico vazio no lugar de dizer que falhou.
        """
        if not self.ok:
            raise SourceUnavailableError(
                f"a fonte respondeu {self.status}: {str(self.corpo)[:200]}"
            )
        return self.corpo


@runtime_checkable
class FonteDoPainel(Protocol):
    """Qualquer coisa de onde o painel saiba ler uma rota da API."""

    def obter(self, rota: str) -> Resposta:
        """A resposta para uma rota, com a query string ja montada."""
        ...


class FonteExemplos:
    """As respostas gravadas em `backend/exemplos.json`."""

    def __init__(self, caminho: Path | None = None) -> None:
        self.caminho = caminho or EXEMPLOS
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        except OSError as erro:
            raise SourceUnavailableError(
                f"nao foi possivel ler {self.caminho}. Refaca com o comando do "
                "campo `_como_refazer` do proprio arquivo"
            ) from erro
        self.limites: str = dados.get("_limites", "")
        self._por_rota = {
            r["rota"]: Resposta(r["status"], r["corpo"]) for r in dados["respostas"]
        }

    @property
    def rotas(self) -> list[str]:
        """As rotas que estao gravadas, para a tela avisar o que nao tem."""
        return sorted(self._por_rota)

    def obter(self, rota: str) -> Resposta:
        """A resposta gravada para a rota, ignorando a query string.

        Paginacao e filtro nao se simulam aqui de proposito: a fonte devolve o
        que foi gravado, e tela que dependa de filtro precisa da API de pe.
        """
        gravada = self._por_rota.get(rota.split("?", 1)[0])
        if gravada is None:
            raise SourceUnavailableError(
                f"a rota {rota!r} nao esta gravada nos exemplos. As gravadas "
                f"sao: {', '.join(self.rotas)}"
            )
        return gravada


class FonteHTTP:
    """A API de leitura, por HTTP."""

    def __init__(
        self, base: str = "http://127.0.0.1:8000", *, espera: float = 5.0
    ) -> None:
        self.base = base.rstrip("/")
        self.espera = espera

    def obter(self, rota: str) -> Resposta:
        """A resposta da API para a rota."""
        import httpx

        try:
            bruta = httpx.get(f"{self.base}{rota}", timeout=self.espera)
        except httpx.HTTPError as erro:
            raise SourceUnavailableError(
                f"a API em {self.base} nao respondeu: {erro}. Suba com "
                "`uvicorn backend.main:app`, com SDCAC_DADOS apontando para os dados"
            ) from erro
        try:
            return Resposta(bruta.status_code, bruta.json())
        except ValueError:
            return Resposta(bruta.status_code, bruta.text)


def _query(**parametros: Any) -> str:
    """A query string dos parametros que nao sao `None`."""
    presentes = {c: v for c, v in parametros.items() if v is not None}
    return f"?{urlencode(presentes)}" if presentes else ""


class Painel:
    """As nove rotas do contrato, uma funcao cada.

    A tela nao monta caminho a mao: caminho montado na tela e onde a divergencia
    com o contrato aparece tarde, em producao, e nao no teste.
    """

    def __init__(self, fonte: FonteDoPainel) -> None:
        self.fonte = fonte

    def saude(self) -> Resposta:
        """`/health` — vale a pena tentar o resto?"""
        return self.fonte.obter(f"{RAIZ_DA_API}/health")

    def configuracoes(self) -> Resposta:
        """`/configurations` — os presets canonicos da ablacao."""
        return self.fonte.obter(f"{RAIZ_DA_API}/configurations")

    def execucoes(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Resposta:
        """`/runs` — as execucoes de pontuacao."""
        return self.fonte.obter(
            f"{RAIZ_DA_API}/runs{_query(limit=limit, offset=offset)}"
        )

    def execucao(self, scoring_run_id: int) -> Resposta:
        """`/runs/{id}` — uma execucao."""
        return self.fonte.obter(f"{RAIZ_DA_API}/runs/{scoring_run_id}")

    def alertas(
        self,
        scoring_run_id: int,
        *,
        band: str | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Resposta:
        """`/runs/{id}/alerts` — alertas, filtraveis por faixa e periodo."""
        filtros = _query(
            band=band, since=since, until=until, limit=limit, offset=offset
        )
        return self.fonte.obter(f"{RAIZ_DA_API}/runs/{scoring_run_id}/alerts{filtros}")

    def funcionarios(
        self,
        scoring_run_id: int,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Resposta:
        """`/runs/{id}/employees` — a nota mais recente de cada pessoa."""
        filtros = _query(limit=limit, offset=offset)
        return self.fonte.obter(
            f"{RAIZ_DA_API}/runs/{scoring_run_id}/employees{filtros}"
        )

    def funcionario(
        self,
        scoring_run_id: int,
        employee_id: int,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Resposta:
        """`/runs/{id}/employees/{id}` — o historico de uma pessoa."""
        filtros = _query(limit=limit, offset=offset)
        return self.fonte.obter(
            f"{RAIZ_DA_API}/runs/{scoring_run_id}/employees/{employee_id}{filtros}"
        )

    def evento(self, scoring_run_id: int, event_id: str) -> Resposta:
        """`/runs/{id}/events/{id}` — a nota de um evento, decomposta.

        E a rota que sustenta o aceite da S9: a decomposicao por dimensao e o
        `hits`, com o motivo em texto, saem daqui.
        """
        return self.fonte.obter(
            f"{RAIZ_DA_API}/runs/{scoring_run_id}/events/{event_id}"
        )

    def metricas(
        self,
        scoring_run_id: int,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Resposta:
        """`/runs/{id}/metrics` — o que o avaliador gravou. A API nao calcula."""
        filtros = _query(limit=limit, offset=offset)
        return self.fonte.obter(f"{RAIZ_DA_API}/runs/{scoring_run_id}/metrics{filtros}")
