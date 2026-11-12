"""Converte o CSV do gerador para o formato do adaptador de arquivo.

O gerador escreve nove CSVs em `corp/` e dois em `ground_truth/`. O adaptador
de `storage/arquivos.py` le outra coisa:

```text
corp/catalogo.json              funcionarios, dispositivos, recursos, faixas
corp/eventos.jsonl              um evento por linha
corp/estado-de-conta.json       account_state
corp/estado-de-equipamento.json device_state_daily
```

Este modulo e a traducao, e **nada aqui inventa dado**: cada campo sai de uma
coluna do CSV ou de uma correspondencia declarada abaixo. Onde os dois lados
nao concordam, a correspondencia esta nomeada numa constante no topo do
arquivo, em vez de escondida no meio de um laco — e tres delas precisam de
ratificacao, nao de leitura.

**O que a traducao expos.** O gerador e os motores usam **vocabularios
diferentes para as mesmas seis personas**: o gerador escreve `day_admin` onde o
`detection.model.Persona` espera `office_daytime`, `shift_ops` onde ele espera
`shift`, e assim por diante. Isso nao e detalhe de formato — as personas sao as
decisoes **D-37** e **D-38**, e duas listas divergentes para a mesma decisao e
defeito de integracao. A correspondencia esta em `PERSONAS` e **pende de
ratificacao**; enquanto isso ela e o que faz o dado gerado chegar aos motores.

**Streaming nos eventos, e so neles.** `eventos.jsonl` sai linha por linha, sem
carregar o CSV inteiro: em escala cheia sao 1,9 milhao de eventos. As tabelas de
apoio tem milhares de linhas e cabem na memoria sem cerimonia.
"""

import csv
import gzip
import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# As correspondencias declaradas
# --------------------------------------------------------------------------

# As seis personas, nos dois vocabularios. O da esquerda e o que o gerador
# escreve (`generator.config.COHORTS`); o da direita e o `detection.model
# .Persona`. **Pende de ratificacao do Davi** — ver o cabecalho deste arquivo.
PERSONAS = {
    "day_admin": "office_daytime",
    "shift_ops": "shift",
    "it_privileged": "it_privileged",
    "sales_traveler": "sales_travel",
    "hybrid_eng": "hybrid",
    "management": "management",
}

# O fuso, que e o segundo desencontro de vocabulario — e o mais grave dos dois.
# O gerador escreve **deslocamento fixo** (`UTC-3`); os motores chamam
# `ZoneInfo(funcionario.timezone)` em sete lugares e precisam de **chave IANA**
# (`America/Sao_Paulo`), que e a convencao do proprio `presets.toml`. Sem esta
# correspondencia a pontuacao estoura no primeiro evento, com
# `ZoneInfoNotFoundError: UTC-3` — foi assim que o desencontro apareceu.
#
# **Por que a conversao e licita aqui.** Deslocamento fixo so equivale a fuso
# quando o fuso nao tem horario de verao, e nenhum dos dois tem: o Brasil
# extinguiu o horario de verao em 2019. As duas chaves abaixo sao as dos dois
# sitios do gerador — `SP` (UTC-3) e `MAO` (UTC-4) de `generator.config.TZ`. Se
# o gerador ganhar um terceiro sitio, a ingestao recusa em vez de adivinhar.
#
# Isso vale as decisoes **D-31** e **D-40**, e **pende de ratificacao do Davi**.
FUSOS = {
    "UTC-3": "America/Sao_Paulo",
    "UTC-4": "America/Manaus",
}

# O gerador escreve `device_type` e um booleano `corporate`; o modelo separa
# **o que o equipamento e** de **de quem ele e**. Os dois telefones viram o
# mesmo `mobile`, e a posse e que os distingue.
EQUIPAMENTOS = {
    "notebook": "notebook",
    "corporate_phone": "mobile",
    "personal_phone": "mobile",
    # O sentinela `device_id = 0` do gerador, que aparece nos eventos de origem
    # externa — 236 em 194 mil, na execucao piloto. Nao tem dono nem estado
    # diario, e por isso entra com `employee_id = 0`: nao existe funcionario 0,
    # e a regra que consulta o dono precisa falhar visivelmente em vez de
    # atribuir o equipamento do atacante a alguem do cadastro.
    "unknown_external": "notebook",
}

# `privilege_level` de `account_state.csv` → `detection.model.Privilege`. A
# escala do gerador e 0, 1, 2; a do modelo e nominal.
PRIVILEGIOS = {0: "standard", 1: "elevated", 2: "admin"}

# O prefixo `fs_` de `generator.config.SYSTEMS` marca compartilhamento de
# arquivo; o resto e sistema. E a unica informacao que o CSV carrega sobre a
# natureza do recurso.
PREFIXO_COMPARTILHAMENTO = "fs_"

SENTINELA_SEM_DONO = 0


class IngestError(Exception):
    """Erro de ingestao, com o arquivo e a coluna que faltaram."""


