"""A aplicacao HTTP — a segunda entrada do monolito.

```bash
SDCAC_DADOS=dados/semente-1 python -m uvicorn backend.main:app --host 127.0.0.1
```

O contrato publicado fica em `/api/v1/openapi.json`, e o painel comeca por ele.
Ha tambem `/docs`, que e a pagina de exploracao que o FastAPI gera — util para
conferir uma rota a mao, e **nao** e o painel: tela, navegacao e texto de
onboarding sao outra peca, governada pela usabilidade.

## O que esta aplicacao protege, e o que nao protege

**Nao ha login na v1, pela D-32.** Dizer que isso e seguro porque a API e so de
leitura seria mentira confortavel, entao o desenho e explicito:

- **escuta em `127.0.0.1`.** A trava e de rede, nao de codigo. Quem quiser expor
  na rede precisa dizer isso em voz alta, com `--host`, e assumir;
- **a trava que de fato protege o experimento e o papel de banco**, nao esta
  aplicacao: `sdcac_app` nao tem permissao de conectar no `ground_truth`. O login
  protegeria a tela; o papel protege o resultado;
- **CORS com lista explicita de origens.** `*` seria o atalho, e deixaria
  qualquer pagina aberta no navegador de quem analisa consultar esta API. A lista
  vem do ambiente, e o padrao e so o desenvolvimento local do painel;
- **paginacao com teto duro de 200.** Nao e conforto de tela: sem teto, uma
  requisicao puxa dois milhoes de eventos, e e a negacao de servico mais barata
  que existe;
- **envelope de erro unico, sem SQL, caminho de arquivo ou rastreio de pilha.**
  O repositorio e publico; isso nao e motivo para a API narrar como ela e feita
  por dentro quando algo falha.

O que **nao** esta aqui, e nem finge estar: limitacao de taxa, cabecalho de
seguranca de navegador, auditoria de consulta. Nenhum deles faz sentido num
instrumento de analise que roda em `localhost` para uma pessoa — e a **D-19**
registra a auditoria como o que a implantacao real exigiria.
"""

import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api import router
from backend.schemas import Erro

TITULO = "SDCAC — API de leitura"
VERSAO = "1.0.0"

ORIGENS_PADRAO = ("http://localhost:5173", "http://127.0.0.1:5173")
VARIAVEL_DE_ORIGENS = "SDCAC_ORIGENS"

DESCRICAO = """
Leitura dos resultados do **Sistema de Avaliação Multidimensional de Risco
Comportamental**.

Toda nota vem **decomposta nas cinco parcelas** — `c0`, `d1`, `d2`,
`d3_conduct`, `d3_posture`. Parcela nula significa *dimensão não avaliada nesta
configuração*, e é diferente de zero, que significa *avaliada e sem risco*.

Esta API **não calcula**: faixa, parcela e motivo vêm do motor; métrica vem do
avaliador. Nenhuma rota escreve, e nenhuma lê o gabarito.
""".strip()


def origens_permitidas() -> list[str]:
    """As origens do CORS, da variavel de ambiente ou o padrao local."""
    bruto = os.environ.get(VARIAVEL_DE_ORIGENS, "")
    if not bruto.strip():
        return list(ORIGENS_PADRAO)
    return [parte.strip() for parte in bruto.split(",") if parte.strip()]


def _erro(
    code: str, message: str, detail: str | None, status_code: int
) -> JSONResponse:
    corpo = Erro(code=code, message=message, detail=detail)
    return JSONResponse(status_code=status_code, content=corpo.model_dump())


def cria_app() -> FastAPI:
    """Monta a aplicacao. Funcao, e nao modulo, para o teste criar a sua."""
    app = FastAPI(
        title=TITULO,
        version=VERSAO,
        description=DESCRICAO,
        openapi_url="/api/v1/openapi.json",
        docs_url="/docs",
        redoc_url=None,
    )

    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origens_permitidas(),
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return _erro(
            code="nao_encontrado" if exc.status_code == 404 else "erro_http",
            message=str(exc.detail),
            detail=None,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def _validacao(_: Request, exc: RequestValidationError) -> JSONResponse:
        # A mensagem diz qual parametro, e nao devolve o corpo inteiro de volta.
        campos = ", ".join(
            ".".join(str(parte) for parte in erro["loc"][1:]) for erro in exc.errors()
        )
        return _erro(
            code="parametro_invalido",
            message="parametro fora do formato esperado",
            detail=campos or None,
            status_code=422,
        )

    @app.exception_handler(Exception)
    async def _inesperado(_: Request, exc: Exception) -> JSONResponse:
        # Sem rastreio de pilha, sem caminho de arquivo, sem SQL. O detalhe fica
        # no log do servidor; o cliente recebe que falhou, e nada sobre como.
        return _erro(
            code="erro_interno",
            message="a requisicao nao pode ser atendida",
            detail=None,
            status_code=500,
        )

    return app


app = cria_app()
