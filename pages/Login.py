import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import bcrypt

# Conexão com o banco de dados
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

def main():
    st.set_page_config(page_title="MyGameHub", layout="wide")

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

    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(r"D:\cc\6p\eng 2\MyGameHub\src\images\341dd759-ea43-4c0d-b395-610fd28c3c2b.webp", width=820)  # Substitua pelo caminho da sua imagem

    # Lógica para exibição das páginas de Login e Registro
    if st.session_state.page == 'login':
        st.subheader("Login")
        username = st.text_input("Usuário", key='login_user')
        password = st.text_input("Senha", type="password", key='login_pass')
        
        if st.button("Entrar"):
            user = session.query(users).filter(users.c.username == username).first()
            if user and check_password(password, user.password):
                st.success("Login efetuado com sucesso!")
            else:
                st.error("Usuário ou senha incorretos!")

        if st.button("Criar nova conta"):
            st.session_state.page = 'register'

    elif st.session_state.page == 'register':
        st.subheader("Registrar")
        new_username = st.text_input("Nome de usuário", key='reg_user')
        new_password = st.text_input("Senha", type="password", key='reg_pass')
        confirm_password = st.text_input("Confirme a senha", type="password", key='reg_confirm_pass')
        
        if st.button("Registrar"):
            if new_password == confirm_password:
                hashed_password = hash_password(new_password)
                new_user = users.insert().values(username=new_username, password=hashed_password)
                session.execute(new_user)
                session.commit()
                st.success("Usuário registrado com sucesso! Por favor, faça login.")
                st.session_state.page = 'login'  # Redireciona para a tela de login após o registro
            else:
                st.error("As senhas não correspondem.")
        
        if st.button("Voltar ao login"):
            st.session_state.page = 'login'

if __name__ == "__main__":
    main()
