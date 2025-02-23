#catalogando o banco de dados da google
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

def get_columns(client, dataset_id, table_name):
    query = f"""
    SELECT column_name, data_type, is_nullable, ordinal_position
    FROM `{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position
    """
    query_job = client.query(query)
    # Criar uma lista de dicionários para transformar em DataFrame
    columns = [dict(column_name=row.column_name,
                    data_type=row.data_type,
                    is_nullable=row.is_nullable,
                    ordinal_position=row.ordinal_position) for row in query_job]
    return columns

def get_relationships(client, dataset_id):
    query = f"""
    SELECT 
      kcu.table_name AS child_table,
      kcu.column_name AS child_column,
      tc.constraint_type,
      kcu.referenced_table_name AS parent_table,
      kcu.referenced_column_name AS parent_column
    FROM 
      `{dataset_id}.INFORMATION_SCHEMA.KEY_COLUMN_USAGE` AS kcu
    JOIN 
      `{dataset_id}.INFORMATION_SCHEMA.TABLE_CONSTRAINTS` AS tc
      ON kcu.constraint_name = tc.constraint_name
    WHERE 
      tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')
    ORDER BY 
      kcu.table_name
    """
    query_job = client.query(query)
    relationships = [dict(child_table=row.child_table,
                          child_column=row.child_column,
                          constraint_type=row.constraint_type,
                          parent_table=row.parent_table,
                          parent_column=row.parent_column) for row in query_job]
    return relationships

def main():
    # Configurar autenticação e identificação do projeto/dataset
    project_id = "meu-projeto"  # Substitua pelo seu project_id
    dataset_id = f"{project_id}.meu_dataset"  # Substitua pelo seu dataset

    # Autenticação via arquivo de chave JSON
    credentials = service_account.Credentials.from_service_account_file('caminho/para/sua_chave.json')
    client = bigquery.Client(credentials=credentials, project=project_id)
    
    # Obter todas as tabelas
    tables = get_tables(client, dataset_id)
    print("Tabelas encontradas:", tables)
    
    # Criar um ExcelWriter para salvar as abas
    excel_file = "catalogo_metadados.xlsx"
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        # Iterar por cada tabela e salvar os metadados de colunas
        for table in tables:
            columns = get_columns(client, dataset_id, table)
            # Converter para DataFrame
            df = pd.DataFrame(columns)
            # Salvar a aba com o nome da tabela
            df.to_excel(writer, sheet_name=table[:31], index=False)  # sheet_name máximo de 31 caracteres
        
        # Opcional: salvar os relacionamentos em uma aba separada
        relationships = get_relationships(client, dataset_id)
        if relationships:
            df_rels = pd.DataFrame(relationships)
            df_rels.to_excel(writer, sheet_name="Relacionamentos", index=False)
    
    print(f"Metadados salvos no arquivo {excel_file}")

if __name__ == "__main__":
    main()
