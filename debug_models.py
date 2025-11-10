# debug_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("CRITICAL ERROR: No API key found in .env file")
else:
    genai.configure(api_key=api_key)
    print(f"Key found (starts with: {api_key[:4]}...). Asking Google for available models...\n")
    try:
        found_any = False
        for m in genai.list_models():
            # We only care about models that can generate text
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ AVAILABLE: {m.name}")
                found_any = True

        if not found_any:
            print("❌ WARNING: Connection successful, but no text-generation models were listed for this key.")

    except Exception as e:
        print(f"🚨 CONNECTION ERROR: {e}")