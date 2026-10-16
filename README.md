# AI Quiz Maker — Turn Study Material into Practice Questions

> **Choose a topic. Set the difficulty. Practice with an AI-generated quiz.**

AI Quiz Maker is a small generative AI study app that turns a topic or study material into a multiple-choice quiz with an answer key and brief explanations.

## 🚀 Live Demo

**Try the app:** [quiz-maker-genai-w22q.onrender.com](https://quiz-maker-genai-w22q.onrender.com)

## 📂 GitHub Repository

[github.com/sahityadhiman/quiz-maker-genai](https://github.com/sahityadhiman/quiz-maker-genai)

---

## 💡 Problem

Students often need quick ways to check what they understand, but writing useful practice questions and answer explanations takes time.

### Core Question

**Can a student turn a topic or their own study material into a quiz they can use for practice?**

## 🎯 Our Solution

Choose a topic or paste source material, select the difficulty and number of questions, then ask Gemini to create a four-option quiz with an answer key. Detailed source material is used as the basis for the questions; a short topic can be expanded with general knowledge.

## 🔄 Quiz Workflow

1. Enter a topic or paste study material.
2. Choose a difficulty: Beginner, Intermediate, or Advanced.
3. Select between 3 and 10 questions.
4. Generate a quiz with four options per question.
5. Review the answer key and one-sentence explanations.
6. Download the quiz as a Markdown file.

## ✨ Key Features

### 📝 Adjustable Quiz Length
Generate 3–10 multiple-choice questions.

### 🎚️ Three Difficulty Levels
Choose Beginner, Intermediate, or Advanced.

### 📖 Source-Aware Generation
When detailed study material is provided, the prompt asks Gemini to base questions on that material. For a short topic, it asks Gemini to use standard knowledge.

### ✅ Answer Key and Explanations
The generated Markdown includes the correct answer and a short explanation for every question.

### ⬇️ Downloadable Result
Download the quiz as `study_quiz.md` for editing or later practice.

### 🔐 Server-Managed Gemini Access
The app reads `GEMINI_API_KEY` from its private host environment. Visitors never enter or see an API key in the app.

## 🧪 Current Prototype

The deployed prototype demonstrates AI-assisted quiz creation in a single Streamlit page. It generates text-based questions and provides a Markdown download; it does not grade submitted answers or track student progress.

## 🛠️ Technology Stack

- **Python** — application logic
- **Streamlit** — interactive web interface
- **Google Gemini** — quiz and explanation generation
- **google-genai** — Gemini Python SDK
- **Render** — public web hosting

## 🏗️ Architecture

~~~~text
Student
  │
  ├── Topic or study material
  ├── Question count
  └── Difficulty
          │
          ▼
Streamlit app (app.py)
          │
          ▼
Google GenAI SDK
          │
          ▼
Gemini model
          │
          ▼
Questions + options + answer key
          │
          ▼
Markdown preview and download
~~~~

## 🚀 Run Locally

### Requirements

- Python 3.10 or later
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Windows PowerShell

~~~~powershell
git clone https://github.com/sahityadhiman/quiz-maker-genai.git
cd quiz-maker-genai
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
streamlit run app.py
~~~~

### macOS or Linux

~~~~bash
git clone https://github.com/sahityadhiman/quiz-maker-genai.git
cd quiz-maker-genai
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
streamlit run app.py
~~~~

Set `GEMINI_API_KEY` in your local environment before starting the app. The app intentionally has no API-key entry field. Never commit a real API key to GitHub.

## ⚙️ Configuration

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `GEMINI_API_KEY` | Yes | — | Gemini API key, set in Render's private environment or your local shell. All visitors to the public app share the configured key's quota. |
| `GEMINI_MODEL` | No | `gemini-3.8-flash` | Gemini model name passed to the SDK. |
| `GEMINI_FALLBACK_MODEL` | No | `gemini-3.6-flash` | Tried automatically if the primary model returns a temporary overload or rate-limit error. |

## ☁️ Deploy on Render

This repository includes a Render Blueprint in `render.yaml`. Create a Blueprint in Render and connect this GitHub repository; Render reads the Blueprint to install the pinned dependencies and start Streamlit.

The public demo is deployed on Render’s free web service with `GEMINI_API_KEY` stored as a private environment variable. Visitors can generate quizzes without entering a key. All visitors share the app owner's Gemini quota. Render free services can sleep while idle, so the first visit after inactivity may take about a minute to load.

## 🔒 Privacy and Limitations

- The topic or study material is sent to Google Gemini when a quiz is generated.
- The public app sends quiz prompts to Google Gemini using the server-managed key. All visitors share its quota; the key itself is not exposed in the page or repository.
- Local runs also require `GEMINI_API_KEY` to be supplied through the shell environment; the app does not accept keys in the UI.
- AI-generated questions and explanations can be wrong or ambiguous. Review the answer key before using a quiz for an exam or assignment.
- Do not paste confidential, personal, or sensitive information into the public demo.
- This prototype generates and downloads quizzes; it does not provide accounts, scoring, or persistent history.
