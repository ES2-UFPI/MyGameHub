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
