from dadosGlobais import *
from crud import *
from manipularAcessos import *
from status import *

#ESSE ARQUIVO É REPONSAVEL PELO RELATORIO, TANTO PRA CRIAR, SALVAR E OUTRAR FUNCIONALIDADES FUTURAS 







# SALVAR RELATÓRIO
def salvarRelatorio(relatorio): # so salvar o relatorio no arquivo
    with open("relatorio.txt", "w", encoding="utf8") as arquivo:
        arquivo.write(relatorio)


# CRIAR RELATÓRIO
def criarRelatorio():
    consultar()

    relatorio = (
        f"{'Matrícula':>12}{'Nome':>20}{'Perfil':>16}"
        f"{'Acesso':>22}{'Máquina':>18}{'Status':>10}"
        f"{'Observações':>20}  Motivo\n"
    )

    for chave, itens in dados.items():
        status, motivo = classificarUsuario(chave, itens)

        relatorio += (
            f"{chave:>12}{itens['nome']:>20}{itens['perfil']:>16}"
            f"{itens['acesso']:>22}{ultimaMaquina(chave):>18}{status:>10}"
            f"{itens['observacoes']:>20}  {motivo}\n"
        )

    salvarRelatorio(relatorio)

    print("Relatório salvo em relatorio.txt")