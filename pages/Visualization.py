# visualization.py
import matplotlib.pyplot as plt
import plotly.express as px

def plot_avg_game_ratings_matplotlib(reviews, jogos):
    if not reviews.empty:
        avg_ratings = reviews.groupby('jogo_id')['nota'].mean()
        avg_ratings = avg_ratings.to_frame().join(jogos.set_index('id')['title']).rename(columns={'nota': 'avg_rating', 'title': 'game_title'})
        avg_ratings = avg_ratings.sort_values('avg_rating', ascending=False)

        plt.figure(figsize=(10, 6))
        plt.bar(avg_ratings['game_title'], avg_ratings['avg_rating'], color='blue')
        plt.xlabel('Jogo')
        plt.ylabel('Nota Média')
        plt.title('Média de Notas por Jogo')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

import plotly.graph_objects as go
import pandas as pd

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
        return None  # Caso não haja reviews, retorna None

