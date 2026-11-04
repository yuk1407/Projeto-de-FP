import os
from datetime import datetime

dados = {}
acessos = []

PERFIS = ("estudante", "professor", "administrador")


# LIMPAR TERMINAL
def limpar():
    os.system("cls" if os.name == "nt" else "clear")


# CONSULTAR OS DADOS DO ARQUIVO
def consultar():
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
def salvar():
    with open("arquivos.txt", "w", encoding="utf8") as arquivo:
        for matricula, info in dados.items():
            arquivo.write(
                f"{matricula},{info['nome']},{info['perfil']},"
                f"{info['horario']},{info['acesso']},"
                f"{info['observacoes']}\n"
            )


# CONSULTAR HISTÓRICO DE ACESSOS
def consultarAcessos():
    acessos.clear()

    try:
        with open("acessos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 3)

                if len(partes) != 4:
                    continue

                matricula, data_hora, maquina, resultado = partes

                acessos.append({
                    "matricula": matricula,
                    "data_hora": data_hora,
                    "maquina": maquina,
                    "resultado": resultado
                })

    except FileNotFoundError:
        pass


# REGISTRAR CADA TENTATIVA DE ACESSO
def registrarAcesso(matricula, maquina, resultado):
    registro = {
        "matricula": matricula,
        "data_hora": agora(),
        "maquina": maquina,
        "resultado": resultado
    }

    acessos.append(registro)

    with open("acessos.txt", "a", encoding="utf8") as arquivo:
        arquivo.write(
            f"{registro['matricula']},{registro['data_hora']},"
            f"{registro['maquina']},{registro['resultado']}\n"
        )


# IDENTIFICAR A ÚLTIMA MÁQUINA UTILIZADA
def ultimaMaquina(matricula):
    for acesso in reversed(acessos):
        if (
            acesso["matricula"] == matricula
            and acesso["resultado"] == "sucesso"
        ):
            return acesso["maquina"]

    return "-"


# SALVAR RELATÓRIO
def salvarRelatorio(relatorio):
    with open("relatorio.txt", "w", encoding="utf8") as arquivo:
        arquivo.write(relatorio)


# DATA E HORÁRIO ATUAL
def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# VERIFICAR LOGIN
def verificar_login(nome, matricula):
    consultar()

    info = dados.get(matricula)

    if info and info["nome"].lower() == nome.lower():
        return info["perfil"].lower()

    return None


# CRIAR PRIMEIRO ADMINISTRADOR
def primeiro_acesso():
    consultar()

    if dados:
        return

    print("\nNenhum usuário cadastrado.")
    print("Vamos criar o primeiro administrador.")

    matricula = input("Matrícula: ").strip()

    while len(matricula) < 4:
        print("A matrícula deve ter pelo menos 4 caracteres.")
        matricula = input("Matrícula: ").strip()

    nome = input("Nome do administrador: ").strip()

    while not nome:
        print("O nome não pode ficar vazio.")
        nome = input("Nome do administrador: ").strip()

    dados[matricula] = {
        "nome": nome,
        "perfil": "administrador",
        "horario": "24h",
        "acesso": "Nunca acessou",
        "observacoes": ""
    }

    salvar()

    print("Administrador criado com sucesso.")


# LOGIN
def login():
    for tentativa in range(3):

        nome = input("\nDigite seu nome: ").strip()
        matricula = input("Digite sua matrícula: ").strip()

        maquina = os.environ.get("COMPUTERNAME", "MAQUINA-DESCONHECIDA")

        perfil = verificar_login(nome, matricula)

        if perfil in PERFIS:

            # Atualiza a data do último acesso
            dados[matricula]["acesso"] = agora()
            salvar()

            # Registra o acesso bem-sucedido
            registrarAcesso(matricula, maquina, "sucesso")

            print("\nLogin realizado com sucesso!")

            return matricula, perfil

        # Registra a tentativa que falhou
        registrarAcesso(matricula, maquina, "falha")

        print("\nNome ou matrícula incorretos!")

    print("\nNúmero máximo de tentativas atingido.")

    return None, None

# EXIBIR USUÁRIO
def exibir(matricula, info):
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


# REGISTRAR USUÁRIO (ADMINISTRADOR)
def registrar():
    limpar()
    consultar()

    matricula = input("Qual a matrícula do usuário: ").strip()

    while len(matricula) < 4:
        print("A matrícula deve ter pelo menos 4 caracteres.")
        matricula = input("Qual a matrícula do usuário: ").strip()

    if matricula in dados:
        print("O usuário já foi cadastrado.")
        return

    nome = input("Nome: ").strip()

    while not nome:
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

    horario = input("Horário permitido (ex: 7h-18h): ").strip()
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
def visualizar():
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


# VISUALIZAR O PRÓPRIO USUÁRIO
def visualizarProprio(matricula):
    limpar()
    consultar()

    if matricula in dados:
        exibir(matricula, dados[matricula])

    else:
        print("O usuário não foi cadastrado.")


# ATUALIZAR USUÁRIO (ADMINISTRADOR)
def atualizarADM(matricula_logada):
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


# ATUALIZAR O PRÓPRIO USUÁRIO
def atualizarProprio(matricula):
    limpar()
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


# DELETAR USUÁRIO (ADMINISTRADOR)
def deletar(matricula_logada):
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
def matricula():
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


# CRIAR RELATÓRIO
def criarRelatorio():
    consultar()

    relatorio = (
        f"{'Matrícula':>12}{'Nome':>20}{'Perfil':>16}"
        f"{'Acesso':>22}{'Máquina':>18}{'Observações':>20}\n"
    )

    for chave, itens in dados.items():

        relatorio += (
            f"{chave:>12}{itens['nome']:>20}{itens['perfil']:>16}"
            f"{itens['acesso']:>22}{ultimaMaquina(chave):>18}"
            f"{itens['observacoes']:>20}\n"
        )

    salvarRelatorio(relatorio)

    print("Relatório salvo em relatorio.txt")


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

        elif opcao == "0":
            print("Saindo da conta...")
            break

        else:
            print("Opção inválida. Tente novamente.")


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


# PERFIL ADMINISTRADOR
def perfil_administrador(matricula_logada):
    menuADM(matricula_logada)


# PROGRAMA PRINCIPAL
def main():

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
