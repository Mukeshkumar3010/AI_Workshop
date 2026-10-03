# from dotenv import load_dotenv
import yaml
import psycopg
# import os
from google import genai
from google.genai import types
# load_dotenv()
# user = os.getenv("user")
# password = os.getenv("password")
# host = os.getenv("host")
# port = os.getenv("port")
# database = os.getenv("database")
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL")
# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
with open("config.yaml", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

database_config = config["database"]
gemini_config = config["gemini"]

user = database_config["user"]
password = database_config["password"]
host = database_config["host"]
port = database_config["port"]
database = database_config["name"]
gemini_api_key = gemini_config["api_key"]
TEXT_MODEL = gemini_config["text_model"]
EMBEDDING_MODEL = gemini_config["embedding_model"]

conn = psycopg.connect(
    user=user,
    password=password,
    host=host,
    port=port,
    dbname=database
)
print("Connection established successfully.")

with conn.cursor() as cur:
    # Execute a query
    cur.execute("SELECT *FROM developers")
    rows = cur.fetchall()
    for row in rows:
        print(row)
conn.rollback()

with conn.cursor() as cur:
    # Insert data
    cur.execute("INSERT INTO developers(name, department, age) VALUES (%s, %s, %s)", ('John Doe', 'EEE', 24))
    conn.commit()
    print("Data inserted successfully")
    cur.execute("SELECT * FROM developers")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        
client = genai.Client(api_key=gemini_api_key)
print("Genmini is ready")
respose = client.models.generate_content(
    model=TEXT_MODEL,
    contents="Explain a database is in 1 simple sentence"
)
print(respose.text)

def create_embedding(text):
    result = client.models.embed_content(
        model = EMBEDDING_MODEL,
        contents = text,
        config = types.EmbedContentConfig(output_dimensionality=768)
    )
    return result.embeddings[0].values
    
e = create_embedding("PostgreSQL is a database.")
print(len(e)) # 768
print(e[:5])
sentences = ["I love dogs.",
             "I like puppies.",
             "The stock market fell today."]

embeddings = [create_embedding(sentence) for sentence in sentences]
print(len(embeddings)) # 3
print(len(embeddings[0])) # 768
