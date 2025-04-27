

from sqlalchemy import extract
from app.db_info import get_bank_entries_by_date_account
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.movimentos_bancarios_phc import MovimentosBancariosPHC
from app.services.messages import mensagem_debug, mensagem_error, mensagem_sucess
from app.session import get_session


def import_bank_entries(ano: int, mes: int):
  debug = True

  with get_session() as session:
    contas = session.query(ContaBancaria).all()

    for conta in contas:
      if debug:
        mensagem_debug(f"\nA processar conta \033[94m{conta.conta_phc}\033[0m - \033[94m{conta.nome_conta}\033[0m")

      success, msg, entries = get_bank_entries_by_date_account(ano, mes, conta.conta_phc)

      if debug:
        mensagem_debug(f"\033[91m{len(entries)} lançamentos encontrados\033[0m")

      if not success:
        mensagem_error(f"Erro ao procurar movimentos: {msg}")
        continue

      deleted_entries = session.query(MovimentosBancariosPHC).filter(
        MovimentosBancariosPHC.conta == conta.conta_phc,
        extract('month', MovimentosBancariosPHC.data) == mes,
        extract('year', MovimentosBancariosPHC.data) == ano
      ).count()


      session.query(MovimentosBancariosPHC).filter(
        MovimentosBancariosPHC.conta == conta.conta_phc,
        extract('month', MovimentosBancariosPHC.data) == mes,
        extract('year', MovimentosBancariosPHC.data) == ano
      ).delete()

      if debug:
        mensagem_debug(f"\033[91mEliminados {deleted_entries} lançamentos\033[0m da conta \033[94m{conta.nome_conta}\033[0m para o mês de \033[94m{mes}/{ano}\033[0m")

      for entry in entries:
        try:
          movimento = MovimentosBancariosPHC(
            data = entry.data,
            data_formatada = entry.data_formatada,
            numero = entry.numero,
            documento = entry.documento,
            descricao = entry.descricao,
            debito = entry.debito,
            credito = entry.credito,
            conta = entry.conta,
            nome_conta = entry.nome_conta,
            id_conta_bancaria=conta.id
          )
          session.add(movimento)
        except Exception as e:
          mensagem_error(f"Erro ao importar movimento: {e}")
          continue

      session.commit()

      if debug:
        mensagem_debug(f"\033[92mImportados {len(entries)} lançamentos\033[0m da conta \033[94m{conta.nome_conta}\033[0m para o mês de \033[94m{mes}/{ano}\033[0m")

  mensagem_sucess(f"Importação de lançamentos bancários concluída com sucesso para o mês de \033[94m{mes}/{ano}\033[0m")
  msg = f"Importação de lançamentos bancários concluída com sucesso para o mês de {mes}/{ano}"
  return True, msg

