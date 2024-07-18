# login.py
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import bcrypt

    # CSS para personalizar a interface
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;  /* Cor verde */
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
        font-size: 16px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #45a049;  /* Cor mais escura para hover */
    }
    </style>
    """, unsafe_allow_html=True)

# Configuração da Conexão com o BD
DATABASE_URL = "postgresql://root:wRoNcAkjnwCvGRdxD2OKAeSevhOLwJ5b@dpg-cq6i442ju9rs73e8bleg-a.oregon-postgres.render.com/loginbd_fg6e"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Definição da tabela 'users'
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String, unique=True),
              Column('password', String),
              Column('name', String),
              Column('gender', String),
              autoload_with=engine)

# Funções de hashing e verificação de senha
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Função para página de login
def login_page():
    st.title('Sistema de Login e Registro')

    menu = ["Login", "Registrar"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        username = st.text_input('Nome de usuário', key='login_username')
        password = st.text_input('Senha', type='password', key='login_password')
        
        if st.button('Entrar'):
            user = session.query(users).filter(users.c.username == username).first()
            if user and check_password(password, user.password):
                st.success(f'Bem-vindo {user.username}!')
                st.session_state.logged_in = True
                st.session_state.username = username
                # Presumindo que você deseje redirecionar após login
                st.session_state.page = 'profile'
            else:
                st.error('Nome de usuário ou senha incorretos')

    elif choice == "Registrar":
        new_username = st.text_input('Nome de usuário', key='reg_username')
        new_password = st.text_input('Senha', type='password', key='reg_password')
        confirm_password = st.text_input('Confirme a senha', type='password', key='reg_confirm_pass')
        
        if st.button('Registrar'):
            if new_password == confirm_password:
                user_exist = session.query(session.query(users).filter(users.c.username == new_username).exists()).scalar()
                if not user_exist:
                    hashed_password = hash_password(new_password)
                    new_user = users.insert().values(username=new_username, password=hashed_password)
                    session.execute(new_user)
                    session.commit()
                    st.success('Usuário criado com sucesso. Por favor, faça login.')
                    st.session_state.page = 'login'
                else:
                    st.error('Este nome de usuário já está em uso')
            else:
                st.error('As senhas não correspondem.')

if __name__ == "__main__":
    login_page()
