import datetime

from app.models.sqlite.conta_bancaria import ContaBancaria
from app.models.sqlite.movimento_invalido import MovimentosInvalidos
from app.models.sqlite.movimentos_phc import PHCMovimento
from app.utils.messages import mensagem_debug, mensagem_sucess, mensagem_warning
from app.session import get_session



def adicionar_movimento_invalido(movimento: PHCMovimento, observacao: str):
  with get_session() as session:

    mensagem_warning(f"Adicionando movimento inválido {movimento.documento} - {observacao}")

    session.add(MovimentosInvalidos(
      atualizado_em=datetime.datetime.now()
      ,diario=movimento.diario
      ,lancamento=movimento.lancamento
      ,documento=movimento.documento
      ,valor=movimento.valor
      ,observacao=observacao
      ,ano_mes=movimento.ano_mes
      ,id_conta_bancaria=movimento.id_conta_bancaria
      ))
    session.commit()

def check_movimento_valido(movimento: PHCMovimento):
  with get_session() as session:

    debug = False

    codigo_banco = session.query(ContaBancaria.codigo_banco).filter(ContaBancaria.id == movimento.id_conta_bancaria).scalar()

    cod_mecanografico = movimento.documento

    if not cod_mecanografico or len(cod_mecanografico) != 11:
      adicionar_movimento_invalido(movimento, "Código mecanográfico inválido ou ausente")
      return

    if cod_mecanografico[0] != "B":
      adicionar_movimento_invalido(movimento, "Código mecanográfico inválido, não começa com 'B'")
      return

    if len(cod_mecanografico) != 11:
      adicionar_movimento_invalido(movimento, "Código mecanográfico inválido, não tem 11 dígitos")
      return

    if cod_mecanografico[1:3] != movimento.ano_mes[2:4]:
      adicionar_movimento_invalido(movimento, "Código mecanográfico inválido, o ano não corresponde ao movimento")
      return

    if cod_mecanografico[3:5] != movimento.ano_mes[4:6]:
      adicionar_movimento_invalido(movimento, "Código mecanográfico inválido, o mês não corresponde ao movimento")
      return

    if cod_mecanografico[5:7] != codigo_banco:
      adicionar_movimento_invalido(movimento, "Código mecanográfico inválido, o código do banco não corresponde ao movimento")
      return

    if debug:
      mensagem_debug(f"Movimento {movimento.documento} validado com sucesso")
    return

def check_movimentos_by_period(period: str):

  delete_invalid_movimentos_by_period(period)

  with get_session() as session:

    movimentos = session.query(PHCMovimento).filter(PHCMovimento.ano_mes == period).all()

    for movimento in movimentos:
      check_movimento_valido(movimento)

    mensagem_sucess(f"Movimentos validados com sucesso para o período \033[94m{period[4:]}/{period[:4]}\033[0m")

def delete_invalid_movimentos_by_period(period: str):

  debug = False

  with get_session() as session:

    deleted_entries = session.query(MovimentosInvalidos).filter(MovimentosInvalidos.ano_mes == period).count()
    session.query(MovimentosInvalidos).filter(MovimentosInvalidos.ano_mes == period).delete()
    session.commit()
    if debug:
      mensagem_debug(f"\033[91mEliminados {deleted_entries} movimentos inválidos\033[0m para o período \033[94m{period[4:]}/{period[:4]}\033[0m")
