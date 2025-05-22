# 🤖 AI-Powered API Automation Code Generator

## 💡 Idea Summary

Build an AI agent that generates Python-based API automation test code using contextual understanding of API endpoints, payloads, and schema documentation. The goal is to automate the process of writing test scripts by leveraging a cloud-based GenAI model and vector database.

---

## 🚀 What This Project Does

- ✅ Accepts API endpoint and prompt as input
- 🧠 Retrieves relevant context (e.g., schema, payloads, test guidelines) from vector DB
- 🪄 Feeds enriched prompt to a GenAI model (like OpenAI GPT-4)
- 🧾 Outputs ready-to-run Python `.py` test files using `requests` or `pytest`
- 💾 Embeds all reference files (schemas, docs, samples) into a cloud vector DB

---

## 📦 Tech Stack

| Component      | Tool/Service          |
|----------------|---------------------  |
| LLM            | OpenAI GPT-4 (API)    |
| Vector DB      | Pinecone / chromaDB   |
| Embedding      | OpenAI Embeddings     |
| Runtime        | Python 3.10+          |
| Dev Environment| VS Code               |

---

## 🗂️ Project Structure

