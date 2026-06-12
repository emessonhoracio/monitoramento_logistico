Agora você está entrando na etapa de **seeding** do banco.

Como o objetivo é alimentar um dashboard Power BI, eu não recomendo inserir registros totalmente aleatórios. O ideal é gerar dados **consistentes entre si**, para que os KPIs façam sentido.

Minha sugestão é criar um script Python que:

1. Popule as tabelas de referência:

   * `regiao`
   * `motorista`
   * `veiculo`
   * `cliente`
   * `rota`

2. Gere:

   * centenas de `pedido`
   * centenas de `entrega`

3. Respeite os relacionamentos e regras do domínio.

---

# Estrutura sugerida

Primeiro insira os dados "mestres":

## Regiões

```sql
INSERT INTO regiao (nome)
VALUES
('Maceió'),
('Arapiraca'),
('Rio Largo'),
('Palmeira dos Índios'),
('União dos Palmares');
```

---

## Motoristas

```sql
INSERT INTO motorista (nome)
VALUES
('Carlos Henrique'),
('João Pedro'),
('Rafael Silva'),
('André Luiz'),
('Felipe Santos'),
('Bruno Oliveira');
```

---

## Veículos

```sql
INSERT INTO veiculo (
    placa,
    modelo,
    capacidade_kg
)
VALUES
('QXA1A10', 'Fiorino', 650),
('QXB2B20', 'Master', 1500),
('QXC3C30', 'Sprinter', 1700),
('QXD4D40', 'Delivery', 2500);
```

---

# Depois gere os dados automaticamente

Instale:

```bash
pip install psycopg faker python-dotenv
```

---

## Exemplo simples

```python
from random import randint, choice
from datetime import datetime, timedelta

from faker import Faker
import psycopg

fake = Faker("pt_BR")

conn = psycopg.connect(
    host="localhost",
    dbname="logistica",
    user="postgres",
    password="postgres"
)

with conn.cursor() as cur:

    # clientes
    for _ in range(50):
        cur.execute(
            """
            INSERT INTO cliente (
                nome,
                cnpj,
                regiao_id,
                ativo
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                fake.company(),
                fake.cnpj(),
                randint(1, 5),
                True
            )
        )

conn.commit()
```

---

# Gerando pedidos

```python
for _ in range(500):

    data_pedido = fake.date_time_between(
        start_date="-6M",
        end_date="now"
    )

    prazo = data_pedido + timedelta(
        days=randint(1, 5)
    )

    valor = randint(100, 5000)

    cliente_id = randint(1, 50)

    cur.execute(
        """
        INSERT INTO pedido (
            cliente_id,
            data_pedido,
            prazo_entrega,
            valor
        )
        VALUES (%s,%s,%s,%s)
        """,
        (
            cliente_id,
            data_pedido,
            prazo,
            valor
        )
    )
```

---

# Gerando entregas

Aqui é onde os KPIs nascem.

```python
pedido_id = ...

data_saida = data_pedido + timedelta(
    hours=randint(1, 24)
)

atrasada = randint(1,100) <= 20
```

---

### 80% no prazo

```python
if not atrasada:

    data_entrega = prazo - timedelta(
        hours=randint(1,12)
    )

    status = "CONCLUIDA"

else:

    data_entrega = prazo + timedelta(
        hours=randint(1,48)
    )

    status = "ATRASADA"
```

---

### custo

```python
distancia = randint(5,60)

custo = round(
    distancia * 2.5
    + randint(5,20),
    2
)
```

---

### inserir

```python
cur.execute(
    """
    INSERT INTO entrega (
        pedido_id,
        motorista_id,
        veiculo_id,
        rota_id,
        data_saida,
        data_entrega,
        status,
        custo,
        distancia_km
    )
    VALUES (
        %s,%s,%s,%s,
        %s,%s,%s,%s,%s
    )
    """,
    (
        pedido_id,
        randint(1,6),
        randint(1,4),
        randint(1,10),
        data_saida,
        data_entrega,
        status,
        custo,
        distancia
    )
)
```

---

# Resultado esperado

Se você gerar:

| Tabela    | Quantidade |
| --------- | ---------- |
| Região    | 5          |
| Motorista | 6          |
| Veículo   | 4          |
| Cliente   | 50         |
| Rota      | 20         |
| Pedido    | 500        |
| Entrega   | 500        |

já terá dados suficientes para:

* Tempo médio de entrega
* % de entregas no prazo
* Tempo médio de atraso
* Entregas por região
* Entregas por motorista
* Entregas por veículo
* Custo médio
* Custo por km
* Produtividade

e montar um dashboard convincente no Power BI.

Eu inclusive sugiro gerar **entre 500 e 1000 entregas**, porque os gráficos ficam muito mais interessantes visualmente do que com apenas 50 ou 100 registros.
