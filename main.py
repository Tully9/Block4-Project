import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection details from the .env file
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SSLMODE = os.getenv("DB_SSLMODE")

# Establish connection to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode=DB_SSLMODE
    )
    return conn

# Create Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Necessary for flashing messages

# Home route - Display data
@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_table;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', rows=rows)

# Add new record - Route
@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    age = request.form['age']
    
    if name and age:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO test_table (name, age) VALUES (%s, %s);", (name, age))
        conn.commit()
        cur.close()
        conn.close()
        flash(f'Record for {name} added successfully!', 'success')
    else:
        flash('Please provide both name and age!', 'error')
    
    return redirect(url_for('home'))

# Update existing record - Route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_record(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        new_name = request.form['name']
        new_age = request.form['age']
        
        if new_name and new_age:
            cur.execute("UPDATE test_table SET name=%s, age=%s WHERE id=%s;", (new_name, new_age, id))
            conn.commit()
            flash(f'Record {id} updated successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please provide both name and age!', 'error')
    
    cur.execute("SELECT * FROM test_table WHERE id=%s;", (id,))
    record = cur.fetchone()
    cur.close()
    conn.close()
    
    return render_template('update.html', record=record)

# Delete record - Route
@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM test_table WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash(f'Record {id} deleted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
