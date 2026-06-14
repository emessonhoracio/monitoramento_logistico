import csv
import os
from random import choice, randint

from faker import Faker


QUANTIDADE_ENDERECOS = 300
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA_SCRIPT, "testes")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "addresses.csv")

CIDADES_ALAGOAS = [
    "Arapiraca",
    "Atalaia",
    "Coruripe",
    "Delmiro Gouveia",
    "Maceió",
    "Maragogi",
    "Marechal Deodoro",
    "Palmeira dos Índios",
    "Penedo",
    "Pilar",
    "Porto Calvo",
    "Rio Largo",
    "Santana do Ipanema",
    "São Miguel dos Campos",
    "União dos Palmares",
]

fake = Faker("pt_BR")


def criar_csv_enderecos() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=["id", "rua", "cidade", "estado", "numero"],
        )
        escritor.writeheader()

        for endereco_id in range(1, QUANTIDADE_ENDERECOS + 1):
            escritor.writerow(
                {
                    "id": endereco_id,
                    "rua": fake.street_name(),
                    "cidade": choice(CIDADES_ALAGOAS),
                    "estado": "Alagoas",
                    "numero": randint(1, 9999),
                }
            )

    print(f"Arquivo criado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    criar_csv_enderecos()
