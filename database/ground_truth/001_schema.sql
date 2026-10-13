-- Banco `ground_truth` — o gabarito
--
--     psql -d ground_truth -v ON_ERROR_STOP=1 -f database/ground_truth/001_schema.sql
--
-- Aqui mora a resposta da prova: quais episodios foram injetados, em quem, e
-- qual rotulo cada evento carrega. A aplicacao nao tem CONNECT neste banco
-- (ver database/00_bancos_e_papeis.sql), e e isso que impede o resultado de
-- ficar bom pelo motivo errado.

-- As quatro categorias de cenario da D-06 e da D-16.
CREATE TYPE episode_category AS ENUM (
    'punctual',
    'contextual',
    'longitudinal',
    'negative_control'
);

-- Tres rotulos, em identificador ingles:
--   normal                 comportamento normal
--   legitimate_deviation   divergente legitimo — nao conta como positivo
--   suspicious             suspeito — o unico que conta como positivo
CREATE TYPE label_kind AS ENUM ('normal', 'legitimate_deviation', 'suspicious');

-- Se o cenario acrescenta eventos ou substitui eventos normais. Acrescentar
-- sempre faria o total diario da vitima dar um salto, e qualquer detector de
-- volume acertaria por causa do gerador, nao do metodo.
CREATE TYPE injection_mode AS ENUM ('add', 'replace');

CREATE TABLE episodes (
    run_id        integer          NOT NULL,
    episode_id    uuid             NOT NULL,
    employee_id   integer          NOT NULL,
    scenario_code text             NOT NULL,
    category      episode_category NOT NULL,
    started_at    timestamptz      NOT NULL,
    ended_at      timestamptz      NOT NULL,
    injection     injection_mode   NOT NULL,
    PRIMARY KEY (run_id, episode_id),
    CONSTRAINT episodes_janela_coerente CHECK (ended_at >= started_at)
);

COMMENT ON TABLE episodes IS 'Um episodio e a unidade de deteccao dos cenarios de contexto e longitudinais, pela D-12. O cenario pontual tambem vira episodio, de um evento so, para a metrica ter o mesmo denominador.';

-- Somente eventos que pertencem a algum episodio. Evento ausente daqui e
-- normal: gravar 2 milhoes de linhas dizendo "normal" nao acrescenta nada.
CREATE TABLE labels (
    run_id     integer    NOT NULL,
    event_id   uuid       NOT NULL,
    episode_id uuid       NOT NULL,
    label      label_kind NOT NULL,
    PRIMARY KEY (run_id, event_id),
    FOREIGN KEY (run_id, episode_id) REFERENCES episodes (run_id, episode_id)
);

COMMENT ON COLUMN labels.label IS 'So suspicious conta como positivo na metrica. legitimate_deviation existe para medir o falso positivo da D2 e da D3.';

-- Nao existe chave estrangeira de labels.event_id para corp.events: sao bancos
-- diferentes, e o PostgreSQL nao atravessa banco. E o preco da trava de
-- CONNECT, e e cobrado em teste: o avaliador confere que todo rotulo aponta
-- para um evento existente, e que nenhum episodio ficou sem rotulo.
