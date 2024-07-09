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