import pandas as pd
import streamlit as st

class GameSearchFacade:
    def __init__(self):
        self.data = self.load_data()
        self.all_tags = self.extract_all_tags()

    @staticmethod
    def clean_price(price):
        if price.lower() == 'free':
            return 0.0
        return float(price.replace('$', '').replace(',', ''))

    @staticmethod
    @st.cache_data
    def load_data():
        data = pd.read_csv('src/data/processed_data.csv')
        data['original_price'] = data['original_price'].apply(GameSearchFacade.clean_price)
        data['popular_tags'] = data['popular_tags'].fillna('').apply(
            lambda x: [tag.strip() for tag in x.strip('[]').replace('"', '').split(',')]
        )
        return data

    def extract_all_tags(self):
        return sorted(set(tag for tags in self.data['popular_tags'] for tag in tags if tag))

    def search_games(self, query='', selected_tags=None, min_price=None, max_price=None):
        if selected_tags is None:
            selected_tags = []
        
        results = self.data.copy()
        
        if query:
            results = results[results['title'].str.contains(query, case=False, na=False)]
        
        if selected_tags:
            results = results[results['popular_tags'].apply(lambda tags: all(tag in tags for tag in selected_tags))]
        
        if min_price is not None and max_price is not None:
            results = results[results['original_price'].between(min_price, max_price)]
        
        return results

    def get_all_tags(self):
        return self.all_tags

# Instanciar o facade
game_search = GameSearchFacade()

# Configurar a interface do usuário
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
st.sidebar.markdown("# Busca 🔎")

st.title('Sistema de Busca de Jogos')
query = st.text_input("Digite o nome do jogo que deseja buscar:")

# Slider para filtrar por preço
min_price, max_price = st.slider(
    'Selecione o intervalo de preços:',
    min_value=float(game_search.data['original_price'].min()),
    max_value=float(game_search.data['original_price'].max()),
    value=(float(game_search.data['original_price'].min()), float(game_search.data['original_price'].max()))
)

# Campo de seleção para filtrar por tags populares
selected_tags = st.multiselect('Selecione as tags populares:', game_search.get_all_tags())

# Buscar jogos com base na entrada do usuário
results = game_search.search_games(query, selected_tags, min_price, max_price)

if not results.empty:
    st.write(f"Resultados para '{query}' com preço entre {min_price} e {max_price} e tags: {', '.join(selected_tags)}:")
    st.dataframe(results)
else:
    st.write("Digite o nome de um jogo para buscar e ajuste o filtro de preço e tags se desejar.")
