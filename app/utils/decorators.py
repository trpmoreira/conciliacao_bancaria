import functools

from app.db_info import test_phc_connection
from app.utils.messages import mensagem_error

def test_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      status = test_phc_connection()
      if status['Status'] == 'OK':
        return func(*args, **kwargs)
      else:
        return mensagem_error(status['Message'])
    return wrapper

