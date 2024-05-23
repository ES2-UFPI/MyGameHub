import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import bcrypt

#Configuração da Conexão com o BD:(usa sqlalchemy)
#URL de conexão com BD PostgreSQL(Está hospedado no render, irá expirar dia 21/06)
DATABASE_URL = "postgresql+psycopg2://mygamehub:gE2QDUghk39G75NtchODQt6XLUeZ8V9L@dpg-cp79fl63e1ms73agq3q0-a.virginia-postgres.render.com/loginbd"
engine = create_engine(DATABASE_URL)                                                        #Objeto que estabelece a conexão com o banco de dados 
metadata = MetaData()                                                                       #Metadados para descrever as tabelas do banco de dados

#Tabela users que contem colunas id,username,password
users = Table('users', metadata,                                                           
              Column('id', Integer, primary_key=True),
              Column('username', String, unique=True),
              Column('password', String))
metadata.create_all(engine)                                                                 #Cria a tabela users no bd, caso não exista

Session = sessionmaker(bind=engine)                                                         #Sessões de interação com BD
session = Session()



#Funções de Hashing e Verificação de Senhas(usa bcrypt)
def hash_password(password):                                                                #Gera um hash seguro para a senha fornecida
    salt = bcrypt.gensalt()         
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(password, hashed):                                                       #Verifica se a senha fornecida corresponde ao hash armazenado
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed)



#Interface do Usuário com StreamLit:(usa steamlit)
st.title('Sistema de Login e Registro')                                                     #Define o Titulo da Aplicação

menu = ["Login", "Registrar"]                                                               #Lista de opções do menu
choice = st.sidebar.selectbox("Menu", menu)                                                 #Cria um menu de navegação na barra lateral



#Lógica de Login:
if choice == "Login":
    username = st.text_input('Nome de usuário', key='login_username')                      #entrada de username e password
    password = st.text_input('Senha', type='password', key='login_password')
    if st.button('Login'):                                                                 #verificação do usuário e da senha
        user = session.query(users).filter(users.c.username == username).first()
        if user and check_password(password, user.password):
            st.success(f'Bem-vindo {user.username}!')
        else:
            st.error('Nome de usuário ou senha incorretos')



#Lógica de Registro:(usa streamlit)
elif choice == "Registrar":
    new_username = st.text_input('Nome de usuário', key='reg_username')                   #Registro de nome de usuário(reg_username), senha(reg_password), e confirmação de senha
    new_password = st.text_input('Senha', type='password', key='reg_password')
    confirm_password = st.text_input('Confirme a senha', type='password', key='reg_confirm')
    if st.button('Registrar'):
        if new_password == confirm_password:                                             #Verificação se senhas correspondem
            user_exist = session.query(session.query(users).filter(users.c.username == new_username).exists()).scalar() #Consulta banco de dados para verificar se username está em uso
            if not user_exist:                                                          
                hashed_password = hash_password(new_password).decode('utf-8')
                new_user = users.insert().values(username=new_username, password=hashed_password)
                session.execute(new_user)
                session.commit()
                st.success('Usuário criado com sucesso. Por favor, faça login.')
            else:
                st.error('Este nome de usuário já está em uso')
        else:
            st.error('As senhas não correspondem')