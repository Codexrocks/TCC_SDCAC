# Equipe e papéis

Três frentes, sem sobreposição. **Mas todos precisam saber explicar o projeto
inteiro na banca** — problema, solução, arquitetura, testes e resultados.

---

## Davi — Líder & Backend

Dono da infraestrutura do projeto: o que roda e o que organiza.

**Responsabilidades**
- Arquitetura do sistema e API REST
- Modelagem e gestão do banco de dados relacional
- Geração e ingestão automatizada de logs/eventos
- Gestão do repositório GitHub e do versionamento
- Liderança executiva: prazos, atas, contato com o orientador

**Stack:** Python · FastAPI · PostgreSQL · Git/GitHub

**Estudar:** Python intermediário · APIs RESTful · SQL/PostgreSQL · Git Flow · Engenharia de Software

**GitHub:** [`@DaviSoaresDilly`](https://github.com/DaviSoaresDilly) · branches `davi/...`

**No repositório:** revisa todos os PRs · **único que executa merge na `main`** · mantém `docs/relatorios/`

---

## Yasmin — Cybersecurity Specialist

Dona do conteúdo de segurança: o que o sistema procura e por quê.

**Responsabilidades**
- Levantamento bibliográfico e referencial teórico
- Definição do baseline de normalidade vs. anomalia
- Modelagem das regras de detecção heurísticas
- Criação das faixas e pesos do Risk Score
- Desenho e execução dos cenários de teste de ataque

**Stack:** SIEM · SOC · UEBA · Incident Response · SecOps

**Estudar:** Pilares da Segurança (CIA) · Análise de Logs · UEBA · Ameaças Internas · Incident Response

**GitHub:** [`@Yas2046`](https://github.com/Yas2046) · branches `yasmin/...`

**No repositório:** dona de `docs/arquitetura.md` (regras e cenários) e do referencial teórico

---

## Filipe — Data & Dashboard Specialist

Dono da leitura dos dados: o que os números mostram.

**Responsabilidades**
- Tratamento, higienização e estruturação dos dados de log
- Construção dos painéis e visualizações do dashboard
- Cálculo de estatísticas e métricas de desempenho
- Módulo opcional de Machine Learning (Isolation Forest)

**Stack:** Python · Pandas · Matplotlib · Scikit-learn · Streamlit

**Estudar:** Análise exploratória de dados · Pandas · Visualização de dados · Métricas de ML (Precision, Recall, F1)

**GitHub:** [`@FilipeF4guiar`](https://github.com/FilipeF4guiar) · branches `filipe/...`

**No repositório:** dono do dashboard e dos resultados/gráficos do artigo · responsável pela [usabilidade](usabilidade.md) do painel

---

## Quem é quem no GitHub

| Pessoa | Usuário | Papel no repositório | Prefixo de branch |
|---|---|---|---|
| Davi | `@DaviSoaresDilly` | Admin · owner da organização | `davi/` |
| Yasmin | `@Yas2046` | Write | `yasmin/` |
| Filipe | `@FilipeF4guiar` | Write | `filipe/` |
| Assistente | `@claude` (workflow) | via GitHub Actions | `claude/` |

Todos abrem PR e aprovam PR dos outros. **Só o Davi executa o merge na `main`** —
é trava do GitHub, explicada em [Configuração](configuracao.md#quem-pode-executar-o-merge).

> Primeira vez no GitHub? O [Guia do GitHub](guia-github.md) parte do zero: o que
> é branch, como aprovar um PR e como escrever documentação sem instalar nada.

## Responsabilidade de todos

- Escrever a parte do artigo que corresponde à sua frente
- Revisar pelo menos 1 PR por semana
- Comparecer à reunião semanal de 30 min
- Saber explicar o projeto inteiro na defesa
