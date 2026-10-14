"""Os adaptadores das portas de `detection/ports.py`.

Aqui vive o que sabe de formato: arquivo hoje, PostgreSQL quando o banco
existir. O nucleo nao importa nada daqui — a dependencia e de fora para dentro,
sempre, e e o CI que confere.

**Por que um adaptador de arquivo, e nao um de banco direto.** O banco nao
existe: nao ha servidor, e o gerador de eventos e a frente da S6. Escrever o
adaptador de PostgreSQL agora produziria algumas centenas de linhas de SQL que
ninguem conseguiria executar, e que pareceriam prontas. O adaptador de arquivo
roda, e o **teste de contrato** que acompanha as portas serve de especificacao
executavel para quem escrever o de banco depois: a implementacao que mentir
reprova.

**O formato nao e contrato.** JSON Lines para evento, JSON para o resto, porque
e o que se le com o olho num `cat` e o que se versiona sem ferramenta. Nenhuma
decisao do artigo depende disso, e trocar por Parquet ou por banco nao muda uma
linha de `detection/`.
"""
