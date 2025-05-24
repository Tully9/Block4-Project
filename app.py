from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE")
    )
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        input_email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM accounts WHERE student_email = %s OR staff_email = %s OR partner_email = %s", 
                    (input_email, input_email, input_email))
        account = cur.fetchone()
        cur.close()
        conn.close()

        if not account or account["password"] != password:
            error = "Invalid email or password"
        else:
            # Determine role
            if account["student_email"] == input_email:
                session["role"] = "student"
                session["email"] = account["student_email"]
                return redirect(url_for("student_dashboard"))
            elif account["staff_email"] == input_email:
                session["role"] = "staff"
                session["email"] = account["staff_email"]
                return redirect(url_for("staff_dashboard"))
            elif account["partner_email"] == input_email:
                session["role"] = "partner"
                session["email"] = account["partner_email"]
                return redirect(url_for("partner_dashboard"))

    return render_template("index.html", error=error)

@app.route('/student_dashboard')
def student_dashboard():
    student_id = session.get('student_id')  # Assume student_id is stored in session after login
    
    # Query to get the available job options
    conn = get_db_connection()
    cur = conn.cursor()

    # Query to get all companies with available positions for the student's year group
    cur.execute("""
        SELECT c.id, c.name, c.logo_url, c.description, c.tech_stack, c.location, c.salary, c.working_block, c.positions_available
        FROM companies c
        WHERE c.positions_available > 0
        AND (c.is_private = FALSE OR EXISTS (
            SELECT 1 FROM student_company_visibility scv
            WHERE scv.student_id = %s AND scv.company_id = c.id
        ))
    """, (student_id,))
    available_jobs = cur.fetchall()

    # Query to get matches for the student
    cur.execute("""
        SELECT m.company_id, c.name, m.match_type, m.match_date
        FROM matches m
        JOIN companies c ON m.company_id = c.id
        WHERE m.student_id = %s
    """, (student_id,))
    matched_jobs = cur.fetchall()

    # Query to get self-arranged jobs
    cur.execute("""
        SELECT c.id, c.name, sa.approved
        FROM self_arranged_jobs sa
        JOIN companies c ON sa.company_id = c.id
        WHERE sa.student_id = %s
    """, (student_id,))
    self_arranged_jobs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        'student_dashboard.html',
        available_jobs=available_jobs,
        matched_jobs=matched_jobs,
        self_arranged_jobs=self_arranged_jobs
    )

@app.route('/apply_for_job/<int:company_id>')
def apply_for_job(company_id):
    student_id = session.get('student_id')
    # Here you can handle CV upload or job application process
    return f"Student {student_id} applied for job {company_id}!"

@app.route('/submit_cv/<int:company_id>', methods=['POST'])
def submit_cv(company_id):
    student_id = session.get("student_id")  # Assume student_id is stored in session
    cv_file = request.files['cv_file']

    if cv_file and allowed_file(cv_file.filename):
        filename = secure_filename(cv_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv_file.save(filepath)

        # Insert CV submission into the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cv_submissions (student_id, company_id, round, cv_file_path)
            VALUES (%s, %s, 1, %s)  -- assuming round 1 for simplicity
        """, (student_id, company_id, filepath))
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('student_dashboard'))
    else:
        return "Invalid file type. Only PDF or DOCX files are allowed."

@app.route("/staff")
def staff_dashboard():
    if session.get("role") != "staff":
        return redirect("/")
    return render_template("staff_dashboard.html", email=session["email"])

@app.route('/partner')
def partner_dashboard():
    email = session.get("email")  # Assume email is stored in session for login
    return render_template('partner_dashboard.html', email=email)

@app.route('/submit_job_request')
def submit_job_request():
    return render_template('job_request_form.html')

@app.route('/process_job_request', methods=['POST'])
def process_job_request():
    # Get form data
    name = request.form['name']
    logo_url = request.form['logo_url']
    description = request.form['description']
    tech_stack = request.form['tech_stack']
    location = request.form['location']
    salary = request.form['salary']
    working_block = request.form['working_block']
    positions_available = request.form['positions_available']
    requires_cv = request.form.get('requires_cv') == 'on'
    is_charity = request.form.get('is_charity') == 'on'
    is_private = request.form.get('is_private') == 'on'

    # Insert data into the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO companies (name, logo_url, description, tech_stack, location, salary, 
                               working_block, positions_available, requires_cv, is_charity, is_private)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, logo_url, description, tech_stack, location, salary, working_block, 
          positions_available, requires_cv, is_charity, is_private))
    conn.commit()
    cur.close()
    conn.close()

    # Redirect to the partner dashboard
    return redirect(url_for('partner_dashboard'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
