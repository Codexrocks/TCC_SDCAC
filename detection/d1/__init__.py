"""D1 — risco do evento individual, com peso por atributo.

Mesmo evento isolado da C0, com mais atributos e peso por atributo em vez de
ponto fixo. A diferenca entre as duas e o que a configuracao C1 mede contra a
linha de base.

Como a C0, a D1 **nao olha o passado do funcionario**: ela consulta cadastro —
fuso da sede do funcionario, dono do dispositivo, sigilo do recurso, tipo da
faixa de rede. Cadastro nao e historico, e a invariante vale para as duas.
"""

from detection.d1.scoring import score_d1

__all__ = ["score_d1"]
