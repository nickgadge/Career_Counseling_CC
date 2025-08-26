# app/routes/parents.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
import io, json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app import db
from app.models import Student, Parent

# ✅ Blueprint variable
parents_bp = Blueprint('parents', __name__, template_folder='../../templates')

# Sample 50 questions structure
PARENT_QUESTIONS = [
    {"id": i+1, "category": cat, "question": f"How can you help your child in {cat}?", "type": "likert"}
    for i, cat in enumerate(
        ["logic", "arts", "science", "social", "commerce"] * 10
    )
]

CATEGORY_LABELS = {
    "logic": {"en": "Logical Thinking", "mr": "तार्किक विचार"},
    "arts": {"en": "Arts", "mr": "कला"},
    "science": {"en": "Science", "mr": "विज्ञान"},
    "social": {"en": "Social", "mr": "सामाजिक"},
    "commerce": {"en": "Commerce", "mr": "व्यापार"}
}

FIELD_MAP = {
    "logic": {"en": ["Problem Solving", "Critical Thinking"], "mr": ["समस्या सोडवणे", "संकटमुक्त विचार"]},
    "arts": {"en": ["Drawing", "Music"], "mr": ["चित्रकला", "संगीत"]},
    "science": {"en": ["Experiments", "Research"], "mr": ["प्रयोग", "संशोधन"]},
    "social": {"en": ["Teamwork", "Leadership"], "mr": ["संघकार्य", "नेतृत्व"]},
    "commerce": {"en": ["Accounting", "Business"], "mr": ["लेखाशास्त्र", "व्यवसाय"]}
}

# -------------------- Routes --------------------

@parents_bp.route("/")
def parents_home():
    return render_template("parents_home.html")  # Collect parent/student info

@parents_bp.route("/details_submit", methods=["POST"])
def parents_details_submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    student_name = request.form.get("student_name", "").strip()
    student_class = request.form.get("student_class", "").strip()

    if not email:
        email = "parents@gmail.com"
    if not name or not email or not phone or not student_name or not student_class:
        flash("Please fill all details / सर्व माहिती भरा", "error")
        return redirect(url_for("parents.parents_home"))

    session["parent_info"] = {
        "name": name,
        "email": email,
        "phone": phone,
        "student_name": student_name,
        "student_class": student_class
    }

    return redirect(url_for("parents.parents_questions"))

@parents_bp.route("/questions")
def parents_questions():
    return render_template("parents_questions.html", questions=PARENT_QUESTIONS, category_labels=CATEGORY_LABELS)

@parents_bp.route("/submit", methods=["POST"])
def parents_submit():
    parent_info = session.get("parent_info")
    if not parent_info:
        flash("Please fill your details first / कृपया माहिती भरा", "error")
        return redirect(url_for("parents.parents_home"))

    scores = {cat: 0 for cat in CATEGORY_LABELS.keys()}
    count = {cat: 0 for cat in CATEGORY_LABELS.keys()}

    for q in PARENT_QUESTIONS:
        qid = str(q["id"])
        val = request.form.get(f"q{qid}")
        if val is None:
            flash("Please answer all questions / सर्व प्रश्नांची उत्तरे द्या", "error")
            return redirect(url_for("parents.parents_questions"))
        try:
            val = int(val)
        except ValueError:
            val = 0
        scores[q["category"]] += val
        count[q["category"]] += 1

    percent = {}
    for cat in scores:
        max_score = count[cat] * 5 if count[cat] else 1
        percent[cat] = round((scores[cat]/max_score)*100, 2)

    top_list = sorted(percent.items(), key=lambda x: x[1], reverse=True)[:3]
    recommendations = []
    for cat, pct in top_list:
        recommendations.append({
            "cat_key": cat,
            "cat_en": CATEGORY_LABELS[cat]["en"],
            "cat_mr": CATEGORY_LABELS[cat]["mr"],
            "pct": pct,
            "fields_en": FIELD_MAP[cat]["en"],
            "fields_mr": FIELD_MAP[cat]["mr"]
        })

    session["parent_result"] = {
        "info": parent_info,
        "percent": percent,
        "recommendations": recommendations
    }

    # -------------------- SAVE TO DATABASE --------------------
    new_parent = Parent(
        name=parent_info['name'],
        email=parent_info['email'],
        phone=parent_info['phone'],
        student_name=parent_info['student_name'],
        student_class=parent_info['student_class'],
        top_category=", ".join([rec['cat_en'] for rec in recommendations]),
        answers=json.dumps({rec['cat_key']: rec['pct'] for rec in recommendations})
    )
    db.session.add(new_parent)
    db.session.commit()
    # -----------------------------------------------------------

    return render_template("parents_result.html",
                           info=parent_info,
                           percent=percent,
                           recommendations=recommendations,
                           category_labels=CATEGORY_LABELS)

# -------------------- PDF report --------------------
@parents_bp.route("/report/pdf")
def parents_report_pdf():
    data = session.get("parent_result")
    if not data:
        flash("No result found / परिणाम नाही. Complete the questionnaire first / सर्व प्रश्नावली भरा", "error")
        return redirect(url_for("parents.parents_home"))

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    info = data["info"]
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, y, "Parents Guidance Report")
    y -= 30
    p.setFont("Helvetica", 11)
    p.drawString(40, y, f"Parent: {info['name']}")
    y -= 16
    p.drawString(40, y, f"Email: {info['email']}")
    y -= 16
    p.drawString(40, y, f"Phone: {info['phone']}")
    y -= 16
    p.drawString(40, y, f"Student: {info['student_name']} ({info['student_class']})")
    y -= 24

    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Category Scores:")
    y -= 16
    p.setFont("Helvetica", 11)
    for cat, pct in data["percent"].items():
        p.drawString(50, y, f"- {CATEGORY_LABELS[cat]['en']} ({CATEGORY_LABELS[cat]['mr']}): {pct}%")
        y -= 14

    y -= 8
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Top Recommendations:")
    y -= 16
    p.setFont("Helvetica", 11)
    for rec in data["recommendations"]:
        p.drawString(50, y, f"* {rec['cat_en']} ({rec['cat_mr']}) - {rec['pct']}%")
        y -= 14
        p.drawString(64, y, "EN: " + ", ".join(rec["fields_en"]))
        y -= 14
        p.drawString(64, y, "MR: " + ", ".join(rec["fields_mr"]))
        y -= 18
        if y < 80:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 11)

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="parents_report.pdf",
                     mimetype="application/pdf")
