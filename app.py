import streamlit as st
import pandas as pd
import PyPDF2
import os

from matcher import get_match_score
from ml_model import calculate_similarity
from extractor import extract_text_from_docx


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="HireAI",
    layout="centered"
)

st.title("HireAI - Resume Screening System")
st.subheader("AI-powered resume and job matching")


# -----------------------------------
# SESSION STATE
# -----------------------------------
if "results" not in st.session_state:
    st.session_state.results = []

if "shortlisted" not in st.session_state:
    st.session_state.shortlisted = []


# -----------------------------------
# SINGLE RESUME MODE
# -----------------------------------
st.markdown("## 📄 Single Resume Analysis")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = ""

if uploaded_file:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    st.success("✅ Resume uploaded successfully")


job_description = st.text_area("Enter Job Description")


if st.button("Analyze Match"):

    if resume_text and job_description:

        score, matched, missing, resume_skills, required_skills = get_match_score(
            resume_text,
            job_description
        )

        ml_score = calculate_similarity(
            " ".join(resume_skills),
            " ".join(required_skills)
        )

        final_score = (score * 0.6) + (ml_score * 0.4)

        st.subheader("📊 Match Result")

        col1, col2, col3 = st.columns(3)

        col1.metric("Keyword", f"{score:.2f}%")
        col2.metric("ML Score", f"{ml_score:.2f}%")
        col3.metric("Final", f"{final_score:.2f}%")

        st.progress(int(final_score))

        st.markdown("### ✅ Matched Skills")
        st.write(", ".join(matched) if matched else "No matched skills")

        st.markdown("### ❌ Missing Skills")
        st.write(", ".join(missing) if missing else "No missing skills")

        if final_score >= 80:
            st.success("🔥 Strong Match")

        elif final_score >= 50:
            st.warning("⚠️ Medium Match")

        else:
            st.error("❌ Weak Match")

    else:
        st.warning("Please upload resume and enter job description.")


# -----------------------------------
# RECRUITER MODE
# -----------------------------------
st.markdown("## 🔍 Recruiter Mode")

uploaded_resumes = st.file_uploader(
    "Upload Multiple Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if st.button("Analyze All Resumes"):

    results = []

    if not uploaded_resumes:
        st.error("❌ Please upload resumes first!")

    else:

        for uploaded_resume in uploaded_resumes:

            file_name = uploaded_resume.name
            text = ""

            # -----------------------------------
            # PDF HANDLING
            # -----------------------------------
            if file_name.endswith(".pdf"):

                pdf_reader = PyPDF2.PdfReader(uploaded_resume)

                for page in pdf_reader.pages:
                    text += page.extract_text()

            # -----------------------------------
            # DOCX HANDLING
            # -----------------------------------
            elif file_name.endswith(".docx"):

                temp_path = f"temp_{file_name}"

                with open(temp_path, "wb") as f:
                    f.write(uploaded_resume.getbuffer())

                text = extract_text_from_docx(temp_path)

                # optional cleanup
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            # -----------------------------------
            # MATCH SCORING
            # -----------------------------------
            score, matched, missing, resume_skills, required_skills = get_match_score(
                text,
                job_description
            )

            if resume_skills and required_skills:

                ml_score = calculate_similarity(
                    " ".join(resume_skills),
                    " ".join(required_skills)
                )

            else:
                ml_score = 0

            final_score = (score * 0.6) + (ml_score * 0.4)

            results.append({
                "file": file_name,
                "score": score,
                "ml_score": ml_score,
                "final_score": final_score,
                "missing": missing
            })

        results.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        st.session_state.results = results


# -----------------------------------
# DISPLAY RESULTS
# -----------------------------------
if st.session_state.results:

    st.markdown("## 📊 Top Candidates")

    for i, res in enumerate(st.session_state.results[:10]):

        file = res["file"]
        score = res["score"]
        ml_score = res["ml_score"]
        final_score = res["final_score"]
        missing = res["missing"]

        st.markdown(f"### #{i+1} - {file}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Keyword", f"{score:.2f}%")
        col2.metric("ML", f"{ml_score:.2f}%")
        col3.metric("Final", f"{final_score:.2f}%")

        st.progress(int(final_score))

        if missing:
            st.info(f"💡 Improve by learning: {', '.join(missing)}")

        if final_score >= 80:
            st.success("🔥 Strong Match")

        elif final_score >= 50:
            st.warning("⚠️ Medium Match")

        else:
            st.error("❌ Weak Match")

        # -----------------------------------
        # SHORTLIST BUTTON
        # -----------------------------------
        if st.button(f"⭐ Shortlist {file}", key=file):

            candidate_data = {
                "Name": file,
                "Keyword Score": score,
                "ML Score": ml_score,
                "Final Score": final_score
            }

            if candidate_data not in st.session_state.shortlisted:
                st.session_state.shortlisted.append(candidate_data)

            st.success(f"{file} shortlisted!")

        st.markdown("---")


# -----------------------------------
# SHORTLIST DISPLAY
# -----------------------------------
st.markdown("## ⭐ Shortlisted Candidates")

if st.session_state.shortlisted:

    df = pd.DataFrame(st.session_state.shortlisted)

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Shortlist (CSV)",
        data=csv,
        file_name="shortlisted_candidates.csv",
        mime="text/csv"
    )

else:
    st.info("No candidates shortlisted yet.")