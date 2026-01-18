# 🚀 AI-Powered Smart Placement Platform

## 💡 The Problem
College placement cells manually review hundreds of PDF resumes to match students with job drives. This is slow, error-prone, and inefficient.

## 🤖 The Solution
An AI-powered platform that:
1.  **Parses Resumes:** Uses **Google Gemini 1.5 Pro** to read PDF resumes.
2.  **Extracts Data:** Automatically pulls Skills, GPA, and Experience.
3.  **Smart Matching:** Instantly matches students to companies (e.g., "Tesla requires Python") based on their extracted skills.

## 🛠️ Tech Stack
* **Frontend:** HTML, CSS, JavaScript (Hosted on Firebase)
* **Backend:** Python, Flask (Tunneled via Ngrok)
* **AI Engine:** Google Gemini API
* **Database:** Firebase Firestore (Real-time)

## 📸 How It Works
1.  Admin posts a Job Drive (e.g., "SpaceX").
2.  Student uploads a PDF Resume.
3.  AI scans the resume -> Extracts "Python, DSA".
4.  System updates the dashboard with matching jobs instantly.

---
*Built for the Hackathon 2026*
