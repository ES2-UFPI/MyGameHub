import pandas as pd
import streamlit as st

def clean_price(price):
    if price.lower() == 'free':
        return 0.0
    return float(price.replace('$', '').replace(',', ''))

@st.cache_data
def load_data():
    data = pd.read_csv('src/data/processed_data.csv')
    data['original_price'] = data['original_price'].apply(clean_price)  # Limpar preços
    # Limpar as tags para remover chaves e garantir que não haja duplicatas
    data['popular_tags'] = data['popular_tags'].fillna('').apply(lambda x: [tag.strip() for tag in x.strip('[]').replace('"', '').split(',')])  
    return data

data = load_data()

# Extrair todas as tags únicas e remover duplicatas
all_tags = sorted(set(tag for tags in data['popular_tags'] for tag in tags if tag))

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
    min_value=float(data['original_price'].min()),
    max_value=float(data['original_price'].max()),
    value=(float(data['original_price'].min()), float(data['original_price'].max()))
)

# Campo de seleção para filtrar por tags populares
selected_tags = st.multiselect('Selecione as tags populares:', all_tags)

if query or selected_tags:
    results = data.copy()
    
    if query:
        results = results[results['title'].str.contains(query, case=False, na=False)]
    
    if selected_tags:
        results = results[results['popular_tags'].apply(lambda tags: all(tag in tags for tag in selected_tags))]
    
    results = results[results['original_price'].between(min_price, max_price)]
    
    st.write(f"Resultados para '{query}' com preço entre {min_price} e {max_price} e tags: {', '.join(selected_tags)}:")
    st.dataframe(results)
else:
    st.write("Digite o nome de um jogo para buscar e ajuste o filtro de preço e tags se desejar.")
