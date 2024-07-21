import streamlit as st
import login as login
import profile

from login import login_page

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    if st.session_state.page == 'login':
        show_home_page()
        login.login_page()
    elif st.session_state.page == 'profile':
        profile.profile_page()

def show_home_page():
    st.title("MyGameHub 🕹️")
    st.subheader("Seu Hub Definitivo para o Mundo dos Jogos")
    
    st.markdown("""
    ## Bem-vindo ao MyGameHub!
    No MyGameHub, você encontrará tudo o que precisa para se manter atualizado com o mundo dos jogos. Desde as últimas notícias e atualizações até recomendações personalizadas de jogos e análises detalhadas. Junte-se a nós e descubra uma comunidade de gamers apaixonados!
    
    ### Funcionalidades:
    - **Notícias e Atualizações 📰**: Fique por dentro das últimas novidades do mundo dos games.
    - **Recomendações Personalizadas 🤖**: Receba sugestões de jogos pelo nosso Agente Virtual baseadas nas suas preferências.
    - **Análises e Reviews 🧠**: Leia e escreva análises sobre seus jogos favoritos.
    - **Busca 🔎**: Pesquise informações sobre seus jogos favoritos.

    **E muito mais!**
                    
    ### Entre ou Cadastre-se 👤:
    Faça login ou crie uma conta para aproveitar todas as funcionalidades do MyGameHub.
    """)

if __name__ == "__main__":
    main()
