from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from app.models.sqlite.base import Base


class MovimentosBancariosPHC(Base):
    __tablename__ = "movimentos_bancarios_phc"

    id = Column(Integer, primary_key=True)
    data = Column(Date)
    data_formatada = Column(String)
    numero = Column(Integer)
    documento = Column(Integer)
    descricao = Column(String)
    debito = Column(Float)
    credito = Column(Float)
    conta = Column(String)
    nome_conta = Column(String)

    id_conta_bancaria = Column(Integer, ForeignKey("contas_bancarias.id"))

