-- Privilegios no banco `ground_truth`
--
--     psql -d ground_truth -v ON_ERROR_STOP=1 -f database/ground_truth/002_privilegios.sql
--
-- Dois papeis, e o terceiro nem chega aqui: `sdcac_app` nao tem CONNECT neste
-- banco. Se algum dia aparecer um GRANT para ele neste arquivo, a trava contra
-- vazamento de rotulo caiu — e tests/test_schema.py reprova por isso.

GRANT USAGE ON SCHEMA public TO generator, evaluator;

-- O gerador escreve o gabarito junto com os eventos, na mesma execucao.
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO generator;

-- O avaliador le o gabarito para calcular FPR e revocacao. Nao escreve.
GRANT SELECT ON ALL TABLES IN SCHEMA public TO evaluator;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT ON TABLES TO generator;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO evaluator;
