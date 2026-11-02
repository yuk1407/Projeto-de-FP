
from datetime import datetime
import os
os.system("cls")



dados = {}

def registrar():
    usuario = input("Qual o nome do usuário: ")

    if usuario in dados:
        print("O usuário já foi cadastrado.")
        return
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
    dados[usuario] = {
        "matricula": input("Matrícula: "),
        "perfil": input("Perfil (estudante, professor, administrador): "),
        "horario": input("Horário permitido (ex: 7h-18h): "),
        "maquina": input("Qual máquina foi usada: "),
        "observacoes": input("Observações (opcional): "),
        "acesso" : horario == datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
    }
    print("Usuário cadastrado com sucesso.")

    info = dados[usuario]  # atalho para o dicionário de dentro

    with open("arquivos.txt", "a", encoding="utf8") as arquivo:
        arquivo.write(f"{usuario},{info['matricula']},{info['perfil']},{info['horario']},{horario},{info['maquina']},{info['observacoes']}\n")

def vizualizar():
    dados = {}  # dicionário vazio, vai ser preenchido com o arquivo

    try:
        with open("arquivos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 4)
                if len(partes) < 5:
                    continue
                nome, matricula, perfil, horario, observacoes = partes
                dados[nome] = {
                    "matricula": matricula,
                    "perfil": perfil,
                    "horario": horario,
                    "observacoes": observacoes
                }
    except FileNotFoundError:
        pass

    if len(dados) == 0:
        print("Não há nada no registro.")
        return

    pergunta = input("Qual o usuário que você deseja checar: ")

    if pergunta in dados:
        info = dados[pergunta]
        matricula = info["matricula"]
        matricula_oculta = matricula[:2] + "*" * max(0, len(matricula) - 2)

        print("-------------------------")
        print("Nome:", pergunta)
        print("Matricula:", matricula_oculta)
        print("Perfil:", info["perfil"])
        print("Horario:", info["horario"])
        print("Observacoes:", info["observacoes"])
    else:
        print("O usuário não foi cadastrado.")

def matricula():
    dados = {}  # dicionário vazio, vai ser preenchido com o arquivo

    try:
        with open("arquivos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 6)
                if len(partes) < 7:
                    continue
                nome, matricula, perfil, horario, acesso, maquina, observacoes = partes
                dados[nome] = {
                    "matricula": matricula,
                    "perfil": perfil,
                    "horario": horario,
                    "acesso": acesso,
                    "maquina": maquina,
                    "observacoes": observacoes
                }
    except FileNotFoundError:
        pass

    if len(dados) == 0:
        print("Não há nada no registro.")
        return

    busca = input("Digite o nome do usuário que deseja revelar a matrícula: ")

    if busca in dados:
        print("Matricula completa:", dados[busca]["matricula"])
    else:
        print("Usuário não encontrado.")

def atualizar():
    dados = {}  # dicionário vazio, vai ser preenchido com o arquivo

    try:
        with open("arquivos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 6)
                if len(partes) < 7:
                    continue
                nome, matricula, perfil, horario, acesso, maquina, observacoes = partes
                dados[nome] = {
                    "matricula": matricula,
                    "perfil": perfil,
                    "horario": horario,
                    "acesso": acesso,
                    "maquina": maquina,
                    "observacoes": observacoes
                }
    except FileNotFoundError:
        pass

    if len(dados) == 0:
        print("Não há nada no registro.")
        return

    matricula_busca = input("Digite a matrícula do usuário que deseja atualizar: ")

    nome_encontrado = None
    for nome, info in dados.items():
        if info["matricula"] == matricula_busca:
            nome_encontrado = nome
            break

    if nome_encontrado is None:
        print("Usuário não encontrado.")
        return

    info = dados[nome_encontrado]

    print("Digite os novos valores (deixe em branco para manter o valor atual):")
    novo_nome = input(f"Nome ({nome_encontrado}): ") or nome_encontrado
    info["perfil"] = input(f"Perfil ({info['perfil']}): ") or info["perfil"]
    info["horario"] = input(f"Horário permitido ({info['horario']}): ") or info["horario"]
    info["maquina"] = input(f"Máquina ({info['maquina']}): ") or info["maquina"]
    info["observacoes"] = input(f"Observações ({info['observacoes']}): ") or info["observacoes"]

    if novo_nome != nome_encontrado:
        if novo_nome in dados:
            print("Já existe um usuário com esse nome. O nome não foi alterado.")
        else:
            dados[novo_nome] = dados.pop(nome_encontrado)

    with open("arquivos.txt", "w", encoding="utf8") as arquivo:
        for nome, info in dados.items():
            arquivo.write(f"{nome},{info['matricula']},{info['perfil']},{info['horario']},{info['acesso']},{info['maquina']},{info['observacoes']}\n")

    print("Usuário atualizado com sucesso.")



def deletar():
    dados = {}  # dicionário vazio, vai ser preenchido com o arquivo

    try:
        with open("arquivos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 6)
                if len(partes) < 7:
                    continue
                nome, matricula, perfil, horario, acesso, maquina, observacoes = partes
                dados[nome] = {
                    "matricula": matricula,
                    "perfil": perfil,
                    "horario": horario,
                    "acesso": acesso,
                    "maquina": maquina,
                    "observacoes": observacoes
                }
    except FileNotFoundError:
        pass

    if len(dados) == 0:
        print("Não há nada no registro.")
        return

    matricula_busca = input("Digite a matrícula do usuário que deseja deletar: ")

    nome_encontrado = None
    for nome, info in dados.items():
        if info["matricula"] == matricula_busca:
            nome_encontrado = nome
            break

    if nome_encontrado is None:
        print("Usuário não encontrado.")
        return

    del dados[nome_encontrado]  # remove o usuário do dicionário

    with open("arquivos.txt", "w", encoding="utf8") as arquivo:
        for nome, info in dados.items():
            arquivo.write(f"{nome},{info['matricula']},{info['perfil']},{info['horario']},{info['acesso']},{info['maquina']},{info['observacoes']}\n")

    print("Usuário deletado com sucesso.")





while True: # MENU PRINCIPAL
    print("\n=== Sentinelalog ===")
    print("1. Registrar usuário")
    print("2. Visualizar usuários")
    print("3. Atualizar usuário")
    print("4. Deletar usuário")
    print("5. Matrícula oculta")
    print("6. Sair")

    opcao = input("Escolha uma opção: ") # parte das opçoes do menu principal
    if opcao == "1":
        registrar()
    elif opcao == "2":
        vizualizar()
    elif opcao == "3":
        atualizar()
    elif opcao == "4":
        deletar()
    elif opcao == "5":
        matricula()
    elif opcao == "6":
        break
    else:
        print("Opção inválida. Tente novamente  .")
