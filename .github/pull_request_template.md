## O que muda

<!-- Uma ou duas frases. -->

## Por quê

<!-- Qual item do cronograma ou da entrega isso atende. -->

## Uso de IA

<!--
Obrigatório: o check "Governança" reprova o PR se algum campo ficar em branco.
Resposta curta e honesta basta. Não usou IA? Escreva "nenhuma" — é resposta
válida, e o silêncio não distingue "não usei" de "esqueci".
Política em docs/uso-de-ia.md.
-->

- **IA usada:** <!-- ex.: Claude Opus 5 · Gemini 2.5 Pro · Copilot · nenhuma -->
- **No que ajudou:** <!-- seja específico: "rascunhou a seção 2", não "ajudou" -->
- **O que é meu:** <!-- o que você pensou, decidiu, leu ou verificou -->
- **Conferi tudo que a IA escreveu:** <!-- sim / não -->

<!--
A última pergunta é a que carrega a responsabilidade: o texto entra no TCC no
seu nome, não no da IA. Referência bibliográfica que ninguém abriu na fonte não
entra — marque a linha com o aviso de citação pendente e siga.
-->

## Arquivo protegido

<!--
Obrigatória só quando o PR toca AGENTS.md, CLAUDE.md, GEMINI.md,
.github/copilot-instructions.md, CONTRIBUTING.md, docs/padroes*.md,
docs/processo.md, .github/** ou scripts/**. Nesse caso o PR também fica 24 h
aberto antes de entrar, e o check "Governança" confere as duas coisas.
Não tocou nenhum desses? Apague esta seção.
-->

- **O que muda:** <!-- a regra ou a checagem, em uma linha -->
- **Por que agora:** <!-- o que aconteceu para ela mudar hoje -->
- **O que segura no lugar:** <!-- se afrouxou, o que passa a impedir o abuso -->

## Checklist

- [ ] Branch no padrão `<autor>/<tipo>/<assunto>` — ex.: `yasmin/docs/referencial-teorico`
- [ ] Commits no padrão `tipo: descrição`, com a linha `Assistido-por:`
- [ ] Se criei página em `docs/`, adicionei ao `docs/SUMMARY.md`
- [ ] Não há `.env`, senha, token ou chave no diff
- [ ] `python3 scripts/validar.py` passou
- [ ] Li o diff inteiro antes de abrir — é a autorrevisão que ficou no lugar da
      revisão de colega
- [ ] Mexi em regra ou checagem? Preenchi a seção **Arquivo protegido** e sei
      que o PR fica **24 h** aberto antes de entrar

## Responsável

<!-- Davi -->
