from app.services.messages import mensagem_info, mensagem_sucess
from app.services.update_balance import update_balance
from app.services.check_movimento import check_movimentos_by_period
from app.services.importacao_bancos import importar_movimentos_banco
from app.services.importacao_phc import importar_movimentos_phc
from app.services.conciliacao import conciliacao_movimentos

def import_month(ano: int, mes: int):

    print("\n")
    mensagem_info(f"Iniciando importação do mês \033[94m{mes:02d}/{ano}\033[0m")
    importar_movimentos_banco(ano, mes)
    importar_movimentos_phc(ano, mes)
    check_movimentos_by_period(f"{ano}{mes:02d}")
    update_balance(f"{ano}{mes:02d}")
    conciliacao_movimentos(f"{ano}{mes:02d}")
    mensagem_sucess(f"Importação do mês \033[94m{mes:02d}/{ano}\033[0m concluída com sucesso")
    print("\n")

