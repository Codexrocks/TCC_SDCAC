# Padrões de código

O código só começa na **S6 (02/10)**. Esta página existe agora para que ninguém
precise decidir formatação no meio da implementação, e para que o revisor tenha
um critério objetivo em vez de gosto pessoal.

Complementa [`padroes.md`](padroes.md), que trata de branch, commit e PR. Aqui é
sobre o que vai dentro dos arquivos.

---

## 1. Linguagem e versão

**Python 3.12.** Todos com a mesma versão *minor* — diferença de versão é a
causa mais comum de "na minha máquina funciona".

> Versões mais novas (3.13, 3.14) costumam demorar a ter pacote pronto para
> `pandas`, `scikit-learn` e afins, e a instalação passa a tentar compilar da
> fonte. Se você já tem uma dessas instalada, mantenha, mas crie o ambiente do
> projeto na 3.12.

Ambiente virtual, sempre, e nunca versionado — o `.gitignore` já cuida disso:

```bash
python3.12 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

---

## 2. Idioma no código

A regra do [`CLAUDE.md`](../CLAUDE.md) aplicada ao código:

| O quê | Idioma | Por quê |
|---|---|---|
| Nomes de variável, função, classe, arquivo | **inglês** | Convenção da linguagem. `risk_score`, não `pontuacao_de_risco` |
| Comentários | **português** | Quem lê é a equipe e a banca |
| Docstrings | **português** | Idem |
| Mensagem de log e de erro para o usuário | **português** | Aparece na tela do analista |
| Nome de coluna no banco | **inglês** | Já definido em [`arquitetura.md`](arquitetura.md) |

```python
def calculate_risk_score(event: Event) -> int:
    """Soma os pontos das regras que o evento dispara.

    O teto e 100 mesmo que a soma das regras passe disso — a faixa
    RISCO ALTO comeca em 76 e nao faz sentido distinguir 100 de 130.
    """
```

---

## 3. Formatação — não se discute em PR

Formatação é decidida por ferramenta, não por revisor. Ninguém comenta espaço
em branco num PR deste projeto.

| Ferramenta | Faz o quê |
|---|---|
| **Ruff formatter** | Formata o arquivo. Linha de 88 colunas, aspas duplas |
| **Ruff linter** | Pega import não usado, variável morta, comparação suspeita, ordenação de import |

Configuração completa no [`pyproject.toml`](../pyproject.toml) da raiz. Antes de
abrir PR:

```bash
ruff format .
ruff check --fix .
```

O `.editorconfig` da raiz garante o mesmo espaçamento em quem usa VS Code,
PyCharm ou outro editor, sem ninguém configurar nada à mão.

---

## 4. Nomes

Segue a **PEP 8**, que é o guia de estilo oficial do Python:

| Elemento | Estilo | Exemplo |
|---|---|---|
| Variável e função | `snake_case` | `failed_attempts`, `load_events()` |
| Classe | `PascalCase` | `RiskScoreCalculator` |
| Constante | `UPPER_SNAKE_CASE` | `MAX_SCORE`, `RULE_WEIGHTS` |
| Módulo e arquivo | `snake_case.py` | `risk_score.py` |
| Privado ao módulo | prefixo `_` | `_normalize_ip()` |

Nome diz o que a coisa é, não o tipo dela. `events`, não `event_list`. Booleano
começa com verbo de estado: `is_anomalous`, `has_alert`.

**Nada de abreviação inventada.** `cnt`, `usr`, `evt` custam mais caro em leitura
do que economizam em digitação. Exceções consagradas — `id`, `ip`, `db`, `api` —
seguem valendo.

---

## 5. Tipagem

**Type hints obrigatórios** em toda função pública: parâmetros e retorno.

```python
def detect_brute_force(events: list[Event], window_minutes: int = 2) -> bool:
    ...
```

Serve para três coisas: o editor autocompleta, o revisor entende a assinatura
sem ler o corpo, e erro de tipo aparece antes de rodar.

Use os tipos nativos (`list[str]`, `dict[str, int]`), não os do módulo `typing`.

---

## 6. Docstrings

**PEP 257.** Toda função pública, classe e módulo tem docstring. Função privada
de três linhas óbvias, não precisa.

```python
def calculate_risk_score(event: Event) -> int:
    """Soma os pontos das regras disparadas pelo evento.

    Args:
        event: Evento ja normalizado, vindo da ingestao.

    Returns:
        Pontuacao de 0 a 100, limitada ao teto.

    Raises:
        ValueError: Se o evento nao tiver timestamp.
    """
```

Comentário explica **por quê**, nunca **o quê** — o código já diz o quê:

```python
# Ruim: incrementa o contador
counter += 1

