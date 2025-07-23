# 🧠 AI Resume Screener

A full-stack Streamlit app that uses **OpenAI GPT-4 + LangChain + FAISS** to intelligently screen, score, and summarize resumes based on a given job description.

> Ideal for recruiters, hiring managers, or tech teams looking to save time evaluating technical candidates.

---

## 🚀 Demo

🌐 [Live App on Streamlit Cloud](#) *(coming soon)*  
📂 Upload .pdf, .docx, or .txt resumes  
🎯 Paste a job description  
⚡ See ranked, GPT-evaluated results in seconds

---

## 📸 Features

✅ GPT-4 powered evaluation (Score /10, Summary, Fit)  
✅ Extracts candidate names from resume content  
✅ Chunked resume processing for better semantic matching  
✅ FAISS vector search via LangChain  
✅ Match % based on keyword overlap  
✅ Star ratings & filter by score  
✅ Download results as CSV  
✅ Ready for Streamlit Community Cloud deployment

---

## 🛠️ Tech Stack

- 🧠 **OpenAI GPT-4** for evaluation
- 🧱 **LangChain** for chunking + embeddings
- 🗂️ **FAISS** for similarity search
- 🌐 **Streamlit** for interactive UI
- 📄 **Unstructured** loader for DOCX/PDF parsing
- 🐍 **Python, pandas, dotenv**

---

## 📦 Installation

```bash
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener
python -m venv venv
venv\\Scripts\\activate   # On Windows
pip install -r requirements.txt
streamlit run dashboard.py
