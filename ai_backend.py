# ... imports ...

app = Flask(__name__)
CORS(app)

# 1. HANDLE FIREBASE KEY (Works on Cloud AND Laptop)
# On Render, we will upload this file securely.
if not os.path.exists("serviceAccountKey.json"):
    print("❌ Error: serviceAccountKey.json not found!")
else:
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

# 2. HANDLE GEMINI KEY (Works on Cloud AND Laptop)
# Check Environment Variable first (Cloud), then fallback to hardcoded (Laptop)
api_key = os.getenv("GOOGLE_API_KEY") 
if not api_key:
    api_key = "AIzaSy..." # Keep your hardcoded key here for local testing

genai.configure(api_key=api_key)

# ... rest of your code ...



import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# ==========================================
# 1. SETUP
# ==========================================

# Initialize Flask App
app = Flask(__name__)

# ENABLE CORS (This fixes the permission error)
CORS(app)

# Load Environment Variables (for API Key)
load_dotenv()

# A. Connect to Firebase
if not os.path.exists("serviceAccountKey.json"):
    print("❌ ERROR: serviceAccountKey.json is missing!")
    exit(1)

cred = credentials.Certificate("serviceAccountKey.json")
# Check if app is already initialized to prevent errors on restart
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# B. Connect to Gemini AI
# Get Key from .env file (Secure)
api_key = "AIzaSyDssYdT_a2mJh7TJm-H5CO5bY8koYdJiZg"

if not api_key:
    # Fallback if .env fails (Paste key here only for hackathon emergency)
    api_key = "AIzaSyDssYdT_a2mJh7TJm-H5CO5bY8koYdJiZg"

genai.configure(api_key=api_key)

# We use the standard free model
model = genai.GenerativeModel('gemini-2.5-flash')

# Create folder for resumes
if not os.path.exists('local_resumes'):
    os.makedirs('local_resumes')

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def extract_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        return None

def analyze_with_gemini(text):
    prompt = f"""
    You are an AI recruiter. Extract data from this resume.
    
    CRITICAL INSTRUCTION: Return ONLY valid JSON. 
    Do not use Markdown formatting (no ```json or ```). 
    Do not include any intro text. Start with {{ and end with }}.

    Structure:
    {{
        "skills": ["Skill1", "Skill2"],
        "gpa": "8.5",
        "degree": "B.Tech"
    }}

    Resume Text:
    {text[:10000]} 
    """
    
    try:
        response = model.generate_content(prompt)
        
        # DEBUG: Print exactly what Gemini sent back
        # print(f"   📝 Gemini Raw Response: {response.text[:100]}...") 
        
        # Clean up any potential markdown just in case
        clean_json = response.text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json.replace("```json", "").replace("```", "")
        elif clean_json.startswith("```"):
            clean_json = clean_json.replace("```", "")
        
        return json.loads(clean_json)
        
    except Exception as e:
        print(f"❌ AI Analysis Failed: {e}")
        return None

# ==========================================
# 3. SERVER ROUTES
# ==========================================

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    print("\n📥 Request Received...")
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    user_id = request.form.get('user_id')
    
    if not user_id:
        return jsonify({"error": "No User ID provided"}), 400

    print(f"   👤 Processing User: {user_id}")

    # Save PDF
    file_path = os.path.join('local_resumes', f"{user_id}.pdf")
    file.save(file_path)
    
    # Read PDF
    text = extract_text(file_path)
    if not text:
        return jsonify({"error": "Could not read PDF text"}), 500

    # Analyze
    print("   🧠 Sending to Gemini...")
    ai_result = analyze_with_gemini(text)
    
    if ai_result:
        # Save to Firestore
        try:
            db.collection("students").document(user_id).set({
                "ai_analysis": ai_result,
                "updated_at": firestore.SERVER_TIMESTAMP
            }, merge=True)
            print("   ✅ Success! Saved to Database.")
            return jsonify({"message": "Success", "data": ai_result}), 200
        except Exception as e:
            print(f"❌ Database Error: {e}")
            return jsonify({"error": "Database save failed"}), 500
    else:
        return jsonify({"error": "AI returned no data"}), 500

if __name__ == '__main__':
    print("🚀 Server Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)")
    app.run(debug=True, port=5000)