# Bom: o log do sistema conta a tentativa que falhou e a que teve
# sucesso depois dela, entao descontamos uma para nao inflar o score
counter += 1
```

---

## 7. Estrutura de pastas

Já definida em [`arquitetura.md`](arquitetura.md). Não invente pasta nova sem
falar com o Davi — e **não crie pasta vazia**, conforme o
[`CLAUDE.md`](../CLAUDE.md). A pasta nasce junto com o primeiro arquivo dela.

Cada módulo faz uma coisa. Se um arquivo passa de ~300 linhas, provavelmente
está fazendo duas.

---

## 8. Testes

**pytest.** Todo arquivo em `detection/` precisa de teste — é o coração do TCC e
o que a banca vai querer ver funcionando.

```
tests/
├── test_risk_score.py
├── test_rules.py
└── scenario_01/ ... scenario_06/     os 6 cenarios de arquitetura.md
```

| Regra | Detalhe |
|---|---|
| Nome do arquivo | `test_<modulo>.py` |
| Nome da função | `test_<o_que_verifica>` — `test_score_soma_horario_e_ip` |
| Estrutura | Arrange, Act, Assert — separados por linha em branco |
| Um teste, uma afirmação | Se precisa de três `assert` sem relação, são três testes |

Rodar:

```bash
pytest
pytest --cov=detection --cov-report=term-missing
```

Os **seis cenários** de `arquitetura.md` viram teste automatizado, com o score
esperado de cada um. É o que transforma "o sistema detecta" em "o sistema
detecta, e aqui está a prova que roda sozinha".

---

## 9. Segredo e configuração

**Nunca no código.** Nem em comentário, nem em teste, nem "temporariamente".

| Onde vai | O quê |
|---|---|
| Variável de ambiente | Credencial de banco, chave de API, token |
| `.env` local | Os valores da máquina de cada um — **nunca versionado** |
| `.env.example` | As chaves com valor vazio, para o outro saber o que precisa preencher |
| `pyproject.toml` | Configuração pública: versão, dependências, ferramentas |

```python
import os

DATABASE_URL = os.environ["DATABASE_URL"]   # estoura cedo se faltar
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

O `scripts/validar.py` procura segredo vazado a cada PR, mas ele pega padrão
conhecido — não confie nele como única barreira.

---

## 10. Log e erro

O sistema é de detecção: log mal feito aqui é falha de produto, não detalhe.

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Evento %s classificado como %s (score %d)", event.id, band, score)
```

- `logging`, nunca `print()` fora de script de uso manual
- Passe os valores como argumento (`%s`), não concatene — assim o log fica
  estruturado e barato quando o nível está desligado
- **Nunca logue credencial, token ou o conteúdo integral de um evento sensível**
- Erro esperado: trate e explique. Erro inesperado: deixe subir. `except:` mudo
  esconde defeito e é reprovado na revisão

| Nível | Quando |
|---|---|
| `DEBUG` | Detalhe de desenvolvimento |
| `INFO` | Evento normal do fluxo: ingestão, classificação |
| `WARNING` | Algo estranho que não impediu de continuar |
| `ERROR` | Falhou de verdade |

---

## 11. Banco de dados

Tabelas `users`, `events`, `alerts`, `risk_scores`, conforme
[`arquitetura.md`](arquitetura.md).

- Schema versionado em `database/schema.sql`. Mudou o schema? Vai no mesmo PR
  do código que depende dele
- Query sempre **parametrizada**. Nunca monte SQL com f-string ou concatenação
  de variável — é injeção de SQL, e num TCC de segurança isso é constrangedor
- Todo `SELECT` que alimenta tela tem `LIMIT`

```python
# Certo
cursor.execute("SELECT * FROM events WHERE user_id = %s LIMIT 100", (user_id,))

# Errado — nunca faca isso
cursor.execute(f"SELECT * FROM events WHERE user_id = {user_id}")
```

---

## 12. O que o revisor olha

Além do que já está em [`padroes.md`](padroes.md):

- [ ] `ruff format` e `ruff check` passam
- [ ] Função pública tem type hint e docstring em português
- [ ] Nome de variável em inglês, sem abreviação inventada
- [ ] Regra de detecção nova tem teste, e o teste falha se a regra for removida
- [ ] Nenhum segredo, nem em teste
- [ ] SQL parametrizado
- [ ] Sem `print()` sobrando nem `except:` mudo
- [ ] Se mexeu no dashboard, atende à [usabilidade](usabilidade.md) — rótulo
      textual junto da cor, contraste de 4,5:1

---

## 13. Referências

PEP 8 — *Style Guide for Python Code*. Disponível em:
https://peps.python.org/pep-0008/

PEP 257 — *Docstring Conventions*. Disponível em:
https://peps.python.org/pep-0257/

PEP 484 — *Type Hints*. Disponível em: https://peps.python.org/pep-0484/

Ruff — documentação. Disponível em: https://docs.astral.sh/ruff/

pytest — documentação. Disponível em: https://docs.pytest.org/
