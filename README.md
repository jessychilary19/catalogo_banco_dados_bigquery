# 📊 Catálogo de Metadados do Banco de Dados com BigQuery

## 🚀 Sobre o Projeto
Este projeto tem como objetivo catalogar todas as tabelas e colunas de um banco de dados no Google BigQuery, extraindo informações valiosas sobre os metadados e relacionamentos entre as tabelas. O resultado é gerado em um arquivo Excel, onde cada aba representa uma tabela do banco de dados, além de uma aba dedicada aos relacionamentos das tabelas.

---

## 📂 Funcionalidades
- **Extração de tabelas**: Lista todas as tabelas disponíveis no dataset.
- **Metadados das colunas**: Recupera o nome, tipo de dado, nulabilidade e posição ordinal das colunas.
- **Relacionamentos das tabelas**: Identifica chaves primárias e estrangeiras entre as tabelas.
- **Geração de relatório em Excel**: Cada tabela é salva em uma aba separada do arquivo Excel.
- **Periocidade das atualizações**: Informa a data da última atualização das tabelas.

---

## 🛠️ Tecnologias Utilizadas
- **Python**
- **Google BigQuery**
- **Pandas**
- **xlsxwriter**
- **Google Cloud Service Account**

---

## ⚙️ Pré-requisitos
- Python 3.8+
- Conta no Google Cloud Platform (GCP) com BigQuery habilitado
- Chave de serviço (Service Account JSON)

### Instalação das Dependências
```bash
pip install google-cloud-bigquery pandas openpyxl
```

---

## 🚦 Como Executar o Projeto
1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/nome-do-repositorio.git
```

2. Navegue até o diretório do projeto:
```bash
cd nome-do-repositorio
```

3. Configure a autenticação do GCP:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="caminho/para/sua_chave.json"
```

4. Execute o script principal:
```bash
python catalogador_bq.py
```

5. O arquivo **catalogo_metadados.xlsx** será gerado na pasta do projeto.

---

## 📂 Estrutura do Projeto
```
├── catalogador_bq.py          # Script principal
├── catalogo_metadados.xlsx    # Saída gerada pelo script
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação do projeto
```

---

## 📌 Melhorias Futuras
- Implementar análise de qualidade dos dados.
- Adicionar logs detalhados durante a execução.
- Permitir filtragem de tabelas específicas no BigQuery.

