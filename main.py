import os
from datetime import datetime

dados = {}
acessos = []
bloqueadas = []  #  lista de máquinas bloqueadas

PERFIS = ("estudante", "professor", "administrador")


# LIMPAR TERMINAL
def limpar():
    os.system("cls" if os.name == "nt" else "clear") 


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


# CONSULTAR HISTÓRICO DE ACESSOS
def consultarAcessos(): # so vai pegar o acesso da pessoa, importante pra parte de sucesso e falha
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
def registrarAcesso(matricula, maquina, resultado): # parte de acesso (log)
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
def ultimaMaquina(matricula): # maquina utilizada
    for acesso in reversed(acessos):
        if (
            acesso["matricula"] == matricula
            and acesso["resultado"] == "sucesso"
        ):
            return acesso["maquina"]

    return "-"


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


# SALVAR RELATÓRIO
def salvarRelatorio(relatorio): # so salvar o relatorio no arquivo
    with open("relatorio.txt", "w", encoding="utf8") as arquivo:
        arquivo.write(relatorio)


# DATA E HORÁRIO ATUAL
def agora(): # parte do horario, vou mexer nisso dps pra verificar se o usuario esta no horario permitido ou nao
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# VERIFICAR LOGIN
def verificar_login(nome, matricula): # parte de verificação do login 
    consultar() # ele consulta os dados

    info = dados.get(matricula) # vai atribuir info com a matricula 

    if info and info["nome"].lower() == nome.lower(): #vai ver o perfil do usuario e retornar ele para o codigo, assimo usaurio entra no perfil certo
        return info["perfil"].lower() 

    return None


# CRIAR PRIMEIRO ADMINISTRADOR
def primeiro_acesso(): # essa parte é so necessaria se nao tiver informação nenhuma e seja o primeiro cadastro
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
    for tentativa in range(3): # parte de tentativa, vou ver como eu mexo nisso pra parte de suspeito e critico

        nome = input("\nDigite seu nome: ").strip()
        matricula = input("Digite sua matrícula: ").strip()

        maquina = os.environ.get("COMPUTERNAME", "MAQUINA-DESCONHECIDA")

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


# REGISTRAR USUÁRIO (ADMINISTRADOR)
def registrar():
    limpar()
    consultar()

    matricula = input("Qual a matrícula do usuário: ").strip() 

    while len(matricula) < 4:
        print("A matrícula deve ter pelo menos 4 caracteres.")# caso tente registrar o usuario com uma matricula pequena
        matricula = input("Qual a matrícula do usuário: ").strip()

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


# VISUALIZAR O PRÓPRIO USUÁRIO
def visualizarProprio(matricula): # visualização so que aluno ou professor
    limpar()
    consultar()

    if matricula in dados:
        exibir(matricula, dados[matricula])

    else:
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


# ATUALIZAR O PRÓPRIO USUÁRIO
def atualizarProprio(matricula):  # mesma coisa so que menos
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


# CRIAR RELATÓRIO
def criarRelatorio(): # esse relatorio so mostra os usuario e algumas informações deles, enfim tenho ctz que vamos ter que mexer nisso alguma hr
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
