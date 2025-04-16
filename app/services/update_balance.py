import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session, sessionmaker
from app.db_info import engine_sqlite

from app.models.sqlite.banco_extrato import BancoExtrato
from app.models.sqlite.bancos_saldos import BancosSaldos
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.movimentos_phc import PHCMovimento

Session = sessionmaker(bind=engine_sqlite)


def update_balance(period: str):
    session = Session()

    # Get all accounts
    accounts = session.query(ContaBancaria).all()

    balances = session.query(BancosSaldos).filter(BancosSaldos.ano_mes == period).count()

    if balances > 0:
        session.query(BancosSaldos).filter(BancosSaldos.ano_mes == period).delete()
        session.commit()
        print(f"Eliminados os saldos do mês {period}")


    for account in accounts:

        account_balance = session.query(func.sum(BancoExtrato.valor).label('total_valor')).filter(
            BancoExtrato.id_conta_bancaria == account.id, BancoExtrato.ano_mes == period).scalar()

        phc_balance = session.query(func.sum(PHCMovimento.valor).label('total_valor')).filter(
            PHCMovimento.id_conta_bancaria == account.id, PHCMovimento.ano_mes == period).scalar()

        def safe_number(value, name):
            if isinstance(value, (int, float)):
                return value
            try:
                return float(value)
            except (TypeError, ValueError):
                print(
                    f"[AVISO] Valor inválido para '{name}': {value}. A assumir 0.")
            return 0.0

        # uso:
        account_balance_safe = safe_number(account_balance, 'account_balance')
        phc_balance_safe = safe_number(phc_balance, 'phc_balance')

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

    return {"Status": "OK", "Message": f"Saldos atualizados com sucesso para o mês {period}"}
