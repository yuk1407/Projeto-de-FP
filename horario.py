from datetime import datetime


#DE INICIO SO TEM UMA FUNÇÃO. CRIEI UM ARQUIVO SO PRA HORARIO PORQUE PROVAVELMENTE A GENTE VAI MEXER MAIS COM ISSO.

# DATA E HORÁRIO ATUAL
def agora(): # parte do horario, vou mexer nisso dps pra verificar se o usuario esta no horario permitido ou nao
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def verificarHorario(horario):
    horario = horario.strip().lower()

    # Permite acesso durante 24 horas
    if horario == "24h":
        return True

    # Verifica se existe um intervalo de horário
    if "-" not in horario:
        return False

    # Pega a hora atual
    horario_atual = datetime.now().hour

    # Separa o horário inicial e final
    inicio, fim = horario.split("-", 1)

    try:
        inicio = int(inicio.replace("h", "").strip())
        fim = int(fim.replace("h", "").strip())
    except ValueError:
        return False

    # Verifica se os horários são válidos
    if not (0 <= inicio <= 23 and 1 <= fim <= 24):
        return False

    # Verifica se está dentro do horário permitido
    if inicio <= horario_atual < fim:
            return True

    return False
