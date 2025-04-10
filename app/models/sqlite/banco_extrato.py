# app/models/sqlite/banco_extrato.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.models.sqlite.base import Base

class BancoExtrato(Base):
    __tablename__ = "banco_extratos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_conta = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String(500))
    valor = Column(Float)
    codigo_mecanografico = Column(String)
    ano_mes = Column(String, nullable=False)


    banco_id = Column(Integer, ForeignKey("bancos.id"))
    id_conta_bancaria = Column(Integer, ForeignKey("contas_bancarias.id"))
