from pathlib import Path
import pandas as pd

# Caminhos das pastas
PASTA_RAW = Path("data/raw")
PASTA_PROCESSED = Path("data/processed")

# Cria a pasta processed, caso ela ainda não exista
PASTA_PROCESSED.mkdir(parents=True, exist_ok=True)

# Carregamento da tabela fato
fato_vendas = pd.read_csv(PASTA_RAW / "fato_vendas.csv")

# Carregamento das dimensões
dim_data = pd.read_csv(PASTA_RAW / "dim_data.csv")
dim_cliente = pd.read_csv(PASTA_RAW / "dim_cliente.csv")
dim_produto = pd.read_csv(PASTA_RAW / "dim_produto.csv")
dim_localizacao = pd.read_csv(PASTA_RAW / "dim_localizacao.csv")
dim_canal_venda = pd.read_csv(PASTA_RAW / "dim_canal_venda.csv")
dim_vendedor = pd.read_csv(PASTA_RAW / "dim_vendedor.csv")
dim_status_entrega = pd.read_csv(PASTA_RAW / "dim_status_entrega.csv")
dim_meta = pd.read_csv(PASTA_RAW / "dim_meta.csv")

# Junção da fato com as dimensões
base = fato_vendas.merge(dim_data, on="id_data", how="left")
base = base.merge(dim_cliente, on="id_cliente", how="left")
base = base.merge(dim_produto, on="id_produto", how="left")
base = base.merge(dim_localizacao, on="id_localizacao", how="left")
base = base.merge(dim_canal_venda, on="id_canal_venda", how="left")
base = base.merge(dim_vendedor, on="id_vendedor", how="left")
base = base.merge(dim_status_entrega, on="id_status_entrega", how="left")
base = base.merge(dim_meta, on="id_meta", how="left")

# Conversão da coluna de data
base["data"] = pd.to_datetime(base["data"], errors="coerce")

# Criação de colunas auxiliares para o dashboard
base["mes_ano"] = base["data"].dt.strftime("%m/%Y")
base["ano_mes_ordem"] = base["data"].dt.strftime("%Y-%m")

# Salva a base consolidada
base.to_csv(PASTA_PROCESSED / "base_dashboard.csv", index=False, encoding="utf-8-sig")

# Resultado no terminal
print("Base consolidada criada com sucesso!")
print(f"Quantidade de linhas: {base.shape[0]}")
print(f"Quantidade de colunas: {base.shape[1]}")
print("\nColunas disponíveis:")
print(list(base.columns))