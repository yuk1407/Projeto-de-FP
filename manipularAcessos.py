from dadosGlobais import *
from crud import *
from horario import *
from datetime import datetime

# TODAS AS FUNÇÕES QUE CONTROLAM O ACESSO ESTÃO AQUI 


# CONSULTAR HISTÓRICO DE ACESSOS
def consultarAcessos(): # so vai pegar o acesso da pessoa, importante pra parte de sucesso e falha
    #carrega o histórico do arquivo
    acessos.clear()

    try:
        with open("acessos.txt", "r", encoding="utf8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",", 3)

                if len(partes) != 4:
                    continue

                matricula, data_hora, maquina, resultado = partes

                # descarta linhas com resultado desconhecido (inclui linhas forjadas com vírgulas)
                if resultado not in RESULTADOS:
                    continue
                # descarta linhas com data inválida
                try:
                    datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    continue

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
    #registra cada tentativa de login
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
    #identifica a última máquina usada
    for acesso in reversed(acessos):
        if (
            acesso["matricula"] == matricula
            and acesso["resultado"] == "sucesso"
        ):
            return acesso["maquina"]

    return "-"

