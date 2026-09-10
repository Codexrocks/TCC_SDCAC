# TCC_SDCAC — Sistema de Detecção de Comportamentos Anômalos em Cybersecurity

Trabalho de Conclusão de Curso · Prof. Euzébio D. de Souza · 2026/2

> **O título está em revisão.** O [plano](docs/plano.md) adota "Sistema de
> Avaliação Multidimensional de Risco Comportamental". A troca depende da decisão
> [D-01](docs/decisoes.md), a comunicar ao orientador — até lá vale o título
> acima, que é o da Tarefa 01 entregue em 03/09.

## O que é

Um **estudo comparativo** em segurança defensiva (Blue Team), sobre ambiente
corporativo simulado. O protótipo avalia o risco de cada evento em três
dimensões — o evento em si, o desvio em relação ao comportamento habitual do
usuário, e a exposição acumulada ao longo de dias — e mede o resultado contra uma
linha de base de regras fixas.

```text
C0 ──────► C1 ──────► C2 ──────► C3
regras     + risco    + desvio    + exposição
fixas      do evento  do usuário  acumulada
(controle) (D1)       (D1+D2)     (D1+D2+D3)
```

**Pergunta de pesquisa:** a avaliação combinada do risco do evento individual, do
desvio comportamental do usuário e da exposição acumulada ao risco reduz a taxa
de falsos positivos, a uma mesma revocação, e aumenta a revocação em cenários
longitudinais, quando comparada à análise baseada exclusivamente em regras fixas
aplicadas a eventos individuais?

A pergunta admite "não", e "não" também é resultado. Formulação completa e
operacionalização das métricas no [plano](docs/plano.md).

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
| [Plano do TCC](docs/plano.md) | O que o trabalho é: pergunta, objetivos, desenho experimental |
| [Registro de decisões](docs/decisoes.md) | O que já foi decidido, e o que continua aberto |
| [Formato COBEM](docs/cobem.md) | Como o artigo é diagramado |
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
