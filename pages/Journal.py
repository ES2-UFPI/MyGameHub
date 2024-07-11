import streamlit as st
from news import news_data

# Configuração da página
st.set_page_config(page_title="Jornal de Jogos", page_icon=":newspaper:", layout="wide")

# Centralizar o título
st.markdown(
    """
    <style>
    .title {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        font-size: 3em;
        font-weight: bold;
    }
    </style>
    <div class="title">Journal</div>
    """,
    unsafe_allow_html=True
)

# Seção de Notícias
st.header("Notícias Recentes")
for article in news_data:
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(article["image"], width=100)
    with col2:
        st.markdown(f"### [{article['title']}](?article_id={article['id']})")
        st.write(article["excerpt"])
        st.markdown(f"<small>{article['time']} - {article['comments']} comentários</small>", unsafe_allow_html=True)
    st.markdown("---")

# Obter o ID do artigo da URL
article_id = st.experimental_get_query_params().get("article_id", [None])[0]

