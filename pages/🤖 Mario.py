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
from src.utils.globals import KEY

@st.cache_resource
def load_data():
    df = pd.read_csv("src/data/processed_data.csv")
    texts = df.apply(lambda x: x['title'] + " - " + x['game_description'], axis=1).tolist()
    vectorstore = FAISS.from_texts(texts, embedding=OpenAIEmbeddings(api_key=KEY))
    return vectorstore.as_retriever()

class Mario:
    def __init__(self):
        self.prompt_template = self._create_prompt_template()
        self.model = self._initialize_model()
        self.chain = self._create_chain()
        self.retrieval_chain = self._create_retrieval_chain()
        self._initialize_session_state()

    def _create_prompt_template(self):
        template = """Você é o Mario, o assistente virtual do MyGameHub. 

        O seu papel é fornecer assistência informativa e amigável aos usuários com dúvidas sobre jogos e recomendações.

        Você deve possuir um conhecimento amplo sobre o mundo dos jogos da Steam para fornecer melhores recomendações e respostas aos usuários.

        Pergunta do usuário: 

        {input}

        Você deve possuir memória e compreensão de todas as perguntas e respostas anteriores para fornecer respostas coerentes e úteis:

        {messages}

        Responda à pergunta para o usuário de forma agradável, sutil e precisa com base no seguinte contexto:

        {context}
        """
        return ChatPromptTemplate.from_template(template)

    def _initialize_model(self):
        return ChatOpenAI(temperature=0.2, model="gpt-4o", api_key=KEY)

    def _create_chain(self):
        return (
            self.prompt_template
            | self.model
            | StrOutputParser()
        )

    def _create_retrieval_chain(self):
        return create_retrieval_chain(load_data(), self.chain)

    def _initialize_session_state(self):
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = ChatMessageHistory()

    def get_response(self, user_input):
        st.session_state.chat_history.add_user_message(user_input)
        response = self.retrieval_chain.invoke({"input": user_input, "messages": st.session_state.chat_history.messages})
        st.session_state.chat_history.add_ai_message(response["answer"])  
        return response["answer"]

    def display_chat_history(self):
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


advisor = Mario()

st.title("Mario")
st.markdown("#### Olá! Bem-vindo ao Mario, o assistente virtual do MyGameHub! Como posso ajudar você hoje?")
user_input = st.text_input("Faça sua pergunta:")

if st.button("Obter resposta"):
    if user_input:
        answer = advisor.get_response(user_input)
        st.markdown("#### Resposta:")
        st.markdown(f"> {answer}")
    else:
        st.error("Por favor, digite uma pergunta.")

advisor.display_chat_history()

st.sidebar.markdown("# Mario 🤖")
st.sidebar.header("Como usar o chatbot")
st.sidebar.text("1. Digite sua pergunta sobre jogos.")
st.sidebar.text("2. Clique em 'Obter resposta.")
st.sidebar.text("3. Caso queira, pode baixar o histórico de conversa em TXT.")