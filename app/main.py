from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.db_info import create_banco, delete_banco_by_id, delete_entries_by_account_and_period, get_bancos, get_contas_bancarias, get_entries_by_account_and_period, get_entries_by_date, get_entries_by_date_account, get_entries_by_period, init_db, test_phc_connection, test_sqlite_connection
from app.schemas.phc_entries import PHCEntry
from app.services.update_balance import update_balance
from app.services.bank_sheet_bulk import bank_bulk_import
from app.services.upload_bank_xlxs import upload_bank_sheet
from app.services.importacao_bancos import importar_movimentos_banco
from app.services.importacao_phc import importar_movimentos_phc

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# Status


@app.get("/status/")
def read_root():
    return {"Status": "OK"}


@app.get("/status/phc/")
def test_phc():
    return test_phc_connection()


@app.get("/status/sqlite/")
def test_sqlite():
    return test_sqlite_connection()

# Entries


@app.get("/entries/{year}/{month}", response_model=list[PHCEntry], response_model_by_alias=True)
def get_entries(year: int, month: int):
    _, _, entries = get_entries_by_date(year, month)
    return entries

@app.get("/entries/{year}/{month}/{account}", response_model=list[PHCEntry], response_model_by_alias=True)
def get_entries_by_account(year: int, month: int, account: int):
    _, _, entries = get_entries_by_date_account(year, month, account)
    return entries

# Bancos

@app.post("/contas_bancarias/novo/{nome_banco}/{nome_conta}/{conta_phc}/{nome_folha}/{codigo_banco}")
def create(nome_banco: str, nome_conta: str, conta_phc: str, nome_folha: str, codigo_banco: str):
    return create_banco(nome_banco, nome_conta, conta_phc, nome_folha, codigo_banco)

@app.get("/contas_bancarias/")
def get_all_contas_bancarias():
    return get_contas_bancarias()

@app.get("/bancos/")
def get_all_bancos():
    return get_bancos()

@app.delete("/bancos/{id}")
def delete_banco(id: int):
    return delete_banco_by_id(id)

@app.post("/bancos/novo/{nome_banco}")
def create_new_banco(nome_banco: str):
    return create_banco(nome_banco)

@app.post("/importacao_phc/{ano}/{mes}")
def importacao_phc(ano: int, mes: int):
    return importar_movimentos_phc(ano, mes)

@app.post("/importacao_bancos/{ano}/{mes}")
def importacao_bancos(ano: int, mes: int):
    return importar_movimentos_banco(ano, mes)

@app.get("/bancos/extrato/{ano}/{mes}/{account_id}")
def entries_by_account_and_period(ano: int, mes: int, account_id: int):
    return get_entries_by_account_and_period(ano, mes, account_id)

@app.get("/bancos/extrato/{ano}/{mes}")
def entries_by_period(ano: int, mes: int):
    return get_entries_by_period(ano, mes)

@app.delete("/bancos/extrato/{ano}/{mes}/{account_id}")
def del_entries_by_account_and_period(ano: int, mes: int, account_id: int):
    return delete_entries_by_account_and_period(ano, mes, account_id)

@app.post("/bancos/upload/{ano}/{mes}")
async def upload_bank_sheet_by_period(ano: int, mes: int, file: UploadFile = File(...)):
    return await upload_bank_sheet(ano, mes, file)

@app.post("/bancos/bulk/{ano}")
def bank_bulk_import_year(ano: int):
    return bank_bulk_import(ano)

@app.post("/bancos/balance/{period}")
def update_balance_by_period(period: str):
    return update_balance(period)

