"""O executor do experimento — entrada sem HTTP.

Uma das duas entradas do monolito. A outra e `backend/`, que fala HTTP. As duas
importam `detection/`; nenhuma das duas e importada por ele.

E aqui que o experimento do artigo roda: duas janelas, quatro configuracoes, um
registro de execucao por configuracao, com o hash da configuracao gravado junto.
"""

from runner.experiment import ExperimentResult, code_sha, run_experiment

__all__ = ["ExperimentResult", "code_sha", "run_experiment"]
