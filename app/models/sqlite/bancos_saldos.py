

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from app.models.sqlite.base import Base


class BancosSaldos(Base):
    __tablename__ = "bancos_saldos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    saldo_phc = Column(Float, nullable=False)
    saldo_bancos = Column(Float, nullable=False)
    diferenca = Column(Float, nullable=False)
    ano_mes = Column(String, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    account_id = Column(Integer, ForeignKey("contas_bancarias.id"))
