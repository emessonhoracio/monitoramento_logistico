import csv
import os
from datetime import date, datetime, timedelta
from random import choices, randint


PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA_SCRIPT, "testes")
ARQUIVO_PEDIDOS = os.path.join(PASTA_SAIDA, "orders.csv")
ARQUIVO_MOTORISTAS = os.path.join(PASTA_SAIDA, "drivers.csv")
ARQUIVO_VEICULOS = os.path.join(PASTA_SAIDA, "vehicles.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "deliveries.csv")

FIELDNAMES = [
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
]
STATUS_ENTREGA = ["entregue", "atrasada", "em andamento", "cancelado"]
PESOS_STATUS = [70, 20, 5, 5]
DIAS_PARA_CANCELAMENTO = 10


def carregar_csv(caminho: str) -> list[dict[str, str]]:
    if not os.path.exists(caminho) or os.path.getsize(caminho) == 0:
        return []

    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


def arquivo_tem_dados(caminho: str) -> bool:
    return os.path.exists(caminho) and os.path.getsize(caminho) > 0


def obter_proximo_id(linhas: list[dict[str, str]]) -> int:
    ids = [
        int(linha["id"])
        for linha in linhas
        if linha.get("id", "").isdigit()
    ]
    return max(ids, default=0) + 1


def carregar_ids_pedidos_com_entrega(entregas: list[dict[str, str]]) -> set[str]:
    return {
        entrega["pedido_id"]
        for entrega in entregas
        if entrega.get("pedido_id")
    }


def carregar_ultimo_hodometro(
    veiculos_ativos: list[dict[str, str]],
    entregas: list[dict[str, str]],
) -> dict[str, int]:
    ultimo_hodometro = {
        veiculo["id"]: int(veiculo["hodometro"]) for veiculo in veiculos_ativos
    }

    for entrega in entregas:
        veiculo_id = entrega.get("veículo_id")
        hodometro_final = entrega.get("hodometro_final", "")
        if veiculo_id in ultimo_hodometro and hodometro_final.isdigit():
            ultimo_hodometro[veiculo_id] = max(
                ultimo_hodometro[veiculo_id],
                int(hodometro_final),
            )

    return ultimo_hodometro


def converter_para_datetime(valor: str) -> datetime:
    return datetime.fromisoformat(valor)


def calcular_data_entrega(
    data_pedido: datetime,
    prazo_entrega: datetime,
    status: str,
) -> date | None:
    if status == "entregue":
        horas_ate_prazo = int((prazo_entrega - data_pedido).total_seconds() // 3600)
        return (data_pedido + timedelta(hours=randint(1, horas_ate_prazo))).date()

    if status == "atrasada":
        return (prazo_entrega + timedelta(hours=randint(1, 72))).date()

    return None


def pedido_passou_do_prazo_cancelamento(data_pedido: datetime) -> bool:
    return (date.today() - data_pedido.date()).days > DIAS_PARA_CANCELAMENTO


def escolher_status_entrega(data_pedido: datetime) -> str:
    status = choices(STATUS_ENTREGA, weights=PESOS_STATUS, k=1)[0]

    if status == "em andamento" and pedido_passou_do_prazo_cancelamento(data_pedido):
        return "cancelado"

    if status == "cancelado" and not pedido_passou_do_prazo_cancelamento(data_pedido):
        return "em andamento"

    return status


def entrega_passou_do_prazo_cancelamento(
    data_pedido: datetime,
    data_entrega: date | None,
) -> bool:
    if data_entrega:
        dias_para_entrega = (data_entrega - data_pedido.date()).days
        return dias_para_entrega > DIAS_PARA_CANCELAMENTO

    return False


def criar_csv_entregas() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    pedidos = carregar_csv(ARQUIVO_PEDIDOS)
    pedidos.sort(key=lambda pedido: pedido["data_pedido"])
    entregas_existentes = carregar_csv(ARQUIVO_SAIDA)
    pedidos_com_entrega = carregar_ids_pedidos_com_entrega(entregas_existentes)
    pedidos_sem_entrega = [
        pedido for pedido in pedidos
        if pedido["id"] not in pedidos_com_entrega
    ]

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

    if not pedidos_sem_entrega:
        print("Nenhum pedido novo para gerar entrega.")
        return

    proximo_id = obter_proximo_id(entregas_existentes)
    escrever_cabecalho = not arquivo_tem_dados(ARQUIVO_SAIDA)
    ultimo_hodometro = carregar_ultimo_hodometro(veiculos_ativos, entregas_existentes)

    with open(ARQUIVO_SAIDA, "a", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=FIELDNAMES)
        if escrever_cabecalho:
            escritor.writeheader()

        for entrega_id, pedido in enumerate(pedidos_sem_entrega, start=proximo_id):
            motorista = choices(motoristas_ativos, k=1)[0]
            veiculo = choices(veiculos_ativos, k=1)[0]

            data_pedido = converter_para_datetime(pedido["data_pedido"])
            prazo_entrega = converter_para_datetime(pedido["prazo_entrega"])

            status = escolher_status_entrega(data_pedido)
            data_entrega = calcular_data_entrega(data_pedido, prazo_entrega, status)
            if entrega_passou_do_prazo_cancelamento(data_pedido, data_entrega):
                status = "cancelado"
                data_entrega = None

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
                    "data_entrega": data_entrega.isoformat() if data_entrega else "",
                    "ano": prazo_entrega.year,
                    "mês": prazo_entrega.month,
                    "status": status,
                    "custo": f"{custo_centavos / 100:.2f}",
                    "hodometro_inicial": hodometro_inicial,
                    "hodometro_final": hodometro_final,
                }
            )

    print(f"Arquivo atualizado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    criar_csv_entregas()
