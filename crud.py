import os
from dadosGlobais import *
from manipularAcessos import *
from maquinasBloqueadas import *
from horario import *

#AQUI TEM TODAS AS FUNÇÕES DO CRUD EM SI E AS FUNÇÕES REFERENTE AS PERMISSÕES DE ALUNOS E PROFESSORES
#OBIVIAMENTE OS DE ADM NÃO ESTÃO AQUI


# LIMPAR TERMINAL
def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def pedirTexto(mensagem): #ele impede que seja colocado virgula no texto, e quebre a parte que mostra os dados do usuario.
    texto = input(mensagem).strip()
    while "," in texto:
        print("O texto não pode conter vírgulas.")
        texto = input(mensagem).strip()
    return texto
    
# CONSULTAR OS DADOS DO ARQUIVO
def consultar(): # consultar o arquivo e atribuir em variaveis
    dados.clear()

    try:
        with open("arquivos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 6)

                if len(partes) == 7:
                    # Formato antigo: possui máquina no cadastro
                    matricula, nome, perfil, horario, acesso, maquina_antiga, observacoes = partes

                elif len(partes) == 6:
                    # Formato novo: não possui máquina fixa
                    matricula, nome, perfil, horario, acesso, observacoes = partes

                else:
                    continue

                dados[matricula] = {
                    "nome": nome,
                    "perfil": perfil,
                    "horario": horario,
                    "acesso": acesso,
                    "observacoes": observacoes
                }

    except FileNotFoundError:
        pass


# SALVAR ALTERAÇÕES NO ARQUIVO
def salvar(): # pega todos os dados e da um print no arquivo de texto
    with open("arquivos.txt", "w", encoding="utf8") as arquivo:
        for matricula, info in dados.items():
            arquivo.write(
                f"{matricula},{info['nome']},{info['perfil']},"
                f"{info['horario']},{info['acesso']},"
                f"{info['observacoes']}\n"
            )


# VERIFICAR LOGIN
def verificar_login(nome, matricula): # parte de verificação do login 
    consultar() # ele consulta os dados

    info = dados.get(matricula) # vai atribuir info com a matricula 

    if info and info["nome"].lower() == nome.lower(): #vai ver o perfil do usuario e retornar ele para o codigo, assimo usaurio entra no perfil certo
        return info["perfil"].lower() 

    return None




# LOGIN
def login():
    for tentativa in range(3): # parte de tentativa, vou ver como eu mexo nisso pra parte de suspeito e critico

        nome = input("\nDigite seu nome: ").strip()
        matricula = input("Digite sua matrícula: ").strip()

        maquina = identificarMaquina()

        # bloqueia o acesso se a máquina estiver na lista de bloqueadas
        if maquinaBloqueada(maquina):
            registrarAcesso(matricula, maquina, "bloqueado")

            print("\nAcesso negado: esta máquina está bloqueada.")

            return None, None # ele so nao entra no perfil caso o pc esteja usando seja bloqueado, provavelmente vou mudar essa parte enfim 
#nao sei exatamente irei ver amanha com o povo 

        perfil = verificar_login(nome, matricula)

        if perfil in PERFIS:

            # Atualiza a data do último acesso
            dados[matricula]["acesso"] = agora() # so muda o horario de acesso
            salvar()

            # Registra o acesso bem-sucedido
            registrarAcesso(matricula, maquina, "sucesso")

            print("\nLogin realizado com sucesso!")

            return matricula, perfil

        # Registra a tentativa que falhou
        registrarAcesso(matricula, maquina, "falha") # vou ver como eu vou usar isso pro suspeito e critico, mas provavekmente 
        #botar condicionais e é isso, faço amanha

        print("\nNome ou matrícula incorretos!")

    print("\nNúmero máximo de tentativas atingido.")

    return None, None

# EXIBIR USUÁRIO
def exibir(matricula, info): # so mostrar nada mais nada menos que so print
    matricula_oculta = (
        matricula[:2] + "*" * max(0, len(matricula) - 2)
    )

    print("\n-------------------------")
    print("Nome:", info["nome"])
    print("Matrícula:", matricula_oculta)
    print("Perfil:", info["perfil"])
    print("Horário:", info["horario"])
    print("Último acesso:", info["acesso"])
    print("Última máquina:", ultimaMaquina(matricula))
    print("Observações:", info["observacoes"])
    print("-------------------------")


# VISUALIZAR O PRÓPRIO USUÁRIO
def visualizarProprio(matricula): # visualização so que aluno ou professor
    limpar()
    consultar()

    if matricula in dados:
        exibir(matricula, dados[matricula])

    else:
        print("O usuário não foi cadastrado.")



# ATUALIZAR O PRÓPRIO USUÁRIO
def atualizarProprio(matricula):  # atualização de usuario com uma permissão mais baixa do que o adm, pois nesse so consegue 
    limpar() # atualizar o proprio usuario
    consultar()

    if matricula not in dados:
        print("O usuário não foi cadastrado.")
        return

    info = dados[matricula]

    print("\nDeixe vazio para manter o dado atual.")

    nome = input(f"Nome ({info['nome']}): ")
    observacoes = input(
        f"Observações ({info['observacoes']}): "
    )

    if nome.strip():
        info["nome"] = nome.strip()

    if observacoes.strip():
        info["observacoes"] = observacoes.strip()

    salvar()

    print("\nUsuário atualizado com sucesso.")


# MENU ESTUDANTE E PROFESSOR
def menuUsuario(matricula_logada, titulo):
    while True:

        print(f"\n=== SentinelLog ({titulo}) ===")
        print("1. Visualizar seu usuário")
        print("2. Atualizar seu usuário")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            visualizarProprio(matricula_logada)

        elif opcao == "2":
            atualizarProprio(matricula_logada)

        elif opcao == "3":
            print("Saindo da conta...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# PERFIL ESTUDANTE
def perfil_estudante(matricula_logada):
    menuUsuario(matricula_logada, "Estudante")


# PERFIL PROFESSOR
def perfil_professor(matricula_logada):
    menuUsuario(matricula_logada, "Professor")
