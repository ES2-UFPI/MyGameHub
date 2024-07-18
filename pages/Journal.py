import streamlit as st
from news import news_data

st.set_page_config(page_title="Jornal de Jogos", page_icon=":newspaper:", layout="wide")


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
        font-family: 'Inter Var', sans-serif;
        text-rendering: optimizeLegibility;
    }
    a {
        color: inherit;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    .link {
        color: #FFD700;
    }
    </style>
    <div class="title">Journal</div>
    """,
    unsafe_allow_html=True
) 

# Obter o ID do artigo da URL
query_params = st.experimental_get_query_params()
article_id = query_params.get("article_id", [None])[0]

if article_id:
    article = next((item for item in news_data if item["id"] == article_id), None)
    if article:
        st.title(article["title"])
        if "subtitle" in article:
            st.subheader(article["subtitle"])
        st.write(article["content"])
    else:
        st.write("Notícia não encontrada.")
else:
    # Seção de Notícias
    st.header("Notícias Recentes")
    for article in news_data:
        col1, col2 = st.columns([1, 5])
        with col1:
            if "image" in article:
                st.image(article["image"], width=240)  # Aumentar o tamanho da imagem
        with col2:
            st.markdown(f"### <a href='?article_id={article['id']}' class='link'>{article['title']}</a>", unsafe_allow_html=True)
            st.write(article["excerpt"])
        st.markdown("---")
