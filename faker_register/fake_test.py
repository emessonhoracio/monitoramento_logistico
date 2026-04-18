import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt_BR')

dados = []

for i in range(100):
    peso = round(random.uniform(1, 300),2)
    
    if peso > 100:
        veiculo = 'Caminhão'
    else:
        veiculo = 'Van'
        
    data_pedido = fake.date_between(start_date='-6M', end_date='today')
    
    prazo = random.choice([1,2,3,5])
    
    entrega = data_pedido + timedelta(days=prazo)
    
    status = 'Entregue'
    
    if random.random() < 0.05:
        status = 'Atrasado'
        entrega += timedelta(days=2)
    
    dados.append({
        'PedidoID': i+1,
        'Cliente': fake.company(),
        'Cidade': fake.city(),
        'PesoKg': peso,
        'Veiculo': veiculo,
        'DataPedido': data_pedido,
        'DataEntrega': entrega,
        'Status': status
    })

df = pd.DataFrame(dados)
df.to_excel('base_logistica.xlsx', index=False)