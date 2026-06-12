BEGIN;

DROP TABLE IF EXISTS entrega CASCADE;
DROP TABLE IF EXISTS pedido CASCADE;
DROP TABLE IF EXISTS rota CASCADE;
DROP TABLE IF EXISTS cliente CASCADE;
DROP TABLE IF EXISTS motorista CASCADE;
DROP TABLE IF EXISTS veiculo CASCADE;
DROP TABLE IF EXISTS regiao CASCADE;

CREATE TABLE regiao (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE cliente (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cnpj VARCHAR(20) UNIQUE,
    regiao_id BIGINT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_cliente_regiao
        FOREIGN KEY (regiao_id)
        REFERENCES regiao(id)
);

CREATE TABLE motorista (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE veiculo (
    id BIGSERIAL PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,
    capacidade_kg NUMERIC(10,2) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT ck_veiculo_capacidade
        CHECK (capacidade_kg > 0)
);

CREATE TABLE rota (
    id BIGSERIAL PRIMARY KEY,
    regiao_id BIGINT NOT NULL,
    distancia_km NUMERIC(10,2) NOT NULL,
    descricao TEXT,

    CONSTRAINT fk_rota_regiao
        FOREIGN KEY (regiao_id)
        REFERENCES regiao(id),

    CONSTRAINT ck_rota_distancia
        CHECK (distancia_km > 0)
);

CREATE TABLE pedido (
    id BIGSERIAL PRIMARY KEY,
    cliente_id BIGINT NOT NULL,
    data_pedido TIMESTAMP NOT NULL,
    prazo_entrega TIMESTAMP NOT NULL,
    valor NUMERIC(12,2) NOT NULL,

    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES cliente(id),

    CONSTRAINT ck_pedido_valor
        CHECK (valor >= 0),

    CONSTRAINT ck_pedido_prazo
        CHECK (prazo_entrega >= data_pedido)
);

CREATE TABLE entrega (
    id BIGSERIAL PRIMARY KEY,

    pedido_id BIGINT NOT NULL,
    motorista_id BIGINT NOT NULL,
    veiculo_id BIGINT NOT NULL,
    rota_id BIGINT NOT NULL,

    data_saida TIMESTAMP NOT NULL,
    data_entrega TIMESTAMP NOT NULL,

    status VARCHAR(20) NOT NULL,

    custo NUMERIC(12,2) NOT NULL,
    distancia_km NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_entrega_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedido(id),

    CONSTRAINT fk_entrega_motorista
        FOREIGN KEY (motorista_id)
        REFERENCES motorista(id),

    CONSTRAINT fk_entrega_veiculo
        FOREIGN KEY (veiculo_id)
        REFERENCES veiculo(id),

    CONSTRAINT fk_entrega_rota
        FOREIGN KEY (rota_id)
        REFERENCES rota(id),

    CONSTRAINT uq_entrega_pedido
        UNIQUE (pedido_id),

    CONSTRAINT ck_entrega_datas
        CHECK (data_entrega >= data_saida),

    CONSTRAINT ck_entrega_custo
        CHECK (custo >= 0),

    CONSTRAINT ck_entrega_distancia
        CHECK (distancia_km >= 0),

    CONSTRAINT ck_entrega_status
        CHECK (
            status IN (
                'CONCLUIDA',
                'ATRASADA'
            )
        )
);

CREATE INDEX idx_cliente_regiao
    ON cliente(regiao_id);

CREATE INDEX idx_rota_regiao
    ON rota(regiao_id);

CREATE INDEX idx_pedido_cliente
    ON pedido(cliente_id);

CREATE INDEX idx_pedido_data
    ON pedido(data_pedido);

CREATE INDEX idx_entrega_motorista
    ON entrega(motorista_id);

CREATE INDEX idx_entrega_veiculo
    ON entrega(veiculo_id);

CREATE INDEX idx_entrega_rota
    ON entrega(rota_id);

CREATE INDEX idx_entrega_saida
    ON entrega(data_saida);

CREATE INDEX idx_entrega_data_entrega
    ON entrega(data_entrega);

CREATE INDEX idx_entrega_status
    ON entrega(status);

COMMIT;