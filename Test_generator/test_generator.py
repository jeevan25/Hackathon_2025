import os
import openai
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Keys from env
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
index_name = os.getenv("PINECONE_INDEX")

# Initialize OpenAI
openai_client = OpenAI(api_key=openai_api_key)

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# Optional: set model name (adjust depending on embedding model used)
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "gpt-4"

def get_embedding(text):
    """Create embedding vector for user query."""
    res = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[text]
    )
    return res.data[0].embedding

def query_vector_db(query, top_k=5):
    """Search Pinecone for top-k most relevant context chunks."""
    query_embedding = get_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]

def build_final_prompt(user_input, context_chunks):
    """Create final prompt to send to GPT-4 with context + user request."""
    context_text = "\n\n".join(context_chunks)
    return f"""You are an expert Python API automation engineer.

Using the following context about the endpoint, generate 5 test cases in Python using the requests library.

Context:
{context_text}

User Request:
{user_input}

Output test code only. Use pytest format if appropriate.
"""

def generate_test_code(user_input):
    """Orchestrates the entire flow from query to final response."""
    context_chunks = query_vector_db(user_input)
    final_prompt = build_final_prompt(user_input, context_chunks)

    print("⏳ Sending to OpenAI...")
    response = openai_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant who writes automated test cases."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.3
    )

    print("\n✅ Generated Test Cases:\n")
    print(response.choices[0].message.content)

# Example usage
if __name__ == "__main__":
    user_question = input("Ask for test generation: ")
    generate_test_code(user_question)
