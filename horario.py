from datetime import datetime


#DE INICIO SO TEM UMA FUNÇÃO. CRIEI UM ARQUIVO SO PRA HORARIO PORQUE PROVAVELMENTE A GENTE VAI MEXER MAIS COM ISSO.

# DATA E HORÁRIO ATUAL
def agora(): # parte do horario, vou mexer nisso dps pra verificar se o usuario esta no horario permitido ou nao
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

