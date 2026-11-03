import os
from datetime import datetime

dados = {}


# CONSULTAR OS DADOS DO ARQUIVO
def consultar(): # FUNÇÂO PARA CONSULTAR OS DADOS DO ARQUIVO

    dados.clear()

    try:
        with open("arquivos.txt", "r", encoding="utf8") as arquivo: #ABRIR O ARQUIVO PARA LEITURA
                for linha in arquivo:
                    partes = linha.strip().split(",", 6)

                    if len(partes) < 7:
                        continue

                    matricula, nome, perfil, horario, acesso, maquina, observacoes = partes

                    dados[matricula] = { #ATRIBUIR OS DADOS DO ARQUIVO PARA O DICIONÁRIO
                        "nome": nome,
                        "perfil": perfil,
                        "horario": horario,
                        "acesso": acesso,
                        "maquina": maquina,
                        "observacoes": observacoes
                }

    except FileNotFoundError: #CASO O ARQUIVO NÃO EXISTA
        pass


# SALVAR ALTERAÇÕES NO ARQUIVO
def salvar(): 
    with open("arquivos.txt", "w", encoding="utf8") as arquivo:
        for matricula, info in dados.items(): #ESCREVE OS DADOS DO DICIONÁRIO NO ARQUIVO
            arquivo.write(
                f"{matricula},{info['nome']},{info['perfil']},"
                f"{info['horario']},{info['acesso']},"
                f"{info['maquina']},{info['observacoes']}\n"
            )

def salvarRelatório(relatorio): 
    with open("relatorio.txt", "w", encoding="utf8") as arquivo:
        arquivo.write(relatorio)
# REGISTRAR USUÁRIO
def registrar():
    os.system("cls")
    consultar()

    matricula = input("Qual a matrícula do usuário: ")

    if matricula in dados: #CASO A MATRICLA JÁ EXISTA
        print("O usuário já foi cadastrado.")
        return

    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    dados[matricula] = { #ATRIBUIR OS DADOS DO USUÁRIO PARA O DICIONÁRIO
        "nome": input("Nome: "),
        "perfil": input("Perfil (estudante, professor, administrador): "),
        "horario": input("Horário permitido (ex: 7h-18h): "),
        "maquina": input("Qual máquina foi usada: "),
        "observacoes": input("Observações (opcional): "),
        "acesso": horario
    }

    salvar()

    print("Usuário cadastrado com sucesso.")


# VISUALIZAR USUÁRIO
def visualizar():
    os.system("cls")
    consultar()

    if len(dados) == 0:
        print("Não há nada no registro.")
        return

    pergunta = input("Qual o usuário que você deseja checar: ")

    encontrado = False

    for matricula, info in dados.items():

        if info["nome"].lower() == pergunta.lower():

            matricula_oculta = matricula[:2] + "*" * max(0, len(matricula) - 2)

            print("\n-------------------------")
            print("Nome:", info["nome"])
            print("Matricula:", matricula_oculta)
            print("Perfil:", info["perfil"])
            print("Horario:", info["horario"])
            print("Último acesso:", info["acesso"])
            print("Máquina:", info["maquina"])
            print("Observacoes:", info["observacoes"])
            print("-------------------------")

            encontrado = True
            break

    if not encontrado:
        print("O usuário não foi cadastrado.")


# ATUALIZAR USUÁRIO
def atualizarADM():
    os.system("cls")
    consultar()

    matricula = input("Digite a matrícula do usuário que deseja atualizar: ")

    if matricula not in dados:
        print("O usuário não foi cadastrado.")
        return

    info = dados[matricula]

    print("Deixe vazio para manter o dado atual.")

    nome = input(f"Nome ({info['nome']}): ")
    perfil = input(f"Perfil ({info['perfil']}): ")
    horario = input(f"Horário ({info['horario']}): ")
    maquina = input(f"Máquina ({info['maquina']}): ")
    observacoes = input(f"Observações ({info['observacoes']}): ")

    if nome:
        info["nome"] = nome

    if perfil:
        info["perfil"] = perfil

    if horario:
        info["horario"] = horario

    if maquina:
        info["maquina"] = maquina

    if observacoes:
        info["observacoes"] = observacoes

    salvar()

    print("Usuário atualizado com sucesso.")

