@AGENTS.md

# Regras — TCC_SDCAC

A linha acima não é enfeite: ela **importa** o
[`AGENTS.md`](AGENTS.md) para o contexto, em vez de pedir que você abra o
arquivo e torcer para que abra.

As regras deste repositório valem para **qualquer** assistente de IA e estão lá,
num arquivo só. Este aqui existe porque o Claude Code procura por `CLAUDE.md`;
o `AGENTS.md` é o padrão que as outras ferramentas leem.

Não duplique regra aqui. Regra nova entra no `AGENTS.md`, e mudá-lo exige 24 h
de Pull Request aberto e a seção `Arquivo protegido` preenchida.

O resumo do que mais pega, sem substituir a leitura:

- Português do Brasil em tudo
- Nunca commitar na `main` — sempre branch + Pull Request
- **Nunca fazer merge nem aprovar PR**
- Declarar a IA usada no commit (`Assistido-por:`) e no PR
- Mudar regra, workflow ou script espera **24 h** e se explica na seção `Arquivo protegido`
- Na dúvida, perguntar antes de fazer
