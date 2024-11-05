from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

db_config = {
    'host': 'database',
    'user': 'admin',
    'password': 'admin',
    'database': 'attendance_db'
}

@app.route('/store_student', methods=['POST'])
def store_student():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    date = datetime.now().strftime('%Y-%m-%d')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, date) VALUES (%s, %s, %s)", (name, age, date))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Student added successfully'})

@app.route('/get_students', methods=['GET'])
def get_students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, age, date FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(students)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
