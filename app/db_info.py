from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv('server_phc')
database = os.getenv('database_phc')
username = os.getenv('username_phc')
password = os.getenv('password_phc')

connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'

engine = create_engine(connection_string)

# Criação do session
session = sessionmaker(bind=engine)


def test_phc_connection():
    print(connection_string)
    try:
        conn = engine.connect()
        cursor = conn.connection.cursor()
        cursor.execute("SELECT top 1 * FROM ml")
        conn.close()
        return {"Status": "OK", "Message": "Conexão com PHC estabelecida"}
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}


def get_entries_by_date(year: int, month: int):
    try:
        conn = engine.connect()
        cursor = conn.connection.cursor()
        cursor.execute(f"""
            SELECT top 10 CONVERT(VARCHAR(10), data, 103) AS 'Data',
            ml.dinome AS 'Diário',
            ml.dilno AS 'Nº',
            ml.adoc AS 'Documento',
            ml.descritivo AS 'Descrição',
            ml.edeb AS 'Débito',
            ml.ecre AS 'Crédito',
            ml.cct AS 'Centro Custo',
            ml.conta AS 'Conta',
            ml.descricao AS 'Nome Conta',
            ml.edeb - ml.ecre AS 'Valor',
            ABS(ml.edeb - ml.ecre) AS 'ABS',
            ml.intid AS 'Id Interna',
            ml.obs AS 'Observações'
            FROM ml
            WHERE conta LIKE '12%'
            AND YEAR(data) = {year}
            AND MONTH(data) = {month}
        """)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            cleaned_row = {}
            for key, value in zip(columns, row):
                if isinstance(value, str):
                    cleaned_row[key] = value.strip()
                else:
                    cleaned_row[key] = value
            entries.append(cleaned_row)

        return True, f"{len(entries)} lançamentos encontrados", entries
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}
