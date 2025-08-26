# app/__init__.py
import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "8329798794"

    # ---------------- Database Config ----------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, "career.db")          # DB will always live in app/career.db
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # ---------------- Import Blueprints ----------------
    from app.routes.main import main_bp
    from app.routes.students import students_bp
    from app.routes.parents import parents_bp
    from app.routes.admin import admin_bp

    # ---------------- Register Blueprints ----------------
    app.register_blueprint(main_bp)                     # old routes
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(parents_bp, url_prefix="/parents")
    app.register_blueprint(admin_bp, url_prefix="/admin")  # admin routes

    # ---------------- Root Redirect ----------------
    @app.route("/")
    def home():
        return redirect(url_for("admin.dashboard"))

    # ---------------- DB Setup ----------------
    with app.app_context():
        db.create_all()

    return app
