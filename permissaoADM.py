from dadosGlobais import *
from crud import *
from relatorio import *
from maquinasBloqueadas import *

#AQUI TEM TODAS AS FUNÇÕES COM PERMISSÃO DE ADM
#TODA FUNÇÃO QUE ESTIVER RELACIONADO A UMA CONTA ADM PRECISA ESTAR AQUI

# CRIAR PRIMEIRO ADMINISTRADOR
def primeiro_acesso(): # essa parte é so necessaria se nao tiver informação nenhuma e seja o primeiro cadastro
    consultar()

    if dados:
        return

    print("\nNenhum usuário cadastrado.")
    print("Vamos criar o primeiro administrador.")
    while True:
        try:

            matricula = int(input("Matrícula: "))
        except ValueError:
            print('matrícula inválida,tente novamente!')
            continue
        else:
            break



    while len(str(matricula)) < 4:
        try:
            print("A matrícula deve ter pelo menos 4 caracteres.")
            matricula = int(input("Matrícula: "))
        except:
            print('matrícula inválida,tente novamente!')
            continue
        



    nome = input("Nome do administrador: ").strip()

    while not nome:
        print("O nome não pode ficar vazio.")
        nome = input("Nome do administrador: ").strip()

    matricula = str(matricula)

    dados[matricula] = {
        "nome": nome,
        "perfil": "administrador",
        "horario": "24h",
        "acesso": "Nunca acessou",
        "observacoes": ""
    }

    salvar()

    print("Administrador criado com sucesso.")


# REGISTRAR USUÁRIO (ADMINISTRADOR)
def registrar():
    limpar()
    consultar()

    while True:
        try:
            matricula = int(input("Qual a matrícula do usuário: "))
        except: 
            print('matrícula inválida,tente novamente!')
            continue
        else:
            break


    while len(str(matricula)) < 4:
        try:
            print("A matrícula deve ter pelo menos 4 caracteres.")# caso tente registrar o usuario com uma matricula pequena
            matricula = int(input("Qual a matrícula do usuário: "))
        except:
            print('matrícula inválida,tente novamente!')
            continue

    matricula = str(matricula)
    if matricula in dados: # verificação se ja foi
        print("O usuário já foi cadastrado.")
        return

    nome = input("Nome: ").strip()

    while not nome: # nem preciso comentar nessa parte super intuitivo tbm :p
        print("O nome não pode ficar vazio.")
        nome = input("Nome: ").strip()

    perfil = input(
        "Perfil (estudante, professor, administrador): "
    ).lower().strip()

    while perfil not in PERFIS:
        print("Perfil inválido.")
        perfil = input(
            "Perfil (estudante, professor, administrador): "
        ).lower().strip()

    horario = input("Horário permitido (ex: 7h-18h): ").strip() # vou mexer nessa bomba dps, nao deve ser dificil a verificação 
    observacoes = input("Observações (opcional): ").strip()

    dados[matricula] = {
        "nome": nome,
        "perfil": perfil,
        "horario": horario,
        "observacoes": observacoes,
        "acesso": "Nunca acessou"
    }

    salvar()

    print("\nUsuário cadastrado com sucesso.")

# VISUALIZAR USUÁRIO (ADMINISTRADOR)
def visualizar(): # aqui é a vizualização especifica do adm, so tem mais informação mas é o mesmo processo
    limpar()
    consultar()

    if len(dados) == 0:
        print("Não há nada no registro.")
        return

    pergunta = input(
        "Qual o usuário que você deseja checar: "
    ).strip()

    encontrado = False

    for matricula, info in dados.items():

        if info["nome"].lower() == pergunta.lower():
            exibir(matricula, info)
            encontrado = True

    if not encontrado:
        print("O usuário não foi cadastrado.")

