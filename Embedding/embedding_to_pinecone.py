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
    context_items = [] 
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        # Ensure we are only trying to read files, not directories
        if os.path.isfile(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    full_text = f.read()
                    context_items.append(
                    {
                        "id": str(uuid.uuid4()), # A unique ID for this file's content
                        # "text": full_text,       # The entire text content of the file
                        "metadata": {"source": fname,"text":full_text} # Metadata indicating the source file
                    })
            except Exception as e:
                print(f"Error reading or processing file {fpath}: {e}")
        else:
            print(f"Skipping non-file item: {fpath}")
    return context_items

# # Embed & store in Pinecone
# def embed_and_store(chunks):
#     for chunk in chunks:
#         res = openai_client.embeddings.create(
#             model="text-embedding-3-small",
#             input=[chunk["text"]]
#         )
#         vector = res.data[0].embedding
#         index.upsert([
#             (chunk["id"], vector, chunk["metadata"])
#         ])
#     print(f"✅ {len(chunks)} chunks embedded & stored.")

# def embed_and_store_item(item_data, openai_client_instance, pinecone_index_instance):
#     """
#     Embeds the text from a single item and stores it in Pinecone.

#     Args:
#         item_data (dict): A dictionary with "id", "text", and "metadata".
#         openai_client_instance: The initialized OpenAI client.
#         pinecone_index_instance: The initialized Pinecone index object.
#     Returns:
#         bool: True if successful, False otherwise.
#     """
#     try:
#         text_to_embed = item_data["text"]
#         item_id = item_data["id"]
#         metadata = item_data.get("metadata", {}) # Default to empty dict if no metadata

#         # Generate embedding
#         res = openai_client_instance.embeddings.create(
#             model="text-embedding-3-small",
#             input=[text_to_embed] # API expects a list of strings
#         )
#         vector = res.data[0].embedding

#         # Upsert to Pinecone using the newer client format
#         pinecone_index_instance.upsert(
#             vectors=[
#                 {"id": item_id, "values": vector, "metadata": metadata}
#             ]
#         )
#         print(f"Successfully embedded and stored item ID '{item_id}' from source '{metadata.get('source', 'N/A')}'.")
#         return True

#     except KeyError as e:
#         print(f"Error: Item data is missing expected key: {e}. Item was: {item_data}")
#         return False
#     except Exception as e:
#         item_id_for_error = item_data.get("id", "unknown_id")
#         source_for_error = item_data.get("metadata", {}).get("source", "unknown_source")
#         print(f"An error occurred while processing item ID '{item_id_for_error}' (source: '{source_for_error}'): {e}")
#         return False



def embed_and_store_item(text, source_filename, openai_client_instance, pinecone_index_instance):
    """
    Embeds a single text chunk and stores it in Pinecone.

    Args:
        text (str): The text to embed.
        source_filename (str): The source filename for metadata.
        openai_client_instance: The OpenAI client instance.
        pinecone_index_instance: The Pinecone index instance.
    """
    try:
        item_id = str(uuid.uuid4())
        metadata =  {"source": source_filename, "text": text["text"]}

        # Create embedding
        res = openai_client_instance.embeddings.create(
            model="text-embedding-3-small",
            input = single_chunk["text"] # API expects a list of strings
        )

        vector = res.data[0].embedding

        # Upsert to Pinecone
        pinecone_index_instance.upsert(
            vectors=[
                {
                    "id": item_id,
                    "values": vector,
                    "metadata": metadata
                }
            ]
        )

        print(f" Successfully embedded and stored item from '{source_filename}' (ID: {item_id}).")
        return True

    except Exception as e:
        print(f"Error embedding/storing text from '{source_filename}': {e}")
        return False




if __name__ == "__main__":
    # chunk = read_context_files("/Users/jeevan.kumar/Documents/Hackathon_2025/Context/context1")
    # embed_and_store_item(chunk,openai_client,index)
    file_path = "Context/context1/get_intel_category.txt"
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        text = text.replace('\n', '')
    
    single_chunk = {
        "id": str(uuid.uuid4()),
        "text": text,
        "metadata": {"source": os.path.basename(file_path), "text": text}
    }

    embed_and_store_item(single_chunk,"get_intel_category.txt", openai_client, pc.Index(index_name))