import streamlit as st
import pandas as pd
from utils import session, users, profiles
from werkzeug.security import generate_password_hash, check_password_hash

def plot_avg_game_ratings_plotly(reviews, jogos):
    if not reviews.empty:
        # Ajusta as notas para a escala de 0 a 5
        reviews['nota'] = reviews['nota'] / 2
        
        # Calcula a média de notas por jogo
        avg_ratings = reviews.groupby('jogo_id')['nota'].mean()
        avg_ratings = avg_ratings.to_frame().join(jogos.set_index('id')['title']).rename(columns={'nota': 'avg_rating', 'title': 'game_title'})
        avg_ratings = avg_ratings.sort_values('avg_rating', ascending=False)

        # Criação do gráfico
        fig = st.go.Figure()

        for index, row in avg_ratings.iterrows():
            fig.add_trace(st.go.Bar(
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

def load_data():
    jogos = pd.read_csv("src/data/processed_data.csv")  # Ajuste o caminho do arquivo se necessário
    jogos['id'] = range(1, len(jogos) + 1)
    return jogos

# Função para carregar avaliações (simulação de dados persistidos)
def load_reviews():
    try:
        return pd.read_csv('src/data/reviews.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=["jogo_id", "usuario", "nota", "comentario", "favorito", "sentimento"])

def delete_account(user_id):
    # Deletar perfil
    session.query(profiles).filter(profiles.c.user_id == user_id).delete()
    # Deletar usuário
    session.query(users).filter(users.c.id == user_id).delete()
    session.commit()

def profile_page():
    if 'username' not in st.session_state or not st.session_state.get('logged_in', False):
        st.error('Por favor, faça login primeiro.')
        return

    username = st.session_state.username
    st.title('Perfil')
    st.sidebar.markdown("# Profile 👤")

    user = session.query(users).filter(users.c.username == username).first()
    profile = session.query(profiles).filter(profiles.c.user_id == user.id).first()

    if profile is None:
        profile = profiles.insert().values(user_id=user.id)
        session.execute(profile)
        session.commit()
        profile = session.query(profiles).filter(profiles.c.user_id == user.id).first()

    st.sidebar.title("Minha Conta")
    settings_mode = st.sidebar.radio("Escolha uma opção:", ["Perfil", "Configurações da Conta"])

    if settings_mode == "Perfil":
        edit_mode = st.session_state.get('edit_mode', False)

        if edit_mode:
            with st.form("profile_info"):
                full_name = st.text_input("Nome Completo", value=profile.full_name if profile.full_name else "")
                bio = st.text_area("Bio", value=profile.bio if profile.bio else "")

                save_changes = st.form_submit_button("Salvar Alterações")
                if save_changes:
                    session.query(profiles).filter(profiles.c.user_id == user.id).update({
                        'full_name': full_name,
                        'bio': bio
                    })
                    session.commit()
                    st.session_state.edit_mode = False  # Turn off edit mode after saving
                    st.success("Perfil atualizado com sucesso!")

                st.form_submit_button("Cancelar", on_click=lambda: st.session_state.__setitem__('edit_mode', False))
        else:
            st.write(f"**Nome Completo:** {profile.full_name if profile.full_name else 'Não definido'}")
            st.write(f"**Bio:** {profile.bio if profile.bio else 'Não definida'}")
            st.button("Editar", on_click=lambda: st.session_state.__setitem__('edit_mode', True))

        st.write("---")
        st.write("**Avaliações**")

        reviews = load_reviews()
        user_reviews = reviews[reviews['usuario'] == username]

        if not user_reviews.empty:
            jogos = load_data()
            user_reviews = user_reviews.merge(jogos[['id', 'title']], left_on='jogo_id', right_on='id')

            for _, row in user_reviews.iterrows():
                st.write(f"**Jogo:** {row['title']}")
                st.write(f"**Nota:** {row['nota']}")
                st.write(f"**Comentário:** {row['comentario']}")
                st.write(f"**Favorito:** {'Sim' if row['favorito'] else 'Não'}")
                st.write("---")

            if st.button("Mostrar Gráfico de Avaliações"):
                fig = plot_avg_game_ratings_plotly(user_reviews, jogos)
                if fig:
                    st.plotly_chart(fig)
        else:
            st.write("Você ainda não fez nenhuma avaliação.")

    else:
        st.header("Configurações de Conta")

        with st.form("account_settings"):
            new_password = st.text_input("Nova Senha", type="password")
            confirm_password = st.text_input("Confirmar Nova Senha", type="password")

            save_changes = st.form_submit_button("Salvar Alterações")
            if save_changes:
                if new_password and new_password != confirm_password:
                    st.error("As senhas não coincidem.")
                else:
                    if new_password:
                        account_data = {'password': generate_password_hash(new_password)}
                        session.query(users).filter(users.c.id == user.id).update(account_data)
                        session.commit()
                        st.success("Configurações de conta atualizadas com sucesso!")

        st.write("---")
        st.write("### Deletar Conta")
        if st.button("Deletar Conta"):
            confirm_delete = st.checkbox("Confirmar Deleção de Conta")
            if confirm_delete:
                delete_account(user.id)
                st.session_state.clear()
                st.success("Conta deletada com sucesso. Por favor, feche o aplicativo.")

if __name__ == "__main__":
    profile_page()