import os
from datetime import datetime
from crud import *
from dadosGlobais import *
from manipularAcessos import *
from maquinasBloqueadas import *
from permissaoADM import *

#arquivo principal





# PROGRAMA PRINCIPAL
def main():
    limpar()

    primeiro_acesso()

    # Carrega o histórico de acessos
    consultarAcessos()

    while True:

        print("\n=== SentinelLog ===")
        print("1. Login")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            matricula_logada, perfil = login()

            if perfil == "estudante":
                perfil_estudante(matricula_logada)

            elif perfil == "professor":
                perfil_professor(matricula_logada)

            elif perfil == "administrador":
                perfil_administrador(matricula_logada)

        elif opcao == "0":
            print("Encerrando o SentinelLog...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
