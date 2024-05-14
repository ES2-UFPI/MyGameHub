import streamlit as st
import pandas as pd
import pickle
import torch
import os
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel

df = pd.read_csv("src/data/processed_data.csv")

embeddings_file = 'src/embeddings/embeddings.pkl'

def generate_embeddings(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
    return embeddings.numpy()

if os.path.exists(embeddings_file):
    with open(embeddings_file, 'rb') as f:
        embeddings_list = pickle.load(f)
else:
    st.error("Arquivo de embeddings não encontrado.")

def get_game_description(title, game_data):
    filtered_data = game_data[game_data['title'].str.lower() == title.lower()]
    if not filtered_data.empty:
        return filtered_data['game_description'].iloc[0]
    else:
        return None

def get_similar_games(query_title, embeddings_list, game_data, top_n=5):
    titles_list = game_data['title'].str.lower().tolist()
    query_title = query_title.lower()  
    query_description = get_game_description(query_title, game_data)
    
    if query_description is None:
        return []

    query_embedding = generate_embeddings(query_description)
    similarities = cosine_similarity([query_embedding], embeddings_list)

    similar_indices = similarities.argsort()[0][-top_n:][::-1]

    similar_games_info = []
    for index in similar_indices:
        if titles_list[index] != query_title:
            game_info = game_data.iloc[index].to_dict()
            similar_games_info.append(game_info)
    
    return similar_games_info

st.title("Recomendações de Jogos")

game_name = st.text_input("Digite o nome de um jogo para obter recomendações:")

if st.button("Buscar Recomendações"):
    if game_name:
        similar_games_info = get_similar_games(game_name, embeddings_list, df)
        if similar_games_info:
            for game_info in similar_games_info:
                st.subheader(game_info['title'])
                st.write("Descrição:", game_info['game_description'])
                st.write("Preço Original:", game_info['original_price'])
                st.write("Data de Lançamento:", game_info['release_date'])
                st.write("Desenvolvedor:", game_info['developer'])
                st.write("Publicador:", game_info['publisher'])
                st.write("Feedback Geral:", game_info['all_reviews_summary'])
                st.write("Recursos do Jogo:", game_info['game_features'])
                st.write("Requisitos Mínimos:", game_info['minimum_requirements'])
                st.write("Link:", game_info['link'])
                st.write("\n")
        else:
            st.write("Não foram encontradas recomendações para este jogo.")
    else:
        st.error("Por favor, digite o nome de um jogo.")