BEGIN;

DROP TABLE IF EXISTS entregas CASCADE;
DROP TABLE IF EXISTS motoristas CASCADE;
DROP TABLE IF EXISTS veiculos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

CREATE TABLE clientes (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    cidade VARCHAR(150) NOT NULL,,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
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
    cliente_id BIGINT NOT NULL REFERENCES clientes(id),
    motorista_id BIGINT NOT NULL REFERENCES motoristas(id),
    veiculo_id BIGINT NOT NULL REFERENCES veiculos(id),

    data_pedido TIMESTAMP NOT NULL,
    data_saida TIMESTAMP NOT NULL,
    prazo_entrega TIMESTAMP NOT NULL,
    data_entrega TIMESTAMP NOT NULL,

    km_inicial NUMERIC(10,2) NOT NULL CHECK (km_inicial >= 0),
    km_final NUMERIC(10,2) NOT NULL CHECK (km_final > km_inicial),
    custo_entrega NUMERIC(10,2) NOT NULL CHECK (custo_entrega >= 0),
    quantidade_itens INTEGER NOT NULL CHECK (quantidade_itens > 0),
    peso_carga_kg NUMERIC(10,2) NOT NULL CHECK (peso_carga_kg > 0),
);

CREATE INDEX idx_entregas_data_pedido ON entregas(data_pedido);
CREATE INDEX idx_entregas_data_entrega ON entregas(data_entrega);
CREATE INDEX idx_entregas_cliente_id ON entregas(cliente_id);
CREATE INDEX idx_entregas_motorista_id ON entregas(motorista_id);
CREATE INDEX idx_entregas_veiculo_id ON entregas(veiculo_id);
CREATE INDEX idx_entregas_km_inicial ON entregas(km_inicial);
CREATE INDEX idx_entregas_km_final ON entregas(km_final);

CREATE INDEX idx_clientes_nome ON clientes(nome);
CREATE INDEX idx_clientes_cnpj ON clientes(cnpj);
CREATE INDEX idx_clientes_regiao_id ON clientes(regiao_id);

COMMIT;