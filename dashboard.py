import streamlit as st
import os
import tempfile
import shutil
import pandas as pd
import re

from app.services.resume_indexer import embed_resumes_from_folder
from app.services.searcher import search_similar_resumes
from app.services.evaluator import evaluate_resume

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("🧠 AI Resume Screener")

job_description = st.text_area("Paste the Job Description", height=200)

uploaded_files = st.file_uploader(
    "Upload Resumes (.pdf, .docx, .txt)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

score_threshold = st.slider("📊 Minimum Score to Display", min_value=1, max_value=10, value=7)

# ✅ Helper: Clean unsafe filenames (spaces, symbols, etc.)
def clean_filename(name):
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", name)

if st.button("⚙️ Process Resumes") and job_description and uploaded_files:
    # 💣 Clean up any old vectorstore
    if os.path.exists("vectorstore_ui"):
        shutil.rmtree("vectorstore_ui")

    with tempfile.TemporaryDirectory() as tmp_dir:
        # ✅ Save uploaded resumes with clean names
        for file in uploaded_files:
            safe_name = clean_filename(file.name)
            save_path = os.path.join(tmp_dir, safe_name)
            with open(save_path, "wb") as f:
                f.write(file.read())

        # 🔎 Embed and search
        with st.spinner("🔎 Embedding and matching resumes..."):
            embed_resumes_from_folder(tmp_dir, save_path="vectorstore_ui", use_chunking=True)
            matches = search_similar_resumes(job_description, db_path="vectorstore_ui", k=10, return_results=True)

        st.subheader("🧠 GPT Evaluation of Top Matches")
        evaluated_data = []

        for i, doc in enumerate(matches, 1):
            raw_name = doc.metadata.get("source", f"Candidate #{i}").split("/")[-1]
            name_guess = re.findall(r"[A-Z][a-z]+\s+[A-Z][a-z]+", doc.page_content[:300])
            name = name_guess[0] if name_guess else raw_name.replace(".pdf", "").replace(".docx", "")

            with st.spinner(f"Evaluating {name} with GPT..."):
                result = evaluate_resume(doc.page_content, job_description)

            try:
                lines = result.split("\n")
                score = int([l for l in lines if l.startswith("Score:")][0].split(":")[1].split("/")[0].strip())
                summary = [l for l in lines if l.startswith("Summary:")][0].replace("Summary:", "").strip()
                fit = [l for l in lines if l.startswith("Fit:")][0].replace("Fit:", "").strip()
            except Exception as e:
                score, summary, fit = None, result, "Unknown"

            if score is not None and score < score_threshold:
                continue

            star_rating = "⭐" * round(score / 2) + "✩" * (5 - round(score / 2))
            st.markdown(f"### 👤 {name}")
            st.markdown(f"**Score:** {score}/10  &nbsp;&nbsp;&nbsp; {star_rating}")
            st.code(result, language="markdown")

            evaluated_data.append({
                "name": name,
                "score": score,
                "fit": fit,
                "summary": summary
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
