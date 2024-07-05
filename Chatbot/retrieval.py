import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
from dotenv import load_dotenv
from utils import mongo_client

load_dotenv()



def get_pdf_text(uploaded_files):
    content = ""
    for uploaded_file in uploaded_files:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            content += page.extract_text()
    return content

def get_chunks(content):
    split_text=RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200 )
    chunks=split_text.split_text(content)
    return chunks

def get_vectorstore(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key= os.getenv('GEMINI_API'))
    documents = []

    for chunk in chunks:
        print(chunk)
        response = embeddings.embed_documents([chunk])
        vector = response[0]
        documents.append({"chunk": chunk, "vector": vector})

    db = mongo_client[os.getenv('MONGO_DB')]
    collection = db[os.getenv('MONGO_COLLECTION')]

    result = collection.insert_many(documents)
    print(f"Inserted {len(result.inserted_ids)} documents into MongoDB Atlas")
    st.write("Pdfs uploaded to database")