# ATUALIZAR USUÁRIO (ADMINISTRADOR)
def atualizarADM(matricula_logada): # adm atualizar blah blah blah
    limpar()
    consultar()

    matricula = input(
        "Digite a matrícula do usuário que deseja atualizar: "
    ).strip()

    if matricula not in dados:
        print("O usuário não foi cadastrado.")
        return

    info = dados[matricula]

    print("\nDeixe vazio para manter o dado atual.")

    nome = input(f"Nome ({info['nome']}): ")

    # Impede que o administrador altere o próprio perfil
    if matricula == matricula_logada:
        print("Você não pode alterar o próprio perfil.")
        perfil = ""

    else:
        perfil = input(
            f"Perfil ({info['perfil']}): "
        ).lower().strip()

    horario = input(f"Horário ({info['horario']}): ")
    observacoes = input(
        f"Observações ({info['observacoes']}): "
    )

    if nome.strip():
        info["nome"] = nome.strip()

    if perfil:
        if perfil in PERFIS:
            info["perfil"] = perfil

        else:
            print("Perfil inválido. Mantido o atual.")

    if horario.strip():
        info["horario"] = horario.strip()

    if observacoes.strip():
        info["observacoes"] = observacoes.strip()

    salvar()

    print("\nUsuário atualizado com sucesso.")


# DELETAR USUÁRIO 
def deletar(matricula_logada): # deletar, so adm pode ne :p
    limpar()
    consultar()

    matricula = input(
        "Digite a matrícula do usuário que deseja deletar: "
    ).strip()

    # Impede a exclusão do próprio administrador
    if matricula == matricula_logada:
        print("Você não pode deletar o usuário com o qual está logado.")
        return

    if matricula not in dados:
        print("O usuário não foi cadastrado.")
        return

    # Impede a exclusão do último administrador
    if dados[matricula]["perfil"] == "administrador":

        administradores = 0

        for info in dados.values():
            if info["perfil"] == "administrador":
                administradores += 1

        if administradores == 1:
            print("Não é possível excluir o último administrador.")
            return

    confirmacao = input(
        "Deseja realmente deletar? (s/n): "
    ).lower().strip()

    if confirmacao == "s":

        # Exclui somente o cadastro.
        # O histórico de acessos permanece preservado.
        del dados[matricula]

        salvar()

        print("Usuário deletado com sucesso.")

    else:
        print("Operação cancelada.")

# REVELAR MATRÍCULA (ADMINISTRADOR)
def matricula(): #mostrar a matricula do usuario sem os asteristicos
    limpar()
    consultar()

    nome = input("Digite o nome do usuário: ").strip()

    encontrado = False

    for numero, info in dados.items():

        if info["nome"].lower() == nome.lower():
            print("Matrícula:", numero)
            encontrado = True

    if not encontrado:
        print("O usuário não foi cadastrado.")


# BLOQUEAR MÁQUINA (ADMINISTRADOR)
def bloquearMaquina(): # opa coisa nova que eu preciso explicar, essa parte eu nao sabia 100% oque fazer mas é a mesma coisa que cadastrar
    limpar()            # so que para as maquinas bloqueadas, tipo eu sei que o cadastro dessas maquinas vão ser necessarias, mas o dps eu nao
    consultarBloqueadas() #sei, tipo ele pode acessar ? isso vai aparecer no log ? sla vou ver com victor dps

    nome_maquina = input("Nome da máquina a bloquear: ").strip()

    if not nome_maquina:
        print("O nome não pode ficar vazio.")
        return
        
    if nome_maquina.lower() in [m.lower() for m in bloqueadas]:
        print("Essa máquina já está bloqueada.")
        return
        
    with open("maquinas_bloqueadas.txt", "a", encoding="utf8") as arquivo:
        arquivo.write(f"{nome_maquina}\n")
        
    print("Máquina bloqueada com sucesso.")



# MENU ADMINISTRADOR
def menuADM(matricula_logada): 
    while True:

        print("\n=== SentinelLog (Administrador) ===")
        print("1. Registrar usuário")
        print("2. Visualizar usuário")
        print("3. Atualizar usuário")
        print("4. Deletar usuário")
        print("5. Revelar matrícula")
        print("6. Criar relatório")
        print("7. Bloquear máquina")  # NOVO
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar()

        elif opcao == "2":
            visualizar()

        elif opcao == "3":
            atualizarADM(matricula_logada)

        elif opcao == "4":
            deletar(matricula_logada)

        elif opcao == "5":
            matricula()

        elif opcao == "6":
            criarRelatorio()

        elif opcao == "7":  # NOVO
            bloquearMaquina()

        elif opcao == "0":
            print("Saindo da conta...")
            break

        else:
            print("Opção inválida. Tente novamente.")


# PERFIL ADMINISTRADOR
def perfil_administrador(matricula_logada):
    menuADM(matricula_logada)