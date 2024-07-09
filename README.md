# Chatbot

This project creates a chatbot that can read, process, and answer questions about a PDF document. It utilizes Google's Generative AI for embedding and text generation, MongoDB for storage, and FAISS for similarity search.

## Features
- Extracts text from PDF documents
- Splits text into manageable chunks
- Embeds text chunks using Google's Generative AI
- Stores embedded chunks in MongoDB
- Retrieves relevant document chunks based on user queries
- Generates responses to user queries using Google's Generative AI

## Prerequisites
- Python 3.8 or higher
- MongoDB instance (local or Atlas)
- Google Generative AI API key

## Project Structure

- pdf-chatbot/
    - main.py -------------- # Main script to preprocess PDF and store chunks in MongoDB
    - retrieval.py --------- # Functions for retrieving relevant document chunks
    - generation.py -------- # Functions for generating responses
    - utils.py ------------- # Utility functions for database connection
    - .env ----------------- # Environment variables (not included in version control)
 
## Code Overview
- main.py
    This is the main entry point of the Streamlit application. It loads and stores conversation data, generates query vectors, performs vector search, and handles user interaction.

- utils.py
    Contains utility functions for connecting to MongoDB Atlas and embedding documents using Google Generative AI.

- retrieval.py
    Defines functions for reading multiple PDF as an input creating the embeddings for the same.

- generation.py
    Includes functions for generating query vectors, performing vector search in MongoDB, and generating responses based on search results.
