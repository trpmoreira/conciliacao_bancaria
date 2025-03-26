from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db_info import create_banco, delete_by_id, get_bancos, get_entries_by_date, init_db, test_phc_connection, test_sqlite_connection
from app.schemas.phc_entries import PHCEntry

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

#Status
@app.get("/status/")
def read_root():
    return {"Status": "OK"}

@app.get("/status/phc/")
def test_phc():
    return test_phc_connection()

@app.get("/status/sqlite/")
def test_sqlite():
    return test_sqlite_connection()

#Entries
@app.get("/entries/{year}/{month}", response_model=list[PHCEntry], response_model_by_alias=True)
def get_entries(year: int, month: int):
    _, _, entries = get_entries_by_date(year, month)
    return entries


#Bancos
@app.get("/bancos/")
def get_all_bancos():
    return get_bancos()

@app.post("/bancos/novo/{nome_banco}/{nome_conta}/{conta_phc}/{nome_folha}/{codigo_banco}")
def create(nome_banco: str, nome_conta: str, conta_phc: str, nome_folha: str, codigo_banco: str):
    return create_banco(nome_banco, nome_conta, conta_phc, nome_folha, codigo_banco)

@app.delete("/bancos/{id}")
def delete(id: int):
    return delete_by_id(id)
