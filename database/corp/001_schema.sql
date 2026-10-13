-- Banco `corp` — a corporacao simulada, SEM rotulo nenhum
--
--     psql -d corp -v ON_ERROR_STOP=1 -f database/corp/001_schema.sql
--
-- Fonte: docs/banco-simulado.md. Esta e a unica lista de tabelas do projeto;
-- duas listas em dois arquivos viram dois schemas na primeira alteracao.

-- ---------------------------------------------------------------------------
-- Listas fechadas (secao 6 da especificacao)
--
-- Valor de lista fechada vira tipo, nao texto livre: o gerador nao inventa
-- valor e a regra nao erra calada. tests/test_schema.py compara estes tipos
-- com a tabela da especificacao e reprova se os dois divergirem.
-- ---------------------------------------------------------------------------

CREATE TYPE event_type AS ENUM (
    'LOGIN',
    'LOGOUT',
    'FILE_ACCESS',
    'FILE_DOWNLOAD',
    'EXTERNAL_DEVICE',
    'WEB_BROWSING',
    'SYSTEM_CONFIG',
    'PHISHING_SIM'
);

CREATE TYPE event_result AS ENUM ('success', 'failure', 'blocked');

CREATE TYPE sensitivity_level AS ENUM (
    'public',
    'internal',
    'confidential',
    'restricted'
);

CREATE TYPE network_kind AS ENUM ('office', 'vpn', 'home', 'external');

-- As seis personas da D-38, em identificador ingles:
--   office_daytime  administrativo diurno   shift         operacao em turno
--   it_privileged   TI privilegiado         sales_travel  comercial viajante
--   hybrid          hibrido (engenharia)    management    gestao e diretoria
CREATE TYPE persona AS ENUM (
    'office_daytime',
    'shift',
    'it_privileged',
    'sales_travel',
    'hybrid',
    'management'
);

CREATE TYPE device_kind AS ENUM ('notebook', 'mobile');
CREATE TYPE device_ownership AS ENUM ('corporate', 'personal');
CREATE TYPE privilege_level AS ENUM ('standard', 'elevated', 'admin');
CREATE TYPE resource_kind AS ENUM ('system', 'file_share');
CREATE TYPE hr_event_kind AS ENUM ('vacation', 'leave', 'role_change');

-- ---------------------------------------------------------------------------
-- Execucoes de geracao
--
-- Uma linha por semente. O `params_hash` e o `generator_sha` sao o que torna
-- a execucao refeita identica — exigencia da secao 3.7 da Metodologia.
-- ---------------------------------------------------------------------------

CREATE TABLE runs (
    run_id         integer     PRIMARY KEY,
    seed           bigint      NOT NULL,
    generator_sha  text        NOT NULL,
    params_hash    text        NOT NULL,
    started_at     timestamptz NOT NULL DEFAULT now(),
    finished_at    timestamptz,
    event_count    bigint,
    notes          text,
    CONSTRAINT runs_janela_coerente CHECK (finished_at IS NULL OR finished_at >= started_at)
);

COMMENT ON TABLE runs IS 'Uma execucao do gerador. O run_id e escolhido por quem gera, nao sorteado, porque nomeia a particao de eventos.';

-- ---------------------------------------------------------------------------
-- Catalogo da organizacao (D-37, D-39 e D-40)
--
-- Sem run_id: departamentos, cargos, sistemas e faixas de rede sao fixados por
-- decisao e valem igual em toda semente. O que varia por semente e quem esta
-- em qual persona e o comportamento de cada um.
-- ---------------------------------------------------------------------------

CREATE TABLE departments (
    department_id smallint PRIMARY KEY,
    name          text     NOT NULL UNIQUE,
    headcount     smallint NOT NULL CHECK (headcount > 0)
);

CREATE TABLE positions (
    position_id smallint        PRIMARY KEY,
    title       text            NOT NULL UNIQUE,
    privilege   privilege_level NOT NULL
);

