"""
Lab SQL Server – EstudosSQL
Cria banco, schema, tabelas com PK/FK/constraints, índices, views e popula dados
para praticar: SELECT, WHERE, ORDER BY, DISTINCT, IN/BETWEEN/LIKE,
agregações (COUNT/SUM/AVG/MIN/MAX), GROUP BY/HAVING, JOINs, subqueries,
CTE, views, funções de data/string, operações matemáticas e tratamento de NULL.

Referências:
- Curso do YouTube usado como base temática (ver conversa).
- Tipos DECIMAL para valores monetários (evitar MONEY).
- Variáveis de ambiente via python-dotenv.
"""

import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


SERVER = os.getenv("SQLSERVER_SERVER", "localhost,1433")
DB_NAME = os.getenv("SQLSERVER_DB", "EstudosSQL")
DRIVER = os.getenv("SQLSERVER_DRIVER", "{ODBC Driver 17 for SQL Server}")
TRUSTED = os.getenv("SQLSERVER_TRUSTED", "1")  # "1" (Windows) ou "0" (SQL Auth)
USERNAME = os.getenv("SQLSERVER_USERNAME", "")
PASSWORD = os.getenv("SQLSERVER_PASSWORD", "")
# Para Driver 18, evite erro de TLS local:
ENCRYPT = os.getenv("SQLSERVER_ENCRYPT", "no")  # "yes" ou "no"
TRUST_CERT = os.getenv("SQLSERVER_TRUSTSERVERCERT", "yes")  # "yes" ou "no"


def make_conn_str(database="master", autocommit=False):
    """
    Abre conexão SQL Server usando variáveis de ambiente.
    No dia a dia: permite trocar DEV/HML/PRD sem expor senhas no código.
    Args:
        database (str): banco alvo (ex.: 'EstudosSQL').
        autocommit (bool): True para DDL como CREATE DATABASE.
    Returns:
        pyodbc.Connection: conexão pronta para uso.
    """
    base = [
        f"DRIVER={DRIVER}",
        f"SERVER={SERVER}",
        f"DATABASE={database}",
    ]
    if TRUSTED == "1":
        base.append("Trusted_Connection=yes")
    else:
        base.append(f"UID={USERNAME}")
        base.append(f"PWD={PASSWORD}")
    # Criptografia (útil p/ Driver 18). Ajuste conforme ambiente.
    base.append(f"Encrypt={ENCRYPT}")
    base.append(f"TrustServerCertificate={TRUST_CERT}")
    conn_str = ";".join(base) + ";"
    return pyodbc.connect(conn_str, autocommit=autocommit)


def exec_many(cursor, sql, rows):
    """
    Executa INSERT/UPDATE em lote com fast_executemany.
    No dia a dia: cargas de Produtos, Pedidos ou Pagamentos de uma planilha/ETL.
    Args:
        cursor (pyodbc.Cursor): cursor ativo.
        sql (str): comando parametrizado (VALUES ?, ?, ...).
        rows (Iterable[tuple]): dados a serem aplicados.
    """
    cursor.fast_executemany = True
    cursor.executemany(sql, rows)


# ---------------------------
# 1) Criar database (idempotente)
# ---------------------------
with make_conn_str(autocommit=True) as cx:
    cur = cx.cursor()
    cur.execute(f"IF DB_ID('{DB_NAME}') IS NULL CREATE DATABASE {DB_NAME};")
    print(f"📦 Banco '{DB_NAME}' OK.")

