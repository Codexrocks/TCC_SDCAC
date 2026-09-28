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

**No repositório:** dona das **regras de detecção e dos cenários**, que vivem em `docs/arquitetura.md`, e do referencial teórico. A **arquitetura v2** — as três dimensões e as quatro configurações — é do Davi, na S5

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
| Yasmin | `@Yas2046` | Leitura — produz fora e o Davi versiona | `yasmin/` (reservado) |
| Filipe | `@FilipeF4guiar` | Leitura — produz fora e o Davi versiona | `filipe/` (reservado) |
| Assistente | `@claude` (workflow) | via GitHub Actions | `claude/` |

**Desde 23/09/2026 só o Davi opera o GitHub.** Yasmin e Filipe produzem fora —
documento, planilha, rascunho — e ele versiona por Pull Request. A autoria não
muda por causa do caminho: quem produziu responde pelo conteúdo, e o Pull Request
precisa dizer de quem é o quê. O caminho completo está no
[cronograma](cronograma.md#como-o-trabalho-chega-ao-repositório).

Com uma pessoa só operando, **não há aprovação de outra pessoa** — o GitHub não
deixa ninguém aprovar o próprio Pull Request. No lugar entraram as 24 h de espera
e a seção `Arquivo protegido` nos arquivos de regra, conferidas pelo check
**Governança**. **Só o Davi executa o merge na `main`** — é trava do GitHub,
explicada em [Configuração](configuracao.md#quem-pode-executar-o-merge).

> Primeira vez no GitHub? O [Guia do GitHub](guia-github.md) parte do zero: o que
> é branch, como aprovar um PR e como escrever documentação sem instalar nada.

## Responsabilidade de todos

- Escrever a parte do artigo que corresponde à sua frente
- Entregar o material da sua frente a tempo de o Davi versionar na semana
- **Declarar a IA que usou**, no que ela ajudou e o que é seu — quem versiona
  transcreve, e campo em branco vira "não declarado por quem produziu" no Pull
  Request. Ver [política de uso de IA](uso-de-ia.md)
- Comparecer à reunião semanal de 30 min
- Saber explicar o projeto inteiro na defesa
