# from langchain.vectorstores import Pinecone
# from langchain.embeddings import OpenAIEmbeddings
# import openai

# # Initialize Pinecone
# pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENV")
# index_name = "hackathon-codegen"

# # Setup vector DB & embedding model
# embeddings = OpenAIEmbeddings()
# vector_db = Pinecone(index_name=index_name, embedding_function=embeddings.embed_query)

# def generate_test_code(api_endpoint, prompt):
#     # Query context from vector DB
#     relevant_docs = vector_db.similarity_search(api_endpoint, k=5)  # get top 5 relevant docs

#     # Construct prompt for LLM
#     context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
#     full_prompt = f"Context:\n{context_text}\n\nGenerate python API automation test code for endpoint: {api_endpoint}\nDetails: {prompt}"

#     # Call OpenAI GPT API
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": full_prompt}],
#         temperature=0
#     )
#     return response.choices[0].message.content

# # Example usage
# code = generate_test_code("/v1/login", "Test login API with valid and invalid credentials")
# with open("test_login.py", "w") as f:
#     f.write(code)
