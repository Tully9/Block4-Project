import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from dotenv import load_dotenv
import crud

# load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Home: dashboard
@app.route('/')
def home():
    stats = crud.get_overview_stats()
    return render_template('index.html', stats=stats)

# --- Companies ---
@app.route('/companies')
def list_companies():
    companies = crud.get_all_companies()
    return render_template('companies.html', companies=companies)

@app.route('/companies/add', methods=['GET','POST'])
def add_company():
    if request.method=='POST':
        data = {
            'name': request.form['name'],
            'logo_url': request.form['logo_url'],
            'description': request.form['description'],
            'tech_stack': request.form['tech_stack'],
            'location': request.form['location'],
            'salary': request.form['salary'],
            'work_block': request.form['work_block'],
            'positions_available': request.form['positions_available'],
            'requires_cv': bool(request.form.get('requires_cv'))
        }
        crud.create_company(data)
        flash("Company added", "success")
        return redirect(url_for('list_companies'))
    return render_template('company_form.html')

# --- Students ---
@app.route('/students')
def list_students():
    students = crud.get_all_students()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        data = {
            'student_id': request.form['student_id'],
            'name': request.form['name'],
            'year': request.form['year']
        }
        crud.create_student(data)
        flash("Student added", "success")
        return redirect(url_for('list_students'))
    return render_template('student_form.html')

# --- Upload Rankings CSV ---
@app.route('/rankings/upload', methods=['GET','POST'])
def upload_rankings():
    if request.method=='POST':
        file = request.files['csv_file']
        block = request.form['work_block']
        year = request.form['year']
        staff_id = request.form['staff_id']
        crud.process_rankings_csv(file, block, year, staff_id)
        flash("Rankings uploaded", "success")
        return redirect(url_for('home'))
    return render_template('upload_rankings.html')

# --- Schedule Interviews & Show Interviews ---
@app.route('/interviews')
def list_interviews():
    interviews = crud.get_interviews()
    return render_template('interviews.html', interviews=interviews)

@app.route('/interviews/schedule', methods=['POST'])
def schedule_interviews():
    round_num = int(request.form['round'])
    block = request.form['work_block']
    year  = int(request.form['year'])
    crud.schedule_round_interviews(round_num, block, year)
    flash(f"Round {round_num} interviews scheduled", "success")
    return redirect(url_for('list_interviews'))

# --- Upload CVs ---
@app.route('/cv/upload/<int:interview_id>', methods=['GET','POST'])
def upload_cv(interview_id):
    if request.method=='POST':
        cv = request.files['cv']
        crud.store_cv(interview_id, cv)
        flash("CV uploaded", "success")
        return redirect(url_for('list_interviews'))
    iv = crud.get_interview(interview_id)
    return render_template('upload_cv.html', interview=iv)

# --- Preferences & Matching ---
@app.route('/preferences/<role>', methods=['GET','POST'])
def preferences(role):
    # role='student' or 'company'
    if request.method=='POST':
        prefs = request.form.getlist('pref[]')  # a list of company_ids or student_ids
        round_num = int(request.form['round'])
        crud.store_preferences(role, request.form['entity_id'], prefs, round_num)
        flash("Preferences saved", "success")
        return redirect(url_for('home'))
    data = crud.get_pref_data(role)
    return render_template('preferences.html', role=role, data=data)

@app.route('/matches/run/<int:round_num>', methods=['POST'])
def run_round(round_num):
    crud.run_matching_round(round_num)
    flash(f"Matching round {round_num} completed", "success")
    return redirect(url_for('home'))

@app.route('/matches')
def show_matches():
    matches = crud.get_matches()
    return render_template('matches.html', matches=matches)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
