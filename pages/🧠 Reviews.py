import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from transformers import pipeline
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData

# Configuração da Conexão com o BD
DATABASE_URL = "postgresql://mygamehub:XnDyt3Xa8O66bmE7Jbc3ly6zZ3f4eiGH@dpg-cqlnivdumphs7397s8k0-a.oregon-postgres.render.com/loginbd_6tj3"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Tabela reviews
reviews_table = Table('reviews', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('jogo_id', Integer),
                      Column('usuario', String),
                      Column('nota', Float),
                      Column('comentario', String),
                      Column('favorito', String),
                      Column('sentimento', String))

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Carregamento de CSS personalizado
def load_custom_css():
    with open('src/data/styleReviews.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Classe para carregar dados
class DataLoader:
    @st.cache_resource
    def load_games():
        jogos = pd.read_csv("src/data/processed_data.csv")  # Usando o arquivo enviado
        jogos['id'] = range(1, len(jogos) + 1)
        return jogos

    @staticmethod
    def load_reviews():
        return pd.read_sql(reviews_table.select(), con=engine)

# Classe para análise de sentimento
class SentimentAnalyzer:
    def __init__(self):
        self.pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    def analyze_sentiment(self, text):
        result = self.pipeline(text)[0]
        label = result['label']
        if label in ['1 star', '2 stars']:
            return 'Negative'
        elif label in ['5 stars', '4 stars']:
            return 'Positive'
        else:
            return 'Neutral'

# Classe para visualização de dados
class DataVisualizer:
    @staticmethod
    def plot_avg_game_ratings_plotly(reviews, jogos):
        if not reviews.empty:
            reviews['nota'] = reviews['nota'] / 2
            avg_ratings = reviews.groupby('jogo_id')['nota'].mean()
            avg_ratings = avg_ratings.to_frame().join(jogos.set_index('id')['title']).rename(columns={'nota': 'avg_rating', 'title': 'game_title'})
            avg_ratings = avg_ratings.sort_values('avg_rating', ascending=False)

            fig = go.Figure()

            for index, row in avg_ratings.iterrows():
                fig.add_trace(go.Bar(
                    x=[row['game_title']], 
                    y=[row['avg_rating']],
                    text=[f"{'★' * int(round(row['avg_rating']))} ({row['avg_rating']:.1f})"],
                    textposition='auto',
                ))

            fig.update_layout(
                title='Média de Notas por Jogo (em estrelas)',
                xaxis_title='Jogos',
                yaxis_title='Nota Média',
                yaxis=dict(range=[0,5]),
                plot_bgcolor='rgba(0,0,0,0)'
            )

            return fig
        else:
            return None

# Classe Facade
class GameReviewFacade:
    def __init__(self):
        self.jogos = DataLoader.load_games()
        self.reviews = DataLoader.load_reviews()
        self.sentiment_analyzer = SentimentAnalyzer()

    def add_review(self, novo_review):
        session.execute(reviews_table.insert().values(novo_review))
        session.commit()
        self.reviews = DataLoader.load_reviews()  # Recarregar as reviews do banco de dados
        return self.reviews

    def analyze_sentiment(self, comentario):
        return self.sentiment_analyzer.analyze_sentiment(comentario)

    def plot_avg_ratings(self):
        return DataVisualizer.plot_avg_game_ratings_plotly(self.reviews, self.jogos)

    def get_reviews_with_game_names(self):
        reviews = self.reviews.copy()
        reviews = reviews.merge(self.jogos[['id', 'title']], left_on='jogo_id', right_on='id', how='left')
        reviews = reviews.drop(columns=['id_y'])
        reviews = reviews.rename(columns={'id_x': 'id', 'title': 'jogo'})
        return reviews

def main():
    st.title("Avaliação de Jogos")
    st.sidebar.markdown("# Reviews 🧠")
    
    load_custom_css()
    facade = GameReviewFacade()

    usuario = st.text_input("Nome do Usuário")
    if not usuario:
        st.warning("Por favor, insira um nome de usuário para continuar.")
        st.stop()

    jogos_dict = facade.jogos.set_index('id')['title'].to_dict()

    jogo_id = st.selectbox(
        "Selecione um jogo para avaliar:",
        facade.jogos['id'],
        format_func=lambda x: jogos_dict[x]
    )

    nota = st.slider("Nota", min_value=0, max_value=10, value=5)
    comentario = st.text_area("Comentário")
    favorito = st.checkbox("Favoritar este jogo")

    if st.button("Analisar Sentimento"):
        sentimento = facade.analyze_sentiment(comentario)
        if sentimento == 'Positive':
            st.success("O sentimento do comentário é positivo!")
        elif sentimento == 'Negative':
            st.error("O sentimento do comentário é negativo.")
        else:
            st.info("O sentimento do comentário é neutro.")

    if st.button("Enviar Avaliação"):
        sentimento = facade.analyze_sentiment(comentario)
        novo_review = {
            "jogo_id": jogo_id, 
            "usuario": usuario, 
            "nota": nota, 
            "comentario": comentario,
            "favorito": favorito,
            "sentimento": sentimento  # Adiciona o sentimento ao review
        }
        facade.add_review(novo_review)
        st.success("Avaliação enviada com sucesso!")

    if st.button("Ver Reviews Existentes"):
        reviews_with_names = facade.get_reviews_with_game_names()
        st.write(reviews_with_names.head())

    if st.button("Mostrar Gráfico com Plotly"):
        fig = facade.plot_avg_ratings()
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()