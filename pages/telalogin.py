import streamlit as st

def main():
    st.set_page_config(page_title="Login", layout="wide")
    
    # CSS para alterar a cor do botão
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;  /* Cor verde */
        color: white;               /* Cor do texto */
        border: none;
        border-radius: 4px;         /* Bordas arredondadas */
        padding: 10px 24px;         /* Padding para o botão */
        font-size: 16px;            /* Tamanho da fonte */
        cursor: pointer;            /* Cursor como ponteiro */
    }
    div.stButton > button:hover {
        background-color: #45a049;  /* Cor um pouco mais escura para o hover */
    }
    </style>
    """, unsafe_allow_html=True)

    # Usando colunas para centralizar a imagem
    col1, col2, col3 = st.columns([1,2,1])
    with col2:  # Usar a coluna central para a imagem
        st.image(r"D:\cc\6p\eng 2\MyGameHub\src\images\341dd759-ea43-4c0d-b395-610fd28c3c2b.webp", width=820, output_format='auto')

    # Espaço antes dos campos de entrada
    st.write("")
    
    # Centralizando os elementos restantes
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.header("Bem-vindo ao MyGameHub!")
        
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if username == "seu_usuario" and password == "sua_senha":
                st.success("Login efetuado com sucesso!")
            else:
                st.error("Usuário ou senha incorretos!")
        
        st.markdown("---")
        st.markdown("Esqueceu a senha?")
        st.markdown("Criar nova conta")

if __name__ == "__main__":
    main()
