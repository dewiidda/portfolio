import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px 
import plotly.io as pio
from models import db, Student, Grade 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://edu_data.db'
app.config['SECRET_KEY'] = 'rahasia'
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            for _, row in df.iterrows:
                student = Student.query.filter_by(name=row['name'], class_name=row['class']).first()
                if not student:
                    student = Student(name=row['name'], class_name=row['class'])
                    db.session.add(student)
                    db.session.flush()
                grade = Grade(
                    student_id=student.id,
                    subject=row['subject'],
                    score=row['score'],
                    semester=row.get('semester','Ganjil'),
                    academic_year=row.get('academic_year', '2025/2026')
                )
                db.session.add(grade)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    grades = Grade.query.all()
    data = []
    for g in grades:
        data.append({
            'student': g.student.name,
            'class': g.student.class_name,
            'subject': g.subject,
            'score': g.score
        })
    df = pd.DataFrame(data)
    if df.empty:
        return "Belum ada data"
    
    class_avg = df.groupby(['class','subject'])['score'].mean().reset_index()
    fig = px.bar(class_avg, x='class',y='score', color='subject',
                 barmode='group', title='Rata-rata nilai perkelas dan mata pelajaran')
    chart_html = pio.to_html(fig, full_html=False)
    
    student_avg = df.groupby('student')['score'].mean().reset_index()
    student_avg['risk'] = student_avg['score'].apply(lambda x: 'Beresiko' if x < 70 else 'Aman')
    risk_fig = px.pie(student_avg, names='risk', title='Proporsi siswa beresiko (<70)')
    risk_html = pio.to_html(risk_fig, full_html=False)
    
    return render_template('dashboard.html',
                           chart=chart_html,
                           risk_chart=risk_html,
                           table=student_avg.to_dict('records'))
if __name__ == '__main__':
    app.run(debug=True)