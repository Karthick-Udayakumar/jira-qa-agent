# 🧪 QA Test Case Generator

AI-powered QA agent that fetches Jira user stories and generates
Positive, Negative, BVA and Edge test cases using Groq LLM.

## Tech Stack
- Jira REST API v3
- Groq · llama-3.3-70b
- Python 3.14 · Streamlit

## Setup
1. Clone the repo
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Create `.env` with your keys (see `.env.example`)
6. Run: `streamlit run app.py`

## .env Setup