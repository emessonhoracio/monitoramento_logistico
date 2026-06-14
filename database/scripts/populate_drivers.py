import csv
# from pathlib import Path
import os
from random import choice

from faker import Faker


QUANTIDADE_MOTORISTAS = 50
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA_SCRIPT, "testes")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "drivers.csv")

fake = Faker("pt_BR")


def criar_csv_motoristas() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=["id", "codigo motorista", "nome", "ativo"]
        )
        escritor.writeheader()
        for motorista_id in range(1, QUANTIDADE_MOTORISTAS + 1):
            # codigo_motorista = [0 for c in len(6-len(codigo_motorista))]
            codigo_motorista = str(motorista_id)
            escritor.writerow(
                {
                    "id": motorista_id,
                    "codigo motorista":codigo_motorista,
                    "nome": fake.name(),
                    "ativo": choice([True, False]),
                }
            )

    print(f"Arquivo criado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    criar_csv_motoristas()
