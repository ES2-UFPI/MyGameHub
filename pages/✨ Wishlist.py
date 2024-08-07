import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# Configuração da Conexão com o BD
DATABASE_URL = "postgresql://mygamehub:XnDyt3Xa8O66bmE7Jbc3ly6zZ3f4eiGH@dpg-cqlnivdumphs7397s8k0-a.oregon-postgres.render.com/loginbd_6tj3"

try:
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    #st.write("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}")

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

def check_user_logged_in():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Por favor, faça login para acessar a lista de desejos.")
        st.stop()

def get_logged_in_user():
    username = st.session_state.username
    user = session.query(users).filter(users.c.username == username).first()
    if user:
        st.write(f"Usuário logado: {user.username}")
    return user

def add_to_wishlist(user_id, game_id):
    new_wishlist_item = wishlist.insert().values(user_id=user_id, game_id=game_id)
    session.execute(new_wishlist_item)
    session.commit()
    st.success('Jogo adicionado à lista de desejos com sucesso!')

def remove_from_wishlist(user_id, game_id):
    session.execute(wishlist.delete().where(wishlist.c.user_id == user_id).where(wishlist.c.game_id == game_id))
    session.commit()

def display_wishlist(user_id):
    st.header('Sua Lista de Desejos')
    wishlist_items = session.query(wishlist).filter(wishlist.c.user_id == user_id).all()
    if wishlist_items:
        for item in wishlist_items:
            col1, col2 = st.columns([3, 1])
            col1.write(f"Jogo: {item.game_id}")
            if col2.button('Remover', key=item.id):
                remove_from_wishlist(user_id, item.game_id)
                st.success(f"Jogo {item.game_id} removido da lista de desejos com sucesso!")
                st.experimental_rerun()  # Atualizar a página para refletir a remoção
    else:
        st.write('Sua lista de desejos está vazia.')

def main():
    check_user_logged_in()
    user = get_logged_in_user()

    if user:
        st.title('Minha Lista de Desejos')
        st.sidebar.markdown("# Wishlist ✨")

        game_id = st.text_input('Nome do Jogo para adicionar à lista de desejos')
        if st.button('Adicionar à lista de desejos'):
            if game_id:
                add_to_wishlist(user.id, game_id)
            else:
                st.error('Por favor, insira o nome de um jogo.')

        display_wishlist(user.id)
    else:
        st.error("Não foi possível recuperar o usuário logado.")

if __name__ == "__main__":
    main()