CREATE TABLE sites (
    site_id  smallint PRIMARY KEY,
    name     text     NOT NULL UNIQUE,
    timezone text     NOT NULL
);

COMMENT ON COLUMN sites.timezone IS 'Nome IANA, ex.: America/Sao_Paulo. A D-40 define duas sedes em fusos diferentes, e e isso que separa a C0 (fuso da sede) da D1 (fuso do funcionario).';

CREATE TABLE resources (
    resource_id   smallint          PRIMARY KEY,
    kind          resource_kind     NOT NULL,
    name          text              NOT NULL UNIQUE,
    sensitivity   sensitivity_level NOT NULL,
    owner_dept_id smallint          REFERENCES departments
);

-- A matriz cargo x sistema da D-39. Sem ela, "acesso incomum" nao tem
-- definicao: e esta tabela que diz quem tinha permissao.
CREATE TABLE resource_access (
    resource_id   smallint NOT NULL REFERENCES resources,
    department_id smallint NOT NULL REFERENCES departments,
    PRIMARY KEY (resource_id, department_id)
);

CREATE TABLE network_ranges (
    range_id smallint     PRIMARY KEY,
    cidr     cidr         NOT NULL,
    kind     network_kind NOT NULL,
    country  text         NOT NULL,
    city     text         NOT NULL
);

COMMENT ON TABLE network_ranges IS 'So faixas reservadas: privadas (RFC 1918) para dentro, documentacao (RFC 5737, RFC 3849) para fora. Repositorio publico nao cita IP de organizacao real. Pais e cidade sao ficticios e saem daqui, nunca de servico de GeoIP.';

-- ---------------------------------------------------------------------------
-- Pessoas, maquinas e sessoes — por semente
-- ---------------------------------------------------------------------------

CREATE TABLE employees (
    run_id        integer         NOT NULL REFERENCES runs,
    employee_id   integer         NOT NULL,
    department_id smallint        NOT NULL REFERENCES departments,
    position_id   smallint        NOT NULL REFERENCES positions,
    site_id       smallint        NOT NULL REFERENCES sites,
    manager_id    integer,
    persona       persona         NOT NULL,
    privilege     privilege_level NOT NULL,
    hired_on      date            NOT NULL,
    PRIMARY KEY (run_id, employee_id),
    FOREIGN KEY (run_id, manager_id) REFERENCES employees (run_id, employee_id)
);

CREATE TABLE devices (
    run_id      integer          NOT NULL,
    device_id   integer          NOT NULL,
    employee_id integer          NOT NULL,
    kind        device_kind      NOT NULL,
    ownership   device_ownership NOT NULL,
    PRIMARY KEY (run_id, device_id),
    FOREIGN KEY (run_id, employee_id) REFERENCES employees (run_id, employee_id)
);

CREATE TABLE sessions (
    run_id      integer     NOT NULL,
    session_id  uuid        NOT NULL,
    employee_id integer     NOT NULL,
    device_id   integer     NOT NULL,
    started_at  timestamptz NOT NULL,
    ended_at    timestamptz,
    is_vpn      boolean     NOT NULL,
    PRIMARY KEY (run_id, session_id),
    FOREIGN KEY (run_id, employee_id) REFERENCES employees (run_id, employee_id),
    FOREIGN KEY (run_id, device_id) REFERENCES devices (run_id, device_id),
    CONSTRAINT sessions_janela_coerente CHECK (ended_at IS NULL OR ended_at >= started_at)
);

-- Ferias, afastamento e mudanca de cargo. Fica em tabela propria porque se a
-- aplicacao pode ou nao ler isso e opcao do experimento, nao do schema.
CREATE TABLE hr_calendar (
    run_id      integer       NOT NULL,
    employee_id integer       NOT NULL,
    kind        hr_event_kind NOT NULL,
    starts_on   date          NOT NULL,
    ends_on     date,
    PRIMARY KEY (run_id, employee_id, kind, starts_on),
    FOREIGN KEY (run_id, employee_id) REFERENCES employees (run_id, employee_id),
    CONSTRAINT hr_calendar_janela_coerente CHECK (ends_on IS NULL OR ends_on >= starts_on)
);

