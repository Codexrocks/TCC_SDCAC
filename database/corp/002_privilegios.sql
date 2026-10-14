-- Privilegios no banco `corp`
--
--     psql -d corp -v ON_ERROR_STOP=1 -f database/corp/002_privilegios.sql
--
-- A regra da especificacao: "so insercao. A tabela nao aceita UPDATE nem
-- DELETE, por privilegio de banco. Log e evidencia." Nenhum GRANT UPDATE ou
-- DELETE aparece neste arquivo, e tests/test_schema.py reprova se aparecer.

GRANT USAGE ON SCHEMA public TO generator, sdcac_app, evaluator;

-- O gerador tambem cria particao por semente, e CREATE no schema e o que
-- permite isso sem ser superusuario.
GRANT CREATE ON SCHEMA public TO generator;

-- ---------------------------------------------------------------------------
-- generator — escreve a corporacao e os eventos
-- ---------------------------------------------------------------------------

GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO generator;

-- ---------------------------------------------------------------------------
-- sdcac_app — so le. O motor pontua, nao corrige o log
-- ---------------------------------------------------------------------------

GRANT SELECT ON ALL TABLES IN SCHEMA public TO sdcac_app;

-- ---------------------------------------------------------------------------
-- evaluator — le para montar o denominador das metricas por usuario-dia
-- ---------------------------------------------------------------------------

GRANT SELECT ON ALL TABLES IN SCHEMA public TO evaluator;

-- Tabela criada depois deste arquivo nasce sem privilegio nenhum, e a carga
-- falharia sem explicacao obvia. Estas linhas valem para o futuro.
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT ON TABLES TO generator;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO sdcac_app, evaluator;
