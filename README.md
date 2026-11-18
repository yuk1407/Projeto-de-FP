# Sistema de sentinelaLog

### Nosso projeto foi criado a fim de simular um sistema de segurança. Utilizamos um cenário de um ADM que consegue acessar dados de uma escola, também tem os perfis de professor e estudante dentro do código.

### Ao rodar o código pela primeira vez deve-se criar um login para o ADM, a matrícula do ADM, por ser algo sério, não será possível ser consultada, o usuário(ADM) deve manter o seu acesso com ele

### O login inicial (Quando não tem um ADM já existente) tem:
- Nome do ADM
- Matrícula do ADM

### Com ADM já existente:
- Login
- Sair

### dentre as opçõe que podem ser acessadas pelo ADM estão :

- Registrar usuário
- Visualizar usuário
- Atualizar usuário
- Deletar usuário
- Revelar matrícula
- Criar relatório
- Bloquear máquina
- Desbloquear máquina
- Agente IA
- Sair

### Entendemos que o ADM está em uma posição de controle e manipulação de arquivos e dados, mas, o unico dado que não será possível alterar é a matrícula do usuário.
### A matrícula é a a chave do nosso dicionário, todos os outros dados presentes no código (nome, horário de acesso etc...) estão sendo relacionados a matrícula. Por isso não colocamos a opção do ADM alterar uma matrícula e sim, os dados que estão atrelados a ela

### O perfil do professor e do aluno tera:

- Visualizar seu usuário
- Atualizar seu usuário
- Sair

### Os dados são salvos em 3 arquivos, cada arquivo contem uma parte das informações que separamos para que o ADM possa analizar da forma em que ele achar melhor.

## Os arquivos são : 

## Acessos.txt 
### Nessa área colocamos informações como a matrícula, horário de acesso, computador em que a tentativa de login foi feita e o sucesso/falha dessa tentativa

![Acessos](Imagens/Acessos.png)
## Arquivos.txt 
### Nessa área colocamos os seguintes dados :
### Matrícula, Nome, Perfil, Horário de acesso permitido, ultimo acesso do usuário e alguma observação(opicional).

![Arquivos](Imagens/Arquivos.png)

## Relatório
### Nessa área colocamos os seguintes dados :
### Matrícula, Nome, Perfil, Acesso, Máquinas, Status, Observações e Motivo(Status)

![Relatório](Imagens/Relatorio.png)

## IA - Groq

### Utilizar um agente de IA é um dos focos do nosso projeto. A utilidade da inteligencia artificial no trabalho que produzimos é adiantar o serviço de buscas "Globais", por exemplo, se o ADM quiser saber a quantidade de matrículas realizadas, ele pode pedir para a IA e ela lhe dará esse resultado.

### A depender da sua posição no sistema, se você for estudante ou professor, terá acesso restrito aos dados que a IA poderá lhe passar.

![Plataforma da IA](Imagens/Plataforma%20da%20IA.png)

## Como utilizar o código?


### O código foi pensado para ser uma plataforma bem intuitiva, possível de ser utilizada por pessoas com níveis de domínio diversos na área de TI.

### 1. Opções de Ações:
- As ações foram pensadas para serem precisas.
- Ao clicar em uma das ações, como "Atualizar usuário" a pessoa conseguirá alterar dados de acordo com seu perfil.
- O usuário do código não precisará escrever, apenas precisa clicar na opção e ela vai acontecer.
- Cada ação é delimitada pelo perfil do usuário, sendo o ADM aquele com mais opções a serem realizadas, já o professor e o estudante tendo opções mais limitadas.

### 2. Facilidade em analisar os dados:
- O ADM consegue alterar os dados apenas sabendo da matrícula.
- Utilizamos dicionário para que todos os dados de um usuário estejam linkados com a sua matrícula

 ### 3. Consulta da IA
- A presença da IA está para conseguir pegar informações necessária às ações do ADM
- Pegar a quantidade de matrículas, nome atrelado a essa matrícula, informar máquinas bloqueadas, máquinas suspeitas etc...
- A hierarquia também está presenta no uso da IA

# Grupo:

### André Allysson
### Bernado Goudel
### Matheus Luiz
### Pedro Miguel
### Steven Kang Lin

