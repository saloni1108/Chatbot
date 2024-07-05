import os
import google.generativeai as genai
import streamlit as st
from retrieval import get_pdf_text, get_chunks, get_vectorstore
from generation import model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils import mongo_client
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv('GEMINI_API'))

gemini_model = genai.GenerativeModel('gemini-1.0-pro-latest')

def prompt_query(user_query, results):
    prompt = (
        f"User Query: {user_query}\n"
        f"Results: {results}\n\n"
        "If the user query matches and is related to the results obtained, "
        "summarize the content in the results and give the details of the user query. "
        "If the query does not match, return 'Can't answer this question.'"
        "mention it in chatbot way relevant answer to querry if the query matches"
        "only mention information in the output"
    )
    response = gemini_model.generate_content(prompt)
    return response.text

def generate_query_vector(query):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key= os.getenv('GEMINI_API'))
    response = embeddings.embed_documents([query])
    query_vector = response[0]
    return query_vector

def search_in_mongodb(query_vector):
    db = mongo_client[os.getenv('MONGO_DB')]
    collection = db[os.getenv('MONGO_COLLECTION')]

    pipeline = [
        {
            "$vectorSearch": {
                "queryVector": query_vector,
                "path": "vector",
                "numCandidates": 100,
                "limit": 4,
                "index": "Vector_search"
            }
        },
        {
            "$project": {
                "chunk": 1,
                "_id": 0
            }
        }
    ]

    try:
        results = collection.aggregate(pipeline)
        closest_docs = list(results)
        return closest_docs
    except Exception as e:
        print("Error executing pipeline:", e)
        return []

def chatbot():
    st.title("Chatbot")
    
    user_query = st.text_input("Enter your query:")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if st.button("Upload"):
        if uploaded_files:
            st.write("Uploading files")
            pdf_content = get_pdf_text(uploaded_files)
            chunks=get_chunks(pdf_content)
            get_vectorstore(chunks)
        else:
            st.warning("Upload pdf files....")
    
    if st.button("Submit"):
        if user_query:
            st.write("Generating response...")
            query_vector = generate_query_vector(user_query)
            results = search_in_mongodb(query_vector)
            response = prompt_query(user_query, results)
            if response:
                st.empty()
                st.write(response)
            else:
                st.empty()
                st.write("Cant generate response") 
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    chatbot()