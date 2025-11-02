from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import init_db

app = Flask(__name__)
init_db()

# Home Page
@app.route('/')
def home():
    conn = sqlite3.connect('smart_health.db')
    c = conn.cursor()
    search = request.args.get('search')
    if search:
        c.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    return render_template('index.html', patients=patients)

# Add Patient
@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    condition = request.form['condition']
    contact = request.form['contact']

    conn = sqlite3.connect('smart_health.db')
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, age, gender, condition, contact) VALUES (?, ?, ?, ?, ?)",
              (name, age, gender, condition, contact))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# Delete Patient
@app.route('/delete/<int:id>')
def delete_patient(id):
    conn = sqlite3.connect('smart_health.db')
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# Edit Patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    conn = sqlite3.connect('smart_health.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        condition = request.form['condition']
        contact = request.form['contact']
        c.execute("UPDATE patients SET name=?, age=?, gender=?, condition=?, contact=? WHERE id=?",
                  (name, age, gender, condition, contact, id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    else:
        c.execute("SELECT * FROM patients WHERE id=?", (id,))
        patient = c.fetchone()
        conn.close()
        return render_template('edit.html', patient=patient)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
