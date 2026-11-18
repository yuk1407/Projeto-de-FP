#todas as variaveis, listas, tuplas e dicionarios que sejam globais precisam ser declaradas aqui


dados = {}
acessos = [] #variável que guarda o histórico de tentativas de login 
bloqueadas = []  #  lista de máquinas bloqueadas

PERFIS = ("estudante", "professor", "administrador")

PERGUNTAS = {
    "estudante": [
        "Resuma os meus acessos.",
        "Tive alguma falha de login?",
        "Quais máquinas eu usei?"
    ],
    "professor": [
        "Resuma os acessos dos alunos.",
        "Algum aluno teve falha de login?",
        "Quais máquinas os alunos usaram?"
    ],
    "administrador": [
        "Quais acessos são suspeitos?",
        "Qual usuário tem mais falhas de login?",
        "Quais máquinas foram usadas por mais de uma pessoa?",
        "Resuma todos os acessos."
    ]
}
