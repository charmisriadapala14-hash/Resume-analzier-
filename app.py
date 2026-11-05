import streamlit as st
import PyPDF2
import re
from collections import Counter

st.set_page_config(
page_title="AI Resume Analyzer",
page_icon="📄",
layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and analyze your skills.")

st.sidebar.header("Job Description")

job_description = st.sidebar.text_area(
"Enter Job Description",
placeholder="Paste the job description here..."
)

uploaded_file = st.file_uploader(
"Upload Your Resume (PDF)",
type=["pdf"]
)

def extract_text(pdf_file):
reader = PyPDF2.PdfReader(pdf_file)
text = ""

for page in reader.pages:
    text += page.extract_text() or ""

return text

def extract_email(text):
emails = re.findall(
r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}',
text
)
return emails[0] if emails else "Not found"

def extract_phone(text):
phones = re.findall(
r'+?\d[\d\s()-]{8,}\d',
text
)
return phones[0] if phones else "Not found"

skills_list = [
"Python", "Java", "C", "C++", "SQL",
"HTML", "CSS", "JavaScript",
"Machine Learning", "Deep Learning",
"Artificial Intelligence", "RAG",
"LangChain", "Streamlit", "React",
"Node.js", "Flask", "Django",
"MongoDB", "MySQL", "Git", "GitHub",
"Data Analysis", "Excel", "Power BI"
]

def find_skills(text):
found_skills = []

for skill in skills_list:
    if re.search(
        r'\b' + re.escape(skill) + r'\b',
        text,
        re.IGNORECASE
    ):
        found_skills.append(skill)

return found_skills

if uploaded_file is not None:

try:
    resume_text = extract_text(uploaded_file)

    if not resume_text.strip():
        st.error("No readable text found in this PDF.")
    else:
        st.success("Resume uploaded successfully!")

        st.subheader("📌 Resume Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Email:**", extract_email(resume_text))

        with col2:
            st.write("**Phone:**", extract_phone(resume_text))

        resume_skills = find_skills(resume_text)

        st.subheader("💻 Skills Identified")

        if resume_skills:
            st.write(", ".join(resume_skills))
        else:
            st.info("No matching skills identified.")

        if job_description.strip():

            job_skills = find_skills(job_description)

            matched = [
                skill for skill in resume_skills
                if skill.lower() in
                [s.lower() for s in job_skills]
            ]

            missing = [
                skill for skill in job_skills
                if skill.lower() not in
                [s.lower() for s in resume_skills]
            ]

            st.subheader("📊 Job Description Analysis")

            if job_skills:
                score = round(
                    len(matched) / len(job_skills) * 100
                )
            else:
                score = 0

            st.metric("Skill Match Score", f"{score}%")

            st.write("**Matching Skills:**")
            st.write(", ".join(matched) if matched else "None")

            st.write("**Skills to Improve:**")
            st.write(", ".join(missing) if missing else "None")

        with st.expander("View Extracted Resume Text"):
            st.write(resume_text)

except Exception as e:
    st.error(f"Error processing resume: {e}")
