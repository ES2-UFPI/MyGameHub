import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# Configuração da Conexão com o BD
DATABASE_URL = "postgresql://mygamehub:XnDyt3Xa8O66bmE7Jbc3ly6zZ3f4eiGH@dpg-cqlnivdumphs7397s8k0-a.oregon-postgres.render.com/loginbd_6tj3"

# Configuração da Conexão com o Banco de Dados
class Database:
    def __init__(self, url):
        self.engine = create_engine(url)
        self.metadata = MetaData()
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

# Facade para Gerenciamento de Usuários e Wishlist
class WishlistFacade:
    def __init__(self, db):
        self.db = db
        self.users = Table('users', self.db.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('username', String, unique=True),
                           Column('password', String))

        self.wishlist = Table('wishlist', self.db.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user_id', Integer),
                              Column('game_id', String))

    def get_logged_in_user(self, username):
        return self.db.session.query(self.users).filter(self.users.c.username == username).first()

    def add_to_wishlist(self, user_id, game_id):
        new_wishlist_item = self.wishlist.insert().values(user_id=user_id, game_id=game_id)
        self.db.session.execute(new_wishlist_item)
        self.db.session.commit()

    def remove_from_wishlist(self, user_id, game_id):
        self.db.session.execute(self.wishlist.delete().where(self.wishlist.c.user_id == user_id).where(self.wishlist.c.game_id == game_id))
        self.db.session.commit()

    def get_wishlist_items(self, user_id):
        return self.db.session.query(self.wishlist).filter(self.wishlist.c.user_id == user_id).all()

# Funções de Interface com o Usuário
def check_user_logged_in():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Por favor, faça login para acessar a lista de desejos.")
        st.stop()

def display_wishlist(facade, user_id):
    st.header('Sua Lista de Desejos')
    wishlist_items = facade.get_wishlist_items(user_id)
    if wishlist_items:
        for item in wishlist_items:
            col1, col2 = st.columns([3, 1])
            col1.write(f"Jogo: {item.game_id}")
            if col2.button('Remover', key=item.id):
                facade.remove_from_wishlist(user_id, item.game_id)
                st.success(f"Jogo {item.game_id} removido da lista de desejos com sucesso!")
                st.experimental_rerun()  # Atualizar a página para refletir a remoção
    else:
        st.write('Sua lista de desejos está vazia.')

# Função Principal
def main():
    check_user_logged_in()
    username = st.session_state.username

    # Instancia a conexão com o banco de dados e a facade
    db = Database(DATABASE_URL)
    facade = WishlistFacade(db)

    user = facade.get_logged_in_user(username)
    if user:
        st.title('Minha Lista de Desejos')
        st.sidebar.markdown("# Wishlist ✨")

        game_id = st.text_input('Nome do Jogo para adicionar à lista de desejos')
        if st.button('Adicionar à lista de desejos'):
            if game_id:
                facade.add_to_wishlist(user.id, game_id)
                st.success('Jogo adicionado à lista de desejos com sucesso!')
            else:
                st.error('Por favor, insira o nome de um jogo.')

        display_wishlist(facade, user.id)
    else:
        st.error("Não foi possível recuperar o usuário logado.")

if __name__ == "__main__":
    main()
