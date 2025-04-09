# app/models/sqlite/conta_bancaria.py
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.sqlite.base import Base


class ContaBancaria(Base):
    __tablename__ = "contas_bancarias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_conta = Column(String, nullable=False)
    conta_phc = Column(String, nullable=False, unique=True)
    excel_nome_folha = Column(String, nullable=False, unique=True)
    excel_nome_descricao = Column(String, nullable=False)
    excel_nome_valor = Column(String, nullable=False)
    excel_nome_codigo_mecanografico = Column(String, nullable=False)
    excel_nome_data = Column(String, nullable=False)
    codigo_banco = Column(String, nullable=False, unique=True)


    id_banco = Column(Integer, ForeignKey("bancos.id"))
    movimentos = relationship("PHCMovimento", back_populates="conta_bancaria")

