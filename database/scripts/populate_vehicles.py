import csv
import os
from random import choice, randint

from faker import Faker


QUANTIDADE_VEICULOS = 50
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA_SCRIPT, "testes")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "vehicles.csv")

MODELOS_CAPACIDADES = {
    "Fiat Fiorino": (500, 700),
    "Renault Master": (1200, 1800),
    "Mercedes-Benz Sprinter": (1400, 2000),
    "Volkswagen Delivery": (2500, 6000),
    "Iveco Daily": (1500, 3500),
    "Ford Transit": (1200, 2000),
}

fake = Faker("pt_BR")


def criar_csv_veiculos() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    placas_geradas = set()

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=[
                "id",
                "placa",
                "modelo",
                "ano",
                "capacidade_kg",
                "hodometro",
                "ativo",
            ],
        )
        escritor.writeheader()

        for veiculo_id in range(1, QUANTIDADE_VEICULOS + 1):
            placa = fake.unique.license_plate()
            while placa in placas_geradas:
                placa = fake.unique.license_plate()
            placas_geradas.add(placa)

            modelo = choice(list(MODELOS_CAPACIDADES))
            capacidade_minima, capacidade_maxima = MODELOS_CAPACIDADES[modelo]

            escritor.writerow(
                {
                    "id": veiculo_id,
                    "placa": placa,
                    "modelo": modelo,
                    "ano": randint(2010, 2026),
                    "capacidade_kg": randint(capacidade_minima, capacidade_maxima),
                    "hodometro": randint(0, 500_000),
                    "ativo": choice([True, False]),
                }
            )

    print(f"Arquivo criado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    criar_csv_veiculos()