@dataclass
class Mapeamento:
    """Os identificadores inteiros que a traducao precisou criar.

    O CSV traz departamento e sitio como texto (`admin_finance`, `vila_sede`);
    o modelo pede inteiro. Os numeros saem da **ordem alfabetica** do que
    aparece no CSV, e nao da ordem de leitura: ordem de leitura mudaria o
    `department_id` de uma pessoa quando o gerador trocasse a ordem das
    coortes, e dois experimentos deixariam de ser comparaveis sem que nada
    acusasse.

    O mapa e gravado junto do catalogo, em `mapeamento.json`, porque numero sem
    o nome de onde veio nao se audita.
    """

    departamentos: dict[str, int] = field(default_factory=dict)
    sitios: dict[str, int] = field(default_factory=dict)

    def como_dicionario(self) -> dict[str, dict[str, int]]:
        return {"departamentos": self.departamentos, "sitios": self.sitios}


def _abre(caminho: Path) -> Iterator[dict[str, str]]:
    """Le um CSV, comprimido ou nao, como sequencia de dicionarios."""
    if not caminho.exists():
        alternativa = caminho.with_suffix(caminho.suffix + ".gz")
        if alternativa.exists():
            caminho = alternativa
        else:
            raise IngestError(f"{caminho} nao existe")

    abrir = gzip.open if caminho.suffix == ".gz" else open
    with abrir(caminho, "rt", newline="", encoding="utf-8") as arquivo:
        yield from csv.DictReader(arquivo)


def _inteiro(texto: str | None) -> int | None:
    """Um inteiro a partir de celula que pode vir vazia ou como float.

    O `pandas` escreve `1.0` numa coluna de inteiros que tenha um vazio — e
    `devices.csv` tem, por causa do sentinela sem dono.
    """
    if texto is None or texto == "":
        return None
    return int(float(texto))


def _booleano(texto: str | None) -> bool:
    """Um booleano a partir do que o `pandas` escreve: `True` ou `False`."""
    return str(texto).strip().lower() in {"true", "1", "yes"}


def _enumera(valores: set[str]) -> dict[str, int]:
    return {nome: i for i, nome in enumerate(sorted(valores), start=1)}


def _catalogo(origem: Path, mapa: Mapeamento) -> dict[str, list[dict]]:
    """Monta o `catalogo.json` a partir das quatro tabelas de cadastro."""
    funcionarios_csv = list(_abre(origem / "employees.csv"))
    if not funcionarios_csv:
        raise IngestError("employees.csv esta vazio")

    mapa.departamentos = _enumera({f["department"] for f in funcionarios_csv})
    mapa.sitios = _enumera({f["site"] for f in funcionarios_csv})

    # O privilegio inicial sai da primeira linha de `account_state`, e nao do
    # booleano `privileged` de `employees.csv`: o booleano nao distingue
    # `elevated` de `admin`, e a C0 trata os dois de forma diferente.
    privilegio_inicial: dict[int, int] = {}
    for linha in _abre(origem / "account_state.csv"):
        emp = int(linha["employee_id"])
        if emp not in privilegio_inicial:
            privilegio_inicial[emp] = int(linha["privilege_level"])

    funcionarios = []
    for f in funcionarios_csv:
        emp = int(f["employee_id"])
        persona = f["persona"]
        if persona not in PERSONAS:
            raise IngestError(
                f"funcionario {emp} tem persona {persona!r}, que nao esta em "
                "ingest.corp.PERSONAS. Persona nova no gerador precisa de "
                "correspondencia declarada, nao de adivinhacao"
            )
        fuso = f["timezone"]
        if fuso not in FUSOS:
            raise IngestError(
                f"funcionario {emp} tem fuso {fuso!r}, que nao esta em "
                "ingest.corp.FUSOS. Os motores chamam ZoneInfo() e precisam de "
                "chave IANA; deslocamento fixo novo precisa de correspondencia "
                "declarada, e so e licita se o fuso nao tiver horario de verao"
            )
        funcionarios.append(
            {
                "employee_id": emp,
                "department_id": mapa.departamentos[f["department"]],
                "site_id": mapa.sitios[f["site"]],
                "persona": PERSONAS[persona],
                "privilege": PRIVILEGIOS[privilegio_inicial.get(emp, 0)],
                "timezone": FUSOS[fuso],
            }
        )

    dispositivos = []
    for d in _abre(origem / "devices.csv"):
        tipo = d["device_type"]
        if tipo not in EQUIPAMENTOS:
            raise IngestError(
                f"equipamento {d['device_id']} e do tipo {tipo!r}, que nao esta "
                "em ingest.corp.EQUIPAMENTOS"
            )
        dono = _inteiro(d.get("owner_employee_id"))
        dispositivos.append(
            {
                "device_id": int(d["device_id"]),
                "employee_id": dono if dono is not None else SENTINELA_SEM_DONO,
                "kind": EQUIPAMENTOS[tipo],
                "ownership": "corporate"
                if _booleano(d.get("corporate"))
                else "personal",
            }
        )

    recursos = []
    for r in _abre(origem / "resources.csv"):
        dono = r.get("owner_department") or ""
        recursos.append(
            {
                "resource_id": int(r["resource_id"]),
                "kind": (
                    "file_share"
                    if r["system"].startswith(PREFIXO_COMPARTILHAMENTO)
                    else "system"
                ),
                "name": r["name"],
                "sensitivity": r["sensitivity"],
                "owner_department_id": mapa.departamentos.get(dono),
            }
        )

    # `network_ranges.csv` nao traz `range_id` — o gerador identifica faixa pela
    # posicao em `W.ranges`, e os eventos referenciam IP, nunca a faixa. O id e
    # a ordem do arquivo, que e a mesma ordem.
    faixas = [
        {
            "range_id": i,
            "cidr": linha["cidr"],
            "kind": linha["type"],
            "country": linha["country"],
            "city": linha["city"],
        }
        for i, linha in enumerate(_abre(origem / "network_ranges.csv"))
    ]

    return {
        "employees": funcionarios,
        "devices": dispositivos,
        "resources": recursos,
        "ranges": faixas,
    }


