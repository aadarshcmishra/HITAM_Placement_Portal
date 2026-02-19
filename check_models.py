
import os
from dotenv import load_dotenv

load_dotenv() # This loads the .env file
import google.generativeai as genai


genai.configure(api_key="AIzaSyDssYdT_a2mJh7TJm-H5CO5bY8koYdJiZg")

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")
