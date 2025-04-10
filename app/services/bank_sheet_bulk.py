
import os
from app.services.importacao_bancos import importar_movimentos_banco


def bank_bulk_import(ano: int):
    resultados = {}

    for mes in range(1, 13):
        file_name = f"{ano:04d}{mes:02d}.xlsx"
        file_location = f"files/bank_sheets/{file_name}"

        if os.path.exists(file_location):
            try:
                resultado = importar_movimentos_banco(ano, mes)
                resultados[f"{ano}-{mes:02d}"] = resultado
            except Exception as e:
                resultados[f"{ano}-{mes:02d}"] = {"status": "erro", "mensagem": str(e)}
        else:
            resultados[f"{ano}-{mes:02d}"] = {"status": "não encontrado"}

    return resultados