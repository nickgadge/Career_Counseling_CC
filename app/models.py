# app/models.py
from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    top_category = db.Column(db.String(50))
    answers = db.Column(db.Text)  # store answers as stringified dict

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(150))
    student_class = db.Column(db.String(50))
    top_category = db.Column(db.String(50))
    answers = db.Column(db.Text)

