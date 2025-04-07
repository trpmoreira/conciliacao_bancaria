# app/models/sqlite/banco.py
from sqlalchemy import Column, Integer, String
from app.models.sqlite.base import Base


class Banco(Base):
    __tablename__ = "bancos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_banco = Column(String, nullable=False, unique=True)
