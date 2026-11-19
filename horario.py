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

    # Verifica horários normais (exemplo: 7h-14h)
    if inicio < fim:
        return inicio <= horario_atual < fim

# Verifica horários que atravessam a meia-noite (exemplo: 22h-6h)
    if inicio > fim:
        return horario_atual >= inicio or horario_atual < fim

    return False


def validarHorario(horario):
    horario = horario.strip().lower()

    if horario == "24h":
        return True

    if horario.count("-") != 1:
        return False

    inicio, fim = horario.split("-", 1)

    inicio = inicio.strip()
    fim = fim.strip()

    if not inicio.endswith("h") or not fim.endswith("h"):
        return False

    inicio = inicio[:-1]
    fim = fim[:-1]

    if not inicio.isdigit() or not fim.isdigit():
        return False

    inicio = int(inicio)
    fim = int(fim)

    if not (0 <= inicio <= 23 and 0 <= fim <= 24):
        return False

    if inicio == fim:
        return False

    return True
