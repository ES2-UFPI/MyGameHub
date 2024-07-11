import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.memory import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_retrieval_chain

@st.cache_resource
def load_data():
    df = pd.read_csv("src/data/processed_data.csv")
    texts = df.apply(lambda x: x['title'] + " - " + x['game_description'], axis=1).tolist()
    vectorstore = FAISS.from_texts(texts, embedding=OpenAIEmbeddings())
    return vectorstore.as_retriever()

load_dotenv()
retriever = load_data()

template = """Você é o Game Advisor, o assistente virtual do MyGameHub. 

O seu papel é fornecer assistência informativa e amigável aos usuários com dúvidas sobre jogos e recomendações.

Você deve possuir um conhecimento amplo sobre o mundo dos jogos da Steam para fornecer melhores recomendações e respostas aos usuários.

Pergunta do usuário: 

{input}

Você deve possuir memória e compreensão de todas as perguntas e respostas anteriores para fornecer respostas coerentes e úteis:

{messages}

Responda à pergunta para o usuário de forma agradável, sutil e precisa com base no seguinte contexto:

{context}

"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(temperature=0.2, model="gpt-4o")

chain = (
    prompt
    | model
    | StrOutputParser()
)

retrieval_chain = create_retrieval_chain(retriever, chain)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ChatMessageHistory()

st.title("Game Advisor")
st.markdown("#### Olá! Bem-vindo ao assistente virtual do MyGameHub! Como posso ajudar você hoje?")
input = st.text_input("Faça sua pergunta:")

if st.button("Obter resposta"):
    if input:
        st.session_state.chat_history.add_user_message(input)
        response = retrieval_chain.invoke({"input": input, "messages": st.session_state.chat_history.messages})
        st.session_state.chat_history.add_ai_message(response["answer"])  
        st.markdown("#### Resposta:")
        st.markdown(f"> {response['answer']}")
    else:
        st.error("Por favor, digite uma pergunta.")

download_str = []
with st.expander("Histórico da Conversa", expanded=True):
    for message in reversed(st.session_state.chat_history.messages):
        if isinstance(message, HumanMessage):
            st.info(f"**Você:** {message.content}", icon="🧐")
            download_str.append(f"Você: {message.content}")
        elif isinstance(message, AIMessage):
            st.success(f"**Game Advisor:** {message.content}", icon="🤖")
            download_str.append(f"Game Advisor: {message.content}")

    download_str = '\n'.join(download_str)
    if download_str:
        st.download_button('Download Conversa', download_str, file_name="conversation_history.txt")

st.sidebar.header("Como usar o chatbot")
st.sidebar.text("1. Digite sua pergunta sobre jogos.")
st.sidebar.text("2. Clique em 'Obter resposta.")
st.sidebar.text("3. Caso queira, pode baixar o histórico de conversa em TXT.")