"""
Este script conecta-se ao SQL Server usando autenticação do Windows,
cria um banco de dados chamado 'EstudosSQL' (caso ainda não exista),
cria uma tabela chamada 'DesempenhoFinanceiro' com colunas intuitivas,
e insere dados fictícios para fins de estudo e prática em SQL.
"""

import pyodbc

"""
Define os parâmetros de conexão iniciais com o SQL Server (instância padrão via TCP/IP na porta 1433).
Conecta-se inicialmente ao banco 'master' apenas para criar o novo banco de dados.
"""
server = "localhost,1433"
database = "master"

conexao_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};DATABASE={database};"
    "Trusted_Connection=yes;"
)

"""
Testa a conexão com o SQL Server. Encerra o script se houver falha.
"""
try:
    conexao_teste = pyodbc.connect(conexao_str)
    print("✅ Conexão bem-sucedida com o SQL Server!")
    conexao_teste.close()
except Exception as e:
    print("❌ Erro de conexão:", e)
    exit()

"""
Cria o banco de dados 'EstudosSQL' usando uma conexão com autocommit (necessário para CREATE DATABASE).
"""
conexao_create = pyodbc.connect(conexao_str, autocommit=True)
cursor_create = conexao_create.cursor()

cursor_create.execute("IF DB_ID('EstudosSQL') IS NULL CREATE DATABASE EstudosSQL;")
print("📦 Banco de dados 'EstudosSQL' criado com sucesso (ou já existia).")

cursor_create.close()
conexao_create.close()

"""
Atualiza a string de conexão para apontar diretamente para o banco recém-criado.
"""
database = "EstudosSQL"
conexao_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};DATABASE={database};"
    "Trusted_Connection=yes;"
)

conexao = pyodbc.connect(conexao_str)
cursor = conexao.cursor()

"""
Cria a tabela 'DesempenhoFinanceiro' com colunas intuitivas.
Se a tabela já existir, ela será removida e recriada.
"""
cursor.execute(
    """
    IF OBJECT_ID('dbo.DesempenhoFinanceiro', 'U') IS NOT NULL
        DROP TABLE dbo.DesempenhoFinanceiro;

    CREATE TABLE dbo.DesempenhoFinanceiro (
        IdPessoa INT,
        NomePessoa NVARCHAR(100),
        AnoReferencia INT,
        ValorRecebido MONEY,
        ValorTrabalho MONEY,
        ValorDespesas MONEY,
        ValorBonus MONEY,
        PercentualRentabilidade FLOAT
    );
    """
)

"""
Insere dados fictícios na tabela para fins de teste e estudo.
"""
dados = [
    (1, "Ana Costa", 2023, 100000.00, 30000.00, 10000.00, 5000.00, 1.43),
    (2, "Bruno Martins", 2023, 90000.00, 25000.00, 8000.00, 2000.00, 1.63),
    (3, "Carla Nunes", 2024, 70000.00, 20000.00, 7000.00, 3000.00, 1.4),
    (4, "Diego Lima", 2024, 0.00, 0.00, 0.00, 0.00, None),
]

cursor.executemany(
    """
    INSERT INTO dbo.DesempenhoFinanceiro (
        IdPessoa, NomePessoa, AnoReferencia,
        ValorRecebido, ValorTrabalho, ValorDespesas,
        ValorBonus, PercentualRentabilidade
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    dados,
)

conexao.commit()
print("📄 Tabela 'DesempenhoFinanceiro' criada e populada com sucesso.")

"""
Encerra a conexão com o banco de dados.
"""
cursor.close()
conexao.close()
print("✅ Conexão encerrada.")
