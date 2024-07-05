import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongo_url = os.getenv('MONGO_URL')

mongo_client = MongoClient(mongo_url)

def create_connection():
    client = MongoClient(mongo_url)
    return client

def close_connection(client):
    client.close()