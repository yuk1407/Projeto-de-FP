import socket
import uuid

from dadosGlobais import *



# CONSULTAR MÁQUINAS BLOQUEADAS
def consultarBloqueadas():  # vai so pegar a lista de maquinas bloqueadas e colocar na lista de bloqueados 
    bloqueadas.clear()

    try:
        with open("maquinas_bloqueadas.txt", "r", encoding="utf8") as arquivo: #procedimento padrao ne
            for linha in arquivo:
                nome_maquina = linha.strip()

                if nome_maquina:
                    bloqueadas.append(nome_maquina)

    except FileNotFoundError:
        pass


# VERIFICAR SE A MÁQUINA ESTÁ BLOQUEADA
def maquinaBloqueada(maquina): #parte da verificação, padrão tbm so segue, genuinamente a mesma coisa que foi feita antes
    consultarBloqueadas()

    return maquina.lower() in [m.lower() for m in bloqueadas]


# LER O IDENTIFICADOR FIXO DO LINUX
def lerMachineId():
    try:
        with open("/etc/machine-id", "r", encoding="utf8") as arquivo:
            return arquivo.read().strip()[:6]
    except (FileNotFoundError, PermissionError):
        return None

# IDENTIFICAR ESTA MÁQUINA
def identificarMaquina():
    nome = socket.gethostname()
    if nome.replace(".", "").isdigit():
        nome = "MAQ"
    
    sufixo = lerMachineId()
    if sufixo is None:
        sufixo = f"{uuid.getnode():012x}"[-6:]
    return f"{nome}-{sufixo}"