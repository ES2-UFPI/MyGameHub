import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# Configuração da Conexão com o BD
DATABASE_URL = "postgresql://mygamehub:XnDyt3Xa8O66bmE7Jbc3ly6zZ3f4eiGH@dpg-cqlnivdumphs7397s8k0-a.oregon-postgres.render.com/loginbd_6tj3"
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
                 Column('game_id', String))

metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Verificar se o usuário está logado
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Por favor, faça login para acessar a lista de desejos.")
    st.stop()

# Obter informações do usuário logado
username = st.session_state.username
user = session.query(users).filter(users.c.username == username).first()

# Página da Lista de Desejos
st.title('Minha Lista de Desejos')
st.sidebar.markdown("# Wishlist ✨")

# Adicionar jogo à lista de desejos
game_id = st.text_input('Nome do Jogo para adicionar à lista de desejos')
if st.button('Adicionar à lista de desejos'):
    if game_id:
        new_wishlist_item = wishlist.insert().values(user_id=user.id, game_id=game_id)
        session.execute(new_wishlist_item)
        session.commit()
        st.success('Jogo adicionado à lista de desejos com sucesso!')
    else:
        st.error('Por favor, insira o nome de um jogo.')

# Função para remover item da lista de desejos
def remove_wishlist_item(user_id, game_id):
    session.execute(wishlist.delete().where(wishlist.c.user_id == user_id).where(wishlist.c.game_id == game_id))
    session.commit()

# Exibir lista de desejos
st.header('Sua Lista de Desejos')
wishlist_items = session.query(wishlist).filter(wishlist.c.user_id == user.id).all()
if wishlist_items:
    for item in wishlist_items:
        col1, col2 = st.columns([3, 1])
        col1.write(f"Jogo: {item.game_id}")
        if col2.button('Remover', key=item.id):
            remove_wishlist_item(user.id, item.game_id)
            st.success(f"Jogo {item.game_id} removido da lista de desejos com sucesso!")
            st.experimental_rerun()  # Atualizar a página para refletir a remoção
else:
    st.write('Sua lista de desejos está vazia.')