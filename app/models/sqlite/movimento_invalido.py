

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from app.models.sqlite.base import Base


class MovimentosInvalidos(Base):
    __tablename__ = "movimentos_invalidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    atualizado_em = Column(DateTime, nullable=False)
    diario = Column(String)
    lancamento = Column(Integer)
    documento = Column(String)
    valor = Column(Float, nullable=False)
    observacao = Column(String, nullable=False)
    ano_mes = Column(String, nullable=False)

    id_conta_bancaria = Column(Integer, ForeignKey("contas_bancarias.id"))
