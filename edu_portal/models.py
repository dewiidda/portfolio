from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(20))
    grades = db.relationship('Grade', backref='student', lazy=True)
    
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(20))
    academic_year = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)