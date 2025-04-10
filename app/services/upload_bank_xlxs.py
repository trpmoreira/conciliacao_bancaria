import os
from fastapi import File, HTTPException, UploadFile


async def upload_bank_sheet(ano, mes, file: UploadFile = File(...)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="O ficheiro deve ser um ficheiro Excel")

    file_name = f"{ano:04d}{mes:02d}.xlsx"

    # Verifica se o ficheiro já existe
    file_location = f"files/bank_sheets/{file_name}"
    if os.path.exists(file_location):
        message = f"O ficheiro {file_name} já existe, foi substituido"
    else:
        message = f"O ficheiro {file_name} foi guardado com sucesso"

    contents = await file.read()

    # Guarda o ficheiro
    with open(file_location, "wb") as file_object:
        file_object.write(contents)

    return {"message": message}
