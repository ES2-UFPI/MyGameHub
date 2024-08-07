import pandas as pd
import streamlit as st

class GameSearchFacade:
    def __init__(self):
        self.data = self.load_and_prepare_data()
        self.all_tags = self.extract_all_tags()

    @staticmethod
    def clean_price(price):
        if price.lower() == 'free':
            return 0.0
        return float(price.replace('$', '').replace(',', ''))

    @staticmethod
    def load_and_prepare_data():
        data = GameSearchFacade.load_data()
        data = GameSearchFacade.clean_data(data)
        return data

    @staticmethod
    @st.cache_data
    def load_data():
        return pd.read_csv('src/data/processed_data.csv')

    @staticmethod
    def clean_data(data):
        data['original_price'] = data['original_price'].apply(GameSearchFacade.clean_price)
        data['popular_tags'] = data['popular_tags'].fillna('').apply(
            lambda x: [tag.strip() for tag in x.strip('[]').replace('"', '').split(',')]
        )
        return data

    def extract_all_tags(self):
        return sorted(set(tag for tags in self.data['popular_tags'] for tag in tags if tag))

    def search_games(self, query='', selected_tags=None, min_price=None, max_price=None):
        selected_tags = selected_tags or []
        results = self.filter_by_query(query)
        results = self.filter_by_tags(results, selected_tags)
        results = self.filter_by_price(results, min_price, max_price)
        return results

    def filter_by_query(self, query):
        if not query:
            return self.data.copy()
        return self.data[self.data['title'].str.contains(query, case=False, na=False)]

    def filter_by_tags(self, data, selected_tags):
        if not selected_tags:
            return data
        return data[data['popular_tags'].apply(lambda tags: all(tag in tags for tag in selected_tags))]

    def filter_by_price(self, data, min_price, max_price):
        if min_price is None or max_price is None:
            return data
        return data[data['original_price'].between(min_price, max_price)]

    def get_all_tags(self):
        return self.all_tags

# Função para configurar a interface do usuário
def configure_interface(game_search):
    set_page_style()
    st.sidebar.markdown("# Busca 🔎")
    st.title('Sistema de Busca de Jogos')

    query = st.text_input("Digite o nome do jogo que deseja buscar:")

    min_price, max_price = get_price_range(game_search)

    selected_tags = st.multiselect('Selecione as tags populares:', game_search.get_all_tags())

    results = game_search.search_games(query, selected_tags, min_price, max_price)

    display_results(query, min_price, max_price, selected_tags, results)

def set_page_style():
    page_bg_img = '''
    <style>
    body {
        background-color: #d3d3d3;
    }

    #header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        background-color: #4f4f4f;
        color: white;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def get_price_range(game_search):
    return st.slider(
        'Selecione o intervalo de preços:',
        min_value=float(game_search.data['original_price'].min()),
        max_value=float(game_search.data['original_price'].max()),
        value=(float(game_search.data['original_price'].min()), float(game_search.data['original_price'].max()))
    )

def display_results(query, min_price, max_price, selected_tags, results):
    if not results.empty:
        st.write(f"Resultados para '{query}' com preço entre {min_price} e {max_price} e tags: {', '.join(selected_tags)}:")
        st.dataframe(results)
    else:
        st.write("Digite o nome de um jogo para buscar e ajuste o filtro de preço e tags se desejar.")

# Instanciar o facade
game_search = GameSearchFacade()

# Configurar a interface do usuário
configure_interface(game_search)