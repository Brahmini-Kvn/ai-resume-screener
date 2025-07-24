# 🧠 AI Resume Screener

An AI-powered resume screening tool that uses **OpenAI GPT-4**, **LangChain**, and **FAISS** to automatically evaluate and rank candidate resumes based on a given job description.

Ideal for **recruiters**, **hiring managers**, and **technical teams** looking to streamline their hiring process.

---

## 🚀 Live Demo

🌐 **Streamlit App**: [Launch Here](https://ai-resume-screener.streamlit.app)  
📤 Upload `.pdf`, `.docx`, or `.txt` resumes  
📝 Paste a job description  
⚡ Get GPT-powered rankings, summaries, and scores instantly

---

## 📸 Features

- ✅ GPT-4 powered evaluation (Score /10, Summary, Fit)
- ✅ Intelligent name extraction from resume text
- ✅ Resume chunking for improved semantic matching
- ✅ FAISS vector similarity search via LangChain
- ✅ Keyword match percentage from job description
- ✅ Recruiter-facing Streamlit dashboard with:
  - Visual score filtering
  - Star-based ranking
  - CSV export of results

---

## 🛠️ Tech Stack

- 🧠 OpenAI GPT-4 (via `langchain-openai`)  
- 🧱 LangChain for text chunking & embeddings  
- 🗂️ FAISS for similarity search  
- 🌐 Streamlit for dashboard UI  
- 🧾 Unstructured for PDF/DOCX/TXT parsing  
- 📦 Python, Pandas, Python-dotenv  

---

## 📦 Installation

```bash
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener
python -m venv venv
venv\\Scripts\\activate  # On Windows
pip install -r requirements.txt
streamlit run dashboard.py
