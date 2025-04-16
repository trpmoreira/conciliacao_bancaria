from app.services.update_balance import update_balance
from app.services.check_movimento import check_movimentos_by_period
from app.services.importacao_bancos import importar_movimentos_banco
from app.services.importacao_phc import importar_movimentos_phc
from app.services.conciliacao import conciliacao_movimentos

def import_month(ano: int, mes: int):

    importar_movimentos_banco(ano, mes)
    print(f"Importados os movimentos bancários do período {ano}{mes:02d}")
    importar_movimentos_phc(ano, mes)
    print(f"Importados os movimentos do PHC do período {ano}{mes:02d}")
    check_movimentos_by_period(f"{ano}{mes:02d}")
    print(f"Validados os movimentos do período {ano}{mes:02d}")
    update_balance(f"{ano}{mes:02d}")
    print(f"Atualizados saldos do período {ano}{mes:02d}")
    conciliacao_movimentos(f"{ano}{mes:02d}")
    print(f"Conciliados os movimentos do período {ano}{mes:02d}")

