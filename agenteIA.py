from dadosGlobais import *
from crud import consultar
from manipularAcessos import consultarAcessos
from agente import falar_com_agente_texto
from datetime import datetime
from horario import verificarHorario


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

    return texto


# CONVERSA FECHADA (PERGUNTAS PRONTAS)
def conversaFechada(texto, perfil):
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
        else:
            print("Opção inválida.")


# CONVERSAR COM O AGENTE
def conversarComAgente(matricula_logada, perfil):
    texto = montarTexto(matricula_logada, perfil)

    if texto.count("\n") <= 1:
        print("Não há acessos para enviar ao agente.")
        return

    print("Seus dados de acesso vão sair do computador e serão enviados à Groq.")
    confirmacao = input("Continuar? (s/n): ").lower().strip()

    if confirmacao != "s":
        print("Operação cancelada.")
        return

    conversaFechada(texto, perfil)



if __name__== "__main__":
    matricula = input("Matrícula: ").strip()
    perfil = input("Perfil: ").strip().lower()
    conversarComAgente(matricula, perfil)