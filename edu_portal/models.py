from flask_sqlalchemy import SQLAlchemy
from database import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(20))
    grades = db.relationship('Grade', backref='student', lazy=True)
    
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.Foreign_key('student.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(10))
    academy_year = db.Column(db.String(9))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)