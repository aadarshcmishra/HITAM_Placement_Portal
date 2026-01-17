import google.generativeai as genai


genai.configure(api_key="AIzaSyATMsYQKdrKN5Jn0EpM8FRwwKO3qj7RYyQ")

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")