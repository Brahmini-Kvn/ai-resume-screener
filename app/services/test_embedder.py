# app/services/test_embedder.py

print("🚀 test_embedder.py script started")

# Add root folder to sys.path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

try:
    from app.services.embedder import embed_resume
    print("✅ Imported embed_resume successfully.")
except Exception as e:
    print(f"❌ Failed to import embed_resume: {e}")
    sys.exit(1)

if __name__ == "__main__":
    try:
        sample_text = "This is a sample resume text to embed."
        print("📨 Calling embed_resume...")
        vectordb = embed_resume(sample_text)
        print("🏁 Embedding process finished successfully.")
    except Exception as e:
        print(f"❌ Error during embedding: {e}")