# ATUALIZAR USUÁRIO
def atualizarESTUDANTE():
    os.system("cls")
    consultar()

    matricula = input("Digite a sua matricula: ")

    if matricula not in dados:
        print("O usuário não foi cadastrado.")
        return

    info = dados[matricula]

    print("Deixe vazio para manter o dado atual.")

    nome = input(f"Nome ({info['nome']}): ")

    observacoes = input(f"Observações ({info['observacoes']}): ")

    if nome:
        info["nome"] = nome

    if observacoes:
        info["observacoes"] = observacoes

    salvar()

    print("Usuário atualizado com sucesso.")

# ATUALIZAR USUÁRIO
def atualizarPROFESSOR():
    os.system("cls")
    consultar()

    matricula = input("Digite a sua matrícula : ")

    if matricula not in dados:
        print("O usuário não foi cadastrado.")
        return

    info = dados[matricula]

    print("Deixe vazio para manter o dado atual.")

    nome = input(f"Nome ({info['nome']}): ")

    observacoes = input(f"Observações ({info['observacoes']}): ")

    if nome:
        info["nome"] = nome


    if observacoes:
        info["observacoes"] = observacoes

    salvar()

    print("Usuário atualizado com sucesso.")


# DELETAR USUÁRIO
def deletar():
    os.system("cls")
    consultar()

    matricula = input("Digite a matrícula do usuário que deseja deletar: ")

    if matricula in dados:

        confirmacao = input("Deseja realmente deletar? (s/n): ")

        if confirmacao.lower() == "s":
            del dados[matricula]
            salvar()
            print("Usuário deletado com sucesso.")

        else:
            print("Operação cancelada.")

    else:
        print("O usuário não foi cadastrado.")


# MATRÍCULA OCULTA
def matricula():
    os.system("cls")
    consultar()

    nome = input("Digite o nome do usuário: ")

    encontrado = False

    for numero, info in dados.items():

        if info["nome"].lower() == nome.lower():

            print("Matrícula:", numero)

            encontrado = True
            break

    if not encontrado:
        print("O usuário não foi cadastrado.")


def criarRelatorio():
    consultar()
    relatorio = f"{"Matrícula":>10}{"Nome":>12}{"Perfil":>12}{"Acesso":>20}{"Maquina":>9}{"Observações":>15}\n"
    for chave, itens in dados.items():
        relatorio += f"{chave:>10}{itens['nome']:>12}{itens['perfil']:>12}{itens['acesso']:>20}{itens['maquina']:>9}{itens['observacoes']:>15}\n"
    salvarRelatório(relatorio)


def menuADM():
    # MENU PRINCIPAL
    while True:


        print("\n=== Sentinelalog ===")
        print("1. Registrar usuário")
        print("2. Visualizar usuário")
        print("3. Atualizar usuário")
        print("4. Deletar usuário")
        print("5. Matrícula oculta")
        print("6. Listar")
        
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar()

        elif opcao == "2":
            visualizar()

        elif opcao == "3":
            atualizarADM()

        elif opcao == "4":
            deletar()

        elif opcao == "5":
            matricula()
        elif opcao == "6":
            criarRelatorio()

        elif opcao == "0":
            print("Encerrando o Sentinelalog...")
            break

        else:
            print("Opção inválida. Tente novamente.")



def menuESTUDANTE():
    # MENU PRINCIPAL
    while True:


        print("\n=== Sentinelalog ===")
        print("1. Visualizar seu usuários")
        print("2. Atualizar seu usuário")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")


        if opcao == "1":
            visualizar()

        elif opcao == "2":
            atualizarESTUDANTE()


        elif opcao == "3":
            print("Encerrando o Sentinelalog...")
            break

        else:
            print("Opção inválida. Tente novamente.")


def menuPROFESSOR():
    # MENU PRINCIPAL
    while True:


        print("\n=== Sentinelalog ===")
        print("1. Visualizar seu usuário")
        print("2. Atualizar seu usuário")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")


        if opcao == "1":
            visualizar()

        elif opcao == "2":
            atualizarPROFESSOR()


        elif opcao == "3":
            print("Encerrando o Sentinelalog...")
            break

        else:
            print("Opção inválida. Tente novamente.")



def main():
    while True:
        print("\n=== Sentinelalog ===")
        print('Perfis disponíveis:\n1. Estudante\n2. Professor\n3. ADM')
        perfil = input("Digite o seu perfil (1-3) ou 0 para sair: ")

        if perfil == '1':
            menuESTUDANTE()
        elif perfil == '2':
            menuPROFESSOR()
        elif perfil == '3':
            menuADM()
        elif perfil == '0':
            break
        else:
            print("Opção inválida")






main()
