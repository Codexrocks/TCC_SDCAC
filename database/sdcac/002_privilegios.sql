-- Privilegios no banco `sdcac`
--
--     psql -d sdcac -v ON_ERROR_STOP=1 -f database/sdcac/002_privilegios.sql
--
-- A aplicacao escreve padrao, nota e alerta. O avaliador escreve so metrica —
-- e nao escreve nota, porque quem ve o gabarito nao pode mexer no score.

GRANT USAGE ON SCHEMA public TO sdcac_app, evaluator;

-- ---------------------------------------------------------------------------
-- sdcac_app — calcula e grava
-- ---------------------------------------------------------------------------

GRANT SELECT, INSERT ON baselines, scoring_runs, risk_scores, alerts TO sdcac_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO sdcac_app;

-- Le a metrica para exibir, sem calcular nem gravar.
GRANT SELECT ON metrics TO sdcac_app;

-- ---------------------------------------------------------------------------
-- evaluator — mede
-- ---------------------------------------------------------------------------

GRANT SELECT ON ALL TABLES IN SCHEMA public TO evaluator;
GRANT INSERT ON metrics TO evaluator;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO evaluator;
