import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from transformers import pipeline

# Carregamento de CSS personalizado
def load_custom_css():
    with open('src/data/styleReviews.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Classe para carregar dados
class DataLoader:
    @staticmethod
    def load_games():
        jogos = pd.read_csv("src/data/processed_data.csv")  # Ajuste o caminho do arquivo se necessário
        jogos['id'] = range(1, len(jogos) + 1)
        return jogos

    @staticmethod
    def load_reviews():
        try:
            return pd.read_csv('src/data/reviews.csv')
        except FileNotFoundError:
            return pd.DataFrame(columns=["jogo_id", "usuario", "nota", "comentario", "favorito", "sentimento"])

    @staticmethod
    def save_reviews(reviews):
        reviews.to_csv('src/data/reviews.csv', index=False)

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
        novo_review_df = pd.DataFrame([novo_review])
        self.reviews = pd.concat([self.reviews, novo_review_df], ignore_index=True)
        DataLoader.save_reviews(self.reviews)
        return self.reviews

    def analyze_sentiment(self, comentario):
        return self.sentiment_analyzer.analyze_sentiment(comentario)

    def get_reviews_for_game(self, jogo_id):
        return self.reviews[self.reviews['jogo_id'] == jogo_id]

    def plot_avg_ratings(self):
        return DataVisualizer.plot_avg_game_ratings_plotly(self.reviews, self.jogos)

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
            "sentimento": sentimento
        }
        facade.add_review(novo_review)
        st.success("Avaliação enviada com sucesso!")

    if st.checkbox("Ver avaliações existentes"):
        avaliacoes_filtradas = facade.get_reviews_for_game(jogo_id)
        if avaliacoes_filtradas.empty:
            st.write("Ainda não há avaliações para este jogo.")
        else:
            st.write(avaliacoes_filtradas)
    
    if st.button("Mostrar Gráfico com Plotly"):
        fig = facade.plot_avg_ratings()
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
