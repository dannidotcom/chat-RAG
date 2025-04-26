import psycopg
import os
from psycopg import Cursor

class RAGSYTEM:
    
    def __init__(self, openai_client: str, db_connection_str: str, data_path: str):
        self.openai_client = openai_client
        self.db_connection_str = db_connection_str
        self.data_path = data_path

        with psycopg.connect(db_connection_str) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS embeddings (
                            id serial PRIMARY KEY,
                            document text,
                            embedding vector(1536)
                    );
                """)
                
                conn.commit()
    
    def compute_embedding(self, document: str) -> list[float]:
        embeddings = self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=document,
            encoding_format="float"
        ).data
        return embeddings[0].embedding
    
    def save_embedding(self, document: str, embedding: list[float], cursor: Cursor) -> None:
        cursor.execute("""
            INSERT INTO embeddings (document, embedding) VALUES (%s, %s)
        """, (document, embedding))
        
    def store_documents(self) -> None:
        
        with psycopg.connect(self.db_connection_str) as conn:
            with conn.cursor() as cur:
                
                files_path = os.listdir(self.data_path)
                documents_path = [file for file in files_path if file.endswith('.txt')]
                
                
                for document_path in documents_path:
                    
                    print("path",os.path.join(self.data_path, document_path))
                    
                    with open(os.path.join(self.data_path, document_path), "r", encoding='utf-8', errors="replace") as file:
                        document = file.read()
                    
                        embedding = self.compute_embedding(document)
                        
                        self.save_embedding(document=document, embedding=embedding, cursor=cur)
                    
                print("All documents have been stored")
                
    
    def semantic_search(self, user_query: str) -> str:
        
        user_query_embedding = self.compute_embedding(user_query)
        
        with psycopg.connect(self.db_connection_str) as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT id, document, embedding
                    FROM embeddings
                    ORDER BY embedding <=> %s::vector ASC
                    LIMIT 1;
                """
                cur.execute(query, [user_query_embedding])
                records = cur.fetchall()
                
                result = " ".join([record[1] for record in records])
                
                return result
            
    def generate_response(self, context: str, user_query: str):
                
        completion = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Tu es un assistant dans un accueil de l'université, tu vas te servir de la question de l'utilisateur : {user_query} , et repondre en langage naturel en te servant de ces informations : {context}"},
                {
                    "role": "user",
                    "content": context
                }
            ]
        )
        return completion.choices[0].message.content
                
    