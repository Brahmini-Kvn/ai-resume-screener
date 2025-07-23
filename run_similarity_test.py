import csv, json

evaluated_results = []

for i, doc in enumerate(results, 1):
    print(f"📄 Resume Match #{i}")
    evaluation = evaluate_resume(doc.page_content, job_description)
    print(evaluation)
    print("\n" + "-" * 80 + "\n")

    # Extract fields from GPT output
    try:
        lines = evaluation.split("\n")
        score = int([l for l in lines if l.startswith("Score:")][0].split(":")[1].split("/")[0].strip())
        summary = [l for l in lines if l.startswith("Summary:")][0].replace("Summary:", "").strip()
        fit = [l for l in lines if l.startswith("Fit:")][0].replace("Fit:", "").strip()
    except Exception as e:
        print(f"❌ Failed to parse GPT response: {e}")
        score, summary, fit = None, evaluation, "Unknown"

    evaluated_results.append({
        "resume_text": doc.page_content,
        "score": score,
        "summary": summary,
        "fit": fit
    })

# Save to CSV
with open("evaluated_resumes.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["score", "summary", "fit", "resume_text"])
    writer.writeheader()
    writer.writerows(evaluated_results)

# Save to JSON
with open("evaluated_resumes.json", "w", encoding="utf-8") as f:
    json.dump(evaluated_results, f, indent=2)

print("✅ Exported results to evaluated_resumes.csv and evaluated_resumes.json")
