import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.memory import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_retrieval_chain

load_dotenv()

ai_prompt = """
Você é o Mario, o assistente virtual do MyGameHub. 
        
O seu papel é fornecer assistência informativa e amigável aos usuários com dúvidas sobre jogos e recomendações.
        
Você deve possuir um conhecimento amplo sobre o mundo dos jogos da Steam para fornecer melhores recomendações e respostas aos usuários.
        
Pergunta do usuário: {input}

Você deve possuir memória e compreensão de todas as perguntas e respostas anteriores para fornecer respostas coerentes e úteis: {messages}

Responda à pergunta para o usuário de forma agradável, sutil e precisa com base no seguinte contexto: {context}
"""

@st.cache_resource
def load_data():
    """Carregando os dados e criando o vectorstore."""
    df = pd.read_csv("src/data/processed_data.csv")
    texts = df.apply(lambda x: x['title'] + " - " + x['game_description'], axis=1).tolist()
    vectorstore = FAISS.from_texts(texts, embedding=OpenAIEmbeddings())
    return vectorstore.as_retriever()

class Mario:
    """
    Classe do assistente virtual Mario do MyGameHub.
    
    Atributos:
        model (ChatOpenAI): O modelo de linguagem usado para gerar respostas.
        chain (object): A cadeia de recuperação de respostas.  
    """
    def __init__(self):
        """Inicializando a instância do Mario, configurando o estado da sessão, o modelo e a cadeia de recuperação."""
        self._initialize_session_state()
        self.model = ChatOpenAI(temperature=0.2, model="gpt-4o", api_key=KEY)
        self.chain = self._create_chain()

    def _initialize_session_state(self):
        """Inicializando o estado da sessão para armazenar o histórico da conversa."""
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = ChatMessageHistory()

    def _create_chain(self):
        """Criando a cadeia de processamento para o agente."""
        prompt = ChatPromptTemplate.from_template(ai_prompt)
        chain = prompt | self.model | StrOutputParser()
        retrieval_chain = create_retrieval_chain(load_data(), chain)
        return retrieval_chain

    def get_response(self, user_input):
        """Obtendo resposta do chatbot."""
        st.session_state.chat_history.add_user_message(user_input)
        response = self.chain.invoke({"input": user_input, "messages": st.session_state.chat_history.messages})
        st.session_state.chat_history.add_ai_message(response["answer"])  
        return response["answer"]

    def display_chat_history(self):
        """Exibindo o histórico da conversa para o usuário."""
        download_str = []
        with st.expander("Histórico da Conversa", expanded=True):
            for message in reversed(st.session_state.chat_history.messages):
                if isinstance(message, HumanMessage):
                    st.info(f"**Você:** {message.content}", icon="🧐")
                    download_str.append(f"Você: {message.content}")
                elif isinstance(message, AIMessage):
                    st.success(f"**Mario:** {message.content}", icon="🤖")
                    download_str.append(f"Mario: {message.content}")

            download_str = '\n'.join(download_str)
            if download_str:
                st.download_button('Download Conversa', download_str, file_name="conversation_history.txt")

mario = Mario()

st.title("🤖 Mario - MyGameHub")
st.markdown("#### Olá! Bem-vindo ao Mario, o assistente virtual do MyGameHub! Como posso ajudar você hoje?")
st.markdown("---")

user_input = st.text_input("Faça sua pergunta:", placeholder="Digite sua pergunta sobre jogos aqui...")
if st.button("Obter resposta"):
    if user_input:
        answer = mario.get_response(user_input)
        st.markdown("#### Resposta:")
        st.markdown(f"> {answer}")
    else:
        st.error("Por favor, digite uma pergunta.")

st.markdown("### Histórico da Conversa")
mario.display_chat_history()

st.sidebar.markdown("# Mario 🤖")
st.sidebar.header("Como usar o chatbot")
st.sidebar.markdown("1. Digite sua pergunta sobre jogos.")
st.sidebar.markdown("2. Clique em 'Obter resposta'.")
st.sidebar.markdown("3. Caso queira, pode baixar o histórico de conversa em TXT.")

st.sidebar.markdown("---")
st.sidebar.header("Sobre o Mario")
st.sidebar.markdown("Mario é seu assistente pessoal para recomendações e informações sobre jogos. Aproveite!")