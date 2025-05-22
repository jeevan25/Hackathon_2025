from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone  # or Qdrant/Weaviate etc
from langchain.embeddings import OpenAIEmbeddings
import pinecone

# Initialize Pinecone (replace with your cloud DB of choice)
pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENV")
index_name = "hackathon-codegen"

# Load files & split
docs = []
for file_path in ["context/payloads.json", "context/schemas.json", "context/guidelines.txt"]:
    loader = TextLoader(file_path)
    docs.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(docs)

# Embed and upload
embeddings = OpenAIEmbeddings()
vector_db = Pinecone.from_documents(docs, embeddings, index_name=index_name)



# from openai import OpenAI

# client = OpenAI(api_key="your-key")

# response = client.embeddings.create(
#     input=["create test for POST /login"],
#     model="text-embedding-3-small"
# )

# vector = response.data[0].embedding



# (Assuming Pinecone client is also initialized)
# pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="YOUR_PINECONE_ENVIRONMENT")
# index_name = "my-rag-index"
# index = pinecone.Index(index_name)






# documents = [
#     "This is the first document about topic A.",
#     "Another document discussing topic A in detail.",
#     "This document is about topic B.",
#     # ... more documents/text chunks
# ]

# for i, doc_text in enumerate(documents):
#     # 1. Get embedding from OpenAI
#     embedding = get_openai_embedding(doc_text) # Using the function defined above

#     # 2. Prepare data for Pinecone
#     vector_id = f"doc_{i}" # A unique ID for your vector
#     metadata = {"text": doc_text, "source": f"document_set_1"} # Example metadata

#     # 3. Upsert to Pinecone
#     # index.upsert(vectors=[(vector_id, embedding, metadata)]) # For older Pinecone client
#     # For the newer Pinecone client (check their latest docs for exact syntax):
#     # index.upsert(vectors=[{'id': vector_id, 'values': embedding, 'metadata': metadata}])

#     print(f"Upserted vector for document {i}")

# # Don't forget to handle API errors, rate limits, etc., in a production app.
