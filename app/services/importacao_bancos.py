from fastapi import HTTPException
import pandas as pd
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.banco_extrato import BancoExtrato  # quando criares o modelo
from app.session import get_session
from app.services.messages import mensagem_debug, mensagem_error, mensagem_sucess, mensagem_warning
import os

def importar_movimentos_banco(ano: int, mes: int):
    debug = False

    with get_session() as session:

        ano_mes = f"{ano:04d}{mes:02d}"
        ficheiro_nome = f"{ano_mes}.xlsx"
        path_ficheiro = os.path.join("files", "bank_sheets", ficheiro_nome)

        if not os.path.exists(path_ficheiro):
            raise HTTPException(status_code=404, detail=f"Ficheiro {ficheiro_nome} não encontrado")

        deleted_entries = {}
        new_entries = {}

        contas = session.query(ContaBancaria).all()

        for conta in contas:
            new_entries[conta.id] = 0

            try:
                df = pd.read_excel(path_ficheiro, sheet_name=conta.excel_nome_folha)
                if debug:
                    mensagem_debug(f"\n Lido a folha \033[94m'{conta.excel_nome_folha}'\033[0m com sucesso")
            except Exception as e:
                mensagem_error(f"Erro ao ler a folha \033[94m'{conta.excel_nome_folha}'\033[0m: {e}")
                continue

            try:
                deleted_entries[conta.id] = session.query(BancoExtrato).filter(BancoExtrato.id_conta_bancaria == conta.id, BancoExtrato.ano_mes == f"{ano}{mes:02d}").count()

                if deleted_entries[conta.id] > 0:
                    session.query(BancoExtrato).filter(BancoExtrato.id_conta_bancaria == conta.id, BancoExtrato.ano_mes == f"{ano}{mes:02d}").delete()
                    session.commit()
                    if debug:
                        mensagem_debug(f"\033[91mEliminados {deleted_entries[conta.id]} lançamentos\033[0m da conta \033[94m{conta.nome_conta}\033[0m para o mês de \033[94m{mes}/{ano}\033[0m")

                    # TODO: Transformar o eliminar numa função para estar acessivel a outros serviços o delete_entries_by_account_and_period não esta a funcionar

            except Exception as e:
                mensagem_error(f"Erro ao eliminar lançamentos: {e}")

            coluna_data = conta.excel_nome_data
            if coluna_data not in df.columns:
                mensagem_warning(f"Coluna \033[94m'{coluna_data}'\033[0m não encontrada na folha \033[94m'{conta.excel_nome_folha}'\033[0m, criando 'data' com valor padrão")
                df["data"] = pd.Timestamp(f"{ano}-{mes:02d}-01")
            else:
                df.rename(columns={coluna_data: "data"}, inplace=True)
                df["data"] = pd.to_datetime(df["data"], errors='coerce', dayfirst=True).fillna(pd.Timestamp(f"{ano}-{mes:02d}-01"))

            for _, row in df.iterrows():

                descricao = str(row.get(conta.excel_nome_descricao, ""))
                valor = row.get(conta.excel_nome_valor, 0)
                codigo_mecanografico = row.get(conta.excel_nome_codigo_mecanografico, "")
                data = row["data"].date()


                movimento = BancoExtrato(
                    nome_conta=conta.nome_conta,
                    data=data,
                    descricao=descricao,
                    valor=valor,
                    codigo_mecanografico=codigo_mecanografico,
                    ano_mes=ano_mes,
                    banco_id=conta.id_banco,
                    id_conta_bancaria=conta.id
                )
                session.add(movimento)
                new_entries[conta.id] = new_entries.get(conta.id, 0) + 1

                if debug:
                    mensagem_debug(f"\033[92mImportados {new_entries[conta.id]} movimentos\033[0m da conta \033[94m{conta.nome_conta}\033[0m para o mês de \033[94m{mes}/{ano}\033[0m")

        message = f"Movimentos bancários importados com sucesso para o mês de {mes}/{ano}"
        mensagem_sucess(f"Movimentos bancários importados com sucesso para o mês de \033[94m{mes:02d}/{ano}\033[0m")

        session.commit()

    return {"message": message, "deleted_entries": deleted_entries, "new_entries": new_entries}
