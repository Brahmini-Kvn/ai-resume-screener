# app/services/resume_indexer.py

import os
from typing import Optional
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_unstructured import UnstructuredLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

def load_resume(filepath: str):
    try:
        if os.path.getsize(filepath) > 3_000_000 or "vivek" in filepath.lower():
            print(f"⚠️ Skipping potentially problematic file: {filepath}")
            return []

        print(f"📄 Loading file: {filepath}")
        docs = UnstructuredLoader(filepath).load()

        for doc in docs:
            doc.metadata["source"] = filepath  # ✅ Attach source for grouping

        return docs
    except Exception as e:
        print(f"❌ Failed to load {filepath}: {e}")
        return []

def embed_resumes_from_folder(
    folder_path: str,
    save_path: str = "vectorstore",
    use_chunking: bool = True,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
):
    all_docs = []

    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if not os.path.isfile(path):
            continue

        resume_docs = load_resume(path)
        if not resume_docs:
            continue

        if use_chunking:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", ".", " "]
            )
            chunks = splitter.split_documents(resume_docs)
            print(f"🔗 Chunked {filename} into {len(chunks)} parts")

            for chunk in chunks:
                chunk.metadata["source"] = path  # ✅ Reinforce metadata on each chunk

            all_docs.extend(chunks)
        else:
            print(f"📄 Using full document for: {filename}")
            all_docs.extend(resume_docs)

    if not all_docs:
        raise ValueError("No valid documents found to embed.")

    vectordb = FAISS.from_documents(all_docs, embedding_model)
    vectordb.save_local(save_path)
    print(f"✅ Embedded {len(all_docs)} docs (chunking: {'on' if use_chunking else 'off'})")
    return vectordb
