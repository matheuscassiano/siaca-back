# SIACA - Sistema de Controle Acadêmico

## Descrição do Projeto
O Sistema Acadêmico é uma API desenvolvida com Django REST Framework, com o objetivo de facilitar a construção de horários de aulas e o gerenciamento de turmas e salas em instituições de ensino. 
A API fornece endpoints para criar, atualizar, visualizar e deletar dados relacionados a alunos, professores, coordenadores, cursos, grades, turmas, salas e horários de aulas.

## Como Executar o Projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. Certifique-se de ter o Python instalado em sua máquina (versão 3.6 ou superior).

2. Clone o repositório do projeto do GitHub.

3. Crie um ambiente virtual para o projeto e ative-o:
```
python -m virtualenv env
source env/bin/activate # No Windows: env\Scripts\activate
```


4. Instale as dependências do projeto:
```
pip install -r requirements.txt
```


5. Realize as migrações do banco de dados:
```
python manage.py migrate
```


6. Crie um superusuário para acessar o painel de administração:
```
python manage.py createsuperuser
```


7. Inicie o servidor de desenvolvimento:
```
python manage.py runserver
```

A API estará disponível em `http://localhost:8000/`.

8. Credenciais de EMAIL:
É necessário criar um arquivo ```credentials.py``` na pasta siaca, com as constantes EMAIL_USER e EMAIL_PASSWORD (uma senha de app deve ser utilizada)


![image](https://github.com/matheuscassiano/siaca-back/assets/9613261/7364a84a-a64d-41d6-8095-e6859c4f9b50)




## Responsáveis
**Marcus Vinicius Gomes Pestana**

**José Vanderley Pereira da Silva Filho**
