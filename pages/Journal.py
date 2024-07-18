import streamlit as st
from news import news_data

st.set_page_config(page_title="Jornal de Jogos", page_icon=":newspaper:", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter+Var:wght@400;700&display=swap');

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
    body {
        font-family: 'Inter Var', sans-serif;
    }
    .content {
        max-width: 800px;
        margin: auto;
        padding: 20px;
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
    button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        background-color: #333;
        color: white;
        border: none;
    }
    button:hover {
        background-color: #555;
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
        content_with_subtitle = article['content'].replace('[SUBTITULO]', '<h2 style="font-size: 2em; font-weight: bold;">Subtítulo Adicionado</h2>')

        st.markdown(
            f"""
            <div class='content'>
                <div class='article-title' style='font-size: 2.5em; font-weight: bold;'>{article['title']}</div>
                <div class='article-content' style='font-size: 1.2em;'>{content_with_subtitle}</div>
                <br>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Voltar"):
            st.experimental_set_query_params() 
    else:
        st.write("Notícia não encontrada.")
else:


    st.header("Notícias Recentes")
    for article in news_data:
        col1, col2 = st.columns([1, 5])
        with col1:
            if "image" in article:
                st.image(article["image"], width=240)  #
            st.markdown(f"### <a href='?article_id={article['id']}' class='link'>{article['title']}</a>", unsafe_allow_html=True)
            st.write(article["excerpt"])
        st.markdown("---")
