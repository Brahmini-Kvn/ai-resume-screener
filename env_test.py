import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Access the key
api_key = os.getenv("OPENAI_API_KEY")

# Print result
if api_key:
    print("✅ OpenAI API Key loaded successfully!")
    print(f"Key starts with: {api_key[:8]}...")
else:
    print("❌ Failed to load OpenAI API Key.")
