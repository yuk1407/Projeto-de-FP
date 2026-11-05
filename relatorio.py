from dadosGlobais import *
from crud import *
from manipularAcessos import *

#ESSE ARQUIVO É REPONSAVEL PELO RELATORIO, TANTO PRA CRIAR, SALVAR E OUTRAR FUNCIONALIDADES FUTURAS 







# SALVAR RELATÓRIO
def salvarRelatorio(relatorio): # so salvar o relatorio no arquivo
    with open("relatorio.txt", "w", encoding="utf8") as arquivo:
        arquivo.write(relatorio)


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