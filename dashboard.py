import streamlit as st
import os
import tempfile
import shutil
import pandas as pd
import re
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText

from app.services.resume_indexer import embed_resumes_from_folder
from app.services.searcher import search_similar_resumes
from app.services.evaluator import evaluate_resume

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("🧠 AI Resume Screener")

def send_email_notification(candidate_name, score):
    message = MIMEText(f"{candidate_name} scored {score}/10 in your AI screening.")
    message["Subject"] = f"📬 High-scoring candidate: {candidate_name}"
    message["From"] = "your@email.com"
    message["To"] = "recruiter@email.com"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your@email.com", "your_password")
            server.send_message(message)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

job_description = st.text_area("Paste the Job Description", height=200)

uploaded_files = st.file_uploader(
    "Upload Resumes (.pdf, .docx, .txt)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

score_threshold = st.slider("📊 Minimum Score to Display", min_value=1, max_value=10, value=7)

if st.button("⚙️ Process Resumes") and job_description and uploaded_files:
    if os.path.exists("vectorstore_ui"):
        shutil.rmtree("vectorstore_ui")

    with tempfile.TemporaryDirectory() as tmp_dir:

        for file in uploaded_files:
            with open(os.path.join(tmp_dir, file.name), "wb") as f:
                f.write(file.read())

        with st.spinner("🔎 Embedding and matching resumes..."):
            embed_resumes_from_folder(tmp_dir, save_path="vectorstore_ui", use_chunking=True)
            matches = search_similar_resumes(job_description, db_path="vectorstore_ui", k=10, return_results=True)

        st.subheader("🧠 GPT Evaluation of Top Matches")
        evaluated_data = []

        job_keywords = set(re.findall(r"[A-Za-z]{3,}", job_description.lower()))

        grouped_docs = defaultdict(list)
        for doc in matches:
            key = doc.metadata.get("source", "unknown")
            grouped_docs[key].append(doc)

        for source, chunks in grouped_docs.items():
            full_text = "\n".join([chunk.page_content for chunk in chunks])

            # Improved name extraction
            first_lines = full_text.strip().splitlines()[:10]
            name = None
            for line in first_lines:
                words = line.strip().split()
                if 1 < len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
                    name = line.strip()
                    break

            if not name:
                name = os.path.basename(source).split('.')[0].split('-')[0].strip().title()

            with st.spinner(f"Evaluating {name} with GPT..."):
                result = evaluate_resume(full_text, job_description)

            try:
                lines = result.split("\n")
                score = int([l for l in lines if l.startswith("Score:")][0].split(":")[1].split("/")[0].strip())
                summary = [l for l in lines if l.startswith("Summary:")][0].replace("Summary:", "").strip()
                fit = [l for l in lines if l.startswith("Fit:")][0].replace("Fit:", "").strip()
            except Exception as e:
                score, summary, fit = None, result, "Unknown"

            if score is not None and score < score_threshold:
                continue

            # Keyword match percentage
            resume_keywords = set(re.findall(r"[A-Za-z]{3,}", full_text.lower()))
            match_count = len(job_keywords & resume_keywords)
            match_percent = round((match_count / len(job_keywords)) * 100, 1) if job_keywords else 0

            # Send email alert if high score
            if score >= 8:
                send_email_notification(name, score)

            star_rating = "⭐" * round(score / 2) + "✩" * (5 - round(score / 2))
            st.markdown(f"### 👤 {name}")
            st.markdown(f"**Score:** {score}/10  &nbsp;&nbsp;&nbsp; {star_rating}")
            st.code(result, language="markdown")

            evaluated_data.append({
                "name": name,
                "score": score,
                "fit": fit,
                "summary": summary,
                "match %": f"{match_percent}%"
            })

        if evaluated_data:
            df = pd.DataFrame(evaluated_data)
            st.markdown("### 📊 Final Candidate Table")
            st.dataframe(df.sort_values(by="score", ascending=False), use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="evaluated_resumes.csv",
                mime="text/csv"
            )