-- ---------------------------------------------------------------------------
-- Estado, nao evento (D-30)
--
-- Higiene de seguranca que dura. Virar evento diario inflaria o volume sem
-- acrescentar informacao. As duas tabelas precisam ser lidas "como estavam
-- naquele dia", nunca no estado final — ler o estado final e a falha da D-17
-- por outro caminho.
-- ---------------------------------------------------------------------------

CREATE TABLE device_state_daily (
    run_id         integer NOT NULL,
    device_id      integer NOT NULL,
    state_date     date    NOT NULL,
    patch_age_days smallint NOT NULL CHECK (patch_age_days >= 0),
    antivirus_on   boolean NOT NULL,
    PRIMARY KEY (run_id, device_id, state_date),
    FOREIGN KEY (run_id, device_id) REFERENCES devices (run_id, device_id)
);

CREATE TABLE account_state (
    run_id      integer         NOT NULL,
    employee_id integer         NOT NULL,
    valid_from  timestamptz     NOT NULL,
    valid_to    timestamptz,
    mfa_enabled boolean         NOT NULL,
    privilege   privilege_level NOT NULL,
    PRIMARY KEY (run_id, employee_id, valid_from),
    FOREIGN KEY (run_id, employee_id) REFERENCES employees (run_id, employee_id),
    CONSTRAINT account_state_janela_coerente CHECK (valid_to IS NULL OR valid_to > valid_from)
);

-- ---------------------------------------------------------------------------
-- Eventos — o envelope da secao 2
-- ---------------------------------------------------------------------------

CREATE TABLE events (
    run_id      integer      NOT NULL,
    event_id    uuid         NOT NULL,
    employee_id integer      NOT NULL,
    occurred_at timestamptz  NOT NULL,
    ingested_at timestamptz  NOT NULL,
    event_type  event_type   NOT NULL,
    result      event_result NOT NULL,
    ip_address  inet         NOT NULL,
    device_id   integer      NOT NULL,
    session_id  uuid         NOT NULL,
    resource_id smallint     REFERENCES resources,
    is_vpn      boolean      NOT NULL,
    attributes  jsonb        NOT NULL,
    PRIMARY KEY (run_id, event_id),
    FOREIGN KEY (run_id, employee_id) REFERENCES employees (run_id, employee_id),
    FOREIGN KEY (run_id, device_id) REFERENCES devices (run_id, device_id),
    FOREIGN KEY (run_id, session_id) REFERENCES sessions (run_id, session_id),
    -- A sensibilidade e atributo do recurso e vale igual em todo tipo de
    -- evento. Repetida no jsonb, ela divergiria do catalogo na primeira
    -- alteracao — e foi exatamente o defeito que a especificacao corrigiu.
    CONSTRAINT events_sem_sensitivity_no_jsonb CHECK (NOT (attributes ? 'sensitivity')),
    CONSTRAINT events_attributes_e_objeto CHECK (jsonb_typeof(attributes) = 'object')
) PARTITION BY LIST (run_id);

COMMENT ON COLUMN events.ingested_at IS 'Latencia de engenharia, NUNCA metrica do TCC. Toda metrica temporal usa occurred_at.';

-- O formato de toda janela das dimensoes 2 e 3.
CREATE INDEX events_funcionario_tempo ON events (run_id, employee_id, occurred_at);

-- Nao existe particao DEFAULT de proposito: carga de semente sem particao
-- criada deve falhar alto, e nao cair num deposito onde ninguem procura.
-- Antes de cada carga:
--     CREATE TABLE events_run_7 PARTITION OF events FOR VALUES IN (7);
-- Para descartar uma semente depois de avaliada:
--     DROP TABLE events_run_7;
