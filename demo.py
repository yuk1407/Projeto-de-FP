"""
demo.py — Demonstração ao vivo do agente (Aula 27)

Coloque na mesma pasta: agente.py, credenciais_exemplo.csv, acessos_exemplo.csv
e o seu arquivo .env com a chave (copie o .env.example e preencha).
Rode com: python demo.py
"""

from agente import falar_com_agente

TURMAS = {
    "A": ("credenciais_exemplo.csv", "CofreSeguro"),
    "B": ("acessos_exemplo.csv", "SentinelaLog"),
}

turma = input("Turma (A ou B)? > ").strip().upper()
while turma not in TURMAS:
    turma = input("Digite A ou B > ").strip().upper()

arquivo, sistema = TURMAS[turma]
print(f"\nUsando {arquivo} no sistema {sistema}. Digite 'sair' para encerrar.")

while True:
    pergunta = input("\nPergunta > ").strip()
    if pergunta.lower() == "sair":
        break
    falar_com_agente(arquivo, pergunta, sistema)
