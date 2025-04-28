from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
from langchain import hub
import os 

class service:
    def __init__(self, modelo: str):
        # Configuração do modelo
        # model = ChatOllama(model=modelo)
        os.environ['OPENAI_API_KEY'] = ''

        model = ChatOpenAI(model='gpt-3.5-turbo')

        # Conexão com o banco de dados PostgreSQL
        db = SQLDatabase.from_uri(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
        )

        # Criação do SQLDatabaseToolkit
        toolkit = SQLDatabaseToolkit(
            db=db,
            llm=model,
        )

        # Prompt inicial para o assistente
        system_message = hub.pull('hwchase17/react')
        self.prompt_template = """
            Você é um assistente de IA que ajuda os usuários a interagir com um banco de dados PostgreSQL. 
            Você pode responder perguntas sobre os dados, executar consultas SQL e fornecer informações úteis. 
            Sempre forneça respostas claras e concisas.
            Responda sempre e somente em português.
            Se você não souber a resposta, diga que não sabe.

            Pergunta do usuário:
            {question}
            """

        # prompt_template = PromptTemplate(
        #     input_variables=["question"],  # Variáveis obrigatórias
        #     template=system_message
        # )

        agent = create_react_agent( 
            llm=model,
            tools=toolkit.get_tools(),
            prompt=system_message,
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=toolkit.get_tools(),
            verbose=True,
        )


# ia_service = service(modelo="llama3:8b")  # ou outro modelo disponível

# output = ia_service.agent_executor.invoke({
#         'input': ia_service.prompt_template.format(question="Me liste os projetos, analise a descrição e veja qual é o projeto mais relevantes e rápidos de se fazer")
#     })
#     # result = response.json()
# print(output.get('output'))
# print(output.get('output'))