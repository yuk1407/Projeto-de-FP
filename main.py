import os
from datetime import datetime

dados = {}
PERFIS = ("estudante", "professor", "administrador")


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


# CONSULTAR OS DADOS DO ARQUIVO
def consultar(): #FUNÇÃO ESSENCIAL PARA O A MANIPULAÇÃO DE ARQUIVO
    dados.clear()

    try:
        with open("arquivos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 6)

                if len(partes) < 7: # DIVIDE EM PARTESS
                    continue

                matricula, nome, perfil, horario, acesso, maquina, observacoes = partes #ATRIBUI NAS VARIAVEIS

                dados[matricula] = {
                    "nome": nome,
                    "perfil": perfil,
                    "horario": horario,
                    "acesso": acesso,
                    "maquina": maquina,
                    "observacoes": observacoes
                }

    except FileNotFoundError:
        pass


# SALVAR ALTERAÇÕES NO ARQUIVO
def salvar():
    with open("arquivos.txt", "w", encoding="utf8") as arquivo: #PRINT NO ARQUIVO TXT
        for matricula, info in dados.items():
            arquivo.write(
                f"{matricula},{info['nome']},{info['perfil']},"
                f"{info['horario']},{info['acesso']},"
                f"{info['maquina']},{info['observacoes']}\n"
            )


def salvarRelatorio(relatorio): # PARTE DO RELATORIO
    with open("relatorio.txt", "w", encoding="utf8") as arquivo:
        arquivo.write(relatorio)


def agora(): #TEMPO DA BIBLIOTECA DATATIME
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# LOGIN
def verificar_login(nome, matricula): 
    """Retorna o perfil se nome e matrícula baterem; senão, None."""
    consultar()

    info = dados.get(matricula) #COOMPARAÇÃO

    if info and info["nome"].lower() == nome.lower():
        return info["perfil"].lower()

    return None


def primeiro_acesso(): 
    """Se não existir nenhum usuário, cria o primeiro administrador."""
    consultar()

    if dados:
        return

    print("\nNenhum usuário cadastrado. Vamos criar o primeiro administrador.")
    matricula = input("Matrícula: ")
    nome = input("Nome: ")

    dados[matricula] = {
        "nome": nome,
        "perfil": "administrador",
        "horario": "24h",
        "acesso": agora(),
        "maquina": "-",
        "observacoes": ""
    }
    salvar()
    print("Administrador criado com sucesso.")


def login(): 
    """Retorna (matricula, perfil) se o login der certo; senão, (None, None)."""
    for tentativa in range(3): # TENTATIVAS
        nome = input("Digite seu nome: ")
        matricula = input("Digite sua matrícula: ")

        perfil = verificar_login(nome, matricula)

        if perfil in PERFIS:
            # registra o último acesso
            dados[matricula]["acesso"] = agora()
            salvar()
            return matricula, perfil

        print("\nNome ou matrícula incorretos!")

    print("Número máximo de tentativas atingido.")
    return None, None


# FUNÇÕES DO SISTEMA
def exibir(matricula, info): #VISUALIZAR 
    matricula_oculta = matricula[:2] + "*" * max(0, len(matricula) - 2) #ESCONDER A MATRICULA

    print("\n-------------------------")
    print("Nome:", info["nome"])
    print("Matricula:", matricula_oculta)
    print("Perfil:", info["perfil"])
    print("Horario:", info["horario"])
    print("Último acesso:", info["acesso"])
    print("Máquina:", info["maquina"])
    print("Observacoes:", info["observacoes"])
    print("-------------------------")


# REGISTRAR USUÁRIO (ADM)
def registrar():
    limpar()
    consultar()

    matricula = input("Qual a matrícula do usuário: ")

    if matricula in dados:
        print("O usuário já foi cadastrado.")
        return

    nome = input("Nome: ")

    perfil = input("Perfil (estudante, professor, administrador): ").lower()
    while perfil not in PERFIS:
        print("Perfil inválido.")
        perfil = input("Perfil (estudante, professor, administrador): ").lower()

    dados[matricula] = { #ATIBUIÇÃO DAS VARIAVEIS AO DICT
        "nome": nome,
        "perfil": perfil,
        "horario": input("Horário permitido (ex: 7h-18h): "),
        "maquina": input("Qual máquina foi usada: "),
        "observacoes": input("Observações (opcional): "),
        "acesso": agora()
    }

    salvar()
    print("Usuário cadastrado com sucesso.")


# VISUALIZAR USUÁRIO (ADM: busca por nome)
def visualizar():
    limpar()
    consultar()

    if len(dados) == 0:
        print("Não há nada no registro.")
        return

    pergunta = input("Qual o usuário que você deseja checar: ") #COMPARAR

    for matricula, info in dados.items():
        if info["nome"].lower() == pergunta.lower():
            exibir(matricula, info)
            return

    print("O usuário não foi cadastrado.")


# VISUALIZAR O PRÓPRIO USUÁRIO (estudante/professor)
def visualizarProprio(matricula): #VISUALIZAÇÃO DO PROPRIO PERFIL
    limpar()
    consultar()

    if matricula in dados:
        exibir(matricula, dados[matricula]) # MOSTRA COISAS ESPECIFICAS
    else:
        print("O usuário não foi cadastrado.")


# ATUALIZAR USUÁRIO (ADM)
def atualizarADM():
    limpar()
    consultar()

    matricula = input("Digite a matrícula do usuário que deseja atualizar: ")

    if matricula not in dados:
        print("O usuário não foi cadastrado.")
        return

    info = dados[matricula] # COMPARAÇÃO

    print("Deixe vazio para manter o dado atual.")

    nome = input(f"Nome ({info['nome']}): ") #PRINTS
    perfil = input(f"Perfil ({info['perfil']}): ").lower()
    horario = input(f"Horário ({info['horario']}): ")
    maquina = input(f"Máquina ({info['maquina']}): ")
    observacoes = input(f"Observações ({info['observacoes']}): ")

    if nome:
        info["nome"] = nome

    if perfil:
        if perfil in PERFIS:
            info["perfil"] = perfil
        else:
            print("Perfil inválido, mantido o atual.")

    if horario:
        info["horario"] = horario

    if maquina:
        info["maquina"] = maquina

    if observacoes:
        info["observacoes"] = observacoes

    salvar()
    print("Usuário atualizado com sucesso.")


# ATUALIZAR O PRÓPRIO USUÁRIO (estudante e professor)
def atualizarProprio(matricula): 
    limpar()
    consultar()

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


# DELETAR USUÁRIO (ADM)
def deletar(matricula_logada):
    limpar()
    consultar()

    matricula = input("Digite a matrícula do usuário que deseja deletar: ")

    if matricula == matricula_logada: #VERIFICAÇÃO CASO TENTE SE DELETAR
        print("Você não pode deletar o usuário com o qual está logado.")
        return

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


# MATRÍCULA OCULTA (ADM)
def matricula():
    limpar()
    consultar()

    nome = input("Digite o nome do usuário: ")

    for numero, info in dados.items():
        if info["nome"].lower() == nome.lower():
            print("Matrícula:", numero)
            return

    print("O usuário não foi cadastrado.")


def criarRelatorio(): #AINDA VAMOS VER COMO FAZER ISSO DIREITINHO
    consultar()

    relatorio = (
        f"{'Matrícula':>10}{'Nome':>12}{'Perfil':>14}"
        f"{'Acesso':>20}{'Maquina':>9}{'Observações':>15}\n"
    )

    for chave, itens in dados.items():
        relatorio += (
            f"{chave:>10}{itens['nome']:>12}{itens['perfil']:>14}"
            f"{itens['acesso']:>20}{itens['maquina']:>9}{itens['observacoes']:>15}\n"
        )

    salvarRelatorio(relatorio)
    print("Relatório salvo em relatorio.txt")


# MENUS
def menuADM(matricula_logada):
    while True:
        print("\n=== Sentinelalog (Administrador) ===")
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
            deletar(matricula_logada)
        elif opcao == "5":
            matricula()
        elif opcao == "6":
            criarRelatorio()
        elif opcao == "0":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Estudante e professor têm o mesmo menu
def menuUsuario(matricula_logada, titulo):
    while True:
        print(f"\n=== Sentinelalog ({titulo}) ===")
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


def perfil_estudante(matricula_logada):
    menuUsuario(matricula_logada, "Estudante")


def perfil_professor(matricula_logada):
    menuUsuario(matricula_logada, "Professor")


def perfil_administrador(matricula_logada):
    menuADM(matricula_logada)


# PROGRAMA PRINCIPAL
def main():
    primeiro_acesso()

    while True:
        print("\n=== Sentinelalog ===")
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
            print("Encerrando o Sentinelalog...")
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()
