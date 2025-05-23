import json
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
# index_name = os.getenv("PINECONE_INDEX_NAME")
index_name = "my-index"

# Initialize OpenAI
openai_client = OpenAI(api_key=openai_api_key)

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# Optional: set model name (adjust depending on embedding model used)
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4"

def get_embedding(text):
    """Create embedding vector for user query."""
    res = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return res.data[0].embedding

def query_vector_db(query, top_k=1):
    """Search Pinecone for top-k most relevant context chunks."""
    query_embedding = get_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    for match in results["matches"]:
      print(match.metadata) 
    # import pdb; pdb.set_trace()  
    return [match["metadata"]["text"] for match in results["matches"]]

def build_final_prompt(user_input, context_chunk):
    file_path1 = "/Users/jeevan.kumar/Documents/Hackathon_2025/Instructions/instruct.txt"
    with open(file_path1, "r", encoding="utf-8") as f:
        text = f.read()
        text = text.replace('\n', '')

    """Create final prompt to send to GPT-4 with context + user request."""
    context_text = "\n\n".join(context_chunk)
    instruct = text
    
    return f"""You are an expert Python API automation engineer.

                Using the following context about the endpoint

                Use the instructions to structure the test cases according to our framework standards.

                Instructions :
                {instruct}

                Context:
                {context_text}

                User Request:
                {user_input}


                Generate 10 test cases(5 positive, 2 negative and 3 edge case) in Python. Generate a test file and a helper file
                """

def generate_test_code(user_input,test_file_name):
    """Orchestrates the entire flow from query to final response."""
    context_chunk = query_vector_db(user_input)
    final_prompt = build_final_prompt(user_input, context_chunk)

    print("⏳ Sending to OpenAI...")
    response = openai_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful attentive expert SDET assistant who writes automated test cases."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.3
    )
    print("\n Generated Test Cases:\n")
    print(response.choices[0].message.content)
    output_dir = "/Users/jeevan.kumar/Documents/Hackathon_2025/GeneratedTests"
    os.makedirs(output_dir, exist_ok=True)  # creates folder if not present
    output_file = os.path.join(output_dir, "generated_"+test_file_name+".py")
    with open(output_file, "w", encoding="utf-8") as f:
          f.write(response.choices[0].message.content)
    
    

# Example usage
if __name__ == "__main__":
    # user_question = input("/csap/v1/allowed_indicators/,indicators")
    user_question = input("Enter your end point :")
    test_file_name = input("Enter the test file name :")

    generate_test_code(user_question,test_file_name)
