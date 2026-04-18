BEGIN;

INSERT INTO regioes (nome)
VALUES
    ('Maceió'),
    ('Arapiraca'),
    ('Palmeira dos Índios'),
    ('Rio Largo'),
    ('União dos Palmares');

INSERT INTO motoristas (nome)
VALUES
    ('Carlos Henrique'),
    ('João Pedro'),
    ('Marcos Vinícius'),
    ('Rafael Silva'),
    ('André Luiz'),
    ('Felipe Santos'),
    ('Gustavo Almeida'),
    ('Bruno Oliveira');

INSERT INTO veiculos (placa, modelo, capacidade_kg)
VALUES
    ('QXA1A10', 'Fiat Fiorino', 650.00),
    ('QXB2B20', 'Renault Master', 1500.00),
    ('QXC3C30', 'Hyundai HR', 1800.00),
    ('QXD4D40', 'Volkswagen Delivery', 2500.00),
    ('QXE5E50', 'Mercedes Sprinter', 1700.00);

-- INSERT INTO entregas (
--     pedido_codigo,
--     regiao_id,
--     motorista_id,
--     veiculo_id,
--     data_pedido,
--     data_saida,
--     prazo_entrega,
--     data_entrega,
--     km_rodado,
--     custo_entrega,
--     quantidade_itens,
--     peso_carga_kg,
--     status_entrega
-- )
-- SELECT
--     'PED' || LPAD(gs::TEXT, 6, '0') AS pedido_codigo,
--     (1 + FLOOR(RANDOM() * 5))::BIGINT AS regiao_id,
--     (1 + FLOOR(RANDOM() * 8))::BIGINT AS motorista_id,
--     (1 + FLOOR(RANDOM() * 5))::BIGINT AS veiculo_id,

--     dt_pedido AS data_pedido,
--     dt_saida AS data_saida,
--     dt_prazo AS prazo_entrega,
--     dt_entrega AS data_entrega,

--     km_rodado,
--     ROUND((km_rodado * (1.8 + RANDOM() * 1.7) + (5 + RANDOM() * 20))::NUMERIC, 2) AS custo_entrega,
--     (1 + FLOOR(RANDOM() * 20))::INTEGER AS quantidade_itens,
--     ROUND((20 + RANDOM() * 780)::NUMERIC, 2) AS peso_carga_kg,

--     CASE
--         WHEN dt_entrega <= dt_prazo THEN 'ENTREGUE_NO_PRAZO'
--         ELSE 'ENTREGUE_COM_ATRASO'
--     END AS status_entrega
-- FROM (
--     SELECT
--         gs,
--         (
--             TIMESTAMP '2024-01-01 08:00:00'
--             + ((FLOOR(RANDOM() * 90))::TEXT || ' days')::INTERVAL
--             + ((FLOOR(RANDOM() * 10))::TEXT || ' hours')::INTERVAL
--             + ((FLOOR(RANDOM() * 60))::TEXT || ' minutes')::INTERVAL
--         ) AS dt_pedido,

--         ROUND((5 + RANDOM() * 55)::NUMERIC, 2) AS km_rodado
--     FROM generate_series(1, 300) AS gs
-- ) base
-- CROSS JOIN LATERAL (
--     SELECT
--         base.dt_pedido + ((1 + FLOOR(RANDOM() * 6))::TEXT || ' hours')::INTERVAL AS dt_saida
-- ) s1
-- CROSS JOIN LATERAL (
--     SELECT
--         s1.dt_saida + ((4 + FLOOR(RANDOM() * 48))::TEXT || ' hours')::INTERVAL AS dt_prazo
-- ) s2
-- CROSS JOIN LATERAL (
--     SELECT
--         CASE
--             WHEN RANDOM() < 0.78 THEN
--                 s2.dt_prazo - ((FLOOR(RANDOM() * 5))::TEXT || ' hours')::INTERVAL
--             ELSE
--                 s2.dt_prazo + ((1 + FLOOR(RANDOM() * 24))::TEXT || ' hours')::INTERVAL
--         END AS dt_entrega
-- ) s3
-- CROSS JOIN LATERAL (
--     SELECT
--         base.dt_pedido,
--         s1.dt_saida,
--         s2.dt_prazo,
--         s3.dt_entrega,
--         base.km_rodado
-- ) final_data;

COMMIT;