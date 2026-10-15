"""Exporta o contrato da API para arquivo versionado.

```bash
python -m backend.openapi
```

**Por que o contrato fica no git, e nao so no servidor.** O painel e a frente do
Filipe, e ele nao pode depender de a API estar de pe para saber o que ela
devolve: o arquivo no repositorio e lido sem rodar nada. Alem disso, mudanca de
contrato passa a **aparecer no diff** — hoje ela apareceria so quando alguma tela
quebrasse.

Um teste compara o arquivo com o que a aplicacao gera e reprova se divergirem, do
mesmo jeito que o `docs/quadro.md` e comparado com o `quadro.toml`.
"""

import json
from pathlib import Path

CONTRATO = Path(__file__).resolve().parent / "openapi.json"


def contrato() -> dict:
    """O OpenAPI que a aplicacao gera agora."""
    from backend.main import cria_app

    return cria_app().openapi()


def texto_do_contrato() -> str:
    """O contrato serializado como o arquivo versionado guarda."""
    return json.dumps(contrato(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    CONTRATO.write_text(texto_do_contrato(), encoding="utf-8")
    dados = contrato()
    rotas = len(dados.get("paths", {}))
    print(f"contrato gravado em {CONTRATO.name}: {rotas} rotas")  # noqa: T201
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
