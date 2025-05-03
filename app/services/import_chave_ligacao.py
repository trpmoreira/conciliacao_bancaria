import os

from fastapi import File, HTTPException, UploadFile
import pandas as pd
from app.models.sqlite.chave_ligacao import ChaveLigacao
from app.utils.messages import mensagem_debug, mensagem_error, mensagem_sucess, mensagem_warning
from app.session import get_session


def import_chave_ligacao():
    debug = True

    with get_session() as session:

      file_name = "chaveligacao.xlsx"
      path_ficheiro = os.path.join("files", file_name)

      data = pd.read_excel(path_ficheiro,
        dtype={
        "Conta PHC": str,
        "Nome Conta": str,
        "Conta Brasague": str,
        "Nome Conta Brasague": str,
        "CONTAGER": str,
        "CONTAAUX": str
        })

      if not data.empty:
          if debug:
            mensagem_debug(f"\n Lido o ficheiro \033[94m'{file_name}'\033[0m com sucesso")
      else:
          mensagem_error(f"O ficheiro \033[94m'{file_name}'\033[0m não tem dados")
          raise Exception(f"O ficheiro {file_name} não tem dados")

      # Insert data into the database
      for row in data.to_dict(orient="records"):
          chave_ligacao = ChaveLigacao(
              phc_conta=row["Conta PHC"],
              phc_nome=row["Nome Conta"],
              brasague_conta=row["Conta Brasague"],
              brasague_nome=row["Nome Conta Brasague"],
              brasague_contager=row["CONTAGER"],
              brasague_contaaux=row["CONTAAUX"],
          )
          session.add(chave_ligacao)
      session.commit()
      mensagem_sucess(f"Dados importados com sucesso")

      return {"message": "Dados importados com sucesso"}


async def get_chave_ligacao(file: UploadFile = File(...)):
    if not file.filename.endswith('.xlsx'):
      raise HTTPException(status_code=400, detail="O ficheiro deve ser um ficheiro Excel")

    file_name = "chaveligacao.xlsx"

    #TODO: fazer testes ao ficheiro para verificar se tem as colunas corretas

    # Verifica se o ficheiro já existe
    path_ficheiro = os.path.join("files", file_name)

    if os.path.exists(path_ficheiro):
        mensagem_warning(f"\n O ficheiro \033[94m'{file_name}'\033[0m já existe, será substituido")


    # Guarda o ficheiro
    try:
        contents = await file.read()
        with open(path_ficheiro, "wb") as file_object:
            file_object.write(contents)

        mensagem_sucess(f"\n O ficheiro \033[94m'{file_name}'\033[0m foi guardado com sucesso")
        message = f"O ficheiro {file_name} foi guardado com sucesso"
    except Exception as e:
        mensagem_error(f"\n Erro ao guardar o ficheiro \033[94m'{file_name}'\033[0m")
        message = f"Erro ao guardar o ficheiro {file_name}"
        raise HTTPException(status_code=500, detail=f"Erro ao guardar o ficheiro: {str(e)}")

    return {"message": message}
