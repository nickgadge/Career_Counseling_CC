# app/routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from app.data.questions import QUESTIONS, CATEGORY_LABELS, FIELD_MAP
import io, os, smtplib
from email.message import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app import db
from app.models import Student, Parent


STUDENT_DB = []  # <-- keep in-memory DB for admin panel
PARENT_DB = []

# ✅ Blueprint variable
students_bp = Blueprint('students', __name__, template_folder='../../templates')

EMOJI_MAP = {1: 1, 2: 3, 3: 4, 4: 5}  # 😞→1, 😐→3, 🙂→4, 😍→5

# Home route
@students_bp.route("/")
def students_home():
    return render_template("students.html",
                           questions=QUESTIONS,
                           category_labels=CATEGORY_LABELS)

# Form submission route
@students_bp.route("/submit", methods=["POST"])
def students_submit():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()

    if not name or not phone or not address:
        flash("Please fill your Name, Phone and Address. / कृपया नाव, फोन आणि पत्ता भरा.", "error")
        return redirect(url_for("students.students_home"))

    scores = {"logic": 0, "arts": 0, "science": 0, "social": 0, "commerce": 0}
    per_category_count = {"logic": 0, "arts": 0, "science": 0, "social": 0, "commerce": 0}

    q_index = {str(q["id"]): q for q in QUESTIONS}

    for qid, q in q_index.items():
        qtype = q.get("type", "likert")
        cat = q["category"]

        if qtype == "multi":
            selected = request.form.getlist(f"q{qid}[]")
            if not selected:
                flash("Please answer all questions. / कृपया सर्व प्रश्नांची उत्तरे द्या.", "error")
                return redirect(url_for("students.students_home"))
            max_opt = len(q.get("multi_options", [])) or 1
            val = round((len(selected) / max_opt) * 5)
            val = max(1, min(val, 5))
        else:
            raw = request.form.get(f"q{qid}")
            if raw is None:
                flash("Please answer all questions. / कृपया सर्व प्रश्नांची उत्तरे द्या.", "error")
                return redirect(url_for("students.students_home"))
            try:
                raw_val = int(raw)
            except ValueError:
                raw_val = 0

            if qtype == "emoji":
                val = EMOJI_MAP.get(raw_val, 3)
            elif qtype == "slider":
                val = round((raw_val / 10) * 4) + 1
                val = max(1, min(val, 5))
            else:
                val = max(1, min(raw_val, 5))

        scores[cat] += val
        per_category_count[cat] += 1

    percent = {}
    top_list = []
    for cat, total in scores.items():
        max_score = per_category_count[cat] * 5 if per_category_count[cat] else 1
        pct = round((total / max_score) * 100, 2)
        percent[cat] = pct
        top_list.append((cat, pct))

    top_list.sort(key=lambda x: x[1], reverse=True)
    top3 = top_list[:3]

    recommendations = []
    for cat, pct in top3:
        recommendations.append({
            "cat_key": cat,
            "cat_mr": CATEGORY_LABELS[cat]["mr"],
            "cat_en": CATEGORY_LABELS[cat]["en"],
            "pct": pct,
            "fields_en": FIELD_MAP[cat]["en"],
            "fields_mr": FIELD_MAP[cat]["mr"]
        })

    chart_labels = [CATEGORY_LABELS[c]["en"] for c in ["logic", "arts", "science", "social", "commerce"]]
    chart_data = [percent["logic"], percent["arts"], percent["science"], percent["social"], percent["commerce"]]

    session["last_result"] = {
        "name": name, "phone": phone, "address": address,
        "percent": percent, "recommendations": recommendations,
        "chart_labels": chart_labels, "chart_data": chart_data
    }

    # Save Student to DB
    student = Student(
        name=name,
        phone=phone,
        address=address,
        top_category=top3[0][0],  # store best category
    )
    db.session.add(student)
    db.session.commit()


    return render_template("result.html",
                           name=name, phone=phone, address=address,
                           percent=percent, chart_labels=chart_labels, chart_data=chart_data,
                           recommendations=recommendations, category_labels=CATEGORY_LABELS)

# PDF download route
@students_bp.route("/report/pdf")
def report_pdf():
    data = session.get("last_result")
    if not data:
        flash("No result found. Please complete the test first.", "error")
        return redirect(url_for("students.students_home"))

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, y, "Career Counseling - Student Report")
    y -= 30
    p.setFont("Helvetica", 11)
    p.drawString(40, y, f"Name: {data['name']}")
    y -= 16
    p.drawString(40, y, f"Phone: {data['phone']}")
    y -= 16
    p.drawString(40, y, f"Address: {data['address']}")
    y -= 24

    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Category Scores:")
    y -= 16
    p.setFont("Helvetica", 11)
    for cat in ["logic", "arts", "science", "social", "commerce"]:
        pct = data["percent"][cat]
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
                     download_name="student_report.pdf",
                     mimetype="application/pdf")

# Email PDF route
@students_bp.route("/email", methods=["POST"])
def email_report():
    parent_email = request.form.get("parent_email", "").strip()
    if not parent_email:
        flash("Enter parent email. / पालकांचा ईमेल भरा.", "error")
        return redirect(url_for("students.students_home"))

    data = session.get("last_result")
    if not data:
        flash("No result found. Please complete the test first.", "error")
        return redirect(url_for("students.students_home"))

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, y, "Career Counseling - Student Report")
    y -= 30
    p.setFont("Helvetica", 11)
    p.drawString(40, y, f"Name: {data['name']}")
    y -= 16
    p.drawString(40, y, f"Phone: {data['phone']}")
    y -= 16
    p.drawString(40, y, f"Address: {data['address']}")
    y -= 24
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Category Scores:")
    y -= 16
    p.setFont("Helvetica", 11)
    for cat in ["logic", "arts", "science", "social", "commerce"]:
        pct = data["percent"][cat]
        p.drawString(50, y, f"- {CATEGORY_LABELS[cat]['en']}: {pct}%")
        y -= 14
    p.showPage()
    p.save()
    pdf_bytes = buffer.getvalue()

    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")
    SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

    if not EMAIL_USER or not EMAIL_PASS:
        flash("Email not configured on server. Set EMAIL_USER and EMAIL_PASS env vars.", "error")
        return redirect(url_for("students.students_home"))

    try:
        msg = EmailMessage()
        msg["Subject"] = "Student Career Report"
        msg["From"] = EMAIL_USER
        msg["To"] = parent_email
        msg.set_content(
            f"Hello,\n\nAttached is the student career report for {data['name']}.\n\nRegards,\nCareer Counseling Platform"
        )
        msg.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename="student_report.pdf")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        flash("Email sent to parent successfully.", "success")
    except Exception as e:
        flash(f"Email failed: {e}", "error")

    return redirect(url_for("students.students_home"))
