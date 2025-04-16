# app/models/sqlite/movimentos_phc.py
from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.sqlite.base import Base

class PHCMovimento(Base):
    __tablename__ = "phc_movimentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    diario = Column(String)
    lancamento = Column(Integer)
    documento = Column(String)
    descricao = Column(Text)
    debito = Column(Float)
    credito = Column(Float)
    centro_custo = Column(String)
    conta_phc = Column(String, nullable=False)
    nome_conta_phc = Column(String)
    valor = Column(Float)
    abs_valor = Column(Float)
    id_interna = Column(String)
    observacoes = Column(Text)

    ano_mes = Column(String, nullable=False)
    id_conta_bancaria = Column(Integer, ForeignKey("contas_bancarias.id"))

    conta_bancaria = relationship("ContaBancaria", back_populates="movimentos")
