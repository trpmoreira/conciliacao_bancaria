from sqlalchemy import func
from app.models.sqlite.banco_extrato import BancoExtrato
from app.models.sqlite.conciliacao_movimentos import ConciliacaoMovimentos
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.movimentos_phc import PHCMovimento
from app.session import get_session


def conciliacao_movimentos(periodo: str):
  with get_session() as session:

    accounts = session.query(ContaBancaria).all()

    for account in accounts:
      movimentos = session.query(BancoExtrato).filter(BancoExtrato.id_conta_bancaria == account.id, BancoExtrato.ano_mes == periodo).all()

      for movimento in movimentos:

        phc_valor = session.query(
            func.sum(PHCMovimento.valor)
        ).filter(
            PHCMovimento.id_conta_bancaria == account.id,
            PHCMovimento.ano_mes == periodo,
            PHCMovimento.documento == movimento.codigo_mecanografico
        ).scalar()

        if not phc_valor:
          phc_valor = 0

        session.add(ConciliacaoMovimentos(
          id_conta_bancaria=movimento.id_conta_bancaria,
          ano_mes=periodo,
          data_movimento=movimento.data,
          descricao=movimento.descricao,
          valor_banco=movimento.valor,
          valor_phc=phc_valor,
          valor_diferenca=movimento.valor - phc_valor,
          codigo_mecanografico=movimento.codigo_mecanografico
        ))

        session.commit()
