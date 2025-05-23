import pinecone

# Initialize Pinecone (assumes you already initialized it earlier)
index = pinecone.Index("your-index-name")

# Chunk text describing the endpoint
chunk_text = """
Endpoint: /create-user
Method: POST
Authentication: Required

Schema:
{
  "username": "string",         # Required, non-empty
  "email": "string",            # Required, valid email format
  "role_id": "integer",         # Required, must be fetched from /get-roles endpoint
  "status": "string"            # Optional, allowed values: ["active", "inactive", "pending"]
}

Key Notes:
- "username" and "email" are mandatory fields.
- "role_id" depends on valid role IDs from the /get-roles endpoint.
- If "status" is omitted, defaults to "pending".

Dependencies:
- role_id: Requires calling /get-roles to retrieve valid role IDs.

Expected Response:
{
  "user_id": "integer",
  "message": "User created successfully."
}

Error Scenarios:
- Missing mandatory fields ("username", "email", or "role_id") should return 400 Bad Request.
- Invalid "role_id" (not in /get-roles response) returns 422 Unprocessable Entity.
- Invalid data types should return descriptive error messages.
"""

# Normally, you create an embedding vector for the chunk_text before upserting:
# For demo, let's assume you have a function get_embedding(text) -> vector

def get_embedding(text: str) -> list[float]:
    # Placeholder: replace with your embedding model call
    # e.g., OpenAI embedding API or local embedding model
    return [0.0] * 1536  # example dummy vector of size 1536

embedding_vector = get_embedding(chunk_text)

# Upsert into Pinecone
index.upsert([
    {
        "id": "endpoint:/create-user",
        "values": embedding_vector,
        "metadata": {
            "method": "POST",
            "auth_required": True,
            "depends_on": ["/get-roles"],
            "text": chunk_text
        }
    }
])

print("Chunk for /create-user endpoint uploaded to Pinecone!")