# ---------------------------
# 2) Criar schema e tabelas
# ---------------------------
with make_conn_str(database=DB_NAME) as cx:
    cur = cx.cursor()

    # Schema didático
    cur.execute(
        "IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='lab') EXEC('CREATE SCHEMA lab');"
    )

    # Tabelas principais (PK, FK, CHECK, DEFAULTs)
    cur.execute(
        """
    -- Limpeza idempotente (SQL Server 2016+)
    IF OBJECT_ID('lab.Pagamento','U') IS NOT NULL DROP TABLE lab.Pagamento;
    IF OBJECT_ID('lab.ItemPedido','U') IS NOT NULL DROP TABLE lab.ItemPedido;
    IF OBJECT_ID('lab.Pedido','U')      IS NOT NULL DROP TABLE lab.Pedido;
    IF OBJECT_ID('lab.Produto','U')     IS NOT NULL DROP TABLE lab.Produto;
    IF OBJECT_ID('lab.Categoria','U')   IS NOT NULL DROP TABLE lab.Categoria;
    IF OBJECT_ID('lab.Cliente','U')     IS NOT NULL DROP TABLE lab.Cliente;
    IF OBJECT_ID('lab.Funcionario','U') IS NOT NULL DROP TABLE lab.Funcionario;
    IF OBJECT_ID('lab.Departamento','U')IS NOT NULL DROP TABLE lab.Departamento;

    CREATE TABLE lab.Departamento (
        IdDepartamento  INT IDENTITY(1,1) PRIMARY KEY,
        Nome            NVARCHAR(80) NOT NULL UNIQUE,
        CriadoEm        DATETIME2     NOT NULL CONSTRAINT DF_Dep_Criado DEFAULT SYSUTCDATETIME()
    );

    CREATE TABLE lab.Funcionario (
        IdFuncionario   INT IDENTITY(1,1) PRIMARY KEY,
        Nome            NVARCHAR(120) NOT NULL,
        Email           NVARCHAR(120) NULL UNIQUE,
        Salario         DECIMAL(12,2) NOT NULL CHECK (Salario >= 0),
        IdDepartamento  INT NOT NULL,
        Ativo           BIT NOT NULL CONSTRAINT DF_Func_Ativo DEFAULT 1,
        CriadoEm        DATETIME2 NOT NULL CONSTRAINT DF_Func_Criado DEFAULT SYSUTCDATETIME(),
        CONSTRAINT FK_Func_Dep FOREIGN KEY (IdDepartamento) REFERENCES lab.Departamento(IdDepartamento)
    );

    CREATE TABLE lab.Cliente (
        IdCliente       INT IDENTITY(1,1) PRIMARY KEY,
        Nome            NVARCHAR(120) NOT NULL,
        Email           NVARCHAR(120) NULL UNIQUE,
        Cidade          NVARCHAR(80)  NULL,
        UF              CHAR(2)       NULL,
        CriadoEm        DATETIME2     NOT NULL CONSTRAINT DF_Cliente_Criado DEFAULT SYSUTCDATETIME()
    );

    CREATE TABLE lab.Categoria (
        IdCategoria     INT IDENTITY(1,1) PRIMARY KEY,
        Nome            NVARCHAR(80) NOT NULL UNIQUE
    );

    CREATE TABLE lab.Produto (
        IdProduto       INT IDENTITY(1,1) PRIMARY KEY,
        Nome            NVARCHAR(120) NOT NULL,
        IdCategoria     INT NOT NULL,
        PrecoUnitario   DECIMAL(12,2) NOT NULL CHECK (PrecoUnitario >= 0),
        Ativo           BIT NOT NULL CONSTRAINT DF_Prod_Ativo DEFAULT 1,
        CONSTRAINT FK_Prod_Cat FOREIGN KEY (IdCategoria) REFERENCES lab.Categoria(IdCategoria)
    );

    CREATE TABLE lab.Pedido (
        IdPedido        INT IDENTITY(1,1) PRIMARY KEY,
        IdCliente       INT NOT NULL,
        IdFuncionario   INT NULL, -- vendedor
        DataPedido      DATE NOT NULL,
        Status          VARCHAR(20) NOT NULL CHECK (Status IN ('ABERTO','FATURADO','CANCELADO')),
        Frete           DECIMAL(12,2) NOT NULL DEFAULT 0,
        Desconto        DECIMAL(12,2) NOT NULL DEFAULT 0,
        CONSTRAINT FK_Ped_Cli FOREIGN KEY (IdCliente) REFERENCES lab.Cliente(IdCliente),
        CONSTRAINT FK_Ped_Func FOREIGN KEY (IdFuncionario) REFERENCES lab.Funcionario(IdFuncionario)
    );

    CREATE TABLE lab.ItemPedido (
        IdItem          INT IDENTITY(1,1) PRIMARY KEY,
        IdPedido        INT NOT NULL,
        IdProduto       INT NOT NULL,
        Qtde            INT NOT NULL CHECK (Qtde > 0),
        PrecoUnitario   DECIMAL(12,2) NOT NULL CHECK (PrecoUnitario >= 0),
        -- total da linha como coluna calculada (para operações matemáticas)
        TotalLinha AS (CONVERT(DECIMAL(18,2), Qtde * PrecoUnitario)) PERSISTED,
        CONSTRAINT UQ_Item_Pedido_Prod UNIQUE (IdPedido, IdProduto),
        CONSTRAINT FK_Item_Ped FOREIGN KEY (IdPedido) REFERENCES lab.Pedido(IdPedido) ON DELETE CASCADE,
        CONSTRAINT FK_Item_Prod FOREIGN KEY (IdProduto) REFERENCES lab.Produto(IdProduto)
    );

    CREATE TABLE lab.Pagamento (
        IdPagamento     INT IDENTITY(1,1) PRIMARY KEY,
        IdPedido        INT NOT NULL,
        DataPgto        DATE NOT NULL,
        Valor           DECIMAL(12,2) NOT NULL CHECK (Valor >= 0),
        MeioPgto        VARCHAR(20) NOT NULL CHECK (MeioPgto IN ('PIX','CARTAO','BOLETO','DINHEIRO')),
        CONSTRAINT FK_Pgto_Ped FOREIGN KEY (IdPedido) REFERENCES lab.Pedido(IdPedido) ON DELETE CASCADE
    );

    -- Índices úteis para exercícios (pesquisas, filtros, JOINs)
    CREATE INDEX IX_Prod_Cat ON lab.Produto(IdCategoria);
    CREATE INDEX IX_Ped_Cliente_Data ON lab.Pedido(IdCliente, DataPedido);
    CREATE INDEX IX_Item_Pedido ON lab.ItemPedido(IdPedido);
    CREATE INDEX IX_Cliente_UF ON lab.Cliente(UF);

    -- View com agregação e JOIN (para GROUP BY/HAVING e filtro por período)
    IF OBJECT_ID('lab.vw_VendasPorClienteAno','V') IS NOT NULL DROP VIEW lab.vw_VendasPorClienteAno;
    """
    )  # terminamos o batch aqui

    # A partir daqui, precisamos criar a VIEW em um batch à parte
    cur.execute(
        """
    CREATE VIEW lab.vw_VendasPorClienteAno
    AS
    WITH vendas AS (
        SELECT
            p.IdCliente,
            YEAR(p.DataPedido) AS Ano,
            SUM(i.TotalLinha)   AS ValorProdutos,
            SUM(p.Frete)        AS ValorFrete,
            SUM(p.Desconto)     AS Descontos
        FROM lab.Pedido p
        JOIN lab.ItemPedido i ON i.IdPedido = p.IdPedido
        WHERE p.Status <> 'CANCELADO'
        GROUP BY p.IdCliente, YEAR(p.DataPedido)
    )
    SELECT
        c.IdCliente,
        c.Nome       AS Cliente,
        v.Ano,
        (v.ValorProdutos + v.ValorFrete - v.Descontos) AS FaturamentoBruto
    FROM vendas v
    JOIN lab.Cliente c ON c.IdCliente = v.IdCliente;
    """
    )

    # ---------------------------
    # 3) Popular dados (seed)
    # ---------------------------
    # Departamentos
    exec_many(
        cur,
        "INSERT INTO lab.Departamento(Nome) VALUES (?)",
        [("Vendas",), ("Financeiro",), ("Operações",)],
    )

    # Funcionários (para INNER JOIN e filtros)
    exec_many(
        cur,
        """
        INSERT INTO lab.Funcionario(Nome, Email, Salario, IdDepartamento, Ativo)
        VALUES (?, ?, ?, ?, ?)
    """,
        [
            ("Ana Vendedora", "ana@empresa.com", 4500.00, 1, 1),
            ("Bruno Vendedor", "bruno@empresa.com", 4200.00, 1, 1),
            ("Carla Finance", "carla@empresa.com", 7000.00, 2, 1),
            ("Diego Ops", None, 5000.00, 3, 0),
        ],
    )

    # Clientes (para LIKE/IN/BETWEEN e DISTINCT)
    exec_many(
        cur,
        """
        INSERT INTO lab.Cliente(Nome, Email, Cidade, UF) VALUES (?, ?, ?, ?)
    """,
        [
            ("João Silva", "joao@mail.com", "Porto Alegre", "RS"),
            ("Maria Souza", "maria@mail.com", "Curitiba", "PR"),
            ("Carlos Lima", "carlos@mail.com", "São Paulo", "SP"),
            ("Ana Paula", "ana@mail.com", "Florianópolis", "SC"),
            ("Joana Santos", None, "Pelotas", "RS"),
        ],
    )

    # Categorias e Produtos
    exec_many(
        cur,
        "INSERT INTO lab.Categoria(Nome) VALUES (?)",
        [("Bebidas",), ("Alimentos",), ("Eletrônicos",)],
    )

    exec_many(
        cur,
        """
        INSERT INTO lab.Produto(Nome, IdCategoria, PrecoUnitario, Ativo)
        VALUES (?, ?, ?, ?)
    """,
        [
            ("Café 500g", 2, 25.90, 1),
            ("Chá Verde 200g", 2, 18.50, 1),
            ("Refrigerante Lata 350ml", 1, 5.99, 1),
            ("Fone Bluetooth", 3, 199.90, 1),
            ("Cabo USB-C", 3, 29.90, 1),
            ('TV 55"', 3, 2799.00, 1),
        ],
    )

    # Pedidos (datas para BETWEEN/DATEPART; status para filtros)
    exec_many(
        cur,
        """
        INSERT INTO lab.Pedido(IdCliente, IdFuncionario, DataPedido, Status, Frete, Desconto)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        [
            (1, 1, "2025-01-15", "FATURADO", 20.00, 5.00),
            (2, 2, "2025-02-10", "FATURADO", 35.00, 0.00),
            (3, 1, "2025-03-05", "ABERTO", 15.00, 0.00),
            (4, 2, "2024-12-20", "CANCELADO", 15.00, 10.00),
            (1, 1, "2024-11-25", "FATURADO", 25.00, 0.00),
        ],
    )

    # Itens
    exec_many(
        cur,
        """
        INSERT INTO lab.ItemPedido(IdPedido, IdProduto, Qtde, PrecoUnitario) VALUES (?, ?, ?, ?)
    """,
        [
            (1, 1, 2, 25.90),  # Café
            (1, 4, 1, 199.90),  # Fone
            (2, 3, 6, 5.99),  # Refri
            (2, 5, 2, 29.90),  # Cabo
            (3, 6, 1, 2799.00),  # TV
            (5, 1, 1, 25.90),
            (5, 3, 12, 5.99),
        ],
    )

    # Pagamentos (para SUM/AVG, HAVING)
    exec_many(
        cur,
        """
        INSERT INTO lab.Pagamento(IdPedido, DataPgto, Valor, MeioPgto) VALUES (?, ?, ?, ?)
    """,
        [
            (1, "2025-01-16", 250.00, "PIX"),
            (1, "2025-01-17", 50.00, "CARTAO"),
            (2, "2025-02-11", 120.00, "BOLETO"),
            (5, "2024-11-26", 150.00, "DINHEIRO"),
        ],
    )

    cx.commit()
    print("✅ Schema/tabelas/dados criados.")

# ---------------------------
# 4) Dicas de exercícios (curtas)
# ---------------------------
print(
    """
Agora pratique:
1) SELECT básico: liste produtos ativos ordenando por nome (ASC) e por preço (DESC).
2) WHERE com IN/BETWEEN/LIKE: clientes do RS ou SC; pedidos entre 2025-01-01 e 2025-03-31; produtos com nome contendo 'C'.
3) DISTINCT: liste UFs únicas dos clientes.
4) Agregações: SUM/AVG/MIN/MAX/COUNT por cliente; faturamento por ano.
5) GROUP BY + HAVING: clientes com faturamento bruto > 200 em 2025 usando lab.vw_VendasPorClienteAno.
6) JOINs: produtos por categoria; itens de um pedido com totais; pedidos + clientes + vendedor.
7) Subquery: produtos mais caros que a média da sua categoria.
8) CTE: somatório mensal de vendas e filtrar apenas meses > média geral.
9) Funções de DATA: YEAR/MONTH/DATEPART; STRING: UPPER/LEFT/RIGHT/LEN; matemáticas: ROUND.
10) Índices: compare planos com/sem filtro por IdCliente e DataPedido (IX_Ped_Cliente_Data).
"""
)
