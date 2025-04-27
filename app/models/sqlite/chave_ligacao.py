from sqlalchemy import Column, Integer, String
from app.models.sqlite.base import Base


class ChaveLigacao(Base):
    __tablename__ = "chave_ligacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phc_conta = Column(String, nullable=False, unique=True)
    phc_nome = Column(String, nullable=False)
    brasague_conta = Column(String)
    brasague_nome = Column(String)
    brasague_contager = Column(String)
    brasague_contaaux = Column(String)