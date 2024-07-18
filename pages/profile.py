import streamlit as st
from utils import session, users, profiles
from pages.Reviews import load_reviews, load_data, plot_avg_game_ratings_plotly

def profile_page():
    if 'username' not in st.session_state or not st.session_state.get('logged_in', False):
        st.error('Por favor, faça login primeiro.')
        return

    username = st.session_state.username
    st.title('Perfil')

    user = session.query(users).filter(users.c.username == username).first()
    profile = session.query(profiles).filter(profiles.c.user_id == user.id).first()

    if profile is None:
        profile = profiles.insert().values(user_id=user.id)
        session.execute(profile)
        session.commit()
        profile = session.query(profiles).filter(profiles.c.user_id == user.id).first()

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

if __name__ == "__main__":
    profile_page()
