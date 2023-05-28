import mysql.connector
from mysql.connector import errorcode


class DatabaseConnection:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            print("Conexão bem-sucedida ao banco de dados")
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Erro de acesso: Usuário ou senha incorretos")
            else:
                print("Erro ao conectar ao banco de dados:", error)

    def close(self):
        if self.conn is not None:
            self.conn.close()
            print("Conexão fechada")


class TableCreation:
    def __init__(self, connection):
        self.connection = connection

    # CRIA TABELA
    def create_table(self, table, columns):
        cursor = self.connection.conn.cursor()
        column_definitions = ', '.join(columns)
        sql_create_table = f"CREATE TABLE IF NOT EXISTS {table} ({column_definitions})"
        cursor.execute(sql_create_table)
        self.connection.conn.commit()
        cursor.close()
        print(f"Tabela '{table}' criada com sucesso")

    # ADICIONA COLUNAS A TABELA EXISTENTE
    def add_column(self, table, column):
        cursor = self.connection.conn.cursor()
        sql_add_column = f"ALTER TABLE {table} ADD COLUMN {column}"
        cursor.execute(sql_add_column)
        self.connection.conn.commit()
        cursor.close()
        print(f"Coluna '{column}' adicionada à tabela '{table}' com sucesso")

    # ADICIONA DADOS À TABELA
    def add_data(self, table, data):
        cursor = self.connection.conn.cursor()
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        sql_insert_data = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql_insert_data, values)
        self.connection.conn.commit()
        cursor.close()
        print(f"Dados adicionados à tabela '{table}' com sucesso")


# Solicitar entrada do usuário para as informações de conexão
host = input("Digite o host do banco de dados: ")
user = input("Digite o usuário do banco de dados: ")
password = input("Digite a senha do banco de dados: ")
database = input("Digite o nome do banco de dados: ")
port = input("Digite o número da porta do banco de dados: ")

# Criando uma instância da classe DatabaseConnection
db_connection = DatabaseConnection(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
db_connection.connect()

# Criando uma instância da classe TableCreation
table_creation = TableCreation(db_connection)

print("Criar tabela ou adicionar dados?")
opcao = input("Digite 'c' para criar uma tabela ou 'a' para adicionar dados a uma tabela existente: ")

if opcao.lower() == "c":
    print("Criação de tabela")
    nome_tabela = input("Digite o nome da tabela: ")

    # Verifica se a tabela já existe
    cursor = db_connection.conn.cursor()
    sql_check_table = f"SHOW TABLES LIKE '{nome_tabela}'"
    cursor.execute(sql_check_table)
    table_exists = cursor.fetchone()

    if table_exists:
        print("A tabela já existe.")
    else:
        num_colunas = int(input("Digite o número de colunas da tabela: "))
        colunas = []
        for i in range(num_colunas):
            nome_coluna = input(f"Digite o nome da coluna {i + 1}: ")
            tipo_coluna = input(f"Digite o tipo de dado da coluna {i + 1}: ")
            colunas.append(f"{nome_coluna} {tipo_coluna}")
        table_creation.create_table(nome_tabela, colunas)

elif opcao.lower() == "a":
    print("Adição de dados à tabela")
    nome_tabela = input("Digite o nome da tabela existente: ")

    # Verifica se a tabela existe
    cursor = db_connection.conn.cursor()
    sql_check_table = f"SHOW TABLES LIKE '{nome_tabela}'"
    cursor.execute(sql_check_table)
    table_exists = cursor.fetchone()

    if table_exists:
        # Obtém as colunas existentes na tabela
        cursor.execute(f"DESCRIBE {nome_tabela}")
        column_names = [row[0] for row in cursor.fetchall()]
        dados = {}
        for coluna in column_names:
            valor_coluna = input(f"Digite o valor para a coluna '{coluna}': ")
            dados[coluna] = valor_coluna
        table_creation.add_data(nome_tabela, dados)
        print(f"Dados adicionados à tabela '{nome_tabela}':")
        for coluna, valor in dados.items():
            print(f"{coluna}: {valor}")
    else:
        print("A tabela especificada não existe.")

else:
    print("Opção inválida.")


# Fechando a conexão com o banco de dados
db_connection.close()
