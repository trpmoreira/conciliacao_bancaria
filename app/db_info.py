from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from app.models.sqlite.base import Base
from app.models.sqlite.banco import Banco
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.movimentos_phc import PHCMovimento

load_dotenv()

server = os.getenv('server_phc')
database = os.getenv('database_phc')
username = os.getenv('username_phc')
password = os.getenv('password_phc')

connection_string_phc = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'

engine_phc = create_engine(connection_string_phc)
engine_sqlite = create_engine(os.getenv('DATABASE_URL_SQLLITE'))

#Criar as tabelas em sqlite
def init_db():
    Base.metadata.create_all(engine_sqlite)

Session = sessionmaker(bind=engine_sqlite)


def test_phc_connection():
    try:
        conn = engine_phc.connect()
        cursor = conn.connection.cursor()
        cursor.execute("SELECT top 1 * FROM ml")
        conn.close()
        return {"Status": "OK", "Message": "Conexão com PHC estabelecida"}
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}

def test_sqlite_connection():
    try:
        conn = engine_sqlite.connect()
        conn.close()
        return {"Status": "OK", "Message": "Conexão com SQLite estabelecida"}
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}


def get_entries_by_date(year: int, month: int):
    try:
        conn = engine_phc.connect()
        cursor = conn.connection.cursor()
        cursor.execute(f"""
            SELECT CONVERT(VARCHAR(10), data, 103) AS 'Data',
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

def get_entries_by_date_account(year: int, month: int, account: str):
    try:
        conn = engine_phc.connect()
        cursor = conn.connection.cursor()
        cursor.execute(f"""
            SELECT CONVERT(VARCHAR(10), data, 103) AS 'Data',
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
            WHERE conta = '{account}'
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

def get_contas_bancarias():
    try:
        session = Session()
        bancos = session.query(Banco).all()
        session.close()

        banco_dicts = []

        for banco in bancos:
            banco_dicts.append({
                "id": banco.id,
                "nome_banco": banco.nome_banco.strip(),
                "nome_conta": banco.nome_conta.strip(),
                "conta_phc": banco.conta_phc.strip(),
                "nome_folha": banco.nome_folha.strip(),
                "codigo_banco": banco.codigo_banco.strip()
            })

        return banco_dicts


    except Exception as e:
        return {"Status": "Error 40", "Message": str(e)}

def create_conta_bancaria(nome_banco: str, nome_conta: str, conta_phc: str, nome_folha: str, codigo_banco: str):
    try:
        session = Session()
        banco = Banco(nome_banco=nome_banco, nome_conta=nome_conta, conta_phc=conta_phc, nome_folha=nome_folha, codigo_banco=codigo_banco)
        session.add(banco)
        session.commit()
        session.close()
        return {"Status": "OK", "Message": f"Conta {nome_conta}, do banco {nome_banco} criada com sucesso"}
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}

def get_contas_bancarias():
    try:
        session = Session()
        contas = session.query(ContaBancaria).all()
        session.close()
        return contas
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}


def create_banco(nome_banco: str):
    try:
        session = Session()
        banco = Banco(nome_banco=nome_banco)
        session.add(banco)
        session.commit()
        session.close()
        return {"Status": "OK", "Message": f"Banco {nome_banco} criado com sucesso"}
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}

def get_bancos():
    try:
        session = Session()
        bancos = session.query(Banco).all()
        session.close()
        return bancos
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}


def delete_banco_by_id(id: int):
    try:
        session = Session()
        session.query(Banco).filter(Banco.id == id).delete()
        session.commit()
        session.close()
        return {"Status": "OK", "Message": f"Conta {id} eliminada com sucesso"}
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}

