from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = mysql.connector.connect(
    host="65.0.101.41",
    user="ubuntu",
    password="Ubuntu@123",
    database="newdb"
)

@app.route('/')
def login_redirect():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = user[1]
            return redirect(url_for('add_student'))
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        conn.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        student_class = int(request.form['student_class'])
        tamilmarks = int(request.form['tamilmarks'])
        englishmarks = int(request.form['englishmarks'])
        sciencemarks = int(request.form['sciencemarks'])
        mathsmarks = int(request.form['mathsmarks'])
        socialmarks = int(request.form['socialmarks'])
        address = request.form['address']

        cursor = conn.cursor()

        query = "INSERT INTO students(name, age, student_class, tamilmarks, englishmarks, sciencemarks, mathsmarks, socialmarks, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, age, student_class, tamilmarks, englishmarks, sciencemarks, mathsmarks, socialmarks, address)
        cursor.execute(query, values)

        conn.commit()
        cursor.close()

        return 'Student added successfully'
    else:
        return render_template('add_student.html')


@app.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        student_class = int(request.form['student_class'])
        tamilmarks = int(request.form['tamilmarks'])
        englishmarks = int(request.form['englishmarks'])
        sciencemarks = int(request.form['sciencemarks'])
        mathsmarks = int(request.form['mathsmarks'])
        socialmarks = int(request.form['socialmarks'])
        address = request.form['address']

        cursor = conn.cursor()

        query = "UPDATE students SET name=%s, age=%s, student_class=%s, tamilmarks=%s, englishmarks=%s, sciencemarks=%s, mathsmarks=%s, socialmarks=%s, address=%s WHERE id=%s"
        values = (name, age, student_class, tamilmarks, englishmarks, sciencemarks, mathsmarks, socialmarks, address, student_id)
        cursor.execute(query, values)

        conn.commit()
        cursor.close()

        return redirect(url_for('view_students'))

    else:
        cursor = conn.cursor()
        query = "SELECT * FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()
        cursor.close()

        return render_template('update_student.html', student_id=student_id, student=student)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    # if 'username' not in session:
    #     return redirect(url_for('login'))

    cursor = conn.cursor()

    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()

    cursor.close()

    return redirect(url_for('view_students'))

@app.route('/view_students')
def view_students():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor()
    query = "SELECT * FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    cursor.close()

    return render_template('view_students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
