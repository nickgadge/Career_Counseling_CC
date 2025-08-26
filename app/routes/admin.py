from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Student, Parent

admin_bp = Blueprint('admin', __name__)  # default template folder is app/templates

# -------------------- Dashboard --------------------
@admin_bp.route("/dashboard")
def dashboard():
    total_students = Student.query.count()
    total_parents = Parent.query.count()
    return render_template("dashboard.html",
                           total_students=total_students,
                           total_parents=total_parents)

# -------------------- Students List --------------------
@admin_bp.route("/users")
def students_list():
    students = Student.query.order_by(Student.id.desc()).all()
    return render_template("users.html", students=students)  # updated template name

# -------------------- Delete Student --------------------
@admin_bp.route("/users/delete/<int:student_id>")
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete student: {e}", "error")
    return redirect(url_for("admin.students_list"))

# -------------------- Parents List --------------------
@admin_bp.route("/parent")
def parents_list():
    parents = Parent.query.order_by(Parent.id.desc()).all()
    return render_template("parents.html", parents=parents)  # updated template name

# -------------------- Delete Parent --------------------
@admin_bp.route("/parent/delete/<int:parent_id>")
def delete_parent(parent_id):
    parent = Parent.query.get_or_404(parent_id)
    try:
        db.session.delete(parent)
        db.session.commit()
        flash("Parent deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete parent: {e}", "error")
    return redirect(url_for("admin.parents_list"))

