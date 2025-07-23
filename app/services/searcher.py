# app/services/searcher.py

from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

def search_similar_resumes(query: str, db_path: str = "vectorstore", k: int = 3, return_results: bool = False):
    vectordb = FAISS.load_local(
        db_path,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )
    results = vectordb.similarity_search(query, k=k)

    if return_results:
        return results

    print(f"\n🔍 Top {k} results for query: \"{query}\"\n")
    for i, doc in enumerate(results, 1):
        print(f"--- Result #{i} ---\n{doc.page_content}\n")
