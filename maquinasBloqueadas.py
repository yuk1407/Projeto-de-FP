from dadosGlobais import *

# CONSULTAR MÁQUINAS BLOQUEADAS
def consultarBloqueadas():
    bloqueadas.clear()

    try:
        with open("maquinas_bloqueadas.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                nome_maquina = linha.strip()

                if nome_maquina:
                    bloqueadas.append(nome_maquina)

    except FileNotFoundError:
        pass


# VERIFICAR SE A MÁQUINA ESTÁ BLOQUEADA
def maquinaBloqueada(maquina):
    consultarBloqueadas()

    return maquina.lower() in [m.lower() for m in bloqueadas]


def bloquearMaquinaAutomatico(nome_maquina):
    if not nome_maquina:
        return
    
    if nome_maquina.lower() in [m.lower() for m in bloqueadas]:
        return
    
    with open("maquinas_bloqueadas.txt", "a", encoding="utf8") as arquivo:
        arquivo.write(f"{nome_maquina}\n")
        print("maquina atual bloqueada!")
    

