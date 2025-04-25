def mensagem_sucess(texto):
    print(f"\033[92m[SUCESS]\033[0m {texto}")

def mensagem_warning(texto):
    print(f"\033[93m[WARNING]\033[0m {texto}")

def mensagem_error(texto):
    print(f"\033[91m[ERROR]\033[0m {texto}")

def mensagem_info(texto):
    print(f"\033[94m[INFO]\033[0m {texto}")

def mensagem_debug(texto):
    print(f"\033[90m[DEBUG]\033[0m {texto}")