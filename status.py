import re
from datetime import datetime
from dadosGlobais import *
from maquinasBloqueadas import maquinaBloqueada


# VERIFICA SE O HORÁRIO DO ACESSO ESTÁ DENTRO DO PERMITIDO
def horarioPermitido(horario, data_hora):
    horario = horario.lower().strip()

    if horario in ("24h", "24"):
        return True

    numeros = re.findall(r"\d+", horario)  # "7h-18h" -> ["7", "18"]

    if len(numeros) < 2:
        return True  # formato desconhecido: não pune o usuário

    inicio, fim = int(numeros[0]), int(numeros[1])
    hora = datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S").hour

    if inicio <= fim:
        return inicio <= hora < fim

    return hora >= inicio or hora < fim  # horário que vira a noite (ex: 22h-6h)


# QUANTAS VEZES A MÁQUINA JÁ FALHOU NO LOGIN
def falhasDaMaquina(maquina):
    return sum(
        1 for a in acessos
        if a["maquina"].lower() == maquina.lower()
        and a["resultado"] == "falha"
    )


# ÚLTIMO REGISTRO DE ACESSO DA MATRÍCULA
def ultimoAcesso(matricula):
    for acesso in reversed(acessos):
        if acesso["matricula"] == matricula:
            return acesso

    return None

def classificarUsuario(matricula, info):
    acesso = ultimoAcesso(matricula)

    if acesso is None:
        return "Normal", "sem acessos"

    maquina = acesso["maquina"]
    falhas = falhasDaMaquina(maquina)
    fora_horario = not horarioPermitido(info["horario"], acesso["data_hora"])
    bloqueada = maquinaBloqueada(maquina)

    motivos = []

    if bloqueada:
        motivos.append("máquina bloqueada")
    if falhas > 0:
        motivos.append(f"{falhas} falha(s) na máquina")
    if fora_horario:
        motivos.append("fora do horário")

    if bloqueada or falhas >= 3 or (fora_horario and falhas > 0):
        status = "Crítico"
    elif fora_horario or falhas > 0:
        status = "Suspeito"
    else:
        status = "Normal"

    return status, ", ".join(motivos) if motivos else "-"