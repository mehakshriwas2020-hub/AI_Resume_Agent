from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
import tempfile

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening Project Running"
    }


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    text = ""

    with pdfplumber.open(temp_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return {
        "filename": file.filename,
        "resume_text": text[:1000]
    }


def calculate_ats(resume_text, jd_text):

    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched_words = resume_words.intersection(jd_words)

    missing_skills = list(jd_words - resume_words)

    score = (len(matched_words) / len(jd_words)) * 100

    return round(score, 2), missing_skills


@app.post("/ats_score")
def ats_score(
    resume_text: str = Form(...),
    jd_text: str = Form(...)
):

    score, missing_skills = calculate_ats(
        resume_text,
        jd_text
    )

    return {
        "ATS Score": score,
        "Missing Skills": missing_skills
    }
@app.post("/interview_questions")
def interview_questions(resume_text: str = Form(...)):

    questions = []

    text = resume_text.lower()

    if "python" in text:
        questions.append("What are Python decorators?")

    if "sql" in text:
        questions.append("What is the difference between INNER JOIN and LEFT JOIN?")

    if "machine learning" in text:
        questions.append("What is overfitting in Machine Learning?")

    if "fastapi" in text:
        questions.append("Why would you choose FastAPI over Flask?")

    if "power bi" in text:
        questions.append("What are the advantages of Power BI dashboards?")

    return {
        "Interview Questions": questions
    }
@app.post("/extract_skills")
def extract_skills(resume_text: str = Form(...)):

    skills_db = [
        "python",
        "sql",
        "java",
        "c",
        "machine learning",
        "fastapi",
        "power bi",
        "pandas",
        "numpy",
        "scikit-learn",
        "git",
        "github",
        "mysql",
        "data analytics"
    ]

    found_skills = []

    text = resume_text.lower()

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return {
        "Extracted Skills": found_skills
    }
@app.post("/analyze_resume")
def analyze_resume(
    resume_text: str = Form(...),
    jd_text: str = Form(...)
):

    skills_db = [
        "python", "sql", "java", "c", "machine learning",
        "fastapi", "power bi", "pandas", "numpy",
        "scikit-learn", "git", "github", "mysql",
        "data analytics", "docker", "aws"
    ]

    text = resume_text.lower()

    # Skill Extraction
    extracted_skills = []

    for skill in skills_db:
        if skill in text:
            extracted_skills.append(skill)

    # ATS Score
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched_words = resume_words.intersection(jd_words)

    if len(jd_words) == 0:
        score = 0
    else:
        score = (len(matched_words) / len(jd_words)) * 100

    missing_skills = list(jd_words - resume_words)

    # Resume Strength
    if len(extracted_skills) >= 8:
        strength = "Strong"
    elif len(extracted_skills) >= 5:
        strength = "Average"
    else:
        strength = "Weak"

    # Interview Questions
    questions = []

    if "python" in text:
        questions.append("Explain Python decorators.")

    if "sql" in text:
        questions.append("Difference between INNER JOIN and LEFT JOIN?")

    if "machine learning" in text:
        questions.append("What is overfitting?")

    if "fastapi" in text:
        questions.append("Why use FastAPI?")

    if "power bi" in text:
        questions.append("How do Power BI dashboards help business users?")

    return {
        "ATS Score": round(score, 2),
        "Resume Strength": strength,
        "Extracted Skills": extracted_skills,
        "Missing Skills": missing_skills,
        "Interview Questions": questions
    }