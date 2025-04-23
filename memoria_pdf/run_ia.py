from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


model = OllamaLLM(model="llama3:8b", temperature=0.7, max_tokens=1000)


persist_directory = 'db'
embedding = OllamaEmbeddings(model="llama3:8b")

vector_store = Chroma(
    embedding_function=embedding,
    persist_directory=persist_directory,
    collection_name='laptop_manual',
)

retriever = vector_store.as_retriever()

system_prompt = '''
Use o contexto para responder as perguntas.
Contexto: {context}
'''

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        ('human', '{input}'),
    ]
)

question_answer_chain = create_stuff_documents_chain(
    llm=model,
    prompt=prompt,
)

chain = create_retrieval_chain(
    retriever=retriever,
    combine_docs_chain=question_answer_chain,
)

query = 'O que é python ?'

response = chain.invoke(
    {'input': query},
)

print(response['answer'])
print(response)