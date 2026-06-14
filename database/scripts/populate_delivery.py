import csv
import os
from datetime import datetime, timedelta
from random import choices, randint


PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA_SCRIPT, "testes")
ARQUIVO_PEDIDOS = os.path.join(PASTA_SAIDA, "orders.csv")
ARQUIVO_MOTORISTAS = os.path.join(PASTA_SAIDA, "drivers.csv")
ARQUIVO_VEICULOS = os.path.join(PASTA_SAIDA, "vehicles.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "deliveries.csv")

STATUS_ENTREGA = ["entregue", "atrasada", "em andamento"]
PESOS_STATUS = [70, 20, 10]


def carregar_csv(caminho: str) -> list[dict[str, str]]:
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


def calcular_data_entrega(
    data_pedido: datetime,
    prazo_entrega: datetime,
    status: str,
) -> datetime:
    if status == "entregue":
        horas_ate_prazo = int((prazo_entrega - data_pedido).total_seconds() // 3600)
        return data_pedido + timedelta(hours=randint(1, horas_ate_prazo))

    if status == "atrasada":
        return prazo_entrega + timedelta(hours=randint(1, 72))

    agora = datetime.now().replace(microsecond=0)
    return max(agora, prazo_entrega)


def criar_csv_entregas() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    pedidos = carregar_csv(ARQUIVO_PEDIDOS)
    pedidos.sort(key=lambda pedido: pedido["data_pedido"])

    motoristas_ativos = [
        motorista for motorista in carregar_csv(ARQUIVO_MOTORISTAS)
        if motorista["ativo"].lower() == "true"
    ]
    veiculos_ativos = [
        veiculo for veiculo in carregar_csv(ARQUIVO_VEICULOS)
        if veiculo["ativo"].lower() == "true"
    ]

    if not pedidos or not motoristas_ativos or not veiculos_ativos:
        raise ValueError("São necessários pedidos, motoristas ativos e veículos ativos.")

    ultimo_hodometro = {
        veiculo["id"]: int(veiculo["hodometro"]) for veiculo in veiculos_ativos
    }

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=[
                "id",
                "pedido_id",
                "motorista_id",
                "veículo_id",
                "data_entrega",
                "ano",
                "mês",
                "status",
                "custo",
                "hodometro_inicial",
                "hodometro_final",
            ],
        )
        escritor.writeheader()

        for entrega_id, pedido in enumerate(pedidos, start=1):
            motorista = choices(motoristas_ativos, k=1)[0]
            veiculo = choices(veiculos_ativos, k=1)[0]
            status = choices(STATUS_ENTREGA, weights=PESOS_STATUS, k=1)[0]

            data_pedido = datetime.fromisoformat(pedido["data_pedido"])
            prazo_entrega = datetime.fromisoformat(pedido["prazo_entrega"])
            data_entrega = calcular_data_entrega(data_pedido, prazo_entrega, status)

            hodometro_inicial = ultimo_hodometro[veiculo["id"]]
            hodometro_final = hodometro_inicial + randint(5, 300)
            ultimo_hodometro[veiculo["id"]] = hodometro_final

            custo_centavos = randint(5_000, 150_000)

            escritor.writerow(
                {
                    "id": entrega_id,
                    "pedido_id": pedido["id"],
                    "motorista_id": motorista["id"],
                    "veículo_id": veiculo["id"],
                    "data_entrega": data_entrega.isoformat(sep=" "),
                    "ano": data_entrega.year,
                    "mês": data_entrega.month,
                    "status": status,
                    "custo": f"{custo_centavos / 100:.2f}",
                    "hodometro_inicial": hodometro_inicial,
                    "hodometro_final": hodometro_final,
                }
            )

    print(f"Arquivo criado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    criar_csv_entregas()
