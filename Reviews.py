import streamlit as st
import pandas as pd
from Visualization import plot_avg_game_ratings_matplotlib, plot_avg_game_ratings_plotly

# Função para carregar os dados dos jogos
def load_data():
    jogos = pd.read_csv("processed_data.csv")  # Ajuste o caminho do arquivo se necessário
    jogos['id'] = range(1, len(jogos) + 1)
    return jogos

# Função para carregar avaliações (simulação de dados persistidos)
def load_reviews():
    try:
        return pd.read_csv('reviews.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=["jogo_id", "usuario", "nota", "comentario", "favorito"])

# Função para salvar avaliações (persistência de dados)
def save_reviews(reviews):
    reviews.to_csv('reviews.csv', index=False)

def add_review(reviews, novo_review):
    novo_review_df = pd.DataFrame([novo_review])
    reviews = pd.concat([reviews, novo_review_df], ignore_index=True)
    save_reviews(reviews)
    return reviews

def main():
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

    # Geração de gráficos
    if st.button("Mostrar Gráfico com Matplotlib"):
        plt = plot_avg_game_ratings_matplotlib(reviews, jogos)
        st.pyplot(plt)
    
    if st.button("Mostrar Gráfico com Plotly"):
        fig = plot_avg_game_ratings_plotly(reviews, jogos)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()