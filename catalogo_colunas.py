#catalogo de todas as colunas que existem no banco de dados
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

def get_tables(client, dataset_id):
    query = f"""
    SELECT table_name
    FROM `{dataset_id}.INFORMATION_SCHEMA.TABLES`
    WHERE table_type = 'BASE TABLE'
    """
    query_job = client.query(query)
    tables = [row.table_name for row in query_job]
    return tables

def get_columns_for_table(client, dataset_id, table_name):
    query = f"""
    SELECT table_name, column_name
    FROM `{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position
    """
    query_job = client.query(query)
    columns = [dict(table_name=row.table_name, column_name=row.column_name) for row in query_job]
    return columns

def main():
    # Configurar autenticação e identificação do projeto/dataset
    project_id = "meu-projeto"  # Substitua pelo seu project_id
    dataset_id = f"{project_id}.meu_dataset"  # Substitua pelo seu dataset

    # Autenticação via arquivo de chave JSON
    credentials = service_account.Credentials.from_service_account_file('caminho/para/sua_chave.json')
    client = bigquery.Client(credentials=credentials, project=project_id)

    # Obter todas as tabelas do dataset
    tables = get_tables(client, dataset_id)
    print("Tabelas encontradas:", tables)

    # Lista para armazenar os metadados das colunas
    all_columns = []
    for table in tables:
        columns = get_columns_for_table(client, dataset_id, table)
        all_columns.extend(columns)

    # Converter a lista para um DataFrame
    df = pd.DataFrame(all_columns)

    # Opcional: Remover duplicatas caso alguma coluna com o mesmo nome apareça em tabelas diferentes
    # df_unique = df.drop_duplicates(subset=['column_name'])

    # Salvar o DataFrame em uma planilha Excel
    excel_file = "colunas_padronizadas.xlsx"
    df.to_excel(excel_file, index=False, sheet_name="Colunas")

    print(f"Informações das colunas salvas em {excel_file}")

if __name__ == "__main__":
    main()
