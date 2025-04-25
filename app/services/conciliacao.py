from sqlalchemy import func
from app.models.sqlite.banco_extrato import BancoExtrato
from app.models.sqlite.conciliacao_movimentos import ConciliacaoMovimentos
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.movimentos_phc import PHCMovimento
from app.services.messages import mensagem_debug, mensagem_error, mensagem_sucess
from app.session import get_session


def conciliacao_movimentos(periodo: str):

  debug = False

  with get_session() as session:

    # Apagar os movimentos já conciliados para este período
    try:
      count = session.query(ConciliacaoMovimentos).filter(ConciliacaoMovimentos.ano_mes == periodo).count()
      session.query(ConciliacaoMovimentos).filter(ConciliacaoMovimentos.ano_mes == periodo).delete()
      if debug:
        mensagem_debug(f"\033[91mEliminados {count} movimentos já conciliados\033[0m para o período \033[94m{periodo[4:]}/{periodo[:4]}\033[0m")
    except Exception as e:
      mensagem_error(f"Erro ao apagar movimentos já conciliados para o período {periodo}: {e}")

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

        valor_banco = movimento.valor

        if not isinstance(valor_banco, (int, float)):
          valor_banco = 0
          mensagem_error(f"Movimento do bancário \033[94m{movimento.codigo_mecanografico}\033[0m da conta \033[94m{movimento.nome_conta}\033[0m não tem valor")

        if not movimento.codigo_mecanografico:
          movimento.codigo_mecanografico = "ERROR"
          mensagem_error(f"Movimento do {movimento.nome_conta} não tem código mecanográfico")

        session.add(ConciliacaoMovimentos(
          id_conta_bancaria=movimento.id_conta_bancaria,
          ano_mes=periodo,
          data_movimento=movimento.data,
          descricao=movimento.descricao,
          valor_banco=valor_banco,
          valor_phc=phc_valor,
          valor_diferenca=valor_banco - phc_valor,
          codigo_mecanografico=movimento.codigo_mecanografico
        ))

        session.commit()

  mensagem_sucess(f"Movimentos conciliados com sucesso para o período \033[94m{periodo[4:]}/{periodo[:4]}\033[0m")
