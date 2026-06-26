# Monitoramento Logistico - SIGE

Projeto de apoio ao monitoramento logistico do SIGE, com foco em gerar,
organizar e analisar dados de clientes, enderecos, pedidos, motoristas,
veiculos e entregas.

O repositorio contem scripts Python para criacao de massas de dados em CSV

## Aviso sobre os dados

Todos os dados deste projeto sao ficticios.

As informacoes de nomes, empresas, CNPJs, placas, enderecos, pedidos,
entregas, custos e hodometros sao geradas artificialmente para fins de estudo,
teste, demonstracao e desenvolvimento. Elas nao representam clientes,
motoristas, veiculos, empresas ou operacoes reais.

## Estrutura principal

- `database/scripts`: scripts Python usados para gerar dados.
- `database/data`: dados CSV mantidos no projeto.
- `requirements.txt`: dependencias Python usadas no projeto.

## Regras de negocio dos scripts

### Enderecos

Script: `database/scripts/populate_address.py`

- Gera 300 enderecos.
- Usa nomes de ruas ficticios.
- Restringe as cidades a uma lista de municipios de Alagoas.
- Define o estado como `Alagoas`.
- Gera numeros de endereco entre 1 e 9999.
- Salva o resultado em `database/data/addresses.csv`.

### Clientes

Scripts:

- `database/scripts/populate_clients.py`

Regras do gerador CSV:

- Usa os enderecos existentes em `addresses.csv`.
- Cria um cliente para cada endereco carregado.
- Gera nome de empresa e CNPJ ficticios.
- Associa cada cliente a um endereco.
- Define o status `ativo` de forma aleatoria.
- Salva o resultado em `database/data/clients.csv`.

### Motoristas

Script: `database/scripts/populate_drivers.py`

- Gera 50 motoristas.
- Usa nomes ficticios.
- Define o codigo do motorista com base no proprio ID.
- Define o status `ativo` de forma aleatoria.
- Salva o resultado em `database/data/drivers.csv`.

### Veiculos

Script: `database/scripts/populate_vehicles.py`

- Gera 50 veiculos.
- Usa placas ficticias e unicas.
- Escolhe modelos a partir de uma lista predefinida.
- Define a capacidade em kg conforme a faixa permitida para cada modelo.
- Gera ano entre 2010 e 2026.
- Gera hodometro inicial entre 0 e 500.000 km.
- Define o status `ativo` de forma aleatoria.
- Salva o resultado em `database/data/vehicles.csv`.

### Pedidos

Script: `database/scripts/populate_orders.py`

- Gera 10.000 pedidos por execucao.
- Usa clientes existentes em `clients.csv`.
- Gera pedidos a partir de 2025-01-01 ate a data atual.
- Nao gera pedidos aos domingos.
- Define prazo de entrega como 3 dias apos a data do pedido.
- Gera valor entre R$ 200,00 e R$ 5.000,00.
- Acrescenta novos pedidos ao arquivo existente, mantendo a sequencia de IDs.
- Salva o resultado em `database/data/orders.csv`.

### Entregas

Script: `database/scripts/populate_delivery.py`

- Gera entregas apenas para pedidos que ainda nao possuem entrega.
- Usa somente motoristas ativos.
- Usa somente veiculos ativos.
- Ordena os pedidos por data antes de gerar as entregas.
- Sorteia o status da entrega com os seguintes pesos:
  - `entregue`: 70%
  - `atrasada`: 20%
  - `em andamento`: 5%
  - `cancelado`: 5%
- Entregas com status `entregue` recebem data entre a data do pedido e o prazo.
- Entregas com status `atrasada` recebem data ate 72 horas apos o prazo.
- Pedidos em andamento com mais de 10 dias sao convertidos para `cancelado`.
- Pedidos cancelados com menos de 10 dias sao convertidos para `em andamento`.
- Entregas com duracao maior que 10 dias sao canceladas.
- O hodometro final sempre avanca de 5 a 300 km em relacao ao hodometro
  inicial.
- O ultimo hodometro conhecido de cada veiculo e reaproveitado para novas
  entregas.
- Gera custo entre R$ 50,00 e R$ 1.500,00.
- Acrescenta novas entregas ao arquivo existente, mantendo a sequencia de IDs.
- Salva o resultado em `database/data/deliveries.csv`.

## Como preparar o ambiente

Instale as dependencias Python:

```bash
pip install -r requirements.txt
```

## Ordem sugerida para gerar CSVs

```bash
python database/scripts/populate_address.py
python "database/scripts/populate_clients copy.py"
python database/scripts/populate_drivers.py
python database/scripts/populate_vehicles.py
python database/scripts/populate_orders.py
python database/scripts/populate_delivery.py
```

Essa ordem respeita as dependencias entre os arquivos: clientes dependem de
enderecos, pedidos dependem de clientes e entregas dependem de pedidos,
motoristas e veiculos.
