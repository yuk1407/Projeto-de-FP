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


def bloquearMaquinaAutomatico(nome_maquina):
    if not nome_maquina:
        return
    
    if nome_maquina.lower() in [m.lower() for m in bloqueadas]:
        return
    
    with open("maquinas_bloqueadas.txt", "a", encoding="utf8") as arquivo:
        arquivo.write(f"{nome_maquina}\n")
        print("maquina atual bloqueada!")
    

