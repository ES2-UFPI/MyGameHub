import streamlit as st
from news import news_data
import datetime

st.title('Journal 📰')
st.sidebar.markdown("# Journal 📰")
st.markdown(
    """
    <style>
    .title {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2.5em;
        margin-bottom: 20px;
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
    a.link {
        color: black;  
    }
    .button-link {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        background-color: #white;
        color: white;
        text-align: center;
        text-decoration: none;
    }
    .button-link:hover {
        background-color: #gray;
    }
    .company-title {
        font-size: 1.1em;
        color: gray;
        margin-top: -10px;
    }
    .article-title {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 200px;
        color:#e6735e;  
    }
    .article-content {
        font-size: 1.3em;
        line-height: 1.6;
    }
    .subtitle {
        font-size: 1.5em;
        font-weight: bold;
        margin: 30px 0 10px;
        color: #e6735e;  
    }
    .article-image {
        width: 100%;
        height: auto;
        margin: 20px 0;
    }
    .related-section {
        margin-top: 30px;
        padding: 20px;
        background-color: #white;
        border-radius: 10px;
        display: flex;
        align-items: center;
    }
    .related-section img {
        width: 80px;
        height: 80px;
        margin-right: 20px;
    }
    .related-section div {
        display: flex;
        flex-direction: column;
    }
    .related-section a {
        font-size: 1.2em;
        font-weight: bold;
    }
    .related-section a:hover {
        color: #black;
    }
    .publish-date {
        font-size: 0.9em;
        color: gray;
        margin-top: -10px;
    }

    @media (max-width: 768px) {
        .title {
            font-size: 2em;
        }
        .search-bar {
            width: 100%;
            float: none;
            margin-top: 10px;
        }
        .related-section {
            flex-direction: column;
            align-items: flex-start;
        }
        .related-section img {
            width: 100%;
            height: auto;
            margin-bottom: 10px;
        }
        .related-section div {
            align-items: flex-start;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para formatar a data de publicação
def format_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %b %Y")

# Barra de pesquisa
search_query = st.text_input("Pesquisar jogo:", "", key="search", placeholder="Digite o nome do jogo...")

# Obter o ID do artigo da URL
query_params = st.experimental_get_query_params()
article_id = query_params.get("article_id", [None])[0]
game_name = query_params.get("game", [None])[0]

# Filtrar notícias com base na pesquisa
if search_query:
    filtered_articles = [item for item in news_data if search_query.lower() in item["game"].lower()]
else:
    filtered_articles = news_data

if article_id:
    article = next((item for item in filtered_articles if item["id"] == article_id), None)
    if article:
        st.markdown(
            f"""
            <div class='content'>
                <div class='article-title'>{article['title']}</div>
                <div class='publish-date'>Publicado em {format_date(article['publish_date'])}</div>
                <div class='article-content'>{article['content']}</div>
                <br>
                <a href='/Journal' class='button-link'>Voltar</a>
                <div class="related-section">
                    <img src="{article['game_image']}" alt="Game Image">
                    <div>
                        <div>Jogo / Desenvolvedora</div>
                        <a href='?game={article["game"]}' class='link'>{article["game"]}</a>
                        <div class='company-title'>{article['company']}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("Notícia não encontrada.")
elif game_name:
    st.header(f"Notícias relacionadas a {game_name}")
    related_articles = [item for item in filtered_articles if item["game"] == game_name]
    for article in related_articles:
        col1, col2 = st.columns([6,9])
        with col1:
            if "image" in article:
                st.image(article["image"], width=240)
        with col2:
            st.markdown(f"### <a href='?article_id={article['id']}' class='link'>{article['title']}</a>", unsafe_allow_html=True)
            st.write(article.get("excerpt", "Descrição não disponível."))
            st.write(f"Publicado em {format_date(article['publish_date'])}")

        st.markdown("---")
else:
    st.header("Notícias Recentes")
    for article in filtered_articles:
        col1, col2 = st.columns([6, 9])
        with col1:
            if "image" in article:
                st.image(article["image"], width=240)
        with col2:
            st.markdown(f"### <a href='?article_id={article['id']}' class='link'>{article['title']}</a>", unsafe_allow_html=True)
            st.write(f"Publicado em {format_date(article['publish_date'])}")
            st.write(article.get("excerpt", "Descrição não disponível."))
        st.markdown("---")