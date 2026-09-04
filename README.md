# TCC_SDCAC — Sistema de Detecção de Comportamentos Anômalos em Cybersecurity

Trabalho de Conclusão de Curso · Prof. Euzébio D. de Souza · 2026/2

## O que é

Protótipo que analisa eventos de usuários, identifica comportamentos fora do
padrão, calcula um **Risk Score (0–100)** e dispara alertas num dashboard de
monitoramento. Segurança defensiva (Blue Team), em ambiente corporativo simulado.

**Pergunta de pesquisa:** como a análise automatizada de eventos e comportamentos
de usuários pode contribuir para a identificação de atividades anômalas em
ambientes corporativos?

## Equipe

| Pessoa | Papel | Frente |
|---|---|---|
| **Davi** | Líder & Backend | API, banco de dados, repositório, prazos |
| **Yasmin** | Cybersecurity Specialist | Referencial teórico, regras de detecção, Risk Score |
| **Filipe** | Data & Dashboard Specialist | Dados, dashboard, métricas |

Detalhes em [`docs/equipe.md`](docs/equipe.md).

## Como este projeto se organiza

- **GitHub (aqui)** — versionamento do código do protótipo e fonte da documentação.
- **GitBook** — leitura da documentação, sincronizado automaticamente com a pasta `docs/`.
- **Claude** — assistente do repositório: responde a `@claude` em issues e PRs e
  registra relatórios em `docs/relatorios/`.

## Documentação

| Página | Conteúdo |
|---|---|
| [Equipe e papéis](docs/equipe.md) | Quem faz o quê |
| [Processo de trabalho](docs/processo.md) | Como GitHub, GitBook e Claude se encaixam |
| [Padrões](docs/padroes.md) | Branch, commit, pull, push, merge, docs, relatórios |
| [Configuração](docs/configuracao.md) | GitBook, secrets, ruleset, CODEOWNERS — passo a passo |
| [Cronograma](docs/cronograma.md) | As 16 semanas |
| [Arquitetura](docs/arquitetura.md) | Fluxo, regras de risco, cenários de teste |
| [Entregas](docs/entregas/tarefa-01.md) | O que o professor pediu |
| [Relatórios](docs/relatorios/) | Histórico das sessões com o Claude |

## Antes de abrir um Pull Request

```bash
python3 scripts/validar.py
```

Confere nome de branch, formato dos commits, cobertura do `SUMMARY.md`, links
quebrados e segredo vazado. O mesmo script roda no CI a cada PR.

Resumo das regras: [`CONTRIBUTING.md`](CONTRIBUTING.md) · Regras do assistente: [`CLAUDE.md`](CLAUDE.md)
