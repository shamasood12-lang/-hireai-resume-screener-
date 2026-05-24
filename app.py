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

# -----------------------------------
# CUSTOM DARK THEME
# -----------------------------------
st.markdown("""
    <style>

    .stApp {
        background-color: #0f1117;
        color: white;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #00ffd5;
    }

    .stButton>button {
        background-color: #00ffd5;
        color: black;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
    }

    .stTextInput>div>div>input,
    .stTextArea textarea {
        background-color: #262730;
        color: white;
        border-radius: 10px;
    }

    .stFileUploader {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
    }

    .css-1d391kg {
        background-color: #161a28;
    }

    </style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------
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
# SINGLE RESUME ANALYSIS
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
        extracted = page.extract_text()

        if extracted:
            resume_text += extracted

    st.success("✅ Resume uploaded successfully")


job_description = st.text_area("Enter Job Description")


# -----------------------------------
# SINGLE ANALYSIS BUTTON
# -----------------------------------
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

        st.markdown("## 📊 Match Result")

        col1, col2, col3 = st.columns(3)

        # -----------------------------------
        # CARD 1
        # -----------------------------------
        with col1:
            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:20px;
                border-radius:15px;
                text-align:center;
            ">
                <h3 style='color:#38bdf8;'>Keyword</h3>
                <h1 style='color:white;'>{score:.2f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        # -----------------------------------
        # CARD 2
        # -----------------------------------
        with col2:
            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:20px;
                border-radius:15px;
                text-align:center;
            ">
                <h3 style='color:#a78bfa;'>ML Score</h3>
                <h1 style='color:white;'>{ml_score:.2f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        # -----------------------------------
        # CARD 3
        # -----------------------------------
        with col3:
            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:20px;
                border-radius:15px;
                text-align:center;
            ">
                <h3 style='color:#34d399;'>Final</h3>
                <h1 style='color:white;'>{final_score:.2f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        st.progress(int(final_score))

        # -----------------------------------
        # MATCHED SKILLS
        # -----------------------------------
        st.markdown("### ✅ Matched Skills")

        if matched:
            st.write(", ".join(matched))
        else:
            st.write("No matched skills")

        # -----------------------------------
        # MISSING SKILLS
        # -----------------------------------
        st.markdown("### ❌ Missing Skills")

        if missing:
            st.write(", ".join(missing))
        else:
            st.write("No missing skills")

        # -----------------------------------
        # RESULT CATEGORY
        # -----------------------------------
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


# -----------------------------------
# ANALYZE ALL BUTTON
# -----------------------------------
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
                    extracted = page.extract_text()

                    if extracted:
                        text += extracted

            # -----------------------------------
            # DOCX HANDLING
            # -----------------------------------
            elif file_name.endswith(".docx"):

                temp_path = f"temp_{file_name}"

                with open(temp_path, "wb") as f:
                    f.write(uploaded_resume.getbuffer())

                text = extract_text_from_docx(temp_path)

                if os.path.exists(temp_path):
                    os.remove(temp_path)

            # -----------------------------------
            # MATCHING
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

        # -----------------------------------
        # SORT RESULTS
        # -----------------------------------
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

        # -----------------------------------
        # CARD 1
        # -----------------------------------
        with col1:
            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:20px;
                border-radius:15px;
                text-align:center;
            ">
                <h3 style='color:#38bdf8;'>Keyword</h3>
                <h1 style='color:white;'>{score:.2f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        # -----------------------------------
        # CARD 2
        # -----------------------------------
        with col2:
            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:20px;
                border-radius:15px;
                text-align:center;
            ">
                <h3 style='color:#a78bfa;'>ML</h3>
                <h1 style='color:white;'>{ml_score:.2f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        # -----------------------------------
        # CARD 3
        # -----------------------------------
        with col3:
            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:20px;
                border-radius:15px;
                text-align:center;
            ">
                <h3 style='color:#34d399;'>Final</h3>
                <h1 style='color:white;'>{final_score:.2f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        st.progress(int(final_score))

        # -----------------------------------
        # IMPROVEMENT SUGGESTION
        # -----------------------------------
        if missing:
            st.info(f"💡 Improve by learning: {', '.join(missing)}")

        # -----------------------------------
        # RESULT CATEGORY
        # -----------------------------------
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