from random import randint, choice
from datetime import datetime, timedelta

from faker import Faker
import psycopg

fake = Faker("pt_BR")

conn = psycopg.connect(
    host="localhost",
    dbname="sige",
    user="admin",
    password="admin"
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