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

@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/")
    return render_template("student_dashboard.html", email=session["email"])

@app.route("/staff")
def staff_dashboard():
    if session.get("role") != "staff":
        return redirect("/")
    return render_template("staff_dashboard.html", email=session["email"])

@app.route("/partner")
def partner_dashboard():
    if session.get("role") != "partner":
        return redirect("/")
    return render_template("partner_dashboard.html", email=session["email"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
