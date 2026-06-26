import csv
import os
from datetime import date, timedelta
from random import choice, randint


QUANTIDADE_PEDIDOS = 10000
DATA_INICIAL = date(2025, 1, 1)
DATA_FINAL = date.today()
PRAZO_ENTREGA_DIAS = 3
VALOR_MINIMO_CENTAVOS = 20_000
VALOR_MAXIMO_CENTAVOS = 500_000
FIELDNAMES = ["id", "cliente_id", "data_pedido", "prazo_entrega", "valor"]

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA_SCRIPT, "testes")
ARQUIVO_CLIENTES = os.path.join(PASTA_SAIDA, "clients.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "orders.csv")


def carregar_ids_clientes() -> list[str]:
    with open(ARQUIVO_CLIENTES, newline="", encoding="utf-8-sig") as arquivo:
        return [linha["id"] for linha in csv.DictReader(arquivo)]


def arquivo_tem_dados(caminho: str) -> bool:
    return os.path.exists(caminho) and os.path.getsize(caminho) > 0


def obter_proximo_id(caminho: str) -> int:
    if not arquivo_tem_dados(caminho):
        return 1

    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        ids = [
            int(linha["id"])
            for linha in csv.DictReader(arquivo)
            if linha.get("id", "").isdigit()
        ]

    return max(ids, default=0) + 1


def listar_datas_validas() -> list[date]:
    quantidade_dias = (DATA_FINAL - DATA_INICIAL).days
    datas = [DATA_INICIAL + timedelta(days=dia) for dia in range(quantidade_dias + 1)]
    return [data_pedido for data_pedido in datas if data_pedido.weekday() != 6]


def criar_csv_pedidos() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    ids_clientes = carregar_ids_clientes()
    datas_validas = listar_datas_validas()
    proximo_id = obter_proximo_id(ARQUIVO_SAIDA)
    escrever_cabecalho = not arquivo_tem_dados(ARQUIVO_SAIDA)

    if not ids_clientes:
        raise ValueError("Nenhum cliente encontrado no arquivo clients.csv.")

    if not datas_validas:
        raise ValueError("Não existem datas válidas para gerar pedidos.")

    with open(ARQUIVO_SAIDA, "a", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=FIELDNAMES)
        if escrever_cabecalho:
            escritor.writeheader()

        for pedido_id in range(proximo_id, proximo_id + QUANTIDADE_PEDIDOS):
            data_pedido = choice(datas_validas)
            prazo_entrega = data_pedido + timedelta(days=PRAZO_ENTREGA_DIAS)
            valor_centavos = randint(VALOR_MINIMO_CENTAVOS, VALOR_MAXIMO_CENTAVOS)

            escritor.writerow(
                {
                    "id": pedido_id,
                    "cliente_id": choice(ids_clientes),
                    "data_pedido": data_pedido.isoformat(),
                    "prazo_entrega": prazo_entrega.isoformat(),
                    "valor": f"{valor_centavos / 100:.2f}",
                }
            )

    print(f"Arquivo criado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    criar_csv_pedidos()
