import csv
import os
from random import choice

from faker import Faker


PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA_SCRIPT, "testes")
ARQUIVO_ENDERECOS = os.path.join(PASTA_SAIDA, "addresses.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "clients.csv")

fake = Faker("pt_BR")


def carregar_ids_enderecos() -> list[str]:
    with open(ARQUIVO_ENDERECOS, newline="", encoding="utf-8-sig") as arquivo:
        return [linha["id"] for linha in csv.DictReader(arquivo)]


def criar_csv_clientes() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    ids_enderecos = carregar_ids_enderecos()

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=["id", "nome", "cnpj", "id_endereço", "ativo"],
        )
        escritor.writeheader()

        for cliente_id, endereco_id in enumerate(ids_enderecos, start=1):
            escritor.writerow(
                {
                    "id": cliente_id,
                    "nome": fake.company(),
                    "cnpj": fake.unique.cnpj(),
                    "id_endereço": endereco_id,
                    "ativo": choice([True, False]),
                }
            )

    print(f"Arquivo criado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    criar_csv_clientes()
