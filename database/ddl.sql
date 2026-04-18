BEGIN;

DROP TABLE IF EXISTS entregas CASCADE;
DROP TABLE IF EXISTS motoristas CASCADE;
DROP TABLE IF EXISTS veiculos CASCADE;
DROP TABLE IF EXISTS regioes CASCADE;

CREATE TABLE regioes (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE motoristas (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE veiculos (
    id BIGSERIAL PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(80) NOT NULL,
    capacidade_kg NUMERIC(10,2) NOT NULL CHECK (capacidade_kg > 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE entregas (
    id BIGSERIAL PRIMARY KEY,
    pedido_codigo VARCHAR(30) NOT NULL UNIQUE,
    regiao_id BIGINT NOT NULL REFERENCES regioes(id),
    motorista_id BIGINT NOT NULL REFERENCES motoristas(id),
    veiculo_id BIGINT NOT NULL REFERENCES veiculos(id),

    data_pedido TIMESTAMP NOT NULL,
    data_saida TIMESTAMP NOT NULL,
    prazo_entrega TIMESTAMP NOT NULL,
    data_entrega TIMESTAMP NOT NULL,

    km_rodado NUMERIC(10,2) NOT NULL CHECK (km_rodado >= 0),
    custo_entrega NUMERIC(10,2) NOT NULL CHECK (custo_entrega >= 0),
    quantidade_itens INTEGER NOT NULL CHECK (quantidade_itens > 0),
    peso_carga_kg NUMERIC(10,2) NOT NULL CHECK (peso_carga_kg > 0),

    status_entrega VARCHAR(20) NOT NULL CHECK (
        status_entrega IN ('ENTREGUE_NO_PRAZO', 'ENTREGUE_COM_ATRASO')
    )
);

CREATE INDEX idx_entregas_data_pedido ON entregas(data_pedido);
CREATE INDEX idx_entregas_data_entrega ON entregas(data_entrega);
CREATE INDEX idx_entregas_regiao_id ON entregas(regiao_id);
CREATE INDEX idx_entregas_motorista_id ON entregas(motorista_id);
CREATE INDEX idx_entregas_veiculo_id ON entregas(veiculo_id);

COMMIT;