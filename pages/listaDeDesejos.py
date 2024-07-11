import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import bcrypt

# Configuração da Conexão com o BD
DATABASE_URL = "postgresql://root:wRoNcAkjnwCvGRdxD2OKAeSevhOLwJ5b@dpg-cq6i442ju9rs73e8bleg-a.oregon-postgres.render.com/loginbd_fg6e"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Tabela users
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String, unique=True),
              Column('password', String))

# Tabela wishlist
wishlist = Table('wishlist', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user_id', Integer),
                 Column('game_id', Integer))

# Tabela games (supondo que você já tenha essa tabela)
games = Table('games', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('genre', String),
              Column('platform', String))

metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Página da Lista de Desejos
st.title('Minha Lista de Desejos')

username = st.text_input('Nome de usuário', key='wishlist_username')
password = st.text_input('Senha', type='password', key='wishlist_password')

if st.button('Login para acessar a lista de desejos'):
    user = session.query(users).filter(users.c.username == username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        st.success(f'Bem-vindo {user.username}!')
        
        # Adicionar jogo à lista de desejos
        game_name = st.text_input('Nome do Jogo para adicionar à lista de desejos')
        if st.button('Adicionar à lista de desejos'):
            game = session.query(games).filter(games.c.name == game_name).first()
            if game:
                new_wishlist_item = wishlist.insert().values(user_id=user.id, game_id=game.id)
                session.execute(new_wishlist_item)
                session.commit()
                st.success('Jogo adicionado à lista de desejos com sucesso!')
            else:
                st.error('Jogo não encontrado')

        # Exibir lista de desejos
        st.header('Sua Lista de Desejos')
        wishlist_items = session.query(wishlist).filter(wishlist.c.user_id == user.id).all()
        if wishlist_items:
            for item in wishlist_items:
                game = session.query(games).filter(games.c.id == item.game_id).first()
                st.write(f"Jogo: {game.name} | Gênero: {game.genre} | Plataforma: {game.platform}")
        else:
            st.write('Sua lista de desejos está vazia.')
    else:
        st.error('Nome de usuário ou senha incorretos')
