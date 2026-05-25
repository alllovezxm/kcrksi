
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'students.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL UNIQUE,
            class_name TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        class_name = request.form['class_name']
        phone = request.form['phone']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, student_id, class_name, phone) VALUES (?, ?, ?, ?)',
                     (name, student_id, class_name, phone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/&lt;int:id&gt;', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        class_name = request.form['class_name']
        phone = request.form['phone']
        
        cursor.execute('UPDATE students SET name=?, student_id=?, class_name=?, phone=? WHERE id=?',
                     (name, student_id, class_name, phone, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/delete/&lt;int:id&gt;')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

