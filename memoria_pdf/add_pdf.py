import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings


pdf_path = r"EBOOK - INTRODUÇÃO A PYTHON (EDITORA IFRN).pdf"

loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
chunks = text_splitter.split_documents(
    documents=docs,
)

persist_directory = 'db'

embedding = OllamaEmbeddings(model="llama3:8b")
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory=persist_directory,
    collection_name='laptop_manual',
)
