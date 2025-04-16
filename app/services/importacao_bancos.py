from fastapi import HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.banco_extrato import BancoExtrato  # quando criares o modelo
from sqlalchemy.orm import sessionmaker
from app.db_info import delete_entries_by_account_and_period, engine_sqlite
import os

Session = sessionmaker(bind=engine_sqlite)

def importar_movimentos_banco(ano: int, mes: int):
    session = Session()

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
            deleted_entries[conta.id] = session.query(BancoExtrato).filter(BancoExtrato.id_conta_bancaria == conta.id, BancoExtrato.ano_mes == f"{ano}{mes:02d}").count()

            if deleted_entries[conta.id] > 0:
                session.query(BancoExtrato).filter(BancoExtrato.id_conta_bancaria == conta.id, BancoExtrato.ano_mes == f"{ano}{mes:02d}").delete()
                session.commit()
                print(f"Eliminados {deleted_entries[conta.id]} lançamentos da conta {conta.nome_conta} para o mês de {mes}/{ano}")

                # TODO: Transformar o eliminar numa função para estar acessivel a outros serviços o delete_entries_by_account_and_period não esta a funcionar

        except Exception as e:
            print(f"Erro ao eliminar lançamentos: {e}")

        try:
            df = pd.read_excel(path_ficheiro, sheet_name=conta.excel_nome_folha)
            print(f"Lido a folha '{conta.excel_nome_folha}' com sucesso")
        except Exception as e:
            print(f"Erro ao ler a folha '{conta.excel_nome_folha}': {e}")
            continue

        # Converte a coluna de datas de forma vetorizada
        #df.rename(columns={conta.excel_nome_data: "data"}, inplace=True)
        #df["data"] = pd.to_datetime(df["data"], errors='coerce', dayfirst=True).fillna(pd.Timestamp(f"{ano}-{mes:02d}-01"))

        coluna_data = conta.excel_nome_data
        if coluna_data not in df.columns:
            print(f"\033[33m[AVISO]\033[0m Coluna \033[32m'{coluna_data}'\033[0m não encontrada na folha \033[32m'{conta.excel_nome_folha}'\033[0m, criando 'data' com valor padrão")
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

        print(f"{new_entries[conta.id]} movimentos da conta {conta.nome_conta} importados com sucesso para o mês de {mes}/{ano}")

    message = f"Movimentos importados com sucesso para o mês de {mes}/{ano}"

    session.commit()

    return {"message": message, "deleted_entries": deleted_entries, "new_entries": new_entries}
