

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from app.models.sqlite.base import Base


class ConciliacaoMovimentos(Base):
    __tablename__ = 'conciliacao_movimentos'

    id = Column(Integer, primary_key=True)
    id_conta_bancaria = Column(Integer, ForeignKey('contas_bancarias.id'))
    ano_mes = Column(String, nullable=False)
    data_movimento = Column(Date, nullable=False)
    descricao = Column(String)
    valor_banco = Column(Float)
    valor_phc = Column(Float)
    valor_diferenca = Column(Float)
    codigo_mecanografico = Column(String, nullable=False)

