## O que muda

Recalcula o quadro contra a data de hoje. As três páginas geradas são
`docs/quadro.md` e os blocos marcados de `docs/cronograma.md` e
`docs/decisoes.md`.

Este PR foi aberto pelo workflow **Quadro**, sem nenhum assistente no meio: o
conteúdo sai de `scripts/quadro.py` lendo o `quadro.toml`. Para reproduzir:

```
python3 scripts/quadro.py
```

## Por quê

Situação de prazo escrita à mão envelhece em silêncio. Em 26/09/2026 o
cronograma dizia que a Tarefa 02 vencia "amanhã" — o prazo tinha sido 24/09.

Nada de **fato** muda aqui. Data, dono, critério e estado moram no `quadro.toml`
e só mudam quando uma pessoa edita. O que muda neste PR é só o que se calcula:
que dia é hoje, o que venceu, o que entra na semana.

## Uso de IA

- **IA usada:** nenhuma
- **No que ajudou:** nada. O conteúdo é aritmética de data feita por
  `scripts/quadro.py`, determinística e reproduzível por qualquer pessoa que rode
  o script
- **O que é meu:** os fatos do `quadro.toml`, que são editados à mão por pessoas
  em Pull Request próprio. Este PR não inventa nem altera nenhum deles
- **Conferi tudo que a IA escreveu:** não se aplica — nenhuma IA escreveu. Quem
  for mergear confere o diff, que é curto por construção

## Checklist

- [x] Branch no padrão `<autor>/<tipo>/<assunto>`
- [x] Commits no padrão `tipo: descrição`, com a linha `Assistido-por:`
- [x] Não criei página nova em `docs/`
- [x] Não há `.env`, senha, token ou chave no diff
- [x] Nenhum arquivo protegido no diff — só as três páginas geradas
- [ ] Alguém leu o diff antes do merge

## Responsável

Davi
