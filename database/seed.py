from pathlib import Path
import psycopg

FILES = [
    Path("./ddl.sql"),
    Path("./dml.sql"),
]

conn_info = {
    "host": "localhost",
    "port": 5433,
    "dbname": "sige",
    "user": "sige",
    "password": "sige",
}

try:
    with psycopg.connect(**conn_info) as conn:
        with conn.cursor() as cur:
            for file_path in FILES:
                print(f"Executando: {file_path}")
                sql = file_path.read_text(encoding="utf-8")
                cur.execute(sql)

        conn.commit()

    print("Banco populado com sucesso.")

except Exception as e:
    print(f"Erro ao executar scripts SQL: {e}")
