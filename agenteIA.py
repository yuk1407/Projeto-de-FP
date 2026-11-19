from dadosGlobais import *
from crud import consultar, substituirCaractere
from manipularAcessos import consultarAcessos
from agente import falar_com_agente_texto
from datetime import datetime
from horario import agora
from horario import verificarHorario
from maquinasBloqueadas import *

# REGISTRAR CADA TENTATIVA DE ACESSO
def registrarInteracaoIA(matricula, pergunta): # vai registrar cada uso da ia 

    info = dados.get(matricula)
   
    interacao = {
        "matricula": matricula,
        "pergunta": substituirCaractere(pergunta,"-"),
        "data_hora": agora(),
        "maquina": identificarMaquina(),
        "nome" : info['nome'],
        "perfil" : info['perfil']

    }

    historicoIA.append(interacao)

    with open("historicoIA.txt", "a", encoding="utf8") as arquivo:
        arquivo.write(
            f"{interacao['matricula']},{interacao['pergunta']},"
            f"{interacao['maquina']},{interacao['data_hora']},"
            f"{interacao['nome']},{interacao['perfil']}\n"
        )

def consultarHistoricoIA(): #vai consultar todo o historico do uso da IA
    
    historicoIA.clear()

    try:
        with open("historicoIA.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 5)

                if len(partes) != 6:
                    continue

                matricula, pergunta, maquina, data_hora, nome, perfil  = partes

                # descarta linhas com data inválida
                try:
                    datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    continue

                historicoIA.append({
                    "matricula": matricula,
                    "pergunta": pergunta,
                    "maquina": maquina,
                    "data_hora" :data_hora,
                    "nome": nome,
                    "perfil": perfil
                })

    except FileNotFoundError:
        pass

# REGRA DE PERMISSÃO: QUEM PODE VER OS ACESSOS DE QUEM
def podeVer(perfil, matricula_logada, matricula_alvo):
    if matricula_alvo == matricula_logada:
        return True

    info = dados.get(matricula_alvo)

    if info is None:
        return perfil == "administrador"

    perfil_alvo = info["perfil"]

    if perfil == "administrador":
        return perfil_alvo != "administrador"

    if perfil == "professor":
        return perfil_alvo == "estudante"

    return False



# CONFERIR SE O ACESSO FOI DENTRO DO HORÁRIO PERMITIDO
def dentroDoHorario(horario, data_hora):
    try:
        hora = datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S").hour
    except ValueError:
        return "indeterminado"

    if horario == "24h":
        return "sim"

    partes = horario.replace("h", "").split("-")

    if len(partes) != 2 or not (partes[0].isdigit() and partes[1].isdigit()):
        return "indeterminado"

    inicio = int(partes[0])
    fim = int(partes[1])

    if inicio <= fim:
        permitido = inicio <= hora < fim
    else:
        permitido = hora >= inicio or hora < fim

    if permitido:
        return "sim"
    return "nao"




# MONTAR O TEXTO QUE VAI PARA O AGENTE
def montarTexto(matricula_logada, perfil):
    consultar()
    consultarAcessos()
    consultarHistoricoIA()
    consultarBloqueadas
    
    texto = "data_hora,usuario,perfil,horario_permitido,dentro_do_horario,maquina,resultado\n"

    for acesso in acessos:

        if not podeVer(perfil, matricula_logada, acesso["matricula"]):
            continue

        info = dados.get(acesso["matricula"])

        if info:
            nome = info["nome"]
            perfil_alvo = info["perfil"]
            horario = info["horario"]
            dentro = dentroDoHorario(horario, acesso["data_hora"])
        else:
            nome = "desconhecido"
            perfil_alvo = "desconhecido"
            horario = "desconhecido"
            dentro = "indeterminado"

        texto += (
            f"{acesso['data_hora']},{nome},{perfil_alvo},{horario},{dentro},"
            f"{acesso['maquina']},{acesso['resultado']}\n"
        )

    texto2 = "data_hora,nome,perfil,maquina,pergunta\n"

    for uso in historicoIA:
        texto2 += (
            f"{uso['data_hora']},{uso['nome']},{uso['perfil']},{uso['maquina']},{uso['pergunta']}\n"
        )

    texto3 = f"""
    1 - caso a pergunta pedir alguma coisa relacionada a matratricula,fale que voce não tem acesso a matricula 
    e que é para o usuario verificar a matricula manualmente
    2 - quantidade de matriculas: {len(dados)}
    """

    texto4 = "maquinas bloqueadas:\n"
    for maquina in bloqueadas:
        texto4 += (f"{maquina}\n")


    return f"tentativas de login:\n{texto}\n {"-" * 60}\nhistorico do uso de IA:\n{texto2}\n{"_" * 60}\n{texto4}\n\n{texto3}"


# CONVERSA FECHADA (PERGUNTAS PRONTAS)
def conversaFechada(texto, perfil,matricula_logada):
    perguntas = PERGUNTAS.get(perfil, [])

    if not perguntas:
        print("Não há perguntas disponíveis para este perfil.")
        return

    while True:
        print("\nEscolha uma pergunta:")

        for i in range(len(perguntas)):
            print(f"{i + 1}. {perguntas[i]}")

        print("0. Sair")

        opcao = input("Opção: ").strip()

        if opcao == "0":
            break

        if opcao.isdigit() and 1 <= int(opcao) <= len(perguntas):
            pergunta = perguntas[int(opcao) - 1]
            falar_com_agente_texto(texto, pergunta, "SentinelaLog")
            registrarInteracaoIA(matricula_logada,pergunta)

        else:
            print("Opção inválida.")


# CONVERSA ABERTA (O ADMINISTRADOR DIGITA A PERGUNTA)
def conversaAberta(texto,matricula_logada):
    print("\nDigite sua pergunta (ou digite 0 para sair).")

    while True:
        pergunta = input("Pergunta: ").strip()

        if pergunta == "0":
            break

        if not pergunta:
            print("A pergunta não pode ficar vazia.")
            continue

        falar_com_agente_texto(texto, pergunta, "SentinelaLog")
        registrarInteracaoIA(matricula_logada,pergunta)


# CONVERSAR COM O AGENTE
def conversarComAgente(matricula_logada):
    consultar()

    info = dados.get(matricula_logada)

    if info is None:
        print("Usuário não encontrado.")
        return

    # o perfil vem do cadastro, nunca do que o usuário digita
    perfil = info["perfil"].lower()

    texto = montarTexto(matricula_logada, perfil)

    if texto.count("\n") <= 1:
        print("Não há acessos para enviar ao agente.")
        return

    print("Seus dados de acesso vão sair do computador e serão enviados à Groq.")
    confirmacao = input("Continuar? (s/n): ").lower().strip()

    if confirmacao != "s":
        print("Operação cancelada.")
        return

    conversaFechada(texto, perfil,matricula_logada)


# CONVERSAR COM O AGENTE DIGITANDO (SÓ ADMINISTRADOR)
def conversarComAgenteAberto(matricula_logada):
    consultar()

    info = dados.get(matricula_logada)

    if info is None:
        print("Usuário não encontrado.")
        return

    perfil = info["perfil"].lower()

    # a trava fica aqui dentro, e não só no menu
    if perfil != "administrador":
        print("Apenas administradores podem usar a conversa aberta.")
        return

    texto = montarTexto(matricula_logada, perfil)

    if texto.count("\n") <= 1:
        print("Não há acessos para enviar ao agente.")
        return

    print("Os dados de acesso vão sair do computador e serão enviados à Groq.")
    confirmacao = input("Continuar? (s/n): ").lower().strip()

    if confirmacao != "s":
        print("Operação cancelada.")
        return

    conversaAberta(texto,matricula_logada)