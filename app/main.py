from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db_info import get_entries_by_date, test_phc_connection
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

@app.get("/status/")
def read_root():
    return {"Status": "OK"}

@app.get("/status/phc/")
def test_phc():
    return test_phc_connection()

@app.get("/entries/{year}/{month}", response_model=list[PHCEntry], response_model_by_alias=True)
def get_entries(year: int, month: int):
    _, _, entries = get_entries_by_date(year, month)
    return entries


