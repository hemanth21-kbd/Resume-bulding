from flask import Flask, render_template, request, redirect, make_response, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from xhtml2pdf import pisa
from io import BytesIO
import os
import json
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

# ---------------- Configuration ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resume.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

# Ensure the upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)

# ---------------- Database Model ----------------
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

    objective = db.Column(db.Text)
    skills = db.Column(db.Text)
    education = db.Column(db.Text)
    projects = db.Column(db.Text)

    certifications = db.Column(db.Text)
    achievements = db.Column(db.Text)
    languages = db.Column(db.Text)
    hobbies = db.Column(db.Text)


    photo = db.Column(db.String(200))
    template = db.Column(db.String(50), default="modern")

# Create database AFTER model definition
with app.app_context():
    db.create_all()

# ---------------- Dashboard ----------------
@app.route("/")
def home():
    # --- Change 2: Simplified query syntax with .isnot(None) ---
    total = Resume.query.count()
    
    photos = Resume.query.filter(
        Resume.photo.isnot(None), 
        Resume.photo != ""
    ).count()

    return render_template(
        "dashboard.html",
        total=total,
        photos=photos
    )

# ---------------- Create Resume ----------------
@app.route("/resume", methods=["GET", "POST"])
def resume():

    if request.method == "POST":

        photo = request.files.get("photo")
        filename = ""

        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        new_resume = Resume(
            name=request.form.get("name", ""),
            email=request.form.get("email", ""),
            phone=request.form.get("phone", ""),
            address=request.form.get("address", ""),
            objective=request.form.get("objective", ""),
            skills=request.form.get("skills", ""),
            education=request.form.get("education", ""),
            projects=request.form.get("projects", ""),
            certifications=request.form.get("certifications", ""),
            achievements=request.form.get("achievements", ""),
            languages=request.form.get("languages", ""),
            hobbies=request.form.get("hobbies", ""),
            photo=filename,
template=request.form.get("template", "modern")
        )

        db.session.add(new_resume)
        db.session.commit()

        return render_template(
    f"{new_resume.template}.html",
    resume=new_resume
)

    return render_template("resume.html")

# ---------------- View All ----------------
@app.route("/resumes")
def resumes():
    resumes = db.session.scalars(db.select(Resume)).all()
    return render_template("resumes.html", resumes=resumes)

# ---------------- Edit ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    resume = db.session.get(Resume, id)
    if not resume:
        return "Resume not found", 404

    if request.method == "POST":
        resume.name = request.form.get("name", "")
        resume.email = request.form.get("email", "")
        resume.phone = request.form.get("phone", "")
        resume.address = request.form.get("address", "")
        resume.objective = request.form.get("objective", "")
        resume.skills = request.form.get("skills", "")
        resume.education = request.form.get("education", "")
        resume.projects = request.form.get("projects", "")
        resume.certifications = request.form.get("certifications", "")
        resume.achievements = request.form.get("achievements", "")
        resume.languages = request.form.get("languages", "")
        resume.hobbies = request.form.get("hobbies", "")
       

        photo = request.files.get("photo")
        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            resume.photo = filename

        db.session.commit()
        return redirect(url_for("resumes"))

    return render_template("edit.html", resume=resume)

# ---------------- Delete ----------------
@app.route("/delete/<int:id>")
def delete(id):
    resume = db.session.get(Resume, id)
    if not resume:
        return "Resume not found", 404

    db.session.delete(resume)
    db.session.commit()
    return redirect(url_for("resumes"))

# ---------------- Search ----------------
@app.route("/search")
def search():
    keyword = request.args.get("name", "")
    resumes = db.session.scalars(
        db.select(Resume).where(Resume.name.contains(keyword))
    ).all()
    return render_template("resumes.html", resumes=resumes)

# ---------------- Download PDF ----------------
@app.route("/download/<int:id>")
def download(id):
    resume = db.session.get(Resume, id)
    if not resume:
        return "Resume not found", 404

    html = render_template(
        "pdf.html",
        resume=resume
    )

    pdf = BytesIO()
    
    # --- Change 3: PDF Error handling ---
    result = pisa.CreatePDF(html, dest=pdf)
    if result.err:
        return "Error generating PDF", 500

    response = make_response(pdf.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    
    safe_filename = secure_filename(f"{resume.name}_Resume.pdf")
    response.headers["Content-Disposition"] = f'attachment; filename="{safe_filename}"'

    return response

# ---------------- AI Resume Builder ----------------
@app.route("/ai-resume", methods=["GET", "POST"])
def ai_resume():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        job_title = request.form.get("job_title", "")
        experience = request.form.get("experience", "")
        template = request.form.get("template", "modern")
        api_key = app.config.get("OPENAI_API_KEY", "")

        if not name or not email:
            flash("Name and Email are required.", "danger")
            return redirect(url_for("ai_resume"))

        generated = generate_resume_content(api_key, name, job_title, experience)

        photo = request.files.get("photo")
        filename = ""
        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        new_resume = Resume(
            name=name,
            email=email,
            phone=phone,
            address=address,
            objective=generated.get("objective", ""),
            skills=generated.get("skills", ""),
            education=generated.get("education", ""),
            projects=generated.get("projects", ""),
            certifications=generated.get("certifications", ""),
            achievements=generated.get("achievements", ""),
            languages=generated.get("languages", ""),
            hobbies=generated.get("hobbies", ""),
            photo=filename,
            template=template,
        )

        db.session.add(new_resume)
        db.session.commit()

        return render_template(
            f"{new_resume.template}.html",
            resume=new_resume,
        )

    return render_template("ai_resume.html")


def generate_resume_content(api_key, name, job_title, experience):
    if not api_key:
        return fallback_resume_content(name, job_title, experience)

    try:
        import openai

        client = openai.OpenAI(api_key=api_key)
        prompt = f"""
        Generate a professional resume in JSON format for the following person.
        Return ONLY valid JSON, no markdown, no code fences, no extra text.

        Name: {name}
        Job Title / Target Role: {job_title}
        Experience / Background: {experience}

        JSON structure:
        {{
          "objective": "2-3 sentence career objective",
          "skills": "comma-separated list of relevant skills",
          "education": "highest qualification and details",
          "projects": "2-3 notable projects",
          "certifications": "relevant certifications (or empty string)",
          "achievements": "key achievements (or empty string)",
          "languages": "languages known",
          "hobbies": "hobbies and interests (or empty string)"
        }}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful resume assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=600,
        )

        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\n?", "", content)
            content = re.sub(r"\n?```$", "", content)
        return json.loads(content)
    except Exception:
        return fallback_resume_content(name, job_title, experience)


def fallback_resume_content(name, job_title, experience):
    return {
        "objective": f"Results-driven {job_title or 'professional'} with experience in {experience or 'the industry'}. Seeking to leverage skills and deliver value in a challenging role.",
        "skills": "Communication, Problem Solving, Teamwork, Time Management, Technical Skills",
        "education": "Bachelor's Degree in a relevant field.",
        "projects": "Multiple projects demonstrating strong analytical and technical abilities.",
        "certifications": "",
        "achievements": "",
        "languages": "English",
        "hobbies": "Reading, Technology, Sports",
    }


# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True)