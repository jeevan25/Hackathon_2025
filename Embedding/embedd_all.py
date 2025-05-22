# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Pinecone  # or Qdrant/Weaviate etc
# from langchain.embeddings import OpenAIEmbeddings
# import pinecone

# # Initialize Pinecone (replace with your cloud DB of choice)
# pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENV")
# index_name = "hackathon-codegen"

# # Load files & split
# docs = []
# for file_path in ["context/payloads.json", "context/schemas.json", "context/guidelines.txt"]:
#     loader = TextLoader(file_path)
#     docs.extend(loader.load())

# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# docs = splitter.split_documents(docs)

# # Embed and upload
# embeddings = OpenAIEmbeddings()
# vector_db = Pinecone.from_documents(docs, embeddings, index_name=index_name)
