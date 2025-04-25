import datetime
from sqlalchemy import func

from app.models.sqlite.banco_extrato import BancoExtrato
from app.models.sqlite.bancos_saldos import BancosSaldos
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.movimentos_phc import PHCMovimento
from app.services.messages import mensagem_debug, mensagem_sucess, mensagem_warning
from app.session import get_session


def update_balance(period: str):

    debug = False

    with get_session() as session:

        # Get all accounts
        accounts = session.query(ContaBancaria).all()

        balances = session.query(BancosSaldos).filter(BancosSaldos.ano_mes == period).count()

        if balances > 0:
            session.query(BancosSaldos).filter(BancosSaldos.ano_mes == period).delete()
            session.commit()
            if debug:
                mensagem_debug(f"\033[91mEliminados os saldos do mês {period}\033[0m")


        for account in accounts:

            account_balance = session.query(func.sum(BancoExtrato.valor).label('total_valor')).filter(
                BancoExtrato.id_conta_bancaria == account.id, BancoExtrato.ano_mes == period).scalar()

            phc_balance = session.query(func.sum(PHCMovimento.valor).label('total_valor')).filter(
                PHCMovimento.id_conta_bancaria == account.id, PHCMovimento.ano_mes == period).scalar()

            def safe_number(account, value, name):
                if isinstance(value, (int, float)):
                    return value
                try:
                    return float(value)
                except (TypeError, ValueError):
                    mensagem_warning(
                        f"Valor inválido na conta \033[32m{account.nome_conta}\033[0m para '{name}': {value}. A assumir 0.")
                return 0.0

            # uso:
            account_balance_safe = safe_number(account, account_balance, 'account_balance')
            phc_balance_safe = safe_number(account, phc_balance, 'phc_balance')

            diferenca = account_balance_safe - phc_balance_safe

            session.add(BancosSaldos(
                saldo_phc = phc_balance_safe,
                saldo_bancos = account_balance_safe,
                diferenca = diferenca,
                ano_mes = period,
                last_updated = datetime.datetime.now(),
                account_id = account.id
            ))

            session.commit()

        mensagem_sucess(f"Saldos atualizados com sucesso para o mês \033[94m{period[4:]}/{period[:4]}\033[0m")
    return {"Status": "OK", "Message": f"Saldos atualizados com sucesso para o mês {period}"}
