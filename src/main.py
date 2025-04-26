import os
from openai import OpenAI
from dotenv import load_dotenv
from rag_system import RAGSYTEM
import chainlit as cl


load_dotenv()


data_path = "./data"
# Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_KEY")
openai_client = OpenAI(api_key=openai_api_key)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST= os.getenv("HOST")
PORT = os.getenv("PORT")
db_connection_str = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={HOST} port={PORT}"

try:
    rag_system = RAGSYTEM(openai_client, db_connection_str, data_path=data_path)
except Exception as e:
    print(f"Failed to connect to database: {e}")
    print(f"Connection string used: {db_connection_str}")
    raise


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    
    user_query = message.content
    
    user_query_context = rag_system.semantic_search(user_query)
        
    final_response = rag_system.generate_response(user_query_context, user_query)
    
    # Send a response back to the user
    await cl.Message(
        content= final_response,
    ).send()
