import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_custom_css():
    with open('src/data/styleReviews.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def plot_avg_game_ratings_plotly(reviews, jogos):
    if not reviews.empty:
        # Ajusta as notas para a escala de 0 a 5
        reviews['nota'] = reviews['nota'] / 2
        
        # Calcula a média de notas por jogo
        avg_ratings = reviews.groupby('jogo_id')['nota'].mean()
        avg_ratings = avg_ratings.to_frame().join(jogos.set_index('id')['title']).rename(columns={'nota': 'avg_rating', 'title': 'game_title'})
        avg_ratings = avg_ratings.sort_values('avg_rating', ascending=False)

        # Criação do gráfico
        fig = go.Figure()

        for index, row in avg_ratings.iterrows():
            fig.add_trace(go.Bar(
                x=[row['game_title']], 
                y=[row['avg_rating']],
                text=[f"{'★' * int(round(row['avg_rating']))} ({row['avg_rating']:.1f})"],  # Mostra estrelas e a nota
                textposition='auto',
            ))

        # Personalizações adicionais
        fig.update_layout(
            title='Média de Notas por Jogo (em estrelas)',
            xaxis_title='Jogos',
            yaxis_title='Nota Média',
            yaxis=dict(range=[0,5]),  # Define o limite do eixo y para 5
            plot_bgcolor='rgba(0,0,0,0)'
        )

        return fig
    else:
        return None

# Função para carregar os dados dos jogos
def load_data():
    jogos = pd.read_csv("src/data/processed_data.csv")  # Ajuste o caminho do arquivo se necessário
    jogos['id'] = range(1, len(jogos) + 1)
    return jogos

# Função para carregar avaliações (simulação de dados persistidos)
def load_reviews():
    try:
        return pd.read_csv('src/data/reviews.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=["jogo_id", "usuario", "nota", "comentario", "favorito"])

# Função para salvar avaliações (persistência de dados)
def save_reviews(reviews):
    reviews.to_csv('src/data/reviews.csv', index=False)

def add_review(reviews, novo_review):
    novo_review_df = pd.DataFrame([novo_review])
    reviews = pd.concat([reviews, novo_review_df], ignore_index=True)
    save_reviews(reviews)
    return reviews

def main():
    load_custom_css()
    st.title("Avaliação de Jogos")

    jogos = load_data()
    reviews = load_reviews()

    # Autenticação simples
    usuario = st.text_input("Nome do Usuário")
    if not usuario:
        st.warning("Por favor, insira um nome de usuário para continuar.")
        st.stop()

    # Mapeamento de jogos
    jogos_dict = jogos.set_index('id')['title'].to_dict()

    # Seleção do jogo
    jogo_id = st.selectbox(
        "Selecione um jogo para avaliar:",
        jogos['id'],
        format_func=lambda x: jogos_dict[x]
    )

    # Entrada para avaliação
    nota = st.slider("Nota", min_value=0, max_value=10, value=5)
    comentario = st.text_area("Comentário")
    favorito = st.checkbox("Favoritar este jogo")

    # Submissão de avaliação
    if st.button("Enviar Avaliação"):
        novo_review = {
            "jogo_id": jogo_id, 
            "usuario": usuario, 
            "nota": nota, 
            "comentario": comentario,
            "favorito": favorito
        }
        reviews = add_review(reviews, novo_review)
        st.success("Avaliação enviada com sucesso!")

    # Visualização das avaliações
    if st.checkbox("Ver avaliações existentes"):
        avaliacoes_filtradas = reviews[reviews['jogo_id'] == jogo_id]
        if avaliacoes_filtradas.empty:
            st.write("Ainda não há avaliações para este jogo.")
        else:
            st.write(avaliacoes_filtradas)

if __name__ == "__main__":
    main()