def _eventos(origem: Path, destino: Path) -> int:
    """Escreve `eventos.jsonl` linha por linha e devolve quantos sairam.

    `attributes` chega como texto JSON numa coluna do CSV e sai como objeto: o
    adaptador faz `dict(linha["attributes"])`, e texto viraria dicionario de
    caracteres sem erro nenhum.
    """
    total = 0
    with destino.open("w", encoding="utf-8") as saida:
        for linha in _abre(origem / "events.csv"):
            recurso = _inteiro(linha.get("resource_id"))
            evento = {
                "run_id": int(linha["run_id"]),
                "event_id": linha["event_id"],
                "employee_id": int(linha["employee_id"]),
                "occurred_at": linha["occurred_at"],
                "event_type": linha["event_type"],
                "result": linha["result"],
                "ip_address": linha["ip_address"],
                "device_id": int(linha["device_id"]),
                "session_id": linha["session_id"],
                "is_vpn": _booleano(linha.get("is_vpn")),
                "resource_id": recurso,
                "attributes": json.loads(linha["attributes"] or "{}"),
            }
            saida.write(json.dumps(evento, ensure_ascii=False) + "\n")
            total += 1
    if total == 0:
        raise IngestError("events.csv nao tem evento nenhum")
    return total


def _estado_de_conta(origem: Path) -> list[dict]:
    return [
        {
            "run_id": int(linha["run_id"]),
            "employee_id": int(linha["employee_id"]),
            "valid_from": linha["valid_from"],
            "valid_to": linha["valid_to"] or None,
            "mfa_enabled": _booleano(linha["mfa_enabled"]),
            "privilege": PRIVILEGIOS[int(linha["privilege_level"])],
        }
        for linha in _abre(origem / "account_state.csv")
    ]


def _estado_de_equipamento(origem: Path) -> list[dict]:
    return [
        {
            "run_id": int(linha["run_id"]),
            "device_id": int(linha["device_id"]),
            "state_date": linha["date"],
            "patch_age_days": int(linha["patch_age_days"]),
            "antivirus_on": _booleano(linha["antivirus_active"]),
        }
        for linha in _abre(origem / "device_state_daily.csv")
    ]


def converte_run(origem: Path, destino: Path) -> dict[str, int]:
    """Converte um `run_NNN/` do gerador para um diretorio do adaptador.

    Args:
        origem: o `run_NNN/` que o gerador escreveu, com `corp/` dentro.
        destino: onde gravar `corp/` no formato do adaptador. O `sdcac/` nao e
            criado aqui: quem o cria e o executor, ao abrir a execucao.

    Returns:
        Quantas linhas sairam de cada arquivo, para o relatorio da ingestao.

    Raises:
        IngestError: Se faltar arquivo, coluna ou correspondencia declarada.
    """
    corp_origem = origem / "corp"
    corp_destino = destino / "corp"
    corp_destino.mkdir(parents=True, exist_ok=True)

    mapa = Mapeamento()
    catalogo = _catalogo(corp_origem, mapa)
    (corp_destino / "catalogo.json").write_text(
        json.dumps(catalogo, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (corp_destino / "mapeamento.json").write_text(
        json.dumps(mapa.como_dicionario(), ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    (corp_destino / "estado-de-conta.json").write_text(
        json.dumps(_estado_de_conta(corp_origem), ensure_ascii=False), encoding="utf-8"
    )
    (corp_destino / "estado-de-equipamento.json").write_text(
        json.dumps(_estado_de_equipamento(corp_origem), ensure_ascii=False),
        encoding="utf-8",
    )
    eventos = _eventos(corp_origem, corp_destino / "eventos.jsonl")

    return {
        "funcionarios": len(catalogo["employees"]),
        "equipamentos": len(catalogo["devices"]),
        "recursos": len(catalogo["resources"]),
        "faixas": len(catalogo["ranges"]),
        "eventos": eventos,
    }
