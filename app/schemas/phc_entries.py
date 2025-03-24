from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, ValidationError, field_validator
from typing import Optional

class PHCEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: date = Field(..., alias="Data")
    diario: str = Field(..., alias="Diário")
    numero: int = Field(..., alias="Nº")
    documento: str = Field(..., alias="Documento")
    descricao: str = Field(..., alias="Descrição")
    debito: float = Field(..., alias="Débito")
    credito: float = Field(..., alias="Crédito")
    centro_custo: Optional[str] = Field(default="", alias="Centro Custo")
    conta: str = Field(..., alias="Conta")
    nome_conta: str = Field(..., alias="Nome Conta")
    valor: float = Field(..., alias="Valor")
    abs_valor: float = Field(..., alias="ABS")
    id_interna: Optional[str] = Field(default="", alias="Id Interna")
    observacoes: Optional[str] = Field(default="", alias="Observações")

    @field_validator("data", mode="before")
    def parse_data_em_dd_mm_aaaa(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except ValidationError:
            return date(2025,2,1)