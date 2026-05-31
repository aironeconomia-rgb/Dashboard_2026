from pathlib import Path
import pandas as pd

# Caminho da pasta onde estão os arquivos CSV
pasta_raw = Path("data/raw")

# Lista todos os arquivos CSV da pasta
arquivos_csv = list(pasta_raw.glob("*.csv"))

print("Arquivos encontrados na pasta data/raw:")
print("-" * 50)

for arquivo in arquivos_csv:
    print(f"\nArquivo: {arquivo.name}")

    # Lê apenas as 5 primeiras linhas para testar
    df = pd.read_csv(arquivo)

    print(f"Quantidade de linhas: {df.shape[0]}")
    print(f"Quantidade de colunas: {df.shape[1]}")
    print("Colunas:")
    print(list(df.columns))