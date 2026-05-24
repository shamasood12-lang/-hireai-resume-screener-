import os
from extractor import extract_text_from_docx
from matcher import get_match_score

# 👇 CHANGE THIS if your folder name is different
folder_path = "resumes"

job_description = """
Looking for Python Developer with Django, REST APIs, Docker, AWS
"""

results = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".docx") or file.endswith(".DOCX"):
            path = os.path.join(root, file)

            print(f"Processing: {file}")  # debug

            text = extract_text_from_docx(path)

            score, matched, missing, resume_skills, required_skills = get_match_score(text, job_description)

            results.append((file, score, matched, missing))


# sort by score
results.sort(key=lambda x: x[1], reverse=True)

print("\n=== TOP RESULTS ===\n")

for file, score, matched, missing in results[:10]:
    print(f"{file} --> {score}%")
    print(f"Matched: {matched}")
    print(f"Missing: {missing}")
    print("-" * 40)


# extra summary (for your sir 🔥)
if results:
    avg_score = sum(r[1] for r in results) / len(results)
    print(f"\nAverage Score: {round(avg_score,2)}%")
    print(f"Total Resumes Tested: {len(results)}")
else:
    print("No resumes found.")