import os
import json
import pinecone
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

'''
# # Initialize Pinecone
# pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

# # Create index if not exists
# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(index_name, dimension=1536)

# index = pinecone.Index(index_name) '''

# Create a Pinecone client instance
pc = pinecone.Pinecone(api_key=pinecone_api_key)

# Optional: create index if not already present
index_name = "my-index"
dimension = 1536  # For OpenAI embeddings

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud='aws',region='us-east-1')
    )

# Connect to the index
index = pc.Index(index_name)

# Helper: read and chunk content from file
def read_context_files(folder_path):
    context_chunks = []
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            for chunk in chunks:
                context_chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": chunk,
                    "metadata": {"source": fname}
                })
    return context_chunks

# Embed & store in Pinecone
def embed_and_store(chunks):
    for chunk in chunks:
        res = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=[chunk["text"]]
        )
        vector = res.data[0].embedding
        index.upsert([
            (chunk["id"], vector, chunk["metadata"])
        ])
    print(f"✅ {len(chunks)} chunks embedded & stored.")

if __name__ == "__main__":
    all_chunks = read_context_files("/Users/jeevan.kumar/Documents/Hackathon_2025/Context")
    embed_and_store(all_chunks)
