# app/services/embedder.py

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# Load API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
print(f"OpenAI API Key loaded? {'Yes' if openai_api_key else 'No'}")

# Initialize embedding model
embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

def embed_resume(text):
    print("➡️ Starting embed_resume function")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])
    print(f"🧩 Split text into {len(docs)} chunk(s)")

    try:
        print("🧪 Creating FAISS in-memory vector store...")
        vectordb = FAISS.from_documents(
            documents=docs,
            embedding=embedding_model
        )
        print("✅ Created FAISS vector store")
    except Exception as e:
        print(f"❌ FAISS failure: {e}")
        raise

    return vectordb
