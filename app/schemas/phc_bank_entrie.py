from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, ValidationError, field_validator
from typing import Optional

class BankEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: date = Field(..., alias="Data")
    data_formatada: str = Field(..., alias="Data Formatada")
    numero: int = Field(..., alias="Número")
    documento: str = Field(..., alias="Documento")
    descricao: str = Field(..., alias="Descrição")
    debito: Optional[float] = Field(default=0.0, alias="Débito")
    credito: Optional[float] = Field(default=0.0, alias="Crédito")
    conta: str = Field(..., alias="Conta")
    nome_conta: str = Field(..., alias="Nome Conta")

    @field_validator("data", mode="before")
    def parse_data_em_dd_mm_aaaa(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except Exception:
            return date(2025, 2, 1)  # valor seguro, ajusta se quiseres
