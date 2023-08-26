CREATE TABLE users
(
    id         INTEGER                     NOT NULL UNIQUE PRIMARY KEY,
    is_blocked BOOLEAN                     NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NULL
);

CREATE TABLE chats
(
    id         VARCHAR(255)                NOT NULL UNIQUE PRIMARY KEY,
    user_id    INTEGER                     NOT NULL,
    data       jsonb                       NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NULL,

    FOREIGN KEY (user_id) REFERENCES users (id)
);
CREATE SEQUENCE users_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE users_id_seq OWNED BY users.id;
ALTER TABLE ONLY users
    ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

CREATE TABLE operation_categories
(
    id             INTEGER                     NOT NULL UNIQUE PRIMARY KEY,
    user_id        INTEGER                     NOT NULL,
    name           VARCHAR(255)                NOT NULL,
    is_active      BOOLEAN                     NOT NULL DEFAULT TRUE,
    operation_type SMALLINT                    NOT NULL,
    created_at     TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at     TIMESTAMP WITHOUT TIME ZONE NULL,

    FOREIGN KEY (user_id) REFERENCES users (id)
);
CREATE SEQUENCE operation_categories_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE operation_categories_id_seq OWNED BY operation_categories.id;
ALTER TABLE ONLY operation_categories
    ALTER COLUMN id SET DEFAULT nextval('operation_categories_id_seq'::regclass);

CREATE TABLE operations
(
    id          INTEGER                     NOT NULL UNIQUE PRIMARY KEY,
    user_id     INTEGER                     NOT NULL,
    category_id INTEGER                     NULL,
    status      SMALLINT                    NOT NULL DEFAULT 0,
    type        SMALLINT                    NULL,
    amount      DOUBLE PRECISION            NOT NULL,
    comment     TEXT                        NULL,
    created_at  TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at  TIMESTAMP WITHOUT TIME ZONE NULL,

    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (category_id) REFERENCES operation_categories (id)
);
CREATE SEQUENCE operations_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE operations_id_seq OWNED BY operations.id;
ALTER TABLE ONLY operations
    ALTER COLUMN id SET DEFAULT nextval('operations_id_seq'::regclass);


