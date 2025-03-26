# app/models/banco.py
from sqlalchemy import Column, Integer, String
from app.models.sqlite.base import Base


class Banco(Base):
    __tablename__ = "bancos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_banco = Column(String, nullable=False)          # Ex: "Santander"
    nome_conta = Column(String, nullable=False)          # Ex: "Santander DO"
    conta_phc = Column(String, nullable=False)           # Ex: "120101"
    nome_folha = Column(String, nullable=False)          # Ex: "santander"
    codigo_banco = Column(String, nullable=False)        # Ex: "01"
