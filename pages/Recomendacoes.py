import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

class RecommendationSystem:
    def __init__(self):
        self.llm = ChatOpenAI(
            model='gpt-4o',
            temperature=0.5
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um agente de inteligência artificial especializado em recomendar jogos da plataforma Steam. Quando o usuário digitar o nome de um jogo, você deve procurar por jogos bastante semelhantes e recomendá-los, fornecendo todas as informações possíveis dos jogos, como descrição, desenvolvedor, gênero, preço, data de lançamento e link. Responda com base na faixa de preço e data de lançamento especificada pelo usuário. Cordialmente, agradeça pela interação ao final."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        self.search = TavilySearchResults()
        self.tools = [self.search]
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=self.tools
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools
        )

    def get_recommendations(self, user_input):
        response = self.agent_executor.invoke({
            "input": user_input
        })
        return response["output"]

agent = RecommendationSystem()

st.title("Recomendações de Jogos")

game_name = st.text_input("Digite o nome de um jogo para obter recomendações:")

price_range = st.slider("Selecione a faixa de preço", 0, 100, (0, 50))

release_date_range = st.slider("Selecione a faixa de data de lançamento", 2000, 2024, (2010, 2024))

if st.button("Buscar Recomendações"):
    if game_name:
        with st.spinner('Buscando recomendações...'):

            user_input = f"Nome do jogo: {game_name}. Faixa de preço: entre {price_range[0]} e {price_range[1]} dólares. Data de lançamento: entre {release_date_range[0]} e {release_date_range[1]}."
            response = agent.get_recommendations(user_input)
            st.write(response)
    else:
        st.error("Por favor, digite o nome de um jogo.")