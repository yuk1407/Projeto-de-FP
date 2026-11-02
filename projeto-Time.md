#with ----- as ---, abre arquivo e fecha automaticamente depois de terminar de usar

#eu deveria ter criado um fubção para abrir o arquivo e atribuir as variaveis, vou fazer amanha isso

# se tiver algo de errado me fala ou ajeita e da um pull request 
from datetime import datetime
import os
os.system("cls")
#Funções do CRUD

#Função de registar
#acho que é isso que eles tao pedindo, mas deve ta faltando algo 
def registrar(): 
    os.system("cls")
    nome = input("Digite o nome do usuario: ")
    matricula = input("Digite a matricula do usuario: ")
    perfil = input("Digite o perfil do usuario (estudante, professor, administrador): ")
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # datetime pega o horário atual automaticamente
    print(f"Horário registrado: {horario}")
    maquina = input("Digite a máquina de origem: ")
    resultado = input("Digite o resultado do acesso (sucesso/falha): ")
    observacoes = input("Digite observações adicionais (opcional): ")

    with open("dados.txt", "a") as arquivo:
        arquivo.write(f"{nome},{matricula},{perfil},{horario},{maquina},{resultado},{observacoes}\n")


# Função de visualizar
def vizualizar():
    os.system("cls")
    usuarios = []

    with open("dados.txt", "r") as arquivo: 
        for linha in arquivo:
            dados = linha.strip().split(",") # pega cada linha do arquivo e separa os dados por vírgula
            
            usuario = { # atribui cada dado com uma variavel
                "nome": dados[0],
                "matricula": dados[1],
                "perfil": dados[2],
                "horario": dados[3],
                "maquina": dados[4],
                "resultado": dados[5],
                "observacoes": dados[6]
            }

            usuarios.append(usuario)

    if len(usuarios) == 0: #caso não tenha nenhum usuário cadastrado
        print("Nenhum usuario cadastrado.")
        return

    for usuario in usuarios: #esconde a matricula

        matricula = usuario["matricula"]
        matricula_oculta = matricula[:2] + "*" * max(0, len(matricula) - 2) #substitui por asteriscos

        print("-------------------------")
        print("Nome:", usuario["nome"])
        print("Matricula:", matricula_oculta)
        print("Perfil:", usuario["perfil"])
        print("Horario:", usuario["horario"])
        print("Maquina:", usuario["maquina"])
        print("Resultado:", usuario["resultado"])
        print("Observacoes:", usuario["observacoes"])



def matricula():#opçao de revelar (não vou mentir que eu nao sei exatemente oque eles querem aqui)
    os.system("cls")
    usuarios = []

    with open("dados.txt", "r") as arquivo: 
        for linha in arquivo:
            dados = linha.strip().split(",") 
            
            usuario = {
                "nome": dados[0],
                "matricula": dados[1],
                "perfil": dados[2],
                "horario": dados[3],
                "maquina": dados[4],
                "resultado": dados[5],
                "observacoes": dados[6]
            }
            usuarios.append(usuario)



        busca = input("Digite o nome do usuário que deseja revelar a matrícula: ")

        for usuario in usuarios:
            if usuario["nome"] == busca:
                print("Matricula completa:", usuario["matricula"])
                return

        else:
            print("Usuário não encontrado.")

#função de atualizar os dados
def atualizar():
    os.system("cls")
    matricula = input("Digite a matrícula do usuário que deseja atualizar: ")

    usuarios = []

    with open("dados.txt", "r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(",")
            usuario = {
                "nome": dados[0],
                "matricula": dados[1],
                "perfil": dados[2],
                "horario": dados[3],
                "maquina": dados[4],
                "resultado": dados[5],
                "observacoes": dados[6]
            }
            usuarios.append(usuario)

    usuario_encontrado = None #cria uma variavel para armazenar o usuario encontrado

    for usuario in usuarios: #vai ver todos os usuario e comparar com oque foi digitado
        if usuario["matricula"] == matricula:
            usuario_encontrado = usuario # caso encontrado ele atribui o usuario encontrado a variavel
            break

    if usuario_encontrado is None: # caso nao encontrar nenhum usuario com a matricula
        print("Usuário não encontrado.")
        return

    print("Digite os novos valores (deixe em branco para manter o valor atual):")
    novo_nome = input(f"Nome ({usuario_encontrado['nome']}): ") or usuario_encontrado['nome']
    novo_perfil = input(f"Perfil ({usuario_encontrado['perfil']}): ") or usuario_encontrado['perfil']
    novo_horario = input(f"Horário ({usuario_encontrado['horario']}): ") or usuario_encontrado['horario']
    nova_maquina = input(f"Máquina ({usuario_encontrado['maquina']}): ") or usuario_encontrado['maquina']
    novo_resultado = input(f"Resultado ({usuario_encontrado['resultado']}): ") or usuario_encontrado['resultado']
    novas_observacoes = input(f"Observações ({usuario_encontrado['observacoes']}): ") or usuario_encontrado['observacoes']

    usuario_atualizado = {
        "nome": novo_nome,
        "matricula": matricula,
        "perfil": novo_perfil,
        "horario": novo_horario,
        "maquina": nova_maquina,
        "resultado": novo_resultado,
        "observacoes": novas_observacoes
    }

    usuarios.remove(usuario_encontrado)
    usuarios.append(usuario_atualizado)

    with open("dados.txt", "w", encoding="utf8") as arquivo:
        for usuario in usuarios:
            arquivo.write(f"Nome: {usuario['nome']}\n")
            arquivo.write(f"Matrícula: {usuario['matricula']}\n")
            arquivo.write(f"Perfil: {usuario['perfil']}\n")
            arquivo.write(f"Horário: {usuario['horario']}\n")
            arquivo.write(f"Máquina: {usuario['maquina']}\n")
            arquivo.write(f"Resultado: {usuario['resultado']}\n")
            arquivo.write(f"Observações: {usuario['observacoes']}\n")
            arquivo.write("-" * 30 + "\n")

#funcao de deletar
def deletar():
    os.system("cls")
    matricula = input("Digite a matrícula do usuário que deseja deletar: ")

    usuarios = []

    with open("dados.txt", "r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(",")
            usuario = {
                "nome": dados[0],
                "matricula": dados[1],
                "perfil": dados[2],
                "horario": dados[3],
                "maquina": dados[4],
                "resultado": dados[5],
                "observacoes": dados[6]
            }
            usuarios.append(usuario)

    usuario_encontrado = None

    for usuario in usuarios: # mesma explixcação da funçao de atualizar
        if usuario["matricula"] == matricula:
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None:
        print("Usuário não encontrado.")
        return

    usuarios.remove(usuario_encontrado) # deleta oque foi encontrado

    with open("dados.txt", "w", encoding="utf8") as arquivo:
        for usuario in usuarios:
            arquivo.write(f"Nome: {usuario['nome']}\n")
            arquivo.write(f"Matrícula: {usuario['matricula']}\n")
            arquivo.write(f"Perfil: {usuario['perfil']}\n")
            arquivo.write(f"Horário: {usuario['horario']}\n")
            arquivo.write(f"Máquina: {usuario['maquina']}\n")
            arquivo.write(f"Resultado: {usuario['resultado']}\n")
            arquivo.write(f"Observações: {usuario['observacoes']}\n")
            arquivo.write("-" * 30 + "\n")
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
        print("Opção inválida. Tente novamente.")
