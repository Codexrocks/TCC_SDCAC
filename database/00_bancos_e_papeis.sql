-- Bancos e papeis do TCC_SDCAC
--
-- Roda UMA VEZ, conectado como superusuario, antes de qualquer outro arquivo.
-- CREATE DATABASE nao roda dentro de transacao: aplique com
--     psql -v ON_ERROR_STOP=1 -f database/00_bancos_e_papeis.sql
--
-- Sao tres bancos, e nao tres schemas, porque a trava contra vazamento de
-- rotulo e o privilegio CONNECT, que no PostgreSQL vale por banco. Com bancos
-- separados, a aplicacao nao tem como cruzar evento com gabarito nem por
-- engano: consulta entre bancos exige extensao, e nenhuma esta instalada.
-- Ver docs/banco-simulado.md, secao 8.
--
-- Os papeis nascem SEM SENHA. A senha de cada um e definida fora daqui, a
-- partir do .env da maquina:
--     ALTER ROLE generator PASSWORD :'senha'
-- Repositorio publico nao guarda credencial, nem de ambiente local.

-- ---------------------------------------------------------------------------
-- Papeis
-- ---------------------------------------------------------------------------

-- Escreve os eventos e o gabarito. E o unico que enxerga os dois lados.
CREATE ROLE generator LOGIN;

-- A aplicacao: le o corp, escreve no sdcac. NUNCA conecta no ground_truth.
CREATE ROLE sdcac_app LOGIN;

-- Calcula as metricas: le o gabarito e os scores. Nao escreve score.
CREATE ROLE evaluator LOGIN;

-- ---------------------------------------------------------------------------
-- Bancos
-- ---------------------------------------------------------------------------

CREATE DATABASE corp;
CREATE DATABASE ground_truth;
CREATE DATABASE sdcac;

-- ---------------------------------------------------------------------------
-- Quem conecta onde
--
-- O PostgreSQL da CONNECT a PUBLIC em banco novo. Sem o REVOKE abaixo, a
-- separacao dos tres bancos seria decorativa.
-- ---------------------------------------------------------------------------

REVOKE CONNECT ON DATABASE corp FROM PUBLIC;
REVOKE CONNECT ON DATABASE ground_truth FROM PUBLIC;
REVOKE CONNECT ON DATABASE sdcac FROM PUBLIC;

GRANT CONNECT ON DATABASE corp TO generator, sdcac_app, evaluator;

-- A linha que falta e a que importa: sdcac_app NAO aparece aqui.
GRANT CONNECT ON DATABASE ground_truth TO generator, evaluator;

GRANT CONNECT ON DATABASE sdcac TO sdcac_app, evaluator;
